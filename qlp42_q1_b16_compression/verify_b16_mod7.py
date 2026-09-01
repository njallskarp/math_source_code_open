#!/usr/bin/env python3
"""Exact mod-7 compression filter for the q=1, b=16 QLP-42 row."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

G = tuple[int, int]
Pattern = tuple[tuple[int, ...], tuple[int, ...], int]

LENGTH = 21
WORD_MASK = (1 << LENGTH) - 1
HALF_SHIFTS = range(1, 11)
TAU_SIGNATURE = (1 << 3) | (1 << 9)


def rotate(word: int, shift: int) -> int:
    return ((word >> shift) | (word << (LENGTH - shift))) & WORD_MASK


def correlation_signature(word: int) -> int:
    return sum(
        ((word & rotate(word, shift)).bit_count() & 1) << (shift - 1)
        for shift in HALF_SHIFTS
    )


def symmetric_b_word(opposite_pairs: tuple[int, ...]) -> int:
    return sum((1 << shift) | (1 << (LENGTH - shift)) for shift in opposite_pairs)


def positions(word: int) -> tuple[int, ...]:
    return tuple(position for position in range(LENGTH) if (word >> position) & 1)


def orbit_representative(word: int) -> tuple[int, ...]:
    return min(positions(rotate(word, shift)) for shift in range(LENGTH))


def fiber_counts(support: tuple[int, ...]) -> tuple[int, ...]:
    counts = [0] * 7
    for position in support:
        counts[position % 7] += 1
    return tuple(counts)


def dihedral_representative(
    a_counts: tuple[int, ...], b_counts: tuple[int, ...], center: int
) -> tuple[tuple[int, ...], tuple[int, ...], int]:
    candidates = []
    for sign in (1, -1):
        for shift in range(7):
            candidates.append(
                (
                    tuple(a_counts[(sign * index + shift) % 7] for index in range(7)),
                    tuple(b_counts[(sign * index + shift) % 7] for index in range(7)),
                    (sign * (center - shift)) % 7,
                )
            )
    return min(candidates)


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def multiply_conjugate(left: G, right: G) -> G:
    return (
        left[0] * right[0] + left[1] * right[1],
        left[1] * right[0] - left[0] * right[1],
    )


def root_sum_domain(count: int) -> tuple[G, ...]:
    unscaled = {
        (real, imag)
        for real in range(-count, count + 1)
        for imag in range(-count, count + 1)
        if abs(real) + abs(imag) <= count
        and (real + imag - count) % 2 == 0
    }
    return tuple(sorted((real - imag, real + imag) for real, imag in unscaled))


def fingerprint(word: tuple[G, ...]) -> tuple[int, ...]:
    result = [sum(real * real + imag * imag for real, imag in word)]
    for shift in range(1, 4):
        correlation = (0, 0)
        for index, value in enumerate(word):
            correlation = add(
                correlation,
                multiply_conjugate(value, word[(index + shift) % 7]),
            )
        result.extend(correlation)
    return tuple(result)


def enumerate_a_fingerprints(
    counts: tuple[int, ...], domains: dict[int, tuple[G, ...]]
) -> tuple[int, int, set[tuple[int, ...]]]:
    derive = counts.index(max(counts))
    indices = tuple(index for index in range(7) if index != derive)
    allowed = set(domains[counts[derive]])
    raw_prefixes = 0
    sum_zero = 0
    fingerprints: set[tuple[int, ...]] = set()
    for prefix in product(*(domains[counts[index]] for index in indices)):
        raw_prefixes += 1
        last = (-sum(value[0] for value in prefix), -sum(value[1] for value in prefix))
        if last not in allowed:
            continue
        sum_zero += 1
        word: list[G] = [(0, 0)] * 7
        word[derive] = last
        for index, value in zip(indices, prefix, strict=True):
            word[index] = value
        fingerprints.add(fingerprint(tuple(word)))
    return raw_prefixes, sum_zero, fingerprints


def enumerate_b_words(pattern: Pattern, domains: dict[int, tuple[G, ...]]) -> set[tuple[G, ...]]:
    _a_counts, b_counts, center = pattern
    candidates = set()
    for center_sign in (1, -1):
        for diagonal_word in product(*(domains[count] for count in b_counts)):
            word = list(diagonal_word)
            word[center] = add(word[center], (center_sign, 0))
            if tuple(map(sum, zip(*word, strict=True))) == (1, 0):
                candidates.add(tuple(word))
    return candidates


def complement_target(b_fingerprint: tuple[int, ...]) -> tuple[int, ...]:
    result = [37 - b_fingerprint[0]]
    for shift in range(1, 4):
        result.extend((-6 - b_fingerprint[2 * shift - 1], -b_fingerprint[2 * shift]))
    return tuple(result)


def classify() -> tuple[
    list[tuple[int, list[int], list[Pattern]]], Counter[Pattern], int
]:
    a_words = [
        sum(1 << position for position in support)
        for support in combinations(range(LENGTH), 5)
    ]
    by_signature: dict[int, list[int]] = defaultdict(list)
    for word in a_words:
        by_signature[correlation_signature(word)].append(word)

    classified: list[tuple[int, list[int]]] = []
    patterns: Counter[Pattern] = Counter()
    orbit_total = 0
    for opposite_pairs in combinations(HALF_SHIFTS, 8):
        b_word = symmetric_b_word(opposite_pairs)
        f_word = ((~b_word) & WORD_MASK) & ~1
        b_signature = correlation_signature(b_word)
        f_signature = correlation_signature(f_word)
        required = 0
        for shift in HALF_SHIFTS:
            bit = shift - 1
            value = (
                (f_signature >> bit) & 1
                if (b_word >> shift) & 1
                else ((TAU_SIGNATURE ^ b_signature) >> bit) & 1
            )
            required |= value << bit
        matches = by_signature[required]
        if not matches:
            continue
        classified.append((b_word, matches))
        orbit_total += len({orbit_representative(word) for word in matches})
        b_diagonal_support = tuple(
            position
            for position in range(1, LENGTH)
            if not (b_word >> position) & 1
        )
        b_counts = fiber_counts(b_diagonal_support)
        pair_patterns = []
        for a_word in matches:
            a_support = tuple(
                position for position in range(LENGTH) if not (a_word >> position) & 1
            )
            pattern = dihedral_representative(fiber_counts(a_support), b_counts, 0)
            patterns[pattern] += 1
            pair_patterns.append(pattern)
        classified[-1] = (b_word, matches, pair_patterns)

    assert len(classified) == 25
    assert sum(len(matches) for _, matches, _ in classified) == 1575
    assert orbit_total == 75

    assert len(patterns) == 57
    return classified, patterns, orbit_total


def main() -> None:
    classified, patterns, orbit_total = classify()
    domains = {count: root_sum_domain(count) for count in range(4)}
    assert [len(domains[count]) for count in range(4)] == [1, 4, 9, 16]

    a_cache = {
        counts: enumerate_a_fingerprints(counts, domains)
        for counts in sorted({pattern[0] for pattern in patterns})
    }
    feasible_patterns: set[Pattern] = set()
    b_words_total = 0
    feasible_b_words_total = 0
    for pattern in patterns:
        b_words = enumerate_b_words(pattern, domains)
        b_words_total += len(b_words)
        targets = {complement_target(fingerprint(word)) for word in b_words}
        matches = targets & a_cache[pattern[0]][2]
        feasible_b_words_total += sum(target in matches for target in targets)
        if matches:
            feasible_patterns.add(pattern)

    survivors_by_b: dict[int, list[int]] = defaultdict(list)
    for b_index, (_b_word, matches, pair_patterns) in enumerate(classified):
        for a_word, pattern in zip(matches, pair_patterns, strict=True):
            if pattern in feasible_patterns:
                survivors_by_b[b_index].append(a_word)

    surviving_orbits = 0
    for words in survivors_by_b.values():
        orbit_counts = Counter(orbit_representative(word) for word in words)
        assert set(orbit_counts.values()) == {21}
        surviving_orbits += len(orbit_counts)

    feasible_labeled = sum(patterns[pattern] for pattern in feasible_patterns)
    assert len(feasible_patterns) == 24
    assert feasible_labeled == 756
    assert len(survivors_by_b) == 18
    assert surviving_orbits == 36

    output = [
        f"third_order_b_masks={len(classified)}",
        f"third_order_labeled_pairs={sum(len(matches) for _, matches, _ in classified)}",
        f"third_order_a_rotation_orbits={orbit_total}",
        f"mod7_support_patterns={len(patterns)}",
        f"a_count_patterns={len(a_cache)}",
        f"a_raw_prefixes={sum(item[0] for item in a_cache.values())}",
        f"a_sum_zero_words={sum(item[1] for item in a_cache.values())}",
        f"a_distinct_fingerprints={sum(len(item[2]) for item in a_cache.values())}",
        f"b_compressed_words_across_patterns={b_words_total}",
        f"feasible_b_fingerprints_across_patterns={feasible_b_words_total}",
        f"eliminated_support_patterns={len(patterns) - len(feasible_patterns)}",
        f"surviving_support_patterns={len(feasible_patterns)}",
        f"eliminated_b_masks={len(classified) - len(survivors_by_b)}",
        f"surviving_b_masks={len(survivors_by_b)}",
        f"eliminated_labeled_pairs={1575 - feasible_labeled}",
        f"surviving_labeled_pairs={feasible_labeled}",
        f"eliminated_a_rotation_orbits={orbit_total - surviving_orbits}",
        f"surviving_a_rotation_orbits={surviving_orbits}",
        "global_remaining_b_masks=470",
        "global_remaining_labeled_pairs=193557",
        "global_remaining_a_rotation_orbits=9217",
        "certificate=verified",
    ]
    expected = (Path(__file__).parent / "verification_output.txt").read_text(encoding="utf-8")
    assert expected == "\n".join(output) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
