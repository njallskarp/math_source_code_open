#!/usr/bin/env python3
"""Direct seventh-order S test of the last two q=1, b=16 case-1 orbits."""

from __future__ import annotations

import numpy as np

import prototype_numpy as base


def encode(real: np.ndarray, imag: np.ndarray, shift: int, low: np.ndarray, high: np.ndarray) -> None:
    # Z[i]/(pi^7): z=r+si maps to (r mod 8, r+s mod 16).
    value = (real.astype(np.uint64) & 7) | (((real + imag).astype(np.uint64) & 15) << 3)
    if shift <= 9:
        low |= value << (7 * (shift - 1))
    else:
        high |= value


def scalar_key(values: list[tuple[int, int]]) -> tuple[int, int]:
    low = 0
    high = 0
    for shift, (real, imag) in enumerate(values, 1):
        value = (real & 7) | (((real + imag) & 15) << 3)
        if shift <= 9:
            low |= value << (7 * (shift - 1))
        else:
            high = value
    return low, high


def a_target_keys(positions: list[int]) -> set[tuple[int, int]]:
    result = set()
    patterns = base.phase_patterns((3, -3), 5)
    assert len(patterns) == 25
    for values in patterns:
        word = [(0, 0)] * base.N
        for position, value in zip(positions, values, strict=True):
            word[position] = value
        needed = []
        for shift in range(1, 11):
            a_real, a_imag = base.paf(word, shift)
            target_real, target_imag = base.target_s(shift)
            needed.append((target_real - a_real, target_imag - a_imag))
        result.add(scalar_key(needed))
    return result


def enumerate_b() -> tuple[int, set[tuple[int, int]]]:
    equal_word = sum(1 << position for position in (2, 6, 15, 19))
    b_word = base.WORD_MASK ^ equal_word ^ 1
    directory = base.Path(__file__).resolve().parent
    fourth = base.load_module(
        directory.parent / "qlp42_q1_b16_fourth_order" / "verify_b16_fourth_order.py",
        "seventh_fourth",
        base.FOURTH_SHA256,
    )
    base_module = fourth.load_dependency()
    theta = fourth.theta_values(base_module, b_word)
    shifts = [shift for shift in range(1, 11) if (b_word >> shift) & 1]
    assert len(shifts) == 8
    sign_positions = []
    for shift in shifts:
        sign_positions.extend((shift, base.N - shift))
    sign_positions.append(0)
    position_index = {position: index for index, position in enumerate(sign_positions)}

    masks = np.arange(1 << 17, dtype=np.uint32)[:, None]
    bit_positions = np.arange(17, dtype=np.uint32)[None, :]
    signs = (1 - 2 * ((masks >> bit_positions) & 1).astype(np.int8)).astype(np.int8)
    reachable = set()
    exact_count = 0
    for axes in range(256):
        values = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            values.extend((base.active(axis, 0), base.active(axis ^ theta[shift - 1], 0)))
        values.append((0, -1))
        value_real = np.array([value[0] for value in values], dtype=np.int16)
        value_imag = np.array([value[1] for value in values], dtype=np.int16)
        real_sums = signs @ value_real
        imag_sums = signs @ value_imag
        exact = (real_sums == 4) & (imag_sums == -3)
        exact_signs = signs[exact]
        exact_count += len(exact_signs)
        low = np.zeros(len(exact_signs), dtype=np.uint64)
        high = np.zeros(len(exact_signs), dtype=np.uint64)
        for shift in range(1, 11):
            real = np.zeros(len(exact_signs), dtype=np.int16)
            imag = np.zeros(len(exact_signs), dtype=np.int16)
            for left_position, left_index in position_index.items():
                right_index = position_index.get((left_position + shift) % base.N)
                if right_index is None:
                    continue
                left_real, left_imag = values[left_index]
                right_real, right_imag = values[right_index]
                scalar = exact_signs[:, left_index] * exact_signs[:, right_index]
                real += scalar * (left_real * right_real + left_imag * right_imag)
                imag += scalar * (left_imag * right_real - left_real * right_imag)
            encode(real, imag, shift, low, high)
        pairs = np.rec.fromarrays((low, high), names="low,high")
        unique = np.unique(pairs)
        reachable.update((int(item.low), int(item.high)) for item in unique)
    assert exact_count == 500_992
    return exact_count, reachable


def main() -> None:
    exact_count, reachable = enumerate_b()
    supports = ((0, 2, 4, 10, 12), (0, 2, 4, 13, 15))
    survivors = 0
    for support in supports:
        feasible = bool(a_target_keys(list(support)) & reachable)
        survivors += int(feasible)
        print(
            f"a_support={','.join(map(str, support))} "
            f"seventh_s_soluble={int(feasible)}"
        )
    print(f"exact_b_assignments={exact_count}")
    print(f"seventh_b_residue_fingerprints={len(reachable)}")
    print(f"surviving_orbits={survivors}")
    print("certificate=verified")


if __name__ == "__main__":
    main()
