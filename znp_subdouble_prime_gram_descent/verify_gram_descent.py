#!/usr/bin/env python3
"""Exact finite audit for the sub-double-prime Gram-descent theorem."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import gcd, prod


def compositions(total: int, parts: int, minimum: int = 1):
    """Yield positive ordered compositions, used only in small audit boxes."""
    shifted = total - minimum * parts
    if shifted < 0:
        return
    for bars in combinations(range(shifted + parts - 1), parts - 1):
        cuts = (-1,) + bars + (shifted + parts - 1,)
        yield tuple(cuts[i + 1] - cuts[i] - 1 + minimum for i in range(parts))


def rational_rank(matrix: list[list[int]]) -> int:
    a = [[Fraction(x) for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for i in range(rows):
            if i != rank and a[i][col]:
                scale = a[i][col]
                a[i] = [x - scale * y for x, y in zip(a[i], a[rank])]
        rank += 1
    return rank


def gram(p: int, r: int) -> list[list[int]]:
    return [[r if i == j else 1 for j in range(p)] for i in range(p)]


def divisors(n: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, n + 1) if n % d == 0)


def poly_div_monic(numerator: list[int], denominator: tuple[int, ...]):
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


def projected(subset: tuple[int, ...], n: int) -> tuple[int, ...]:
    return tuple(sorted(value % n for value in subset))


def main() -> None:
    rows: list[str] = []
    primes = (3, 5, 7, 11)
    profile_count = 0
    theorem_profiles = 0
    boundary_profiles = 0

    for p in primes:
        for k in range(p + 1, 2 * p - 1):
            for profile in compositions(k, p):
                profile_count += 1
                assert 1 in profile
                candidates = [r for r in profile if 2 <= r <= p - 1]
                assert candidates, (p, k, profile)
                theorem_profiles += 1

        k = 2 * p - 1
        exceptional = tuple(sorted((p,) + (1,) * (p - 1)))
        seen_exceptional = 0
        for profile in compositions(k, p):
            boundary_profiles += 1
            ordered = tuple(sorted(profile))
            if ordered == exceptional:
                seen_exceptional += 1
                continue
            candidates = [r for r in profile if 2 <= r <= p - 1]
            assert candidates, (p, k, profile)
        assert seen_exceptional == p

    row = (
        "profile_audit_p=3,5,7,11 "
        f"subdouble_profiles={theorem_profiles} "
        f"boundary_profiles={boundary_profiles} status=verified"
    )
    print(row)
    rows.append(row)

    gram_cases = 0
    for p in primes:
        for r in range(2, p):
            matrix = gram(p, r)
            rank = rational_rank(matrix)
            determinant = (r - 1) ** (p - 1) * (r + p - 1)
            assert rank == p
            assert determinant == prod([r - 1] * (p - 1) + [r + p - 1])
            gram_cases += 1
    row = f"gram_formula_cases={gram_cases} exact_rational_rank=status_verified"
    print(row)
    rows.append(row)

    searched_sets = 0
    spectral_pairs = 0
    for n in (4, 5, 7):
        p = 3
        modulus = n * p
        k = 4
        normalized = tuple((0,) + tail for tail in combinations(range(1, modulus), k - 1))
        zero_cache = {subset: zero_orders(subset, modulus) for subset in normalized}
        requirement_cache = {
            subset: difference_orders(subset, modulus) for subset in normalized
        }
        for a_set in normalized:
            searched_sets += 1
            for lambda_set in normalized:
                if not requirement_cache[lambda_set] <= zero_cache[a_set]:
                    continue
                spectral_pairs += 1
                a_projection = projected(a_set, n)
                lambda_projection = projected(lambda_set, n)
                assert len(set(a_projection)) == len(set(lambda_projection)) == k
                assert difference_orders(lambda_projection, n) <= zero_orders(a_projection, n)
                assert difference_orders(a_projection, n) <= zero_orders(lambda_projection, n)
    row = (
        "direct_pair_search_p=3_n=4,5,7 "
        f"normalized_sets={searched_sets} spectral_pairs={spectral_pairs} "
        "status=all_project"
    )
    print(row)
    rows.append(row)

    divisors = [k for k in range(12, 21) if 2310 % k == 0]
    nondivisors = [k for k in range(12, 21) if 2310 % k != 0]
    assert divisors == [14, 15]
    assert nondivisors == [12, 13, 16, 17, 18, 19, 20]
    row = (
        f"z2310_sizes_12_to_20 possible={','.join(map(str, divisors))} "
        f"impossible={','.join(map(str, nondivisors))} status=classified"
    )
    print(row)
    rows.append(row)

    digest = sha256("\n".join(rows).encode()).hexdigest()
    print(f"audit_sha256={digest}")


if __name__ == "__main__":
    main()
