#!/usr/bin/env python3
"""Direct NumPy reproduction of the q=1, b=10 seventh-H obstruction."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import numpy as np


DIRECT_SHA256 = "959ea6e001a807b7fc831d559593d012720264bae4e6a42d6e540cd3abd3c039"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_direct(directory: Path):
    path = directory.parent / "qlp42_q1_b10_frontier" / "independent_numpy.py"
    assert digest(path) == DIRECT_SHA256
    spec = importlib.util.spec_from_file_location("b10_h_seventh_direct", path)
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


def read_frontier():
    assert sys.stdin.readline().rstrip("\n") == "a_s_word\tb_s_word"
    rows = []
    for line in sys.stdin:
        a_support, b_word = map(int, line.rstrip("\n").split("\t"))
        rows.append((a_support, b_word))
    assert rows == sorted(rows)
    assert len(rows) == len(set(rows)) == 198
    assert len({a for a, _ in rows}) == 192
    assert len({b for _, b in rows}) == 64
    return rows


def enumerate_h_b_seventh(module, b_word: int, theta: tuple[int, ...]):
    shifts = [shift for shift in range(1, 11) if not ((b_word >> shift) & 1)]
    assert len(shifts) == 5
    positions = [position for shift in shifts for position in (shift, module.N - shift)]
    positions.append(0)
    masks = np.arange(1024, dtype=np.uint16)[:, None]
    bits = np.arange(10, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bits) & 1).astype(np.int8)).astype(np.int8)
    exact = 0
    blocks = []
    for axes in range(32):
        baseline = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            baseline.extend(
                (module.active(axis), module.active(axis ^ theta[shift - 1]))
            )
        values = signs[:, :, None] * np.array(baseline, dtype=np.int8)[None, :, :]
        center = np.broadcast_to(
            np.array((-1, 0), dtype=np.int8), (len(values), 1, 2)
        )
        values = np.concatenate((values, center), axis=1)
        selection = np.all(values.sum(axis=1) == np.array((1, 0)), axis=1)
        exact += int(selection.sum())
        if selection.any():
            blocks.append(encode_paf7(module, positions, values[selection], False))
    assert exact == 3384
    keys = np.unique(fingerprint_keys(np.concatenate(blocks)))
    return exact, keys


def main() -> None:
    directory = Path(__file__).resolve().parent
    module = load_direct(directory)
    dependency = module.load_dependency(directory)
    rows = read_frontier()
    entries, _ = module.reconstruct_inputs(dependency)
    entries_by_word = {entry[0]: entry for entry in entries}

    b_data = {}
    b_fingerprint_counts = []
    for b_word in sorted({b for _, b in rows}):
        _, _, theta = entries_by_word[b_word]
        _, keys = enumerate_h_b_seventh(module, b_word, theta)
        b_data[b_word] = keys
        b_fingerprint_counts.append(len(keys))

    phase_words = module.zero_sum_phase_words10()
    surviving = []
    a_fingerprint_counts = []
    by_support = {}
    for a_support, b_word in rows:
        by_support.setdefault(a_support, []).append(b_word)
    for row_number, (a_support, b_words) in enumerate(sorted(by_support.items()), 1):
        positions = [
            position for position in range(module.N)
            if not ((a_support >> position) & 1)
        ]
        assert len(positions) == 10
        keys = np.unique(fingerprint_keys(
            encode_paf7(module, positions, phase_words, True)
        ))
        a_fingerprint_counts.append(len(keys))
        for b_word in b_words:
            if np.intersect1d(keys, b_data[b_word], assume_unique=True).size:
                surviving.append((a_support, b_word))
        if row_number % 10 == 0:
            print(
                f"completed_a_support={row_number}/192;"
                f"surviving_rows={len(surviving)}",
                file=sys.stderr,
                flush=True,
            )

    assert not surviving
    print("input_sixth_h_orbit_pairs=198")
    print("input_sixth_h_case_incidences=1188")
    print("input_unique_a_supports=192")
    print("input_unique_b_masks=64")
    print("supports_completed=192")
    print("seventh_h_surviving_orbit_pairs=0")
    print("seventh_h_surviving_case_incidences=0")
    print("seventh_h_surviving_b_masks=0")
    print(
        "h_a_seventh_fingerprint_range="
        f"{min(a_fingerprint_counts)}-{max(a_fingerprint_counts)}"
    )
    print(
        "h_b_seventh_fingerprint_range="
        f"{min(b_fingerprint_counts)}-{max(b_fingerprint_counts)}"
    )
    print("h_b_exact_assignments=3384")
    print(f"h_a_exact_assignments={len(by_support) * len(phase_words)}")
    print("independent_direct_numpy_certificate=verified")


if __name__ == "__main__":
    main()
