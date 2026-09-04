"""Verify an exact three-order cancellation at a unique maximal cube root."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from functools import cache

from explore_cube_jet import (
    ZERO,
    add,
    cross_cancelled_orders,
    cross_jet_report,
    inv,
    mul,
    neg,
    pole_wave,
    polynomial_product,
)

LEFT_NONDIVISIBLE = (7, 4, 4, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1)
RIGHT_NONDIVISIBLE = (11, 7, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1)


def family(parameter: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if parameter < 0:
        raise ValueError("the parameter must be nonnegative")
    left_divisible = (
        9,
        6,
        *(3 * (2 * parameter + 1) for _ in range(3)),
        3,
        3,
        3,
    )
    right_divisible = (
        3 * (parameter + 2),
        3 * (2 * parameter + 1),
        3 * (3 * parameter + 1),
        3,
        3,
        3,
    )
    left = tuple(sorted((*LEFT_NONDIVISIBLE, *left_divisible), reverse=True))
    right = tuple(sorted((*RIGHT_NONDIVISIBLE, *right_divisible), reverse=True))
    return left, right


LEFT, RIGHT = family(0)


@cache
def prime_divisors(value: int) -> tuple[int, ...]:
    result: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            result.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        result.append(value)
    return tuple(result)


def maximal_prime_profile(partition: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    primes = sorted({prime for part in partition for prime in prime_divisors(part)})
    counts = {prime: sum(part % prime == 0 for part in partition) for prime in primes}
    maximum = max(counts.values())
    return (
        len(partition) - maximum,
        tuple(prime for prime in primes if counts[prime] == maximum),
    )


def normalized_cross_differences_exact(
    left: tuple[int, ...], right: tuple[int, ...], depth: int
) -> tuple[tuple[Fraction, Fraction], ...]:
    """Compare the two cross waves after making their leading terms opposite."""
    first = polynomial_product(pole_wave(left, False), pole_wave(right, True))
    second = polynomial_product(pole_wave(left, True), pole_wave(right, False))
    degree = len(first) - 1
    leading = first[degree]
    if add(leading, second[degree]) != ZERO:
        raise AssertionError("the leading terms do not cancel")
    result: list[tuple[Fraction, Fraction]] = []
    for drop in range(1, depth + 1):
        first_ratio = mul(first[degree - drop], inv(leading))
        second_ratio = mul(second[degree - drop], inv(neg(leading)))
        difference = add(first_ratio, neg(second_ratio))
        result.append(difference)
    return tuple(result)


def normalized_cross_differences(
    left: tuple[int, ...], right: tuple[int, ...], depth: int
) -> tuple[tuple[str, str], ...]:
    return tuple(
        tuple(str(entry) for entry in difference)
        for difference in normalized_cross_differences_exact(left, right, depth)
    )


def first_surviving_difference(parameter: int) -> tuple[Fraction, Fraction]:
    scalar = Fraction(40895 - 2520 * parameter * (parameter + 1), 12)
    return scalar, 2 * scalar


def verify() -> dict[str, object]:
    expected = {
        "nominal_order": 28,
        "actual_order": 25,
        "cancelled_orders": 3,
        "determinant_zero": 14,
        "residual_order": 11,
    }
    checked_parameters = tuple(range(13))
    for parameter in checked_parameters:
        left, right = family(parameter)
        expected_width = 63 + 18 * parameter
        if sum(left) != expected_width or sum(right) != expected_width:
            raise AssertionError((parameter, sum(left), sum(right)))
        left_profile = maximal_prime_profile(left)
        right_profile = maximal_prime_profile(right)
        if left_profile != (14, (3,)) or right_profile != (14, (3,)):
            raise AssertionError((parameter, left_profile, right_profile))
        report = cross_jet_report(left, right)
        if report != expected or cross_cancelled_orders(left, right, 4) != 3:
            raise AssertionError((parameter, report))
        differences = normalized_cross_differences_exact(left, right, 3)
        if differences[:2] != ((Fraction(0), Fraction(0)),) * 2:
            raise AssertionError((parameter, differences))
        if differences[2] != first_surviving_difference(parameter):
            raise AssertionError((parameter, differences))

    report = cross_jet_report(LEFT, RIGHT)
    differences = normalized_cross_differences(LEFT, RIGHT, 4)

    result: dict[str, object] = {
        "width": 63,
        "left_cycles": len(LEFT),
        "right_cycles": len(RIGHT),
        "maximizing_prime": 3,
        "common_defect": 14,
        "parameter_formula": "width=63+18t, t>=0",
        "checked_parameters": checked_parameters,
        **report,
        "normalized_differences": differences,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return result


def main() -> None:
    report = verify()
    print(
        "VERIFIED maximal cube-root jet cancellation; "
        f"width={report['width']}; common_defect={report['common_defect']}; "
        f"cancelled_orders={report['cancelled_orders']}; "
        f"residual_order={report['residual_order']}; sha256={report['sha256']}"
    )


if __name__ == "__main__":
    main()
