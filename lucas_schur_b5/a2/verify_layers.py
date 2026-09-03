#!/usr/bin/env python3
"""Exact q-Pascal and Schur-layer audit for canonical Lucas (a,b)=(2,5)."""

from __future__ import annotations

import argparse
from math import comb


def add_shifted(left: list[int], right: list[int], shift: int) -> list[int]:
    result = [0] * max(len(left), len(right) + shift)
    for index, coefficient in enumerate(left):
        result[index] += coefficient
    for index, coefficient in enumerate(right):
        result[index + shift] += coefficient
    return result


def gaussian_rectangles(max_width: int) -> list[list[list[int]]]:
    gaussian = [[[1] for _ in range(max_width + 1)] for _ in range(6)]
    for width in range(1, max_width + 1):
        for parts in range(1, 6):
            gaussian[parts][width] = add_shifted(
                gaussian[parts][width - 1], gaussian[parts - 1][width], width
            )
    return gaussian


def partition_table(parts: tuple[int, ...], limit: int) -> list[int]:
    values = [0] * (limit + 1)
    values[0] = 1
    for part in parts:
        for degree in range(part, limit + 1):
            values[degree] += values[degree - part]
    return values


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


def value(values: list[int], index: int) -> int:
    return values[index] if 0 <= index < len(values) else 0


def ell(rows: list[list[int]], n: int, r: int) -> int:
    if n < 0 or r < 0 or 2 * r > n:
        return 0
    return rows[n][r]


def formula_g(k: int, i: int, p: list[int], v: list[int]) -> int:
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


def direct_g(k: int, gaussian: list[list[list[int]]]) -> list[int]:
    degree = 10 * k
    difference = [
        value(gaussian[5][2 * k], i) - value(gaussian[2][5 * k], i)
        for i in range(degree + 1)
    ]
    return [
        difference[i] - (difference[i - 1] if i else 0)
        for i in range(degree // 2 + 1)
    ]


def direct_lucas_schur(k: int, g: list[int], rows: list[list[int]]) -> list[int]:
    degree = 10 * k
    return [
        sum(
            (-1) ** (i + 1) * g[i] * ell(rows, degree - 2 * i, r - i)
            for i in range(r + 1)
        )
        for r in range(degree // 2 + 1)
    ]


def paired_lucas_schur(k: int, g: list[int], rows: list[list[int]]) -> list[int]:
    degree = 10 * k
    result = [0] * (degree // 2 + 1)
    pair_count = (len(g) - 1) // 2
    for pair in range(pair_count):
        A = g[2 * pair + 1]
        B = g[2 * pair + 2]
        C = 2 * A - B
        assert A >= 0 and C >= 0
        shift = 2 * pair + 1
        m = degree - 4 * pair - 1
        for r in range(len(result)):
            local = r - shift
            kernel = (
                ell(rows, m - 2, local)
                + ell(rows, m - 3, local - 2)
                + ell(rows, m - 4, local - 2)
            )
            result[r] += A * kernel + C * ell(rows, m - 3, local - 1)

    terminal = 2 * pair_count + 1
    if terminal < len(g):
        A = g[terminal]
        assert terminal == degree // 2 and terminal % 2 == 1 and A >= 0
        result[terminal] += A  # e2^terminal F_1
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=100)
    args = parser.parse_args()
    if args.max_k < 28:
        parser.error("need --max-k >= 28")

    gaussian = gaussian_rectangles(5 * args.max_k)
    p = partition_table((2, 3, 4, 5), 10 * args.max_k)
    v = partition_table((2,), 10 * args.max_k)
    rows = ell_table(10 * args.max_k)
    least: tuple[int, int, int] | None = None

    for k in range(3, args.max_k + 1):
        degree = 10 * k
        layers = direct_g(k, gaussian)
        expected = [formula_g(k, i, p, v) for i in range(5 * k + 1)]
        assert layers == expected, ("restricted-partition formula", k)
        for pair in range((len(layers) - 1) // 2):
            A = layers[2 * pair + 1]
            C = 2 * A - layers[2 * pair + 2]
            assert A >= 0, ("A sign", k, pair, A)
            assert C >= 0, ("C sign", k, pair, C)
        if 5 * k % 2:
            assert layers[-1] >= 0, ("terminal sign", k, layers[-1])

        direct = direct_lucas_schur(k, layers, rows)
        paired = paired_lucas_schur(k, layers, rows)
        assert direct == paired, ("paired reconstruction", k)
        assert direct[:3] == [0, 0, 0]
        assert min(direct[3:]) > 0, ("strict Schur sign", k)
        assert direct[3] == 1, ("leading coefficient", k, direct[3])
        for r in range(4, degree // 2 + 1):
            lower_bound = comb(degree - 8, r - 4) - (
                comb(degree - 8, r - 5) if r >= 5 else 0
            )
            assert direct[r] >= lower_bound, ("ballot lower bound", k, r)
        current = min(
            (coefficient, k, r)
            for r, coefficient in enumerate(direct)
            if coefficient
        )
        least = current if least is None else min(least, current)

    print("exact q-Pascal/restricted-partition/Schur verification passed")
    print(f"formula and odd-even domination checked through k={args.max_k}")
    print(f"positive block reconstruction checked through k={args.max_k}")
    print(f"least nonzero Lucas Schur coefficient: {least}")


if __name__ == "__main__":
    main()
