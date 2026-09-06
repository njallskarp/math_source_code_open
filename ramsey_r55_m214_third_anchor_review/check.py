#!/usr/bin/env python3
"""Audit actual h3192 rows against physically decoded h3160 root systems."""
import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

N = 43
E = frozenset(range(2, 15))
C = frozenset(range(N)) - E
PAIRS = [None] + list(itertools.combinations(range(N), 2))
IDS = {p: i for i, p in enumerate(PAIRS) if p is not None}
SELECTORS = frozenset(range(13245, 13634))
BASE_ROWS = 1974689
BASE_SHA = "469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f"
SUFFIX_SHA = "a1a63de5c4bb005b468a8352963ec003b2696eb155c07c16f50b0e7b86bd8d7b"
STRONG_SHA = "a3838c52d9a4cdbc98e67caf137bf6b18e024e075e5e0c4331254dd66d4c3556"
OLD_HEADER = b"* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n"
NEW_HEADER = b"* #variable= 13633 #constraint= 2057998 #equal= 87 intsize= 64\n"
CELL_ORDER = ((1, 1), (1, 0), (0, 1), (0, 0))
CELL_NAME = dict(zip(CELL_ORDER, "HABO"))
FAMILIES = ("E8", "E77", "C8", "C77", "C77partition")


def need(condition, message):
    if not condition:
        raise ValueError(message)


def edge(a, b):
    need(a != b and 0 <= a < N and 0 <= b < N, "physical pair")
    return IDS[tuple(sorted((a, b)))]


E_STARS = {frozenset(edge(v, w) for w in E if w != v): v for v in range(N)}


def parse(raw):
    need(raw.endswith(b"\n"), "missing newline")
    parts = raw.split()
    need(len(parts) >= 5 and len(parts) % 2 == 1 and parts[-1] == b";", "row grammar")
    need(parts[-3] == b">=", "guard inequality")
    terms = {}
    for i in range(0, len(parts) - 3, 2):
        token, coefficient = parts[i + 1], int(parts[i])
        need(token.startswith(b"x") and token[1:].isdigit(), "variable spelling")
        variable = int(token[1:])
        need(1 <= variable <= 13633 and variable not in terms and coefficient != 0,
             "variable range/duplicate or zero coefficient")
        terms[variable] = coefficient
    return terms, int(parts[-2])


def deguard(row):
    terms, rhs = row
    selectors = set(terms) & SELECTORS
    need(len(selectors) == 1, "unique selector")
    selector = next(iter(selectors))
    physical = {v: a for v, a in terms.items() if v != selector}
    need(physical and all(v <= 903 for v in physical), "physical edges only")
    need(sum(min(a, 0) for a in physical.values()) >= rhs, "inactive guard restricts")
    return selector, (tuple(sorted(physical.items())), rhs - terms[selector])


def root_from(rows):
    """Recover cells and anomalous values from the actual active inequalities."""
    units, bounds = {}, defaultdict(dict)
    for terms, rhs in rows:
        signs = {a for _, a in terms}
        need(signs in ({1}, {-1}), "root signs")
        sign = next(iter(signs))
        variables = frozenset(v for v, _ in terms)
        if len(variables) == 1:
            v = next(iter(variables))
            need(rhs == (1 if sign == 1 else 0) and v not in units, "root unit")
            units[v] = int(sign == 1)
        else:
            need(sign not in bounds[variables], "duplicate root bound")
            bounds[variables][sign] = rhs * sign
    equalities = {}
    for variables, values in bounds.items():
        need(set(values) == {-1, 1} and values[-1] == values[1], "root equality")
        equalities[variables] = values[1]
    a = {E_STARS[vs]: value for vs, value in equalities.items() if vs in E_STARS}
    need(set(a) == set(range(N)) and a[0] == a[1] == 6, "complete a-values")
    anomalies = tuple(v for v in range(N) if a[v] != 6)
    need((len(anomalies) == 1 and a[anomalies[0]] == 8)
         or (len(anomalies) == 2 and all(a[v] == 7 for v in anomalies)), "anomaly values")
    need(set(anomalies) <= E or set(anomalies) <= C, "anomaly class")
    family = ("E" if anomalies[0] in E else "C") + ("8" if len(anomalies) == 1 else "77")
    anchor_edges = {i for i in range(1, 904) if PAIRS[i][0] < 2}
    need(anchor_edges <= units.keys() and units[edge(0, 1)] == 1, "anchor units")
    bits = {v: (units[edge(0, v)], units[edge(1, v)]) for v in range(2, N)}
    cells = {b: frozenset(v for v in bits if bits[v] == b) for b in CELL_ORDER}
    common = len(cells[1, 1])
    k = len(cells[1, 1] & E)
    need(9 <= common <= 13 and 0 <= k <= 6, "pair domain")
    extras = {vs: t for vs, t in equalities.items() if vs not in E_STARS}
    if extras:
        need(family == "C77", "partition family")
        p, q = anomalies
        expected = {frozenset((edge(v, p), edge(v, q))): 1 for v in C - {p, q}}
        need(extras == expected and units.get(edge(p, q)) == 0, "all partition conditions")
        need(set(units) == anchor_edges | {edge(p, q)}, "partition units")
        family = "C77partition"
    else:
        need(set(units) == anchor_edges, "ordinary units")
    pattern = "".join(CELL_NAME[b] for b in CELL_ORDER for v in anomalies if bits[v] == b)
    # This grouping is recovered from physical colors and a-values, not a producer layout.
    grouped = defaultdict(list)
    for v in range(2, N):
        grouped[(v in E, bits[v], a[v])].append(v)
    groups = tuple(tuple(g) for g in sorted(grouped.values(), key=lambda g: g[0]))
    pool = tuple(v for v in sorted(cells[1, 1] & C) if a[v] == 6)
    need(len(pool) >= 2 and pool in groups, "ordinary central-H pool")
    constraints = frozenset(rows)
    need(len(constraints) == len(rows), "duplicate active root row")
    return {"key": (family, common, k, pattern), "groups": groups, "pool": pool,
            "cells": cells, "constraints": constraints, "anomalies": anomalies}


