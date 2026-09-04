#!/usr/bin/env python3
"""Independent exact audit for the sub-double-prime Gram-descent review.

This deliberately differs from the target checker in two ways:

* profile totals are obtained from closed binomial formulas rather than by
  enumerating ordered compositions;
* small spectral pairs are tested with SymPy's cyclotomic polynomials rather
  than the target's hand-written polynomial arithmetic.

The finite checks are falsification evidence for the proof, not a replacement
for its universal cuboid and Gram-rank argument.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import comb, gcd
import sys

import sympy
from sympy import Matrix, Poly, ZZ, cyclotomic_poly, symbols


X = symbols("X")


def divisors(n: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, n + 1) if n % d == 0)


@lru_cache(maxsize=None)
def cyclotomic(d: int) -> Poly:
    return Poly(cyclotomic_poly(d, X), X, domain=ZZ)


@lru_cache(maxsize=None)
def zero_orders(subset: tuple[int, ...], modulus: int) -> frozenset[int]:
    mask = Poly(sum(X**a for a in subset), X, domain=ZZ)
    return frozenset(
        d
        for d in divisors(modulus)
        if d > 1 and mask.rem(cyclotomic(d)).is_zero
    )


@lru_cache(maxsize=None)
def difference_orders(subset: tuple[int, ...], modulus: int) -> frozenset[int]:
    return frozenset(
        modulus // gcd(modulus, (a - b) % modulus)
        for a, b in combinations(subset, 2)
    )


def normalized_subsets(modulus: int, size: int) -> tuple[tuple[int, ...], ...]:
    if size > modulus:
        return ()
    return tuple((0, *tail) for tail in combinations(range(1, modulus), size - 1))


def projected(subset: tuple[int, ...], modulus: int) -> tuple[int, ...]:
    return tuple(sorted(a % modulus for a in subset))


def count_spectral_pairs(n: int, p: int, size: int) -> tuple[int, int]:
    modulus = n * p
    subsets = normalized_subsets(modulus, size)
    zeros = {a: zero_orders(a, modulus) for a in subsets}
    differences = {a: difference_orders(a, modulus) for a in subsets}
    pair_count = 0

    for a_set in subsets:
        for lambda_set in subsets:
            if not differences[lambda_set] <= zeros[a_set]:
                continue
            pair_count += 1

            # The reviewed theorem says both projections are injective and
            # spectral.  Check both orientations, not just one.
            a_projection = projected(a_set, n)
            lambda_projection = projected(lambda_set, n)
            assert len(set(a_projection)) == size
            assert len(set(lambda_projection)) == size
            assert difference_orders(lambda_projection, n) <= zero_orders(
                a_projection, n
            )
            assert difference_orders(a_projection, n) <= zero_orders(
                lambda_projection, n
            )

    return len(subsets), pair_count


def main() -> None:
    print(
        f"python={sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} "
        f"sympy={sympy.__version__}"
    )
    rows: list[str] = []

    target_primes = (3, 5, 7, 11)
    theorem_profiles = sum(
        comb(k - 1, p - 1)
        for p in target_primes
        for k in range(p + 1, 2 * p - 1)
    )
    boundary_profiles = sum(comb(2 * p - 2, p - 1) for p in target_primes)
    exceptional_boundary_profiles = sum(target_primes)
    assert theorem_profiles == 168_808
    assert boundary_profiles == 185_756
    row = (
        "closed_form_profiles "
        f"subdouble={theorem_profiles} boundary={boundary_profiles} "
        f"exceptional_ordered={exceptional_boundary_profiles} status=verified"
    )
    print(row)
    rows.append(row)

    gram_primes = (3, 5, 7, 11, 13)
    gram_cases = 0
    for p in gram_primes:
        for r in range(2, p):
            matrix = Matrix(p, p, lambda i, j: r if i == j else 1)
            determinant = matrix.det(method="domain-ge")
            assert determinant == (r - 1) ** (p - 1) * (
                r + p - 1
            )
            assert determinant != 0  # Hence the exact rank is p.
            gram_cases += 1
    row = (
        f"sympy_gram primes={','.join(map(str, gram_primes))} "
        f"cases={gram_cases} exact_rank_and_determinant=verified"
    )
    print(row)
    rows.append(row)

    total_pairs = 0
    for n in (2, 4, 5, 7):
        subset_count, pair_count = count_spectral_pairs(n=n, p=3, size=4)
        total_pairs += pair_count
        row = (
            f"exact_spectral_search p=3 n={n} normalized_sets={subset_count} "
            f"spectral_pairs={pair_count} all_pairs_project=verified"
        )
        print(row)
        rows.append(row)
    assert total_pairs == 57

    possible = tuple(k for k in range(12, 21) if 2310 % k == 0)
    impossible = tuple(k for k in range(12, 21) if 2310 % k != 0)
    assert possible == (14, 15)
    assert impossible == (12, 13, 16, 17, 18, 19, 20)
    row = (
        "z2310_interval possible=14,15 "
        "impossible=12,13,16,17,18,19,20 status=verified"
    )
    print(row)
    rows.append(row)

    digest = sha256("\n".join(rows).encode()).hexdigest()
    print(f"review_audit_sha256={digest}")


if __name__ == "__main__":
    main()
