#!/usr/bin/env python3
"""Independent sparse Z[e1,e2] verification of the Lucas (3,4) theorem."""

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
    """Sagan--Savage recurrence, with no division or Gaussian conversion."""
    choose = [[ZERO for _ in range(5)] for _ in range(limit + 1)]
    for n in range(limit + 1):
        choose[n][0] = ONE
        if n <= 4:
            choose[n][n] = ONE
        for k in range(1, min(4, n - 1) + 1):
            choose[n][k] = add(
                mul(values[k + 1], choose[n - 1][k]),
                e2_shift(mul(values[n - k - 1], choose[n - 1][k - 1]), 1),
            )
    return choose


def restricted_234(n: int) -> int:
    if n < 0:
        return 0
    return sum(
        1
        for c in range(n // 4 + 1)
        for b in range((n - 4 * c) // 3 + 1)
        if (n - 4 * c - 3 * b) % 2 == 0
    )


def restricted_23(n: int) -> int:
    if n < 0:
        return 0
    return sum(1 for b in range(n // 3 + 1) if (n - 3 * b) % 2 == 0)


def h(k: int, i: int) -> int:
    return (
        restricted_234(i - 4)
        - sum(restricted_234(i - 3 * k - nu) for nu in range(1, 5))
        + sum(restricted_23(i - 4 * k - nu) for nu in range(1, 4))
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
    return [
        coefficient - (monomial[index - 1] if index else 0)
        for index, coefficient in enumerate(monomial)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=40)
    args = parser.parse_args()
    if args.max_k < 2:
        parser.error("need --max-k >= 2")

    binomial_limit = 4 * args.max_k + 5
    lucas = lucas_table(12 * args.max_k + 2)
    choose = lucas_binomial_table(lucas, binomial_limit)

    for k in range(2, args.max_k + 1):
        degree = 12 * k
        direct = add(choose[3 * k + 4][4], neg(choose[4 * k + 3][3]))
        expansion = add(
            *(
                e2_shift(lucas[degree - 2 * i + 1], i, (-1) ** i * h(k, i))
                for i in range(6 * k + 1)
            )
        )
        assert direct == expansion, ("literal polynomial expansion", k)
        coefficients = schur_coefficients(direct, degree)
        assert coefficients[:4] == [0, 0, 0, 0]
        assert min(coefficients[4:]) > 0, ("Schur sign", k)

    print("independent sparse Z[e1,e2] verification passed")
    print(f"literal expansion (22) and strict Schur positivity checked for 2 <= k <= {args.max_k}")


if __name__ == "__main__":
    main()
