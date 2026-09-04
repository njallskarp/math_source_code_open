"""Exact checks for the saturated cyclotomic whole-jet invariant."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from functools import cache
from math import comb, factorial, prod

Partition = tuple[int, ...]
Element = tuple[Fraction, ...]
Series = list[Element]

PRIME = 5
DEGREE = PRIME - 1
ZERO: Element = (Fraction(0),) * DEGREE
ONE: Element = (Fraction(1),) + (Fraction(0),) * (DEGREE - 1)
ZETA: Element = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))

LEFT: Partition = (12, 7, 5, 5, 5, 1)
RIGHT: Partition = (10, 5, 5, 5, 4, 3, 3)


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
    # Reduce by Phi_5(z)=1+z+z^2+z^3+z^4.
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
    columns: list[Element] = []
    for index in range(DEGREE):
        basis = tuple(Fraction(position == index) for position in range(DEGREE))
        columns.append(mul(value, basis))
    matrix = [
        [columns[column][row] for column in range(DEGREE)] + [Fraction(row == 0)]
        for row in range(DEGREE)
    ]
    for column in range(DEGREE):
        pivot = next((row for row in range(column, DEGREE) if matrix[row][column]), None)
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
                    for entry, pivot_entry in zip(matrix[row], matrix[column], strict=True)
                ]
    result = tuple(matrix[row][-1] for row in range(DEGREE))
    if mul(value, result) != ONE:
        raise AssertionError("field inversion failed")
    return result


def series_inverse(denominator: Series, cutoff: int) -> Series:
    result = [ZERO] * cutoff
    result[0] = inverse(denominator[0])
    for degree in range(1, cutoff):
        total = ZERO
        for index in range(1, min(degree, len(denominator) - 1) + 1):
            total = add(total, mul(denominator[index], result[degree - index]))
        result[degree] = neg(mul(result[0], total))
    return result


def series_product(left: Series, right: Series, cutoff: int) -> Series:
    result = [ZERO] * cutoff
    for i, a in enumerate(left[:cutoff]):
        for j, b in enumerate(right[: cutoff - i]):
            result[i + j] = add(result[i + j], mul(a, b))
    return result


def factor_denominator(weight: int, root: Element, vanishes: bool, cutoff: int) -> Series:
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
def local_analytic_jet(partition: Partition, at_one: bool, cutoff: int) -> tuple[Element, ...]:
    root = ONE if at_one else ZETA
    weights = (1, *partition)
    vanishing = [at_one or weight % PRIME == 0 for weight in weights]
    order = sum(vanishing)
    cutoff = min(cutoff, order)
    result = [ONE] + [ZERO] * (cutoff - 1)
    for weight, does_vanish in zip(weights, vanishing, strict=True):
        denominator = factor_denominator(weight, root, does_vanish, cutoff)
        result = series_product(result, series_inverse(denominator, cutoff), cutoff)
    return tuple(result)


@cache
def binomial_polynomial(top_shift: int) -> tuple[Fraction, ...]:
    result = [Fraction(1)]
    for shift in range(1, top_shift + 1):
        coefficients = [Fraction(0)] * (len(result) + 1)
        for degree, coefficient in enumerate(result):
            coefficients[degree] += shift * coefficient
            coefficients[degree + 1] += coefficient
        result = coefficients
    divisor = factorial(top_shift)
    return tuple(coefficient / divisor for coefficient in result)


def pole_wave_top(partition: Partition, at_one: bool, depth: int) -> tuple[Element, ...]:
    order = len(partition) + 1 if at_one else sum(part % PRIME == 0 for part in partition)
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


def sum_elements(values: object) -> Element:
    result = ZERO
    for value in values:  # type: ignore[union-attr]
        result = add(result, value)
    return result


def product_top(left: tuple[Element, ...], right: tuple[Element, ...]) -> tuple[Element, ...]:
    return tuple(
        sum_elements(mul(left[index], right[drop - index]) for index in range(drop + 1))
        for drop in range(len(left))
    )


def cross_report(left: Partition, right: Partition, depth: int) -> dict[str, int]:
    left_root_order = sum(part % PRIME == 0 for part in left)
    right_root_order = sum(part % PRIME == 0 for part in right)
    first = product_top(pole_wave_top(left, False, depth), pole_wave_top(right, True, depth))
    second = product_top(pole_wave_top(left, True, depth), pole_wave_top(right, False, depth))
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


def falling(start: int, length: int) -> int:
    return prod(start - offset for offset in range(length))


def polynomial_product(left: list[int], right: list[int], cutoff: int, prime: int) -> list[int]:
    result = [0] * cutoff
    for i, a in enumerate(left[:cutoff]):
        for j, b in enumerate(right[: cutoff - i]):
            result[i + j] = (result[i + j] + a * b) % prime
    return result


def polynomial_inverse(polynomial: list[int], cutoff: int, prime: int) -> list[int]:
    result = [0] * cutoff
    result[0] = pow(polynomial[0], -1, prime)
    for degree in range(1, cutoff):
        result[degree] = (
            -result[0]
            * sum(
                polynomial[index] * result[degree - index]
                for index in range(1, min(degree, len(polynomial) - 1) + 1)
            )
        ) % prime
    return result


def polynomial_power(polynomial: list[int], exponent: int, cutoff: int, prime: int) -> list[int]:
    if exponent < 0:
        return polynomial_power(
            polynomial_inverse(polynomial, cutoff, prime),
            -exponent,
            cutoff,
            prime,
        )
    result = [1] + [0] * (cutoff - 1)
    base = polynomial
    while exponent:
        if exponent & 1:
            result = polynomial_product(result, base, cutoff, prime)
        base = polynomial_product(base, base, cutoff, prime)
        exponent //= 2
    return result


def diagonal_transform(series: list[int], pole_order: int, prime: int) -> list[int]:
    return [
        coefficient * falling(pole_order - 1, degree) % prime
        for degree, coefficient in enumerate(series)
    ]


def saturated_residue_jet(q: int, defect: int, prime: int) -> tuple[int, ...]:
    """Return the universal residue of H_tau(pi X) modulo (pi, X^defect)."""
    if q < 1 or defect < 1 or prime < 3:
        raise ValueError("q, defect positive and an odd prime are required")
    base = [0] * defect
    base[0] = 1
    if prime - 1 < defect:
        base[prime - 1] = -1 % prime
    common = polynomial_power(base, -q, defect, prime)
    one_plus = [0] * defect
    one_plus[0] = 1
    if defect > 1:
        one_plus[1] = 1
    root_local = polynomial_product(
        common,
        polynomial_power(one_plus, -(defect + 1), defect, prime),
        defect,
        prime,
    )
    root_wave = diagonal_transform(root_local, q, prime)
    one_wave = diagonal_transform(common, q + defect + 1, prime)
    return tuple(
        polynomial_product(
            root_wave,
            polynomial_inverse(one_wave, defect, prime),
            defect,
            prime,
        )
    )


def saturated_residue_closed(q: int, defect: int, prime: int) -> tuple[int, ...]:
    numerator = [0] * defect
    denominator = [0] * defect
    numerator[0] = denominator[0] = 1
    for degree in range(1, min(defect, prime - 1)):
        numerator[degree] = (
            (-1) ** degree * comb(defect + degree, degree) * falling(q - 1, degree)
        ) % prime
    if prime - 1 < defect and q % prime == 0 and defect % prime == 0:
        numerator[prime - 1] = -1 % prime
    if prime - 1 < defect and (q + defect + 1) % prime == 0:
        denominator[prime - 1] = -q % prime
    return tuple(
        polynomial_product(
            numerator,
            polynomial_inverse(denominator, defect, prime),
            defect,
            prime,
        )
    )


def p_valuation(value: int, prime: int) -> int:
    valuation = 0
    while value and value % prime == 0:
        valuation += 1
        value //= prime
    return valuation


def scaled_rational_residue(value: Fraction, degree: int, prime: int) -> int:
    """Reduce value*pi^degree when it is integral at pi=1-zeta_p."""
    valuation = p_valuation(value.numerator, prime) - p_valuation(value.denominator, prime)
    local_valuation = degree + (prime - 1) * valuation
    if local_valuation < 0:
        raise ValueError("nonintegral scaled coefficient")
    if local_valuation > 0:
        return 0
    numerator = value.numerator // prime ** p_valuation(value.numerator, prime)
    denominator = value.denominator // prime ** p_valuation(value.denominator, prime)
    # pi^(p-1)/p = -1 modulo pi.
    return (numerator * pow(denominator, -1, prime) * (-1) ** (-valuation)) % prime


def normalized_vanishing_factor_residues(weight: int, prime: int) -> tuple[int, ...]:
    if weight % prime:
        raise ValueError("weight must be divisible by prime")
    return tuple(
        scaled_rational_residue(
            Fraction((-1) ** degree * comb(weight, degree + 1), weight),
            degree,
            prime,
        )
        for degree in range(weight)
    )


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


def denominator_remainder(parts: Partition, prime: int) -> tuple[int, ...]:
    """Reduce product(1-z^a) modulo Phi_p(z), for prime p."""
    polynomial = [1]
    for part in parts:
        factor = [0] * (part + 1)
        factor[0] = 1
        factor[part] = -1
        product_polynomial = [0] * (len(polynomial) + part)
        for i, left in enumerate(polynomial):
            for j, right in enumerate(factor):
                product_polynomial[i + j] += left * right
        polynomial = product_polynomial
    cyclotomic = [1] * prime
    while len(polynomial) >= len(cyclotomic):
        leading = polynomial[-1]
        if leading:
            shift = len(polynomial) - len(cyclotomic)
            for index, coefficient in enumerate(cyclotomic):
                polynomial[shift + index] -= leading * coefficient
        while polynomial and polynomial[-1] == 0:
            polynomial.pop()
    return tuple(polynomial + [0] * (prime - 1 - len(polynomial)))


def verify() -> dict[str, object]:
    factor_checks = 0
    for prime in (3, 5, 7, 11):
        for multiplier in range(1, 2 * prime + 1):
            residues = normalized_vanishing_factor_residues(prime * multiplier, prime)
            expected = [0] * len(residues)
            expected[0] = 1
            expected[prime - 1] = -1 % prime
            if residues != tuple(expected):
                raise AssertionError((prime, multiplier, residues))
            factor_checks += 1

    formula_checks = 0
    for prime in (3, 5, 7, 11):
        for defect in range(1, 3 * prime + 2):
            for q in range(1, 3 * prime + 2):
                transformed = saturated_residue_jet(q, defect, prime)
                closed = saturated_residue_closed(q, defect, prime)
                if transformed != closed:
                    raise AssertionError((prime, defect, q, transformed, closed))
                formula_checks += 1

    if sum(LEFT) != 35 or sum(RIGHT) != 35:
        raise AssertionError((sum(LEFT), sum(RIGHT)))
    if maximal_prime_profile(LEFT) != (3, (5,)):
        raise AssertionError(maximal_prime_profile(LEFT))
    if maximal_prime_profile(RIGHT) != (3, (5,)):
        raise AssertionError(maximal_prime_profile(RIGHT))
    left_block = prod(range(3, 7))
    right_block = prod(range(4, 8))
    left_nondivisible = tuple(part for part in LEFT if part % PRIME)
    right_nondivisible = tuple(part for part in RIGHT if part % PRIME)
    if left_block * prod(left_nondivisible) != right_block * prod(right_nondivisible):
        raise AssertionError("the exact factorial/product balance failed")
    left_denominator = denominator_remainder(left_nondivisible, PRIME)
    right_denominator = denominator_remainder(right_nondivisible, PRIME)
    if left_denominator != (-1, -2, -3, 1):
        raise AssertionError(left_denominator)
    if right_denominator != tuple(-entry for entry in left_denominator):
        raise AssertionError((left_denominator, right_denominator))
    if p_valuation(left_block, PRIME) != p_valuation(right_block, PRIME):
        raise AssertionError((left_block, right_block))
    valuation = p_valuation(left_block, PRIME)
    if (left_block // PRIME**valuation + right_block // PRIME**valuation) % PRIME:
        raise AssertionError("the witness must pass the leading residue condition")

    left_jet = saturated_residue_closed(3, 3, PRIME)
    right_jet = saturated_residue_closed(4, 3, PRIME)
    if left_jet != (1, 2, 0) or right_jet != (1, 3, 0):
        raise AssertionError((left_jet, right_jet))
    exact = cross_report(LEFT, RIGHT, 3)
    if exact != {
        "nominal_order": 10,
        "cancelled_orders": 1,
        "actual_order": 9,
        "determinant_zero": 7,
        "residual_order": 2,
    }:
        raise AssertionError(exact)

    blind_left = saturated_residue_closed(8, 14, 3)
    blind_right = saturated_residue_closed(6, 14, 3)
    if blind_left != (1,) + (0,) * 13 or blind_right != blind_left:
        raise AssertionError((blind_left, blind_right))

    report: dict[str, object] = {
        "theorem": "universal saturated whole-jet residue",
        "local_factor_checks": factor_checks,
        "closed_formula_checks": formula_checks,
        "witness_prime": PRIME,
        "witness_width": 35,
        "witness_defect": 3,
        "left_divisible": 3,
        "right_divisible": 4,
        "left_residue_jet": left_jet,
        "right_residue_jet": right_jet,
        "cube_family_residue_blind": blind_left,
        **exact,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    report = verify()
    print(
        "VERIFIED saturated whole-jet residue; "
        f"factor_checks={report['local_factor_checks']}; "
        f"formula_checks={report['closed_formula_checks']}; "
        f"witness_cancelled={report['cancelled_orders']}; "
        f"residual_order={report['residual_order']}; "
        f"sha256={report['sha256']}"
    )


if __name__ == "__main__":
    main()
