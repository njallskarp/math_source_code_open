#!/usr/bin/env python3
"""Exact regression checker for the diagonal Euler-preperiod theorem.

The universal theorem is proved in DIAGONAL_PREPERIOD_THEOREM.md.  This
checker supplies finite definition-level evidence using only Python integers.

Usage: python3 verify_diagonal_preperiod.py [prime_bound]
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import sys


def euler_up_down(limit: int) -> list[int]:
    """Return A_0,...,A_limit using the Entringer triangle."""
    values = [1]
    previous = [1]
    for n in range(1, limit + 1):
        row = [0] * (n + 1)
        for k in range(1, n + 1):
            row[k] = row[k - 1] + previous[n - k]
        values.append(row[n])
        previous = row
    return values


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
    return [p for p in range(3, limit + 1, 2) if sieve[p]]


def valuation(value: int, prime: int) -> int:
    if value == 0:
        raise ValueError("valuation of zero is not used")
    result = 0
    while value % prime == 0:
        value //= prime
        result += 1
    return result


def criterion_class(p: int, values: list[int]) -> str:
    """Class from the first three rows of Guelec's exact criterion."""
    if values[p - 1] % p:
        return "p"
    if values[p - 2] % (p * p):
        return "p-1"
    if values[p - 3] % (p * p * p):
        return "p-2"
    return "<=p-3"


def theorem_class(p: int, values: list[int]) -> str:
    """Class from the endpoint/Wieferich formulation of the theorem."""
    if p % 4 == 3:
        return "p"
    if pow(2, p - 1, p**3) != 1:
        return "p-1"
    if values[p - 3] % (p**3):
        return "p-2"
    return "<=p-3"


def verify(bound: int) -> dict[str, object]:
    if bound < 3:
        raise ValueError("prime bound must be at least 3")
    values = euler_up_down(bound)
    primes = primes_up_to(bound)
    classes: Counter[str] = Counter()
    higher_wieferich: list[int] = []

    for p in primes:
        expected_endpoint = 0 if p % 4 == 1 else p - 2
        assert values[p - 1] % p == expected_endpoint

        tangent_v = valuation(values[p - 2], p)
        fermat_v = valuation(2 ** (p - 1) - 1, p) - 1
        assert tangent_v == fermat_v

        direct = criterion_class(p, values)
        translated = theorem_class(p, values)
        assert direct == translated
        classes[direct] += 1
        if pow(2, p - 1, p**3) == 1:
            higher_wieferich.append(p)

    record: dict[str, object] = {
        "prime_bound": bound,
        "prime_count": len(primes),
        "class_counts": dict(sorted(classes.items())),
        "higher_wieferich_primes": higher_wieferich,
        "endpoint_checks": len(primes),
        "valuation_checks": len(primes),
        "classification_checks": len(primes),
        "python": sys.version.split()[0],
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    record["record_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return record


def main() -> None:
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
    print(json.dumps(verify(bound), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
