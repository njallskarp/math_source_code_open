#!/usr/bin/env python3
"""Exact audit of the least internal-symmetry obstruction for path blocks."""

from __future__ import annotations

import hashlib
import itertools
import json
from math import comb


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def poly_pow(base: list[int], exponent: int) -> list[int]:
    result = [1]
    for _ in range(exponent):
        result = poly_mul(result, base)
    return result


def rational_coefficients(numerator: list[int], denominator: list[int], count: int) -> list[int]:
    if denominator[0] != 1:
        raise ValueError("denominator must have constant coefficient one")
    result: list[int] = []
    for n in range(count):
        value = numerator[n] if n < len(numerator) else 0
        for j in range(1, min(n, len(denominator) - 1) + 1):
            value -= denominator[j] * result[n - j]
        result.append(value)
    return result


def fixed_count_sum(dilation: int) -> int:
    """Fixed lattice points in q P_3^(2) under one end-block swap."""
    return sum((dilation - r + 1) * (r // 2 + 1) * comb(r + 2, 2) for r in range(dilation + 1))


def fixed_count_direct(dilation: int) -> int:
    """Definition-level count in fixed coordinates (u,b1,b2,c1,c2)."""
    count = 0
    for u, b1, b2, c1, c2 in itertools.product(range(dilation + 1), repeat=5):
        if 2 * u + b1 + b2 <= dilation and b1 + b2 + c1 + c2 <= dilation:
            count += 1
    return count


def partitions(total: int, maximum: int | None = None) -> tuple[tuple[int, ...], ...]:
    if total == 0:
        return ((),)
    if maximum is None or maximum > total:
        maximum = total
    result = []
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, first):
            result.append((first, *tail))
    return tuple(result)


def determinant_from_cycles(cycles: tuple[int, ...]) -> list[int]:
    """Homogenized determinant: one slack fixed point plus coordinate cycles."""
    result = [1, -1]
    for length in cycles:
        factor = [0] * (length + 1)
        factor[0] = 1
        factor[length] = -1
        result = poly_mul(result, factor)
    return result


def verify_two_block_simplex(max_width: int = 7, coefficients: int = 17) -> int:
    """Check h*_g=1 for all internal cycle types when m=2."""
    checked = 0
    for width in range(2, max_width + 1):
        for left in partitions(width):
            for right in partitions(width):
                denominator = determinant_from_cycles(left + right)
                ehrhart = rational_coefficients([1], denominator, coefficients)
                hstar = [
                    sum(
                        denominator[j] * ehrhart[n - j]
                        for j in range(min(n, len(denominator) - 1) + 1)
                    )
                    for n in range(coefficients)
                ]
                if hstar != [1] + [0] * (coefficients - 1):
                    raise AssertionError((width, left, right, hstar))
                checked += 1
    return checked


def verify() -> dict[str, object]:
    # The closed fixed-point Ehrhart series is N/((1-t)^6(1+t)^3).
    numerator = [1, 2, 6, 2, 1]
    denominator = poly_mul(poly_pow([1, -1], 6), poly_pow([1, 1], 3))

    # Audit the generating-function derivation after clearing denominators:
    # 4F(t)=6t/(1-t)^4+3/(1-t)^3+1/(1+t)^3 and E=F/(1-t)^2.
    term1 = poly_mul([0, 6], poly_pow([1, 1], 3))
    term2 = poly_mul([3, -3], poly_pow([1, 1], 3))
    term3 = poly_pow([1, -1], 4)
    common_numerator = [0] * max(len(term1), len(term2), len(term3))
    for term in (term1, term2, term3):
        for i, value in enumerate(term):
            common_numerator[i] += value
    if common_numerator != [4 * value for value in numerator]:
        raise AssertionError((common_numerator, numerator))

    formula_dilations = 81
    rational_counts = rational_coefficients(numerator, denominator, formula_dilations)
    sum_counts = [fixed_count_sum(q) for q in range(formula_dilations)]
    if rational_counts != sum_counts:
        raise AssertionError("closed series differs from exact finite sum")

    direct_dilations = 8
    direct_counts = [fixed_count_direct(q) for q in range(direct_dilations)]
    if direct_counts != rational_counts[:direct_dilations]:
        raise AssertionError("definition-level enumeration differs")

    # The coordinate action has one 2-cycle and four fixed coordinates; the
    # homogenizing coordinate is fixed.  Thus det=(1-t^2)(1-t)^5.
    equivariant_determinant = poly_mul([1, 0, -1], poly_pow([1, -1], 5))
    hstar_from_counts = [
        sum(
            equivariant_determinant[j] * rational_counts[n - j]
            for j in range(min(n, len(equivariant_determinant) - 1) + 1)
        )
        for n in range(formula_dilations)
    ]

    # After cancellation, h*_g(t)=N(t)/(1+t)^2.
    hstar_closed = rational_coefficients(numerator, [1, 2, 1], formula_dilations)
    if hstar_from_counts != hstar_closed:
        raise AssertionError("equivariant h* calculation differs")
    numerator_at_minus_one = sum(value * (-1) ** i for i, value in enumerate(numerator))
    if numerator_at_minus_one != 4:
        raise AssertionError("the noncancellation witness changed")

    simplex_cycle_type_pairs = verify_two_block_simplex()
    report = {
        "direct_dilations": direct_dilations,
        "formula_dilations": formula_dilations,
        "fixed_counts_prefix": direct_counts,
        "hstar_prefix": hstar_closed[:12],
        "numerator": numerator,
        "numerator_at_minus_one": numerator_at_minus_one,
        "simplex_cycle_type_pairs": simplex_cycle_type_pairs,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    report = verify()
    print(
        "VERIFIED least internal-symmetry obstruction; "
        f"direct_dilations={report['direct_dilations']}; "
        f"formula_dilations={report['formula_dilations']}; "
        f"simplex_cycle_type_pairs={report['simplex_cycle_type_pairs']}; "
        f"numerator_at_minus_one={report['numerator_at_minus_one']}; "
        f"sha256={report['sha256']}"
    )
    print(f"fixed_counts_prefix={report['fixed_counts_prefix']}")
    print(f"hstar_prefix={report['hstar_prefix']}")


if __name__ == "__main__":
    main()
