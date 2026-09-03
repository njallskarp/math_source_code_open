#!/usr/bin/env python3
"""Exact audit of the adjacent-layer proof for the Lucas b=4 family."""

from __future__ import annotations

import argparse


BASES = {
    4: [0, 0, 0, 1, 17, 112, 359, 562, 298],
    5: [0, 0, 0, 1, 25, 265, 1553, 5489, 11881, 14776, 7072],
    6: [0, 0, 0, 1, 33, 481, 4080, 22331, 82570, 209273, 357921, 382208, 169687],
    7: [
        0, 0, 0, 1, 41, 761, 8464, 62932, 330380, 1260272, 3536152,
        7277787, 10713402, 10379464, 4392776,
    ],
    8: [
        0, 0, 0, 1, 49, 1105, 15216, 143148, 975355, 4978186,
        19411857, 58412092, 135830579, 241830481, 320163336,
        289330066, 118298681,
    ],
    9: [
        0, 0, 0, 1, 57, 1513, 24848, 282948, 2372843, 15193467,
        75994995, 301241491, 954191962, 2422106612, 4911365195,
        7857954618, 9615754202, 8250609000, 3287685543,
    ],
}


def add_shifted(left: list[int], right: list[int], shift: int) -> list[int]:
    result = [0] * max(len(left), len(right) + shift)
    for index, coefficient in enumerate(left):
        result[index] += coefficient
    for index, coefficient in enumerate(right):
        result[index + shift] += coefficient
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


def difference(left: list[int], right: list[int], degree: int) -> list[int]:
    return [value(left, index) - value(right, index) for index in range(degree + 1)]


def direct_k(c: int, gaussian: list[list[list[int]]]) -> list[int]:
    """Schur coefficients of K_c from q-Pascal, without interval formula (17)."""
    h_c = difference(gaussian[4][c], gaussian[2][2 * c], 4 * c)
    old = difference(gaussian[4][c - 6], gaussian[2][2 * (c - 6)], 4 * (c - 6))
    monomial = [
        h_c[index + 3] - value(old, index - 9) for index in range(4 * c - 5)
    ]
    return [
        coefficient - (monomial[index - 1] if index else 0)
        for index, coefficient in enumerate(monomial[: 2 * c - 2])
    ]


def interval_k(c: int, r: int) -> int:
    base = int(0 <= r <= c - 3)
    intervals = sum(
        3 + 2 * j <= r <= 2 * c - 5 - 2 * j
        for j in range((c - 4) // 2 + 1)
    )
    spike = int(9 <= r <= 2 * c - 3 and (r - 9) % 2 == 0)
    return base + intervals + spike


def paired_rho(c: int, coefficients: list[int], rows: list[list[int]]) -> list[int]:
    """Build rho solely from the manifestly nonnegative paired blocks."""
    degree = 4 * c - 6
    result = [0] * (2 * c - 2)

    # General pairs j=0,...,c-4.  Formula (20) is used literally.
    for j in range(c - 3):
        a = coefficients[2 * j]
        b = coefficients[2 * j + 1]
        assert 0 <= b <= 2 * a
        m = degree - 4 * j + 1
        shift = 2 * j
        for u in range(len(result)):
            local = u - shift
            positive_difference = (
                ell(rows, m - 2, local)
                + ell(rows, m - 3, local - 2)
                + ell(rows, m - 4, local - 2)
            )
            result[u] += a * positive_difference
            result[u] += (2 * a - b) * ell(rows, m - 3, local - 1)

    # The final pair and final odd singleton form equation (23).
    terminal_shift = 2 * c - 6
    terminal = [1, 8, 18, 9]
    for offset, coefficient in enumerate(terminal):
        result[terminal_shift + offset] += coefficient
    return result


def direct_tau_rho(c: int, coefficients: list[int], rows: list[list[int]]) -> list[int]:
    """Apply tau to K_c as one alternating triangular transform."""
    degree = 4 * c - 6
    result = []
    for u in range(2 * c - 2):
        result.append(
            sum(
                (-1) ** r * coefficient * ell(rows, degree - 2 * r, u - r)
                for r, coefficient in enumerate(coefficients)
            )
        )
    return result


def direct_d(c: int, gaussian: list[list[list[int]]], rows: list[list[int]]) -> list[int]:
    h = difference(gaussian[4][c], gaussian[2][2 * c], 4 * c)
    first_difference = [
        coefficient - (h[index - 1] if index else 0)
        for index, coefficient in enumerate(h[: 2 * c + 1])
    ]
    return [
        sum(
            (-1) ** (i + 1)
            * first_difference[i]
            * ell(rows, 4 * c - 2 * i, r - i)
            for i in range(r + 1)
        )
        for r in range(2 * c + 1)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-c", type=int, default=300)
    args = parser.parse_args()
    if args.max_c < 10:
        parser.error("need --max-c >= 10")

    gaussian = gaussian_rectangles(2 * args.max_c)
    rows = ell_table(4 * args.max_c)

    for c, expected in BASES.items():
        assert direct_d(c, gaussian, rows) == expected, ("base", c)

    least_rho: tuple[int, int, int] | None = None
    for c in range(10, args.max_c + 1):
        direct = direct_k(c, gaussian)
        counted = [interval_k(c, r) for r in range(2 * c - 2)]
        assert direct == counted, ("interval formula", c)

        # Closed even/odd formulas and every boundary used in the proof.
        for j in range(c - 1):
            even = int(2 * j <= c - 3) + max(0, min(j - 1, c - j - 2))
            odd = (
                int(2 * j + 1 <= c - 3)
                + max(0, min(j, c - j - 2))
                + int(4 <= j <= c - 2)
            )
            assert counted[2 * j] == even
            assert counted[2 * j + 1] == odd
        assert counted[-4:] == [1, 2, 0, 1]

        paired = paired_rho(c, counted, rows)
        triangular = direct_tau_rho(c, direct, rows)
        assert paired == triangular, ("paired reconstruction", c)
        current = min((coefficient, c, u) for u, coefficient in enumerate(paired))
        least_rho = current if least_rho is None else min(least_rho, current)
        assert current[0] >= 1, ("rho sign", current)

    print("exact adjacent-layer pairing verification passed")
    print("six base arrays reproduced by independent q-Pascal inversion")
    print(f"interval counts and paired reconstruction checked for 10 <= c <= {args.max_c}")
    print(f"least rho(c,u): {least_rho}")


if __name__ == "__main__":
    main()
