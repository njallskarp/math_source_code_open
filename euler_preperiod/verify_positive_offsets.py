#!/usr/bin/env python3
"""Exact regression checker for the positive-offset preperiod theorem.

The universal proof is in POSITIVE_OFFSET_THEOREM.md.  This script uses only
Python integers and the definition-level Entringer recurrence.

Usage: python3 verify_positive_offsets.py [prime_bound]
"""

from __future__ import annotations

import hashlib
import json
import math
import sys


OFFSET_LIMIT = 13


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
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
    return [p for p in range(3, limit + 1, 2) if sieve[p]]


def factorization(value: int) -> list[list[int]]:
    """Return the exact trial-division factorization as [prime, exponent]."""
    if value < 1:
        raise ValueError("factorization expects a positive integer")
    factors: list[list[int]] = []
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            exponent = 0
            while remaining % divisor == 0:
                remaining //= divisor
                exponent += 1
            factors.append([divisor, exponent])
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append([remaining, 1])
    return factors


def secant_even_mod(limit: int, modulus: int) -> dict[int, int]:
    """Even A_n modulo modulus from (sec z)(cos z)=1.

    This is independent of the Entringer triangle used by ``euler_up_down``.
    """
    if limit < 0 or limit % 2:
        raise ValueError("limit must be a nonnegative even integer")
    if modulus < 2:
        raise ValueError("modulus must be at least 2")
    residues = {0: 1}
    for n in range(2, limit + 1, 2):
        residues[n] = (-sum(
            (-1) ** j * math.comb(n, 2 * j) * residues[n - 2 * j]
            for j in range(1, n // 2 + 1)
        )) % modulus
    return residues


def predicted_preperiod(p: int, t: int, values: list[int]) -> int:
    """The theorem's value for 1 <= t <= 13 and r=p+t."""
    if not 1 <= t <= OFFSET_LIMIT:
        raise ValueError("the finite classification covers 1 <= t <= 13")
    r = p + t
    return r if values[t] % p else r - 1


def top_two_criterion(p: int, r: int, values: list[int]) -> int | None:
    """Return r or r-1 from the first two rows, else None for a deeper case."""
    if values[r - 1] % p:
        return r
    if values[r - 2] % (p * p):
        return r - 1
    return None


def verify(bound: int) -> dict[str, object]:
    if bound < 3:
        raise ValueError("prime bound must be at least 3")
    values = euler_up_down(max(bound + OFFSET_LIMIT, 54))
    primes = primes_up_to(bound)

    small_values = values[: OFFSET_LIMIT + 1]
    consecutive_gcds = [
        math.gcd(small_values[t - 1], small_values[t])
        for t in range(1, OFFSET_LIMIT + 1)
    ]
    assert consecutive_gcds[:12] == [1] * 12
    assert consecutive_gcds[12] == 43

    exceptional_modulus = 43 * 43
    secant_residues = secant_even_mod(54, exceptional_modulus)
    assert values[54] % exceptional_modulus == 774
    assert secant_residues[54] == 774

    exceptional_pairs: list[list[int]] = []
    shift_checks = 0
    classification_checks = 0
    for p in primes:
        epsilon = 1 if p % 4 == 1 else -1
        for t in range(1, OFFSET_LIMIT + 1):
            r = p + t
            assert (values[r - 1] - epsilon * values[t]) % p == 0
            shift_checks += 1
            if t >= 2:
                assert (values[r - 2] - epsilon * values[t - 1]) % p == 0
                shift_checks += 1

            predicted = predicted_preperiod(p, t, values)
            direct = top_two_criterion(p, r, values)
            assert direct == predicted
            classification_checks += 1
            if predicted == r - 1:
                exceptional_pairs.append([p, t])

    record: dict[str, object] = {
        "prime_bound": bound,
        "prime_count": len(primes),
        "offset_limit": OFFSET_LIMIT,
        "classification_checks": classification_checks,
        "shift_congruence_checks": shift_checks,
        "exceptional_pairs_within_bound": exceptional_pairs,
        "small_values": small_values,
        "small_factorizations": {
            str(t): factorization(small_values[t])
            for t in range(1, OFFSET_LIMIT + 1)
        },
        "consecutive_gcds_t_1_through_13": consecutive_gcds,
        "exceptional_p2_lift": {
            "prime": 43,
            "offset": 13,
            "index": 54,
            "modulus": exceptional_modulus,
            "residue": 774,
            "quotient_mod_prime": 18,
            "independent_recurrences": ["Entringer", "secant-times-cosine"],
        },
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
