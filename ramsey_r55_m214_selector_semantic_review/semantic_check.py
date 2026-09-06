#!/usr/bin/env python3
"""Decode the complete h3160 OPB semantically; import no producer modules.

This checks an encoding, not satisfiability. All arithmetic is exact.
"""

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

N = 43
E = frozenset(range(2, 15))
C = frozenset(range(N)) - E
PAIRS = [None] + list(itertools.combinations(range(N), 2))
TRIPLES = list(itertools.combinations(range(N), 3))
EDGE_ID = {p: i for i, p in enumerate(PAIRS) if p is not None}
TRIANGLE_ID = {t: 904 + i for i, t in enumerate(TRIPLES)}
SELECTORS = frozenset(range(13245, 13634))
FAMILIES = ("E8", "E77", "C8", "C77", "C77partition")
BASE_ROWS = 1974689
FORMULA_ROWS = 2044421
FORMULA_SHA = "469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f"
BASE_SHA = "5f160c74a405726503649581080e3127d6a21c25b8fb59f6ffe72740dce600c4"
TAIL_SHA = "43da325c040c3cec73a0bdf6041f6e70f89b4a89fafb4d7d4b472279f970767a"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def edge(i, j):
    return EDGE_ID[tuple(sorted((i, j)))]


def parse(raw):
    """Strict OPB subset used by the pinned source, independent of term order."""
    need(raw.endswith(b"\n"), "missing newline")
    parts = raw.split()
    need(len(parts) >= 5 and len(parts) % 2 == 1
         and parts[-1] == b";", "row grammar")
    relation = parts[-3]
    need(relation in (b">=", b"="), "row relation")
    rhs = int(parts[-2])
    terms = {}
    for index in range(0, len(parts) - 3, 2):
        coefficient = int(parts[index])
        token = parts[index+1]
        need(token.startswith(b"x") and token[1:].isdigit(), "variable grammar")
        variable = int(token[1:])
        need(1 <= variable <= 13633 and variable not in terms, "variable range/duplicate")
        need(coefficient != 0 and abs(coefficient) < 2**63, "coefficient range")
        terms[variable] = coefficient
    need(abs(rhs) < 2**63, "rhs range")
    return terms, relation, rhs


def five_signature(row):
    terms, relation, rhs = row
    need(relation == b">=" and len(terms) == 10
         and all(i <= 903 for i in terms), "five-set row shape")
    values = set(terms.values())
    need((values, rhs) in (({1}, 1), ({-1}, -9)), "five-set signs/bound")
    vertices = sorted({v for i in terms for v in PAIRS[i]})
    need(len(vertices) == 5 and set(terms) == {
        edge(i, j) for i, j in itertools.combinations(vertices, 2)}, "complete five-set")
    # Colexicographic combinatorial rank; the producer emits lexicographic order.
    rank = sum(math.comb(v, k) for k, v in enumerate(vertices, 1))
    return rank, 1 if rhs == 1 else 2


def triangle_signature(row):
    terms, relation, rhs = row
    z_ids = [i for i in terms if 904 <= i <= 13244]
    need(relation == b">=" and len(z_ids) == 1
         and all(i <= 13244 for i in terms), "triangle row shape")
    z = z_ids[0]
    triangle = TRIPLES[z-904]
    sides = [edge(i, j) for i, j in itertools.combinations(triangle, 2)]
    if len(terms) == 2:
        remaining = set(terms) - {z}
        side = next(iter(remaining))
        need(side in sides and terms[z] == -1 and terms[side] == 1
             and rhs == 0, "triangle upper implication")
        return z-904, 1 << sides.index(side)
    need(len(terms) == 4 and set(terms) == {z, *sides}
         and terms[z] == 1 and all(terms[i] == -1 for i in sides)
         and rhs == -2, "triangle lower implication")
    return z-904, 8


def star_lookup(domain):
    if domain == "triangles":
        return {frozenset(i for t, i in TRIANGLE_ID.items() if v in t): v
                for v in range(N)}
    return {frozenset(edge(v, w) for w in domain if w != v): v for v in range(N)}


DEGREE_STARS = star_lookup(range(N))
TRIANGLE_STARS = star_lookup("triangles")
E_STARS = star_lookup(E)


def star_vertex(row, lookup, relation, target):
    terms, actual_relation, rhs = row
    variables = frozenset(terms)
    need(actual_relation == relation and set(terms.values()) == {1}
         and variables in lookup, "physical star")
    vertex = lookup[variables]
    need(rhs == target(vertex), "star target")
    return vertex


