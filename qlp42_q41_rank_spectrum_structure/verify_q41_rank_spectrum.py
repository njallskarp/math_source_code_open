#!/usr/bin/env python3
"""Structural certificate for the QLP-42 q=41 D_b rank spectrum."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

N = 21
FULL = (1 << N) - 1

# Irreducible factors of x^21+1 over F_2.
F1 = 0b11
F2 = 0b111
F3A = 0b1011
F3B = 0b1101
F6A = (1 << 6) | (1 << 4) | (1 << 2) | (1 << 1) | 1
F6B = (1 << 6) | (1 << 5) | (1 << 4) | (1 << 2) | 1
FACTORS = (F1, F2, F3A, F3B, F6A, F6B)


def degree(poly: int) -> int:
    return poly.bit_length() - 1


def poly_multiply(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
    return result


def poly_divmod(dividend: int, divisor: int) -> tuple[int, int]:
    quotient = 0
    divisor_degree = degree(divisor)
    while dividend and degree(dividend) >= divisor_degree:
        shift = degree(dividend) - divisor_degree
        quotient ^= 1 << shift
        dividend ^= divisor << shift
    return quotient, dividend


def poly_mod(dividend: int, divisor: int) -> int:
    return poly_divmod(dividend, divisor)[1]


def poly_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, poly_mod(left, right)
    return left


def field_multiply(left: int, right: int, modulus: int) -> int:
    return poly_mod(poly_multiply(left, right), modulus)


def field_square(value: int, modulus: int) -> int:
    return field_multiply(value, value, modulus)


def frobenius_power(value: int, power: int, modulus: int) -> int:
    for _ in range(power):
        value = field_square(value, modulus)
    return value


def reciprocal(poly: int) -> int:
    result = 0
    d = degree(poly)
    for index in range(d + 1):
        if (poly >> index) & 1:
            result |= 1 << (d - index)
    return result


def is_irreducible(poly: int) -> bool:
    d = degree(poly)
    x = poly_mod(0b10, poly)
    power = x
    for k in range(1, d // 2 + 1):
        power = field_square(power, poly)
        if poly_gcd(power ^ x, poly) != 1:
            return False
    return frobenius_power(x, d, poly) == x


def binary_rank(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for value in vectors:
        while value:
            pivot = degree(value)
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def verify_factorization() -> None:
    product = 1
    for factor in FACTORS:
        assert is_irreducible(factor)
        product = poly_multiply(product, factor)
    assert product == (1 << N) | 1
    assert reciprocal(F1) == F1
    assert reciprocal(F2) == F2
    assert reciprocal(F3A) == F3B
    assert reciprocal(F6A) == F6B
    assert [degree(factor) for factor in FACTORS] == [1, 2, 3, 3, 6, 6]


def self_reciprocal_rank_distribution() -> Counter[int]:
    # On F_4, inversion is the Frobenius t -> t^2 and
    # L_b(s)=b*s^2+b^2*s.
    result: Counter[int] = Counter()
    for b in range(1 << 2):
        b_squared = field_square(b, F2)
        columns = []
        for basis in (1, 2):
            value = field_multiply(b, field_square(basis, F2), F2)
            value ^= field_multiply(b_squared, basis, F2)
            columns.append(value)
        result[binary_rank(columns)] += 1
    assert result == Counter({1: 3, 0: 1})
    return result


def reciprocal_pair_rank_distribution(modulus: int) -> Counter[int]:
    # After identifying reciprocal fields, star swaps the two factors and
    # L_(u,v)(p,q)=u*q+v*p.  A nonzero pair is a surjection onto the field.
    d = degree(modulus)
    result: Counter[int] = Counter()
    basis = [1 << index for index in range(d)]
    for u in range(1 << d):
        for v in range(1 << d):
            columns = [field_multiply(v, value, modulus) for value in basis]
            columns += [field_multiply(u, value, modulus) for value in basis]
            result[binary_rank(columns)] += 1
    assert result == Counter({d: (1 << (2 * d)) - 1, 0: 1})
    return result


def predicted_rank(mask: int) -> int:
    epsilon = int(poly_mod(mask, F2) != 0)
    delta = int(poly_mod(mask, F3A) != 0 or poly_mod(mask, F3B) != 0)
    eta = int(poly_mod(mask, F6A) != 0 or poly_mod(mask, F6B) != 0)
    return epsilon + 3 * delta + 6 * eta


def rotate(mask: int, shift: int) -> int:
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def d_columns(mask: int) -> list[int]:
    columns = []
    for index in range(N):
        column = 0
        for shift in range(1, 11):
            bit = ((mask >> ((index + shift) % N)) ^ (mask >> ((index - shift) % N))) & 1
            column |= bit << (shift - 1)
        columns.append(column)
    return columns


def verify_direct_ranks() -> int:
    masks = set(range(1 << 15))
    value = 0x5141
    for _ in range(1 << 15):
        value = (1_103_515_245 * value + 12_345) & FULL
        masks.add(value)
    masks.update((0, FULL, 1, FULL ^ 1))
    for mask in masks:
        assert binary_rank(d_columns(mask)) == predicted_rank(mask)
    return len(masks)


def rank_counts() -> Counter[int]:
    counts = Counter(predicted_rank(mask) for mask in range(1 << N))
    expected = Counter(
        {
            0: 2,
            1: 6,
            3: 126,
            4: 378,
            6: 8190,
            7: 24570,
            9: 515970,
            10: 1547910,
        }
    )
    assert counts == expected

    product_counts: Counter[int] = Counter()
    for epsilon, epsilon_count in ((0, 1), (1, 3)):
        for delta, delta_count in ((0, 1), (3, 63)):
            for eta, eta_count in ((0, 1), (6, 4095)):
                product_counts[epsilon + delta + eta] += 2 * epsilon_count * delta_count * eta_count
    assert counts == product_counts
    return counts


def periodic_mask(pattern: int, period: int) -> int:
    return sum(((pattern >> (index % period)) & 1) << index for index in range(N))


def fixed_rank_counts(period: int) -> Counter[int]:
    return Counter(predicted_rank(periodic_mask(pattern, period)) for pattern in range(1 << period))


def orbit_rows(counts: Counter[int]) -> list[dict[str, str]]:
    fixed_1 = fixed_rank_counts(1)
    fixed_3 = fixed_rank_counts(3)
    fixed_7 = fixed_rank_counts(7)
    assert fixed_1 == Counter({0: 2})
    assert fixed_3 == Counter({1: 6, 0: 2})
    assert fixed_7 == Counter({3: 126, 0: 2})

    rows = []
    for rank in sorted(counts):
        numerator = counts[rank] + 12 * fixed_1[rank] + 6 * fixed_3[rank] + 2 * fixed_7[rank]
        assert numerator % N == 0
        rows.append(
            {
                "rank": str(rank),
                "word_count": str(counts[rank]),
                "fixed_period_1": str(fixed_1[rank]),
                "fixed_period_3": str(fixed_3[rank]),
                "fixed_period_7": str(fixed_7[rank]),
                "rotation_orbits": str(numerator // N),
            }
        )
    return rows


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    verify_factorization()
    f4_distribution = self_reciprocal_rank_distribution()
    f8_pair_distribution = reciprocal_pair_rank_distribution(F3A)
    f64_pair_distribution = reciprocal_pair_rank_distribution(F6A)
    direct_checks = verify_direct_ranks()
    counts = rank_counts()
    rows = orbit_rows(counts)
    root = Path(__file__).resolve().parent
    assert rows == read_tsv(root / "rank_orbit_table.tsv")

    print("factor_degrees=1,2,3,3,6,6")
    print("reciprocal_blocks=1,3,6")
    print(f"f4_local_distribution={dict(sorted(f4_distribution.items()))}")
    print(f"f8_pair_distribution={dict(sorted(f8_pair_distribution.items()))}")
    print(f"f64_pair_distribution={dict(sorted(f64_pair_distribution.items()))}")
    print(f"direct_rank_checks={direct_checks}")
    print("rank_spectrum=" + ",".join(map(str, sorted(counts))))
    print("rank_word_counts=" + ",".join(str(counts[rank]) for rank in sorted(counts)))
    print("rank_rotation_orbits=" + ",".join(row["rotation_orbits"] for row in rows))
    print("rank_orbit_table=verified")
    print("certificate=verified")


if __name__ == "__main__":
    main()
