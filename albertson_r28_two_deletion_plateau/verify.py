#!/usr/bin/env python3
"""Exact certificate for the Albertson r=28 two-deletion plateau."""

from __future__ import annotations

from bisect import bisect_right
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import comb


BASE_LINES = (
    (Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(-3)),
    (Fraction(7, 3), Fraction(-25, 3)),
    (Fraction(37, 9), Fraction(-155, 9)),
    (Fraction(5), Fraction(-203, 9)),
)
Z28 = 7098
DENOMINATOR = comb(51, 2)


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
                candidate = ceil_fraction(multiplier * hull_value(tables[s], hulls[s], mean))
                values[q] = max(values[q], candidate)
        tables[n] = values
        hulls[n] = lower_hull(values)
    return tables


def histogram_text(values: tuple[int, ...]) -> str:
    counts = Counter(values)
    return ",".join(f"{value}^{counts[value]}" for value in sorted(counts))


def pair_baseline(table53: list[int], row: int, excesses: tuple[int, ...]) -> int:
    """Sum the two-deletion bounds as if every vertex pair were an edge of G."""
    return sum(
        table53[row - 53 - excesses[i] - excesses[j]]
        for i in range(55)
        for j in range(i + 1, 55)
    )


def penalty(table53: list[int], row: int, excess_sum: int) -> int:
    """Loss when the deleted pair is a nonedge of G, hence an edge of H."""
    return table53[row - 53 - excess_sum] - table53[row - 54 - excess_sum]


def row_768_penalty_interval(
    table53: list[int], extras: tuple[int, ...], singleton_excesses: tuple[int, int]
) -> tuple[int, int, str]:
    """Bound the penalty using only degrees and the forbidden singleton edge."""
    edge_count = comb(55, 2) - 768
    singleton_degree_sum = sum(27 - x for x in singleton_excesses)
    assert singleton_excesses in ((25, 25), (24, 25))
    assert all(penalty(table53, 768, w + x) == 26 for w in singleton_excesses for x in (0,) + extras)

    # All remaining edges have penalty 30 except the indicated exceptional
    # edges, whose penalty is 29.  The bounds count those exceptional edges.
    if extras == (1,):
        assert penalty(table53, 768, 0) == 30
        assert penalty(table53, 768, 1) == 29
        exceptional_min, exceptional_max = 24, 26
        reason = "24<=e_01<=26"
    elif extras == (2,):
        assert penalty(table53, 768, 0) == 30
        assert penalty(table53, 768, 2) == 29
        exceptional_min, exceptional_max = 23, 25
        reason = "23<=e_02<=25"
    elif extras == (1, 1):
        assert penalty(table53, 768, 0) == 30
        assert penalty(table53, 768, 1) == penalty(table53, 768, 2) == 29
        exceptional_min, exceptional_max = 47, 52
        reason = "47<=e_01+e_11<=52"
    else:
        raise AssertionError(extras)

    constant = 30 * edge_count - 4 * singleton_degree_sum
    return constant - exceptional_max, constant - exceptional_min, reason


def row_769_penalty_interval(
    table53: list[int], extras: tuple[int, ...], singleton_excesses: tuple[int, int]
) -> tuple[int, int, str]:
    """The sole positive correction is an edge of excess types zero and one."""
    edge_count = comb(55, 2) - 769
    singleton_degree_sum = sum(27 - x for x in singleton_excesses)
    rare = (0,) + extras
    assert singleton_excesses in ((25, 25), (24, 25))
    assert all(penalty(table53, 769, w + x) == 26 for w in singleton_excesses for x in rare)
    for i, a in enumerate(rare):
        for b in rare[i:]:
            expected = 30 if {a, b} == {0, 1} else 29
            assert penalty(table53, 769, a + b) == expected

    number_excess_one = extras.count(1)
    lower = 29 * edge_count - 3 * singleton_degree_sum
    upper = lower + 26 * number_excess_one
    return lower, upper, f"0<=e_01<={26 * number_excess_one}"


PROFILES = {
    768: (
        ((25, 25), (1,)),
        ((24, 25), (2,)),
        ((24, 25), (1, 1)),
    ),
    769: (
        ((25, 25), (3,)),
        ((24, 25), (4,)),
        ((25, 25), (1, 2)),
        ((24, 25), (1, 3)),
        ((24, 25), (2, 2)),
        ((25, 25), (1, 1, 1)),
        ((24, 25), (1, 1, 2)),
        ((24, 25), (1, 1, 1, 1)),
    ),
}


def main() -> None:
    table53 = build_tables(53)[53]
    target_numerator = DENOMINATOR * (Z28 - 1) + 1
    output = [
        "PASS Albertson r=28 two-deletion plateau",
        f"denominator={DENOMINATOR} target_numerator={target_numerator}",
    ]
    row_bounds: dict[int, set[int]] = {768: set(), 769: set()}
    best_shortfalls: dict[int, int] = {}

    for row, profiles in PROFILES.items():
        for singleton_excesses, extras in profiles:
            values = tuple(sorted(singleton_excesses + extras + (0,) * (53 - len(extras))))
            assert len(values) == 55 and sum(values) == 2 * row - 55 * 27
            baseline = pair_baseline(table53, row, values)
            if row == 768:
                penalty_min, penalty_max, reason = row_768_penalty_interval(
                    table53, extras, singleton_excesses
                )
            else:
                penalty_min, penalty_max, reason = row_769_penalty_interval(
                    table53, extras, singleton_excesses
                )
            sum_min = baseline - penalty_max
            sum_max = baseline - penalty_min
            bound_min = ceil_fraction(Fraction(sum_min, DENOMINATOR))
            bound_max = ceil_fraction(Fraction(sum_max, DENOMINATOR))
            assert bound_min == bound_max
            row_bounds[row].add(bound_min)
            best_shortfalls[row] = min(
                best_shortfalls.get(row, 10**30), target_numerator - sum_max
            )
            output.append(
                f"row={row} profile={histogram_text(values)} baseline={baseline} "
                f"penalty=[{penalty_min},{penalty_max}] sum=[{sum_min},{sum_max}] "
                f"bound={bound_min} reason={reason}"
            )

    assert row_bounds == {768: {7063}, 769: {7095}}
    assert best_shortfalls == {768: 43486, 769: 3099}
    output.append("row=768 universal_two_deletion_bound=7063 optimistic_target_shortfall=43486")
    output.append("row=769 universal_two_deletion_bound=7095 optimistic_target_shortfall=3099")
    digest = sha256(("\n".join(output) + "\n").encode()).hexdigest()
    output.append(f"certificate_sha256={digest}")
    print("\n".join(output))


if __name__ == "__main__":
    main()
