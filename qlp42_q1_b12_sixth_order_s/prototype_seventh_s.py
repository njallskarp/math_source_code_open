#!/usr/bin/env python3
"""Direct seventh-order S scan of every QLP-42 q=1, b=12 type."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import numpy as np

N = 21
WORD_MASK = (1 << N) - 1
SIXTH_SHA256 = "89badfca8170e0830336b4b7d1e823095966b473b7bf418935e9bae0c5b5af88"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_sixth(directory: Path):
    path = directory / "prototype_numpy.py"
    assert digest(path) == SIXTH_SHA256
    spec = importlib.util.spec_from_file_location("b12_sixth_dependency", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def encode_coordinates(real, imag, shift, low, high):
    block = shift - 1
    destination = low if block < 5 else high
    offset = 7 * (block % 5)
    destination |= (real.astype(np.uint64) & 7) << offset
    destination |= ((real + imag).astype(np.uint64) & 15) << (offset + 3)


def encode_a(b14, positions, values):
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
        target_real, target_imag = b14.target_s(shift)
        encode_coordinates(target_real - real, target_imag - imag, shift, low, high)
    pairs = np.unique(np.stack((low, high), axis=1), axis=0)
    return {(int(left), int(right)) for left, right in pairs}


def enumerate_b(entry, targets, signs, active):
    shifts = [shift for shift in range(1, 11) if (entry.b_word >> shift) & 1]
    assert len(shifts) == 6
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
        for case_number, selection in enumerate(selections):
            local = selection[union_indices]
            exact_counts[case_number] += int(local.sum())
            pairs = np.unique(np.stack((low[local], high[local]), axis=1), axis=0)
            reachable[case_number].update(
                (int(left), int(right)) for left, right in pairs
            )
    return exact_counts, reachable


def main() -> None:
    directory = Path(__file__).resolve().parent
    sixth = load_sixth(directory)
    b14 = sixth.load_b14(directory)
    module = b14.load_dependency(directory)
    labeled, orbit_counts = module.enumerate_a_counts()
    entries = [
        entry
        for entry in module.classify_types(labeled, orbit_counts)
        if entry.b_opposite == 12
    ]
    representatives, direct_labeled = sixth.orbit_representatives(
        module, {entry.required_signature for entry in entries}
    )
    assert len(entries) == 98
    assert sum(entry.orbits for entry in entries) == 3_637
    for entry in entries:
        assert direct_labeled[entry.required_signature] == entry.labeled
        assert len(representatives[entry.required_signature]) == entry.orbits

    a_patterns = []
    b_targets = []
    for case in module.REPRESENTATIVES:
        target_a, target_b = b14.sum_targets(case)
        a_patterns.append(b14.phase_patterns(target_a, 9))
        b_targets.append(target_b)
    masks = np.arange(1 << 13, dtype=np.uint16)[:, None]
    bit_positions = np.arange(13, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bit_positions) & 1).astype(np.int8)).astype(np.int8)

    a_cache = {}
    assignment_counts = [set() for _ in module.REPRESENTATIVES]
    fingerprint_counts = [set() for _ in module.REPRESENTATIVES]
    surviving_orbits = [0] * len(module.REPRESENTATIVES)
    surviving_masks = [set() for _ in module.REPRESENTATIVES]
    survivor_rows = 0
    for entry_number, entry in enumerate(entries, start=1):
        exact_counts, reachable = enumerate_b(entry, b_targets, signs, b14.active)
        for case_number in range(len(module.REPRESENTATIVES)):
            assignment_counts[case_number].add(exact_counts[case_number])
            fingerprint_counts[case_number].add(len(reachable[case_number]))
        for a_word in representatives[entry.required_signature]:
            support = [position for position in range(N) if (a_word >> position) & 1]
            row_survives = False
            for case_number in range(len(module.REPRESENTATIVES)):
                key = (a_word, case_number)
                if key not in a_cache:
                    a_cache[key] = encode_a(b14, support, a_patterns[case_number])
                if a_cache[key] & reachable[case_number]:
                    surviving_orbits[case_number] += 1
                    surviving_masks[case_number].add(entry.b_word)
                    row_survives = True
            survivor_rows += int(row_survives)
        print(
            f"completed_b_mask={entry_number}/98;"
            f"a_orbits={entry.orbits};"
            f"current_survivor_rows={survivor_rows}",
            flush=True,
        )

    print("input_b_masks=98")
    print("input_rotation_orbits_per_case=3637")
    print("case\ta_phase_assignments\tb_exact_assignments\tb_fingerprints\tsurviving_orbits\tsurviving_masks")
    for case_number in range(len(module.REPRESENTATIVES)):
        print(
            case_number,
            len(a_patterns[case_number]),
            ",".join(map(str, sorted(assignment_counts[case_number]))),
            ",".join(map(str, sorted(fingerprint_counts[case_number]))),
            surviving_orbits[case_number],
            len(surviving_masks[case_number]),
            sep="\t",
        )
    print(f"survivor_rows={survivor_rows}")
    print("prototype_certificate=verified")


if __name__ == "__main__":
    main()
