#!/usr/bin/env python3
"""Structural audit of the clean-room r=28 separator certificate.

Unlike verify.py, this script does not generate all component partitions.  It
uses a uniform deficiency minimum for 6<=b<=24, convex internal-edge maxima at
b=25,26, and explicit boundary lists only for b=3,4,5,27,28.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from math import comb


R, N, TARGET = 28, 55, 7098


def falling(n: int, k: int) -> int:
    answer = 1
    for j in range(k):
        answer *= n - j
    return answer


BASE = {
    0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
    5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150,
}


@lru_cache(maxsize=None)
def complete_lower(q: int) -> int:
    if q in BASE:
        return BASE[q]
    return -(-(q * complete_lower(q - 1)) // (q - 4))


@lru_cache(maxsize=None)
def graph_lower(n: int, m: int) -> int:
    if n < 4 or m <= 0:
        return 0
    best = Fraction(0)
    for k in range(4, n + 1):
        line = Fraction(5 * m * k * (k - 1), n * (n - 1))
        line -= Fraction(203 * (k - 2), 9)
        value = line * Fraction(falling(n, 4), falling(k, 4))
        best = max(best, value)
    return best.numerator // best.denominator


def crossing_k6n(n: int) -> int:
    return 6 * (n // 2) * ((n - 1) // 2)


def bipartite_lower(a: int, b: int) -> int:
    answer = 0
    for x, y in ((a, b), (b, a)):
        if x >= 6:
            answer = max(answer, x * (x - 1) * crossing_k6n(y) // 30)
    return answer


def multipartite_lower(parts: tuple[int, ...]) -> int:
    totals = {0}
    for size in parts:
        totals |= {value + size for value in totals}
    total = sum(parts)
    return max(bipartite_lower(x, total - x) for x in totals)


def deficiency(parts: tuple[int, ...], b: int) -> int:
    return sum(s * max(0, R - b - s) for s in parts)


SMALL_BOUNDARY = {
    3: (
        (51, 1), (50, 1, 1), (29, 23), (27, 25),
        (27, 24, 1), (26, 25, 1), (25, 25, 2), (25, 25, 1, 1),
    ),
    4: ((49, 1, 1), (27, 23, 1), (25, 25, 1), (25, 24, 1, 1)),
    5: ((25, 23, 1, 1),),
}


def split_lower(parts: tuple[int, ...], b: int, row: int) -> int:
    budget = 2 * row - N * (R - 1)
    h_total = comb(N, 2) - row
    d = sum(parts)
    p_min = sum(s - 1 for s in parts)
    p_max = sum(comb(s, 2) for s in parts)
    y_min = deficiency(parts, b)
    cd, cb = comb(d, 2), comb(b, 2)
    clique = complete_lower(len(parts))
    multipartite = multipartite_lower(parts)
    answer = None
    for y in range(y_min, budget + 1):
        for q in range(3, cb + 1):
            p = d * (R - 1) - y - h_total + q
            if p_min <= p <= p_max:
                value_d = max(clique, multipartite, graph_lower(d, cd - p))
                value = value_d + graph_lower(b, cb - q)
                answer = value if answer is None else min(answer, value)
    assert answer is not None
    return answer


def small_survivors(row: int) -> dict[int, tuple[tuple[int, ...], ...]]:
    budget = 2 * row - N * (R - 1)
    answer = {}
    for b, candidates in SMALL_BOUNDARY.items():
        admissible = tuple(parts for parts in candidates if deficiency(parts, b) <= budget)
        live = tuple(parts for parts in admissible if multipartite_lower(parts) <= TARGET)
        if live:
            answer[b] = live
    return answer


def main() -> None:
    lines = ["PASS structural Albertson r=28 separator certificate audit"]

    # Let a=28-b.  Starting from b-1 odd singletons leaves 2a vertices.
    # For 4<=a<=22, at most two odd components can be raised to the zero-cost
    # threshold a (or a+1 when a is even), so the remaining b-3 singletons
    # each cost a-1=27-b.  Equality is attained by the displayed construction.
    middle = tuple((b, (b - 3) * (27 - b)) for b in range(6, 25))
    assert min(value for _, value in middle) == 63
    lines.append("middle_b=6..24 deficiency_min=(b-3)(27-b)>=63>53")

    # b=25: D=30 with at least 24 odd components; six excess vertices give
    # sum C(|C|,2)<=C(7,2)=21.  b=26 analogously gives C(5,2)=10.
    b25_upper = 30 * (25 - R + 1) + 53 + 2 * 21
    b26_upper = 29 * (26 - R + 1) + 53 + 2 * 10
    assert b25_upper == 35 < 25 * 3 == 75
    assert b26_upper == 44 < 26 * 2 == 52
    lines.append("b=25 internal_H_max=21 cross_upper<=35<cross_lower=75")
    lines.append("b=26 internal_H_max=10 cross_upper<=44<cross_lower=52")

    expected = {
        3: ((51, 1), (50, 1, 1)),
        4: ((49, 1, 1),),
    }
    for row in (768, 769):
        survivors = small_survivors(row)
        assert survivors == expected
        lines.append(
            f"row={row} b=3,4,5 boundary_candidates=13 "
            "survivors=b3:51,1;50,1,1|b4:49,1,1"
        )

        # At b=27 the only possibilities are 3+1^25, 2+1^26, 1^28.
        # The latter two force TK_28; the former loses to the split bound.
        b27_split = split_lower((3,) + (1,) * 25, 27, row)
        budget = 2 * row - N * (R - 1)
        cross_upper_2 = 28 * 0 + budget + 2
        gb_floor = -(-(27 * 27 - cross_upper_2) // 2)
        assert gb_floor > comb(26, 2)
        assert b27_split > TARGET

        # At b=28, 27 required odd components on 27 vertices force 1^27.
        b28_split = split_lower((1,) * 27, 28, row)
        assert b28_split > TARGET
        lines.append(
            f"row={row} terminal b27_split={b27_split} "
            f"K28_minus_edge_GB_floor={gb_floor}>325 b28_split={b28_split}>7098"
        )

    digest = sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    lines.append(f"audit_sha256={digest}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
