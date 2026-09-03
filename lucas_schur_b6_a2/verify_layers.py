#!/usr/bin/env python3
"""Exact q-Pascal, KOH, recurrence, and Schur-layer audit for (2,6)."""

from __future__ import annotations

import argparse
from functools import lru_cache
from math import comb


Polynomial = tuple[int, ...]
ZERO: Polynomial = ()
ONE: Polynomial = (1,)


def trim(values: list[int]) -> Polynomial:
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(*polys: Polynomial) -> Polynomial:
    result = [0] * max((len(poly) for poly in polys), default=0)
    for poly in polys:
        for degree, coefficient in enumerate(poly):
            result[degree] += coefficient
    return trim(result)


def neg(poly: Polynomial) -> Polynomial:
    return tuple(-coefficient for coefficient in poly)


def mul(*polys: Polynomial) -> Polynomial:
    result = ONE
    for right in polys:
        if not result or not right:
            return ZERO
        product = [0] * (len(result) + len(right) - 1)
        for i, x in enumerate(result):
            for j, y in enumerate(right):
                product[i + j] += x * y
        result = trim(product)
    return result


def shift(poly: Polynomial, degree: int) -> Polynomial:
    return (0,) * degree + poly if poly else ZERO


def value(poly: Polynomial | list[int], index: int) -> int:
    return poly[index] if 0 <= index < len(poly) else 0


@lru_cache(maxsize=None)
def gaussian(n: int, r: int) -> Polynomial:
    if r < 0 or r > n or n < 0:
        return ZERO
    r = min(r, n - r)
    if r == 0:
        return ONE
    return add(gaussian(n - 1, r), shift(gaussian(n - 1, r - 1), n - r))


def width_six_koh(c: int) -> Polynomial:
    terms = [
        gaussian(6 * c + 1, 1),
        shift(mul(gaussian(c - 1, 1), gaussian(5 * c - 1, 1)), 2),
        shift(mul(gaussian(2 * c - 3, 1), gaussian(4 * c - 3, 1)), 4),
        shift(add(
            mul(gaussian(c - 2, 2), gaussian(4 * c - 3, 1)),
            gaussian(3 * c - 4, 2),
        ), 6),
        shift(mul(
            gaussian(c - 3, 1), gaussian(2 * c - 5, 1), gaussian(3 * c - 5, 1)
        ), 8),
        shift(add(
            mul(gaussian(c - 3, 3), gaussian(3 * c - 5, 1)),
            gaussian(2 * c - 5, 3),
        ), 12),
        shift(mul(gaussian(c - 4, 2), gaussian(2 * c - 6, 2)), 14),
        shift(mul(gaussian(c - 4, 4), gaussian(2 * c - 7, 1)), 20),
        shift(gaussian(c - 4, 6), 30),
    ]
    return add(*terms)


def width_two_tail(c: int) -> Polynomial:
    return add(
        *(shift(gaussian(6 * c - 4 * index + 1, 1), 2 * index) for index in range(15)),
        shift(gaussian(3 * c - 28, 2), 30),
    )


def explicit_k(c: int) -> Polynomial:
    positive = [
        mul(gaussian(c - 2, 1), gaussian(5 * c - 2, 1)),
        shift(mul(gaussian(2 * c - 3, 1), gaussian(4 * c - 3, 1)), 1),
        shift(add(
            mul(gaussian(c - 2, 2), gaussian(4 * c - 3, 1)),
            gaussian(3 * c - 4, 2),
        ), 3),
        shift(mul(
            gaussian(c - 3, 1), gaussian(2 * c - 5, 1), gaussian(3 * c - 5, 1)
        ), 5),
        shift(add(
            mul(gaussian(c - 3, 3), gaussian(3 * c - 5, 1)),
            gaussian(2 * c - 5, 3),
        ), 9),
        shift(mul(gaussian(c - 4, 2), gaussian(2 * c - 6, 2)), 11),
        shift(mul(gaussian(c - 4, 4), gaussian(2 * c - 7, 1)), 17),
    ]
    negative = add(*(
        shift(gaussian(6 * c - 4 * index + 1, 1), 2 * index - 3)
        for index in range(2, 15)
    ))
    return add(*positive, neg(negative))


def partition_table(parts: tuple[int, ...], limit: int) -> list[int]:
    values = [0] * (limit + 1)
    values[0] = 1
    for part in parts:
        for degree in range(part, limit + 1):
            values[degree] += values[degree - part]
    return values


def formula_h(c: int, i: int, p: list[int], v: list[int]) -> int:
    return (
        value(p, i)
        - value(v, i)
        - sum(value(p, i - c - nu) for nu in range(1, 7))
        + sum(
            value(p, i - 2 * c - mu - nu)
            for mu in range(1, 7)
            for nu in range(mu + 1, 7)
        )
    )


def direct_h(c: int) -> list[int]:
    difference = add(gaussian(c + 6, 6), neg(gaussian(3 * c + 2, 2)))
    return [
        value(difference, i) - value(difference, i - 1)
        for i in range(3 * c + 1)
    ]


