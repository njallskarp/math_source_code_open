#!/usr/bin/env python3
"""Exact certificate for the mod-7 binary shadow of the norm-32 QLP-42 shell."""

from __future__ import annotations

from collections import defaultdict
from csv import DictReader
from itertools import product
from pathlib import Path

LENGTH = 21
QUOTIENT = 7
WORD_MASK = (1 << LENGTH) - 1
QUOTIENT_MASK = (1 << QUOTIENT) - 1
ROOTS = ((1, 0), (0, 1), (-1, 0), (0, -1))

# Representatives are bit masks on Z/7Z.  Bit r is the residue-r entry.
EXPECTED_ORBITS = (
    (0, 1),
    (1, 0),
    (1, 23),
    (1, 29),
    (3, 19),
    (5, 7),
    (7, 5),
    (9, 21),
    (11, 63),
    (13, 63),
    (15, 47),
    (19, 3),
    (21, 9),
    (23, 1),
    (27, 31),
    (29, 1),
    (31, 27),
    (43, 55),
    (47, 15),
    (55, 43),
    (63, 11),
    (63, 13),
    (63, 127),
    (127, 63),
)


def rotate(word: int, shift: int, length: int) -> int:
    mask = (1 << length) - 1
    return ((word >> shift) | (word << (length - shift))) & mask


def canonical_rotation(word: int, length: int) -> int:
    return min(rotate(word, shift, length) for shift in range(length))


def overlap_parity(word: int, shift: int, length: int) -> int:
    return (word & rotate(word, shift, length)).bit_count() & 1


def quotient_shadow(word: int) -> int:
    result = 0
    for residue in range(QUOTIENT):
        bit = (
            ((word >> residue) & 1)
            ^ ((word >> (residue + QUOTIENT)) & 1)
            ^ ((word >> (residue + 2 * QUOTIENT)) & 1)
        )
        result |= bit << residue
    return result


def support(word: int) -> str:
    return "{" + ",".join(str(j) for j in range(QUOTIENT) if (word >> j) & 1) + "}"


