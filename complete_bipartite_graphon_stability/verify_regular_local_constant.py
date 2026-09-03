#!/usr/bin/env python3
"""Exact finite-step audit of the sharp regular-local K_(s,t) constant.

The checker double-centers finite adjacency matrices to obtain symmetric
regular kernels.  It evaluates the final inequalities directly rather than
using the signed-subgraph domination from the analytic proof.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
import platform
from fractions import Fraction
from typing import Sequence


Matrix = tuple[tuple[Fraction, ...], ...]


def adjacency_matrix(n: int, edge_mask: int) -> Matrix:
    """Decode lexicographically ordered simple-graph edges."""
    if n < 1:
        raise ValueError("n must be positive")
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    bit = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (edge_mask >> bit) & 1:
                matrix[i][j] = matrix[j][i] = Fraction(1)
            bit += 1
    return tuple(tuple(row) for row in matrix)


def double_center(matrix: Sequence[Sequence[Fraction]]) -> Matrix:
    """Apply H A H for the uniform measure, giving zero row sums."""
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be nonempty and square")
    if any(matrix[i][j] != matrix[j][i] for i in range(n) for j in range(n)):
        raise ValueError("matrix must be symmetric")
    row_means = tuple(sum(row) / n for row in matrix)
    grand_mean = sum(row_means) / n
    centered = tuple(
        tuple(matrix[i][j] - row_means[i] - row_means[j] + grand_mean for j in range(n))
        for i in range(n)
    )
    if any(sum(row) != 0 for row in centered):
        raise AssertionError("double centering failed")
    return centered


def scale_to_radius(matrix: Matrix, radius: Fraction) -> Matrix:
    if radius <= 0:
        raise ValueError("radius must be positive")
    maximum = max(abs(value) for row in matrix for value in row)
    if maximum == 0:
        raise ValueError("cannot scale the zero matrix")
    return tuple(tuple(radius * value / maximum for value in row) for row in matrix)


def matrix_rank(matrix: Matrix) -> int:
    """Compute exact rank by rational Gaussian elimination."""
    rows = [list(row) for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (index for index in range(rank, row_count) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for index in range(row_count):
            if index == rank or not rows[index][column]:
                continue
            multiplier = rows[index][column]
            rows[index] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(rows[index], rows[rank])
            ]
        rank += 1
    return rank


def add_constant(matrix: Matrix, p: Fraction) -> Matrix:
    return tuple(tuple(p + value for value in row) for row in matrix)


def kst_density(matrix: Matrix, s: int, t: int) -> Fraction:
    """Compute a uniform step-graphon K_(s,t) density via common neighbors."""
    if s < 2 or t < 2:
        raise ValueError("s and t must both be at least two")
    n = len(matrix)
    total = Fraction(0)
    for left in itertools.product(range(n), repeat=s):
        common = sum(math.prod(matrix[x][y] for x in left) for y in range(n)) / n
        total += common**t
    return total / n**s


def c4_density(matrix: Matrix) -> Fraction:
    """Compute t(C4,F) directly from its four vertex variables."""
    n = len(matrix)
    total = Fraction(0)
    for x1, y1, x2, y2 in itertools.product(range(n), repeat=4):
        total += (
            matrix[x1][y1]
            * matrix[x2][y1]
            * matrix[x2][y2]
            * matrix[x1][y2]
        )
    return total / n**4


def cut_norm(matrix: Matrix) -> Fraction:
    """Enumerate the exact uniform step-kernel cut norm."""
    n = len(matrix)
    best = Fraction(0)
    for first_mask in range(1 << n):
        for second_mask in range(1 << n):
            integral = sum(
                matrix[i][j]
                for i in range(n)
                for j in range(n)
                if (first_mask >> i) & 1 and (second_mask >> j) & 1
            ) / n**2
            best = max(best, abs(integral))
    return best


def remainder_factor(edge_count: int, r: Fraction) -> Fraction:
    return sum(
        Fraction(math.comb(edge_count, k)) * r ** (k - 4)
        for k in range(6, edge_count + 1)
    )


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def check_instance(
    f_matrix: Matrix, p: Fraction, r: Fraction, s: int, t: int
) -> tuple[Fraction, ...]:
    n = len(f_matrix)
    if any(sum(row) != 0 for row in f_matrix):
        raise AssertionError("kernel is not regular")
    eta = max(abs(value) for row in f_matrix for value in row)
    if eta > r * p:
        raise AssertionError("kernel exceeds the declared local radius")
    w_matrix = add_constant(f_matrix, p)
    if any(not 0 <= value <= 1 for row in w_matrix for value in row):
        raise AssertionError("p+F is not a graphon")

    density = kst_density(w_matrix, s, t)
    edge_count = s * t
    delta = density - p**edge_count
    c4 = c4_density(f_matrix)
    cut = cut_norm(f_matrix)
    copies = math.comb(s, 2) * math.comb(t, 2)
    leading = copies * p ** (edge_count - 4) * c4
    factor = remainder_factor(edge_count, r)
    error_bound = factor * p ** (edge_count - 4) * c4

    if abs(delta - leading) > error_bound:
        raise AssertionError(
            f"remainder failed for n={n}, s={s}, t={t}: "
            f"error={abs(delta-leading)}, bound={error_bound}"
        )
    if 256 * cut**4 > c4:
        raise AssertionError("centered cut--Schatten inequality failed")
    if factor < copies and 256 * p ** (edge_count - 4) * (copies - factor) * cut**4 > delta:
        raise AssertionError("combined local constant failed")
    if delta < 0:
        raise AssertionError("Sidorenko deficit is negative")
    return density, delta, c4, cut, leading, error_bound


def run_checks(max_atoms: int, max_part: int) -> tuple[int, int, int, str]:
    if max_atoms < 2:
        raise ValueError("max_atoms must be at least two")
    if max_part < 2:
        raise ValueError("max_part must be at least two")

    p = Fraction(2, 5)
    radii = (Fraction(1, 50), Fraction(1, 100))
    kernels = 0
    higher_rank_kernels = 0
    instances = 0
    digest = hashlib.sha256()
    for n in range(2, max_atoms + 1):
        edge_count = n * (n - 1) // 2
        for edge_mask in range(1 << edge_count):
            centered = double_center(adjacency_matrix(n, edge_mask))
            if all(value == 0 for row in centered for value in row):
                continue
            kernels += 1
            if matrix_rank(centered) > 1:
                higher_rank_kernels += 1
            for r in radii:
                f_matrix = scale_to_radius(centered, r * p)
                for s in range(2, max_part + 1):
                    for t in range(2, max_part + 1):
                        values = check_instance(f_matrix, p, r, s, t)
                        record = ":".join(
                            (
                                str(n),
                                str(edge_mask),
                                fraction_text(r),
                                str(s),
                                str(t),
                                *(fraction_text(value) for value in values),
                            )
                        )
                        digest.update(record.encode("ascii"))
                        digest.update(b"\n")
                        instances += 1
    return kernels, higher_rank_kernels, instances, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-atoms", type=int, default=4)
    parser.add_argument("--max-part", type=int, default=4)
    args = parser.parse_args()

    kernels, higher_rank_kernels, instances, digest = run_checks(
        args.max_atoms, args.max_part
    )
    print(f"python={platform.python_version()}")
    print("p=2/5")
    print("radii=1/50,1/100")
    print(f"max_atoms={args.max_atoms}")
    print(f"max_part={args.max_part}")
    print(f"nonzero_regular_kernels={kernels}")
    print(f"rank_greater_than_one={higher_rank_kernels}")
    print(f"checked_instances={instances}")
    print(f"record_sha256={digest}")
    print("status=PASS")


if __name__ == "__main__":
    main()
