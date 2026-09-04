#!/usr/bin/env python3
"""Independent exact audit of the P_3^(2) internal-swap obstruction.

The target checker sums over a residual-capacity variable.  This checker uses
block-sum states, reconstructs the determinant from an explicit permutation
matrix, and resolves the resulting C2 character into trivial/sign
multiplicities.  It also checks the m=2 simplex boundary by enumerating
monomials for every internal permutation through width three.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterator, Sequence


def poly_add(left: Sequence[int], right: Sequence[int]) -> list[int]:
    size = max(len(left), len(right))
    result = [0] * size
    for index in range(size):
        result[index] = (left[index] if index < len(left) else 0) + (
            right[index] if index < len(right) else 0
        )
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_scale(poly: Sequence[int], scalar: int) -> list[int]:
    return [scalar * coefficient for coefficient in poly]


def poly_mul(left: Sequence[int], right: Sequence[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def poly_pow(base: Sequence[int], exponent: int) -> list[int]:
    result = [1]
    for _ in range(exponent):
        result = poly_mul(result, base)
    return result


def permutation_sign(permutation: Sequence[int]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant_i_minus_t_permutation(mapping: Sequence[int]) -> list[int]:
    """Compute det(I-tP) by the Leibniz formula, without cycle-type input."""
    size = len(mapping)
    matrix: list[list[list[int]]] = []
    for row in range(size):
        matrix_row = []
        for column in range(size):
            entry = [1] if row == column else [0]
            if row == mapping[column]:
                entry = poly_add(entry, [0, -1])
            matrix_row.append(entry)
        matrix.append(matrix_row)

    determinant = [0]
    for columns in itertools.permutations(range(size)):
        term = [1]
        for row, column in enumerate(columns):
            entry = matrix[row][column]
            if entry == [0]:
                term = [0]
                break
            term = poly_mul(term, entry)
        if term != [0]:
            determinant = poly_add(
                determinant, poly_scale(term, permutation_sign(columns))
            )
    return determinant


def multiply_series(coefficients: Sequence[int], polynomial: Sequence[int]) -> list[int]:
    return [
        sum(
            polynomial[j] * coefficients[degree - j]
            for j in range(min(degree, len(polynomial) - 1) + 1)
        )
        for degree in range(len(coefficients))
    ]


def block_sum_count(dilation: int, swap_first_block: bool) -> int:
    """Count from exact block sums (R1,R2,R3), independently of the target sum."""
    total = 0
    for middle_sum in range(dilation + 1):
        cap = dilation - middle_sum
        middle_multiplicity = middle_sum + 1
        for left_sum in range(cap + 1):
            if swap_first_block:
                left_multiplicity = int(left_sum % 2 == 0)
            else:
                left_multiplicity = left_sum + 1
            for right_sum in range(cap + 1):
                right_multiplicity = right_sum + 1
                total += (
                    left_multiplicity
                    * middle_multiplicity
                    * right_multiplicity
                )
    return total


def full_tuple_count(dilation: int, swap_first_block: bool) -> int:
    """Definition-level six-coordinate enumeration for small dilations."""
    total = 0
    for point in itertools.product(range(dilation + 1), repeat=6):
        x1, x2, b1, b2, c1, c2 = point
        if swap_first_block and x1 != x2:
            continue
        if x1 + x2 + b1 + b2 > dilation:
            continue
        if b1 + b2 + c1 + c2 > dilation:
            continue
        total += 1
    return total


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def fixed_monomial_count(
    total_degree: int, variable_count: int, mapping: Sequence[int]
) -> int:
    count = 0
    for exponents in weak_compositions(total_degree, variable_count):
        if all(exponents[index] == exponents[mapping[index]] for index in range(variable_count)):
            count += 1
    return count


def two_block_internal_mapping(
    width: int, left: Sequence[int], right: Sequence[int]
) -> tuple[int, ...]:
    mapping = list(range(2 * width + 1))
    for index, image in enumerate(left):
        mapping[index] = image
    for index, image in enumerate(right):
        mapping[width + index] = width + image
    return tuple(mapping)  # The final slack variable is fixed.


def verify_simplex_boundary(max_width: int = 3, dilations: int = 9) -> int:
    """Definition-level m=2 check over every internal permutation."""
    checked = 0
    for width in range(1, max_width + 1):
        for left in itertools.permutations(range(width)):
            for right in itertools.permutations(range(width)):
                mapping = two_block_internal_mapping(width, left, right)
                determinant = determinant_i_minus_t_permutation(mapping)
                fixed_counts = [
                    fixed_monomial_count(q, 2 * width + 1, mapping)
                    for q in range(dilations)
                ]
                hstar = multiply_series(fixed_counts, determinant)
                if hstar != [1] + [0] * (dilations - 1):
                    raise AssertionError((width, left, right, hstar))
                checked += 1
    return checked


def verify() -> dict[str, object]:
    series_dilations = 24
    direct_dilations = 5

    identity_counts = [
        block_sum_count(q, swap_first_block=False) for q in range(series_dilations)
    ]
    fixed_counts = [
        block_sum_count(q, swap_first_block=True) for q in range(series_dilations)
    ]
    for q in range(direct_dilations):
        if identity_counts[q] != full_tuple_count(q, swap_first_block=False):
            raise AssertionError(("identity full-tuple mismatch", q))
        if fixed_counts[q] != full_tuple_count(q, swap_first_block=True):
            raise AssertionError(("fixed full-tuple mismatch", q))

    identity_determinant = determinant_i_minus_t_permutation(tuple(range(7)))
    swap_mapping = (1, 0, 2, 3, 4, 5, 6)
    swap_determinant = determinant_i_minus_t_permutation(swap_mapping)
    if identity_determinant != poly_pow([1, -1], 7):
        raise AssertionError(identity_determinant)
    if swap_determinant != poly_mul([1, 0, -1], poly_pow([1, -1], 5)):
        raise AssertionError(swap_determinant)

    ordinary_hstar = multiply_series(identity_counts, identity_determinant)
    if ordinary_hstar != [1, 4, 1] + [0] * (series_dilations - 3):
        raise AssertionError(ordinary_hstar)

    fixed_ehrhart_denominator = poly_mul(
        poly_pow([1, -1], 6), poly_pow([1, 1], 3)
    )
    fixed_ehrhart_numerator = multiply_series(
        fixed_counts, fixed_ehrhart_denominator
    )
    if fixed_ehrhart_numerator != [1, 2, 6, 2, 1] + [0] * (
        series_dilations - 5
    ):
        raise AssertionError(fixed_ehrhart_numerator)

    swap_hstar = multiply_series(fixed_counts, swap_determinant)
    expected_swap = [1, 0, 5] + [
        4 * (-1) ** degree * (degree - 1)
        for degree in range(3, series_dilations)
    ]
    if swap_hstar != expected_swap:
        raise AssertionError(swap_hstar)

    trivial_multiplicities = []
    sign_multiplicities = []
    for identity_value, swap_value in zip(ordinary_hstar, swap_hstar, strict=True):
        if (identity_value + swap_value) % 2:
            raise AssertionError("nonintegral C2 character multiplicity")
        trivial_multiplicities.append((identity_value + swap_value) // 2)
        sign_multiplicities.append((identity_value - swap_value) // 2)

    expected_trivial = [1, 2, 3] + [
        2 * (-1) ** degree * (degree - 1)
        for degree in range(3, series_dilations)
    ]
    expected_sign = [0, 2, -2] + [
        2 * (-1) ** (degree + 1) * (degree - 1)
        for degree in range(3, series_dilations)
    ]
    if trivial_multiplicities != expected_trivial:
        raise AssertionError(trivial_multiplicities)
    if sign_multiplicities != expected_sign:
        raise AssertionError(sign_multiplicities)

    simplex_permutations = verify_simplex_boundary()
    report: dict[str, object] = {
        "c2_sign_prefix": sign_multiplicities[:12],
        "c2_tail_checks": series_dilations - 3,
        "c2_trivial_prefix": trivial_multiplicities[:12],
        "direct_dilations": direct_dilations,
        "fixed_counts_prefix": fixed_counts[:8],
        "fixed_ehrhart_numerator": fixed_ehrhart_numerator[:5],
        "identity_counts_prefix": identity_counts[:8],
        "ordinary_hstar": ordinary_hstar[:3],
        "series_dilations": series_dilations,
        "simplex_dilations": 9,
        "simplex_permutations": simplex_permutations,
        "swap_hstar_prefix": swap_hstar[:12],
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    report = verify()
    print(
        "INDEPENDENT AUDIT PASSED; "
        f"direct_dilations={report['direct_dilations']}; "
        f"series_dilations={report['series_dilations']}; "
        f"c2_tail_checks={report['c2_tail_checks']}; "
        f"simplex_permutations={report['simplex_permutations']}; "
        f"simplex_dilations={report['simplex_dilations']}; "
        f"sha256={report['sha256']}"
    )
    print(f"ordinary_hstar={report['ordinary_hstar']}")
    print(f"fixed_ehrhart_numerator={report['fixed_ehrhart_numerator']}")
    print(f"identity_counts_prefix={report['identity_counts_prefix']}")
    print(f"fixed_counts_prefix={report['fixed_counts_prefix']}")
    print(f"swap_hstar_prefix={report['swap_hstar_prefix']}")
    print(f"c2_trivial_prefix={report['c2_trivial_prefix']}")
    print(f"c2_sign_prefix={report['c2_sign_prefix']}")


if __name__ == "__main__":
    main()
