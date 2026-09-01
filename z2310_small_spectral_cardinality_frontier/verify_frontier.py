#!/usr/bin/env python3
"""Exact arithmetic audit for the Z/2310Z small-cardinality frontier."""

from __future__ import annotations

import math
import sys


N = 2310
P = 11
BASE = 210


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def prime_factors(n: int) -> list[int]:
    factors: list[int] = []
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            factors.append(candidate)
            while n % candidate == 0:
                n //= candidate
        candidate += 1
    if n > 1:
        factors.append(n)
    return factors


def main() -> None:
    assert N == BASE * P
    assert math.gcd(BASE, P) == 1
    assert prime_factors(N) == [2, 3, 5, 7, 11]
    assert math.prod(prime_factors(N)) == N

    base_divisors = divisors(BASE)
    assert len(base_divisors) == 16
    descent_pairs = [(P * d, d) for d in base_divisors]
    assert descent_pairs[-1] == (N, BASE)

    possible = [d for d in divisors(N) if d < P]
    positive_sizes = list(range(1, P))
    impossible = [k for k in positive_sizes if k not in possible]
    assert possible == [1, 2, 3, 5, 6, 7, 10]
    assert impossible == [4, 8, 9]

    print(f"N={N} base={BASE} descent_prime={P}")
    print("prime_factors=" + ",".join(map(str, prime_factors(N))))
    print("base_divisors=" + ",".join(map(str, base_divisors)))
    print(
        "descent_pairs="
        + ",".join(f"{source}->{target}" for source, target in descent_pairs)
    )
    print("possible_sizes_below_11=" + ",".join(map(str, possible)))
    print("impossible_sizes_below_11=" + ",".join(map(str, impossible)))
    print("status=all_exact_arithmetic_checks_passed")


if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        print("status=assertion_failed", file=sys.stderr)
        raise
