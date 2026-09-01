"""Exact symbolic counting for coefficient-noncontracting Collatz prefixes.

For a binary parity word e_0...e_{j-1}, put q_i=sum(e_0,...,e_{i-1}).
The word is coefficient-noncontracting when 3**q_i >= 2**i at every
prefix length i.  The dynamic program below counts these words by (i, q_i)
without enumerating the underlying 2-adic residue cylinders.

All mathematical decisions use exact integers.  No floating-point arithmetic
is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Iterable, Iterator, Sequence
from itertools import product
from math import comb, gcd

Word = tuple[int, ...]
Distribution = dict[int, int]


def coefficient_safe(word: Sequence[int]) -> bool:
    """Return whether every prefix has multiplier 3**q / 2**j at least one."""
    odd_count = 0
    for length, bit in enumerate(word, start=1):
        if bit not in (0, 1):
            raise ValueError("a parity word must contain only 0 and 1")
        odd_count += bit
        if 3**odd_count < 2**length:
            return False
    return True


def affine_offset(word: Sequence[int]) -> int:
    """Return B in 2**k T**k(n) = 3**q n + B for a parity word."""
    offset = 0
    for index, bit in enumerate(word):
        if bit not in (0, 1):
            raise ValueError("a parity word must contain only 0 and 1")
        offset = (3 if bit else 1) * offset + bit * 2**index
    return offset


def cylinder_residue(word: Sequence[int]) -> int:
    """Return the least start residue modulo 2**len(word) for ``word``."""
    modulus = 2 ** len(word)
    if modulus == 1:
        return 0
    odd_count = sum(word)
    return (-affine_offset(word) * pow(3**odd_count, -1, modulus)) % modulus


def extend_frontier(frontier: Distribution, length: int) -> tuple[Distribution, int]:
    """Extend a safe length-(length-1) distribution by one parity bit.

    Return the new safe distribution and the number of words whose first
    coefficient contraction occurs at this extension.
    """
    if length < 1:
        raise ValueError("length must be positive")
    next_frontier: Distribution = {}
    first_crossings = 0
    threshold = 2**length
    for odd_count, count in frontier.items():
        for bit in (0, 1):
            next_odd_count = odd_count + bit
            if 3**next_odd_count >= threshold:
                next_frontier[next_odd_count] = (
                    next_frontier.get(next_odd_count, 0) + count
                )
            else:
                first_crossings += count
    return next_frontier, first_crossings


def frontier_rows(max_depth: int) -> Iterator[tuple[int, Distribution, int]]:
    """Yield (depth, distribution, first-crossing count) through max_depth."""
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    frontier: Distribution = {0: 1}
    yield 0, frontier, 0
    for depth in range(1, max_depth + 1):
        frontier, first_crossings = extend_frontier(frontier, depth)
        yield depth, frontier, first_crossings


def canonical_distribution(frontier: Distribution) -> bytes:
    """Return canonical UTF-8 JSON bytes for an ordered q-count distribution."""
    payload = [[odd_count, frontier[odd_count]] for odd_count in sorted(frontier)]
    return json.dumps(payload, separators=(",", ":")).encode("ascii")


def divisors(value: int) -> Iterator[int]:
    """Yield the positive divisors of ``value`` in increasing order."""
    if value < 1:
        raise ValueError("value must be positive")
    small: list[int] = []
    large: list[int] = []
    candidate = 1
    while candidate * candidate <= value:
        if value % candidate == 0:
            small.append(candidate)
            if candidate * candidate != value:
                large.append(value // candidate)
        candidate += 1
    yield from small
    yield from reversed(large)


def euler_phi(value: int) -> int:
    """Return Euler's totient using exact trial division."""
    if value < 1:
        raise ValueError("value must be positive")
    result = value
    remaining = value
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            result -= result // prime
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result -= result // remaining
    return result


