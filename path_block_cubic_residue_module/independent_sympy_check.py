"""Independent SymPy reconstruction of the exact small-pole collision."""

from __future__ import annotations

from math import comb, factorial

import sympy as sp

P = 3
CUTOFF = 11
LEFT = (6, 5, 1)
RIGHT = (7, 3, 2)

symbol = sp.Symbol("z")
field = sp.QQ.alg_field_from_poly(sp.Poly(symbol**2 + symbol + 1, symbol))
ZETA = field.from_sympy(field.ext)
ONE = field.one
ZERO = field.zero
PI = ONE - ZETA


def scalar(value):
    return field.from_sympy(sp.Rational(value))


def inverse_series(denominator: list, cutoff: int) -> list:
    result = [ZERO] * cutoff
    result[0] = denominator[0] ** -1
    for degree in range(1, cutoff):
        total = ZERO
        for index in range(1, min(degree, len(denominator) - 1) + 1):
            total += denominator[index] * result[degree - index]
        result[degree] = -result[0] * total
    return result


def multiply_series(left: list, right: list, cutoff: int) -> list:
    result = [ZERO] * cutoff
    for i, a in enumerate(left[:cutoff]):
        for j, b in enumerate(right[: cutoff - i]):
            result[i + j] += a * b
    return result


def denominator_factor(weight: int, root, vanishes: bool, cutoff: int) -> list:
    root_power = root**weight
    if vanishes:
        return [
            root_power * scalar((-1) ** degree * comb(weight, degree + 1))
            for degree in range(min(weight, cutoff))
        ]
    result = [ONE - root_power]
    result.extend(
        root_power * scalar((-1) ** (degree + 1) * comb(weight, degree))
        for degree in range(1, min(weight, cutoff - 1) + 1)
    )
    return result


def analytic_jet(partition: tuple[int, ...], at_one: bool, cutoff: int) -> list:
    root = ONE if at_one else ZETA
    weights = (1, *partition)
    vanishing = [at_one or weight % P == 0 for weight in weights]
    order = sum(vanishing)
    cutoff = min(cutoff, order)
    result = [ONE] + [ZERO] * (cutoff - 1)
    for weight, does_vanish in zip(weights, vanishing, strict=True):
        denominator = denominator_factor(weight, root, does_vanish, cutoff)
        result = multiply_series(result, inverse_series(denominator, cutoff), cutoff)
    return result


def binomial_polynomial(top_shift: int) -> list[sp.Rational]:
    result = [sp.Rational(1)]
    for shift in range(1, top_shift + 1):
        next_result = [sp.Rational(0)] * (len(result) + 1)
        for degree, coefficient in enumerate(result):
            next_result[degree] += shift * coefficient
            next_result[degree + 1] += coefficient
        result = next_result
    divisor = factorial(top_shift)
    return [coefficient / divisor for coefficient in result]


def pole_top(partition: tuple[int, ...], at_one: bool, depth: int) -> list:
    order = len(partition) + 1 if at_one else sum(a % P == 0 for a in partition)
    jet = analytic_jet(partition, at_one, min(order, depth + 1))
    bases = [binomial_polynomial(order - index - 1) for index in range(len(jet))]
    result = []
    for drop in range(depth + 1):
        degree = order - 1 - drop
        coefficient = ZERO
        if degree >= 0:
            for index, local_coefficient in enumerate(jet):
                if degree < len(bases[index]):
                    coefficient += local_coefficient * scalar(bases[index][degree])
        result.append(coefficient)
    return result


def scaled_h(partition: tuple[int, ...]) -> list:
    root = pole_top(partition, False, CUTOFF - 1)
    at_one = pole_top(partition, True, CUTOFF - 1)
    root = [coefficient / root[0] for coefficient in root]
    at_one = [coefficient / at_one[0] for coefficient in at_one]
    quotient = multiply_series(root, inverse_series(at_one, CUTOFF), CUTOFF)
    return [coefficient * PI**degree for degree, coefficient in enumerate(quotient)]


def fraction(value) -> sp.Rational:
    return sp.Rational(int(value.numerator), int(value.denominator))


def coordinates(value) -> tuple[sp.Rational, sp.Rational]:
    entries = value.to_list()
    if len(entries) == 1:
        return fraction(entries[0]), sp.Rational(0)
    if len(entries) != 2:
        raise AssertionError(entries)
    return fraction(entries[1]), fraction(entries[0])


def valuation_integer(value: int) -> int:
    value = abs(value)
    result = 0
    while value and value % 3 == 0:
        result += 1
        value //= 3
    return result


def valuation_rational(value: sp.Rational) -> int:
    return valuation_integer(int(value.p)) - valuation_integer(int(value.q))


def pi_valuation(value) -> int | None:
    if value == ZERO:
        return None
    a, b = coordinates(value)
    return valuation_rational(a * a - a * b + b * b)


def main() -> None:
    left = scaled_h(LEFT)
    right = scaled_h(RIGHT)
    differences = [a - b for a, b in zip(left, right, strict=True)]
    valuations = tuple(pi_valuation(value) for value in differences)
    if any(order is not None for order in valuations):
        raise AssertionError(valuations)
    print(
        "INDEPENDENT SYMPY PASS; pair=(6,5,1)/(7,3,2); coefficients=11; "
        "exact_transform_identity=true"
    )


if __name__ == "__main__":
    main()
