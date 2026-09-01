#!/usr/bin/env python3
"""Verify the odd-length CRT rank formula over F_2.

The script has no third-party dependencies.  It factors x^n+1 over F_2,
classifies irreducible factors under polynomial reciprocity, predicts the full
rank generating polynomial, and independently computes every binary matrix
D_b for every axis b at odd lengths n <= 17.
"""

from __future__ import annotations

import hashlib
from collections import Counter


def degree(p: int) -> int:
    return p.bit_length() - 1


def poly_divmod(a: int, b: int) -> tuple[int, int]:
    if b == 0:
        raise ZeroDivisionError
    q = 0
    db = degree(b)
    while a and degree(a) >= db:
        shift = degree(a) - db
        q ^= 1 << shift
        a ^= b << shift
    return q, a


def poly_mod(a: int, modulus: int) -> int:
    return poly_divmod(a, modulus)[1]


def poly_gcd(a: int, b: int) -> int:
    while b:
        a, b = b, poly_mod(a, b)
    return a


def poly_mul_mod(a: int, b: int, modulus: int) -> int:
    product = 0
    while b:
        if b & 1:
            product ^= a
        b >>= 1
        a <<= 1
    return poly_mod(product, modulus)


def reciprocal(p: int) -> int:
    d = degree(p)
    result = 0
    for j in range(d + 1):
        if (p >> j) & 1:
            result |= 1 << (d - j)
    return result


def is_irreducible(f: int) -> bool:
    """Rabin's criterion, with all possible small factor degrees tested."""
    d = degree(f)
    if d < 1 or (f & 1) == 0:
        return False
    x = poly_mod(0b10, f)
    frobenius_power = x
    for k in range(1, d + 1):
        frobenius_power = poly_mul_mod(
            frobenius_power, frobenius_power, f
        )
        if k <= d // 2 and poly_gcd(frobenius_power ^ x, f) != 1:
            return False
    return frobenius_power == x


