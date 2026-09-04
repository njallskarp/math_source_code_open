"""Exact verifier for the complete cubic-root jet modulo pi^3."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from functools import cache
from math import comb, factorial

Element = tuple[Fraction, Fraction]
Series = list[Element]
Partition = tuple[int, ...]

ZERO: Element = (Fraction(0), Fraction(0))
ONE: Element = (Fraction(1), Fraction(0))
ZETA: Element = (Fraction(0), Fraction(1))
PI: Element = (Fraction(1), Fraction(-1))

LEFT_NONDIVISIBLE = (7, 4, 4, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1)
RIGHT_NONDIVISIBLE = (11, 7, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1)
DEFECT = 14


def family(parameter: int) -> tuple[Partition, Partition]:
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


def add(left: Element, right: Element) -> Element:
    return left[0] + right[0], left[1] + right[1]


def neg(value: Element) -> Element:
    return -value[0], -value[1]


def scale(value: Element, scalar: int | Fraction) -> Element:
    return value[0] * scalar, value[1] * scalar


def mul(left: Element, right: Element) -> Element:
    a, b = left
    c, d = right
    # zeta^2=-1-zeta.
    return a * c - b * d, a * d + b * c - b * d


def power(base: Element, exponent: int) -> Element:
    if exponent < 0:
        return power(inverse(base), -exponent)
    result = ONE
    while exponent:
        if exponent & 1:
            result = mul(result, base)
        base = mul(base, base)
        exponent //= 2
    return result


def inverse(value: Element) -> Element:
    a, b = value
    norm = a * a - a * b + b * b
    if not norm:
        raise ZeroDivisionError(value)
    result = (a - b) / norm, -b / norm
    if mul(value, result) != ONE:
        raise AssertionError("field inversion failed")
    return result


def p_valuation_integer(value: int, prime: int = 3) -> int:
    if not value:
        raise ValueError("zero has infinite valuation")
    value = abs(value)
    valuation = 0
    while value % prime == 0:
        valuation += 1
        value //= prime
    return valuation


def p_valuation_fraction(value: Fraction, prime: int = 3) -> int:
    if not value:
        raise ValueError("zero has infinite valuation")
    return p_valuation_integer(value.numerator, prime) - p_valuation_integer(
        value.denominator, prime
    )


def pi_valuation(value: Element) -> int | None:
    if value == ZERO:
        return None
    a, b = value
    norm = a * a - a * b + b * b
    return p_valuation_fraction(norm)


def residue_fraction(value: Fraction, prime: int = 3) -> int:
    valuation = p_valuation_fraction(value, prime) if value else 1
    if valuation < 0:
        raise ValueError(f"nonintegral rational coordinate: {value}")
    if valuation > 0:
        return 0
    return value.numerator * pow(value.denominator, -1, prime) % prime


def unit_residue_after_division(value: Element, valuation: int) -> int:
    if pi_valuation(value) != valuation:
        raise ValueError((value, valuation, pi_valuation(value)))
    quotient = mul(value, power(PI, -valuation))
    return (residue_fraction(quotient[0]) + residue_fraction(quotient[1])) % 3


def congruent(left: Element, right: Element, modulus_power: int) -> bool:
    valuation = pi_valuation(add(left, neg(right)))
    return valuation is None or valuation >= modulus_power


def series_product(left: Series, right: Series, cutoff: int) -> Series:
    result = [ZERO] * cutoff
    for i, a in enumerate(left[:cutoff]):
        for j, b in enumerate(right[: cutoff - i]):
            result[i + j] = add(result[i + j], mul(a, b))
    return result


def series_inverse(denominator: Series, cutoff: int) -> Series:
    if not denominator or denominator[0] == ZERO:
        raise ZeroDivisionError("series constant term")
    result = [ZERO] * cutoff
    result[0] = inverse(denominator[0])
    for degree in range(1, cutoff):
        total = ZERO
        for index in range(1, min(degree, len(denominator) - 1) + 1):
            total = add(total, mul(denominator[index], result[degree - index]))
        result[degree] = neg(mul(result[0], total))
    return result


def multiply_factors(factors: list[Series], cutoff: int) -> Series:
    result = [ONE] + [ZERO] * (cutoff - 1)
    for factor in factors:
        result = series_product(result, factor, cutoff)
    return result


def exact_denominator_factor(weight: int, root: Element, vanishes: bool, cutoff: int) -> Series:
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
def exact_local_analytic_jet(
    partition: Partition, at_one: bool, cutoff: int
) -> tuple[Element, ...]:
    root = ONE if at_one else ZETA
    weights = (1, *partition)
    vanishing = [at_one or weight % 3 == 0 for weight in weights]
    order = sum(vanishing)
    cutoff = min(cutoff, order)
    inverse_factors = [
        series_inverse(exact_denominator_factor(weight, root, does_vanish, cutoff), cutoff)
        for weight, does_vanish in zip(weights, vanishing, strict=True)
    ]
    return tuple(multiply_factors(inverse_factors, cutoff))


@cache
def binomial_polynomial(top_shift: int) -> tuple[Fraction, ...]:
    result = [Fraction(1)]
    for shift in range(1, top_shift + 1):
        next_result = [Fraction(0)] * (len(result) + 1)
        for degree, coefficient in enumerate(result):
            next_result[degree] += shift * coefficient
            next_result[degree + 1] += coefficient
        result = next_result
    divisor = factorial(top_shift)
    return tuple(coefficient / divisor for coefficient in result)


def exact_pole_wave_top(partition: Partition, at_one: bool, depth: int) -> tuple[Element, ...]:
    order = len(partition) + 1 if at_one else sum(part % 3 == 0 for part in partition)
    jet = exact_local_analytic_jet(partition, at_one, min(order, depth + 1))
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


def exact_scaled_h(partition: Partition, cutoff: int) -> tuple[Element, ...]:
    root = list(exact_pole_wave_top(partition, False, cutoff - 1))
    at_one = list(exact_pole_wave_top(partition, True, cutoff - 1))
    root_inverse = inverse(root[0])
    one_inverse = inverse(at_one[0])
    root = [mul(coefficient, root_inverse) for coefficient in root]
    at_one = [mul(coefficient, one_inverse) for coefficient in at_one]
    quotient = series_product(root, series_inverse(at_one, cutoff), cutoff)
    return tuple(mul(coefficient, power(PI, degree)) for degree, coefficient in enumerate(quotient))


def cubic_divisible_factor() -> Series:
    # 1-pi X+(pi-1)X^2 modulo pi^3.
    return [ONE, neg(PI), add(PI, neg(ONE))]


def one_nondisible_factor(weight: int) -> Series:
    if weight % 3 == 0:
        raise ValueError("a nondivisible weight is required")
    return [
        ONE,
        scale(PI, Fraction(-(weight - 1), 2)),
        scale(power(PI, 2), Fraction((weight - 1) * (weight - 2), 6)),
    ]


def root_nondisible_factor(weight: int) -> Series:
    if weight % 3 == 0:
        raise ValueError("a nondivisible weight is required")
    root_power = power(ZETA, weight)
    denominator_inverse = inverse(add(ONE, neg(root_power)))
    result = [ONE]
    for degree in range(1, 4):
        result.append(
            mul(
                scale(
                    mul(root_power, power(PI, degree)),
                    (-1) ** (degree + 1) * comb(weight, degree),
                ),
                denominator_inverse,
            )
        )
    return result


def lifted_local_jet(partition: Partition, at_one: bool, cutoff: int) -> tuple[Element, ...]:
    factors: list[Series] = []
    for weight in (1, *partition):
        if weight % 3 == 0:
            denominator = cubic_divisible_factor()
        elif at_one:
            denominator = one_nondisible_factor(weight)
        else:
            denominator = root_nondisible_factor(weight)
        factors.append(series_inverse(denominator, cutoff))
    return tuple(multiply_factors(factors, cutoff))


def falling(start: int, length: int) -> int:
    result = 1
    for offset in range(length):
        result *= start - offset
    return result


def binomial_correction(length: int, cutoff: int) -> Series:
    result = [ONE] + [ZERO] * (cutoff - 1)
    for shift in range(1, length + 1):
        factor = [ONE]
        if cutoff > 1:
            factor.append(scale(PI, shift))
        result = series_product(result, factor, cutoff)
    return result


def lifted_wave(local_jet: tuple[Element, ...], pole_order: int, cutoff: int) -> Series:
    result = [ZERO] * cutoff
    for degree, coefficient in enumerate(local_jet[: min(pole_order, cutoff)]):
        scalar = falling(pole_order - 1, degree)
        if not scalar:
            continue
        correction = binomial_correction(pole_order - degree - 1, cutoff - degree)
        for extra, correction_coefficient in enumerate(correction):
            result[degree + extra] = add(
                result[degree + extra],
                scale(mul(coefficient, correction_coefficient), scalar),
            )
    return result


def lifted_scaled_h(partition: Partition, cutoff: int) -> tuple[Element, ...]:
    root_order = sum(part % 3 == 0 for part in partition)
    one_order = len(partition) + 1
    root_local = lifted_local_jet(partition, False, cutoff)
    one_local = lifted_local_jet(partition, True, cutoff)
    root_wave = lifted_wave(root_local, root_order, cutoff)
    one_wave = lifted_wave(one_local, one_order, cutoff)
    return tuple(series_product(root_wave, series_inverse(one_wave, cutoff), cutoff))


def complete_difference_layer(
    left: Partition, right: Partition, cutoff: int, layer: int
) -> tuple[int, ...]:
    left_h = exact_scaled_h(left, cutoff)
    right_h = exact_scaled_h(right, cutoff)
    result = []
    for left_coefficient, right_coefficient in zip(left_h, right_h, strict=True):
        difference = add(left_coefficient, neg(right_coefficient))
        valuation = pi_valuation(difference)
        if valuation is not None and valuation < layer:
            raise AssertionError((difference, valuation, layer))
        result.append(unit_residue_after_division(difference, layer) if valuation == layer else 0)
    return tuple(result)


def verify() -> dict[str, object]:
    local_factor_checks = 0
    model = cubic_divisible_factor()
    for multiplier in range(1, 41):
        weight = 3 * multiplier
        exact = [
            scale(
                power(PI, degree),
                Fraction((-1) ** degree * comb(weight, degree + 1), weight),
            )
            for degree in range(weight)
        ]
        for degree, coefficient in enumerate(exact):
            expected = model[degree] if degree < len(model) else ZERO
            if not congruent(coefficient, expected, 3):
                raise AssertionError((weight, degree, coefficient, expected))
            local_factor_checks += 1

    left, right = family(0)
    exact_left = exact_scaled_h(left, DEFECT)
    exact_right = exact_scaled_h(right, DEFECT)
    model_left = lifted_scaled_h(left, DEFECT)
    model_right = lifted_scaled_h(right, DEFECT)
    for exact, lifted in zip(exact_left, model_left, strict=True):
        if not congruent(exact, lifted, 3):
            raise AssertionError((exact, lifted))
    for exact, lifted in zip(exact_right, model_right, strict=True):
        if not congruent(exact, lifted, 3):
            raise AssertionError((exact, lifted))

    layer = complete_difference_layer(left, right, DEFECT, 2)
    expected_layer = (0, 0, 0, 1) + (0,) * 10
    if layer != expected_layer:
        raise AssertionError(layer)
    differences = [
        add(left_coefficient, neg(right_coefficient))
        for left_coefficient, right_coefficient in zip(exact_left, exact_right, strict=True)
    ]
    if differences[:3] != [ZERO, ZERO, ZERO] or differences[3] == ZERO:
        raise AssertionError(differences[:4])
    nonzero_valuations = [
        valuation for value in differences if (valuation := pi_valuation(value)) is not None
    ]
    if min(nonzero_valuations) != 2:
        raise AssertionError(nonzero_valuations)

    parameter_checks = 0
    for parameter in range(13):
        parameter_left, parameter_right = family(parameter)
        if sum(parameter_left) != 63 + 18 * parameter:
            raise AssertionError((parameter, sum(parameter_left)))
        if sum(parameter_right) != sum(parameter_left):
            raise AssertionError((parameter, sum(parameter_right)))
        if complete_difference_layer(parameter_left, parameter_right, DEFECT, 2) != expected_layer:
            raise AssertionError(parameter)
        parameter_checks += 1

    # The lifted wave transform has uniformly bounded degree modulo pi^3.
    transform_degree_checks = 0
    for pole_order in range(1, 61):
        local = lifted_local_jet((3,) * pole_order, True, 12)
        wave = lifted_wave(local, pole_order + 1, 12)
        for degree in range(6, len(wave)):
            valuation = pi_valuation(wave[degree])
            if valuation is not None and valuation < 3:
                raise AssertionError((pole_order, degree, wave[degree], valuation))
        transform_degree_checks += 1

    report: dict[str, object] = {
        "theorem": "complete cubic-root lift modulo pi^3",
        "local_factor_checks": local_factor_checks,
        "parameter_checks": parameter_checks,
        "transform_degree_checks": transform_degree_checks,
        "defect": DEFECT,
        "minimum_difference_valuation": 2,
        "associated_graded_difference": layer,
        "residual_order": 11,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def main() -> None:
    report = verify()
    print(
        "VERIFIED complete cubic lift; "
        f"factor_checks={report['local_factor_checks']}; "
        f"parameter_checks={report['parameter_checks']}; "
        f"transform_checks={report['transform_degree_checks']}; "
        f"graded_difference=X^3; residual_order={report['residual_order']}; "
        f"sha256={report['sha256']}"
    )


if __name__ == "__main__":
    main()
