#!/usr/bin/env python3
"""Exact intrinsic and anchored deficiency histograms for the M=215 slice.

No graph or SAT search is performed. See PROOF.md for the exhaustive reduction.
Types are (red degree, red excess over 7, blue excess over 7).
"""
from collections import Counter
from functools import lru_cache
from itertools import product
import hashlib
import json
from pathlib import Path

PROFILES = {
    "A": {20: 11, 21: 32},
    "B": {19: 1, 20: 9, 21: 33},
    "C": {20: 12, 21: 30, 22: 1},
}


@lru_cache(None)
def vector_partitions(red, blue, lower=(0, 0)):
    """Multisets of nonzero pairs summing to (red, blue), lexicographically."""
    if red == blue == 0:
        return ((),)
    return tuple(
        ((r, b),) + tail
        for r in range(red + 1)
        for b in range(blue + 1)
        if (r or b) and (r, b) >= lower
        for tail in vector_partitions(red - r, blue - b, (r, b))
    )


def intrinsic_keys():
    keys = []
    for red, blue in ((2, 3), (5, 0)):
        for er in range(red + 1):
            for eb in range(blue + 1):
                if (er + eb) % 2 == 0:
                    continue
                for left, right in product(
                    vector_partitions(er, eb),
                    vector_partitions(red - er, blue - eb),
                ):
                    defects = tuple(sorted(
                        [(20, *x) for x in left] + [(21, *x) for x in right]
                    ))
                    keys.append(("A", defects))
    # In B the two units are on different vertices, one in E and one outside E.
    for other_degree in (19, 21):
        for color in range(2):
            keys.append(("B", tuple(sorted((
                (20, 1 - color, color), (other_degree, color, 1 - color)
            )))))
    # In C both units are red, and central excess is even.
    for degree in (20, 21, 22):
        keys.append(("C", ((degree, 2, 0),)))
    for d, e in ((20, 20), (20, 22), (21, 21)):
        keys.append(("C", ((d, 1, 0), (e, 1, 0))))
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate intrinsic key")
    return tuple(sorted(keys))


def full_types(key):
    name, defects = key
    types = Counter(defects)
    for degree, count in PROFILES[name].items():
        remaining = count - sum(n for (d, _, _), n in types.items() if d == degree)
        if remaining < 0:
            raise ValueError("too many defective vertices")
        if remaining:
            types[degree, 0, 0] = remaining
    return types


def red_side_capacities(name, special_red):
    if name == "A":
        if special_red:
            raise ValueError("A has no singleton exceptional class")
        return {20: 5, 21: 16}
    if name == "B":
        return {19: special_red, 20: 5 - 2 * special_red, 21: 16 + special_red}
    return {20: 5 + special_red, 21: 16 - 2 * special_red, 22: special_red}


def rooted_keys():
    """(profile, all defects, singleton side, red-neighbor defects).

The fixed anchor has type (21,0,0). Zero-excess multiplicities on both
sides are reconstructed from the degree capacities; no labeled multiplicity
is discarded except permutation of vertices of exactly identical type.
"""
    out = []
    for name, defects in intrinsic_keys():
        multiplicities = Counter(defects)
        kinds = sorted(multiplicities)
        for amounts in product(*(range(multiplicities[t] + 1) for t in kinds)):
            red_defects = tuple(t for t, n in zip(kinds, amounts) for _ in range(n))
            red_counts = Counter(t[0] for t in red_defects)
            blue_counts = Counter(t[0] for t in defects)
            blue_counts.subtract(red_counts)
            for special_red in ((0,) if name == "A" else (0, 1)):
                caps = red_side_capacities(name, special_red)
                if all(
                    red_counts[d] <= caps[d]
                    and blue_counts[d] <= n - (d == 21) - caps[d]
                    for d, n in PROFILES[name].items()
                ):
                    out.append((name, defects, special_red, red_defects))
    if len(out) != len(set(out)):
        raise ValueError("duplicate rooted key")
    return tuple(sorted(out))


def rooted_types(key):
    name, defects, special_red, red_defects = key
    total = full_types((name, defects))
    red = Counter(red_defects)
    for degree, cap in red_side_capacities(name, special_red).items():
        red[degree, 0, 0] = cap - sum(n for (d, _, _), n in red.items() if d == degree)
    red = +red
    blue = total.copy()
    blue.subtract(red)
    blue[21, 0, 0] -= 1
    if any(n < 0 for n in blue.values()):
        raise ValueError("invalid side reconstruction")
    return red, +blue


def canonical_anchor_key(adjacency, types, candidates):
    """Minimum type-incidence vector; candidates and types are equivariant.

This generic helper does not check Ramsey or deficiency premises. In the
theorem the candidates are exactly the vertices of type (21,0,0).
"""
    kinds = sorted(set(types))
    vectors = []
    for v in candidates:
        counts = Counter(types[w] for w in adjacency[v])
        vectors.append(tuple(counts[t] for t in kinds))
    if not vectors:
        raise ValueError("no candidate anchor")
    return min(vectors)


def certificate_bytes():
    obj = {"schema": 1, "intrinsic": intrinsic_keys(), "rooted": rooted_keys()}
    return (json.dumps(obj, separators=(",", ":")) + "\n").encode()


def report():
    intrinsic = intrinsic_keys()
    rooted = rooted_keys()
    minima = {}
    for name in PROFILES:
        vals = []
        for key in rooted:
            if key[0] != name:
                continue
            red, blue = rooted_types(key)
            if sum(red.values()) != 21 or sum(blue.values()) != 21:
                raise ValueError("side size mismatch")
            if sum(t[0] * n for t, n in red.items()) != 436:
                raise ValueError("red-side degree sum mismatch")
            if sum(t[0] * n for t, n in blue.items()) != 435:
                raise ValueError("blue-side degree sum mismatch")
            dcount = full_types((key[0], key[1]))[21, 0, 0]
            vals.append((dcount, red[21, 0, 0], blue[21, 0, 0]))
        minima[name] = [min(x[i] for x in vals) for i in range(3)]
    return {
        "intrinsic_by_profile": dict(sorted(Counter(k[0] for k in intrinsic).items())),
        "rooted_by_profile": dict(sorted(Counter(k[0] for k in rooted).items())),
        "intrinsic_total": len(intrinsic),
        "rooted_total": len(rooted),
        "minimum_D_redD_blueD": minima,
        "global_minimum_D_redD_blueD": [min(x[i] for x in minima.values()) for i in range(3)],
        "certificate_sha256": hashlib.sha256(certificate_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", type=Path)
    args = parser.parse_args()
    if args.write_certificate:
        args.write_certificate.write_bytes(certificate_bytes())
    print(json.dumps(report(), indent=2, sort_keys=True))
