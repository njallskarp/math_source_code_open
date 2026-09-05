#!/usr/bin/env python3
"""Exact checker for the r=28 small-separator profile compression."""

from __future__ import annotations

from bisect import bisect_right
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
from math import comb


BASE_LINES = (
    (Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(-3)),
    (Fraction(7, 3), Fraction(-25, 3)),
    (Fraction(37, 9), Fraction(-155, 9)),
    (Fraction(5), Fraction(-203, 9)),
)


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def lower_hull(values: list[int]) -> list[int]:
    hull: list[int] = []
    for x in range(len(values)):
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            if Fraction(values[b] - values[a], b - a) < Fraction(values[x] - values[b], x - b):
                break
            hull.pop()
        hull.append(x)
    return hull


def hull_value(values: list[int], hull: list[int], x: Fraction) -> Fraction:
    if x.denominator == 1 and x.numerator in hull:
        return Fraction(values[x.numerator])
    j = max(0, bisect_right(hull, x) - 1)
    if j == len(hull) - 1:
        j -= 1
    left, right = hull[j], hull[j + 1]
    assert left <= x <= right
    return Fraction(values[left]) + Fraction(values[right] - values[left], right - left) * (x - left)


def build_tables(max_n: int) -> dict[int, list[int]]:
    """Published affine lines plus the reviewed rounded convex recurrence."""
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[int]] = {}
    for n in range(4, max_n + 1):
        values = [
            max(ceil_fraction(a * q + b * (n - 2)) for a, b in BASE_LINES)
            for q in range(comb(n, 2) + 1)
        ]
        for s in range(4, n):
            multiplier = Fraction(comb(n, s), comb(n - 4, s - 4))
            for q in range(len(values)):
                mean = Fraction(q * s * (s - 1), n * (n - 1))
                values[q] = max(values[q], ceil_fraction(multiplier * hull_value(tables[s], hulls[s], mean)))
        tables[n] = values
        hulls[n] = lower_hull(values)
    return tables


