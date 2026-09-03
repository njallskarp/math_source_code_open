#!/usr/bin/env python3
"""Definition-level sparse Z[e1,e2] audit for canonical Lucas (2,5)."""

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


def e2_shift(poly: Polynomial, power: int, scale: int = 1) -> Polynomial:
    return {
        (e1_degree, e2_degree + power): scale * coefficient
        for (e1_degree, e2_degree), coefficient in poly.items()
        if scale * coefficient
    }


def lucas_table(limit: int) -> list[Polynomial]:
    values = [ZERO, ONE]
    for _ in range(1, limit):
        values.append(add(mul(E1, values[-1]), e2_shift(values[-2], 1)))
    return values


def lucas_binomial_table(values: list[Polynomial], limit: int) -> list[list[Polynomial]]:
    choose = [[ZERO for _ in range(6)] for _ in range(limit + 1)]
    for n in range(limit + 1):
        choose[n][0] = ONE
        if n <= 5:
            choose[n][n] = ONE
        for k in range(1, min(5, n - 1) + 1):
            choose[n][k] = add(
                mul(values[k + 1], choose[n - 1][k]),
                e2_shift(mul(values[n - k - 1], choose[n - 1][k - 1]), 1),
            )
    return choose


def partition_table(parts: tuple[int, ...], limit: int) -> list[int]:
    values = [0] * (limit + 1)
    values[0] = 1
    for part in parts:
        for degree in range(part, limit + 1):
            values[degree] += values[degree - part]
    return values


def value(values: list[int], index: int) -> int:
    return values[index] if 0 <= index < len(values) else 0


def g(k: int, i: int, p: list[int], v: list[int]) -> int:
    return (
        value(p, i)
        - value(v, i)
        - sum(value(p, i - 2 * k - nu) for nu in range(1, 6))
        + sum(
            value(p, i - 4 * k - mu - nu)
            for mu in range(1, 6)
            for nu in range(mu + 1, 6)
        )
    )


def schur_coefficients(poly: Polynomial, degree: int) -> list[int]:
    monomial = []
    for r in range(degree // 2 + 1):
        coefficient = 0
        for (e1_degree, e2_degree), value_ in poly.items():
            choice = r - e2_degree
            if 0 <= choice <= e1_degree:
                coefficient += value_ * math.comb(e1_degree, choice)
        monomial.append(coefficient)
    return [
        coefficient - (monomial[index - 1] if index else 0)
        for index, coefficient in enumerate(monomial)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=50)
    args = parser.parse_args()
    if args.max_k < 3:
        parser.error("need --max-k >= 3")

    degree_limit = 10 * args.max_k
    binomial_limit = 5 * args.max_k + 2
    lucas = lucas_table(degree_limit + 2)
    choose = lucas_binomial_table(lucas, binomial_limit)
    p = partition_table((2, 3, 4, 5), degree_limit)
    v = partition_table((2,), degree_limit)

    for k in range(3, args.max_k + 1):
        degree = 10 * k
        direct = add(choose[5 * k + 2][2], neg(choose[2 * k + 5][5]))
        expansion = add(*(
            e2_shift(lucas[degree - 2 * i + 1], i, (-1) ** (i + 1) * g(k, i, p, v))
            for i in range(degree // 2 + 1)
        ))
        assert direct == expansion, ("literal polynomial expansion", k)
        coefficients = schur_coefficients(direct, degree)
        assert coefficients[:3] == [0, 0, 0]
        assert min(coefficients[3:]) > 0, ("Schur sign", k)

    print("independent sparse Z[e1,e2] verification passed")
    print(f"literal expansion and strict Schur positivity checked for 3 <= k <= {args.max_k}")


if __name__ == "__main__":
    main()
