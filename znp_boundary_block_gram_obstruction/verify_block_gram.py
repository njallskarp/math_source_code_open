#!/usr/bin/env python3
"""Exact audit of the simultaneous one-fat-level block-Gram obstruction."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import gcd


def block_gram(p: int, r: int) -> list[list[int]]:
    """The forced Gram matrix, large block first."""
    q = p - 1
    size = r + q
    matrix = [[1] * size for _ in range(size)]
    for i in range(size):
        matrix[i][i] = r
    for i in range(r):
        for j in range(r):
            if i != j:
                matrix[i][j] = -q
    return matrix


def quadratic(matrix: list[list[int]], vector: list[int]) -> int:
    return sum(
        vector[i] * matrix[i][j] * vector[j]
        for i in range(len(vector))
        for j in range(len(vector))
    )


def divisors(n: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, n + 1) if n % d == 0)


def poly_div_monic(
    numerator: list[int], denominator: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    out = numerator[:]
    quotient = [0] * max(1, len(out) - len(denominator) + 1)
    while len(out) >= len(denominator):
        coefficient = out[-1]
        shift = len(out) - len(denominator)
        quotient[shift] = coefficient
        for i, value in enumerate(denominator):
            out[shift + i] -= coefficient * value
        while out and out[-1] == 0:
            out.pop()
    return tuple(quotient), tuple(out)


@lru_cache(maxsize=None)
def cyclotomic(n: int) -> tuple[int, ...]:
    polynomial = [-1] + [0] * (n - 1) + [1]
    for d in divisors(n):
        if d == n:
            continue
        quotient, remainder = poly_div_monic(polynomial, cyclotomic(d))
        assert not remainder
        polynomial = list(quotient)
    return tuple(polynomial)


def zero_orders(subset: tuple[int, ...], modulus: int) -> frozenset[int]:
    mask = [0] * modulus
    for value in subset:
        mask[value] = 1
    zeros = set()
    for d in divisors(modulus):
        if d == 1:
            continue
        _, remainder = poly_div_monic(mask, cyclotomic(d))
        if not remainder:
            zeros.add(d)
    return frozenset(zeros)


def difference_orders(subset: tuple[int, ...], modulus: int) -> frozenset[int]:
    return frozenset(
        modulus // gcd(modulus, (a - b) % modulus)
        for a, b in combinations(subset, 2)
    )


def level_profile(subset: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple(sorted(Counter(value % p for value in subset).values(), reverse=True))


def audit_block_matrices() -> int:
    cases = 0
    for p in (3, 5, 7, 11):
        for r in range(2, 2 * p - 1):
            k = r + p - 1
            matrix = block_gram(p, r)
            assert len(matrix) == k
            assert all(matrix[i][i] == r for i in range(k))

            # Integer version of the negative constant-block direction.
            witness = [k - 1] * r + [-r] * (p - 1)
            expected = -r * (k - 1) * (r - 1) * (p - 2) * k
            assert quadratic(matrix, witness) == expected
            assert expected < 0

            compression_det = -((r - 1) * (p - 2) * k)
            direct_det = (p - 1 - r * (p - 2)) * (r + p - 2) - r * (p - 1)
            assert direct_det == compression_det
            cases += 1
    return cases


def audit_small_boundary() -> tuple[int, int, int, int]:
    p = 3
    k = 2 * p - 1
    normalized_sets = 0
    spectral_pairs = 0
    one_sided_exceptional = 0
    both_exceptional = 0

    for n in (2, 4, 5):
        modulus = n * p
        subsets = [
            (0,) + tail
            for tail in combinations(range(1, modulus), k - 1)
        ]
        normalized_sets += len(subsets)
        zeros = {subset: zero_orders(subset, modulus) for subset in subsets}
        differences = {
            subset: difference_orders(subset, modulus) for subset in subsets
        }
        exceptional = (p, 1, 1)
        for a_set in subsets:
            for lambda_set in subsets:
                if not differences[lambda_set] <= zeros[a_set]:
                    continue
                # Orthogonal square Fourier matrices are symmetric; audit the
                # reverse zero condition directly rather than importing it.
                assert differences[a_set] <= zeros[lambda_set]
                spectral_pairs += 1
                a_exceptional = level_profile(a_set, p) == exceptional
                l_exceptional = level_profile(lambda_set, p) == exceptional
                if a_exceptional ^ l_exceptional:
                    one_sided_exceptional += 1
                if a_exceptional and l_exceptional:
                    both_exceptional += 1
    return (
        normalized_sets,
        spectral_pairs,
        one_sided_exceptional,
        both_exceptional,
    )


def main() -> None:
    rows: list[str] = []

    cases = audit_block_matrices()
    row = (
        f"block_gram_cases={cases} p=3,5,7,11 "
        "r=2..2p-2 exact_negative_witness=verified"
    )
    print(row)
    rows.append(row)

    normalized, pairs, one_sided, both = audit_small_boundary()
    row = (
        "boundary_pair_search_p=3_n=2,4,5 "
        f"normalized_sets={normalized} spectral_pairs={pairs} "
        f"one_sided_exceptional={one_sided} both_exceptional={both}"
    )
    print(row)
    rows.append(row)
    assert pairs == 161
    assert one_sided == 40
    assert both == 0

    possible = [k for k in range(12, 22) if 2310 % k == 0]
    impossible = [k for k in range(12, 22) if 2310 % k != 0]
    assert possible == [14, 15, 21]
    assert impossible == [12, 13, 16, 17, 18, 19, 20]
    row = (
        f"z2310_sizes_12_to_21 possible={','.join(map(str, possible))} "
        f"impossible={','.join(map(str, impossible))} status=classified"
    )
    print(row)
    rows.append(row)

    digest = sha256("\n".join(rows).encode()).hexdigest()
    print(f"audit_sha256={digest}")


if __name__ == "__main__":
    main()
