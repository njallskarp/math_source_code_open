"""Exact checks for the Collatz symbolic affine-prefix functional.

All comparisons use integers or fractions.Fraction.  No floating-point
arithmetic is used in a mathematical decision.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Iterator, Sequence
from fractions import Fraction
from itertools import combinations

Word = tuple[int, ...]


def words_with_weight(length: int, weight: int) -> Iterator[Word]:
    """Generate all binary words of a fixed length and Hamming weight."""
    for positions in combinations(range(length), weight):
        word = [0] * length
        for position in positions:
            word[position] = 1
        yield tuple(word)


def rotations(word: Word) -> Iterator[Word]:
    """Generate all indexed rotations, retaining repetitions for periodic words."""
    for shift in range(len(word)):
        yield word[shift:] + word[:shift]


def affine_offset(word: Sequence[int]) -> int:
    """Return B in 2^k T^k(n) = 3^q n + B for this parity word."""
    offset = 0
    odd_count = 0
    for index, bit in enumerate(word):
        if bit not in (0, 1):
            raise ValueError("a parity word must contain only 0 and 1")
        offset = (3 if bit else 1) * offset + bit * 2**index
        odd_count += bit
    return offset


def prefix_cap(word: Sequence[int]) -> Fraction:
    """Largest start allowed by all contracting prefixes of ``word``.

    The full word is required to be contracting, so the returned minimum is
    always defined.
    """
    offset = 0
    odd_count = 0
    cap: Fraction | None = None
    for length, bit in enumerate(word, start=1):
        if bit not in (0, 1):
            raise ValueError("a parity word must contain only 0 and 1")
        offset = (3 if bit else 1) * offset + bit * 2 ** (length - 1)
        odd_count += bit
        denominator = 2**length - 3**odd_count
        if denominator > 0:
            candidate = Fraction(offset, denominator)
            cap = candidate if cap is None else min(cap, candidate)
    if cap is None:
        raise ValueError("the word has no contracting prefix")
    return cap


def upper_christoffel_word(length: int, weight: int) -> Word:
    """Return the upper mechanical word with slope ``weight / length``."""
    if not 0 <= weight <= length or length <= 0:
        raise ValueError("require 0 <= weight <= length and positive length")

    def ceil_div(numerator: int, denominator: int) -> int:
        return (numerator + denominator - 1) // denominator

    return tuple(
        ceil_div(index * weight, length)
        - ceil_div((index - 1) * weight, length)
        for index in range(1, length + 1)
    )


def check_rotation_bridge(word: Word) -> None:
    """Check max rotation cap = min rotation offset / (2^k - 3^q)."""
    denominator = 2 ** len(word) - 3 ** sum(word)
    if denominator <= 0:
        raise ValueError("rotation bridge requires a contracting full word")
    indexed_rotations = tuple(rotations(word))
    left = max(prefix_cap(rotation) for rotation in indexed_rotations)
    right = Fraction(
        min(affine_offset(rotation) for rotation in indexed_rotations),
        denominator,
    )
    if left != right:
        raise AssertionError((word, left, right))


def verify(max_length: int, rotation_check_length: int) -> dict[str, int]:
    """Run the exhaustive fixed-length/fixed-weight checks."""
    parameter_pairs = 0
    words_checked = 0
    rotation_words_checked = 0
    for length in range(1, max_length + 1):
        for weight in range(length + 1):
            if 3**weight >= 2**length:
                continue
            parameter_pairs += 1
            candidates = tuple(words_with_weight(length, weight))
            words_checked += len(candidates)
            best_cap = max(prefix_cap(word) for word in candidates)
            maximizers = tuple(
                word for word in candidates if prefix_cap(word) == best_cap
            )
            expected = upper_christoffel_word(length, weight)
            if maximizers != (expected,):
                raise AssertionError(
                    (length, weight, expected, maximizers, best_cap)
                )
            if length <= rotation_check_length:
                for word in candidates:
                    check_rotation_bridge(word)
                    rotation_words_checked += 1
    return {
        "max_length": max_length,
        "rotation_check_length": min(max_length, rotation_check_length),
        "parameter_pairs": parameter_pairs,
        "words_checked": words_checked,
        "rotation_words_checked": rotation_words_checked,
    }


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=16)
    parser.add_argument("--rotation-check-length", type=int, default=12)
    args = parser.parse_args(argv)
    if args.max_length < 1:
        parser.error("--max-length must be positive")
    if args.rotation_check_length < 0:
        parser.error("--rotation-check-length must be nonnegative")
    return args


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)
    report = verify(args.max_length, args.rotation_check_length)
    for key, value in report.items():
        print(f"{key}={value}")
    print("status=all exact checks passed")


if __name__ == "__main__":
    main()