def factor_xn_plus_one(n: int) -> list[int]:
    """Factor x^n+1 over F_2 by exact trial division.

    This deliberately simple implementation is fast for the tested n <= 23.
    Odd n makes x^n+1 square-free.
    """
    remaining = (1 << n) | 1
    factors: list[int] = []
    for d in range(1, n // 2 + 1):
        for middle in range(1 << max(d - 1, 0)):
            candidate = (1 << d) | 1 | (middle << 1)
            if not is_irreducible(candidate):
                continue
            quotient, remainder = poly_divmod(remaining, candidate)
            if remainder == 0:
                factors.append(candidate)
                remaining = quotient
    if remaining != 1:
        assert is_irreducible(remaining)
        factors.append(remaining)
    factors.sort(key=lambda p: (degree(p), p))
    product = 1
    for f in factors:
        raw = 0
        a = product
        b = f
        while b:
            if b & 1:
                raw ^= a
            b >>= 1
            a <<= 1
        product = raw
    assert product == ((1 << n) | 1)
    return factors


def reciprocal_orbits(factors: list[int]) -> list[tuple[str, int, tuple[int, ...]]]:
    factor_set = set(factors)
    seen: set[int] = set()
    result: list[tuple[str, int, tuple[int, ...]]] = []
    for f in factors:
        if f == 0b11 or f in seen:
            continue
        f_star = reciprocal(f)
        assert f_star in factor_set
        d = degree(f)
        if f_star == f:
            assert d % 2 == 0
            result.append(("S", d, (f,)))
            seen.add(f)
        else:
            assert degree(f_star) == d
            result.append(("P", d, tuple(sorted((f, f_star)))))
            seen.update((f, f_star))
    result.sort(key=lambda item: (item[1], item[0], item[2]))
    return result


def predicted_rank(b: int, orbits: list[tuple[str, int, tuple[int, ...]]]) -> int:
    rank = 0
    for orbit_type, d, fs in orbits:
        active = any(poly_mod(b, f) != 0 for f in fs)
        if active:
            rank += d // 2 if orbit_type == "S" else d
    return rank


def gf2_rank(columns: list[int]) -> int:
    pivots: dict[int, int] = {}
    for value in columns:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def direct_rank(n: int, b: int) -> int:
    """Rank D_b directly from its n columns, independently of factorization."""
    m = (n - 1) // 2
    columns: list[int] = []
    for j in range(n):
        column = 0
        for s in range(1, m + 1):
            bit = ((b >> ((j + s) % n)) ^ (b >> ((j - s) % n))) & 1
            column |= bit << (s - 1)
        columns.append(column)
    return gf2_rank(columns)


def multiply_count_polynomial(
    coefficients: list[int], increment: int, active_count: int
) -> list[int]:
    result = [0] * (len(coefficients) + increment)
    for rank, count in enumerate(coefficients):
        result[rank] += count
        result[rank + increment] += count * active_count
    return result


def predicted_histograms(
    orbits: list[tuple[str, int, tuple[int, ...]]]
) -> tuple[dict[int, int], dict[int, int]]:
    """Return rank counts for all axes and for even-weight axes."""
    coefficients = [1]
    for orbit_type, d, _ in orbits:
        if orbit_type == "S":
            increment = d // 2
            active_count = (1 << d) - 1
        else:
            increment = d
            active_count = (1 << (2 * d)) - 1
        coefficients = multiply_count_polynomial(
            coefficients, increment, active_count
        )
    even = {rank: count for rank, count in enumerate(coefficients) if count}
    all_axes = {rank: 2 * count for rank, count in even.items()}
    return all_axes, even


def format_histogram(histogram: dict[int, int]) -> str:
    return ",".join(f"{rank}:{count}" for rank, count in sorted(histogram.items()))


def surjective_even_axis_count(
    orbits: list[tuple[str, int, tuple[int, ...]]]
) -> int:
    result = 1
    for orbit_type, d, _ in orbits:
        component_dimension = d if orbit_type == "S" else 2 * d
        result *= (1 << component_dimension) - 1
    return result


def main() -> None:
    direct_digest = hashlib.sha256()
    tested_axes = 0
    expected_n21 = {
        0: 2,
        1: 6,
        3: 126,
        4: 378,
        6: 8190,
        7: 24570,
        9: 515970,
        10: 1547910,
    }
    expected_n23 = {0: 2, 11: 8388606}

    print("odd-length CRT rank-formula certificate")
    for n in range(3, 24, 2):
        factors = factor_xn_plus_one(n)
        assert factors[0] == 0b11
        orbits = reciprocal_orbits(factors)
        all_histogram, even_histogram = predicted_histograms(orbits)
        assert sum(all_histogram.values()) == 1 << n
        assert sum(even_histogram.values()) == 1 << (n - 1)

        orbit_schema = "+".join(
            f"{orbit_type}{d}" for orbit_type, d, _ in orbits
        )
        print(
            f"n={n:2d} orbit_schema={orbit_schema:<15s} "
            f"all_ranks={format_histogram(all_histogram)}"
        )

        if n <= 17:
            observed: Counter[int] = Counter()
            all_ones = (1 << n) - 1
            for b in range(1 << n):
                predicted = predicted_rank(b, orbits)
                direct = direct_rank(n, b)
                assert predicted == direct
                assert direct_rank(n, b ^ all_ones) == direct
                observed[direct] += 1
                direct_digest.update(
                    f"{n}:{b:0{n}b}:{predicted}:{direct}\n".encode("ascii")
                )
                tested_axes += 1
            assert dict(sorted(observed.items())) == all_histogram

        if n == 21:
            assert all_histogram == expected_n21
            assert surjective_even_axis_count(orbits) == 773955
            assert sum(
                count * (1 << rank) for rank, count in even_histogram.items()
            ) == 926456335
        if n == 23:
            assert all_histogram == expected_n23
            assert surjective_even_axis_count(orbits) == 4194303
            assert sum(
                count * (1 << rank) for rank, count in even_histogram.items()
            ) == 8589932545

    print(f"exhaustive_axes_n_le_17={tested_axes}")
    print(f"direct_record_sha256={direct_digest.hexdigest()}")
    print("n21_published_spectrum_match=yes")
    print("n23_prime_dichotomy_match=yes")
    print("n21_surjective_even_axes=773955")
    print("n21_total_even_image_points=926456335")
    print("n23_surjective_even_axes=4194303")
    print("n23_total_even_image_points=8589932545")
    print("status=PASS")


if __name__ == "__main__":
    main()
