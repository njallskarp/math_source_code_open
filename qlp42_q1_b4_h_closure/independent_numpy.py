#!/usr/bin/env python3
"""Definition-level NumPy proof of the QLP-42 q=1, b=4 H obstruction."""

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
B6_NUMPY_SHA256 = "b1ed67c2f728dc5f7bfc22bf1cbbcb925737a65825a046984102b4911583bd62"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_b6(directory: Path):
    path = directory.parent / "qlp42_q1_b6_h_closure" / "independent_numpy.py"
    assert digest(path) == B6_NUMPY_SHA256
    spec = importlib.util.spec_from_file_location("b4_h_b6_base", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def reconstruct_inputs(base, third):
    labeled = Counter()
    representatives: dict[int, set[int]] = defaultdict(set)
    for positions in combinations(range(N), 17):
        word = sum(1 << position for position in positions)
        signature = third.autocorrelation_signature(word)
        labeled[signature] += 1
        representatives[signature].add(
            min(third.rotate(word, shift) for shift in range(N))
        )

    entries = []
    for bits in range(1 << 10):
        b_word = third.symmetric_b_word(bits)
        if b_word.bit_count() != 4:
            continue
        f_word = ((~b_word) & WORD_MASK) & ~1
        b_signature = third.autocorrelation_signature(b_word)
        f_signature = third.autocorrelation_signature(f_word)
        required = 0
        theta = []
        for shift in range(1, 11):
            bit = shift - 1
            tau = (third.TAU_SIGNATURE >> bit) & 1
            b_corr = (b_signature >> bit) & 1
            f_corr = (f_signature >> bit) & 1
            a_corr = f_corr if (b_word >> shift) & 1 else tau ^ b_corr
            required |= a_corr << bit
            theta.append(1 ^ tau ^ b_corr ^ f_corr)
        if labeled[required]:
            entries.append((b_word, required, tuple(theta)))

    assert len(entries) == 10
    assert sum(labeled[required] for _, required, _ in entries) == 420
    assert sum(len(representatives[required]) for _, required, _ in entries) == 20
    return entries, representatives


def zero_sum_h_words() -> np.ndarray:
    choices = list(combinations(range(4), 2))
    values = np.empty((len(choices) ** 2, 4, 2), dtype=np.int8)
    row = 0
    for real_positive in choices:
        real = -np.ones(4, dtype=np.int8)
        real[list(real_positive)] = 1
        for imag_positive in choices:
            imag = -np.ones(4, dtype=np.int8)
            imag[list(imag_positive)] = 1
            values[row, :, 0] = real
            values[row, :, 1] = imag
            row += 1
    assert row == 36
    assert np.all(values.sum(axis=1) == 0)
    return values


def enumerate_h_b(base, b_word: int, theta: tuple[int, ...], center: int):
    shifts = [shift for shift in range(1, 11) if not ((b_word >> shift) & 1)]
    assert len(shifts) == 8
    positions = [position for shift in shifts for position in (shift, N - shift)] + [0]
    masks = np.arange(1 << 16, dtype=np.uint16)[:, None]
    bits = np.arange(16, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bits) & 1).astype(np.int8)).astype(np.int8)
    exact = 0
    raw_blocks = []
    for axes in range(1 << 8):
        baseline = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            baseline.extend(
                (base.active(axis), base.active(axis ^ theta[shift - 1]))
            )
        values = signs[:, :, None] * np.array(baseline, dtype=np.int8)[None, :, :]
        center_column = np.broadcast_to(
            np.array((center, 0), dtype=np.int8), (len(values), 1, 2)
        )
        values = np.concatenate((values, center_column), axis=1)
        selection = np.all(values.sum(axis=1) == np.array((1, 0)), axis=1)
        exact += int(selection.sum())
        if selection.any():
            raw_blocks.append(base.raw_paf(positions, values[selection]))
    raw = np.concatenate(raw_blocks)
    return exact, np.unique(base.keys6(raw)), np.unique(base.keys7(raw))


def main() -> None:
    started = time.monotonic()
    directory = Path(__file__).resolve().parent
    base = load_b6(directory)
    third = base.load_third_order(directory.parent / "qlp42_q1_b6_h_closure")
    entries, representatives = reconstruct_inputs(base, third)

    phase_words = zero_sum_h_words()
    by_support = {}
    for _, required, _ in entries:
        for support in representatives[required]:
            if support in by_support:
                continue
            positions = [p for p in range(N) if not ((support >> p) & 1)]
            assert len(positions) == 4
            raw = base.complement_h(base.raw_paf(positions, phase_words))
            by_support[support] = (
                np.unique(base.keys6(raw)),
                np.unique(base.keys7(raw)),
            )

    frontiers = [set(), set()]
    center_counts = []
    b_ranges = [[], []]
    for entry_index, (b_word, required, theta) in enumerate(entries):
        positive = base.count_h_b_sums(b_word, theta, 1)
        negative = base.count_h_b_sums(b_word, theta, -1)
        center_counts.append((positive, negative))
        assert (positive == 0) != (negative == 0)
        center = 1 if positive else -1
        exact, values6, values7 = enumerate_h_b(base, b_word, theta, center)
        assert exact == max(positive, negative)
        b_ranges[0].append(len(values6))
        b_ranges[1].append(len(values7))
        for support in representatives[required]:
            if np.intersect1d(by_support[support][0], values6, assume_unique=True).size:
                frontiers[0].add((support, b_word))
            if np.intersect1d(by_support[support][1], values7, assume_unique=True).size:
                frontiers[1].add((support, b_word))
        print(
            f"b={entry_index + 1}/10 word={b_word} centers=({positive},{negative}) "
            f"fingerprints=({len(values6)},{len(values7)}) "
            f"frontiers=({len(frontiers[0])},{len(frontiers[1])})",
            flush=True,
        )

    ordered = [sorted(frontier) for frontier in frontiers]
    assert ordered == [[(503807, 21120), (524207, 21120)], []]
    a_ranges = [
        [len(values[order]) for values in by_support.values()]
        for order in range(2)
    ]
    print("reflected_b_masks=10")
    print("labeled_type_pairs=420")
    print("input_rotation_orbit_pairs=20")
    print(f"distinct_a_supports={len(by_support)}")
    print(f"center_count_distribution={dict(sorted(Counter(center_counts).items()))}")
    print("h_b_positive_center_assignments=1317824")
    print("h_b_negative_center_assignments=0")
    print("h_a_zero_sum_assignments_per_support=36")
    print(f"h_b_sixth_fingerprint_range={min(b_ranges[0])}-{max(b_ranges[0])}")
    print(f"h_b_seventh_fingerprint_range={min(b_ranges[1])}-{max(b_ranges[1])}")
    print(f"h_a_sixth_fingerprint_range={min(a_ranges[0])}-{max(a_ranges[0])}")
    print(f"h_a_seventh_fingerprint_range={min(a_ranges[1])}-{max(a_ranges[1])}")
    print(f"sixth_order_h_pairs={len(ordered[0])}")
    print(f"seventh_order_h_pairs={len(ordered[1])}")
    for order, frontier in zip((6, 7), ordered, strict=True):
        payload = "".join(f"{support}\t{b_word}\n" for support, b_word in frontier)
        print(f"frontier_{order}_sha256={hashlib.sha256(payload.encode()).hexdigest()}")
        for support, b_word in frontier:
            print(f"frontier_{order}_pair={support},{b_word}")
    print("certificate=verified")
    print(f"elapsed_seconds={time.monotonic() - started:.3f}")


if __name__ == "__main__":
    main()