def edge(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


T = (0, 1, 2)
S = 3
W = (4, 5)
B = (0, 1, 2, 3)
TRIANGLE = frozenset((edge(0, 1), edge(0, 2), edge(1, 2)))
OPTIONAL = tuple(edge(S, t) for t in T) + tuple(edge(w, b) for w in W for b in B)


def neighbors(edges: frozenset[tuple[int, int]], vertex: int) -> set[int]:
    result = set()
    for a, b in edges:
        if a == vertex:
            result.add(b)
        elif b == vertex:
            result.add(a)
    return result


def has_safe_cut_matching(edges: frozenset[tuple[int, int]], deleted: int) -> bool:
    """Necessary local trace of a perfect matching of H-deleted.

    The two singleton components must be injected into B-deleted.  If a used
    matching edge wb completes a triangle deleted-w-b, the rest of the perfect
    matching would certify a forbidden conformal triangle, so that edge is not
    safe.
    """
    choices: list[list[int]] = []
    for w in W:
        local = []
        nw = neighbors(edges, w)
        for b in sorted(nw - {deleted}):
            completes_triangle = deleted in nw and edge(deleted, b) in edges
            if not completes_triangle:
                local.append(b)
        choices.append(local)
    return any(a != b for a in choices[0] for b in choices[1])


def canonical_code(edges: frozenset[tuple[int, int]]) -> str:
    """Quotient by permutations of T and interchange of the two singletons."""
    codes = []
    for perm in permutations(T):
        for swap in (False, True):
            mapping = {
                0: perm[0], 1: perm[1], 2: perm[2], S: S,
                4: 5 if swap else 4, 5: 4 if swap else 5,
            }
            transformed = frozenset(edge(mapping[a], mapping[b]) for a, b in edges)
            codes.append("".join("1" if e in transformed else "0" for e in OPTIONAL))
    return min(codes)


def local_separator_audit() -> tuple[int, tuple[str, ...], tuple[tuple[int, int], ...]]:
    # If B=T and w is a singleton component, choose a neighbour a of w.
    # A perfect matching of H-a must match w to another vertex b of T, and
    # a,b,w is then conformal.  The following checks every possible N_T(w).
    b3_safe = 0
    for mask in range(1, 1 << len(T)):
        n_w = {T[i] for i in range(len(T)) if mask & (1 << i)}
        valid = True
        for deleted in T:
            choices = [b for b in n_w - {deleted} if not (deleted in n_w)]
            if not choices:
                valid = False
                break
        b3_safe += int(valid)
    assert b3_safe == 0

    labelled = []
    for bits in product((0, 1), repeat=len(OPTIONAL)):
        edges = frozenset(set(TRIANGLE) | {OPTIONAL[i] for i, bit in enumerate(bits) if bit})
        if all(has_safe_cut_matching(edges, deleted) for deleted in B):
            labelled.append(edges)

    codes = tuple(sorted({canonical_code(edges) for edges in labelled}))
    degree_types = tuple(sorted({tuple(sorted(len(neighbors(edges, w)) for w in W)) for edges in labelled}))
    assert len(labelled) == 18
    assert codes == ("00000110101", "00000111101", "00101011001")
    assert degree_types == ((2, 2), (2, 3))
    return len(labelled), codes, degree_types


def partitions(total: int, cap: int | None = None) -> tuple[tuple[int, ...], ...]:
    if total == 0:
        return ((),)
    if cap is None:
        cap = total
    result = []
    for first in range(min(total, cap), 0, -1):
        for tail in partitions(total - first, first):
            result.append((first,) + tail)
    return tuple(result)


def histogram_text(values: tuple[int, ...]) -> str:
    counts = Counter(values)
    return ",".join(f"{value}^{counts[value]}" for value in sorted(counts))


def profile_audit(row: int, total_excess: int, table54: list[int]) -> tuple[tuple[str, ...], int, int, tuple[int, ...]]:
    profiles: dict[tuple[int, ...], int] = {}
    for degrees in ((2, 2), (2, 3)):
        singleton_excess = tuple(27 - degree for degree in degrees)
        remainder = total_excess - sum(singleton_excess)
        assert 0 <= remainder <= 4
        for part in partitions(remainder):
            values = tuple(sorted(singleton_excess + part + (0,) * (53 - len(part))))
            assert len(values) == 55 and sum(values) == total_excess
            profiles[values] = sum(table54[row - 27 - value] for value in values)

    records = tuple(
        f"row={row} profile={histogram_text(values)} sum={cost} bound={(cost + 50) // 51}"
        for values, cost in sorted(profiles.items(), key=lambda item: (item[1], item[0]))
    )
    minimum = min(profiles.values())
    bound = (minimum + 50) // 51
    queried = tuple(sorted({row - 27 - value for values in profiles for value in values}))
    return records, minimum, bound, queried


def uniform_lift(minimum: int, target_bound: int) -> int:
    target_sum = 51 * (target_bound - 1) + 1
    lift = max(0, ceil_fraction(Fraction(target_sum - minimum, 55)))
    assert minimum + 55 * lift >= target_sum
    if lift:
        assert minimum + 55 * (lift - 1) < target_sum
    return lift


def main() -> None:
    labelled, codes, degree_types = local_separator_audit()
    table54 = build_tables(54)[54]
    records768, minimum768, bound768, queried768 = profile_audit(768, 51, table54)
    records769, minimum769, bound769, queried769 = profile_audit(769, 53, table54)
    assert len(records768) == 3 and (minimum768, bound768) == (360156, 7062)
    assert len(records769) == 8 and (minimum769, bound769) == (361740, 7093)
    lift768 = uniform_lift(minimum768, 7070)
    lift769 = uniform_lift(minimum769, 7098)
    assert (lift768, lift769) == (7, 4)

    output = [
        "PASS Albertson r=28 separator compression",
        "b3_safe_singleton_neighborhoods=0",
        f"b4_labelled_patterns={labelled} orbits={len(codes)} codes={','.join(codes)}",
        "b4_singleton_degree_types=" + ";".join(f"{a},{b}" for a, b in degree_types),
        *records768,
        f"row=768 profiles={len(records768)} minimum={minimum768} bound={bound768} "
        f"queried_q={','.join(map(str, queried768))} uniform_lift_to_7070={lift768}",
        *records769,
        f"row=769 profiles={len(records769)} minimum={minimum769} bound={bound769} "
        f"queried_q={','.join(map(str, queried769))} uniform_lift_to_7098={lift769}",
    ]
    digest = sha256(("\n".join(output) + "\n").encode()).hexdigest()
    output.append(f"certificate_sha256={digest}")
    print("\n".join(output))


if __name__ == "__main__":
    main()