def one_hot(row):
    terms, relation, rhs = row
    need(frozenset(terms) == SELECTORS and set(terms.values()) == {1}
         and relation == b"=" and rhs == 1, "full Boolean one-hot")


def deguard(row):
    """Return the unique selector and its y=1 inequality; prove y=0 tautology."""
    terms, relation, rhs = row
    selectors = set(terms) & SELECTORS
    need(relation == b">=" and len(selectors) == 1, "single selector guard")
    selector = next(iter(selectors))
    physical = {i: c for i, c in terms.items() if i != selector}
    need(physical and all(i <= 903 for i in physical), "guard physical edges")
    # Exact minimum of a linear form on independent Boolean edge variables.
    need(sum(min(0, c) for c in physical.values()) >= rhs, "inactive guard restricts graph")
    return selector, (physical, relation, rhs - terms[selector])


def root_from_active(rows):
    """Decode, rather than generate, the meaning of one selector's actual rows."""
    units = {}
    bounds = defaultdict(dict)
    for terms, relation, rhs in rows:
        need(relation == b">=" and set(terms.values()) in ({1}, {-1}),
             "active row signs")
        sign = next(iter(terms.values()))
        if len(terms) == 1:
            variable = next(iter(terms))
            need(rhs == (1 if sign == 1 else 0) and variable not in units,
                 "active unit bound/duplicate")
            units[variable] = int(sign == 1)
        else:
            variables = frozenset(terms)
            need(sign not in bounds[variables], "duplicate active bound")
            bounds[variables][sign] = sign * rhs
    equalities = {}
    for variables, limits in bounds.items():
        need(set(limits) == {-1, 1} and limits[-1] == limits[1],
             "missing or unequal active equality bounds")
        equalities[variables] = limits[1]
    a = {}
    extra = {}
    for variables, target in equalities.items():
        if variables in E_STARS:
            a[E_STARS[variables]] = target
        else:
            extra[variables] = target
    need(set(a) == set(range(N)) and a[0] == a[1] == 6,
         "all 43 exact E-incidences and exact anchors")
    anomalies = sorted(v for v in range(N) if a[v] != 6)
    need((len(anomalies) == 1 and a[anomalies[0]] == 8)
         or (len(anomalies) == 2 and all(a[v] == 7 for v in anomalies)),
         "two-unit anomaly profile")
    need(all(v in E for v in anomalies) or all(v in C for v in anomalies),
         "intrinsic anomaly parity")
    anomaly_in_E = anomalies[0] in E
    family = ("E" if anomaly_in_E else "C") + ("8" if len(anomalies) == 1 else "77")
    anchor_ids = {i for i, p in enumerate(PAIRS) if p is not None and p[0] < 2}
    need(anchor_ids <= set(units) and len(anchor_ids) == 83 and units[edge(0, 1)] == 1,
         "complete red-adjacent anchor pair")
    bits_to_name = {(1, 1): "H", (1, 0): "A", (0, 1): "B", (0, 0): "O"}
    word = {v: bits_to_name[units[edge(0, v)], units[edge(1, v)]]
            for v in range(2, N)}
    cells = [[v for v in range(2, N) if (v in E) == exceptional and word[v] == name]
             for exceptional in (True, False) for name in "HABO"]
    need([v for cell in cells for v in cell] == list(range(2, N)), "canonical cell labels")
    e_sizes = [len(cell) for cell in cells[:4]]
    c_sizes = [len(cell) for cell in cells[4:]]
    need(e_sizes[0]+e_sizes[1] == e_sizes[0]+e_sizes[2] == 6
         and c_sizes[0]+c_sizes[1] == c_sizes[0]+c_sizes[2] == 14,
         "physical pair margins")
    common = e_sizes[0] + c_sizes[0]
    need(9 <= common <= 13, "codegree range")
    for cell in cells:
        actual = [v for v in cell if v in anomalies]
        need(actual == cell[:len(actual)], "canonical anomaly labels")
    outside_units = {i: b for i, b in units.items() if i not in anchor_ids}
    if extra or outside_units:
        need(family == "C77", "partition anomaly class")
        p, q = anomalies
        need(outside_units == {edge(p, q): 0}, "universal partition blue pair")
        expected = {frozenset((edge(w, p), edge(w, q))): 1
                    for w in C - {p, q}}
        need(extra == expected and len(extra) == 28, "universal partition domain")
        family = "C77partition"
        need(all(units[edge(u, p)] + units[edge(u, q)] == 1 for u in (0, 1)),
             "partition anchor incidence")
    else:
        needed_bit = 1 if family == "E8" else 0
        need(all(units[edge(0, v)] == needed_bit for v in anomalies),
             "family first-anchor eligibility")
    pattern = "".join(name for name in "HABO" for v in anomalies if word[v] == name)
    return (family, common, e_sizes[0], pattern)


