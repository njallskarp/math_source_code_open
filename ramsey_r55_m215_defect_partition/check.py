#!/usr/bin/env python3
"""Source-independent checker: labeled excess tokens and set partitions.

Imports no partition.py. Reconstructs the arithmetic degree universe and all
certificate entries, not merely their counts. Standard-library exact integers.
"""
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json

U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
W = {18: 21, 19: 12, 20: 3, 21: 0, 22: 3, 23: 12, 24: 21}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def degree_profiles():
    ds = (18, 19, 20, 22, 23, 24)
    out = []
    for counts in product(*(range(39 // W[d] + 1) for d in ds)):
        weight = sum(W[d] * c for d, c in zip(ds, counts))
        if weight not in range(3, 40, 6):
            continue
        p = {d: c for d, c in zip(ds, counts) if c}
        p[21] = 43 - sum(counts)
        twice_m = sum(d * c for d, c in p.items())
        if twice_m % 2 == 0 and 445 <= twice_m // 2 <= 451:
            out.append((twice_m // 2 - 231, weight, p))
    return out


def set_partitions(items):
    """Every partition of distinguishable tokens, each exactly once."""
    if not items:
        yield ()
        return
    head, *tail = items
    for blocks in set_partitions(tail):
        yield ((head,),) + blocks
        for i in range(len(blocks)):
            yield blocks[:i] + ((head,) + blocks[i],) + blocks[i + 1:]


def side_profiles(p, cross_total):
    exceptional = sorted(d for d in p if d != 21)
    for values in product(*(range(p[d] + 1) for d in exceptional)):
        a = dict(zip(exceptional, values))
        a[21] = 21 - sum(values)
        if not 0 <= a[21] <= p[21] - 1:
            continue
        if sum((d - 21) * c for d, c in a.items()) == cross_total - 220:
            yield a


def reconstruct():
    profiles = degree_profiles()
    globals_by_M = Counter(m for m, _, _ in profiles)
    splits_by_M = Counter()
    for m, _, p in profiles:
        splits_by_M[m] += len(list(side_profiles(p, m)))
    require([globals_by_M[m] for m in range(214, 221)] == [1, 3, 7, 14, 21, 27, 31],
            "global arithmetic universe mismatch")
    require([splits_by_M[m] for m in range(214, 221)] == [1, 5, 17, 40, 69, 95, 122],
            "anchored arithmetic universe mismatch")
    intrinsic, rooted = set(), set()
    for m, weight, p in profiles:
        if m != 215:
            continue
        name = "B" if 19 in p else "C" if 22 in p else "A"
        red_cap = sum((U[d] - 7) * c for d, c in p.items())
        blue_cap = sum((U[42 - d] - 7) * c for d, c in p.items())
        surplus = (43 - weight) // 2
        # Derive b(d) directly from the local-neighborhood conservation identity.
        b = {d: comb(42 - d, 2) - 231 + 21 * d
             - (U[d] - 7) - (U[42 - d] - 7) for d in p}
        for red_total in range(surplus + 1):
            blue_total = surplus - red_total
            if (red_cap - red_total) % 3 or (blue_cap - blue_total) % 3:
                continue
            colors = [0] * red_total + [1] * blue_total
            for blocks in set_partitions(list(range(surplus))):
                for degrees in product(sorted(p), repeat=len(blocks)):
                    count_degrees = Counter(degrees)
                    if any(count_degrees[d] > p[d] for d in p):
                        continue
                    defects = tuple(sorted(
                        (d, sum(colors[i] == 0 for i in block), sum(colors[i] == 1 for i in block))
                        for d, block in zip(degrees, blocks)
                    ))
                    sd = Counter()
                    for d, r, blue in defects:
                        sd[d] += r + blue
                    special = [d for d in p if d not in (20, 21)]
                    twice_edges = sd[20] + p[20] * (b[20] - m)
                    if special:
                        d = special[0]
                        require(p[d] == 1, "non-singleton outside E,C")
                        q = b[d] - m + sd[d]
                        if not 0 <= q <= p[20]:
                            continue
                        twice_edges += (d - 21) * q
                    if twice_edges % 2 or not 0 <= twice_edges <= p[20] * (p[20] - 1):
                        continue
                    intrinsic.add((name, defects))
                    for caps in side_profiles(p, 215):
                        for bits in product((0, 1), repeat=len(defects)):
                            red_defects = tuple(t for t, bit in zip(defects, bits) if bit)
                            nr = Counter(t[0] for t in red_defects)
                            nb = Counter(t[0] for t, bit in zip(defects, bits) if not bit)
                            if any(nr[d] > caps[d] or nb[d] > p[d] - (d == 21) - caps[d] for d in p):
                                continue
                            special_red = caps[special[0]] if special else 0
                            rooted.add((name, defects, special_red, red_defects))
    return {"schema": 1, "intrinsic": sorted(intrinsic), "rooted": sorted(rooted)}


def validate(data):
    expected = reconstruct()
    # JSON normalization preserves ordering and multiplicities for entrywise comparison.
    normalized = json.loads(json.dumps(expected))
    require(data == normalized, "certificate differs from complete token reconstruction")
    return expected


def identity_control():
    graphs = vertices = 0
    for n in range(7):
        edges = list(combinations(range(n), 2))
        for mask in range(1 << len(edges)):
            adj = [set() for _ in range(n)]
            for bit, (a, b) in enumerate(edges):
                if mask >> bit & 1:
                    adj[a].add(b)
                    adj[b].add(a)
            degrees = list(map(len, adj))
            m = sum(degrees) // 2
            for v in range(n):
                a = adj[v]
                b = set(range(n)) - a - {v}
                tr = sum(y in adj[x] for x, y in combinations(a, 2))
                tb = sum(y not in adj[x] for x, y in combinations(b, 2))
                require(tr + tb == comb(n - 1 - degrees[v], 2) - m + sum(degrees[w] for w in a),
                        "literal neighborhood identity failure")
                vertices += 1
            graphs += 1
    return graphs, vertices


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path,
                        default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    data = json.loads(raw)
    result = validate(data)
    mutations = 0
    for field in ("intrinsic", "rooted"):
        corrupt = json.loads(raw)
        corrupt[field].pop()
        try:
            validate(corrupt)
        except ValueError:
            mutations += 1
        else:
            raise ValueError("missing-entry mutation accepted")
    corrupt = json.loads(raw)
    corrupt["rooted"][0][2] = 1
    try:
        validate(corrupt)
    except ValueError:
        mutations += 1
    else:
        raise ValueError("wrong-anchor mutation accepted")
    graphs, vertices = identity_control()
    print(json.dumps({
        "intrinsic_entries_checked": len(result["intrinsic"]),
        "rooted_entries_checked": len(result["rooted"]),
        "mutations_rejected": mutations,
        "identity_graphs": graphs,
        "identity_vertex_instances": vertices,
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
    }, sort_keys=True, indent=2))
