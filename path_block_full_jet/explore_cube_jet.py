"""Exact exploratory cube-root jets for endpoint Hadamard products.

This file is deliberately independent of SymPy.  It works in
Q(zeta_3)=Q[z]/(z^2+z+1), expands the endpoint series locally, converts the
principal parts to coefficient-wave polynomials, and measures cancellation
between the two maximal cross waves.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from math import comb

K = tuple[Fraction, Fraction]
Poly = list[K]

ZERO: K = (Fraction(0), Fraction(0))
ONE: K = (Fraction(1), Fraction(0))
ZETA: K = (Fraction(0), Fraction(1))


def add(x: K, y: K) -> K:
    return (x[0] + y[0], x[1] + y[1])


def neg(x: K) -> K:
    return (-x[0], -x[1])


def mul(x: K, y: K) -> K:
    """Multiply using zeta^2=-zeta-1."""
    a, b = x
    c, d = y
    return (a * c - b * d, a * d + b * c - b * d)


def inv(x: K) -> K:
    a, b = x
    norm = a * a - a * b + b * b
    if not norm:
        raise ZeroDivisionError
    return ((a - b) / norm, -b / norm)


def scale(x: K, scalar: int | Fraction) -> K:
    return (x[0] * scalar, x[1] * scalar)


def power(x: K, exponent: int) -> K:
    result = ONE
    base = x
    while exponent:
        if exponent & 1:
            result = mul(result, base)
        base = mul(base, base)
        exponent //= 2
    return result


def series_inverse(denominator: Poly, cutoff: int) -> Poly:
    result = [ZERO] * cutoff
    inverse_constant = inv(denominator[0])
    result[0] = inverse_constant
    for degree in range(1, cutoff):
        total = ZERO
        for index in range(1, min(degree, len(denominator) - 1) + 1):
            total = add(total, mul(denominator[index], result[degree - index]))
        result[degree] = neg(mul(inverse_constant, total))
    return result


def series_product(left: Poly, right: Poly, cutoff: int) -> Poly:
    result = [ZERO] * cutoff
    for i, a in enumerate(left[:cutoff]):
        for j, b in enumerate(right[: cutoff - i]):
            result[i + j] = add(result[i + j], mul(a, b))
    return result


def factor_denominator(weight: int, root: K, vanishes: bool, cutoff: int) -> Poly:
    """Return the local denominator, with its simple u factor removed."""
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
    partition: tuple[int, ...], at_one: bool, cutoff: int | None = None
) -> Poly:
    """Coefficients of u^q F(alpha(1-u)) through degree q-1."""
    root = ONE if at_one else ZETA
    weights = (1, *partition)
    vanishing = [at_one or weight % 3 == 0 for weight in weights]
    order = sum(vanishing)
    if cutoff is None:
        cutoff = order
    cutoff = min(cutoff, order)
    result = [ONE] + [ZERO] * (cutoff - 1)
    for weight, does_vanish in zip(weights, vanishing, strict=True):
        denominator = factor_denominator(weight, root, does_vanish, cutoff)
        result = series_product(
            result, series_inverse(denominator, cutoff), cutoff
        )
    return result


@cache
def rational_binomial_polynomial(top_shift: int) -> tuple[Fraction, ...]:
    """Power-basis coefficients of binom(n+top_shift, top_shift)."""
    result = [Fraction(1)]
    for shift in range(1, top_shift + 1):
        product = [Fraction(0)] * (len(result) + 1)
        for degree, coefficient in enumerate(result):
            product[degree] += shift * coefficient
            product[degree + 1] += coefficient
        result = product
    divisor = 1
    for value in range(2, top_shift + 1):
        divisor *= value
    return tuple(coefficient / divisor for coefficient in result)


def pole_wave(partition: tuple[int, ...], at_one: bool) -> Poly:
    jet = local_analytic_jet(partition, at_one)
    order = len(jet)
    result = [ZERO] * order
    for index, coefficient in enumerate(jet):
        basis = rational_binomial_polynomial(order - index - 1)
        for degree, entry in enumerate(basis):
            result[degree] = add(result[degree], scale(coefficient, entry))
    return trim(result)


@cache
def pole_wave_top(partition: tuple[int, ...], at_one: bool, depth: int) -> tuple[K, ...]:
    """Return the top ``depth+1`` power coefficients, highest first."""
    order = len(partition) + 1 if at_one else sum(part % 3 == 0 for part in partition)
    jet = local_analytic_jet(partition, at_one, min(order, depth + 1))
    bases = [
        rational_binomial_polynomial(order - index - 1)
        for index in range(len(jet))
    ]
    result: Poly = []
    for drop in range(depth + 1):
        degree = order - 1 - drop
        coefficient = ZERO
        if degree < 0:
            result.append(coefficient)
            continue
        for index, local_coefficient in enumerate(jet):
            basis = bases[index]
            if degree < len(basis):
                coefficient = add(
                    coefficient, scale(local_coefficient, basis[degree])
                )
        result.append(coefficient)
    return tuple(result)


def product_top(left: Poly, right: Poly, depth: int) -> Poly:
    result = [ZERO] * (depth + 1)
    for drop in range(depth + 1):
        for index in range(drop + 1):
            result[drop] = add(result[drop], mul(left[index], right[drop - index]))
    return result


def cross_cancelled_orders(
    left: tuple[int, ...], right: tuple[int, ...], depth: int
) -> int:
    """Count initial zero coefficients of the cube-root maximal cross wave."""
    first = product_top(
        pole_wave_top(left, False, depth), pole_wave_top(right, True, depth), depth
    )
    second = product_top(
        pole_wave_top(left, True, depth), pole_wave_top(right, False, depth), depth
    )
    cross = [add(a, b) for a, b in zip(first, second, strict=True)]
    for index, coefficient in enumerate(cross):
        if coefficient != ZERO:
            return index
    return depth + 1


def trim(poly: Poly) -> Poly:
    while len(poly) > 1 and poly[-1] == ZERO:
        poly.pop()
    return poly


def polynomial_product(left: Poly, right: Poly) -> Poly:
    result = [ZERO] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = add(result[i + j], mul(a, b))
    return trim(result)


def polynomial_sum(left: Poly, right: Poly) -> Poly:
    result = [ZERO] * max(len(left), len(right))
    for index, coefficient in enumerate(left):
        result[index] = add(result[index], coefficient)
    for index, coefficient in enumerate(right):
        result[index] = add(result[index], coefficient)
    return trim(result)


def cross_jet_report(left: tuple[int, ...], right: tuple[int, ...]) -> dict[str, int]:
    left_order = sum(part % 3 == 0 for part in left)
    right_order = sum(part % 3 == 0 for part in right)
    if not left_order or not right_order:
        raise ValueError("both endpoints must have a cube-root pole")
    left_cross = polynomial_product(
        pole_wave(left, False), pole_wave(right, True)
    )
    right_cross = polynomial_product(
        pole_wave(left, True), pole_wave(right, False)
    )
    cross = polynomial_sum(left_cross, right_cross)
    nominal_order = left_order + len(right)
    if nominal_order != len(left) + right_order:
        raise ValueError("the cross-wave pole orders are unequal")
    actual_order = 0 if cross == [ZERO] else len(cross)
    determinant_zero = left_order + right_order
    return {
        "nominal_order": nominal_order,
        "actual_order": actual_order,
        "cancelled_orders": nominal_order - actual_order,
        "determinant_zero": determinant_zero,
        "residual_order": max(0, actual_order - determinant_zero),
    }


def main() -> None:
    examples = (
        (
            (4, 4, 3, 3, 3, 3, 1),
            (3, 3, 3, 3, 3, 2, 2, 2),
        ),
        (
            (5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1),
            (13, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1),
        ),
    )
    for left, right in examples:
        print(sum(left), cross_jet_report(left, right))


if __name__ == "__main__":
    main()
