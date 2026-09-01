#!/usr/bin/env python3
"""Direct eighth-order S closure of the two QLP-42 q=1, b=14 survivors."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import numpy as np

N = 21
WORD_MASK = (1 << N) - 1
SEVENTH_SHA256 = "9c14edb8072390892b900f6d7594bc2e6edb8902efedc55c093ea96d86dcfc2e"
EQUAL_POSITIONS = (5, 6, 10, 11, 15, 16)
A_SUPPORTS = (
    (0, 2, 3, 5, 7, 9, 14),
    (0, 5, 7, 9, 11, 12, 14),
)
CASE_NUMBERS = (3, 4)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_seventh(directory: Path):
    path = directory / "prototype_seventh_s.py"
    assert digest(path) == SEVENTH_SHA256
    spec = importlib.util.spec_from_file_location("b14_seventh_dependency", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def encode_coordinates(
    real: np.ndarray, imag: np.ndarray, shift: int, low: np.ndarray, high: np.ndarray
) -> None:
    """Encode Z[i]/((1+i)^8)=Z[i]/(16) coordinatewise."""
    block = shift - 1
    destination = low if block < 5 else high
    offset = 8 * (block % 5)
    destination |= (real.astype(np.uint64) & 15) << offset
    destination |= (imag.astype(np.uint64) & 15) << (offset + 4)


def encode_a(seventh, sixth, positions: tuple[int, ...], values: np.ndarray):
    position_index = {position: index for index, position in enumerate(positions)}
    real_values = values[:, :, 0].astype(np.int16)
    imag_values = values[:, :, 1].astype(np.int16)
    low = np.zeros(len(values), dtype=np.uint64)
    high = np.zeros(len(values), dtype=np.uint64)
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
        target_real, target_imag = sixth.target_s(shift)
        encode_coordinates(target_real - real, target_imag - imag, shift, low, high)
    pairs = np.unique(np.stack((low, high), axis=1), axis=0)
    return {(int(left), int(right)) for left, right in pairs}


def enumerate_b(entry, targets, signs, active):
    shifts = [shift for shift in range(1, 11) if (entry.b_word >> shift) & 1]
    assert len(shifts) == 7
    sign_positions = []
    for shift in shifts:
        sign_positions.extend((shift, N - shift))
    sign_positions.append(0)
    position_index = {position: index for index, position in enumerate(sign_positions)}
    exact_counts = [0] * len(targets)
    reachable = [set() for _ in targets]
    for axes in range(1 << len(shifts)):
        base = []
        for index, shift in enumerate(shifts):
            common_axis = (axes >> index) & 1
            base.extend(
                (
                    active(common_axis, 0),
                    active(common_axis ^ entry.theta[shift - 1], 0),
                )
            )
        base.append((0, -1))
        base_real = np.array([value[0] for value in base], dtype=np.int16)
        base_imag = np.array([value[1] for value in base], dtype=np.int16)
        real_sums = signs @ base_real
        imag_sums = signs @ base_imag
        selections = [
            (real_sums == target[0]) & (imag_sums == target[1]) for target in targets
        ]
        union_indices = np.flatnonzero(np.logical_or.reduce(selections))
        if not len(union_indices):
            continue
        exact_signs = signs[union_indices]
        low = np.zeros(len(exact_signs), dtype=np.uint64)
        high = np.zeros(len(exact_signs), dtype=np.uint64)
        for shift in range(1, 11):
            real = np.zeros(len(exact_signs), dtype=np.int16)
            imag = np.zeros(len(exact_signs), dtype=np.int16)
            for left_position, left_index in position_index.items():
                right_index = position_index.get((left_position + shift) % N)
                if right_index is None:
                    continue
                left_real, left_imag = base[left_index]
                right_real, right_imag = base[right_index]
                scalar = exact_signs[:, left_index] * exact_signs[:, right_index]
                real += scalar * (left_real * right_real + left_imag * right_imag)
                imag += scalar * (left_imag * right_real - left_real * right_imag)
            encode_coordinates(real, imag, shift, low, high)
        for local_case, selection in enumerate(selections):
            local = selection[union_indices]
            exact_counts[local_case] += int(local.sum())
            pairs = np.unique(np.stack((low[local], high[local]), axis=1), axis=0)
            reachable[local_case].update(
                (int(left), int(right)) for left, right in pairs
            )
    return exact_counts, reachable


def main() -> None:
    directory = Path(__file__).resolve().parent
    seventh = load_seventh(directory)
    sixth = seventh.load_sixth(directory)
    module = sixth.load_dependency(directory)
    labeled, orbit_counts = module.enumerate_a_counts()
    entries = [
        entry
        for entry in module.classify_types(labeled, orbit_counts)
        if entry.b_opposite == 14
    ]
    equal_word = sum(1 << position for position in EQUAL_POSITIONS)
    b_word = WORD_MASK ^ equal_word ^ 1
    candidates = [entry for entry in entries if entry.b_word == b_word]
    assert len(candidates) == 1
    entry = candidates[0]
    assert entry.theta == (0, 0, 0, 1, 0, 0, 0, 0, 0, 1)

    a_words = [sum(1 << position for position in support) for support in A_SUPPORTS]
    assert all(
        module.autocorrelation_signature(word) == entry.required_signature
        for word in a_words
    )
    assert len({min(module.rotate(word, shift) for shift in range(N)) for word in a_words}) == 2

    patterns = []
    targets = []
    for case_number in CASE_NUMBERS:
        target_a, target_b = sixth.sum_targets(module.REPRESENTATIVES[case_number])
        patterns.append(sixth.phase_patterns(target_a, 7))
        targets.append(target_b)

    masks = np.arange(1 << 15, dtype=np.uint16)[:, None]
    bit_positions = np.arange(15, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bit_positions) & 1).astype(np.int8)).astype(np.int8)
    exact_counts, reachable = enumerate_b(entry, targets, signs, sixth.active)

    survivors = []
    print("case\ta_support\ta_phase_assignments\tb_exact_assignments\tb_fingerprints\tintersection")
    for local_case, case_number in enumerate(CASE_NUMBERS):
        for support in A_SUPPORTS:
            a_fingerprints = encode_a(seventh, sixth, support, patterns[local_case])
            intersection = len(a_fingerprints & reachable[local_case])
            if intersection:
                survivors.append((case_number, support))
            print(
                case_number,
                ",".join(map(str, support)),
                len(patterns[local_case]),
                exact_counts[local_case],
                len(reachable[local_case]),
                intersection,
                sep="\t",
            )
    assert not survivors
    print("eighth_order_surviving_orbits=0")
    print("prototype_certificate=verified")


if __name__ == "__main__":
    main()
