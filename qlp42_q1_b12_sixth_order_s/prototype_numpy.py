#!/usr/bin/env python3
"""Direct sixth-order S scan of every QLP-42 q=1, b=12 third-order type."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

N = 21
WORD_MASK = (1 << N) - 1
B14_SHA256 = "96d919fa3170b55ca61c14099a31deefe41ff7063d85f315e25c9d6f6a48d3d2"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_b14(directory: Path):
    path = directory.parent / "qlp42_q1_b14_sixth_order_s" / "prototype_numpy.py"
    assert digest(path) == B14_SHA256
    spec = importlib.util.spec_from_file_location("b12_b14_dependency", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def orbit_representatives(module, signatures: set[int]):
    representatives = defaultdict(set)
    direct_labeled = defaultdict(int)
    for support in combinations(range(N), 9):
        word = sum(1 << position for position in support)
        signature = module.autocorrelation_signature(word)
        if signature not in signatures:
            continue
        direct_labeled[signature] += 1
        representatives[signature].add(
            min(module.rotate(word, shift) for shift in range(N))
        )
    return (
        {signature: sorted(words) for signature, words in representatives.items()},
        dict(direct_labeled),
    )


def enumerate_b(entry, target_sums, signs, active):
    shifts = [shift for shift in range(1, 11) if (entry.b_word >> shift) & 1]
    assert len(shifts) == 6
    sign_positions = []
    for shift in shifts:
        sign_positions.extend((shift, N - shift))
    sign_positions.append(0)
    assert len(sign_positions) == 13
    position_index = {position: index for index, position in enumerate(sign_positions)}
    exact_counts = [0] * len(target_sums)
    reachable = [set() for _ in target_sums]

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
            (real_sums == target[0]) & (imag_sums == target[1])
            for target in target_sums
        ]
        union_indices = np.flatnonzero(np.logical_or.reduce(selections))
        if not len(union_indices):
            continue
        exact_signs = signs[union_indices]
        fingerprints = np.zeros(len(exact_signs), dtype=np.uint64)
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
            fingerprints |= (real.astype(np.uint64) & 7) << (6 * (shift - 1))
            fingerprints |= (imag.astype(np.uint64) & 7) << (6 * (shift - 1) + 3)
        for case_number, selection in enumerate(selections):
            local = selection[union_indices]
            exact_counts[case_number] += int(local.sum())
            reachable[case_number].update(
                int(value) for value in np.unique(fingerprints[local])
            )
    return exact_counts, reachable


def main() -> None:
    directory = Path(__file__).resolve().parent
    b14 = load_b14(directory)
    module = b14.load_dependency(directory)
    labeled, orbit_counts = module.enumerate_a_counts()
    entries = [
        entry
        for entry in module.classify_types(labeled, orbit_counts)
        if entry.b_opposite == 12
    ]
    assert len(entries) == 98
    assert sum(entry.labeled for entry in entries) == 76_377
    assert sum(entry.orbits for entry in entries) == 3_637
    signatures = {entry.required_signature for entry in entries}
    assert len(signatures) == 77
    representatives, direct_labeled = orbit_representatives(module, signatures)
    assert sum(map(len, representatives.values())) == 2_802
    for entry in entries:
        assert direct_labeled[entry.required_signature] == entry.labeled
        assert len(representatives[entry.required_signature]) == entry.orbits

    a_patterns = []
    b_targets = []
    for case in module.REPRESENTATIVES:
        target_a, target_b = b14.sum_targets(case)
        a_patterns.append(b14.phase_patterns(target_a, 9))
        b_targets.append(target_b)
    assert [len(patterns) for patterns in a_patterns] == [
        15_876, 7_056, 7_056, 4_536, 4_536, 3_024,
    ]

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
            assert len(support) == 9
            row_survives = False
            for case_number in range(len(module.REPRESENTATIVES)):
                key = (a_word, case_number)
                if key not in a_cache:
                    a_cache[key] = b14.encode_complement_fingerprints(
                        support, a_patterns[case_number]
                    )
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
    print("input_labeled_type_pairs=76377")
    print("input_rotation_orbits_per_case=3637")
    print(f"unique_a_rotation_representatives={len(a_cache) // 6}")
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