def carryless_product(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        right >>= 1
    return result


def check_local_transform() -> None:
    states = set()
    for x, y in product(ROOTS, repeat=2):
        dr, di = x[0] - y[0], x[1] - y[1]
        ar, ai = x[0] + y[0], x[1] + y[1]
        s = ((dr + di) // 2, (di - dr) // 2)
        h = ((ar + ai) // 2, (ai - ar) // 2)
        quarter_turn = int(x[0] * y[0] + x[1] * y[1] == 0)
        assert ((s[0] + s[1]) & 1) == quarter_turn
        assert ((h[0] + h[1]) & 1) == quarter_turn
        states.add((s, h))
    assert len(states) == 16


def check_compressed_targets() -> None:
    target_s = [0] * LENGTH
    target_s[0] = 43
    target_s[4] = target_s[17] = -2
    target_s[10] = target_s[11] = 2
    target_h = [41] + [-2] * (LENGTH - 1)

    compressed_s = [
        sum(target_s[residue + QUOTIENT * j] for j in range(3))
        for residue in range(QUOTIENT)
    ]
    compressed_h = [
        sum(target_h[residue + QUOTIENT * j] for j in range(3))
        for residue in range(QUOTIENT)
    ]
    assert compressed_s == [43, 0, 0, 0, 0, 0, 0]
    assert compressed_h == [37, -6, -6, -6, -6, -6, -6]


def length_seven_pairs() -> set[tuple[int, int]]:
    result = set()
    for left in range(1 << QUOTIENT):
        for right in range(1 << QUOTIENT):
            if ((left.bit_count() + right.bit_count()) & 1) != 1:
                continue
            if all(
                overlap_parity(left, shift, QUOTIENT)
                == overlap_parity(right, shift, QUOTIENT)
                for shift in range(1, (QUOTIENT + 1) // 2)
            ):
                result.add((left, right))
    assert len(result) == 1008
    return result


def full_length_lifts() -> dict[tuple[int, int], int]:
    # groups[parity][signature][mod-7 shadow] is a bit mask of exact weights.
    groups: list[list[dict[int, int]]] = [
        [defaultdict(int) for _ in range(1 << 10)] for _ in range(2)
    ]
    for word in range(1 << LENGTH):
        weight = word.bit_count()
        signature = 0
        for shift in range(1, 11):
            signature |= overlap_parity(word, shift, LENGTH) << (shift - 1)
        shadow = quotient_shadow(word)
        groups[weight & 1][signature][shadow] |= 1 << weight

    pair_weights: dict[tuple[int, int], int] = defaultdict(int)
    for signature in range(1 << 10):
        for left_parity, right_parity in ((0, 1), (1, 0)):
            for left, left_weights in groups[left_parity][signature].items():
                for right, right_weights in groups[right_parity][signature].items():
                    totals = 0
                    for left_weight in range(left_parity, LENGTH + 1, 2):
                        if not ((left_weights >> left_weight) & 1):
                            continue
                        for right_weight in range(right_parity, LENGTH + 1, 2):
                            if (right_weights >> right_weight) & 1:
                                totals |= 1 << (left_weight + right_weight)
                    pair_weights[(left, right)] |= totals
    return pair_weights


def main() -> None:
    factorization = carryless_product(
        carryless_product(0b11, 0b1011), 0b1101
    )
    assert factorization == 0b10000001  # x^7+1 in F_2[x]
    assert 2 * (8**2 - 1) * 8 == 1008
    check_local_transform()
    check_compressed_targets()

    direct_pairs = length_seven_pairs()
    orbit_pairs = sorted(
        {
            (
                canonical_rotation(left, QUOTIENT),
                canonical_rotation(right, QUOTIENT),
            )
            for left, right in direct_pairs
        }
    )
    assert tuple(orbit_pairs) == EXPECTED_ORBITS

    lift_weights = full_length_lifts()
    assert set(lift_weights) == direct_pairs
    for (left, right), totals in lift_weights.items():
        residue_weight = left.bit_count() + right.bit_count()
        assert tuple(total for total in range(43) if (totals >> total) & 1) == tuple(
            residue_weight + 4 * k for k in range(8)
        )

    orbit_weights: dict[tuple[int, int], int] = defaultdict(int)
    for (left, right), totals in lift_weights.items():
        orbit = (
            canonical_rotation(left, QUOTIENT),
            canonical_rotation(right, QUOTIENT),
        )
        orbit_weights[orbit] |= totals

    survivor_counts = defaultdict(int)
    print("orbit\tleft\tright\tweights\tquarter_turn_totals")
    for index, orbit in enumerate(EXPECTED_ORBITS):
        left, right = orbit
        residue_weight = left.bit_count() + right.bit_count()
        expected_totals = tuple(residue_weight + 4 * k for k in range(8))
        actual_totals = tuple(
            total for total in range(43) if (orbit_weights[orbit] >> total) & 1
        )
        assert actual_totals == expected_totals
        for total in actual_totals:
            survivor_counts[total] += 1
        print(
            f"{index:02d}\t{support(left)}\t{support(right)}\t"
            f"{left.bit_count()}+{right.bit_count()}\t"
            + ",".join(map(str, actual_totals))
        )

    expected_survivors = {
        1: 2,
        5: 12,
        9: 22,
        13: 24,
        17: 24,
        21: 24,
        25: 24,
        29: 24,
        33: 22,
        37: 12,
        41: 2,
    }
    assert dict(survivor_counts) == expected_survivors

    with (Path(__file__).parent / "orbit_table.tsv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(DictReader(handle, delimiter="\t"))
    assert len(rows) == len(EXPECTED_ORBITS)
    for index, (row, orbit) in enumerate(zip(rows, EXPECTED_ORBITS, strict=True)):
        left, right = orbit
        residue_weight = left.bit_count() + right.bit_count()
        totals = ",".join(str(residue_weight + 4 * k) for k in range(8))
        assert row == {
            "orbit": f"{index:02d}",
            "left_mask_hex": f"0x{left:02x}",
            "right_mask_hex": f"0x{right:02x}",
            "left_support": support(left),
            "right_support": support(right),
            "residue_weight": str(residue_weight),
            "quarter_turn_totals": totals,
        }

    # Burnside check for independent C_7 rotations.  The identity fixes all
    # 1008 pairs; 12 one-sided nonidentity rotations fix 14 pairs each; the
    # 36 rotations nontrivial on both words fix none.
    fixed_sum = 0
    for left_shift in range(QUOTIENT):
        for right_shift in range(QUOTIENT):
            fixed = sum(
                rotate(left, left_shift, QUOTIENT) == left
                and rotate(right, right_shift, QUOTIENT) == right
                for left, right in direct_pairs
            )
            if left_shift == 0 and right_shift == 0:
                assert fixed == 1008
            elif (left_shift == 0) != (right_shift == 0):
                assert fixed == 14
            else:
                assert fixed == 0
            fixed_sum += fixed
    assert fixed_sum // (QUOTIENT * QUOTIENT) == 24

    print("ordered_length7_pairs=1008")
    print("independent_rotation_orbits=24")
    print("survivors_by_quarter_total=" + ",".join(
        f"{total}:{count}" for total, count in expected_survivors.items()
    ))
    print("certificate=verified")


if __name__ == "__main__":
    main()
