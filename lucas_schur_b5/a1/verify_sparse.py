#!/usr/bin/env python3
"""Direct Z[e1,e2] audit of the canonical Lucas (1,5) identity."""

from __future__ import annotations

import argparse
import math


Monomial = tuple[int, int]
Polynomial = dict[Monomial, int]
ZERO: Polynomial = {}
ONE: Polynomial = {(0, 0): 1}
E1: Polynomial = {(1, 0): 1}


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
    for (a1, a2), x in left.items():
        for (b1, b2), y in right.items():
            monomial = (a1 + b1, a2 + b2)
            result[monomial] = result.get(monomial, 0) + x * y
    return clean(result)


def e2_shift(poly: Polynomial, power: int) -> Polynomial:
    return {(a, b + power): coefficient for (a, b), coefficient in poly.items()}


def lucas_table(limit: int) -> list[Polynomial]:
    values = [ZERO, ONE]
    while len(values) <= limit:
        values.append(add(mul(E1, values[-1]), e2_shift(values[-2], 1)))
    return values


def lucas_binomial_table(values: list[Polynomial], limit: int) -> list[list[Polynomial]]:
    choose = [[ZERO for _ in range(6)] for _ in range(limit + 1)]
    for n in range(limit + 1):
        choose[n][0] = ONE
        if n <= 5:
            choose[n][n] = ONE
        for r in range(1, min(5, n - 1) + 1):
            choose[n][r] = add(
                mul(values[r + 1], choose[n - 1][r]),
                e2_shift(mul(values[n - r - 1], choose[n - 1][r - 1]), 1),
            )
    return choose


def width_five_expansion(k: int, f: list[Polynomial], choose: list[list[Polynomial]]) -> Polynomial:
    return add(
        f[5 * k + 1],
        e2_shift(mul(f[k - 1], f[4 * k - 1]), 2),
        e2_shift(mul(f[2 * k - 3], f[3 * k - 3]), 4),
        e2_shift(mul(choose[k - 2][2], f[3 * k - 3]), 6),
        e2_shift(mul(f[k - 3], choose[2 * k - 4][2]), 8),
        e2_shift(mul(choose[k - 3][3], f[2 * k - 5]), 12),
        e2_shift(choose[k - 3][5], 20),
    )


def difference(k: int, f: list[Polynomial], choose: list[list[Polynomial]]) -> Polynomial:
    return add(choose[k + 5][5], neg(f[5 * k + 1]))


def recurrence_remainder(k: int, f: list[Polynomial], choose: list[list[Polynomial]]) -> Polynomial:
    return add(
        e2_shift(mul(f[k - 1], f[4 * k - 1]), 2),
        e2_shift(mul(f[2 * k - 3], f[3 * k - 3]), 4),
        e2_shift(mul(choose[k - 2][2], f[3 * k - 3]), 6),
        e2_shift(mul(f[k - 3], choose[2 * k - 4][2]), 8),
        e2_shift(mul(choose[k - 3][3], f[2 * k - 5]), 12),
        e2_shift(f[5 * k - 39], 20),
    )


def schur_coefficients(poly: Polynomial, degree: int) -> list[int]:
    monomial = []
    for r in range(degree // 2 + 1):
        coefficient = 0
        for (e1_degree, e2_degree), value in poly.items():
            choice = r - e2_degree
            if 0 <= choice <= e1_degree:
                coefficient += value * math.comb(e1_degree, choice)
        monomial.append(coefficient)
    return [value - (monomial[r - 1] if r else 0) for r, value in enumerate(monomial)]


def ballot(n: int, r: int) -> int:
    return math.comb(n, r) - (math.comb(n, r - 1) if r else 0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=40)
    args = parser.parse_args()
    if args.max_k < 13:
        parser.error("need --max-k >= 13 to exercise the recurrence")

    largest_n = max(args.max_k + 5, 2 * args.max_k - 4)
    f = lucas_table(5 * args.max_k + 2)
    choose = lucas_binomial_table(f, largest_n)

    for k in range(5, args.max_k + 1):
        direct_binomial = choose[k + 5][5]
        expansion = width_five_expansion(k, f, choose)
        assert direct_binomial == expansion, ("width-five KOH image", k)
        delta = difference(k, f, choose)
        assert delta == add(expansion, neg(f[5 * k + 1]))
        assert all(coefficient >= 0 for coefficient in delta.values())

        schur = schur_coefficients(delta, 5 * k)
        assert schur[:2] == [0, 0]
        assert schur[2] == 1
        assert min(schur[2:]) > 0
        n = 4 * k - 2
        for r in range(2, 5 * k // 2 + 1):
            u = r - 2
            j = min(u, n - u)
            assert 0 <= j <= n // 2
            assert schur[r] >= ballot(n, j), ("ballot bound", k, r)

        if k >= 13:
            recurrence = add(
                e2_shift(difference(k - 8, f, choose), 20),
                recurrence_remainder(k, f, choose),
            )
            assert delta == recurrence, ("eight-step recurrence", k)
            assert all(coefficient >= 0 for coefficient in recurrence_remainder(k, f, choose).values())

    print("direct sparse Z[e1,e2] verification passed")
    print(f"seven-term identity and strict Schur support checked for 5<=k<={args.max_k}")
    print(f"eight-step positive recurrence checked for 13<=k<={args.max_k}")


if __name__ == "__main__":
    main()