def read_base(path):
    grouped = defaultdict(list)
    digest, strong = hashlib.sha256(), hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        header = stream.readline()
        need(header == OLD_HEADER, "base header")
        digest.update(header)
        strong.update(NEW_HEADER)
        size += len(header)
        line_count = 1
        for number, raw in enumerate(stream, 1):
            line_count += 1
            size += len(raw)
            digest.update(raw)
            strong.update(raw)
            # The globally reviewed block and one-hot row are identity-pinned,
            # not re-proved here. Decode every subsequent physical root row.
            if number > BASE_ROWS + 1:
                selector, active = deguard(parse(raw))
                grouped[selector].append(active)
    need(size == 172788992 and line_count == 2044422, "base dimensions")
    need(digest.hexdigest() == BASE_SHA, "base identity")
    need(set(grouped) == SELECTORS, "root selectors")
    roots = {s: root_from(grouped[s]) for s in sorted(grouped)}
    need(Counter(r["key"][0] for r in roots.values())
         == dict(zip(FAMILIES, (60, 85, 70, 104, 70))), "family coverage")
    need(len({r["key"] for r in roots.values()}) == 389, "distinct root keys")
    return roots, strong


def swap_constraints(constraints, left, right):
    mapping = list(range(N))
    mapping[left], mapping[right] = right, left
    def transport(variable):
        a, b = PAIRS[variable]
        return edge(mapping[a], mapping[b])
    return frozenset((tuple(sorted((transport(v), c) for v, c in terms)), rhs)
                     for terms, rhs in constraints)


def check_generator(root, left, right):
    # Equality of literal finite systems proves invariance under this generator.
    need(swap_constraints(root["constraints"], left, right) == root["constraints"],
         "root generator fails to preserve actual conditions")


def audit_generators(root):
    count = 0
    for group in root["groups"]:
        for left, right in zip(group, group[1:]):
            need((left in E) == (right in E), "global degree classes")
            check_generator(root, left, right)
            count += 1
    return count


def semantic_suffix(rows, root):
    """Decode row meanings and compare with the theorem, ignoring term order."""
    pool, cells = root["pool"], root["cells"]
    common = root["key"][1]
    common_endpoints = set(range(N))
    for terms, _ in rows:
        for variable, _ in terms:
            common_endpoints &= set(PAIRS[variable])
    need(common_endpoints == {min(pool)}, "canonical ordinary third anchor")
    w = next(iter(common_endpoints))
    expected = Counter()
    ordering = 0
    for group in root["groups"]:
        residual = [v for v in group if v != w]
        for left, right in zip(residual, residual[1:]):
            expected[(tuple(sorted(((edge(w, left), 1), (edge(w, right), -1)))), 0)] += 1
            ordering += 1
    h = cells[1, 1] - {w}
    for vertices, sign, bound in ((h, -1, -4),
                                  (h | cells[1, 0], -1, -12),
                                  (h | cells[0, 1], -1, -12)):
        expected[(tuple(sorted((edge(w, v), sign) for v in vertices)), bound)] += 1
    cuts = 3
    if common > 9:
        expected[(tuple(sorted((edge(w, v), 1) for v in h)), common - 9)] += 1
        cuts += 1
    need(Counter(rows) == expected, "missing, duplicate, or non-theorem active row")
    return w, ordering, cuts


