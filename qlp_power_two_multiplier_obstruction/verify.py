#!/usr/bin/env python3
"""Finite independent orbit audit of the proved multiplier obstruction."""

from collections import Counter
from itertools import product
import json


def subgroup_generated(generators, n):
    h = {1}
    while True:
        enlarged = h | {a * b % n for a in h for b in generators}
        if enlarged == h:
            return frozenset(h)
        h = enlarged


def all_subgroups(n):
    units = frozenset(range(1, n, 2))  # Called only at n = 64.
    found = {frozenset({1})}
    pending = list(found)
    while pending:
        h = pending.pop()
        for a in units - h:
            extended = subgroup_generated(h | {a}, n)
            if extended not in found:
                found.add(extended)
                pending.append(extended)
    # Every proper subgroup can be extended by any omitted generator;
    # induction on a generating set proves completeness of this traversal.
    return sorted(found, key=lambda h: (len(h), sorted(h)))


def orbits(h, n):
    remaining = set(range(n))
    result = []
    while remaining:
        j = min(remaining)
        orbit = frozenset(a * j % n for a in h)
        result.append(orbit)
        remaining -= orbit
    return result


def forced_half_period_pairs(h, n):
    blocks = orbits(h, n)
    label = {j: i for i, block in enumerate(blocks) for j in block}
    return sum(label[j] == label[j + n // 2] for j in range(n // 2))


def audit_small_identity(n):
    h = frozenset({1, 1 + n // 2})
    blocks = orbits(h, n)
    units = ((1, 0), (0, 1), (-1, 0), (0, -1))
    checked = 0
    for values in product(units, repeat=len(blocks)):
        word = [None] * n
        for block, value in zip(blocks, values):
            for j in block:
                word[j] = value
        real = imag = 0
        for j in range(n):
            a, b = word[j]
            c, d = word[(j + n // 2) % n]
            real += a * c + b * d
            imag += b * c - a * d
        squares = 0
        for j in range(0, n // 2, 2):
            a, b = word[j]
            c, d = word[j + n // 2]
            squares += (a + c) ** 2 + (b + d) ** 2
        if real != squares or imag != 0 or real < 0:
            raise AssertionError("sum-of-squares identity failed")
        checked += 1
    return checked


def main():
    groups = all_subgroups(64)
    rows = []
    allowed = []
    for h in groups:
        forced = forced_half_period_pairs(h, 64)
        # Each forced unordered pair contributes +2 to C_X(32);
        # any other unordered pair contributes at least -2.
        lower_bound = 4 * forced - 64
        if 33 not in h:
            allowed.append(sorted(h))
        elif lower_bound < 0:
            raise AssertionError("orbit bound failed to certify an exclusion")
        rows.append({"subgroup": sorted(h), "order": len(h),
                     "forced_half_period_pairs": forced,
                     "autocorrelation_lower_bound": lower_bound,
                     "excluded_by_33": 33 in h})
    if len(groups) != 14 or allowed != [[1], [1, 31], [1, 63]]:
        raise AssertionError("unexpected subgroup classification")
    small = {str(n): audit_small_identity(n) for n in (4, 8)}
    if small != {"4": 64, "8": 4096}:
        raise AssertionError("unexpected invariant-word count")
    print(json.dumps({"status": "PASS", "modulus": 64,
                      "subgroup_count": len(groups),
                      "subgroup_order_counts": dict(sorted(Counter(map(len, groups)).items())),
                      "excluded_subgroups": 11, "remaining_subgroups": allowed,
                      "small_identity_words_checked": small, "subgroups": rows}, indent=2))


if __name__ == "__main__":
    main()
