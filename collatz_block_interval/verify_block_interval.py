"""Exact block composition and all-prefix lift intervals for shortcut Collatz.

Every finite parity word determines one residue cylinder modulo 2**K.  This
module computes the exact interval of nonnegative lift parameters whose starts
remain no larger than every iterate inside the word, and verifies a direct
composition rule for concatenated blocks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from itertools import product

Word = tuple[int, ...]


@dataclass(frozen=True)
class LiftInterval:
    lower: int
    upper: int | None

    def contains(self, value: int) -> bool:
        return self.lower <= value and (self.upper is None or value <= self.upper)


@dataclass(frozen=True)
class Cylinder:
    length: int
    odd_count: int
    residue: int
    endpoint: int
    offset: int


def shortcut_step(value: int) -> int:
    return (3 * value + 1) // 2 if value & 1 else value // 2


def affine_offset(word: Sequence[int]) -> int:
    """Return C in 2**K T**K(n) = 3**q n + C for ``word``."""
    offset = 0
    for index, bit in enumerate(word):
        if bit not in (0, 1):
            raise ValueError("a parity word must contain only 0 and 1")
        offset = (3 if bit else 1) * offset + bit * 2**index
    return offset


def cylinder(word: Sequence[int]) -> Cylinder:
    """Return the least nonnegative residue and endpoint of a parity cylinder."""
    length = len(word)
    odd_count = sum(word)
    offset = affine_offset(word)
    modulus = 2**length
    residue = (
        0 if modulus == 1 else (-offset * pow(3**odd_count, -1, modulus)) % modulus
    )
    endpoint_numerator = 3**odd_count * residue + offset
    endpoint, remainder = divmod(endpoint_numerator, modulus)
    if remainder:
        raise AssertionError((word, endpoint_numerator, modulus))
    return Cylinder(length, odd_count, residue, endpoint, offset)


def realized_trajectory(word: Sequence[int], start: int) -> list[int]:
    """Simulate ``word`` and reject a start with a mismatching parity."""
    trajectory = [start]
    value = start
    for bit in word:
        if value & 1 != bit:
            raise ValueError((word, start, value, bit))
        value = shortcut_step(value)
        trajectory.append(value)
    return trajectory


def ceil_div(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    return -((-numerator) // denominator)


def safe_lift_interval(
    word: Sequence[int], *, positive_starts: bool = True
) -> LiftInterval | None:
    """Return all lifts whose every represented prefix stays above the start.

    If ``r`` is the least cylinder residue and ``K=len(word)``, the starts are
    ``r + 2**K z``.  At prefix ``j`` the margin is exactly

    ``(T**j(r)-r) + (3**q_j * 2**(K-j) - 2**K) z``.

    Each constraint is a half-line in the integer parameter ``z``; their
    intersection is therefore the returned interval.
    """
    data = cylinder(word)
    lower = int(positive_starts and data.residue == 0)
    upper: int | None = None
    value = data.residue
    odd_count = 0
    total_slope = 2**data.length
    for prefix_length, bit in enumerate(word, start=1):
        odd_count += bit
        value = shortcut_step(value)
        intercept = value - data.residue
        slope = 3**odd_count * 2 ** (data.length - prefix_length) - total_slope
        if slope > 0:
            lower = max(lower, ceil_div(-intercept, slope))
        elif slope == 0:
            if intercept < 0:
                return None
        else:
            if intercept < 0:
                return None
            candidate_upper = intercept // (-slope)
            upper = candidate_upper if upper is None else min(upper, candidate_upper)
        if upper is not None and lower > upper:
            return None
    return LiftInterval(max(lower, 0), upper)


def compose_blocks(left: Sequence[int], right: Sequence[int]) -> dict[str, int]:
    """Compose two parity cylinders without replaying the concatenated word."""
    first = cylinder(left)
    second = cylinder(right)
    right_modulus = 2**second.length
    compatible_lift = (
        0
        if right_modulus == 1
        else (
            (second.residue - first.endpoint)
            * pow(3**first.odd_count, -1, right_modulus)
        )
        % right_modulus
    )
    intermediate = first.endpoint + 3**first.odd_count * compatible_lift
    quotient, remainder = divmod(intermediate - second.residue, right_modulus)
    if remainder or quotient < 0:
        raise AssertionError((left, right, intermediate, second.residue))
    return {
        "length": first.length + second.length,
        "odd_count": first.odd_count + second.odd_count,
        "residue": first.residue + 2**first.length * compatible_lift,
        "endpoint": second.endpoint + 3**second.odd_count * quotient,
        "offset": 3**second.odd_count * first.offset + 2**first.length * second.offset,
        "compatible_lift": compatible_lift,
        "intermediate_quotient": quotient,
    }


def interval_record(word: Word) -> list[int | str | None]:
    interval = safe_lift_interval(word)
    return (
        ["".join(map(str, word)), None, None]
        if interval is None
        else [
            "".join(map(str, word)),
            interval.lower,
            interval.upper,
        ]
    )


def canonical_interval_digest(max_length: int) -> str:
    records = [
        interval_record(word)
        for length in range(max_length + 1)
        for word in product((0, 1), repeat=length)
    ]
    encoded = json.dumps(records, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def first_crossing_audit(max_depth: int) -> dict[str, int]:
    """Audit the interval form of Terras's coefficient-stopping conjecture.

    A first-crossing word is coefficient-safe at every proper prefix and has
    ``3**q < 2**K`` at its full length.  The conjecture says that its positive
    all-prefix lift interval is empty, except that ``10`` represents the
    trivial start 1 with equality rather than strict descent.
    """
    frontier: list[tuple[Word, int]] = [((), 0)]
    first_crossings = 0
    unexpected_intervals = 0
    trivial_intervals = 0
    for depth in range(1, max_depth + 1):
        next_frontier: list[tuple[Word, int]] = []
        threshold = 2**depth
        for word, odd_count in frontier:
            for bit in (0, 1):
                extension = word + (bit,)
                next_odd_count = odd_count + bit
                if 3**next_odd_count >= threshold:
                    next_frontier.append((extension, next_odd_count))
                    continue
                first_crossings += 1
                interval = safe_lift_interval(extension)
                if interval is None:
                    continue
                if extension == (1, 0) and interval == LiftInterval(0, 0):
                    trivial_intervals += 1
                else:
                    unexpected_intervals += 1
        frontier = next_frontier
    return {
        "cst_audit_depth": max_depth,
        "cst_first_crossings_checked": first_crossings,
        "cst_trivial_intervals": trivial_intervals,
        "cst_unexpected_intervals": unexpected_intervals,
        "cst_safe_frontier_at_depth": len(frontier),
    }


def probe_values(interval: LiftInterval | None, max_lift: int) -> set[int]:
    probes = set(range(max_lift + 1))
    if interval is not None:
        probes.update((max(0, interval.lower - 1), interval.lower, interval.lower + 1))
        if interval.upper is not None:
            probes.update(
                (max(0, interval.upper - 1), interval.upper, interval.upper + 1)
            )
    return probes


def verify(max_length: int, max_lift: int, cst_depth: int = 0) -> dict[str, int | str]:
    """Exhaustively compare formulas with direct simulation."""
    words_checked = 0
    lifts_checked = 0
    compositions_checked = 0
    for length in range(max_length + 1):
        for word in product((0, 1), repeat=length):
            words_checked += 1
            data = cylinder(word)
            base_trajectory = realized_trajectory(word, data.residue)
            if base_trajectory[-1] != data.endpoint:
                raise AssertionError((word, data, base_trajectory))
            interval = safe_lift_interval(word)
            for lift in sorted(probe_values(interval, max_lift)):
                start = data.residue + 2**length * lift
                trajectory = realized_trajectory(word, start)
                survives = start > 0 and all(value >= start for value in trajectory[1:])
                if survives != (interval is not None and interval.contains(lift)):
                    raise AssertionError((word, lift, interval, trajectory))
                lifts_checked += 1
            for split in range(length + 1):
                composition = compose_blocks(word[:split], word[split:])
                if any(
                    composition[key] != getattr(data, key)
                    for key in ("length", "odd_count", "residue", "endpoint", "offset")
                ):
                    raise AssertionError((word, split, data, composition))
                compositions_checked += 1
    report: dict[str, int | str] = {
        "max_length": max_length,
        "max_lift": max_lift,
        "words_checked": words_checked,
        "lifts_checked": lifts_checked,
        "compositions_checked": compositions_checked,
        "length_10_interval_sha256": canonical_interval_digest(10),
    }
    if cst_depth:
        report.update(first_crossing_audit(cst_depth))
    return report


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=12)
    parser.add_argument("--max-lift", type=int, default=20)
    parser.add_argument("--cst-depth", type=int, default=26)
    args = parser.parse_args(argv)
    if args.max_length < 0:
        parser.error("--max-length must be nonnegative")
    if args.max_lift < 0:
        parser.error("--max-lift must be nonnegative")
    if args.cst_depth < 0:
        parser.error("--cst-depth must be nonnegative")
    return args


def main(argv: Iterable[str] | None = None) -> None:
    args = parse_args(argv)
    for key, value in verify(args.max_length, args.max_lift, args.cst_depth).items():
        print(f"{key}={value}")
    print("status=all exact checks passed")


if __name__ == "__main__":
    main()
