#!/usr/bin/env python3
"""Exact definition-level checks for rank-one K_(s,t) perturbations.

The program enumerates atom assignments and multiplies edge polynomials.  It
does not use the leafless-edge-subgraph classification in the proof note.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import math
import platform
from fractions import Fraction
from typing import Sequence


Polynomial = tuple[Fraction, ...]


def multiply_linear(poly: Polynomial, constant: Fraction, linear: Fraction) -> Polynomial:
    """Multiply an exact coefficient tuple by constant + linear * epsilon."""
    result = [Fraction(0) for _ in range(len(poly) + 1)]
    for degree, coefficient in enumerate(poly):
        result[degree] += constant * coefficient
        result[degree + 1] += linear * coefficient
    return tuple(result)


def validate_distribution(
    values: Sequence[Fraction], weights: Sequence[Fraction]
) -> None:
    if not values or len(values) != len(weights):
        raise ValueError("values and weights must have the same positive length")
    if any(weight <= 0 for weight in weights):
        raise ValueError("weights must be positive")
    if sum(weights) != 1:
        raise ValueError("weights must sum to one")


def moment(
    values: Sequence[Fraction], weights: Sequence[Fraction], degree: int
) -> Fraction:
    validate_distribution(values, weights)
    if degree < 0:
        raise ValueError("moment degree must be nonnegative")
    return sum(weight * value**degree for value, weight in zip(values, weights))


def density_polynomial(
    s: int,
    t: int,
    p: Fraction,
    values: Sequence[Fraction],
    weights: Sequence[Fraction],
) -> Polynomial:
    """Enumerate t(K_(s,t), p + epsilon f tensor f) from the definition."""
    if s < 2 or t < 2:
        raise ValueError("s and t must both be at least two")
    if not 0 < p < 1:
        raise ValueError("p must lie strictly between zero and one")
    validate_distribution(values, weights)

    atom_count = len(values)
    edge_count = s * t
    total = [Fraction(0) for _ in range(edge_count + 1)]
    for assignment in itertools.product(range(atom_count), repeat=s + t):
        assignment_weight = math.prod(weights[index] for index in assignment)
        polynomial: Polynomial = (Fraction(1),)
        for left in range(s):
            for right in range(s, s + t):
                coefficient = values[assignment[left]] * values[assignment[right]]
                polynomial = multiply_linear(polynomial, p, coefficient)
        for degree, coefficient in enumerate(polynomial):
            total[degree] += assignment_weight * coefficient
    return tuple(total)


def direct_cut_coefficient(
    values: Sequence[Fraction], weights: Sequence[Fraction]
) -> Fraction:
    """Enumerate the cut norm of f tensor f over every pair of atom subsets."""
    validate_distribution(values, weights)
    atom_count = len(values)
    best = Fraction(0)
    for first_mask in range(1 << atom_count):
        for second_mask in range(1 << atom_count):
            integral = sum(
                weights[i] * weights[j] * values[i] * values[j]
                for i in range(atom_count)
                for j in range(atom_count)
                if (first_mask >> i) & 1 and (second_mask >> j) & 1
            )
            best = max(best, abs(integral))
    return best


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def run_checks(max_part: int) -> tuple[int, str]:
    if max_part < 2:
        raise ValueError("max_part must be at least two")

    # Mean zero with a nonzero third moment, preventing accidental odd-moment
    # cancellation from masking the fifth-order structural check.
    values = (Fraction(-2), Fraction(1))
    weights = (Fraction(1, 3), Fraction(2, 3))
    p = Fraction(2, 5)
    if moment(values, weights, 1) != 0:
        raise AssertionError("the test perturbation is not mean zero")
    m2 = moment(values, weights, 2)
    if moment(values, weights, 3) == 0:
        raise AssertionError("the test perturbation must have nonzero third moment")

    cut = direct_cut_coefficient(values, weights)
    l1 = sum(weight * abs(value) for value, weight in zip(values, weights))
    if cut != l1**2 / 4:
        raise AssertionError("rank-one cut coefficient mismatch")

    count = 0
    digest = hashlib.sha256()
    polynomials: dict[tuple[int, int], Polynomial] = {}
    for s in range(2, max_part + 1):
        for t in range(2, max_part + 1):
            polynomial = density_polynomial(s, t, p, values, weights)
            edge_count = s * t
            predicted_fourth = (
                math.comb(s, 2)
                * math.comb(t, 2)
                * p ** (edge_count - 4)
                * m2**4
            )
            expected = {
                0: p**edge_count,
                1: Fraction(0),
                2: Fraction(0),
                3: Fraction(0),
                4: predicted_fourth,
                5: Fraction(0),
            }
            for degree, coefficient in expected.items():
                actual = polynomial[degree] if degree < len(polynomial) else Fraction(0)
                if actual != coefficient:
                    raise AssertionError(
                        f"coefficient mismatch for s={s}, t={t}, degree={degree}: "
                        f"actual={actual}, expected={coefficient}"
                    )

            reverse = polynomials.get((t, s))
            if reverse is not None and polynomial != reverse:
                raise AssertionError("orientation symmetry failed")
            polynomials[s, t] = polynomial

            record = ":".join(
                [str(s), str(t), *(fraction_text(value) for value in polynomial)]
            )
            digest.update(record.encode("ascii"))
            digest.update(b"\n")
            count += 1
    return count, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-part", type=int, default=5)
    args = parser.parse_args()

    count, digest = run_checks(args.max_part)
    print(f"python={platform.python_version()}")
    print("p=2/5")
    print("values=-2,1")
    print("weights=1/3,2/3")
    print(f"max_part={args.max_part}")
    print(f"oriented_polynomials={count}")
    print(f"record_sha256={digest}")
    print("status=PASS")


if __name__ == "__main__":
    main()
