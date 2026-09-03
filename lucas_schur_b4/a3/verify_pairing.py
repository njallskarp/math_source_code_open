#!/usr/bin/env python3
"""Exact q-Pascal and Schur-layer audit of the Lucas (a,b)=(3,4) proof."""

from __future__ import annotations

import argparse


BASES = {
    2: [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    3: [0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 0, 1],
    4: [
        0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 3, 2, 4, 2, 4, 2, 4, 2, 4,
        2, 4, 1, 3, 0, 2,
    ],
    5: [
        0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 3, 2, 4, 3, 5, 4, 6, 4, 6,
        4, 6, 4, 6, 4, 6, 3, 5, 2, 4, 0, 2,
    ],
}


def add_shifted(left: list[int], right: list[int], shift: int) -> list[int]:
    result = [0] * max(len(left), len(right) + shift)
    for index, coefficient in enumerate(left):
        result[index] += coefficient
    for index, coefficient in enumerate(right):
        result[index + shift] += coefficient
    return result


def gaussian_rectangles(max_width: int) -> list[list[list[int]]]:
    """G[p][w] is the coefficient array of Gaussian(p+w,p)."""
    gaussian = [[[1] for _ in range(max_width + 1)] for _ in range(5)]
    for width in range(1, max_width + 1):
        for parts in range(1, 5):
            gaussian[parts][width] = add_shifted(
                gaussian[parts][width - 1], gaussian[parts - 1][width], width
            )
    return gaussian


def ell_table(limit: int) -> list[list[int]]:
    """ell[n][r] is [s_(n-r,r)] F_(n+1), from the Pieri recurrence."""
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


def R(n: int) -> int:
    return 0 if n < 0 else (n * n + 6 * n + 12) // 12


def S(n: int) -> int:
    return 0 if n < 0 else n // 3 + 1


def formula_h(k: int, i: int) -> int:
    return (
        restricted_234(i - 4)
        - sum(restricted_234(i - 3 * k - nu) for nu in range(1, 5))
        + sum(restricted_23(i - 4 * k - nu) for nu in range(1, 4))
    )


def parity_A_C(k: int, j: int) -> tuple[int, int]:
    if k % 2 == 0:
        t = k // 2
        u = j - 3 * t
        v = j - 4 * t
        A = (
            R(j - 2) - R(u - 1) - 2 * R(u - 2) - R(u - 3)
            + S(v - 1) + S(v - 2) + S(v - 3)
        )
        C = (
            2 * R(j - 2) - R(j - 3) + R(u) - R(u - 1)
            - 3 * R(u - 2) - R(u - 3) - S(v) + S(v - 1)
            + S(v - 2) + 2 * S(v - 3)
        )
    else:
        t = (k - 1) // 2
        u = j - 3 * t
        v = j - 4 * t - 2
        A = (
            R(j - 2) - R(u - 2) - R(u - 3) - R(u - 4) - R(u - 5)
            + S(v - 1) + S(v - 2) + S(v - 3)
        )
        C = (
            2 * R(j - 2) - R(j - 3) - R(u - 2) - R(u - 4)
            - 2 * R(u - 5) - S(v) + S(v - 1) + S(v - 2)
            + 2 * S(v - 3)
        )
    return A, C


def direct_h(k: int, gaussian: list[list[list[int]]]) -> list[int]:
    degree = 12 * k
    difference = [
        value(gaussian[4][3 * k], i) - value(gaussian[3][4 * k], i)
        for i in range(degree + 1)
    ]
    return [
        difference[i] - (difference[i - 1] if i else 0)
        for i in range(degree // 2 + 1)
    ]


def direct_lucas_schur(k: int, h: list[int], rows: list[list[int]]) -> list[int]:
    degree = 12 * k
    return [
        sum(
            (-1) ** i * h[i] * ell(rows, degree - 2 * i, r - i)
            for i in range(r + 1)
        )
        for r in range(degree // 2 + 1)
    ]


def paired_lucas_schur(k: int, h: list[int], rows: list[list[int]]) -> list[int]:
    """Reconstruct E_k solely from the nonnegative blocks (26)."""
    degree = 12 * k
    result = [0] * (degree // 2 + 1)
    for j in range(3 * k):
        A = h[2 * j]
        B = h[2 * j + 1]
        C = 2 * A - B
        assert A >= 0 and C >= 0
        m = degree - 4 * j + 1
        shift = 2 * j
        for r in range(len(result)):
            local = r - shift
            kernel = (
                ell(rows, m - 2, local)
                + ell(rows, m - 3, local - 2)
                + ell(rows, m - 4, local - 2)
            )
            result[r] += A * kernel + C * ell(rows, m - 3, local - 1)
    result[6 * k] += h[6 * k]
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=100)
    args = parser.parse_args()
    if args.max_k < 5:
        parser.error("need --max-k >= 5")

    gaussian = gaussian_rectangles(4 * args.max_k)
    rows = ell_table(12 * args.max_k)
    least: tuple[int, int, int] | None = None

    # Parity decompositions and closed forms for the restricted partitions.
    for n in range(12 * args.max_k + 1):
        assert restricted_234(2 * n) == R(n)
        assert restricted_234(2 * n + 1) == R(n - 1)
        assert restricted_23(2 * n) == S(n)
        assert restricted_23(2 * n + 1) == S(n - 1)

    for k in range(2, args.max_k + 1):
        h = direct_h(k, gaussian)
        assert h == [formula_h(k, i) for i in range(6 * k + 1)], ("formula", k)
        if k in BASES:
            assert h == BASES[k], ("base", k)

        for j in range(3 * k + 1):
            A, C = parity_A_C(k, j)
            assert A == h[2 * j], ("A formula", k, j)
            assert A >= 0, ("A sign", k, j, A)
            if j < 3 * k:
                assert C == 2 * h[2 * j] - h[2 * j + 1], ("C formula", k, j)
                assert C >= 0, ("C sign", k, j, C)

        direct = direct_lucas_schur(k, h, rows)
        paired = paired_lucas_schur(k, h, rows)
        assert direct == paired, ("paired reconstruction", k)
        assert direct[:4] == [0, 0, 0, 0]
        assert min(direct[4:]) > 0, ("strict Schur sign", k)
        current = min((coefficient, k, r) for r, coefficient in enumerate(direct) if coefficient)
        least = current if least is None else min(least, current)

    print("exact q-Pascal/Schur-layer verification passed")
    print(f"formulas (7), (9), (12), and (13) checked through k={args.max_k}")
    print(f"positive block reconstruction checked through k={args.max_k}")
    print(f"least nonzero Lucas Schur coefficient: {least}")


if __name__ == "__main__":
    main()
