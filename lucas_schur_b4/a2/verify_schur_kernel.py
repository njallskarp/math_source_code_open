#!/usr/bin/env python3
"""Independent q-Pascal/Delannoy/Pieri check of the b=4 Schur recurrence."""

from __future__ import annotations

import argparse
import math


def add_shifted(left: list[int], right: list[int], shift: int) -> list[int]:
    result = [0] * max(len(left), len(right) + shift)
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index + shift] += value
    return result


def gaussian_rectangles(max_width: int, max_parts: int = 4) -> list[list[list[int]]]:
    """G[k][w] is the coefficient array of Gaussian(k+w,k)."""
    gaussian = [[[1] for _ in range(max_width + 1)] for _ in range(max_parts + 1)]
    for width in range(1, max_width + 1):
        for parts in range(1, max_parts + 1):
            gaussian[parts][width] = add_shifted(
                gaussian[parts][width - 1], gaussian[parts - 1][width], width
            )
    return gaussian


def delannoy(a: int, b: int) -> int:
    if a < 0 or b < 0:
        return 0
    return sum(
        2**j * math.comb(a, j) * math.comb(b, j)
        for j in range(min(a, b) + 1)
    )


def ell_table(limit: int) -> list[list[int]]:
    rows: list[list[int]] = []
    for n in range(limit + 1):
        row = []
        for r in range(n // 2 + 1):
            value = 0
            if n >= 1 and r < len(rows[n - 1]):
                value += rows[n - 1][r]
            if n >= 1 and r >= 1 and r - 1 < len(rows[n - 1]):
                value += rows[n - 1][r - 1]
            if n >= 2 and r >= 1 and r - 1 < len(rows[n - 2]):
                value += rows[n - 2][r - 1]
            if n == 0 and r == 0:
                value = 1
            row.append(value)
        rows.append(row)
    return rows


def ell(rows: list[list[int]], n: int, r: int) -> int:
    if n < 0 or r < 0 or 2 * r > n:
        return 0
    return rows[n][r]


def pieri_product(rows: list[list[int]], u: int, v: int) -> list[int]:
    """Schur coefficients of F_(u+1)F_(v+1), using range-add Pieri."""
    if u < 0 or v < 0:
        return []
    size = (u + v) // 2 + 1
    difference = [0] * (size + 1)
    for i, left in enumerate(rows[u]):
        for j, right in enumerate(rows[v]):
            start = i + j
            stop = start + min(u - 2 * i, v - 2 * j)
            weight = left * right
            difference[start] += weight
            difference[stop + 1] -= weight
    result = []
    running = 0
    for index in range(size):
        running += difference[index]
        result.append(running)
    return result


def value(values: list[int], index: int) -> int:
    if 0 <= index < len(values):
        return values[index]
    return 0


def direct_d(
    c: int, gaussian: list[list[list[int]]], rows: list[list[int]]
) -> list[int]:
    """Compute D_c from q-Pascal and the triangular Lucas involution."""
    width_four = gaussian[4][c]
    width_two = gaussian[2][2 * c]
    monomial_difference = [
        value(width_four, index) - value(width_two, index)
        for index in range(2 * c + 1)
    ]
    ordinary_schur = [
        coefficient - (monomial_difference[index - 1] if index else 0)
        for index, coefficient in enumerate(monomial_difference)
    ]
    assert all(coefficient >= 0 for coefficient in ordinary_schur)

    result = []
    for r in range(2 * c + 1):
        coefficient = 0
        for i in range(r + 1):
            coefficient += (-1) ** (i + 1) * ordinary_schur[i] * ell(
                rows, 4 * c - 2 * i, r - i
            )
        result.append(coefficient)
    return result


def explicit_rho(c: int, rows: list[list[int]]) -> list[int]:
    """Formula (13), computed only for the explicit audit bound."""
    result = pieri_product(rows, c - 3, 3 * c - 3)

    for j in range((c - 4) // 2 + 1):
        product = pieri_product(rows, 2 * c - 8 - 4 * j, 2 * c - 4)
        shift = 3 + 2 * j
        for u in range(len(result)):
            result[u] -= value(product, u - shift)

    for j in range(c - 5):
        shift = 9 + 2 * j
        n = 4 * c - 24 - 4 * j
        for u in range(len(result)):
            result[u] -= ell(rows, n, u - shift)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-c", type=int, default=300)
    parser.add_argument("--explicit-max-c", type=int, default=50)
    args = parser.parse_args()
    if args.max_c < 10:
        parser.error("need --max-c >= 10")
    if not 10 <= args.explicit_max_c <= args.max_c:
        parser.error("need 10 <= --explicit-max-c <= --max-c")

    gaussian = gaussian_rectangles(2 * args.max_c)
    rows = ell_table(4 * args.max_c)

    # Closed Delannoy formula independently audits the recurrence kernel.
    for n in range(min(80, 4 * args.max_c) + 1):
        for r in range(n // 2 + 1):
            closed = delannoy(n - r, r) - delannoy(n - r + 1, r - 1)
            assert rows[n][r] == closed, ("Delannoy kernel", n, r)

    coefficients: dict[int, list[int]] = {}
    least_d: tuple[int, int, int] | None = None
    least_rho: tuple[int, int, int] | None = None
    for c in range(4, args.max_c + 1):
        coefficients[c] = direct_d(c, gaussian, rows)
        nonzero_d = [
            (coefficient, c, r)
            for r, coefficient in enumerate(coefficients[c])
            if coefficient
        ]
        current_d = min(nonzero_d)
        least_d = current_d if least_d is None else min(least_d, current_d)
        assert current_d[0] > 0, ("negative D coefficient", c, current_d)

        if c >= 10:
            rho = [
                coefficients[c][u + 3]
                - value(coefficients[c - 6], u - 9)
                for u in range(2 * c - 2)
            ]
            current_rho = min((coefficient, c, u) for u, coefficient in enumerate(rho))
            least_rho = (
                current_rho if least_rho is None else min(least_rho, current_rho)
            )
            assert current_rho[0] > 0, ("negative rho coefficient", c, current_rho)

            if c <= args.explicit_max_c:
                assert rho == explicit_rho(c, rows), ("explicit rho formula", c)

    print("independent q-Pascal/Delannoy/Pieri verification passed")
    print(f"no negative d(c,r) for 4 <= c <= {args.max_c}")
    print(f"least nonzero d(c,r): {least_d}")
    print(f"rho(c,u) >= 1 for 10 <= c <= {args.max_c}")
    print(f"least rho(c,u): {least_rho}")
    print(f"explicit formula (13) audited through c = {args.explicit_max_c}")


if __name__ == "__main__":
    main()