def audit_suffix(parsed, roots):
    grouped = defaultdict(list)
    for row in parsed:
        selector, active = deguard(row)
        need(selector in roots, "unknown selector")
        grouped[selector].append(active)
    need(set(grouped) == set(roots), "complete suffix root cover")
    return {s: semantic_suffix(grouped[s], roots[s]) for s in sorted(roots)}


def controls(parsed, roots):
    count = 0
    def reject(call):
        nonlocal count
        try:
            call()
        except (ValueError, KeyError):
            count += 1
        else:
            raise ValueError("damaged control accepted")
    for raw in (b"+1 x1 +1 x1 -1 x13245 >= 0 ;\n",
                b"+0 x1 -1 x13245 >= 0 ;\n",
                b"+1 x13634 -1 x13245 >= 0 ;\n",
                b"+1 x1 -1 x13245 >= 0 ;",
                b"+1 x1 -1 x13245 = 0 ;\n"):
        reject(lambda raw=raw: parse(raw))
    for raw in (b"+1 x904 -1 x13245 >= 0 ;\n",
                b"+1 x1 -1 x13245 -1 x13246 >= 0 ;\n",
                b"+1 x1 -1 x2 -1 x13245 >= 0 ;\n"):
        reject(lambda raw=raw: deguard(parse(raw)))
    reject(lambda: audit_suffix(parsed[1:], roots))
    reject(lambda: audit_suffix(parsed + [parsed[0]], roots))
    terms, rhs = parsed[0]
    selector = next(iter(set(terms) & SELECTORS))
    modified = dict(terms)
    modified[selector + 1] = modified.pop(selector)
    reject(lambda: audit_suffix([(modified, rhs)] + parsed[1:], roots))
    # Keep the active inequality identical, but make its inactive guard restrictive.
    modified = dict(terms)
    modified[selector] += 1
    reject(lambda: audit_suffix([(modified, rhs + 1)] + parsed[1:], roots))
    modified = dict(terms)
    positive = next(v for v, c in modified.items() if c == 1 and v <= 903)
    modified[positive] = -1
    reject(lambda: audit_suffix([(modified, rhs)] + parsed[1:], roots))
    root = roots[selector]
    w = min(root["pool"])
    negative = next(v for v, c in terms.items() if v <= 903 and c == -1)
    endpoints = set(PAIRS[negative]) - {w}
    old_vertex = next(iter(endpoints))
    old_group = next(set(g) for g in root["groups"] if old_vertex in g)
    other = next(v for v in range(2, N) if v != w and v not in old_group
                 and edge(w, v) not in terms)
    modified = dict(terms)
    modified[edge(w, other)] = modified.pop(negative)
    reject(lambda: audit_suffix([(modified, rhs)] + parsed[1:], roots))
    # A transposition crossing refined cells is not an allowed generator.
    reject(lambda: check_generator(root, old_vertex, other))
    # Deleting one of an equality's two directions must not survive root decoding.
    root_rows = list(root["constraints"])
    location = next(i for i, (t, _) in enumerate(root_rows) if len(t) > 1)
    reject(lambda: root_from(root_rows[:location] + root_rows[location + 1:]))
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=Path)
    parser.add_argument("suffix", type=Path)
    args = parser.parse_args()
    roots, strong = read_base(args.base)
    raw = args.suffix.read_bytes()
    need(len(raw) == 612502 and hashlib.sha256(raw).hexdigest() == SUFFIX_SHA, "suffix identity")
    strong.update(raw)
    need(strong.hexdigest() == STRONG_SHA, "virtual full strengthened stream")
    parsed = [parse(line) for line in raw.splitlines(keepends=True)]
    decoded = audit_suffix(parsed, roots)
    generators = {s: audit_generators(root) for s, root in roots.items()}
    record = [(s, *roots[s]["key"], *decoded[s], len(roots[s]["pool"]), generators[s])
              for s in sorted(roots)]
    audit_hash = hashlib.sha256(json.dumps(record, separators=(",", ":")).encode()).hexdigest()
    result = {
        "roots": len(roots),
        "family_counts": [sum(r["key"][0] == f for r in roots.values()) for f in FAMILIES],
        "ordinary_third_anchor_pool_range": [min(len(r["pool"]) for r in roots.values()),
                                            max(len(r["pool"]) for r in roots.values())],
        "literal_root_generator_checks": sum(generators.values()),
        "inactive_guards_checked": len(parsed),
        "ordering_rows": sum(t[1] for t in decoded.values()),
        "structural_rows": sum(t[2] for t in decoded.values()),
        "root_semantic_audit_sha256": audit_hash,
        "base_sha256": BASE_SHA,
        "suffix_sha256": SUFFIX_SHA,
        "virtual_strengthened_sha256": strong.hexdigest(),
        "negative_controls_rejected": controls(parsed, roots),
        "incidence_orbit_census_recomputed": False,
        "sat_or_unsat_claimed": False,
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
