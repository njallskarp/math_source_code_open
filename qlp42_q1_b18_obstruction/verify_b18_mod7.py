#!/usr/bin/env python3
"""Exact mod-7 obstruction for the q=1, b=18 QLP-42 type row."""

from __future__ import annotations

from itertools import combinations, product
from pathlib import Path

G = tuple[int, int]
LENGTH = 21
WORD_MASK = (1 << LENGTH) - 1
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
HALF_SHIFTS = range(1, 11)
TAU_SIGNATURE = (1 << 3) | (1 << 9)
SUPPORT_COUNTS = (2, 2, 3, 3, 2, 3, 3)


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def multiply(left: G, right: G) -> G:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def multiply_conjugate(left: G, right: G) -> G:
    return (
        left[0] * right[0] + left[1] * right[1],
        left[1] * right[0] - left[0] * right[1],
    )


def rotate(word: int, shift: int) -> int:
    return ((word >> shift) | (word << (LENGTH - shift))) & WORD_MASK


def correlation_signature(word: int) -> int:
    return sum(
        ((word & rotate(word, shift)).bit_count() & 1) << (shift - 1)
        for shift in HALF_SHIFTS
    )


def symmetric_b_word(opposite_pairs: tuple[int, ...]) -> int:
    return sum((1 << shift) | (1 << (LENGTH - shift)) for shift in opposite_pairs)


def combination(word: int) -> tuple[int, ...]:
    return tuple(position for position in range(LENGTH) if (word >> position) & 1)


def orbit_representative(word: int) -> tuple[int, ...]:
    return min(combination(rotate(word, shift)) for shift in range(LENGTH))


def classify_b18_types() -> list[tuple[int, list[int]]]:
    a_words = [sum(1 << position for position in positions) for positions in combinations(range(LENGTH), 3)]
    result = []
    for opposite_pairs in combinations(HALF_SHIFTS, 9):
        b_word = symmetric_b_word(opposite_pairs)
        f_word = ((~b_word) & WORD_MASK) & ~1
        b_signature = correlation_signature(b_word)
        f_signature = correlation_signature(f_word)
        required = 0
        for shift in HALF_SHIFTS:
            bit = shift - 1
            if (b_word >> shift) & 1:
                value = (f_signature >> bit) & 1
            else:
                value = ((TAU_SIGNATURE ^ b_signature) >> bit) & 1
            required |= value << bit
        matches = [word for word in a_words if correlation_signature(word) == required]
        if matches:
            result.append((b_word, matches))

    assert len(result) == 2
    assert [len(matches) for _, matches in result] == [21, 21]
    assert {
        orbit_representative(word) for _, matches in result for word in matches
    } == {(0, 1, 11), (0, 4, 8)}
    assert {
        tuple(position for position in range(1, LENGTH) if not (b_word >> position) & 1)
        for b_word, _ in result
    } == {(4, 17), (10, 11)}

    for b_word, matches in result:
        equal_residues = {
            position % 7
            for position in range(1, LENGTH)
            if not (b_word >> position) & 1
        }
        assert equal_residues == {3, 4}
        for word in matches:
            residues = {position % 7 for position in combination(word)}
            assert any(
                residues == {shift, (shift + 1) % 7, (shift + 4) % 7}
                for shift in range(7)
            )
    return result


def root_sum_domain(count: int) -> tuple[G, ...]:
    reached = {(0, 0)}
    for _ in range(count):
        reached = {add(partial, root) for partial in reached for root in ROOTS}
    formula = {
        (real, imag)
        for real in range(-count, count + 1)
        for imag in range(-count, count + 1)
        if abs(real) + abs(imag) <= count
        and (real + imag - count) % 2 == 0
    }
    assert reached == formula
    return tuple(sorted(multiply((1, 1), value) for value in reached))


def periodic_correlation(word: tuple[G, ...], shift: int) -> G:
    result = (0, 0)
    for index, value in enumerate(word):
        result = add(
            result,
            multiply_conjugate(value, word[(index + shift) % len(word)]),
        )
    return result


def b_compressions() -> list[tuple[G, ...]]:
    result = []
    for center in ((1, 0), (-1, 0)):
        for left, right in product(ROOTS, repeat=2):
            word = [(0, 0)] * 7
            word[0] = center
            word[3] = multiply((1, 1), left)
            word[4] = multiply((1, 1), right)
            candidate = tuple(word)
            if tuple(map(sum, zip(*candidate, strict=True))) == (1, 0):
                result.append(candidate)
    assert len(result) == 6
    assert sum(word[0] == (1, 0) for word in result) == 4
    assert sum(word[0] == (-1, 0) for word in result) == 2
    return result


def enumerate_compressions(
    domains: dict[int, tuple[G, ...]], b_words: list[tuple[G, ...]]
) -> tuple[int, int, list[list[int]]]:
    derive = 6
    derived_domain = set(domains[SUPPORT_COUNTS[derive]])
    sum_zero = 0
    energy_32 = 0
    passes = [[0, 0, 0] for _ in b_words]

    for prefix in product(*(domains[SUPPORT_COUNTS[index]] for index in range(derive))):
        last = (
            -sum(value[0] for value in prefix),
            -sum(value[1] for value in prefix),
        )
        if last not in derived_domain:
            continue
        word = (*prefix, last)
        sum_zero += 1
        if sum(real * real + imag * imag for real, imag in word) != 32:
            continue
        energy_32 += 1
        correlations = tuple(periodic_correlation(word, shift) for shift in range(1, 4))
        for index, b_word in enumerate(b_words):
            for shift in range(3):
                combined = add(correlations[shift], periodic_correlation(b_word, shift + 1))
                if combined != (-6, 0):
                    break
                passes[index][shift] += 1

    return sum_zero, energy_32, passes


def main() -> None:
    classified = classify_b18_types()
    domains = {count: root_sum_domain(count) for count in (2, 3)}
    b_words = b_compressions()
    sum_zero, energy_32, passes = enumerate_compressions(domains, b_words)

    assert sum_zero == 1_028_196
    assert energy_32 == 33_072
    assert passes[:4] == [[664, 16, 0]] * 4
    assert passes[4:] == [[536, 24, 0]] * 2

    raw_tuples = 1
    for count in SUPPORT_COUNTS:
        raw_tuples *= len(domains[count])
    output = [
        f"third_order_b_masks={len(classified)}",
        f"third_order_labeled_pairs={sum(len(matches) for _, matches in classified)}",
        "third_order_a_rotation_orbits=2",
        "a_compressed_support_counts=2233233",
        "b_compressed_support=0,3,4",
        f"d2_size={len(domains[2])}",
        f"d3_size={len(domains[3])}",
        f"raw_domain_tuples={raw_tuples}",
        f"sum_zero_tuples={sum_zero}",
        f"energy_32_tuples={energy_32}",
        "positive_center_b_choices=4",
        f"positive_center_shift1={passes[0][0]}",
        f"positive_center_shifts12={passes[0][1]}",
        f"positive_center_shifts123={passes[0][2]}",
        "negative_center_b_choices=2",
        f"negative_center_shift1={passes[4][0]}",
        f"negative_center_shifts12={passes[4][1]}",
        f"negative_center_shifts123={passes[4][2]}",
        "solutions=0",
        "certificate=verified",
    ]
    expected = (Path(__file__).parent / "verification_output.txt").read_text(
        encoding="utf-8"
    )
    assert expected == "\n".join(output) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