def expected_keys():
    """Literal incidence-orbit census via all four-bin compositions and marks."""
    def margins(total, row):
        for h in range(total+1):
            for left in range(total-h+1):
                for right in range(total-h-left+1):
                    outside = total-h-left-right
                    if h+left == h+right == row:
                        yield (h, left, right, outside)
    keys = set()
    for e in margins(13, 6):
        for central in margins(28, 14):
            common = e[0]+central[0]
            if not 9 <= common <= 13:
                continue
            for prefix, sizes in (("E", e), ("C", central)):
                word = "".join(name*size for name, size in zip("HABO", sizes))
                for v, name in enumerate(word):
                    if name in ("HA" if prefix == "E" else "BO"):
                        keys.add((prefix+"8", common, e[0], name))
                for p, q in itertools.combinations(range(len(word)), 2):
                    pattern = word[p]+word[q]
                    if word[p] in "BO" and word[q] in "BO":
                        keys.add((prefix+"77", common, e[0], pattern))
                    if prefix == "C" and set(pattern) in ({"H", "O"}, {"A", "B"}):
                        keys.add(("C77partition", common, e[0], pattern))
    need(Counter(k[0] for k in keys) == dict(zip(FAMILIES, (60, 85, 70, 104, 70))),
         "independent literal census")
    return keys


def mark_once(flags, index, bit):
    need(not flags[index] & bit, "duplicate physical constraint")
    flags[index] |= bit


def check_header(raw):
    need(raw == b"* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n",
         "complete formula header")


def check(path, run_tests=False):
    formula_hash = hashlib.sha256()
    base_hash = hashlib.sha256()
    tail_hash = hashlib.sha256()
    byte_count = 0
    line_count = 0
    specimens = {}
    active = defaultdict(list)
    with Path(path).open("rb") as stream:
        def read(section):
            nonlocal byte_count, line_count
            raw = stream.readline()
            need(bool(raw), "early EOF")
            line_count += 1
            byte_count += len(raw)
            formula_hash.update(raw)
            if section == "base":
                base_hash.update(raw)
            elif section == "tail":
                tail_hash.update(raw)
            return raw
        check_header(read("header"))
        five_flags = bytearray(math.comb(N, 5))
        for _ in range(2 * math.comb(N, 5)):
            row = parse(read("base"))
            rank, bit = five_signature(row)
            mark_once(five_flags, rank, bit)
            specimens.setdefault("five", row)
        need(all(flag == 3 for flag in five_flags), "missing five-set color")
        triangle_flags = bytearray(len(TRIPLES))
        for _ in range(4 * len(TRIPLES)):
            row = parse(read("base"))
            index, bit = triangle_signature(row)
            mark_once(triangle_flags, index, bit)
            specimens.setdefault("triangle"+str(bit), row)
        need(all(flag == 15 for flag in triangle_flags), "missing triangle direction")
        for name, lookup, relation, target in (
                ("degree", DEGREE_STARS, b"=", lambda v: 20 if v in E else 21),
                ("local_triangle", TRIANGLE_STARS, b"=", lambda v: 93 if v in E else 100),
                ("E_incidence", E_STARS, b">=", lambda v: 6)):
            seen = set()
            for _ in range(N):
                row = parse(read("base"))
                vertex = star_vertex(row, lookup, relation, target)
                need(vertex not in seen, "duplicate physical star")
                seen.add(vertex)
                specimens.setdefault(name, row)
            need(seen == set(range(N)), "missing physical star")
        need(line_count == BASE_ROWS+1, "base row boundary")
        row = parse(read("tail"))
        one_hot(row)
        specimens["one_hot"] = row
        for _ in range(FORMULA_ROWS-BASE_ROWS-1):
            row = parse(read("tail"))
            selector, selected_row = deguard(row)
            active[selector].append(selected_row)
            specimens.setdefault("guard", row)
        need(stream.read(1) == b"", "extra formula content")
    need(set(active) == SELECTORS, "unused or missing selector")
    keys = [root_from_active(active[s]) for s in sorted(SELECTORS)]
    need(len(set(keys)) == 389 and set(keys) == expected_keys(), "complete decoded root set")
    need(line_count == FORMULA_ROWS+1 and byte_count == 172788992, "stream dimensions")
    need(formula_hash.hexdigest() == FORMULA_SHA, "canonical full-stream identity")
    need(base_hash.hexdigest() == BASE_SHA and tail_hash.hexdigest() == TAIL_SHA,
         "canonical section identity")
    key_bytes = "".join("\t".join(map(str, k))+"\n" for k in keys).encode("ascii")
    tests = mutation_tests(specimens, active, keys) if run_tests else None
    return {
        "verdict": "PASS encoding equivalence only; SAT/UNSAT undecided",
        "variables": 13633, "constraints": FORMULA_ROWS, "equalities": 87,
        "five_sets_both_colors": len(five_flags), "triangle_conjunctions": len(TRIPLES),
        "degree_stars": 43, "local_triangle_stars": 43, "E_incidence_stars": 43,
        "roots": len(keys), "family_counts": [
            sum(k[0] == f for k in keys) for f in FAMILIES],
        "inactive_guards_checked": sum(map(len, active.values())),
        "active_anchor_units": 389*83, "active_E_equalities": 389*43,
        "partition_blue_units": 70, "partition_equalities": 70*28,
        "formula_sha256": formula_hash.hexdigest(),
        "base_body_sha256": base_hash.hexdigest(), "selector_suffix_sha256": tail_hash.hexdigest(),
        "decoded_keys_sha256": hashlib.sha256(key_bytes).hexdigest(),
        "negative_controls": tests,
    }


