"""Exact verification of Collatz parity-cylinder transport and a finite screen."""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Iterator, Sequence
from fractions import Fraction
from itertools import product

Word = tuple[int, ...]


def affine_offset(word: Sequence[int]) -> int:
    """Return B in 2^k T^k(n) = 3^q n + B."""
    offset = 0
    for index, bit in enumerate(word):
        if bit not in (0, 1):
            raise ValueError("parity words contain only 0 and 1")
        offset = (3 if bit else 1) * offset + bit * 2**index
    return offset


def simulate(start: int, word: Sequence[int]) -> int:
    """Apply a parity word, rejecting it if a requested parity is not realized."""
    value = start
    for bit in word:
        if value % 2 != bit:
            raise ValueError((start, tuple(word), value, bit))
        value = value // 2 if bit == 0 else (3 * value + 1) // 2
    return value


def cylinder_base(word: Word) -> tuple[int, int]:
    """Return the least nonnegative start and its endpoint for ``word``."""
    length = len(word)
    modulus = 2**length
    odd_multiplier = 3 ** sum(word)
    offset = affine_offset(word)
    residue = (-offset * pow(odd_multiplier, -1, modulus)) % modulus
    numerator = odd_multiplier * residue + offset
    if numerator % modulus:
        raise AssertionError("modular inverse failed to clear the denominator")
    endpoint = numerator // modulus
    if simulate(residue, word) != endpoint:
        raise AssertionError("computed cylinder base does not realize the word")
    return residue, endpoint


def lifted_pair(word: Word, lift: int) -> tuple[int, int]:
    """Return the transported start and endpoint in one parity cylinder."""
    if lift < 0:
        raise ValueError("lift must be nonnegative")
    residue, endpoint = cylinder_base(word)
    start = residue + 2 ** len(word) * lift
    end = endpoint + 3 ** sum(word) * lift
    if simulate(start, word) != end:
        raise AssertionError("cylinder transport identity failed")
    return start, end


def prefix_cap(word: Sequence[int]) -> Fraction:
    """Minimum affine threshold over the contracting prefixes of ``word``."""
    offset = 0
    odd_count = 0
    cap: Fraction | None = None
    for length, bit in enumerate(word, start=1):
        offset = (3 if bit else 1) * offset + bit * 2 ** (length - 1)
        odd_count += bit
        denominator = 2**length - 3**odd_count
        if denominator > 0:
            candidate = Fraction(offset, denominator)
            cap = candidate if cap is None else min(cap, candidate)
    if cap is None:
        raise ValueError("word has no contracting prefix")
    return cap


def upper_christoffel_word(length: int, weight: int) -> Word:
    """Return the upper mechanical word of slope ``weight / length``."""
    return tuple(
        (index * weight + length - 1) // length
        - ((index - 1) * weight + length - 1) // length
        for index in range(1, length + 1)
    )


def binary_words(max_length: int) -> Iterator[Word]:
    for length in range(1, max_length + 1):
        yield from product((0, 1), repeat=length)


def verify_transport(max_word_length: int, max_lift: int) -> dict[str, int]:
    """Exhaustively check base realization, transport, and the lift inequality."""
    words_checked = 0
    lifts_checked = 0
    contracting_bases_checked = 0
    for word in binary_words(max_word_length):
        words_checked += 1
        residue, endpoint = cylinder_base(word)
        for lift in range(max_lift + 1):
            start, end = lifted_pair(word, lift)
            lifts_checked += 1
            if start != residue + 2 ** len(word) * lift:
                raise AssertionError("start transport mismatch")
            if end != endpoint + 3 ** sum(word) * lift:
                raise AssertionError("endpoint transport mismatch")
        denominator = 2 ** len(word) - 3 ** sum(word)
        if denominator > 0 and residue <= endpoint:
            contracting_bases_checked += 1
            for lift in range(max_lift + 1):
                start, end = lifted_pair(word, lift)
                expected = denominator * lift <= endpoint - residue
                if (start <= end) != expected:
                    raise AssertionError((word, lift, start, end, expected))
    return {
        "transport_max_word_length": max_word_length,
        "transport_max_lift": max_lift,
        "transport_words_checked": words_checked,
        "transport_lifts_checked": lifts_checked,
        "contracting_bases_checked": contracting_bases_checked,
    }


def verify_christoffel_gap(max_length: int) -> dict[str, int]:
    """Screen high-density contracting Christoffel words for positive lifts.

    For the canonical Christoffel orientation, the prefix cap equals C/D.  The
    screen checks that the least positive cylinder representative exceeds this
    cap, and hence every nonnegative lift descends over the full word.
    """
    pairs_checked = 0
    for length in range(2, max_length + 1):
        for weight in range(length // 2 + 1, length + 1):
            if 3**weight >= 2**length:
                continue
            pairs_checked += 1
            word = upper_christoffel_word(length, weight)
            numerator = affine_offset(word)
            denominator = 2**length - 3**weight
            cap = Fraction(numerator, denominator)
            if prefix_cap(word) != cap:
                raise AssertionError("canonical prefix cap is not the cycle value")
            residue, endpoint = cylinder_base(word)
            if residue == 0:
                residue = 2**length
            if residue * denominator <= numerator:
                raise AssertionError(
                    ("Christoffel realizability-gap counterexample", length,
                     weight, residue, endpoint, cap)
                )
    return {
        "christoffel_max_length": max_length,
        "christoffel_high_density_pairs_checked": pairs_checked,
        "christoffel_gap_counterexamples": 0,
    }


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport-max-word-length", type=int, default=12)
    parser.add_argument("--transport-max-lift", type=int, default=5)
    parser.add_argument("--christoffel-max-length", type=int, default=500)
    args = parser.parse_args(argv)
    if args.transport_max_word_length < 1:
        parser.error("--transport-max-word-length must be positive")
    if args.transport_max_lift < 0:
        parser.error("--transport-max-lift must be nonnegative")
    if args.christoffel_max_length < 2:
        parser.error("--christoffel-max-length must be at least 2")
    return args


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)
    reports = (
        verify_transport(args.transport_max_word_length, args.transport_max_lift),
        verify_christoffel_gap(args.christoffel_max_length),
    )
    for report in reports:
        for key, value in report.items():
            print(f"{key}={value}")
    print("status=all exact checks passed")


if __name__ == "__main__":
    main()