def binary_necklaces(length: int, weight: int) -> int:
    """Count fixed-length, fixed-weight binary necklaces by Burnside's lemma."""
    if length < 0 or not 0 <= weight <= length:
        raise ValueError("require length >= 0 and 0 <= weight <= length")
    if length == 0:
        return 1
    numerator = sum(
        euler_phi(divisor) * comb(length // divisor, weight // divisor)
        for divisor in divisors(gcd(length, weight))
    )
    quotient, remainder = divmod(numerator, length)
    if remainder:
        raise AssertionError((length, weight, numerator, remainder))
    return quotient


def brute_force_distribution(depth: int) -> Distribution:
    """Enumerate all words at a small depth as an independent local oracle."""
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    result: Distribution = {}
    for word in product((0, 1), repeat=depth):
        if coefficient_safe(word):
            odd_count = sum(word)
            result[odd_count] = result.get(odd_count, 0) + 1
    return result


def verify_small(max_depth: int) -> dict[str, int]:
    """Cross-check the DP, brute force, and parity-word/residue injectivity."""
    words_checked = 0
    for depth, frontier, _ in frontier_rows(max_depth):
        brute = brute_force_distribution(depth)
        if frontier != brute:
            raise AssertionError((depth, frontier, brute))
        residues: set[int] = set()
        safe_words = 0
        for word in product((0, 1), repeat=depth):
            words_checked += 1
            residue = cylinder_residue(word)
            if residue in residues:
                raise AssertionError((depth, word, residue))
            residues.add(residue)
            safe_words += int(coefficient_safe(word))
        if len(residues) != 2**depth or safe_words != sum(frontier.values()):
            raise AssertionError((depth, len(residues), safe_words, frontier))
    return {"brute_force_max_depth": max_depth, "words_checked": words_checked}


def certificate(depth: int) -> dict[str, int | str]:
    """Compute the exact summary certificate at ``depth``."""
    final_frontier: Distribution | None = None
    crossings_at_depth = 0
    cumulative_first_crossings = 0
    for row_depth, frontier, first_crossings in frontier_rows(depth):
        if row_depth:
            cumulative_first_crossings += first_crossings
        final_frontier = frontier
        crossings_at_depth = first_crossings
    assert final_frontier is not None
    encoded = canonical_distribution(final_frontier)
    keys = sorted(final_frontier)
    rational_ballot_weight = 0
    while 3**rational_ballot_weight < 2**depth:
        rational_ballot_weight += 1
    ballot_numerator = comb(depth, rational_ballot_weight)
    rational_ballot_lower_bound = (
        1 if depth == 0 else (ballot_numerator + depth - 1) // depth
    )
    necklace_lower_bound = binary_necklaces(depth, rational_ballot_weight)
    return {
        "depth": depth,
        "safe_words": sum(final_frontier.values()),
        "safe_words_decimal_digits": len(str(sum(final_frontier.values()))),
        "active_q_states": len(final_frontier),
        "minimum_q": keys[0] if keys else -1,
        "maximum_q": keys[-1] if keys else -1,
        "first_crossings_at_depth": crossings_at_depth,
        "cumulative_first_crossings": cumulative_first_crossings,
        "rational_ballot_weight": rational_ballot_weight,
        "rational_ballot_lower_bound": rational_ballot_lower_bound,
        "necklace_lower_bound": necklace_lower_bound,
        "necklace_improvement": necklace_lower_bound - rational_ballot_lower_bound,
        "distribution_sha256": hashlib.sha256(encoded).hexdigest(),
    }


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=300)
    parser.add_argument("--brute-force-depth", type=int, default=14)
    args = parser.parse_args(argv)
    if args.depth < 0:
        parser.error("--depth must be nonnegative")
    if not 0 <= args.brute_force_depth <= 20:
        parser.error("--brute-force-depth must lie between 0 and 20")
    return args


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)
    small_report = verify_small(args.brute_force_depth)
    report = certificate(args.depth)
    for key, value in small_report.items():
        print(f"{key}={value}")
    for key, value in report.items():
        print(f"{key}={value}")
    print("status=all exact checks passed")


if __name__ == "__main__":
    main()
