#!/usr/bin/env python3
"""Direct NumPy reproduction of the b=12 seventh-order H closure."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
from itertools import combinations
from pathlib import Path

import numpy as np


DIRECT_SHA256 = "baafcf32595790a4522818e1befb033017e4e0e0743f0124e9fa06df486a4688"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_direct(directory: Path):
    path = directory.parent / "qlp42_q1_b12_sixth_order_h" / "independent_numpy.py"
    assert digest(path) == DIRECT_SHA256
    spec = importlib.util.spec_from_file_location("b12_h_seventh_direct", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def encode_paf7(module, positions: list[int], values: np.ndarray, complement: bool):
    """Direct ten-shift encoding r+si -> (r mod 8, r+s mod 16)."""
    position_index = {position: index for index, position in enumerate(positions)}
    real_values = values[:, :, 0].astype(np.int16)
    imag_values = values[:, :, 1].astype(np.int16)
    fingerprints = np.zeros((len(values), 10), dtype=np.uint8)
    for shift in range(1, 11):
        real = np.zeros(len(values), dtype=np.int16)
        imag = np.zeros(len(values), dtype=np.int16)
        for left_position, left_index in position_index.items():
            right_index = position_index.get((left_position + shift) % module.N)
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
        fingerprints[:, shift - 1] = (
            (real.astype(np.uint16) & np.uint16(7))
            | (((real + imag).astype(np.uint16) & np.uint16(15)) << np.uint16(3))
        ).astype(np.uint8)
    return fingerprints


def fingerprint_keys(values: np.ndarray) -> np.ndarray:
    contiguous = np.ascontiguousarray(values)
    return contiguous.view(np.dtype((np.void, 10))).reshape(-1)


def theta_for_b(module, dependency, b_word: int) -> tuple[int, ...]:
    f_word = ((~b_word) & module.WORD_MASK) & ~1
    b_signature = dependency.autocorrelation_signature(b_word)
    f_signature = dependency.autocorrelation_signature(f_word)
    theta = []
    for shift in range(1, 11):
        bit = shift - 1
        tau = (dependency.TAU_SIGNATURE >> bit) & 1
        b_corr = (b_signature >> bit) & 1
        f_corr = (f_signature >> bit) & 1
        theta.append(1 ^ tau ^ b_corr ^ f_corr)
    return tuple(theta)


def read_frontier():
    header = sys.stdin.readline().rstrip("\n")
    assert header == "a_s_word\tb_s_word\tcases"
    rows = []
    for line in sys.stdin:
        a_word, b_word, cases = map(int, line.rstrip("\n").split("\t"))
        assert cases in (1, 4, 5)
        rows.append((a_word, b_word, cases))
    assert len(rows) == 77
    assert sum(cases.bit_count() for _, _, cases in rows) == 79
    assert len({a_word for a_word, _, _ in rows}) == 77
    assert len({b_word for _, b_word, _ in rows}) == 18
    return rows


def enumerate_h_b_seventh(module, b_word: int, theta: tuple[int, ...]):
    shifts = [shift for shift in range(1, 11) if not ((b_word >> shift) & 1)]
    assert len(shifts) == 4
    positions = []
    for shift in shifts:
        positions.extend((shift, module.N - shift))
    positions.append(0)
    masks = np.arange(256, dtype=np.uint16)[:, None]
    bits = np.arange(8, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bits) & 1).astype(np.int8)).astype(np.int8)
    exact = 0
    blocks = []
    for axes in range(16):
        baseline = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            baseline.extend(
                (module.active(axis), module.active(axis ^ theta[shift - 1]))
            )
        baseline_array = np.array(baseline, dtype=np.int8)
        values = signs[:, :, None] * baseline_array[None, :, :]
        center = np.broadcast_to(
            np.array((1, 0), dtype=np.int8), (len(values), 1, 2)
        )
        values = np.concatenate((values, center), axis=1)
        selection = np.all(values.sum(axis=1) == np.array((1, 0)), axis=1)
        exact += int(selection.sum())
        if selection.any():
            blocks.append(encode_paf7(module, positions, values[selection], False))
    keys = np.unique(fingerprint_keys(np.concatenate(blocks)))
    assert 608 <= exact <= 676
    return exact, keys


def sign_masks(indices: list[int], negatives: int) -> list[int]:
    return [sum(1 << index for index in choice) for choice in combinations(indices, negatives)]


def enumerate_h_a_seventh(module, a_s_word: int, b_keys: np.ndarray):
    positions = [position for position in range(module.N) if not (a_s_word >> position) & 1]
    assert len(positions) == 12
    exact = 0
    evaluations = 0
    matched = False
    all_keys = []
    bits = np.arange(12, dtype=np.uint16)[None, :]
    for axes in range(1 << 12):
        axis1 = [index for index in range(12) if (axes >> index) & 1]
        axis0 = [index for index in range(12) if not ((axes >> index) & 1)]
        if len(axis0) & 1 or len(axis1) & 1:
            continue
        masks0 = sign_masks(axis0, len(axis0) // 2)
        masks1 = sign_masks(axis1, len(axis1) // 2)
        exact_masks = np.array(
            [left | right for left in masks0 for right in masks1], dtype=np.uint16
        )
        baseline = np.array(
            [module.active((axes >> index) & 1) for index in range(12)],
            dtype=np.int8,
        )
        signs = (
            1 - 2 * ((exact_masks[:, None] >> bits) & 1).astype(np.int8)
        ).astype(np.int8)
        values = signs[:, :, None] * baseline[None, :, :]
        assert np.all(values.sum(axis=1) == 0)
        keys = fingerprint_keys(encode_paf7(module, positions, values, True))
        if np.intersect1d(keys, b_keys, assume_unique=False).size:
            matched = True
        all_keys.append(keys.copy())
        exact += len(values)
        evaluations += len(values)
    assert exact == 853_776
    return exact, evaluations, len(np.unique(np.concatenate(all_keys))), matched


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    arguments = parser.parse_args()
    directory = Path(__file__).resolve().parent
    module = load_direct(directory)
    dependency = module.load_dependency(directory)
    rows = read_frontier()

    b_data = {}
    b_exact_counts = []
    b_fingerprint_counts = []
    for b_word in sorted({row[1] for row in rows}):
        theta = theta_for_b(module, dependency, b_word)
        exact, keys = enumerate_h_b_seventh(module, b_word, theta)
        b_data[b_word] = keys
        b_exact_counts.append(exact)
        b_fingerprint_counts.append(len(keys))

    surviving_orbits = [0] * 6
    surviving_masks = [set() for _ in range(6)]
    surviving_rows = 0
    exact_assignments = 0
    direct_evaluations = 0
    a_fingerprint_counts = []
    for row_number, (a_word, b_word, cases) in enumerate(rows, start=1):
        exact, evaluations, fingerprint_count, matched = enumerate_h_a_seventh(
            module, a_word, b_data[b_word]
        )
        exact_assignments += exact
        direct_evaluations += evaluations
        a_fingerprint_counts.append(fingerprint_count)
        if matched:
            surviving_rows += 1
            for case_number in (0, 2):
                if (cases >> case_number) & 1:
                    surviving_orbits[case_number] += 1
                    surviving_masks[case_number].add(b_word)
        if not arguments.quiet:
            print(
                f"completed_a_support={row_number}/{len(rows)};"
                f"surviving_rows={surviving_rows}",
                flush=True,
            )

    assert surviving_rows == 0
    assert exact_assignments == 77 * 853_776
    print("input_sixth_h_orbit_incidences=79")
    print("input_sixth_h_rows=77")
    print("input_unique_a_supports=77")
    print("input_unique_b_masks=18")
    print("supports_completed=77")
    print(f"seventh_h_surviving_case0_orbits={surviving_orbits[0]}")
    print(f"seventh_h_surviving_case2_orbits={surviving_orbits[2]}")
    print(f"seventh_h_surviving_case0_masks={len(surviving_masks[0])}")
    print(f"seventh_h_surviving_case2_masks={len(surviving_masks[2])}")
    print(f"seventh_h_surviving_rows={surviving_rows}")
    print(
        "h_a_seventh_fingerprint_range="
        f"{min(a_fingerprint_counts)}-{max(a_fingerprint_counts)}"
    )
    print(
        "h_b_seventh_fingerprint_range="
        f"{min(b_fingerprint_counts)}-{max(b_fingerprint_counts)}"
    )
    print(f"h_b_exact_assignment_range={min(b_exact_counts)}-{max(b_exact_counts)}")
    print(f"h_a_exact_assignments={exact_assignments}")
    print(f"h_a_direct_paf_evaluations={direct_evaluations}")
    print("independent_seventh_numpy_certificate=verified")


if __name__ == "__main__":
    main()
