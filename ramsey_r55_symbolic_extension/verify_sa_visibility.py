#!/usr/bin/env python3
"""Independent exact checker for the R(5,5,42) SA visibility lemma.

Unlike derive_sa_visibility.py, this checker uses conditional expectations
and a truth table.  It does not implement or import polynomial arithmetic.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


N = 42
K4 = frozenset((0, 1, 2, 3))


def partial_assignments(max_size: int):
    yield {}
    for size in range(1, max_size + 1):
        for support in itertools.combinations(range(N), size):
            for values in itertools.product((0, 1), repeat=size):
                yield dict(zip(support, values, strict=True))


def atom_probability(partial: dict[int, int]) -> Fraction:
    return Fraction(1, 2 ** len(partial))


def conditional_sum(partial: dict[int, int], support: frozenset[int]) -> Fraction:
    fixed = sum(partial[v] for v in support if v in partial)
    free = len(support - partial.keys())
    return Fraction(fixed) + Fraction(free, 2)


def evaluate_red(bits: tuple[int, ...]) -> int:
    return (3 - sum(bits)) * bits[0] * bits[1] * bits[2]


def evaluate_red_target(bits: tuple[int, ...]) -> int:
    return -bits[0] * bits[1] * bits[2] * bits[3]


def evaluate_blue(bits: tuple[int, ...]) -> int:
    return (-1 + sum(bits)) * (1 - bits[0]) * (1 - bits[1]) * (1 - bits[2])


def evaluate_blue_target(bits: tuple[int, ...]) -> int:
    result = -1
    for bit in bits:
        result *= 1 - bit
    return result


def main() -> None:
    minima = {
        "red_k4": None,
        "blue_k4": None,
        "degree_low": None,
        "degree_high": None,
    }
    partial_count = 0
    check_count = 0
    all_vertices = frozenset(range(N))
    for partial in partial_assignments(2):
        partial_count += 1
        probability = atom_probability(partial)
        red = probability * (3 - conditional_sum(partial, K4))
        blue = probability * (-1 + conditional_sum(partial, K4))
        total = conditional_sum(partial, all_vertices)
        values = {
            "red_k4": red,
            "blue_k4": blue,
            "degree_low": probability * (total - 18),
            "degree_high": probability * (24 - total),
        }
        for name, value in values.items():
            if value < 0:
                raise AssertionError((name, partial, value))
            minima[name] = value if minima[name] is None else min(minima[name], value)
            check_count += 1

    truth_rows = 0
    for bits in itertools.product((0, 1), repeat=4):
        if evaluate_red(bits) != evaluate_red_target(bits):
            raise AssertionError(("red identity", bits))
        if evaluate_blue(bits) != evaluate_blue_target(bits):
            raise AssertionError(("blue identity", bits))
        truth_rows += 1

    print(json.dumps({
        "implementation": "independent conditional-expectation and truth-table checker",
        "arithmetic": "exact fractions",
        "partial_assignment_count": partial_count,
        "inequality_check_count": check_count,
        "truth_table_rows": truth_rows,
        "minimum_uniform_slack": {name: str(value) for name, value in minima.items()},
        "verified": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
