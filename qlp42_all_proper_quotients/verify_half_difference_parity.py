#!/usr/bin/env python3
"""Verify the binary shadow of the norm-32 half-difference equations.

The mathematical proof of the resulting mod-4 count restriction is direct.
This independent finite check enumerates all length-21 binary words, groups
them by their periodic autocorrelation vector over F_2, and verifies the
restriction for every compatible pair of groups without enumerating the
roughly 1.6 billion compatible ordered pairs individually.
"""

from collections import Counter, defaultdict

LENGTH = 21
MASK = (1 << LENGTH) - 1


def rotate(mask: int, shift: int) -> int:
    return ((mask << shift) | (mask >> (LENGTH - shift))) & MASK


def signature(mask: int) -> int:
    result = mask.bit_count() & 1
    for shift in range(1, LENGTH // 2 + 1):
        overlap_parity = (mask & rotate(mask, shift)).bit_count() & 1
        result |= overlap_parity << shift
    return result


def main() -> None:
    counts: Counter[tuple[int, int]] = Counter()
    residues: dict[int, set[int]] = defaultdict(set)
    signature_counts: Counter[int] = Counter()
    for mask in range(1 << LENGTH):
        word_signature = signature(mask)
        weight_residue = mask.bit_count() % 4
        counts[(word_signature, weight_residue)] += 1
        residues[word_signature].add(weight_residue)
        signature_counts[word_signature] += 1

    # The target binary autocorrelation is one at shift zero and zero at all
    # other shifts, so compatible signatures differ only in their low bit.
    compatible_pairs = 0
    for left_signature, left_count in signature_counts.items():
        right_signature = left_signature ^ 1
        compatible_pairs += left_count * signature_counts[right_signature]
        for left_residue in residues[left_signature]:
            for right_residue in residues[right_signature]:
                assert (left_residue + right_residue) % 4 == 1

    triples = []
    for quarter_turns in range(43):
        remainder = 43 - quarter_turns
        if remainder % 2:
            continue
        opposites = remainder // 2
        zeros = 42 - quarter_turns - opposites
        if zeros >= 0 and quarter_turns % 4 == 1:
            triples.append((quarter_turns, opposites, zeros))
    assert triples == [(1 + 4 * t, 21 - 2 * t, 20 - 2 * t) for t in range(11)]

    print(f"binary_words={1 << LENGTH}")
    print(f"autocorrelation_signatures={len(signature_counts)}")
    print(f"compatible_ordered_pairs={compatible_pairs}")
    print("count_triples=" + ",".join(map(str, triples)))
    print("certificate=verified")


if __name__ == "__main__":
    main()
