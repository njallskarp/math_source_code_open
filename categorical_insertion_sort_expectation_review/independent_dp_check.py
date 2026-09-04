#!/usr/bin/env python3
"""Independent exact DP audit of categorical inversion moments.

Unlike the submitted checker, this program never generates multiset words or
i.i.d. words.  It appends a final category to count/inversion states and
aggregates exact multiplicities or Fraction-valued probability masses.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import cache
from hashlib import sha256
from itertools import product
import json
from math import comb, factorial


@cache
def multiset_histogram(counts: tuple[int, ...]) -> tuple[int, ...]:
    """Return coefficients of the inversion polynomial for `counts`."""
    if any(count < 0 for count in counts):
        raise ValueError("counts must be nonnegative")
    if not any(counts):
        return (1,)

    coefficients: list[int] = []
    for letter, count in enumerate(counts):
        if count == 0:
            continue
        predecessor = list(counts)
        predecessor[letter] -= 1
        predecessor_tuple = tuple(predecessor)
        added_inversions = sum(predecessor_tuple[letter + 1 :])
        prior = multiset_histogram(predecessor_tuple)
        required = len(prior) + added_inversions
        if len(coefficients) < required:
            coefficients.extend([0] * (required - len(coefficients)))
        for inversions, multiplicity in enumerate(prior):
            coefficients[inversions + added_inversions] += multiplicity
    return tuple(coefficients)


def elementary_symmetric(values: tuple[Fraction | int, ...], degree: int):
    coefficients = [values[0] * 0 + 1] + [values[0] * 0] * degree
    for value in values:
        for index in range(degree, 0, -1):
            coefficients[index] += value * coefficients[index - 1]
    return coefficients[degree]


def moments(distribution: dict[int, Fraction] | tuple[int, ...]):
    if isinstance(distribution, tuple):
        weighted = {index: Fraction(mass) for index, mass in enumerate(distribution)}
    else:
        weighted = distribution
    total = sum(weighted.values(), Fraction(0))
    if total == 0:
        raise ValueError("distribution has zero mass")
    mean = sum(Fraction(value) * mass for value, mass in weighted.items()) / total
    variance = (
        sum((Fraction(value) - mean) ** 2 * mass for value, mass in weighted.items())
        / total
    )
    return mean, variance


def multinomial_count(counts: tuple[int, ...]) -> int:
    result = factorial(sum(counts))
    for count in counts:
        result //= factorial(count)
    return result


def fixed_formulas(counts: tuple[int, ...]):
    n = sum(counts)
    e2 = elementary_symmetric(counts, 2)
    e3 = elementary_symmetric(counts, 3)
    return Fraction(e2, 2), Fraction((n + 1) * e2 - e3, 12)


def iid_histogram(n: int, probabilities: tuple[Fraction, ...]) -> dict[int, Fraction]:
    """Aggregate the i.i.d. inversion law by (count-vector, inversion) states."""
    if n < 0 or any(probability < 0 for probability in probabilities):
        raise ValueError("invalid i.i.d. law")
    if sum(probabilities, Fraction(0)) != 1:
        raise ValueError("probabilities must sum to one")

    zero_counts = (0,) * len(probabilities)
    states: dict[tuple[tuple[int, ...], int], Fraction] = {(zero_counts, 0): Fraction(1)}
    for _ in range(n):
        next_states: defaultdict[tuple[tuple[int, ...], int], Fraction] = defaultdict(Fraction)
        for (counts, inversions), mass in states.items():
            for letter, probability in enumerate(probabilities):
                if probability == 0:
                    continue
                added_inversions = sum(counts[letter + 1 :])
                successor = list(counts)
                successor[letter] += 1
                next_states[(tuple(successor), inversions + added_inversions)] += mass * probability
        states = dict(next_states)

    distribution: defaultdict[int, Fraction] = defaultdict(Fraction)
    for (_, inversions), mass in states.items():
        distribution[inversions] += mass
    return dict(distribution)


def iid_formulas(n: int, probabilities: tuple[Fraction, ...]):
    s2 = sum(probability**2 for probability in probabilities)
    s3 = sum(probability**3 for probability in probabilities)
    mean = Fraction(n * (n - 1), 4) * (1 - s2)
    variance = (
        Fraction(comb(n, 2), 4) * (1 - s2**2)
        + Fraction(comb(n, 3), 6) * (1 + 8 * s3 - 9 * s2**2)
    )
    return mean, variance


def weak_compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for remainder in weak_compositions(total - first, parts - 1):
            yield (first,) + remainder


def audit_fixed_counts():
    vectors = 0
    for categories in range(1, 6):
        for counts in product(range(6), repeat=categories):
            if sum(counts) > 10:
                continue
            histogram = multiset_histogram(counts)
            assert sum(histogram) == multinomial_count(counts)
            assert histogram == histogram[::-1]
            assert moments(histogram) == fixed_formulas(counts)
            vectors += 1
    return vectors


def audit_iid_laws():
    laws = 0
    distributions = 0
    for denominator in (1, 2, 3, 4, 5):
        for categories in range(1, 5):
            for numerators in weak_compositions(denominator, categories):
                probabilities = tuple(Fraction(value, denominator) for value in numerators)
                for n in range(0, 8):
                    distribution = iid_histogram(n, probabilities)
                    assert sum(distribution.values(), Fraction(0)) == 1
                    assert moments(distribution) == iid_formulas(n, probabilities)
                    distributions += 1
                laws += 1
    return laws, distributions


def main() -> None:
    fixed_vectors = audit_fixed_counts()
    iid_laws, iid_distributions = audit_iid_laws()
    summary = {
        "arithmetic": "Python integers and Fraction",
        "fixed_count_vectors_including_zeros": fixed_vectors,
        "iid_distributions": iid_distributions,
        "iid_laws": iid_laws,
        "method": "last-letter state dynamic programming",
        "python": "3.12.12",
        "variance_stress_test": True,
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    print(f"summary={canonical}")
    print(f"result_sha256={sha256(canonical.encode('ascii')).hexdigest()}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
