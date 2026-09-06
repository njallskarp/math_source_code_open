#!/usr/bin/env python3
"""Independent coefficient-DP audit of the M=215 partition certificate."""

from collections import Counter, defaultdict
from copy import deepcopy
from itertools import combinations, product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
WT = {18: 21, 19: 12, 20: 3, 21: 0, 22: 3, 23: 12, 24: 21}


def need(test, message):
    if not test:
        raise ValueError(message)


def profiles():
    """Derive all degree histograms with 43 vertices, degree sum 892, W<=39."""
    ds = tuple(U)
    found = []
    for counts in product(*(range(40 // WT[d] + 1) for d in ds if d != 21)):
        p = {d: c for d, c in zip((d for d in ds if d != 21), counts) if c}
        p[21] = 43 - sum(counts)
        if p[21] < 0 or sum(d * c for d, c in p.items()) != 892:
            continue
        weight = sum(WT[d] * c for d, c in p.items())
        if weight <= 39 and weight % 6 == 3:
            name = "B" if p.get(19) else "C" if p.get(22) else "A"
            found.append((name, weight, p))
    need(len(found) == 3 and {x[0] for x in found} == {"A", "B", "C"},
         "degree-profile derivation failed")
    return {name: (weight, p) for name, weight, p in found}


def color_totals(weight, p):
    total = (43 - weight) // 2
    red_cap = sum((U[d] - 7) * n for d, n in p.items())
    blue_cap = sum((U[42 - d] - 7) * n for d, n in p.items())
    return tuple((r, total - r) for r in range(total + 1)
                 if (red_cap - r) % 3 == 0 and (blue_cap - total + r) % 3 == 0)


def histogram(items):
    out = Counter()
    need(items == sorted(items), "unsorted defect multiset")
    for item in items:
        need(isinstance(item, list) and len(item) == 3
             and all(isinstance(x, int) for x in item), "malformed defect type")
        d, r, b = item
        need(r >= 0 and b >= 0 and r + b > 0, "invalid defect excess")
        out[d, r, b] += 1
    return out


def aggregate_ok(p, h):
    """Apply the E-class edge parity obtained from the vertexwise identity."""
    used = Counter()
    excess = Counter()
    for (d, r, b), n in h.items():
        need(d in p, "defect degree outside profile")
        used[d] += n
        excess[d] += n * (r + b)
    need(all(used[d] <= p[d] for d in p), "too many defects of one degree")
    e_size = p.get(20, 0)
    special = next((d for d in p if d not in (20, 21)), None)

    def constant(d):
        cap = U[d] + U[42 - d] - 14
        base = comb(42 - d, 2) - 446 + 21 * d
        return cap - base

    q = 0 if special is None else excess[special] - constant(special)
    if not 0 <= q <= e_size:
        return False
    epsilon = 0 if special is None else special - 21
    twice_edges = excess[20] - e_size * constant(20) + epsilon * q
    return twice_edges % 2 == 0 and 0 <= twice_edges <= e_size * (e_size - 1)


def count_intrinsic(p, totals):
    """Count multisets as a coefficient product, without constructing keys."""
    red_total, blue_total = totals
    ds = tuple(sorted(p))
    types = [(d, r, b) for d in ds for r in range(red_total + 1)
             for b in range(blue_total + 1) if r + b]
    # State holds color sums, vertex counts by degree, and excess sums by degree.
    states = {(0, 0, (0,) * len(ds), (0,) * len(ds)): 1}
    for d, r, b in types:
        i = ds.index(d)
        nxt = defaultdict(int)
        for (sr, sb, counts, sums), coefficient in states.items():
            for n in range(p[d] - counts[i] + 1):
                nr, nb = sr + n * r, sb + n * b
                if nr > red_total or nb > blue_total:
                    break
                nc, ns = list(counts), list(sums)
                nc[i] += n
                ns[i] += n * (r + b)
                nxt[nr, nb, tuple(nc), tuple(ns)] += coefficient
        states = nxt
    answer = 0
    for (r, b, counts, sums), coefficient in states.items():
        if (r, b) != totals:
            continue
        synthetic = Counter({(d, s, 0): 1 for d, s in zip(ds, sums) if s})
        if aggregate_ok(p, synthetic):
            answer += coefficient
    return answer


def capacities(p):
    """Solve side size 21 and side degree sum 436 exactly."""
    ds = tuple(sorted(p))
    out = []
    for counts in product(*(range(p[d] - (d == 21) + 1) for d in ds)):
        if sum(counts) == 21 and sum(d * n for d, n in zip(ds, counts)) == 436:
            out.append(dict(zip(ds, counts)))
    need(out, "no exact-anchor side capacity")
    return tuple(out)


def count_splits(h, p, cap):
    """Count side submultisets via a one-variable factor for each defect type."""
    ds = tuple(sorted(p))
    states = {(0,) * len(ds): 1}
    for (d, _r, _b), multiplicity in sorted(h.items()):
        i = ds.index(d)
        nxt = defaultdict(int)
        for counts, coefficient in states.items():
            for red_count in range(multiplicity + 1):
                nc = list(counts)
                nc[i] += red_count
                nxt[tuple(nc)] += coefficient
        states = nxt
    total = Counter()
    for (d, _r, _b), n in h.items():
        total[d] += n
    return sum(coefficient for counts, coefficient in states.items() if all(
        counts[i] <= cap[d]
        and total[d] - counts[i] <= p[d] - (d == 21) - cap[d]
        for i, d in enumerate(ds)))


def validate(data):
    need(set(data) == {"schema", "intrinsic", "rooted"} and data["schema"] == 1,
         "unexpected certificate schema")
    ps = profiles()
    predicted_i, observed_i = Counter(), Counter()
    for name, (weight, p) in ps.items():
        predicted_i[name] = sum(count_intrinsic(p, totals)
                                for totals in color_totals(weight, p))

    parents, histograms = set(), {}
    for entry in data["intrinsic"]:
        need(isinstance(entry, list) and len(entry) == 2, "malformed intrinsic key")
        name, items = entry
        need(name in ps, "unknown profile")
        key = json.dumps(entry, separators=(",", ":"))
        need(key not in parents, "duplicate intrinsic key")
        h = histogram(items)
        weight, p = ps[name]
        totals = (sum(r * n for (_d, r, _b), n in h.items()),
                  sum(b * n for (_d, _r, b), n in h.items()))
        need(totals in color_totals(weight, p), "wrong color totals")
        need(aggregate_ok(p, h), "E-class parity identity failed")
        parents.add(key)
        histograms[key] = h
        observed_i[name] += 1
    need(observed_i == predicted_i, "intrinsic coefficient count mismatch")

    caps = {name: capacities(p) for name, (_weight, p) in ps.items()}
    predicted_r = Counter()
    for key, h in histograms.items():
        name = json.loads(key)[0]
        predicted_r[name] += sum(count_splits(h, ps[name][1], cap) for cap in caps[name])

    seen, observed_r = set(), Counter()
    for entry in data["rooted"]:
        need(isinstance(entry, list) and len(entry) == 4, "malformed rooted key")
        name, items, special_red, red_items = entry
        parent = json.dumps([name, items], separators=(",", ":"))
        need(parent in parents, "missing intrinsic parent")
        key = json.dumps(entry, separators=(",", ":"))
        need(key not in seen, "duplicate rooted key")
        h, rh = histograms[parent], histogram(red_items) if red_items else Counter()
        need(all(rh[t] <= h[t] for t in rh), "red defects are not a submultiset")
        p = ps[name][1]
        special = next((d for d in p if d not in (20, 21)), None)
        matches = [cap for cap in caps[name]
                   if (0 if special is None else cap[special]) == special_red]
        need(len(matches) == 1, "bad singleton-edge color")
        cap = matches[0]
        rd, td = Counter(), Counter()
        for (d, _r, _b), n in rh.items():
            rd[d] += n
        for (d, _r, _b), n in h.items():
            td[d] += n
        need(all(rd[d] <= cap[d]
                 and td[d] - rd[d] <= p[d] - (d == 21) - cap[d] for d in p),
             "defect split exceeds side capacity")
        seen.add(key)
        observed_r[name] += 1
    need(observed_r == predicted_r, "rooted coefficient count mismatch")
    return {
        "intrinsic_by_profile": dict(sorted(observed_i.items())),
        "rooted_by_profile": dict(sorted(observed_r.items())),
        "side_capacities": {name: [dict(sorted(x.items())) for x in value]
                            for name, value in sorted(caps.items())},
    }


def formula_control():
    """Check exact triple gates and five-set rows on all graphs through order 6."""
    graphs = vertices = five_sets = 0
    for n in range(7):
        edges = list(combinations(range(n), 2))
        index = {e: i for i, e in enumerate(edges)}
        triples = [(t, sum(1 << index[e] for e in combinations(t, 2)))
                   for t in combinations(range(n), 3)]
        fives = [sum(1 << index[e] for e in combinations(s, 2))
                 for s in combinations(range(n), 5)]
        for graph in range(1 << len(edges)):
            adj = [set() for _ in range(n)]
            for bit, (u, v) in enumerate(edges):
                if graph >> bit & 1:
                    adj[u].add(v)
                    adj[v].add(u)
            for v in range(n):
                gate_r = sum(mask & graph == mask and v in t for t, mask in triples)
                gate_b = sum(mask & graph == 0 and v in t for t, mask in triples)
                local_r = sum(b in adj[a] for a, b in combinations(adj[v], 2))
                blue = set(range(n)) - adj[v] - {v}
                local_b = sum(b not in adj[a] for a, b in combinations(blue, 2))
                need((gate_r, gate_b) == (local_r, local_b), "triple-gate mismatch")
                vertices += 1
            for mask in fives:
                red = (mask & graph).bit_count()
                need((1 <= red <= 9) == (red not in (0, 10)), "five-set row mismatch")
                five_sets += 1
            graphs += 1
    return graphs, vertices, five_sets


def run(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    result = validate(data)
    mutations = []
    for field in ("intrinsic", "rooted"):
        broken = deepcopy(data)
        broken[field].pop()
        mutations.append(broken)
    broken = deepcopy(data)
    broken["rooted"][0][2] = 1
    mutations.append(broken)
    broken = deepcopy(data)
    broken["intrinsic"].append(deepcopy(broken["intrinsic"][0]))
    mutations.append(broken)
    rejected = 0
    for broken in mutations:
        try:
            validate(broken)
        except ValueError:
            rejected += 1
    need(rejected == len(mutations), "a mutated certificate was accepted")
    graphs, vertices, fives = formula_control()
    result.update({
        "status": "INDEPENDENTLY_VERIFIED_M215_DEFECT_PARTITION_INTERFACE",
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "intrinsic_total": len(data["intrinsic"]),
        "rooted_total": len(data["rooted"]),
        "mutations_rejected": rejected,
        "finite_control_graphs": graphs,
        "finite_control_vertex_instances": vertices,
        "finite_control_five_set_instances": fives,
    })
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path,
                        default=Path(__file__).parent.parent
                        / "ramsey_r55_m215_defect_partition" / "certificate.json")
    args = parser.parse_args()
    print(json.dumps(run(args.certificate), indent=2, sort_keys=True))
