#!/usr/bin/env python3
"""Exact arithmetic audit for the order-2k one-triple Kempe obstruction.

The recurrence code is intentionally self-contained.  It reconstructs the
same universal affine inputs and reviewed convex induced-subgraph recurrence
used in the independently published r=29 pass-1 certificate.
"""

from __future__ import annotations

from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from math import comb


K = 29
N = 58
ROWS = (838, 839, 840)
Z29 = 8281


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


BASE_LINES = (
    (Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(-3)),
    (Fraction(7, 3), Fraction(-25, 3)),
    (Fraction(4), Fraction(-103, 6)),
    (Fraction(37, 9), Fraction(-155, 9)),
    (Fraction(5), Fraction(-203, 9)),
)


def base_values(n: int) -> list[int]:
    return [
        max(ceil_fraction(a * q + b * (n - 2)) for a, b in BASE_LINES)
        for q in range(comb(n, 2) + 1)
    ]


def lower_hull(values: list[int]) -> list[int]:
    """Abscissae of the greatest convex minorant of point values."""
    hull: list[int] = []
    for x in range(len(values)):
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            left = Fraction(values[b] - values[a], b - a)
            right = Fraction(values[x] - values[b], x - b)
            if left < right:
                break
            hull.pop()
        hull.append(x)
    return hull


def hull_value(values: list[int], hull: list[int], x: Fraction) -> Fraction:
    if x.denominator == 1 and x.numerator in hull:
        return Fraction(values[x.numerator])
    j = bisect_right(hull, x) - 1
    if j == len(hull) - 1:
        j -= 1
    q0, q1 = hull[j], hull[j + 1]
    assert q0 <= x <= q1
    return Fraction(values[q0]) + Fraction(
        values[q1] - values[q0], q1 - q0
    ) * (x - q0)


def recursive_tables(max_order: int) -> dict[int, list[int]]:
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[int]] = {}
    for n in range(4, max_order + 1):
        values = base_values(n)
        for s in range(4, n):
            multiplier = Fraction(comb(n, s), comb(n - 4, s - 4))
            for q in range(len(values)):
                mean = Fraction(q * s * (s - 1), n * (n - 1))
                candidate = ceil_fraction(
                    multiplier * hull_value(tables[s], hulls[s], mean)
                )
                values[q] = max(values[q], candidate)
        tables[n] = values
        hulls[n] = lower_hull(values)
    return tables


def excess_histogram_audit(
    m: int, order57: list[int]
) -> tuple[int, int, int]:
    """Return histogram count, minimum deletion sum, number of minimizers."""
    total_excess = 2 * m - (K - 1) * N
    values = [order57[m - (K - 1) - x] for x in range(K)]
    histogram_count = 0
    best = 10**30
    minimizers = 0

    # Connected H forbids a universal vertex of G, hence x <= k-1 = 28.
    def visit(x: int, slots: int, remaining: int, cost: int) -> None:
        nonlocal histogram_count, best, minimizers
        if x == 0:
            if remaining != 0:
                return
            final_cost = cost + slots * values[0]
            histogram_count += 1
            if final_cost < best:
                best = final_cost
                minimizers = 1
            elif final_cost == best:
                minimizers += 1
            return
        for count in range(min(slots, remaining // x) + 1):
            visit(
                x - 1,
                slots - count,
                remaining - count * x,
                cost + count * values[x],
            )

    visit(K - 1, N, total_excess, 0)
    return histogram_count, best, minimizers


def aggregate_profiles(m: int) -> int:
    """Count formal scalar profiles allowed by all proved scalar constraints."""
    complement_edges = comb(N, 2) - m
    total_excess = 2 * m - (K - 1) * N
    p_upper = (m - (K - 1) - comb(K - 1, 2)) // 2
    count = 0
    for q in range(1, comb(K, 2) + 1):
        for p in range(2, min(comb(K - 1, 2), p_upper) + 1):
            c = complement_edges - K - q - p
            if not K <= c <= K * (K - 1):
                continue
            excess_a = K * (K - 1) - 2 * q - c
            excess_b = K * (K - 1) - 2 * p - c
            if excess_a < 0 or excess_b < 0:
                continue
            if excess_a + excess_b != total_excess:
                continue
            if q + p > comb(K, 2):
                continue
            count += 1
    return count


def main() -> None:
    assert K == 29 and N == 2 * K and Z29 == 8281
    tables = recursive_tables(57)
    budget = (N - 4) * (Z29 - 1)
    records = []
    for m in ROWS:
        complement_edges = comb(N, 2) - m
        excess = 2 * m - (K - 1) * N
        low_vertices = N - excess
        c_lower = complement_edges - K - comb(K, 2)
        p_upper = (m - (K - 1) - comb(K - 1, 2)) // 2
        histograms, deletion_min, minimizers = excess_histogram_audit(
            m, tables[57]
        )
        required_lift = budget + 1 - deletion_min
        profiles = aggregate_profiles(m)
        assert low_vertices > 0
        assert required_lift > 0
        assert profiles > 30
        records.append(
            (
                m,
                complement_edges,
                excess,
                low_vertices,
                c_lower,
                p_upper,
                histograms,
                deletion_min,
                minimizers,
                required_lift,
                profiles,
            )
        )

    print("parameters=k29,n58,Z29=8281,deletion_budget=447120")
    print("rows=" + ";".join(f"m{r[0]}:E{r[1]}:X{r[2]}" for r in records))
    print("degree28_min=" + ",".join(f"m{r[0]}:{r[3]}" for r in records))
    print("two_block=q+p<=406")
    print("cross_edge_min=" + ",".join(f"m{r[0]}:{r[4]}" for r in records))
    print("kempe_p_max=" + ",".join(f"m{r[0]}:{r[5]}" for r in records))
    print("no_TK29=Delta(H[N_G(v)])>=2,therefore_p>=2")
    print("excess_histograms=" + ",".join(f"m{r[0]}:{r[6]}" for r in records))
    print("deletion_sum_min=" + ",".join(f"m{r[0]}:{r[7]}" for r in records))
    print("deletion_minimizers=" + ",".join(f"m{r[0]}:{r[8]}" for r in records))
    print("required_sum_lift=" + ",".join(f"m{r[0]}:{r[9]}" for r in records))
    print("formal_scalar_profiles=" + ",".join(f"m{r[0]}:{r[10]}" for r in records))
    print("gate_decision=pause_r29_no_row_closed_and_profiles_gt_30")
    digest = sha256(repr(records).encode("ascii")).hexdigest()
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
