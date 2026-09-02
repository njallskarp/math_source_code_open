#!/usr/bin/env python3
"""Independent direct-PAF replay of every all-weight terminal frontier row."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
from math import comb
from pathlib import Path

import numpy as np


N = 21
FULL = (1 << N) - 1
WEIGHTS = (0, 4, 8, 12, 16, 20)
EXPECTED_WORDS = {0: 1, 4: 5_985, 8: 203_490, 12: 293_930, 16: 20_349, 20: 21}
EXPECTED_ORBITS = {0: 1, 4: 285, 8: 9_690, 12: 14_000, 16: 969, 20: 1}
PAIR_MASKS = np.arange(1 << 10, dtype=np.uint16)
PAIR_SIGNS = 1 - 2 * ((PAIR_MASKS[:, None] >> np.arange(10)) & 1).astype(np.int16)
S_A_TARGETS = ((1, -1), (3, -3), (3, -3), (5, -1), (5, -1), (5, -3))
S_B_TARGETS = ((4, -5), (4, -3), (0, -5), (4, -1), (4, 1), (0, -3))
CENTERS = ((1, 1), (-1, 1), (-1, -1), (1, -1))


def rotate(mask: int, shift: int) -> int:
    shift %= N
    if shift == 0:
        return mask & FULL
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def reflected_axes(a_half: int) -> int:
    result = 0
    for shift in range(1, 11):
        if (a_half >> (shift - 1)) & 1:
            result |= (1 << shift) | (1 << (N - shift))
    return result


def signature(mask: int) -> int:
    parity = mask.bit_count() & 1
    return sum(
        (parity ^ ((mask & rotate(mask, shift)).bit_count() & 1)) << (shift - 1)
        for shift in range(1, 11)
    )


def theta_masks(a_half: int, e_signature: int) -> tuple[int, int]:
    a = reflected_axes(a_half)
    f = (FULL ^ 1) ^ a
    h = 0
    s = 0
    for shift in range(1, 11):
        a_shift = (a_half >> (shift - 1)) & 1
        f_shift = 1 ^ a_shift
        c_a = (a & rotate(a, shift)).bit_count() & 1
        c_f = (f & rotate(f, shift)).bit_count() & 1
        e = (e_signature >> (shift - 1)) & 1
        tau = int(shift in (4, 10))
        h |= (1 ^ a_shift ^ c_a ^ e) << (shift - 1)
        s |= (1 ^ f_shift ^ c_f ^ e ^ tau) << (shift - 1)
    return h, s


def paf(real: np.ndarray, imag: np.ndarray) -> np.ndarray:
    assert real.dtype == imag.dtype == np.int16
    result = np.empty((real.shape[0], 10, 2), dtype=np.int16)
    for shift in range(1, 11):
        rr = np.roll(real, -shift, axis=1)
        ii = np.roll(imag, -shift, axis=1)
        result[:, shift - 1, 0] = np.sum(real * rr + imag * ii, axis=1, dtype=np.int16)
        result[:, shift - 1, 1] = np.sum(imag * rr - real * ii, axis=1, dtype=np.int16)
    return result


def pi_residues(values: np.ndarray, power: int) -> np.ndarray:
    current = values.astype(np.int32, copy=True)
    result = np.zeros(values.shape[:-1], dtype=np.uint16)
    for place in range(power):
        digit = (current[..., 0] + current[..., 1]) & 1
        result |= digit.astype(np.uint16) << place
        old_real = current[..., 0] - digit
        old_imag = current[..., 1]
        assert np.all(((old_real + old_imag) & 1) == 0)
        current = np.stack(
            ((old_real + old_imag) // 2, (old_imag - old_real) // 2), axis=-1
        )
    return result


def row_set(rows: np.ndarray) -> set[bytes]:
    return {row.tobytes() for row in np.ascontiguousarray(rows)}


def membership(rows: np.ndarray, support: set[bytes]) -> np.ndarray:
    contiguous = np.ascontiguousarray(rows)
    return np.fromiter(
        (row.tobytes() in support for row in contiguous),
        dtype=np.bool_,
        count=contiguous.shape[0],
    )


def expanded_combinations(positions: list[int], weight: int) -> np.ndarray:
    return np.fromiter(
        (
            sum(1 << positions[index] for index in chosen)
            for chosen in combinations(range(len(positions)), weight)
        ),
        dtype=np.uint32,
    )


def negative_masks(axes: int, target: tuple[int, int]) -> np.ndarray:
    imaginary = [index for index in range(N) if (axes >> index) & 1]
    real = [index for index in range(N) if not ((axes >> index) & 1)]
    negative_real = (len(real) - target[0]) // 2
    negative_imag = (len(imaginary) - target[1]) // 2
    assert 0 <= negative_real <= len(real)
    assert 0 <= negative_imag <= len(imaginary)
    assert 2 * negative_real == len(real) - target[0]
    assert 2 * negative_imag == len(imaginary) - target[1]
    real_masks = expanded_combinations(real, negative_real)
    imag_masks = expanded_combinations(imaginary, negative_imag)
    return (real_masks[:, None] | imag_masks[None, :]).reshape(-1)


def unit_arrays(axes: int, signs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    bits = ((signs[:, None] >> np.arange(N)) & 1).astype(np.int16)
    signed = 1 - 2 * bits
    axis_bits = np.array([(axes >> index) & 1 for index in range(N)], dtype=np.int16)
    return signed * (1 - axis_bits), signed * axis_bits


def a_arrays(
    a_half: int, theta: int, component: str, center: tuple[int, int] | None = None
) -> tuple[np.ndarray, np.ndarray]:
    axes = reflected_axes(a_half)
    if component == "S":
        axes = (FULL ^ 1) ^ axes
    real = np.zeros((1 << 10, N), dtype=np.int16)
    imag = np.zeros_like(real)
    if center is not None:
        real[:, 0], imag[:, 0] = center
    for pair in range(10):
        shift = pair + 1
        left = PAIR_SIGNS[:, pair]
        right = left if not ((theta >> pair) & 1) else -left
        if (axes >> shift) & 1:
            imag[:, shift] = left
            imag[:, N - shift] = right
        else:
            real[:, shift] = left
            real[:, N - shift] = right
    return real, imag


def required_h(values: np.ndarray) -> np.ndarray:
    result = -values.astype(np.int16, copy=True)
    result[..., 0] -= 2
    return result


def required_s(values: np.ndarray) -> np.ndarray:
    result = -values.astype(np.int16, copy=True)
    result[:, 3, 0] -= 2
    result[:, 9, 0] += 2
    return result


def parse_stream(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    begin = lines.index("stream_begin")
    end = lines.index("stream_end")
    header = lines[begin + 1].split("\t")
    rows = [
        dict(zip(header, line.split("\t"), strict=True))
        for line in lines[begin + 2 : end]
    ]
    assert len(rows) == 24_946
    return rows


def allowed_cases(weight: int) -> tuple[int, ...]:
    if weight == 0:
        return (2, 5)
    if weight == 20:
        return (3, 4)
    return tuple(range(6))


def verify_manifest(rows: list[dict[str, str]]) -> None:
    by_weight: dict[int, set[int]] = {weight: set() for weight in WEIGHTS}
    orbit_counts: Counter[tuple[int, int]] = Counter()
    for row in rows:
        weight = int(row["weight"])
        value = int(row["b_axis"], 16)
        assert weight in WEIGHTS and value.bit_count() == weight
        assert value == min(rotate(value, shift) for shift in range(N))
        orbit = {rotate(value, shift) for shift in range(N)}
        assert len(orbit) == int(row["orbit_size"])
        assert by_weight[weight].isdisjoint(orbit)
        by_weight[weight].update(orbit)
        orbit_counts[(weight, len(orbit))] += 1
    for weight in WEIGHTS:
        assert len(by_weight[weight]) == EXPECTED_WORDS[weight]
        assert sum(1 for row in rows if int(row["weight"]) == weight) == EXPECTED_ORBITS[weight]
    assert orbit_counts[(12, 7)] == 5
    assert orbit_counts[(12, 21)] == 13_995


def build_a_needed(e_signature: int) -> list[np.ndarray]:
    result: list[np.ndarray] = []
    for a_half in range(1 << 10):
        theta_h, _ = theta_masks(a_half, e_signature)
        real, imag = a_arrays(a_half, theta_h, "H")
        keep = (np.sum(real, axis=1) == 0) & (np.sum(imag, axis=1) == 0)
        result.append(required_h(paf(real[keep], imag[keep])))
    return result


def exact_h_masks(row: dict[str, str], a_needed: list[np.ndarray]) -> list[int]:
    weight = int(row["weight"])
    b_axis = int(row["b_axis"], 16)
    e_signature = int(row["signature"], 16)
    assert b_axis.bit_count() == weight and signature(b_axis) == e_signature
    b_signs = negative_masks(b_axis, (1, 0))
    expected_signs = comb(weight, weight // 2) * comb(N - weight, (20 - weight) // 2)
    assert b_signs.size == expected_signs
    b_real, b_imag = unit_arrays(b_axis, b_signs)
    b_values = paf(b_real, b_imag)

    deepened = int(row["b12"]) != 0
    masks = [0] * 9
    for power in range(4, 13):
        support = row_set(pi_residues(b_values, power))
        if power <= 7 or deepened:
            assert len(support) == int(row[f"b{power}"])
        for a_half, needed in enumerate(a_needed):
            if np.any(membership(pi_residues(needed, power), support)):
                masks[power - 4] |= 1 << a_half
    return masks


def exact_s_support(row: dict[str, str], case_index: int) -> set[bytes]:
    b_axis = int(row["b_axis"], 16)
    s_b_axes = FULL ^ b_axis
    b_signs = negative_masks(s_b_axes, S_B_TARGETS[case_index])
    b_real, b_imag = unit_arrays(s_b_axes, b_signs)
    return row_set(pi_residues(paf(b_real, b_imag), 12))


def exact_s_survives(
    row: dict[str, str], a_half: int, case_index: int, b_support: set[bytes]
) -> bool:
    e_signature = int(row["signature"], 16)
    _, theta_s = theta_masks(a_half, e_signature)
    for center in CENTERS:
        real, imag = a_arrays(a_half, theta_s, "S", center)
        target = S_A_TARGETS[case_index]
        keep = (np.sum(real, axis=1) == target[0]) & (np.sum(imag, axis=1) == target[1])
        if not np.any(keep):
            continue
        needed = required_s(paf(real[keep], imag[keep]))
        if np.any(membership(pi_residues(needed, 12), b_support)):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream", type=Path, required=True)
    args = parser.parse_args()
    rows = parse_stream(args.stream)
    verify_manifest(rows)

    frontier = [row for row in rows if int(row["a12_mask"], 16)]
    controls: list[dict[str, str]] = []
    for weight in WEIGHTS:
        empty = [
            row
            for row in rows
            if int(row["weight"]) == weight and not int(row["a12_mask"], 16)
        ]
        if empty:
            step = max(1, len(empty) // 2)
            controls.extend(empty[::step][:2])
    audited = frontier + controls

    by_signature: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in audited:
        by_signature[int(row["signature"], 16)].append(row)
    for e_signature, group in sorted(by_signature.items()):
        a_needed = build_a_needed(e_signature)
        for row in group:
            masks = exact_h_masks(row, a_needed)
            for power, mask in zip(range(4, 13), masks, strict=True):
                assert mask == int(row[f"a{power}_mask"], 16), (
                    row["weight"],
                    row["b_axis"],
                    power,
                )

    case_tests = 0
    survivors = 0
    frontier_counts: Counter[int] = Counter()
    frontier_axis_counts: Counter[int] = Counter()
    for row in frontier:
        weight = int(row["weight"])
        frontier_counts[weight] += 1
        a_mask = int(row["a12_mask"], 16)
        frontier_axis_counts[weight] += a_mask.bit_count()
        cases = allowed_cases(weight)
        s_supports = {case: exact_s_support(row, case) for case in cases}
        observed_masks = {case: 0 for case in cases}
        for a_half in range(1 << 10):
            if not ((a_mask >> a_half) & 1):
                continue
            for case_index in cases:
                case_tests += 1
                if exact_s_survives(row, a_half, case_index, s_supports[case_index]):
                    observed_masks[case_index] |= 1 << a_half
                    survivors += 1
        for case_index in range(6):
            expected = int(row[f"hs{case_index}_mask"], 16)
            assert expected == observed_masks.get(case_index, 0)

    assert survivors == 0
    assert frontier_counts == Counter({12: 116, 8: 81, 16: 12, 4: 9, 0: 1})
    assert frontier_axis_counts == Counter({12: 252, 8: 198, 4: 42, 16: 24, 0: 4})

    print("implementation=independent_numpy_direct_paf_frontier")
    print("stream_b_rotation_orbits=24946")
    print("stream_labeled_b_axes=524776")
    print("weight12_short_orbits=5")
    print("weight12_full_orbits=13995")
    for weight in WEIGHTS:
        print(f"weight_{weight}_exact_h_frontier_b_orbits={frontier_counts[weight]}")
        print(f"weight_{weight}_exact_h_frontier_axis_orbits={frontier_axis_counts[weight]}")
    print(f"fully_recomputed_frontier_b_orbits={len(frontier)}")
    print(f"fully_recomputed_empty_b_orbits={len(controls)}")
    print("recomputed_orders=4,5,6,7,8,9,10,11,12")
    print(f"exact_hs_case_tests={case_tests}")
    print(f"exact_hs_survivors={survivors}")
    print("q41_all_weight_exclusion=verified")


if __name__ == "__main__":
    main()
