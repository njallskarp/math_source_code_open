#!/usr/bin/env python3
"""Direct-mod-8 sixth-order S scan of QLP-42 q=1, b=16 cases 0--4."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from collections import defaultdict
from itertools import product
from pathlib import Path

import numpy as np

N = 21
WORD_MASK = (1 << N) - 1
PI = (1, 1)
FOURTH_SHA256 = "a5f616a19e241bcdced0962a2843631d1bb13a30de41cfbc05a2c0999e74bacf"
SUM_SHA256 = "d0ecc7b462f6a3e87eb1a3feb0acb13dcd326ddcc83cd84c6aa23c48349fc730"
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str, expected: str):
    assert digest(path) == expected
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def active(axis: int, sign: int) -> tuple[int, int]:
    value = (1, 1) if axis == 0 else (-1, 1)
    return (-value[0], -value[1]) if sign else value


def paf(word: list[tuple[int, int]], shift: int) -> tuple[int, int]:
    real = 0
    imag = 0
    for position, (left_real, left_imag) in enumerate(word):
        right_real, right_imag = word[(position + shift) % N]
        real += left_real * right_real + left_imag * right_imag
        imag += left_imag * right_real - left_real * right_imag
    return real, imag


def target_s(shift: int) -> tuple[int, int]:
    if shift == 4:
        return -2, 0
    if shift == 10:
        return 2, 0
    return 0, 0


def sum_targets(case: tuple[int, int, int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    p, q, x, y = case
    return (p + q, q - p), (x + y - 1, y - x)


def phase_patterns(target: tuple[int, int], count: int) -> list[tuple[tuple[int, int], ...]]:
    roots = tuple(active(axis, sign) for axis in (0, 1) for sign in (0, 1))
    result = []
    for indices in product(range(4), repeat=count):
        values = tuple(roots[index] for index in indices)
        if tuple(map(sum, zip(*values, strict=True))) == target:
            result.append(values)
    return result


def a_targets(positions: list[int], patterns: list[tuple[tuple[int, int], ...]]) -> set[int]:
    targets = set()
    for values in patterns:
        word = [(0, 0)] * N
        for position, value in zip(positions, values, strict=True):
            word[position] = value
        fingerprint = 0
        for shift in range(1, 11):
            a_real, a_imag = paf(word, shift)
            target_real, target_imag = target_s(shift)
            fingerprint |= ((target_real - a_real) & 7) << (6 * (shift - 1))
            fingerprint |= ((target_imag - a_imag) & 7) << (6 * (shift - 1) + 3)
        targets.add(fingerprint)
    return targets


def enumerate_b(
    fourth,
    base_module,
    b_word: int,
    target_sums: list[tuple[int, int]],
    signs: np.ndarray,
) -> tuple[list[int], list[set[int]]]:
    theta = fourth.theta_values(base_module, b_word)
    shifts = [shift for shift in range(1, 11) if (b_word >> shift) & 1]
    assert len(shifts) == 8
    sign_positions = []
    for shift in shifts:
        sign_positions.extend((shift, N - shift))
    sign_positions.append(0)
    position_index = {position: index for index, position in enumerate(sign_positions)}
    exact_counts = [0] * len(target_sums)
    reachable = [set() for _ in target_sums]

    for axes in range(256):
        base = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            base.extend((active(axis, 0), active(axis ^ theta[shift - 1], 0)))
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
                right_position = (left_position + shift) % N
                right_index = position_index.get(right_position)
                if right_index is None:
                    continue
                left_real, left_imag = base[left_index]
                right_real, right_imag = base[right_index]
                scalar = exact_signs[:, left_index] * exact_signs[:, right_index]
                real += scalar * (left_real * right_real + left_imag * right_imag)
                imag += scalar * (left_imag * right_real - left_real * right_imag)
            fingerprints |= (real.astype(np.uint64) & 7) << (6 * (shift - 1))
            fingerprints |= (imag.astype(np.uint64) & 7) << (6 * (shift - 1) + 3)
        for case, selection in enumerate(selections):
            local = selection[union_indices]
            exact_counts[case] += int(local.sum())
            reachable[case].update(int(value) for value in np.unique(fingerprints[local]))
    return exact_counts, reachable


def positions(word: int) -> str:
    return ",".join(str(index) for index in range(N) if (word >> index) & 1)


def main() -> None:
    directory = Path(__file__).resolve().parent
    fourth_path = directory.parent / "qlp42_q1_b16_fourth_order" / "verify_b16_fourth_order.py"
    sum_path = directory.parent / "qlp42_q1_b16_sum_intersection" / "verify_b16_sum_intersection.py"
    fourth = load_module(fourth_path, "all_cases_fourth", FOURTH_SHA256)
    sum_module = load_module(sum_path, "all_cases_sums", SUM_SHA256)
    base_module = fourth.load_dependency()
    survivors = sum_module.orbit_representatives(fourth, base_module)
    assert len(survivors) == 32

    a_patterns = []
    b_targets = []
    for case in CASES:
        target_a, target_b = sum_targets(case)
        patterns = phase_patterns(target_a, 5)
        assert patterns
        a_patterns.append(patterns)
        b_targets.append(target_b)

    grouped = defaultdict(list)
    for result in survivors:
        grouped[result.b_word].append(result)
    assert len(grouped) == 18

    masks = np.arange(1 << 17, dtype=np.uint32)[:, None]
    bit_positions = np.arange(17, dtype=np.uint32)[None, :]
    signs = (1 - 2 * ((masks >> bit_positions) & 1).astype(np.int8)).astype(np.int8)

    case_orbits = [0] * 5
    case_masks = [set() for _ in CASES]
    assignment_counts = [set() for _ in CASES]
    rows = []
    for b_word, results in grouped.items():
        exact_counts, reachable = enumerate_b(fourth, base_module, b_word, b_targets, signs)
        for case in range(5):
            assignment_counts[case].add(exact_counts[case])
        for result in results:
            a_positions = [position for position in range(N) if (result.a_word >> position) & 1]
            assert len(a_positions) == 5
            feasible_cases = []
            residue_counts = []
            for case in range(5):
                targets = a_targets(a_positions, a_patterns[case])
                feasible = bool(targets & reachable[case])
                residue_counts.append(len(reachable[case]))
                if feasible:
                    feasible_cases.append(case)
                    case_orbits[case] += 1
                    case_masks[case].add(b_word)
            equal_word = WORD_MASK ^ b_word ^ 1
            rows.append((
                positions(equal_word),
                positions(result.a_word),
                result.rank,
                ",".join(map(str, feasible_cases)) if feasible_cases else "-",
                ",".join(map(str, residue_counts)),
            ))
    rows.sort()
    if "--dump-table" in sys.argv:
        print(
            "b_equal_positions\ta_opposite_orbit_representative\tfourth_order_rank"
            "\tsixth_s_feasible_cases\tb_residue_counts"
        )
        for row in rows:
            print(*row, sep="\t")
        return
    print(f"input_orbits={len(rows)}")
    print(f"input_b_masks={len(grouped)}")
    print("case\ta_phase_assignments\tb_exact_assignment_counts\tsurviving_orbits\tsurviving_masks")
    for case in range(5):
        print(
            case,
            len(a_patterns[case]),
            ",".join(map(str, sorted(assignment_counts[case]))),
            case_orbits[case],
            len(case_masks[case]),
            sep="\t",
        )
    print("certificate=verified")


if __name__ == "__main__":
    main()
