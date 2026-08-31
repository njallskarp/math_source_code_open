#!/usr/bin/env python3
"""Exact verifier for the oriented mod-7 QLP-42 binary-shadow lemma."""

from __future__ import annotations

from collections import Counter
from csv import DictReader
from itertools import product
from pathlib import Path

LENGTH = 7
MASK = (1 << LENGTH) - 1
ROOTS = ((1, 0), (0, 1), (-1, 0), (0, -1))
REPRESENTATIVES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)
EXPECTED_ORBITS = (
    (0x00, 0x01),
    (0x03, 0x13),
    (0x05, 0x07),
    (0x09, 0x15),
    (0x0F, 0x2F),
    (0x17, 0x01),
    (0x1B, 0x1F),
    (0x1D, 0x01),
    (0x2B, 0x37),
    (0x3F, 0x0B),
    (0x3F, 0x0D),
    (0x3F, 0x7F),
)
EXPECTED_SURVIVORS = {
    1: 1,
    5: 6,
    9: 11,
    13: 12,
    17: 12,
    21: 12,
    25: 12,
    29: 12,
    33: 11,
    37: 6,
    41: 1,
}


def rotate(word: int, shift: int) -> int:
    return ((word >> shift) | (word << (LENGTH - shift))) & MASK


def canonical_rotation(word: int) -> int:
    return min(rotate(word, shift) for shift in range(LENGTH))


def overlap_parity(word: int, shift: int) -> int:
    return (word & rotate(word, shift)).bit_count() & 1


def support(word: int) -> str:
    return "{" + ",".join(str(j) for j in range(LENGTH) if word >> j & 1) + "}"


def div_one_plus_i(value: tuple[int, int]) -> tuple[int, int]:
    real, imag = value
    assert (real + imag) % 2 == 0
    assert (imag - real) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def check_local_and_sum_parity() -> None:
    states = set()
    for x, y in product(ROOTS, repeat=2):
        s = div_one_plus_i((x[0] - y[0], x[1] - y[1]))
        h = div_one_plus_i((x[0] + y[0], x[1] + y[1]))
        quarter = int(x[0] * y[0] + x[1] * y[1] == 0)
        assert ((s[0] + s[1]) & 1) == quarter
        assert ((h[0] + h[1]) & 1) == quarter
        states.add((s, h))
    assert len(states) == 16

    for p, q, x, y in REPRESENTATIVES:
        sum_s_a = (p + q, q - p)
        sum_h_a = (0, 0)
        sum_s_b = (x + y - 1, y - x)
        sum_h_b = (1, 0)
        assert (sum(sum_s_a) & 1) == (sum(sum_h_a) & 1) == 0
        assert (sum(sum_s_b) & 1) == (sum(sum_h_b) & 1) == 1


def quotient_pairs() -> set[tuple[int, int]]:
    result = set()
    for left in range(1 << LENGTH):
        for right in range(1 << LENGTH):
            if ((left.bit_count() + right.bit_count()) & 1) != 1:
                continue
            if all(
                overlap_parity(left, shift) == overlap_parity(right, shift)
                for shift in range(1, (LENGTH + 1) // 2)
            ):
                result.add((left, right))
    assert len(result) == 1008
    return result


def main() -> None:
    check_local_and_sum_parity()
    all_pairs = quotient_pairs()
    oriented_pairs = {
        (left, right)
        for left, right in all_pairs
        if left.bit_count() % 2 == 0 and right.bit_count() % 2 == 1
    }
    assert len(oriented_pairs) == 504

    orbits = tuple(
        sorted(
            {
                (canonical_rotation(left), canonical_rotation(right))
                for left, right in oriented_pairs
            }
        )
    )
    assert orbits == EXPECTED_ORBITS

    fixed_sum = 0
    for left_shift in range(LENGTH):
        for right_shift in range(LENGTH):
            fixed = sum(
                rotate(left, left_shift) == left
                and rotate(right, right_shift) == right
                for left, right in oriented_pairs
            )
            if left_shift == 0 and right_shift == 0:
                assert fixed == 504
            elif (left_shift == 0) != (right_shift == 0):
                assert fixed == 7
            else:
                assert fixed == 0
            fixed_sum += fixed
    assert fixed_sum == 588
    assert fixed_sum // (LENGTH * LENGTH) == 12

    survivors = Counter()
    with (Path(__file__).parent / "oriented_orbit_table.tsv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(DictReader(handle, delimiter="\t"))
    assert len(rows) == len(EXPECTED_ORBITS)
    for index, (row, orbit) in enumerate(zip(rows, EXPECTED_ORBITS, strict=True)):
        left, right = orbit
        residue_weight = left.bit_count() + right.bit_count()
        totals = tuple(residue_weight + 4 * k for k in range(8))
        assert row == {
            "orbit": f"{index:02d}",
            "left_mask_hex": f"0x{left:02x}",
            "right_mask_hex": f"0x{right:02x}",
            "left_support": support(left),
            "right_support": support(right),
            "residue_weight": str(residue_weight),
            "quarter_turn_totals": ",".join(map(str, totals)),
        }
        survivors.update(totals)
    assert dict(sorted(survivors.items())) == EXPECTED_SURVIVORS

    assert EXPECTED_ORBITS[0] == (0, 1)
    assert EXPECTED_ORBITS[-1] == (0x3F, 0x7F)
    print("ordered_pairs=504")
    print("independent_rotation_orbits=12")
    print(
        "survivors_by_quarter_total="
        + ",".join(f"{total}:{count}" for total, count in EXPECTED_SURVIVORS.items())
    )
    print("extreme_q1_orbit=0x00,0x01")
    print("extreme_q41_orbit=0x3f,0x7f")
    print("certificate=verified")


if __name__ == "__main__":
    main()
