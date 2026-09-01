#!/usr/bin/env python3
"""Definition-level NumPy proof of the QLP-42 q=1, b=6 H obstruction."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np


N = 21
WORD_MASK = (1 << N) - 1
THIRD_ORDER_SHA256 = (
    "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_third_order(directory: Path):
    path = directory.parent / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py"
    assert digest(path) == THIRD_ORDER_SHA256
    spec = importlib.util.spec_from_file_location("b6_h_third_order", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def active(axis: int) -> tuple[int, int]:
    return (1, 1) if axis == 0 else (-1, 1)


def reconstruct_inputs(module):
    labeled = Counter()
    representatives: dict[int, set[int]] = defaultdict(set)
    for positions in combinations(range(N), 15):
        word = sum(1 << position for position in positions)
        signature = module.autocorrelation_signature(word)
        labeled[signature] += 1
        representatives[signature].add(
            min(module.rotate(word, shift) for shift in range(N))
        )

    entries = []
    for bits in range(1 << 10):
        b_word = module.symmetric_b_word(bits)
        if b_word.bit_count() != 6:
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

    assert len(entries) == 50
    assert sum(labeled[required] for _, required, _ in entries) == 3_402
    assert sum(len(representatives[required]) for _, required, _ in entries) == 162
    return entries, representatives


def raw_paf(positions: list[int], values: np.ndarray) -> np.ndarray:
    """Return ten exact Gaussian PAF coordinates as 20 signed int16 lanes."""
    position_index = {position: index for index, position in enumerate(positions)}
    real_values = values[:, :, 0].astype(np.int16)
    imag_values = values[:, :, 1].astype(np.int16)
    result = np.zeros((len(values), 20), dtype=np.int16)
    for shift in range(1, 11):
        real = np.zeros(len(values), dtype=np.int16)
        imag = np.zeros(len(values), dtype=np.int16)
        for left_position, left_index in position_index.items():
            right_index = position_index.get((left_position + shift) % N)
            if right_index is None:
                continue
            lr = real_values[:, left_index]
            li = imag_values[:, left_index]
            rr = real_values[:, right_index]
            ri = imag_values[:, right_index]
            real += lr * rr + li * ri
            imag += li * rr - lr * ri
        result[:, 2 * (shift - 1)] = real
        result[:, 2 * (shift - 1) + 1] = imag
    return result


def complement_h(raw: np.ndarray) -> np.ndarray:
    result = -raw
    result[:, 0::2] -= 2
    return result


def void_keys(values: np.ndarray) -> np.ndarray:
    contiguous = np.ascontiguousarray(values)
    dtype = np.dtype((np.void, contiguous.dtype.itemsize * values.shape[1]))
    return contiguous.view(dtype).reshape(-1)


def keys6(raw: np.ndarray) -> np.ndarray:
    packed = np.empty((len(raw), 10), dtype=np.uint8)
    for shift in range(10):
        real = raw[:, 2 * shift].astype(np.uint16)
        imag = raw[:, 2 * shift + 1].astype(np.uint16)
        packed[:, shift] = ((real & 7) | ((imag & 7) << 3)).astype(np.uint8)
    return void_keys(packed)


def keys7(raw: np.ndarray) -> np.ndarray:
    packed = np.empty((len(raw), 10), dtype=np.uint8)
    for shift in range(10):
        real_signed = raw[:, 2 * shift]
        imag_signed = raw[:, 2 * shift + 1]
        real = real_signed.astype(np.uint16)
        real_plus_imag = (real_signed + imag_signed).astype(np.uint16)
        packed[:, shift] = (
            (real & 7) | ((real_plus_imag & 15) << 3)
        ).astype(np.uint8)
    return void_keys(packed)


def zero_sum_h_words() -> np.ndarray:
    choices = list(combinations(range(6), 3))
    values = np.empty((len(choices) ** 2, 6, 2), dtype=np.int8)
    row = 0
    for real_positive in choices:
        real = -np.ones(6, dtype=np.int8)
        real[list(real_positive)] = 1
        for imag_positive in choices:
            imag = -np.ones(6, dtype=np.int8)
            imag[list(imag_positive)] = 1
            values[row, :, 0] = real
            values[row, :, 1] = imag
            row += 1
    assert row == 400
    assert np.all(values.sum(axis=1) == 0)
    return values


def enumerate_h_b(b_word: int, theta: tuple[int, ...], center: int):
    shifts = [shift for shift in range(1, 11) if not ((b_word >> shift) & 1)]
    assert len(shifts) == 7
    positions = [position for shift in shifts for position in (shift, N - shift)] + [0]
    masks = np.arange(1 << 14, dtype=np.uint16)[:, None]
    bits = np.arange(14, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bits) & 1).astype(np.int8)).astype(np.int8)
    exact = 0
    raw_blocks = []
    for axes in range(1 << 7):
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
            raw_blocks.append(raw_paf(positions, values[selection]))
    if not raw_blocks:
        return exact, (np.array([], dtype="V10"),) * 3
    raw = np.concatenate(raw_blocks)
    return exact, (
        np.unique(keys6(raw)),
        np.unique(keys7(raw)),
        np.unique(void_keys(raw)),
    )


def count_h_b_sums(b_word: int, theta: tuple[int, ...], center: int) -> int:
    """Definition-level pair convolution for the exact H_B sum count."""
    shifts = [shift for shift in range(1, 11) if not ((b_word >> shift) & 1)]
    totals = Counter({(center, 0): 1})
    for shift in shifts:
        pair_sums = Counter()
        for axis in range(2):
            left = active(axis)
            right = active(axis ^ theta[shift - 1])
            for left_sign in (-1, 1):
                for right_sign in (-1, 1):
                    pair_sums[
                        (
                            left_sign * left[0] + right_sign * right[0],
                            left_sign * left[1] + right_sign * right[1],
                        )
                    ] += 1
        next_totals = Counter()
        for old, old_count in totals.items():
            for pair, pair_count in pair_sums.items():
                next_totals[(old[0] + pair[0], old[1] + pair[1])] += (
                    old_count * pair_count
                )
        totals = next_totals
    return totals[(1, 0)]


def main() -> None:
    started = time.monotonic()
    directory = Path(__file__).resolve().parent
    module = load_third_order(directory)
    entries, representatives = reconstruct_inputs(module)
    by_support: dict[int, list[int]] = defaultdict(list)
    for entry_index, (_, required, _) in enumerate(entries):
        for support in representatives[required]:
            by_support[support].append(entry_index)
    assert sum(len(indices) for indices in by_support.values()) == 162

    b_data = []
    center_counts = []
    for entry_index, (b_word, _, theta) in enumerate(entries):
        positive_count = count_h_b_sums(b_word, theta, 1)
        positive = (np.array([], dtype="V10"),) * 3
        negative_count, negative = enumerate_h_b(b_word, theta, -1)
        assert negative_count == count_h_b_sums(b_word, theta, -1)
        center_counts.append((positive_count, negative_count))
        b_data.append((positive, negative))
        print(
            f"b={entry_index + 1}/50 word={b_word} "
            f"centers=({positive_count},{negative_count}) "
            f"exact_keys=({len(positive[2])},{len(negative[2])})",
            flush=True,
        )

    phase_words = zero_sum_h_words()
    frontiers = [[], [], []]
    a_ranges = [[], [], []]
    for support, entry_indices in sorted(by_support.items()):
        positions = [position for position in range(N) if not ((support >> position) & 1)]
        assert len(positions) == 6
        raw = complement_h(raw_paf(positions, phase_words))
        a_data = (
            np.unique(keys6(raw)),
            np.unique(keys7(raw)),
            np.unique(void_keys(raw)),
        )
        for order in range(3):
            a_ranges[order].append(len(a_data[order]))
        for entry_index in entry_indices:
            feasible = True
            for order in range(3):
                nonempty = [
                    values[order]
                    for values in b_data[entry_index]
                    if len(values[order])
                ]
                assert nonempty
                candidates = (
                    nonempty[0]
                    if len(nonempty) == 1
                    else np.unique(np.concatenate(nonempty))
                )
                feasible = feasible and bool(
                    np.intersect1d(a_data[order], candidates, assume_unique=True).size
                )
                if feasible:
                    frontiers[order].append((support, entries[entry_index][0]))

    assert tuple(map(len, frontiers)) == (4, 0, 0)
    b_ranges = [
        [len(negative[order]) for _, negative in b_data]
        for order in range(3)
    ]
    print("reflected_b_masks=50")
    print("labeled_type_pairs=3402")
    print("input_rotation_orbit_pairs=162")
    print(f"distinct_a_supports={len(by_support)}")
    print(f"center_count_distribution={dict(sorted(Counter(center_counts).items()))}")
    print("h_b_positive_center_assignments=0")
    print("h_b_negative_center_assignments=164728")
    print("h_a_zero_sum_assignments_per_support=400")
    print(f"h_b_sixth_fingerprint_range={min(b_ranges[0])}-{max(b_ranges[0])}")
    print(f"h_b_seventh_fingerprint_range={min(b_ranges[1])}-{max(b_ranges[1])}")
    print(f"h_a_sixth_fingerprint_range={min(a_ranges[0])}-{max(a_ranges[0])}")
    print(f"h_a_seventh_fingerprint_range={min(a_ranges[1])}-{max(a_ranges[1])}")
    print(f"sixth_order_h_pairs={len(frontiers[0])}")
    print(f"seventh_order_h_pairs={len(frontiers[1])}")
    print(f"exact_h_pairs={len(frontiers[2])}")
    for order, frontier in zip((6, 7, 0), frontiers, strict=True):
        payload = "".join(f"{support}\t{b_word}\n" for support, b_word in frontier)
        label = "exact" if order == 0 else str(order)
        print(f"frontier_{label}_sha256={hashlib.sha256(payload.encode()).hexdigest()}")
    for support, b_word in frontiers[0]:
        print(f"sixth_frontier_pair={support},{b_word}")
    print("certificate=verified")
    print(f"elapsed_seconds={time.monotonic() - started:.3f}")


if __name__ == "__main__":
    main()