def mutation_tests(specimens, active, keys):
    count = 0
    def rejects(function, value):
        nonlocal count
        try:
            function(value)
        except (ValueError, KeyError, IndexError):
            count += 1
        else:
            raise ValueError("negative control accepted")
    for bad in (b"+1 x1 +1 x1 >= 1 ;\n", b"+1 x0 >= 0 ;\n",
                b"+1 x13634 >= 0 ;\n", b"+0 x1 >= 0 ;\n",
                b"+1 x1 <= 0 ;\n", b"+1 x1 >= 0 ;"):
        rejects(parse, bad)
    rejects(check_header, b"* #variable= 13632 #constraint= 2044421 #equal= 87 intsize= 64\n")
    terms, rel, rhs = specimens["five"]
    rejects(five_signature, (terms, rel, 0))
    damaged = dict(terms)
    damaged.pop(next(iter(damaged)))
    damaged[edge(41, 42)] = 1
    rejects(five_signature, (damaged, rel, rhs))
    for bit in (1, 8):
        terms, rel, rhs = specimens["triangle"+str(bit)]
        rejects(triangle_signature, (terms, rel, rhs+1))
    for name, lookup, relation, target in (
            ("degree", DEGREE_STARS, b"=", lambda v: 20 if v in E else 21),
            ("local_triangle", TRIANGLE_STARS, b"=", lambda v: 93 if v in E else 100),
            ("E_incidence", E_STARS, b">=", lambda v: 6)):
        terms, rel, rhs = specimens[name]
        rejects(lambda row: star_vertex(row, lookup, relation, target), (terms, rel, rhs+1))
    terms, rel, rhs = specimens["one_hot"]
    rejects(one_hot, (terms, b">=", rhs))
    damaged = dict(terms)
    damaged.pop(min(damaged))
    rejects(one_hot, (damaged, rel, rhs))
    terms, rel, rhs = specimens["guard"]
    rejects(deguard, (terms, rel, 1))
    damaged = dict(terms)
    damaged[13633] = -1
    rejects(deguard, (damaged, rel, rhs))
    root_rows = active[min(SELECTORS)]
    rejects(root_from_active, root_rows[1:])
    rejects(root_from_active, root_rows + [root_rows[0]])
    rejects(root_from_active, root_rows[:-1])
    partition_selector = next(s for s, key in zip(sorted(SELECTORS), keys)
                              if key[0] == "C77partition")
    partition_rows = active[partition_selector]
    rejects(root_from_active, partition_rows[:-2])
    rejects(root_from_active, partition_rows[:-57] + partition_rows[-56:])
    flags = bytearray([1])
    rejects(lambda unused: mark_once(flags, 0, 1), None)
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formula", type=Path)
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()
    print(json.dumps(check(args.formula, args.negative_controls), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
