#!/usr/bin/env python3
"""Direct NumPy check of the two singleton b=12 eighth-S incidences."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

N = 21
WORD_MASK = (1 << N) - 1
DEPENDENCY_SHA256 = "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"
A_S_SUPPORT = (0, 1, 2, 3, 4, 5, 10, 13, 16)
B_EQUAL_POSITIONS = (3, 4, 8, 10, 11, 13, 17, 18)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependency(directory: Path):
    path = directory.parent / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py"
    assert digest(path) == DEPENDENCY_SHA256
    spec = importlib.util.spec_from_file_location("b12_h_third_order", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def active(axis: int, sign: int = 0) -> tuple[int, int]:
    value = (1, 1) if axis == 0 else (-1, 1)
    return (-value[0], -value[1]) if sign else value


def encode_paf(positions: list[int], values: np.ndarray, complement: bool) -> np.ndarray:
    """Directly encode ten Gaussian PAF coordinates modulo 8."""
    position_index = {position: index for index, position in enumerate(positions)}
    real_values = values[:, :, 0].astype(np.int16)
    imag_values = values[:, :, 1].astype(np.int16)
    fingerprints = np.zeros(len(values), dtype=np.uint64)
    for shift in range(1, 11):
        real = np.zeros(len(values), dtype=np.int16)
        imag = np.zeros(len(values), dtype=np.int16)
        for left_position, left_index in position_index.items():
            right_index = position_index.get((left_position + shift) % N)
            if right_index is None:
                continue
            left_real = real_values[:, left_index]
            left_imag = imag_values[:, left_index]
            right_real = real_values[:, right_index]
            right_imag = imag_values[:, right_index]
            real += left_real * right_real + left_imag * right_imag
            imag += left_imag * right_real - left_real * right_imag
        if complement:
            real = -2 - real
            imag = -imag
        offset = np.uint64(6 * (shift - 1))
        fingerprints |= (real.astype(np.uint64) & np.uint64(7)) << offset
        fingerprints |= (imag.astype(np.uint64) & np.uint64(7)) << (offset + np.uint64(3))
    return fingerprints


def b_word_and_theta(module):
    equal_word = sum(1 << position for position in B_EQUAL_POSITIONS)
    b_word = WORD_MASK ^ equal_word ^ 1
    assert b_word.bit_count() == 12
    f_word = ((~b_word) & WORD_MASK) & ~1
    b_signature = module.autocorrelation_signature(b_word)
    f_signature = module.autocorrelation_signature(f_word)
    theta = []
    required = 0
    for shift in range(1, 11):
        bit = shift - 1
        tau = (module.TAU_SIGNATURE >> bit) & 1
        b_corr = (b_signature >> bit) & 1
        f_corr = (f_signature >> bit) & 1
        a_corr = f_corr if (b_word >> shift) & 1 else tau ^ b_corr
        required |= a_corr << bit
        theta.append(1 ^ tau ^ b_corr ^ f_corr)
    a_word = sum(1 << position for position in A_S_SUPPORT)
    assert a_word.bit_count() == 9
    assert module.autocorrelation_signature(a_word) == required
    assert module.rotate(a_word, 0) == a_word
    return b_word, tuple(theta)


def enumerate_h_b(b_word: int, theta: tuple[int, ...], center: int):
    shifts = [shift for shift in range(1, 11) if not ((b_word >> shift) & 1)]
    assert len(shifts) == 4
    positions = []
    for shift in shifts:
        positions.extend((shift, N - shift))
    positions.append(0)
    exact = 0
    fingerprint_blocks = []
    masks = np.arange(256, dtype=np.uint16)[:, None]
    bits = np.arange(8, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bits) & 1).astype(np.int8)).astype(np.int8)
    for axes in range(16):
        baseline = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            baseline.extend((active(axis), active(axis ^ theta[shift - 1])))
        baseline_array = np.array(baseline, dtype=np.int8)
        values = signs[:, :, None] * baseline_array[None, :, :]
        center_column = np.broadcast_to(
            np.array((center, 0), dtype=np.int8), (len(values), 1, 2)
        )
        values = np.concatenate((values, center_column), axis=1)
        selection = np.all(values.sum(axis=1) == np.array((1, 0)), axis=1)
        exact += int(selection.sum())
        if selection.any():
            fingerprint_blocks.append(encode_paf(positions, values[selection], False))
    if not fingerprint_blocks:
        return exact, set()
    fingerprints = np.unique(np.concatenate(fingerprint_blocks))
    return exact, {int(value) for value in fingerprints}


def sign_masks(indices: list[int], negatives: int) -> list[int]:
    return [sum(1 << index for index in choice) for choice in combinations(indices, negatives)]


def enumerate_h_a_needed():
    positions = [position for position in range(N) if position not in A_S_SUPPORT]
    assert len(positions) == 12
    needed = set()
    exact_assignments = 0
    direct_paf_evaluations = 0
    for axes in range(1 << 12):
        axis1 = [index for index in range(12) if (axes >> index) & 1]
        axis0 = [index for index in range(12) if not ((axes >> index) & 1)]
        if len(axis0) & 1 or len(axis1) & 1:
            continue
        masks0 = sign_masks(axis0, len(axis0) // 2)
        masks1 = sign_masks(axis1, len(axis1) // 2)
        sign_masks_exact = np.array(
            [left | right for left in masks0 for right in masks1], dtype=np.uint16
        )
        baseline = np.array(
            [active((axes >> index) & 1) for index in range(12)], dtype=np.int8
        )
        bits = np.arange(12, dtype=np.uint16)[None, :]
        signs = (
            1 - 2 * ((sign_masks_exact[:, None] >> bits) & 1).astype(np.int8)
        ).astype(np.int8)
        values = signs[:, :, None] * baseline[None, :, :]
        assert np.all(values.sum(axis=1) == 0)
        fingerprints = encode_paf(positions, values, True)
        needed.update(int(value) for value in fingerprints)
        exact_assignments += len(values)
        direct_paf_evaluations += len(values)
    return exact_assignments, direct_paf_evaluations, needed


def main() -> None:
    directory = Path(__file__).resolve().parent
    module = load_dependency(directory)
    labeled, orbits = module.enumerate_a_counts()
    entries = [
        entry
        for entry in module.classify_types(labeled, orbits)
        if entry.b_opposite == 12
    ]
    assert len(entries) == 98
    global_positive_counts = []
    global_positive_fingerprints = []
    global_negative_counts = []
    for entry in entries:
        positive_count, positive_set = enumerate_h_b(entry.b_word, entry.theta, 1)
        negative_count, negative_set = enumerate_h_b(entry.b_word, entry.theta, -1)
        global_positive_counts.append(positive_count)
        global_positive_fingerprints.append(len(positive_set))
        global_negative_counts.append(negative_count)
        assert not negative_set
    assert min(global_positive_counts) == 608
    assert max(global_positive_counts) == 676
    assert max(global_negative_counts) == 0
    b_word, theta = b_word_and_theta(module)
    positive_exact, positive_fingerprints = enumerate_h_b(b_word, theta, 1)
    negative_exact, negative_fingerprints = enumerate_h_b(b_word, theta, -1)
    assert positive_exact == 608
    assert len(positive_fingerprints) == 304
    assert negative_exact == 0
    assert not negative_fingerprints
    a_exact, direct_paf_evaluations, a_needed = enumerate_h_a_needed()
    assert a_exact == 853_776
    intersection = a_needed & positive_fingerprints
    assert not intersection
    print("input_b_masks=98")
    print("positive_center_h_b_exact_assignment_range=608-676")
    print(
        "positive_center_h_b_fingerprint_range="
        f"{min(global_positive_fingerprints)}-{max(global_positive_fingerprints)}"
    )
    print("negative_center_h_b_exact_assignments=0")
    print("case3_h_center=1")
    print("case3_h_b_exact_assignments=608")
    print("case3_h_b_fingerprints=304")
    print(f"case3_h_a_exact_assignments={a_exact}")
    print(f"case3_h_a_needed_fingerprints={len(a_needed)}")
    print(f"case3_direct_paf_evaluations={direct_paf_evaluations}")
    print("case3_sixth_h_intersection=0")
    print("case4_h_center=-1")
    print("case4_h_b_exact_assignments=0")
    print("case4_sixth_h_intersection=0")
    print("independent_numpy_certificate=verified")


if __name__ == "__main__":
    main()
