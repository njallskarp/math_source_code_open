#!/usr/bin/env python3
"""Independent direct-mod-8 audit of the sixth-order S classification."""

from __future__ import annotations

from collections import defaultdict
from csv import DictReader
from pathlib import Path

import numpy as np

N = 21
WORD_MASK = (1 << N) - 1
PI = (1, 1)


def active(axis: int, sign: int) -> tuple[int, int]:
    value = (1, 1) if axis == 0 else (-1, 1)
    return (-value[0], -value[1]) if sign else value


def rotate(word: int, shift: int) -> int:
    return ((word >> shift) | (word << (N - shift))) & WORD_MASK


def correlation_signature(word: int) -> int:
    return sum(
        ((word & rotate(word, shift)).bit_count() & 1) << (shift - 1)
        for shift in range(1, 11)
    )


def theta_values(b_word: int) -> tuple[int, ...]:
    f_word = ((~b_word) & WORD_MASK) & ~1
    b_signature = correlation_signature(b_word)
    f_signature = correlation_signature(f_word)
    return tuple(
        1
        ^ int(shift in (4, 10))
        ^ ((b_signature >> (shift - 1)) & 1)
        ^ ((f_signature >> (shift - 1)) & 1)
        for shift in range(1, 11)
    )


def paf(word: list[tuple[int, int]], shift: int) -> tuple[int, int]:
    real = 0
    imag = 0
    for position, (left_real, left_imag) in enumerate(word):
        right_real, right_imag = word[(position + shift) % N]
        real += left_real * right_real + left_imag * right_imag
        imag += left_imag * right_real - left_real * right_imag
    return real, imag


def target_s(shift: int) -> tuple[int, int]:
    if shift == 4:
        return -2, 0
    if shift == 10:
        return 2, 0
    return 0, 0


def a_targets(positions: list[int]) -> set[int]:
    targets = set()
    for exceptional in positions:
        word = [(0, 0)] * N
        for position in positions:
            word[position] = active(
                0 if position == exceptional else 1,
                0 if position == exceptional else 1,
            )
        assert tuple(map(sum, zip(*word, strict=True))) == (5, -3)
        fingerprint = 0
        for shift in range(1, 11):
            a_real, a_imag = paf(word, shift)
            target_real, target_imag = target_s(shift)
            fingerprint |= ((target_real - a_real) & 7) << (6 * (shift - 1))
            fingerprint |= ((target_imag - a_imag) & 7) << (6 * (shift - 1) + 3)
        targets.add(fingerprint)
    assert 1 <= len(targets) <= 5
    return targets


def parse_positions(text: str) -> list[int]:
    return [int(value) for value in text.split(",")]


def enumerate_b(
    b_word: int, targets: set[int], signs: np.ndarray
) -> tuple[int, set[int], set[int]]:
    theta = theta_values(b_word)
    shifts = [shift for shift in range(1, 11) if (b_word >> shift) & 1]
    assert len(shifts) == 8
    sign_positions = []
    for shift in shifts:
        sign_positions.extend((shift, N - shift))
    sign_positions.append(0)
    position_index = {position: index for index, position in enumerate(sign_positions)}
    exact_count = 0
    reachable: set[int] = set()
    matched: set[int] = set()

    for axes in range(256):
        base = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            base.extend((active(axis, 0), active(axis ^ theta[shift - 1], 0)))
        base.append((0, -1))
        base_real = np.array([value[0] for value in base], dtype=np.int16)
        base_imag = np.array([value[1] for value in base], dtype=np.int16)
        real_sums = signs @ base_real
        imag_sums = signs @ base_imag
        exact = (real_sums == 0) & (imag_sums == -3)
        exact_signs = signs[exact]
        exact_count += len(exact_signs)
        if not len(exact_signs):
            continue

        fingerprints = np.zeros(len(exact_signs), dtype=np.uint64)
        for shift in range(1, 11):
            real = np.zeros(len(exact_signs), dtype=np.int16)
            imag = np.zeros(len(exact_signs), dtype=np.int16)
            for left_position, left_index in position_index.items():
                right_position = (left_position + shift) % N
                right_index = position_index.get(right_position)
                if right_index is None:
                    continue
                left_real, left_imag = base[left_index]
                right_real, right_imag = base[right_index]
                scalar = exact_signs[:, left_index] * exact_signs[:, right_index]
                real += scalar * (
                    left_real * right_real + left_imag * right_imag
                )
                imag += scalar * (
                    left_imag * right_real - left_real * right_imag
                )
            fingerprints |= (real.astype(np.uint64) & 7) << (6 * (shift - 1))
            fingerprints |= (imag.astype(np.uint64) & 7) << (6 * (shift - 1) + 3)
        unique = np.unique(fingerprints)
        reachable.update(int(value) for value in unique)
        if len(matched) != len(targets):
            unique_set = set(map(int, unique))
            matched.update(targets & unique_set)

    assert exact_count == 804_968
    return exact_count, reachable, matched


def main() -> None:
    directory = Path(__file__).resolve().parent
    with (directory.parent / "qlp42_q1_b16_fifth_order_s" / "orbit_table.tsv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = [row for row in DictReader(handle, delimiter="\t") if row["fifth_s_soluble"] == "1"]
    assert len(rows) == 16

    grouped: dict[int, list[dict[str, str]]] = defaultdict(list)
    row_targets = {}
    for row in rows:
        equal_word = sum(1 << position for position in parse_positions(row["b_equal_positions"]))
        b_word = WORD_MASK ^ equal_word ^ 1
        grouped[b_word].append(row)
        key = (row["b_equal_positions"], row["a_opposite_orbit_representative"])
        row_targets[key] = a_targets(parse_positions(row["a_opposite_orbit_representative"]))
    assert len(grouped) == 11

    masks = np.arange(1 << 17, dtype=np.uint32)[:, None]
    bit_positions = np.arange(17, dtype=np.uint32)[None, :]
    signs = (1 - 2 * ((masks >> bit_positions) & 1).astype(np.int8)).astype(np.int8)

    output = []
    for b_word, group in grouped.items():
        all_targets = set().union(*(
            row_targets[(row["b_equal_positions"], row["a_opposite_orbit_representative"])]
            for row in group
        ))
        exact_count, reachable, matched = enumerate_b(b_word, all_targets, signs)
        for row in group:
            key = (row["b_equal_positions"], row["a_opposite_orbit_representative"])
            feasible = bool(row_targets[key] & matched)
            output.append((
                row["b_equal_positions"],
                row["a_opposite_orbit_representative"],
                row["fourth_order_rank"],
                exact_count,
                len(reachable),
                int(feasible),
            ))
    order = {
        (row["b_equal_positions"], row["a_opposite_orbit_representative"]): index
        for index, row in enumerate(rows)
    }
    output.sort(key=lambda row: order[(row[0], row[1])])
    print(
        "b_equal_positions\ta_opposite_orbit_representative\tfourth_order_rank"
        "\tb_exact_s_phase_assignments\tb_sixth_residue_fingerprints"
        "\tsixth_s_soluble"
    )
    for row in output:
        print(*row, sep="\t")


if __name__ == "__main__":
    main()
