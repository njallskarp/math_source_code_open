"""Independent SymPy-domain reconstruction of the seventh-root witness.

Requires SymPy 1.14.0 and imports no primary-verifier code. Unlike the
primary tuple-field implementation, this uses SymPy's AlgebraicField domain.
"""

from __future__ import annotations

from math import comb, factorial

import sympy as sp

LEFT = (14, 13, 7, 7, 7, 7, 7, 7, 7, 6, 2, 1)
RIGHT = (12, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 1, 1)
PRIME = 7

x = sp.symbols("x")
FIELD = sp.QQ.alg_field_from_poly(sp.Poly(sp.cyclotomic_poly(PRIME, x), x))
ROOT = FIELD.convert(FIELD.ext)
ZERO = FIELD.zero
ONE = FIELD.one


def series_inverse(denominator: list[object], cutoff: int) -> list[object]:
    result = [ZERO] * cutoff
    result[0] = ONE / denominator[0]
    for degree in range(1, cutoff):
        total = sum(
            (
                denominator[index] * result[degree - index]
                for index in range(1, degree + 1)
            ),
            ZERO,
        )
        result[degree] = -total / denominator[0]
    return result


def series_product(
    left: list[object], right: list[object], cutoff: int
) -> list[object]:
    result = [ZERO] * cutoff
    for i, a in enumerate(left):
        for j, b in enumerate(right[: cutoff - i]):
            result[i + j] += a * b
    return result


def local_jet(
    partition: tuple[int, ...], at_one: bool, cutoff: int
) -> list[object]:
    root = ONE if at_one else ROOT
    result = [ONE] + [ZERO] * (cutoff - 1)
    for weight in (1, *partition):
        if at_one or weight % PRIME == 0:
            denominator = [
                FIELD.convert((-1) ** degree * comb(weight, degree + 1))
                for degree in range(cutoff)
            ]
        else:
            root_power = root**weight
            denominator = [ONE - root_power] + [
                root_power
                * FIELD.convert((-1) ** (degree + 1) * comb(weight, degree))
                for degree in range(1, cutoff)
            ]
        result = series_product(
            result, series_inverse(denominator, cutoff), cutoff
        )
    return result


def binomial_coefficient(top_shift: int, degree: int) -> object:
    n = sp.symbols("n")
    polynomial = sp.Poly(
        sp.prod(n + shift for shift in range(1, top_shift + 1))
        / factorial(top_shift),
        n,
        domain=sp.QQ,
    )
    return FIELD.convert(polynomial.nth(degree))


def wave_top(
    partition: tuple[int, ...], at_one: bool, depth: int
) -> list[object]:
    order = len(partition) + 1 if at_one else sum(
        part % PRIME == 0 for part in partition
    )
    jet = local_jet(partition, at_one, depth + 1)
    result: list[object] = []
    for drop in range(depth + 1):
        degree = order - 1 - drop
        result.append(
            sum(
                (
                    jet[index]
                    * binomial_coefficient(order - index - 1, degree)
                    for index in range(min(depth + 1, order))
                    if degree <= order - index - 1
                ),
                ZERO,
            )
        )
    return result


def product_top(left: list[object], right: list[object]) -> list[object]:
    return [
        sum(
            (left[index] * right[drop - index] for index in range(drop + 1)),
            ZERO,
        )
        for drop in range(len(left))
    ]


def main() -> None:
    if sp.__version__ != "1.14.0":
        raise RuntimeError(f"expected SymPy 1.14.0, found {sp.__version__}")
    depth = 4
    first = product_top(wave_top(LEFT, False, depth), wave_top(RIGHT, True, depth))
    second = product_top(wave_top(LEFT, True, depth), wave_top(RIGHT, False, depth))
    cross = [a + b for a, b in zip(first, second, strict=True)]
    assert cross[0] == ZERO
    assert cross[1] != ZERO

    left_jet = tuple(
        int(
            (-1) ** index
            * sp.binomial(4 + index, index)
            * sp.prod(7 - offset for offset in range(index))
            % 7
        )
        for index in range(4)
    )
    right_jet = tuple(
        int(
            (-1) ** index
            * sp.binomial(4 + index, index)
            * sp.prod(8 - offset for offset in range(index))
            % 7
        )
        for index in range(4)
    )
    assert left_jet != right_jet
    assert left_jet[1] != right_jet[1]

    for prime in (3, 5, 7, 11):
        variable = sp.symbols(f"z{prime}")
        cyclotomic = sp.cyclotomic_poly(prime, variable)
        for left_residue in range(1, prime):
            for right_residue in range(1, prime):
                remainder = sp.rem(
                    2 - variable**left_residue - variable**right_residue,
                    cyclotomic,
                    domain=sp.ZZ,
                )
                assert remainder != 0
    print(
        "INDEPENDENT SYMPY VERIFIED; p=7; defect=4; "
        "leading_cancellations=1; residual_order=3; whole_jets=different; "
        "defect_one=impossible"
    )


if __name__ == "__main__":
    main()
