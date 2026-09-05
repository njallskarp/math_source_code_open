#!/usr/bin/env python3
"""Independent combinatorial audit of coverage and formula census."""

from __future__ import annotations

import itertools
import math
from collections import Counter


def totalizer_census(size: int, target: int) -> tuple[int, int, int]:
    """Return auxiliary variables, clauses including two units, and merges."""
    limit = target + 1

    def build(length: int) -> tuple[int, int, int, int]:
        if length == 1:
            return 1, 0, 0, 0
        left_length = length // 2
        right_length = length - left_length
        left_out, left_vars, left_clauses, left_merges = build(left_length)
        right_out, right_vars, right_clauses, right_merges = build(right_length)
        output = min(length, limit)
        clauses = 0
        for i in range(left_out + 1):
            for j in range(right_out + 1):
                clauses += int(1 <= i + j <= output)
                clauses += int(i + j + 1 <= output)
        return (
            output,
            left_vars + right_vars + output,
            left_clauses + right_clauses + clauses,
            left_merges + right_merges + 1,
        )

    _, variables, clauses, merges = build(size)
    return variables, clauses + 2, merges


def main() -> None:
    e_markings = Counter()
    labeled_partner_neighborhoods = 0
    for subset in itertools.combinations(range(13), 6):
        s = int(5 in subset)
        k = len(set(subset) & set(range(5)))
        p = s + k
        e_cells = (p, 6 - p, 6 - p, 1 + p)
        c_cells = (13 - p, 1 + p, 1 + p, 13 - p)
        if tuple(e_cells[i] + c_cells[i] for i in range(4)) != (13, 7, 7, 14):
            raise AssertionError((subset, e_cells, c_cells))
        central_choices = math.comb(14, 13 - p) * math.comb(14, 1 + p)
        labeled_partner_neighborhoods += central_choices
        e_markings[(s, k)] += 1
    expected_markings = {
        (s, k): math.comb(5, k) * math.comb(7, 6 - s - k)
        for s in (0, 1) for k in range(6)
    }
    if e_markings != Counter(expected_markings) or sum(e_markings.values()) != math.comb(13, 6):
        raise AssertionError(e_markings)
    if labeled_partner_neighborhoods != 2_425_062_140:
        raise AssertionError(labeled_partner_neighborhoods)

    exact_specs = (
        [(42, 20)] * 13 + [(42, 21)] * 30
        + [(12, 6)] * 12 + [(12, 8)] + [(13, 6)] * 30
        + [(20, 13), (861, 100), (861, 100), (210, 100), (210, 110)]
    )
    variables = clauses = merges = 0
    for size, target in exact_specs:
        new_variables, new_clauses, new_merges = totalizer_census(size, target)
        variables += new_variables
        clauses += new_clauses
        merges += new_merges
    if len(exact_specs) != 91 or (variables, clauses, merges) != (26_986, 507_636, 4_423):
        raise AssertionError((len(exact_specs), variables, clauses, merges))

    conjunction_clauses = 8 * math.comb(42, 2)
    local_clauses = 2 * (math.comb(21, 4) + math.comb(21, 5)) + 2 * (
        math.comb(42, 4) + math.comb(42, 5)
    )
    units = 42
    total_variables = 903 + 2 * math.comb(42, 2) + variables
    total_clauses = units + conjunction_clauses + local_clauses + clauses
    if (conjunction_clauses, local_clauses, total_variables, total_clauses) != (
        6_888, 1_977_864, 29_611, 2_492_430,
    ):
        raise AssertionError((conjunction_clauses, local_clauses, total_variables, total_clauses))

    print(
        "PASS marking_cover E_markings=1716 orbit_types=12 "
        "labeled_partner_neighborhoods=2425062140"
    )
    print(
        "PASS formula_census variables=29611 clauses=2492430 exact_sums=91 "
        "totalizer_variables=26986 totalizer_clauses=507636"
    )


if __name__ == "__main__":
    main()
