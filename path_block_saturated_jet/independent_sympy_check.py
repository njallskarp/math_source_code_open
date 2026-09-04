"""Independent SymPy reconstruction of the saturated witness and residue jet."""

from __future__ import annotations

from math import comb, factorial

import sympy as sp

P = 5
LEFT = (12, 7, 5, 5, 5, 1)
RIGHT = (10, 5, 5, 5, 4, 3, 3)

z = sp.Symbol("z")
field = sp.QQ.alg_field_from_poly(sp.Poly(sp.cyclotomic_poly(P, z), z))
ZETA = field.from_sympy(field.ext)
ZERO = field.zero
ONE = field.one


def scalar(value: int | sp.Rational):
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
        factor = denominator_factor(weight, root, does_vanish, cutoff)
        result = multiply_series(result, inverse_series(factor, cutoff), cutoff)
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


def product_top(left: list, right: list) -> list:
    return [
        sum(
            (left[index] * right[drop - index] for index in range(drop + 1)),
            ZERO,
        )
        for drop in range(len(left))
    ]


def exact_cross_cancellations() -> int:
    first = product_top(pole_top(LEFT, False, 3), pole_top(RIGHT, True, 3))
    second = product_top(pole_top(LEFT, True, 3), pole_top(RIGHT, False, 3))
    cross = [a + b for a, b in zip(first, second, strict=True)]
    return next(index for index, coefficient in enumerate(cross) if coefficient != ZERO)


def falling(start: int, length: int) -> int:
    result = 1
    for offset in range(length):
        result *= start - offset
    return result


def invert_mod(series: list[int], cutoff: int, prime: int) -> list[int]:
    result = [0] * cutoff
    result[0] = pow(series[0], -1, prime)
    for degree in range(1, cutoff):
        result[degree] = (
            -result[0]
            * sum(
                series[index] * result[degree - index]
                for index in range(1, min(degree, len(series) - 1) + 1)
            )
            % prime
        )
    return result


def multiply_mod(left: list[int], right: list[int], cutoff: int, prime: int) -> list[int]:
    result = [0] * cutoff
    for i, a in enumerate(left):
        for j, b in enumerate(right[: cutoff - i]):
            result[i + j] = (result[i + j] + a * b) % prime
    return result


def residue_jet(q: int, defect: int, prime: int) -> tuple[int, ...]:
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
    return tuple(multiply_mod(numerator, invert_mod(denominator, defect, prime), defect, prime))


def main() -> None:
    cancellations = exact_cross_cancellations()
    left_jet = residue_jet(3, 3, 5)
    right_jet = residue_jet(4, 3, 5)
    blind = residue_jet(8, 14, 3) == residue_jet(6, 14, 3)
    if cancellations != 1 or left_jet != (1, 2, 0) or right_jet != (1, 3, 0):
        raise AssertionError((cancellations, left_jet, right_jet))
    if not blind:
        raise AssertionError("the cube family must lie in the residue-blind stratum")
    print(
        "INDEPENDENT SYMPY PASS; exact_p5_cancellations=1; "
        "left_jet=(1,2,0); right_jet=(1,3,0); cube_family_blind=True"
    )


if __name__ == "__main__":
    main()