def ell_table(limit: int) -> list[list[int]]:
    rows: list[list[int]] = []
    for n in range(limit + 1):
        row = []
        for r in range(n // 2 + 1):
            coefficient = int(n == 0 and r == 0)
            if n >= 1 and r < len(rows[n - 1]):
                coefficient += rows[n - 1][r]
            if n >= 1 and r >= 1 and r - 1 < len(rows[n - 1]):
                coefficient += rows[n - 1][r - 1]
            if n >= 2 and r >= 1 and r - 1 < len(rows[n - 2]):
                coefficient += rows[n - 2][r - 1]
            row.append(coefficient)
        rows.append(row)
    return rows


def ell(rows: list[list[int]], n: int, r: int) -> int:
    if n < 0 or r < 0 or 2 * r > n:
        return 0
    return rows[n][r]


def lucas_schur_from_h(c: int, layers: list[int], rows: list[list[int]]) -> list[int]:
    degree = 6 * c
    return [
        sum(
            (-1) ** (i + 1) * layers[i] * ell(rows, degree - 2 * i, r - i)
            for i in range(r + 1)
        )
        for r in range(degree // 2 + 1)
    ]


def remainder_schur(c: int, layers: list[int], rows: list[list[int]]) -> list[int]:
    degree = 6 * c - 6
    return [
        sum(
            (-1) ** i * layers[i] * ell(rows, degree - 2 * i, r - i)
            for i in range(r + 1)
        )
        for r in range(degree // 2 + 1)
    ]


def paired_remainder(c: int, layers: list[int], rows: list[list[int]]) -> list[int]:
    degree = 6 * c - 6
    result = [0] * (degree // 2 + 1)
    pair_count = len(layers) // 2
    for pair in range(pair_count):
        A = layers[2 * pair]
        B = layers[2 * pair + 1]
        C = 2 * A - B
        assert A >= 0 and C >= 0
        shift_ = 2 * pair
        m = degree - 4 * pair + 1
        for r in range(len(result)):
            local = r - shift_
            kernel = (
                ell(rows, m - 2, local)
                + ell(rows, m - 3, local - 2)
                + ell(rows, m - 4, local - 2)
            )
            result[r] += A * kernel + C * ell(rows, m - 3, local - 1)

    terminal = 2 * pair_count
    if terminal < len(layers):
        A = layers[terminal]
        assert terminal == degree // 2 and terminal % 2 == 0 and A >= 0
        result[terminal] += A
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-c", type=int, default=100)
    args = parser.parse_args()
    if args.max_c < 16:
        parser.error("need --max-c >= 16")

    p = partition_table((2, 3, 4, 5, 6), 6 * args.max_c)
    v = partition_table((2,), 6 * args.max_c)
    rows = ell_table(6 * args.max_c)
    schur_rows: dict[int, list[int]] = {}
    least: tuple[int, int, int] | None = None

    for c in range(6, args.max_c + 1):
        assert gaussian(c + 6, 6) == width_six_koh(c), ("width-six KOH", c)
        if c >= 10:
            assert gaussian(3 * c + 2, 2) == width_two_tail(c), ("width-two tail", c)

        layers = direct_h(c)
        expected = [formula_h(c, i, p, v) for i in range(3 * c + 1)]
        assert layers == expected, ("restricted-partition formula", c)
        direct = lucas_schur_from_h(c, layers, rows)
        schur_rows[c] = direct
        assert direct[:3] == [0, 0, 0]
        assert min(direct[3:]) > 0, ("direct Schur sign", c)
        assert direct[3] == 1
        for r in range(4, 3 * c + 1):
            lower = comb(6 * c - 8, r - 4) - (
                comb(6 * c - 8, r - 5) if r >= 5 else 0
            )
            assert direct[r] >= lower, ("ballot lower bound", c, r)

        current = min(
            (coefficient, c, r)
            for r, coefficient in enumerate(direct)
            if coefficient
        )
        least = current if least is None else min(least, current)

        if c < 16:
            continue
        previous_layers = direct_h(c - 10)
        k_layers = [
            layers[r + 3] - value(previous_layers, r - 27)
            for r in range(3 * c - 2)
        ]
        K = explicit_k(c)
        assert [value(K, r) - value(K, r - 1) for r in range(3 * c - 2)] == k_layers
        H = add(gaussian(c + 6, 6), neg(gaussian(3 * c + 2, 2)))
        H_previous = add(gaussian(c - 4, 6), neg(gaussian(3 * c - 28, 2)))
        assert H == add(shift(H_previous, 30), shift(K, 3)), ("KOH recurrence", c)

        for pair in range(len(k_layers) // 2):
            A = k_layers[2 * pair]
            C = 2 * A - k_layers[2 * pair + 1]
            assert A >= 0 and C >= 0, ("remainder layer sign", c, pair, A, C)
        if len(k_layers) % 2:
            assert k_layers[-1] >= 0

        remainder = remainder_schur(c, k_layers, rows)
        paired = paired_remainder(c, k_layers, rows)
        assert remainder == paired, ("paired remainder", c)
        assert min(remainder) >= 0
        reconstructed = [0] * (3 * c + 1)
        for r, coefficient in enumerate(schur_rows[c - 10]):
            reconstructed[r + 30] += coefficient
        for r, coefficient in enumerate(remainder):
            reconstructed[r + 3] += coefficient
        assert reconstructed == direct, ("Schur recurrence", c)

    print("exact q-Pascal/KOH/restricted-partition audit passed")
    print(f"ten bases and KOH-Schur recurrence checked through c={args.max_c}")
    print(f"positive remainder pairing checked through c={args.max_c}")
    print(f"least nonzero Lucas Schur coefficient: {least}")


if __name__ == "__main__":
    main()
