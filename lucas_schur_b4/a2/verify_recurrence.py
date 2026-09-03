#!/usr/bin/env python3
"""Exact Z[e1,e2] checks for the Lucas b=4 KOH--Schur recurrence."""

from __future__ import annotations

import argparse
import math

Monomial = tuple[int, int]
Polynomial = dict[Monomial, int]


def clean(poly: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def add(*polys: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def neg(poly: Polynomial) -> Polynomial:
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for (e1_left, e2_left), a in left.items():
        for (e1_right, e2_right), b in right.items():
            monomial = (e1_left + e1_right, e2_left + e2_right)
            result[monomial] = result.get(monomial, 0) + a * b
    return clean(result)


def e2_shift(poly: Polynomial, power: int) -> Polynomial:
    return {
        (e1_degree, e2_degree + power): coefficient
        for (e1_degree, e2_degree), coefficient in poly.items()
    }


ZERO: Polynomial = {}
ONE: Polynomial = {(0, 0): 1}
E1: Polynomial = {(1, 0): 1}


def lucas_table(limit: int) -> list[Polynomial]:
    values = [ZERO, ONE]
    for _ in range(1, limit):
        values.append(add(mul(E1, values[-1]), e2_shift(values[-2], 1)))
    return values


def lucas_binomial_table(
    values: list[Polynomial], limit: int, max_k: int = 4
) -> list[list[Polynomial]]:
    """Sagan--Savage recurrence; no factorial quotient or division."""
    choose = [[ZERO for _ in range(max_k + 1)] for _ in range(limit + 1)]
    for n in range(limit + 1):
        choose[n][0] = ONE
        if n <= max_k:
            choose[n][n] = ONE
        for k in range(1, min(max_k, n - 1) + 1):
            choose[n][k] = add(
                mul(values[k + 1], choose[n - 1][k]),
                e2_shift(mul(values[n - k - 1], choose[n - 1][k - 1]), 1),
            )
    return choose


def get_choose(choose: list[list[Polynomial]], n: int, k: int) -> Polynomial:
    if n < 0 or k < 0 or k > n or k >= len(choose[0]):
        return ZERO
    return choose[n][k]


def schur_coefficients(poly: Polynomial, degree: int) -> list[int]:
    """Two-variable Schur coefficients from consecutive monomial weights."""
    monomial = []
    for r in range(degree // 2 + 1):
        coefficient = 0
        for (e1_degree, e2_degree), value in poly.items():
            choice = r - e2_degree
            if 0 <= choice <= e1_degree:
                coefficient += value * math.comb(e1_degree, choice)
        monomial.append(coefficient)
    return [
        value - (monomial[index - 1] if index else 0)
        for index, value in enumerate(monomial)
    ]


def all_nonnegative(values: list[int]) -> bool:
    return all(value >= 0 for value in values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-c", type=int, default=60)
    args = parser.parse_args()
    if args.max_c < 10:
        parser.error("need --max-c >= 10")

    limit = 4 * args.max_c + 3
    lucas = lucas_table(limit)
    choose = lucas_binomial_table(lucas, limit)

    # Width-two KOH identity and its iteration.
    for r in range(0, 2 * args.max_c + 1):
        lhs = get_choose(choose, r + 2, 2)
        rhs = add(lucas[2 * r + 1], e2_shift(get_choose(choose, r, 2), 2))
        assert lhs == rhs, ("width two", r)
        expanded = add(
            *(
                e2_shift(lucas[2 * r - 4 * j + 1], 2 * j)
                for j in range(r // 2 + 1)
            )
        )
        assert lhs == expanded, ("width two iteration", r)

    differences: dict[int, Polynomial] = {}
    for c in range(4, args.max_c + 1):
        # The five width-four KOH summands.
        width_four = add(
            lucas[4 * c + 1],
            e2_shift(mul(lucas[c - 1], lucas[3 * c - 1]), 2),
            e2_shift(get_choose(choose, 2 * c - 2, 2), 4),
            e2_shift(
                mul(get_choose(choose, c - 2, 2), lucas[2 * c - 3]), 6
            ),
            e2_shift(get_choose(choose, c - 2, 4), 12),
        )
        assert get_choose(choose, c + 4, 4) == width_four, ("width four", c)

        differences[c] = add(
            get_choose(choose, 2 * c + 2, 2),
            neg(get_choose(choose, c + 4, 4)),
        )
        d_coefficients = schur_coefficients(differences[c], 4 * c)
        assert all_nonnegative(d_coefficients), ("D Schur sign", c)

        if c >= 10:
            remainder = add(
                mul(lucas[c - 2], lucas[3 * c - 2]),
                neg(
                    e2_shift(
                        mul(get_choose(choose, c - 2, 2), lucas[2 * c - 3]),
                        3,
                    )
                ),
                neg(e2_shift(get_choose(choose, 2 * c - 10, 2), 9)),
            )
            recurrence_rhs = add(
                e2_shift(differences[c - 6], 12), e2_shift(remainder, 3)
            )
            assert differences[c] == recurrence_rhs, ("six-step recurrence", c)
            rho = schur_coefficients(remainder, 4 * c - 6)
            assert min(rho) >= 1, ("remainder Schur sign", c)

    print("exact Z[e1,e2] KOH and recurrence verification passed")
    print(f"D_c is Schur-positive for 4 <= c <= {args.max_c}")
    print(f"rho(c,u) >= 1 for 10 <= c <= {args.max_c}")


if __name__ == "__main__":
    main()
