#!/usr/bin/env python3
"""Exact q-Pascal and Schur-layer audit of the Lucas (a,b)=(4,5) theorem."""

from __future__ import annotations

import argparse


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


def formula_g(k: int, i: int, p: list[int], q: list[int]) -> int:
    return (
        value(p, i - 5)
        - sum(value(p, i - 4 * k - nu) for nu in range(1, 6))
        + sum(
            value(p, i - 8 * k - mu - nu)
            for mu in range(1, 6)
            for nu in range(mu + 1, 6)
        )
        + sum(value(q, i - 5 * k - nu) for nu in range(1, 5))
    )


def direct_g(k: int, gaussian: list[list[list[int]]]) -> list[int]:
    degree = 20 * k
    difference = [
        value(gaussian[5][4 * k], i) - value(gaussian[4][5 * k], i)
        for i in range(degree + 1)
    ]
    return [
        difference[i] - (difference[i - 1] if i else 0)
        for i in range(degree // 2 + 1)
    ]


def direct_lucas_schur(k: int, g: list[int], rows: list[list[int]]) -> list[int]:
    degree = 20 * k
    return [
        sum(
            (-1) ** (i + 1) * g[i] * ell(rows, degree - 2 * i, r - i)
            for i in range(r + 1)
        )
        for r in range(degree // 2 + 1)
    ]


def paired_lucas_schur(k: int, g: list[int], rows: list[list[int]]) -> list[int]:
    degree = 20 * k
    result = [0] * (degree // 2 + 1)
    for pair in range(5 * k):
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
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=80)
    args = parser.parse_args()
    if args.max_k < 14:
        parser.error("need --max-k >= 14")

    gaussian = gaussian_rectangles(5 * args.max_k)
    p = partition_table((2, 3, 4, 5), 20 * args.max_k)
    q = partition_table((2, 3, 4), 20 * args.max_k)
    rows = ell_table(20 * args.max_k)
    least: tuple[int, int, int] | None = None

    for k in range(2, args.max_k + 1):
        layers = direct_g(k, gaussian)
        expected = [formula_g(k, i, p, q) for i in range(10 * k + 1)]
        assert layers == expected, ("restricted-partition formula", k)
        for pair in range(5 * k):
            A = layers[2 * pair + 1]
            C = 2 * A - layers[2 * pair + 2]
            assert A >= 0, ("A sign", k, pair, A)
            assert C >= 0, ("C sign", k, pair, C)

        direct = direct_lucas_schur(k, layers, rows)
        paired = paired_lucas_schur(k, layers, rows)
        assert direct == paired, ("paired reconstruction", k)
        assert direct[:5] == [0, 0, 0, 0, 0]
        assert min(direct[5:]) > 0, ("strict Schur sign", k)
        current = min((coefficient, k, r) for r, coefficient in enumerate(direct) if coefficient)
        least = current if least is None else min(least, current)

    print("exact q-Pascal/restricted-partition/Schur verification passed")
    print(f"formula and shifted adjacent domination checked through k={args.max_k}")
    print(f"positive block reconstruction checked through k={args.max_k}")
    print(f"least nonzero Lucas Schur coefficient: {least}")


if __name__ == "__main__":
    main()
