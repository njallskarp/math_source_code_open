#!/usr/bin/env python3
"""Exact finite-step audit of the unrestricted local K_(s,t) expansion.

The checker starts from arbitrary symmetric mean-zero step kernels, separates
their degree and regular components, and evaluates the claimed expansion and
cut-norm ingredients directly with ``Fraction`` arithmetic.  It also extracts
the fourth coefficient of the two-scale perturbation polynomial exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
import platform
from fractions import Fraction
from typing import Sequence

from verify_regular_local_constant import (
    Matrix,
    add_constant,
    adjacency_matrix,
    c4_density,
    cut_norm,
    fraction_text,
    kst_density,
    scale_to_radius,
)


Polynomial = tuple[Fraction, ...]


def mean_center(matrix: Sequence[Sequence[Fraction]]) -> Matrix:
    """Subtract the uniform grand mean, preserving symmetry."""
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be nonempty and square")
    if any(matrix[i][j] != matrix[j][i] for i in range(n) for j in range(n)):
        raise ValueError("matrix must be symmetric")
    grand_mean = sum(sum(row) for row in matrix) / n**2
    centered = tuple(
        tuple(matrix[i][j] - grand_mean for j in range(n)) for i in range(n)
    )
    if sum(sum(row) for row in centered) != 0:
        raise AssertionError("mean centering failed")
    return centered


def degree_regular_decomposition(matrix: Matrix) -> tuple[tuple[Fraction, ...], Matrix, Matrix]:
    """Return a, D=a tensor 1+1 tensor a, and U=F-D."""
    n = len(matrix)
    if sum(sum(row) for row in matrix) != 0:
        raise ValueError("kernel must have mean zero")
    degree = tuple(sum(row) / n for row in matrix)
    degree_kernel = tuple(
        tuple(degree[i] + degree[j] for j in range(n)) for i in range(n)
    )
    regular = tuple(
        tuple(matrix[i][j] - degree_kernel[i][j] for j in range(n))
        for i in range(n)
    )
    if sum(degree) != 0 or any(sum(row) != 0 for row in regular):
        raise AssertionError("degree--regular decomposition failed")
    return degree, degree_kernel, regular


def add_matrices(first: Matrix, second: Matrix) -> Matrix:
    return tuple(
        tuple(x + y for x, y in zip(first_row, second_row))
        for first_row, second_row in zip(first, second)
    )


def expansion_constants(edge_count: int, x: Fraction) -> tuple[Fraction, Fraction]:
    """Return the explicit degree and C4 relative-error coefficients."""
    if not 0 <= x <= 1:
        raise ValueError("x must lie in [0,1]")
    one_degree_count = edge_count * 2 ** (edge_count - 1)
    degree_error = Fraction(6**edge_count) * x + one_degree_count * x**2
    c4_error = (2**edge_count + one_degree_count) * x**2
    return degree_error, c4_error


def check_instance(
    f_matrix: Matrix, p: Fraction, r: Fraction, s: int, t: int
) -> tuple[Fraction, ...]:
    """Check the uniform expansion and its three cut-norm ingredients."""
    n = len(f_matrix)
    eta = max(abs(value) for row in f_matrix for value in row)
    if eta > r * p:
        raise AssertionError("kernel exceeds the declared local radius")
    if sum(sum(row) for row in f_matrix) != 0:
        raise AssertionError("kernel does not have edge density zero")
    w_matrix = add_constant(f_matrix, p)
    if any(not 0 <= value <= 1 for row in w_matrix for value in row):
        raise AssertionError("p+F is not a graphon")

    degree, degree_kernel, regular = degree_regular_decomposition(f_matrix)
    if add_matrices(degree_kernel, regular) != f_matrix:
        raise AssertionError("components do not reconstruct F")
    variance = sum(value**2 for value in degree) / n
    c4 = c4_density(regular)
    h = max(
        max(abs(value) for value in degree),
        max(abs(value) for row in regular for value in row),
    )
    if h > 3 * eta:
        raise AssertionError("component sup-norm bound failed")
    x = h / p
    if x > 1:
        raise AssertionError("component radius exceeds proof range")

    edge_count = s * t
    adjacent_pairs = s * math.comb(t, 2) + t * math.comb(s, 2)
    four_cycles = math.comb(s, 2) * math.comb(t, 2)
    degree_scale = p ** (edge_count - 2) * variance
    c4_scale = p ** (edge_count - 4) * c4
    leading = adjacent_pairs * degree_scale + four_cycles * c4_scale
    degree_error, c4_error = expansion_constants(edge_count, x)
    error_bound = degree_error * degree_scale + c4_error * c4_scale

    density = kst_density(w_matrix, s, t)
    delta = density - p**edge_count
    if abs(delta - leading) > error_bound:
        raise AssertionError(
            f"expansion failed for n={n}, s={s}, t={t}: "
            f"error={abs(delta-leading)}, bound={error_bound}"
        )
    if delta < 0:
        raise AssertionError("Sidorenko deficit is negative")
    if delta > 2**edge_count * p**edge_count * r**2:
        raise AssertionError("elementary deficit upper bound failed")

    regular_cut = cut_norm(regular)
    degree_cut = cut_norm(degree_kernel)
    full_cut = cut_norm(f_matrix)
    if 256 * regular_cut**4 > c4:
        raise AssertionError("centered cut--Schatten inequality failed")
    if degree_cut**2 > variance:
        raise AssertionError("degree-kernel cut bound failed")
    if full_cut > regular_cut + degree_cut:
        raise AssertionError("cut-norm triangle inequality failed")
    return (
        density,
        delta,
        variance,
        c4,
        h,
        leading,
        error_bound,
        full_cut,
        regular_cut,
        degree_cut,
    )


def poly_add(first: Polynomial, second: Polynomial, limit: int = 4) -> Polynomial:
    return tuple(
        (first[k] if k < len(first) else 0)
        + (second[k] if k < len(second) else 0)
        for k in range(min(limit, max(len(first), len(second)) - 1) + 1)
    )


def poly_mul(first: Polynomial, second: Polynomial, limit: int = 4) -> Polynomial:
    result = [Fraction(0) for _ in range(min(limit, len(first) + len(second) - 2) + 1)]
    for i, x in enumerate(first):
        for j, y in enumerate(second):
            if i + j <= limit:
                result[i + j] += x * y
    return tuple(result)


def poly_pow(base: Polynomial, exponent: int, limit: int = 4) -> Polynomial:
    result: Polynomial = (Fraction(1),)
    for _ in range(exponent):
        result = poly_mul(result, base, limit)
    return result


def two_scale_coefficients(
    regular: Matrix,
    degree_seed: Sequence[Fraction],
    p: Fraction,
    s: int,
    t: int,
) -> Polynomial:
    """Return coefficients through epsilon^4 for p+epsilon U+epsilon^2 D."""
    n = len(regular)
    if len(degree_seed) != n or sum(degree_seed) != 0:
        raise ValueError("degree seed must have matching size and mean zero")
    if any(sum(row) != 0 for row in regular):
        raise ValueError("U must be regular")
    entries = tuple(
        tuple((p, regular[i][j], degree_seed[i] + degree_seed[j]) for j in range(n))
        for i in range(n)
    )
    total: Polynomial = (Fraction(0),)
    for left in itertools.product(range(n), repeat=s):
        common: Polynomial = (Fraction(0),)
        for y in range(n):
            product: Polynomial = (Fraction(1),)
            for x_index in left:
                product = poly_mul(product, entries[x_index][y])
            common = poly_add(common, tuple(value / n for value in product))
        total = poly_add(total, poly_pow(common, t))
    return tuple(value / n**s for value in total)


def check_two_scale(
    regular: Matrix,
    degree_seed: Sequence[Fraction],
    p: Fraction,
    s: int,
    t: int,
) -> Polynomial:
    coefficients = two_scale_coefficients(regular, degree_seed, p, s, t)
    coefficients = coefficients + (Fraction(0),) * (5 - len(coefficients))
    if coefficients[0] != p ** (s * t) or any(coefficients[k] != 0 for k in range(1, 4)):
        raise AssertionError("two-scale coefficients below order four did not vanish")
    variance = sum(value**2 for value in degree_seed) / len(degree_seed)
    adjacent_pairs = s * math.comb(t, 2) + t * math.comb(s, 2)
    four_cycles = math.comb(s, 2) * math.comb(t, 2)
    expected = (
        adjacent_pairs * p ** (s * t - 2) * variance
        + four_cycles * p ** (s * t - 4) * c4_density(regular)
    )
    if coefficients[4] != expected:
        raise AssertionError(
            f"two-scale fourth coefficient mismatch: {coefficients[4]} != {expected}"
        )
    return coefficients


def run_checks(max_atoms: int, max_part: int) -> tuple[int, int, int, int, str]:
    if max_atoms < 2:
        raise ValueError("max_atoms must be at least two")
    if max_part < 2:
        raise ValueError("max_part must be at least two")
    p = Fraction(2, 5)
    radii = (Fraction(1, 50), Fraction(1, 100))
    kernels = 0
    irregular_kernels = 0
    instances = 0
    two_scale_instances = 0
    digest = hashlib.sha256()
    for n in range(2, max_atoms + 1):
        graph_edges = n * (n - 1) // 2
        for edge_mask in range(1 << graph_edges):
            centered = mean_center(adjacency_matrix(n, edge_mask))
            if all(value == 0 for row in centered for value in row):
                continue
            kernels += 1
            degree, _, regular = degree_regular_decomposition(centered)
            if any(degree):
                irregular_kernels += 1
            if any(value for row in regular for value in row) and any(degree):
                seed_scale = max(abs(value) for value in degree)
                seed = tuple(value / seed_scale for value in degree)
                for s in range(2, max_part + 1):
                    for t in range(2, max_part + 1):
                        coefficients = check_two_scale(regular, seed, p, s, t)
                        digest.update(
                            ("T:" + ":".join(
                                (str(n), str(edge_mask), str(s), str(t),
                                 *(fraction_text(value) for value in coefficients))
                            ) + "\n").encode("ascii")
                        )
                        two_scale_instances += 1
            for r in radii:
                f_matrix = scale_to_radius(centered, r * p)
                for s in range(2, max_part + 1):
                    for t in range(2, max_part + 1):
                        values = check_instance(f_matrix, p, r, s, t)
                        digest.update(
                            ("G:" + ":".join(
                                (str(n), str(edge_mask), fraction_text(r), str(s), str(t),
                                 *(fraction_text(value) for value in values))
                            ) + "\n").encode("ascii")
                        )
                        instances += 1
    return kernels, irregular_kernels, instances, two_scale_instances, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-atoms", type=int, default=4)
    parser.add_argument("--max-part", type=int, default=4)
    args = parser.parse_args()
    kernels, irregular, instances, two_scale, digest = run_checks(
        args.max_atoms, args.max_part
    )
    print(f"python={platform.python_version()}")
    print("p=2/5")
    print("radii=1/50,1/100")
    print(f"max_atoms={args.max_atoms}")
    print(f"max_part={args.max_part}")
    print(f"nonzero_mean_centered_kernels={kernels}")
    print(f"degree_irregular_kernels={irregular}")
    print(f"checked_general_instances={instances}")
    print(f"checked_two_scale_coefficients={two_scale}")
    print(f"record_sha256={digest}")
    print("status=PASS")


if __name__ == "__main__":
    main()
