#!/usr/bin/env python3
"""Verify the divisor/order form of the odd-length rank enumerator."""

from __future__ import annotations

import hashlib
from math import isqrt

from verify_rank_formula import (
    factor_xn_plus_one,
    multiply_count_polynomial,
    predicted_histograms,
    reciprocal_orbits,
)


def divisors(n: int) -> list[int]:
    lower: list[int] = []
    upper: list[int] = []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            lower.append(d)
            if d * d != n:
                upper.append(n // d)
    return lower + upper[::-1]


def euler_phi(n: int) -> int:
    result = n
    p = 2
    remaining = n
    while p * p <= remaining:
        if remaining % p == 0:
            result -= result // p
            while remaining % p == 0:
                remaining //= p
        p += 1
    if remaining > 1:
        result -= result // remaining
    return result


def multiplicative_order_two(q: int) -> int:
    assert q > 1 and q % 2 == 1
    value = 1
    for order in range(1, euler_phi(q) + 1):
        value = (2 * value) % q
        if value == 1:
            return order
    raise AssertionError("order not found")


def arithmetic_orbit_schema(n: int) -> list[tuple[str, int]]:
    """Return one (type, degree) entry per reciprocal-factor orbit."""
    schema: list[tuple[str, int]] = []
    for q in divisors(n):
        if q == 1:
            continue
        order = multiplicative_order_two(q)
        factor_count = euler_phi(q) // order
        self_reciprocal = (
            order % 2 == 0 and pow(2, order // 2, q) == q - 1
        )
        if self_reciprocal:
            schema.extend(("S", order) for _ in range(factor_count))
        else:
            assert factor_count % 2 == 0
            schema.extend(("P", order) for _ in range(factor_count // 2))
    schema.sort(key=lambda item: (item[1], item[0]))
    return schema


def arithmetic_even_histogram(n: int) -> dict[int, int]:
    coefficients = [1]
    for orbit_type, d in arithmetic_orbit_schema(n):
        if orbit_type == "S":
            increment = d // 2
            active_count = (1 << d) - 1
        else:
            increment = d
            active_count = (1 << (2 * d)) - 1
        coefficients = multiply_count_polynomial(
            coefficients, increment, active_count
        )
    return {rank: count for rank, count in enumerate(coefficients) if count}


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for p in range(3, isqrt(n) + 1, 2):
        if n % p == 0:
            return False
    return True


def predicted_dichotomy_criterion(n: int) -> bool:
    if not is_prime(n):
        return False
    order = multiplicative_order_two(n)
    half = (n - 1) // 2
    return order == n - 1 or (order == half and half % 2 == 1)


def main() -> None:
    spectrum_digest = hashlib.sha256()
    dichotomy_lengths: list[int] = []

    # This compares cyclotomic-order arithmetic with actual polynomial
    # factorization and reciprocal pairing.
    for n in range(3, 24, 2):
        factor_schema = sorted(
            [
                (orbit_type, d)
                for orbit_type, d, _ in reciprocal_orbits(
                    factor_xn_plus_one(n)
                )
            ],
            key=lambda item: (item[1], item[0]),
        )
        arithmetic_schema = arithmetic_orbit_schema(n)
        assert arithmetic_schema == factor_schema
        factor_all, factor_even = predicted_histograms(
            reciprocal_orbits(factor_xn_plus_one(n))
        )
        arithmetic_even = arithmetic_even_histogram(n)
        assert arithmetic_even == factor_even
        assert {rank: 2 * count for rank, count in arithmetic_even.items()} == factor_all

    # A broader exact arithmetic survey checks all structural identities and
    # the dichotomy classification, without factoring polynomials.
    for n in range(3, 1000, 2):
        m = (n - 1) // 2
        schema = arithmetic_orbit_schema(n)
        component_dimension = sum(
            d if orbit_type == "S" else 2 * d
            for orbit_type, d in schema
        )
        assert component_dimension == n - 1

        even_histogram = arithmetic_even_histogram(n)
        assert sum(even_histogram.values()) == 1 << (n - 1)
        assert even_histogram[0] == 1
        assert max(even_histogram) == m

        full_rank_count = 1
        for orbit_type, d in schema:
            dimension = d if orbit_type == "S" else 2 * d
            full_rank_count *= (1 << dimension) - 1
        assert even_histogram[m] == full_rank_count

        dichotomy = set(even_histogram) == {0, m}
        assert dichotomy == predicted_dichotomy_criterion(n)
        if dichotomy:
            assert even_histogram == {0: 1, m: (1 << (n - 1)) - 1}
            dichotomy_lengths.append(n)

        spectrum_digest.update(f"n={n};".encode("ascii"))
        for rank, count in sorted(even_histogram.items()):
            spectrum_digest.update(f"{rank}:{count},".encode("ascii"))
        spectrum_digest.update(b"\n")

    print("odd-length arithmetic rank-enumerator certificate")
    print("factorization_agreement_odd_n_3_through_23=yes")
    print("arithmetic_identity_checks_odd_n_3_through_999=499")
    print("dichotomy_lengths_below_1000=" + ",".join(map(str, dichotomy_lengths)))
    print(f"spectrum_stream_sha256={spectrum_digest.hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
