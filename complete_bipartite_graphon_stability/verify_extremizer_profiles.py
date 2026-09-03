#!/usr/bin/env python3
"""Exact finite-step profiles for asymptotic K_(s,t) extremizers.

Two mechanisms are checked with ``Fraction`` arithmetic:

* an orthogonal rank-one spectral tail, showing the fourth-Schatten stability
  exponent 1/4 is necessary;
* degree modes at epsilon^2 and epsilon^3, separating the critical energy
  scale from a negligible degree perturbation.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import platform
from fractions import Fraction
from typing import Sequence

from verify_nonregular_local_constant import degree_regular_decomposition
from verify_regular_local_constant import (
    Matrix,
    add_constant,
    c4_density,
    cut_norm,
    fraction_text,
    kst_density,
)


Polynomial = tuple[Fraction, ...]


def outer(vector: Sequence[Fraction]) -> Matrix:
    return tuple(tuple(x * y for y in vector) for x in vector)


def add_scaled(first: Matrix, second: Matrix, scale: Fraction) -> Matrix:
    return tuple(
        tuple(x + scale * y for x, y in zip(first_row, second_row))
        for first_row, second_row in zip(first, second)
    )


def scale(matrix: Matrix, factor: Fraction) -> Matrix:
    return tuple(tuple(factor * x for x in row) for row in matrix)


def poly_add(first: Polynomial, second: Polynomial, limit: int) -> Polynomial:
    degree = min(limit, max(len(first), len(second)) - 1)
    return tuple(
        (first[k] if k < len(first) else 0)
        + (second[k] if k < len(second) else 0)
        for k in range(degree + 1)
    )


def poly_mul(first: Polynomial, second: Polynomial, limit: int) -> Polynomial:
    result = [Fraction(0) for _ in range(min(limit, len(first) + len(second) - 2) + 1)]
    for i, x in enumerate(first):
        for j, y in enumerate(second):
            if i + j <= limit:
                result[i + j] += x * y
    return tuple(result)


def poly_pow(base: Polynomial, exponent: int, limit: int) -> Polynomial:
    result: Polynomial = (Fraction(1),)
    for _ in range(exponent):
        result = poly_mul(result, base, limit)
    return result


def scaled_density_coefficients(
    regular: Matrix,
    degree_seed: Sequence[Fraction],
    degree_power: int,
    p: Fraction,
    s: int,
    t: int,
    limit: int = 4,
) -> Polynomial:
    """Expand t(K_s,t,p+epsilon U+epsilon^degree_power D)."""
    n = len(regular)
    if degree_power < 2:
        raise ValueError("degree_power must be at least two")
    if len(degree_seed) != n or sum(degree_seed) != 0:
        raise ValueError("degree seed must have matching size and mean zero")
    if any(sum(row) != 0 for row in regular):
        raise ValueError("regular kernel must have zero row sums")

    entries: list[list[Polynomial]] = []
    for i in range(n):
        row: list[Polynomial] = []
        for j in range(n):
            coefficients = [Fraction(0) for _ in range(degree_power + 1)]
            coefficients[0] = p
            coefficients[1] = regular[i][j]
            coefficients[degree_power] = degree_seed[i] + degree_seed[j]
            row.append(tuple(coefficients))
        entries.append(row)

    total: Polynomial = (Fraction(0),)
    for left in itertools.product(range(n), repeat=s):
        common: Polynomial = (Fraction(0),)
        for y in range(n):
            product: Polynomial = (Fraction(1),)
            for x in left:
                product = poly_mul(product, entries[x][y], limit)
            common = poly_add(
                common, tuple(coefficient / n for coefficient in product), limit
            )
        total = poly_add(total, poly_pow(common, t, limit), limit)
    coefficients = tuple(coefficient / n**s for coefficient in total)
    return coefficients + (Fraction(0),) * (limit + 1 - len(coefficients))


def base_signs() -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    return (
        (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1)),
        (Fraction(1), Fraction(-1), Fraction(1), Fraction(-1)),
    )


def spectral_tail_profile(denominator: int) -> tuple[Fraction, ...]:
    if denominator < 2:
        raise ValueError("denominator must be at least two")
    rho = Fraction(1, denominator)
    first_sign, second_sign = base_signs()
    first = outer(first_sign)
    second = outer(second_sign)
    kernel = add_scaled(first, second, rho)
    if any(sum(row) != 0 for row in kernel):
        raise AssertionError("spectral-tail kernel is not regular")
    c4 = c4_density(kernel)
    cut = cut_norm(kernel)
    tail_cut = cut_norm(scale(second, rho))
    if c4 != 1 + rho**4:
        raise AssertionError("fourth-Schatten profile is incorrect")
    if cut != Fraction(1, 4):
        raise AssertionError("spectral-tail cut norm is incorrect")
    if tail_cut != rho / 4:
        raise AssertionError("rank-one tail cut norm is incorrect")
    relative_cut_fourth = (4 * cut) ** 4 / c4
    relative_tail_fourth = rho**4 / c4
    return rho, c4, cut, tail_cut, relative_cut_fourth, relative_tail_fourth


def degree_profile(
    denominator: int, degree_power: int, p: Fraction, s: int, t: int
) -> tuple[Fraction, ...]:
    if denominator < 2:
        raise ValueError("denominator must be at least two")
    epsilon = Fraction(1, denominator)
    regular_sign, degree_seed = base_signs()
    regular = outer(regular_sign)
    degree_kernel = tuple(
        tuple(degree_seed[i] + degree_seed[j] for j in range(4)) for i in range(4)
    )
    f_matrix = add_scaled(scale(regular, epsilon), degree_kernel, epsilon**degree_power)
    w_matrix = add_constant(f_matrix, p)
    if any(not 0 <= value <= 1 for row in w_matrix for value in row):
        raise AssertionError("profile is not a graphon")

    degree, decomposed_degree, decomposed_regular = degree_regular_decomposition(f_matrix)
    expected_degree = tuple(epsilon**degree_power * value for value in degree_seed)
    if degree != expected_degree:
        raise AssertionError("degree mode has the wrong scale")
    if decomposed_degree != scale(degree_kernel, epsilon**degree_power):
        raise AssertionError("degree-kernel decomposition mismatch")
    if decomposed_regular != scale(regular, epsilon):
        raise AssertionError("regular-core decomposition mismatch")

    coefficients = scaled_density_coefficients(
        regular, degree_seed, degree_power, p, s, t
    )
    if coefficients[0] != p ** (s * t) or any(coefficients[k] for k in range(1, 4)):
        raise AssertionError("coefficients below fourth order did not vanish")
    edge_count = s * t
    adjacent_pairs = s * math.comb(t, 2) + t * math.comb(s, 2)
    four_cycles = math.comb(s, 2) * math.comb(t, 2)
    expected_fourth = four_cycles * p ** (edge_count - 4)
    if degree_power == 2:
        expected_fourth += adjacent_pairs * p ** (edge_count - 2)
    if coefficients[4] != expected_fourth:
        raise AssertionError("fourth coefficient is incorrect")

    density = kst_density(w_matrix, s, t)
    delta = density - p**edge_count
    full_cut = cut_norm(f_matrix)
    degree_cut = cut_norm(decomposed_degree)
    if delta <= 0:
        raise AssertionError("profile deficit is not positive")
    return (
        epsilon,
        density,
        delta,
        full_cut,
        degree_cut,
        full_cut**4 / delta,
        coefficients[4],
    )


def run_checks() -> tuple[int, int, str]:
    digest = hashlib.sha256()
    tail_instances = 0
    degree_instances = 0
    for denominator in (4, 8, 16, 32, 64):
        values = spectral_tail_profile(denominator)
        digest.update(
            ("S:" + ":".join(
                (str(denominator), *(fraction_text(value) for value in values))
            ) + "\n").encode("ascii")
        )
        tail_instances += 1

    p = Fraction(2, 5)
    for denominator in (8, 16, 32, 64):
        for degree_power in (2, 3):
            for s, t in ((2, 2), (2, 3), (3, 3)):
                values = degree_profile(denominator, degree_power, p, s, t)
                digest.update(
                    ("D:" + ":".join(
                        (
                            str(denominator),
                            str(degree_power),
                            str(s),
                            str(t),
                            *(fraction_text(value) for value in values),
                        )
                    ) + "\n").encode("ascii")
                )
                degree_instances += 1
    return tail_instances, degree_instances, digest.hexdigest()


def main() -> None:
    tail_instances, degree_instances, digest = run_checks()
    print(f"python={platform.python_version()}")
    print("arithmetic=fractions.Fraction")
    print(f"spectral_tail_instances={tail_instances}")
    print(f"degree_scale_instances={degree_instances}")
    print(f"record_sha256={digest}")
    print("status=PASS")


if __name__ == "__main__":
    main()
