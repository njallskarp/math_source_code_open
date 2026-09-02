#!/usr/bin/env python3
"""Audit the exact signed-incidence first-fan normalization certificate."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(len(sys.argv) == 2, "usage: verify_incidence_budget_first_fan.py CERTIFICATE.json")
    certificate = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    variables = certificate["variables"]
    clauses = certificate["clauses"]
    clause_size = certificate["clause_size"]
    total = certificate["total_literal_occurrences"]

    require((variables, clauses, clause_size) == (42, 44, 4), "unexpected problem dimensions")
    require(total == clauses * clause_size == 176, "literal-occurrence total is not 44*4")
    require(certificate["bichromatic_minimum_per_variable"] == [1, 1], "coverage floor changed")
    require(certificate["nonsingular_minimum_total_degree"] == 4, "nonsingular floor changed")
    require(certificate["high_arity_singular_minimum_total_degree"] == 11, "singular floor changed")

    # Assume every singular variable has opposite-polarity degree at least 10.
    # One such variable costs at least 1+10; each nonsingular variable costs at least 2+2.
    one_singular_floor = 11 + (variables - 1) * 4
    two_singular_floor = 2 * 11 + (variables - 2) * 4
    require(one_singular_floor == 175, "one-singular incidence floor changed")
    require(two_singular_floor == 182 > total, "two singular vertices should exceed the budget")

    # With a unique singular vertex of degrees (1,m), exact total-incidence and
    # color-divisibility conditions leave one profile only.
    survivors: list[dict[str, int]] = []
    for m in range(10, total + 1):
        slack = total - ((1 + m) + (variables - 1) * 4)
        if slack < 0:
            continue
        for red_extra in range(slack + 1):
            blue_extra = slack - red_extra
            red_occurrences = 1 + 2 * (variables - 1) + red_extra
            blue_occurrences = m + 2 * (variables - 1) + blue_extra
            if red_occurrences % clause_size or blue_occurrences % clause_size:
                continue
            survivors.append(
                {
                    "m": m,
                    "slack": slack,
                    "red_extra": red_extra,
                    "blue_extra": blue_extra,
                    "red_clauses": red_occurrences // clause_size,
                    "blue_clauses": blue_occurrences // clause_size,
                }
            )

    expected = [{
        "m": 10,
        "slack": 1,
        "red_extra": 1,
        "blue_extra": 0,
        "red_clauses": 21,
        "blue_clauses": 23,
    }]
    require(survivors == expected, f"unexpected exceptional profiles: {survivors}")

    exceptional = certificate["sharp_dichotomy"]["exceptional_profile_up_to_color_exchange"]
    require(exceptional["unique_singular_vertex_degrees"] == [1, 10], "wrong singular profile")
    require(exceptional["red_blue_clause_counts"] == [21, 23], "wrong clause split")
    require(exceptional["one_other_vertex_degrees"] == [3, 2], "wrong slack placement")
    require(exceptional["remaining_vertex_count"] == 40, "wrong regular-vertex count")
    require(exceptional["remaining_vertex_degrees"] == [2, 2], "wrong regular profile")

    red_sum = 1 + 3 + 40 * 2
    blue_sum = 10 + 2 + 40 * 2
    require((red_sum, blue_sum) == (84, 92), "exceptional incidence sums changed")
    require((red_sum // 4, blue_sum // 4) == (21, 23), "exceptional clause counts changed")
    require(red_sum + blue_sum == total, "exceptional profile does not use all occurrences")
    require(certificate["normalized_first_fan_maximum_arity"] == 10, "normalization bound changed")

    print(
        "verified: every obstruction admits first fan m<=10; "
        "the m=10 exception is unique up to color exchange with "
        "clause split (21,23) and degrees (1,10),(3,2),40x(2,2)"
    )


if __name__ == "__main__":
    main()
