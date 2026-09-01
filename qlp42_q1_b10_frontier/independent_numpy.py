#!/usr/bin/env python3
"""Independent direct NumPy check of the q=1, b=10 sixth-H frontier."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np


N = 21
WORD_MASK = (1 << N) - 1
DEPENDENCY_SHA256 = "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependency(directory: Path):
    path = directory.parent / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py"
    assert digest(path) == DEPENDENCY_SHA256
    spec = importlib.util.spec_from_file_location("b10_h_third_order", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def active(axis: int) -> tuple[int, int]:
    return (1, 1) if axis == 0 else (-1, 1)


def encode_paf6(positions: list[int], values: np.ndarray, complement: bool) -> np.ndarray:
    """Directly evaluate and pack the ten Gaussian PAF coordinates modulo 8."""
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


def reconstruct_inputs(module):
    labeled = Counter()
    representatives: dict[int, set[int]] = defaultdict(set)
    for positions in combinations(range(N), 11):
        word = sum(1 << position for position in positions)
        signature = module.autocorrelation_signature(word)
        labeled[signature] += 1
        representatives[signature].add(min(module.rotate(word, shift) for shift in range(N)))

    entries = []
    for bits in range(1 << 10):
        b_word = module.symmetric_b_word(bits)
        if b_word.bit_count() != 10:
            continue
        f_word = ((~b_word) & WORD_MASK) & ~1
        b_signature = module.autocorrelation_signature(b_word)
        f_signature = module.autocorrelation_signature(f_word)
        required = 0
        theta = []
        for shift in range(1, 11):
            bit = shift - 1
            tau = (module.TAU_SIGNATURE >> bit) & 1
            b_corr = (b_signature >> bit) & 1
            f_corr = (f_signature >> bit) & 1
            a_corr = f_corr if (b_word >> shift) & 1 else tau ^ b_corr
            required |= a_corr << bit
            theta.append(1 ^ tau ^ b_corr ^ f_corr)
        if labeled[required]:
            entries.append((b_word, required, tuple(theta)))

    assert len(entries) == 140
    assert sum(labeled[required] for _, required, _ in entries) == 56_490
    assert sum(len(representatives[required]) for _, required, _ in entries) == 2_690
    assert len(set().union(*(representatives[required] for _, required, _ in entries))) == 1_972
    return entries, representatives


def enumerate_h_b6(b_word: int, theta: tuple[int, ...], center: int):
    shifts = [shift for shift in range(1, 11) if not ((b_word >> shift) & 1)]
    assert len(shifts) == 5
    positions = [position for shift in shifts for position in (shift, N - shift)] + [0]
    masks = np.arange(1024, dtype=np.uint16)[:, None]
    bits = np.arange(10, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bits) & 1).astype(np.int8)).astype(np.int8)
    exact = 0
    blocks = []
    for axes in range(32):
        baseline = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            baseline.extend((active(axis), active(axis ^ theta[shift - 1])))
        values = signs[:, :, None] * np.array(baseline, dtype=np.int8)[None, :, :]
        center_column = np.broadcast_to(
            np.array((center, 0), dtype=np.int8), (len(values), 1, 2)
        )
        values = np.concatenate((values, center_column), axis=1)
        selection = np.all(values.sum(axis=1) == np.array((1, 0)), axis=1)
        exact += int(selection.sum())
        if selection.any():
            blocks.append(encode_paf6(positions, values[selection], False))
    if not blocks:
        return exact, set()
    return exact, {int(value) for value in np.unique(np.concatenate(blocks))}


def zero_sum_phase_words10() -> np.ndarray:
    choices = list(combinations(range(10), 5))
    values = np.empty((len(choices) ** 2, 10, 2), dtype=np.int8)
    row = 0
    for real_positive in choices:
        real = -np.ones(10, dtype=np.int8)
        real[list(real_positive)] = 1
        for imag_positive in choices:
            imag = -np.ones(10, dtype=np.int8)
            imag[list(imag_positive)] = 1
            values[row, :, 0] = real
            values[row, :, 1] = imag
            row += 1
    assert row == 63_504
    assert np.all(values.sum(axis=1) == 0)
    return values


def main() -> None:
    directory = Path(__file__).resolve().parent
    module = load_dependency(directory)
    entries, representatives = reconstruct_inputs(module)

    b_fingerprints = []
    b_fingerprint_counts = []
    for b_word, _, theta in entries:
        positive_exact, positive = enumerate_h_b6(b_word, theta, 1)
        negative_exact, negative = enumerate_h_b6(b_word, theta, -1)
        assert positive_exact == 0 and not positive
        assert negative_exact == 3_384
        b_fingerprints.append(negative)
        b_fingerprint_counts.append(len(negative))

    entries_by_support: dict[int, list[int]] = defaultdict(list)
    for entry_index, (_, required, _) in enumerate(entries):
        for support in representatives[required]:
            entries_by_support[support].append(entry_index)
    assert len(entries_by_support) == 1_972
    assert sum(map(len, entries_by_support.values())) == 2_690

    phase_words = zero_sum_phase_words10()
    frontier = []
    surviving_b_masks = set()
    for row_number, (support, entry_indices) in enumerate(sorted(entries_by_support.items()), 1):
        positions = [position for position in range(N) if not ((support >> position) & 1)]
        assert len(positions) == 10
        needed = {int(value) for value in encode_paf6(positions, phase_words, True)}
        for entry_index in entry_indices:
            if needed & b_fingerprints[entry_index]:
                b_word = entries[entry_index][0]
                frontier.append((support, b_word))
                surviving_b_masks.add(b_word)
        if row_number % 100 == 0:
            print(
                f"completed_supports={row_number}/1972;"
                f"surviving_orbit_pairs={len(frontier)}",
                file=sys.stderr,
                flush=True,
            )

    frontier.sort()
    assert len(frontier) == 198
    assert len(surviving_b_masks) == 64
    print("input_b_masks=140")
    print("input_labeled_type_pairs=56490")
    print("input_rotation_orbits_per_case=2690")
    print("unique_a_supports=1972")
    print("h_b_fixed_plus_1_minmax=0,0")
    print("h_b_fixed_minus_1_minmax=3384,3384")
    print(f"h6_b_fingerprint_range={min(b_fingerprint_counts)}-{max(b_fingerprint_counts)}")
    print(f"h6_a_exact_assignments={len(entries_by_support) * len(phase_words)}")
    print("h6_surviving_orbit_pairs=198")
    print("h6_surviving_b_masks=64")
    print("independent_direct_numpy_scan=verified")
    for support, b_word in frontier:
        print(f"frontier_pair={support},{b_word}")


if __name__ == "__main__":
    main()
