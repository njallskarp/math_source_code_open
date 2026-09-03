#!/usr/bin/env python3
"""Independent integer-dictionary checks for the Lucas b=3 formulas."""

from __future__ import annotations

import argparse
from collections.abc import Iterable

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
    for (s_left, t_left), a in left.items():
        for (s_right, t_right), b in right.items():
            monomial = (s_left + s_right, t_left + t_right)
            result[monomial] = result.get(monomial, 0) + a * b
    return clean(result)


def t_shift(poly: Polynomial, power: int) -> Polynomial:
    return {
        (s_degree, t_degree + power): coefficient
        for (s_degree, t_degree), coefficient in poly.items()
    }


ZERO: Polynomial = {}
ONE: Polynomial = {(0, 0): 1}
S: Polynomial = {(1, 0): 1}


def lucas_table(limit: int) -> list[Polynomial]:
    values = [ZERO, ONE]
    for _ in range(1, limit):
        values.append(add(mul(S, values[-1]), t_shift(values[-2], 1)))
    return values


def lucas_binomial_table(
    values: list[Polynomial], limit: int, max_k: int = 3
) -> list[list[Polynomial]]:
    """Use the Sagan--Savage recurrence, not factorial division."""
    choose = [[ZERO for _ in range(max_k + 1)] for _ in range(limit + 1)]
    for n in range(limit + 1):
        choose[n][0] = ONE
        if n <= max_k:
            choose[n][n] = ONE
        for k in range(1, min(max_k, n - 1) + 1):
            choose[n][k] = add(
                mul(values[k + 1], choose[n - 1][k]),
                t_shift(mul(values[n - k - 1], choose[n - 1][k - 1]), 1),
            )
    return choose


def get_choose(choose: list[list[Polynomial]], n: int, k: int) -> Polynomial:
    if n < 0 or k < 0 or k > n or k >= len(choose[0]):
        return ZERO
    return choose[n][k]


def all_nonnegative(poly: Polynomial) -> bool:
    return all(coefficient >= 0 for coefficient in poly.values())


def sum_polys(polys: Iterable[Polynomial]) -> Polynomial:
    return add(*polys)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-c", type=int, default=40)
    parser.add_argument("--max-k", type=int, default=40)
    args = parser.parse_args()
    if args.max_c < 3 or args.max_k < 2:
        parser.error("need --max-c >= 3 and --max-k >= 2")

    limit = max(3 * args.max_c + 2, 6 * args.max_k + 2)
    f = lucas_table(limit)
    choose = lucas_binomial_table(f, limit)

    # Check (1) and its full iteration (4).
    for r in range(0, max(args.max_c, 3 * args.max_k) + 1):
        lhs = get_choose(choose, r + 2, 2)
        rhs = add(f[2 * r + 1], t_shift(get_choose(choose, r, 2), 2))
        assert lhs == rhs, ("width two", r)
    for k in range(2, args.max_k + 1):
        expanded = sum_polys(t_shift(f[6 * k - 4 * i + 1], 2 * i) for i in range((3 * k) // 2 + 1))
        assert get_choose(choose, 3 * k + 2, 2) == expanded, ("iteration four", k)

    # Check (2) and its full iteration (5).
    for r in range(1, max(args.max_c, 2 * args.max_k) + 1):
        rhs = add(
            f[3 * r + 1],
            t_shift(mul(f[r - 1], f[2 * r - 1]), 2),
            t_shift(get_choose(choose, r - 1, 3), 6),
        )
        assert get_choose(choose, r + 3, 3) == rhs, ("width three", r)
    for k in range(2, args.max_k + 1):
        first = (t_shift(f[6 * k - 12 * j + 1], 6 * j) for j in range(k // 2 + 1))
        second = (
            t_shift(mul(f[2 * k - 4 * j - 1], f[4 * k - 8 * j - 1]), 6 * j + 2)
            for j in range((2 * k - 1) // 4 + 1)
        )
        assert get_choose(choose, 2 * k + 3, 3) == sum_polys((*first, *second)), (
            "iteration five",
            k,
        )

    # Check theorem formulas (3) and (6), including positivity.
    for c in range(3, args.max_c + 1):
        lhs = add(get_choose(choose, c + 3, 3), neg(f[3 * c + 1]))
        rhs = t_shift(
            add(mul(f[c - 1], f[2 * c - 1]), t_shift(get_choose(choose, c - 1, 3), 4)),
            2,
        )
        assert lhs == rhs and all_nonnegative(lhs), ("a=1", c)

    for k in range(2, args.max_k + 1):
        lhs = add(get_choose(choose, 3 * k + 2, 2), neg(get_choose(choose, 2 * k + 3, 3)))
        rhs_terms = []
        for j in range(k // 2):
            n = 2 * k - 4 * j - 1
            rhs_terms.append(
                t_shift(add(mul(f[n - 1], f[2 * n]), t_shift(f[3 * n - 4], 1)), 6 * j + 3)
            )
        rhs = sum_polys(rhs_terms)
        assert lhs == rhs and all_nonnegative(lhs), ("a=2", k)

    print("pure Python exact-integer recurrence verification passed")
    print(f"a=1 checked for 3 <= c <= {args.max_c}")
    print(f"a=2 checked for 2 <= k <= {args.max_k}")


if __name__ == "__main__":
    main()
