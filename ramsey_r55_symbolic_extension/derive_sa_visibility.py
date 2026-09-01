#!/usr/bin/env python3
"""Exact derivation of the SA visibility threshold for R(5,5,42) extension.

All arithmetic is rational.  A multilinear polynomial is represented by a
dictionary from a square-free monomial to its coefficient; multiplication
automatically reduces x_i^2=x_i.  No Ramsey graphs or numerical solvers are
used.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


N = 42
K4 = (0, 1, 2, 3)
Polynomial = dict[frozenset[int], Fraction]


def clean(poly: Polynomial) -> Polynomial:
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def add(*polys: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return clean(result)


def scale(poly: Polynomial, factor: int | Fraction) -> Polynomial:
    return clean({monomial: coefficient * factor for monomial, coefficient in poly.items()})


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = left_monomial | right_monomial
            result[monomial] = result.get(monomial, Fraction(0)) + (
                left_coefficient * right_coefficient
            )
    return clean(result)


def constant(value: int) -> Polynomial:
    return {frozenset(): Fraction(value)}


def variable(index: int) -> Polynomial:
    return {frozenset((index,)): Fraction(1)}


def one_minus(index: int) -> Polynomial:
    return add(constant(1), scale(variable(index), -1))


def product(polys: list[Polynomial]) -> Polynomial:
    result = constant(1)
    for poly in polys:
        result = multiply(result, poly)
    return result


def uniform_expectation(poly: Polynomial) -> Fraction:
    """Evaluate the moment functional y_S=2^{-|S|}."""
    return sum(
        coefficient * Fraction(1, 2 ** len(monomial))
        for monomial, coefficient in poly.items()
    )


def atoms_of_degree_at_most(max_degree: int):
    """Yield x_I product(1-x_j), with I,J disjoint and |I|+|J| <= d."""
    yield (), (), constant(1)
    for degree in range(1, max_degree + 1):
        for support in itertools.combinations(range(N), degree):
            for mask in range(1 << degree):
                positive = tuple(support[i] for i in range(degree) if mask >> i & 1)
                negative = tuple(support[i] for i in range(degree) if not (mask >> i & 1))
                atom = product(
                    [variable(i) for i in positive]
                    + [one_minus(i) for i in negative]
                )
                yield positive, negative, atom


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main() -> None:
    red_clause = add(constant(3), *[scale(variable(i), -1) for i in K4])
    blue_clause = add(constant(-1), *[variable(i) for i in K4])
    degree_low = add(constant(-18), *[variable(i) for i in range(N)])
    degree_high = add(constant(24), *[scale(variable(i), -1) for i in range(N)])
    constraints = {
        "red_k4": red_clause,
        "blue_k4": blue_clause,
        "degree_low": degree_low,
        "degree_high": degree_high,
    }

    minima: dict[str, Fraction | None] = {name: None for name in constraints}
    atom_count = 0
    inequality_check_count = 0
    for _positive, _negative, atom in atoms_of_degree_at_most(2):
        atom_count += 1
        for name, inequality in constraints.items():
            value = uniform_expectation(multiply(atom, inequality))
            if value < 0:
                raise AssertionError(f"negative uniform moment for {name}: {value}")
            current = minima[name]
            minima[name] = value if current is None or value < current else current
            inequality_check_count += 1

    red_multiplier = product([variable(i) for i in K4[:3]])
    red_forbidden = product([variable(i) for i in K4])
    red_identity = multiply(red_clause, red_multiplier)
    if red_identity != scale(red_forbidden, -1):
        raise AssertionError("red degree-three identity failed")

    blue_multiplier = product([one_minus(i) for i in K4[:3]])
    blue_forbidden = product([one_minus(i) for i in K4])
    blue_identity = multiply(blue_clause, blue_multiplier)
    if blue_identity != scale(blue_forbidden, -1):
        raise AssertionError("blue degree-three identity failed")

    result = {
        "arithmetic": "exact fractions",
        "core_order": N,
        "degree_window": [18, 24],
        "uniform_moments": "y_S = 2^(-|S|)",
        "maximum_verified_multiplier_degree": 2,
        "atom_count": atom_count,
        "inequality_check_count": inequality_check_count,
        "minimum_uniform_slack": {
            name: fraction_text(value) for name, value in minima.items() if value is not None
        },
        "degree_three_red_identity": "(3-x0-x1-x2-x3)x0x1x2 = -x0x1x2x3",
        "degree_three_blue_identity": "(-1+x0+x1+x2+x3)(1-x0)(1-x1)(1-x2) = -prod_{i=0}^3(1-x_i)",
        "conclusion": (
            "SA multiplier degrees 0, 1, and 2 cannot refute the signed-K4 "
            "extension system with the degree window; degree 3 is the first "
            "level that algebraically exposes each forbidden K4 atom."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
