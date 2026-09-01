#!/usr/bin/env python3
"""Verify the exact weight-two sum-one syndrome fiber formula."""

from __future__ import annotations

import hashlib
from collections import Counter
from itertools import combinations
from math import comb, gcd


def direct_syndrome(n: int, b: int, sigma: int) -> int:
    """Evaluate the defining double sum, without using the reflection proof."""
    m = (n - 1) // 2
    result = 0
    for s in range(1, m + 1):
        coordinate = 0
        for j in range(n):
            sigma_difference = ((sigma >> j) ^ (sigma >> ((j + s) % n))) & 1
            axis_difference = ((b >> j) ^ (b >> ((j + s) % n))) & 1
            coordinate ^= sigma_difference & axis_difference
        result |= coordinate << (s - 1)
    return result


def predicted_fiber(n: int, syndrome: int) -> int:
    m = (n - 1) // 2
    if syndrome.bit_count() % 2 == 0:
        return 0
    p = 1
    h = 0
    for s in range(1, m):
        p ^= (syndrome >> (s - 1)) & 1
        h += p
    zero_xor_pairs = m - 1 - h
    return (1 << (h + 1)) * comb(
        zero_xor_pairs, zero_xor_pairs // 2
    )


def exact_sum_one_fibers(n: int) -> Counter[int]:
    """Enumerate exact-sum-one sign words for the adjacent weight-two axis."""
    m = (n - 1) // 2
    b = 0b11
    fibers: Counter[int] = Counter()
    real_positions = range(2, n)
    for negative_reals in combinations(real_positions, m - 1):
        real_mask = sum(1 << j for j in negative_reals)
        for negative_imaginary in (0, 1):
            sigma = real_mask | (1 << negative_imaginary)
            fibers[direct_syndrome(n, b, sigma)] += 1
    return fibers


def canonical_shift(n: int, shift: int) -> int:
    shift %= n
    return min(shift, n - shift)


def verify_unit_decimation(n: int, d: int) -> None:
    """Check the coordinate permutation reducing separation d to 1."""
    assert gcd(n, d) == 1
    m = (n - 1) // 2
    adjacent_axis = 0b11
    separated_axis = 1 | (1 << d)
    for position in range(n):
        adjacent_sigma = 1 << position
        separated_sigma = 1 << ((d * position) % n)
        adjacent = direct_syndrome(n, adjacent_axis, adjacent_sigma)
        separated = direct_syndrome(n, separated_axis, separated_sigma)
        for s in range(1, m + 1):
            target_shift = canonical_shift(n, d * s)
            adjacent_bit = (adjacent >> (s - 1)) & 1
            separated_bit = (separated >> (target_shift - 1)) & 1
            assert adjacent_bit == separated_bit


def main() -> None:
    record_digest = hashlib.sha256()
    total_sign_words = 0
    unit_decimations = 0

    print("odd-length weight-two sum-one fiber certificate")
    for n in range(3, 22, 2):
        m = (n - 1) // 2
        fibers = exact_sum_one_fibers(n)
        allowed = [t for t in range(1 << m) if t.bit_count() % 2 == 1]
        assert set(fibers) == set(allowed)

        for syndrome in range(1 << m):
            observed = fibers[syndrome]
            expected = predicted_fiber(n, syndrome)
            assert observed == expected
            record_digest.update(
                f"n={n};t={syndrome:0{m}b};count={observed}\n".encode("ascii")
            )

        expected_total = 2 * comb(n - 2, m - 1)
        assert sum(fibers.values()) == expected_total
        total_sign_words += expected_total

        for d in range(1, n):
            if gcd(d, n) == 1:
                verify_unit_decimation(n, d)
                unit_decimations += 1

        multiplicities = [fibers[t] for t in allowed]
        print(
            f"n={n:2d} allowed_syndromes={len(allowed)} "
            f"min_fiber={min(multiplicities)} max_fiber={max(multiplicities)} "
            f"sign_words={expected_total}"
        )

    print(f"unit_decimations_checked={unit_decimations}")
    print(f"total_exact_sign_words_checked={total_sign_words}")
    print(f"fiber_record_sha256={record_digest.hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
