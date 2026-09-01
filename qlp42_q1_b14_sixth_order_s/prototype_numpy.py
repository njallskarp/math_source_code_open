#!/usr/bin/env python3
"""Direct sixth-order S scan of every QLP-42 q=1, b=14 third-order type."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

G = tuple[int, int]
N = 21
WORD_MASK = (1 << N) - 1
DEPENDENCY_SHA256 = "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependency(directory: Path):
    path = directory.parent / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py"
    assert digest(path) == DEPENDENCY_SHA256
    spec = importlib.util.spec_from_file_location("b14_third_order_dependency", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def active(axis: int, sign: int) -> G:
    value = (1, 1) if axis == 0 else (-1, 1)
    return (-value[0], -value[1]) if sign else value


def target_s(shift: int) -> G:
    if shift == 4:
        return -2, 0
    if shift == 10:
        return 2, 0
    return 0, 0


def sum_targets(case: tuple[int, int, int, int]) -> tuple[G, G]:
    p, q, x, y = case
    return (p + q, q - p), (x + y - 1, y - x)


def phase_patterns(target: G, count: int) -> np.ndarray:
    roots = np.array(
        [active(axis, sign) for axis in (0, 1) for sign in (0, 1)],
        dtype=np.int8,
    )
    result = []
    for indices in product(range(4), repeat=count):
        values = roots[list(indices)]
        if tuple(int(value) for value in values.sum(axis=0)) == target:
            result.append(values)
    assert result
    return np.stack(result)


def encode_complement_fingerprints(positions: list[int], values: np.ndarray) -> set[int]:
    """Encode target_S-PAF(A) in ten independent Gaussian residues modulo 8."""
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
        wanted_real, wanted_imag = target_s(shift)
        fingerprints |= ((wanted_real - real).astype(np.uint64) & 7) << (6 * (shift - 1))
        fingerprints |= ((wanted_imag - imag).astype(np.uint64) & 7) << (
            6 * (shift - 1) + 3
        )
    return {int(value) for value in np.unique(fingerprints)}


def enumerate_b(
    entry,
    target_sums: list[G],
    signs: np.ndarray,
) -> tuple[list[int], list[set[int]]]:
    shifts = [shift for shift in range(1, 11) if (entry.b_word >> shift) & 1]
    assert len(shifts) == 7
    sign_positions = []
    for shift in shifts:
        sign_positions.extend((shift, N - shift))
    sign_positions.append(0)
    assert len(sign_positions) == 15
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
        union = np.logical_or.reduce(selections)
        union_indices = np.flatnonzero(union)
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


def orbit_representatives(
    module, signatures: set[int]
) -> tuple[dict[int, list[int]], dict[int, int]]:
    representatives: dict[int, set[int]] = defaultdict(set)
    labeled: dict[int, int] = defaultdict(int)
    for support in combinations(range(N), 7):
        word = sum(1 << position for position in support)
        signature = module.autocorrelation_signature(word)
        if signature not in signatures:
            continue
        labeled[signature] += 1
        representative = min(module.rotate(word, shift) for shift in range(N))
        representatives[signature].add(representative)
    result = {signature: sorted(words) for signature, words in representatives.items()}
    return result, dict(labeled)


def positions(word: int) -> str:
    return ",".join(str(index) for index in range(N) if (word >> index) & 1)


def main() -> None:
    directory = Path(__file__).resolve().parent
    module = load_dependency(directory)
    labeled, orbit_counts = module.enumerate_a_counts()
    entries = [
        entry
        for entry in module.classify_types(labeled, orbit_counts)
        if entry.b_opposite == 14
    ]
    assert len(entries) == 56
    assert sum(entry.labeled for entry in entries) == 6_762
    assert sum(entry.orbits for entry in entries) == 322

    signatures = {entry.required_signature for entry in entries}
    representatives, direct_labeled = orbit_representatives(module, signatures)
    for entry in entries:
        assert direct_labeled[entry.required_signature] == entry.labeled
        assert len(representatives[entry.required_signature]) == entry.orbits

    a_patterns = []
    b_targets = []
    for case in module.REPRESENTATIVES:
        target_a, target_b = sum_targets(case)
        a_patterns.append(phase_patterns(target_a, 7))
        b_targets.append(target_b)

    masks = np.arange(1 << 15, dtype=np.uint16)[:, None]
    bit_positions = np.arange(15, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bit_positions) & 1).astype(np.int8)).astype(np.int8)

    a_cache: dict[tuple[int, int], set[int]] = {}
    assignment_counts = [set() for _ in module.REPRESENTATIVES]
    fingerprint_counts = [set() for _ in module.REPRESENTATIVES]
    surviving_orbits = [0] * len(module.REPRESENTATIVES)
    surviving_masks = [set() for _ in module.REPRESENTATIVES]
    survivor_rows = []
    for entry_number, entry in enumerate(entries, start=1):
        exact_counts, reachable = enumerate_b(entry, b_targets, signs)
        for case_number in range(len(module.REPRESENTATIVES)):
            assignment_counts[case_number].add(exact_counts[case_number])
            fingerprint_counts[case_number].add(len(reachable[case_number]))
        for a_word in representatives[entry.required_signature]:
            feasible_cases = []
            support = [position for position in range(N) if (a_word >> position) & 1]
            assert len(support) == 7
            for case_number in range(len(module.REPRESENTATIVES)):
                key = (a_word, case_number)
                if key not in a_cache:
                    a_cache[key] = encode_complement_fingerprints(
                        support, a_patterns[case_number]
                    )
                if a_cache[key] & reachable[case_number]:
                    feasible_cases.append(case_number)
                    surviving_orbits[case_number] += 1
                    surviving_masks[case_number].add(entry.b_word)
            if feasible_cases:
                survivor_rows.append(
                    (
                        positions(WORD_MASK ^ entry.b_word ^ 1),
                        positions(a_word),
                        ",".join(map(str, feasible_cases)),
                    )
                )
        print(
            f"completed_b_mask={entry_number}/56;"
            f"a_orbits={entry.orbits};"
            f"current_survivor_rows={len(survivor_rows)}",
            flush=True,
        )

    print(f"input_b_masks={len(entries)}")
    print(f"input_labeled_type_pairs={sum(entry.labeled for entry in entries)}")
    print(f"input_rotation_orbits={sum(entry.orbits for entry in entries)}")
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
    print(f"survivor_rows={len(survivor_rows)}")
    if "--dump-survivors" in sys.argv:
        print("b_equal_positions\ta_opposite_orbit_representative\tfeasible_cases")
        for row in sorted(survivor_rows):
            print(*row, sep="\t")
    print("prototype_certificate=verified")


if __name__ == "__main__":
    main()
