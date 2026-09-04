"""Exact checks for the whole-jet factorial-block unit obstruction."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from functools import cache
from math import comb, prod

Element = tuple[Fraction, ...]
Series = list[Element]
Partition = tuple[int, ...]

PRIME = 7
DEGREE = PRIME - 1
ZERO: Element = (Fraction(0),) * DEGREE
ONE: Element = (Fraction(1),) + (Fraction(0),) * (DEGREE - 1)
ZETA: Element = (Fraction(0), Fraction(1)) + (Fraction(0),) * (DEGREE - 2)

LEFT: Partition = (14, 13, 7, 7, 7, 7, 7, 7, 7, 6, 2, 1)
RIGHT: Partition = (12, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 1, 1)


def add(left: Element, right: Element) -> Element:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def neg(value: Element) -> Element:
    return tuple(-entry for entry in value)


def scale(value: Element, scalar: int | Fraction) -> Element:
    return tuple(scalar * entry for entry in value)


def mul(left: Element, right: Element) -> Element:
    coefficients = [Fraction(0)] * (2 * DEGREE - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            coefficients[i + j] += a * b
    # Reduce by Phi_p(z)=1+z+...+z^(p-1), highest degree first.
    for degree in range(len(coefficients) - 1, DEGREE - 1, -1):
        leading = coefficients[degree]
        if leading:
            shift = degree - DEGREE
            for index in range(DEGREE + 1):
                coefficients[shift + index] -= leading
    return tuple(coefficients[:DEGREE])


def power(base: Element, exponent: int) -> Element:
    result = ONE
    while exponent:
        if exponent & 1:
            result = mul(result, base)
        base = mul(base, base)
        exponent //= 2
    return result


def inverse(value: Element) -> Element:
    """Invert by exact Gaussian elimination on multiplication by value."""
    columns: list[Element] = []
    for index in range(DEGREE):
        basis = tuple(Fraction(position == index) for position in range(DEGREE))
        columns.append(mul(value, basis))
    matrix = [
        [columns[column][row] for column in range(DEGREE)]
        + [Fraction(row == 0)]
        for row in range(DEGREE)
    ]
    for column in range(DEGREE):
        pivot = next(
            (row for row in range(column, DEGREE) if matrix[row][column]), None
        )
        if pivot is None:
            raise ZeroDivisionError(value)
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        divisor = matrix[column][column]
        matrix[column] = [entry / divisor for entry in matrix[column]]
        for row in range(DEGREE):
            if row == column:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry in zip(
                        matrix[row], matrix[column], strict=True
                    )
                ]
    result = tuple(matrix[row][-1] for row in range(DEGREE))
    if mul(value, result) != ONE:
        raise AssertionError("field inversion failed")
    return result


def series_inverse(denominator: Series, cutoff: int) -> Series:
    result = [ZERO] * cutoff
    inverse_constant = inverse(denominator[0])
    result[0] = inverse_constant
    for degree in range(1, cutoff):
        total = ZERO
        for index in range(1, min(degree, len(denominator) - 1) + 1):
            total = add(total, mul(denominator[index], result[degree - index]))
        result[degree] = neg(mul(inverse_constant, total))
    return result


def series_product(left: Series, right: Series, cutoff: int) -> Series:
    result = [ZERO] * cutoff
    for i, a in enumerate(left[:cutoff]):
        for j, b in enumerate(right[: cutoff - i]):
            result[i + j] = add(result[i + j], mul(a, b))
    return result


def factor_denominator(
    weight: int, root: Element, vanishes: bool, cutoff: int
) -> Series:
    root_power = power(root, weight)
    if vanishes:
        return [
            scale(root_power, (-1) ** degree * comb(weight, degree + 1))
            for degree in range(min(weight, cutoff))
        ]
    result = [add(ONE, neg(root_power))]
    result.extend(
        scale(root_power, (-1) ** (degree + 1) * comb(weight, degree))
        for degree in range(1, min(weight, cutoff - 1) + 1)
    )
    return result


@cache
def local_analytic_jet(
    partition: Partition, at_one: bool, cutoff: int
) -> tuple[Element, ...]:
    root = ONE if at_one else ZETA
    weights = (1, *partition)
    vanishing = [at_one or weight % PRIME == 0 for weight in weights]
    order = sum(vanishing)
    cutoff = min(cutoff, order)
    result = [ONE] + [ZERO] * (cutoff - 1)
    for weight, does_vanish in zip(weights, vanishing, strict=True):
        denominator = factor_denominator(weight, root, does_vanish, cutoff)
        result = series_product(
            result, series_inverse(denominator, cutoff), cutoff
        )
    return tuple(result)


@cache
def binomial_polynomial(top_shift: int) -> tuple[Fraction, ...]:
    result = [Fraction(1)]
    for shift in range(1, top_shift + 1):
        product_coefficients = [Fraction(0)] * (len(result) + 1)
        for degree, coefficient in enumerate(result):
            product_coefficients[degree] += shift * coefficient
            product_coefficients[degree + 1] += coefficient
        result = product_coefficients
    divisor = prod(range(1, top_shift + 1))
    return tuple(coefficient / divisor for coefficient in result)


def pole_wave_top(
    partition: Partition, at_one: bool, depth: int
) -> tuple[Element, ...]:
    order = len(partition) + 1 if at_one else sum(
        part % PRIME == 0 for part in partition
    )
    jet = local_analytic_jet(partition, at_one, min(order, depth + 1))
    bases = [binomial_polynomial(order - index - 1) for index in range(len(jet))]
    result: list[Element] = []
    for drop in range(depth + 1):
        degree = order - 1 - drop
        coefficient = ZERO
        if degree >= 0:
            for index, local_coefficient in enumerate(jet):
                if degree < len(bases[index]):
                    coefficient = add(
                        coefficient,
                        scale(local_coefficient, bases[index][degree]),
                    )
        result.append(coefficient)
    return tuple(result)


def product_top(
    left: tuple[Element, ...], right: tuple[Element, ...]
) -> tuple[Element, ...]:
    return tuple(
        sum_elements(mul(left[index], right[drop - index]) for index in range(drop + 1))
        for drop in range(len(left))
    )


def sum_elements(values: object) -> Element:
    result = ZERO
    for value in values:  # type: ignore[union-attr]
        result = add(result, value)
    return result


def maximal_prime_profile(partition: Partition) -> tuple[int, tuple[int, ...]]:
    primes: set[int] = set()
    for part in partition:
        value = part
        divisor = 2
        while divisor * divisor <= value:
            if value % divisor == 0:
                primes.add(divisor)
                while value % divisor == 0:
                    value //= divisor
            divisor += 1
        if value > 1:
            primes.add(value)
    counts = {prime: sum(part % prime == 0 for part in partition) for prime in primes}
    maximum = max(counts.values())
    return len(partition) - maximum, tuple(
        sorted(prime for prime, count in counts.items() if count == maximum)
    )


def falling(start: int, length: int) -> int:
    return prod(start - offset for offset in range(length))


def whole_jet_polynomial(divisible_count: int, defect: int, prime: int) -> tuple[int, ...]:
    return tuple(
        ((-1) ** index)
        * comb(defect + index, index)
        * falling(divisible_count - 1, index)
        % prime
        for index in range(defect)
    )


def cross_report(left: Partition, right: Partition, depth: int) -> dict[str, int]:
    left_root_order = sum(part % PRIME == 0 for part in left)
    right_root_order = sum(part % PRIME == 0 for part in right)
    first = product_top(
        pole_wave_top(left, False, depth), pole_wave_top(right, True, depth)
    )
    second = product_top(
        pole_wave_top(left, True, depth), pole_wave_top(right, False, depth)
    )
    cross = tuple(add(a, b) for a, b in zip(first, second, strict=True))
    cancelled = next((index for index, value in enumerate(cross) if value != ZERO), depth + 1)
    nominal_order = left_root_order + len(right)
    if nominal_order != len(left) + right_root_order:
        raise AssertionError("cross waves do not have equal nominal order")
    determinant_zero = left_root_order + right_root_order
    return {
        "nominal_order": nominal_order,
        "cancelled_orders": cancelled,
        "actual_order": nominal_order - cancelled,
        "determinant_zero": determinant_zero,
        "residual_order": nominal_order - cancelled - determinant_zero,
    }


def verify() -> dict[str, object]:
    if sum(LEFT) != 85 or sum(RIGHT) != 85:
        raise AssertionError((sum(LEFT), sum(RIGHT)))
    if maximal_prime_profile(LEFT) != (4, (7,)):
        raise AssertionError(maximal_prime_profile(LEFT))
    if maximal_prime_profile(RIGHT) != (4, (7,)):
        raise AssertionError(maximal_prime_profile(RIGHT))

    defect = 4
    left_count = 8
    right_count = 9
    left_block = prod(range(left_count, left_count + defect + 1))
    right_block = prod(range(right_count, right_count + defect + 1))
    if left_block % PRIME == 0 or right_block % PRIME == 0:
        raise AssertionError("the witness must lie in the unit stratum")
    if (left_block + right_block) % PRIME:
        raise AssertionError("the hard witness must pass the leading congruence")

    left_jet = whole_jet_polynomial(left_count, defect, PRIME)
    right_jet = whole_jet_polynomial(right_count, defect, PRIME)
    if left_jet == right_jet or left_jet[1] == right_jet[1]:
        raise AssertionError((left_jet, right_jet))

    exact = cross_report(LEFT, RIGHT, defect)
    if exact != {
        "nominal_order": 21,
        "cancelled_orders": 1,
        "actual_order": 20,
        "determinant_zero": 17,
        "residual_order": 3,
    }:
        raise AssertionError(exact)

    result: dict[str, object] = {
        "theorem": "factorial-block p-units obstruct full maximal cross-jet cancellation",
        "prime": PRIME,
        "width": 85,
        "defect": defect,
        "left_divisible": left_count,
        "right_divisible": right_count,
        "left_block_mod_p": left_block % PRIME,
        "right_block_mod_p": right_block % PRIME,
        "left_whole_jet_mod_p": left_jet,
        "right_whole_jet_mod_p": right_jet,
        **exact,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return result


def main() -> None:
    report = verify()
    print(
        "VERIFIED whole-jet unit obstruction; "
        f"p={report['prime']}; defect={report['defect']}; "
        f"leading_cancellations={report['cancelled_orders']}; "
        f"residual_order={report['residual_order']}; "
        f"sha256={report['sha256']}"
    )


if __name__ == "__main__":
    main()
