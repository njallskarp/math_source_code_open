#!/usr/bin/env python3
"""Definition-level NumPy proof of the QLP-42 q=1, b=8 closure."""

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
THIRD_ORDER_SHA256 = (
    "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"
)
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)
LINEAR_HASH_COEFFICIENTS = np.array(
    (
        0x2CB0F69F4ABEA221, 0x9417034723148989,
        0xDD555950609DFE03, 0xDBAFB150DEB12800,
        0x7E789B2E6C442CB6, 0xF41E5636C7E4F8C4,
        0x0959D150F8FBA7E4, 0xA97316F13CDB9EEA,
        0x74CD8258F9520068, 0x55C74A62E116868B,
        0xD2F4C799A2023CBD, 0xDF98CB79A37B51B9,
        0x396F5885524F3905, 0xAF1D56386CA3B276,
        0xA9FFBE6B5104E85A, 0x6BD0C51B9FD533B3,
        0x980CE91C50AB4B56, 0x28AC395780FE62C5,
        0x768912E3A6BCEDC7, 0x50B3E8C9332C7C88,
    ),
    dtype=np.uint64,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_third_order(directory: Path):
    path = directory.parent / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py"
    assert digest(path) == THIRD_ORDER_SHA256
    spec = importlib.util.spec_from_file_location("b8_exact_third_order", path)
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
    for positions in combinations(range(N), 13):
        word = sum(1 << position for position in positions)
        signature = module.autocorrelation_signature(word)
        labeled[signature] += 1
        representatives[signature].add(
            min(module.rotate(word, shift) for shift in range(N))
        )

    entries = []
    for bits in range(1 << 10):
        b_word = module.symmetric_b_word(bits)
        if b_word.bit_count() != 8:
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

    assert len(entries) == 98
    assert sum(labeled[required] for _, required, _ in entries) == 49_350
    assert sum(len(representatives[required]) for _, required, _ in entries) == 2_350
    assert len(set().union(*(representatives[r] for _, r, _ in entries))) == 1_867
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
    return contiguous.view(np.dtype((np.void, contiguous.dtype.itemsize * values.shape[1]))).reshape(-1)


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
    choices = list(combinations(range(8), 4))
    values = np.empty((len(choices) ** 2, 8, 2), dtype=np.int8)
    row = 0
    for real_positive in choices:
        real = -np.ones(8, dtype=np.int8)
        real[list(real_positive)] = 1
        for imag_positive in choices:
            imag = -np.ones(8, dtype=np.int8)
            imag[list(imag_positive)] = 1
            values[row, :, 0] = real
            values[row, :, 1] = imag
            row += 1
    assert row == 4_900
    assert np.all(values.sum(axis=1) == 0)
    return values


def enumerate_h_b(b_word: int, theta: tuple[int, ...], center: int):
    shifts = [shift for shift in range(1, 11) if not ((b_word >> shift) & 1)]
    assert len(shifts) == 6
    positions = [position for shift in shifts for position in (shift, N - shift)] + [0]
    masks = np.arange(1 << 12, dtype=np.uint16)[:, None]
    bits = np.arange(12, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bits) & 1).astype(np.int8)).astype(np.int8)
    exact = 0
    raw_blocks = []
    for axes in range(1 << 6):
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


def h_frontiers(entries, representatives):
    b_data = []
    positive_counts = []
    negative_counts = []
    b_ranges = [[], [], []]
    for b_word, _, theta in entries:
        positive, data = enumerate_h_b(b_word, theta, 1)
        negative, empty = enumerate_h_b(b_word, theta, -1)
        assert negative == 0 and all(len(values) == 0 for values in empty)
        assert positive in (27_072, 28_496)
        positive_counts.append(positive)
        negative_counts.append(negative)
        b_data.append(data)
        for order in range(3):
            b_ranges[order].append(len(data[order]))

    by_support: dict[int, list[int]] = defaultdict(list)
    for entry_index, (_, required, _) in enumerate(entries):
        for support in representatives[required]:
            by_support[support].append(entry_index)

    phase_words = zero_sum_h_words()
    frontiers = [[], [], []]
    a_ranges = [[], [], []]
    for support, entry_indices in sorted(by_support.items()):
        positions = [position for position in range(N) if not ((support >> position) & 1)]
        assert len(positions) == 8
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
                feasible = feasible and bool(
                    np.intersect1d(
                        a_data[order], b_data[entry_index][order], assume_unique=True
                    ).size
                )
                if feasible:
                    frontiers[order].append((support, entry_index))

    assert len(frontiers[0]) == 739
    assert len(frontiers[1]) == 54
    assert len(frontiers[2]) == 40
    return frontiers, by_support, positive_counts, negative_counts, a_ranges, b_ranges


def sum_targets(case: tuple[int, int, int, int]):
    p, q, x, y = case
    return (p + q, q - p), (x + y - 1, y - x)


def target_s_vector() -> np.ndarray:
    target = np.zeros(20, dtype=np.int16)
    target[2 * (4 - 1)] = -2
    target[2 * (10 - 1)] = 2
    return target


def enumerate_s_b(b_word: int, theta: tuple[int, ...], case_number: int):
    shifts = [shift for shift in range(1, 11) if (b_word >> shift) & 1]
    assert len(shifts) == 4
    positions = [position for shift in shifts for position in (shift, N - shift)] + [0]
    masks = np.arange(1 << 8, dtype=np.uint16)[:, None]
    bits = np.arange(8, dtype=np.uint16)[None, :]
    signs = (1 - 2 * ((masks >> bits) & 1).astype(np.int8)).astype(np.int8)
    center_imag = -1 if case_number in (0, 2, 3) else 1
    target_sum = np.array(sum_targets(CASES[case_number])[1], dtype=np.int16)
    blocks = []
    exact = 0
    for axes in range(1 << 4):
        baseline = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            baseline.extend((active(axis), active(axis ^ theta[shift - 1])))
        values = signs[:, :, None] * np.array(baseline, dtype=np.int8)[None, :, :]
        center = np.broadcast_to(
            np.array((0, center_imag), dtype=np.int8), (len(values), 1, 2)
        )
        values = np.concatenate((values, center), axis=1)
        selection = np.all(values.sum(axis=1) == target_sum, axis=1)
        exact += int(selection.sum())
        if selection.any():
            blocks.append(target_s_vector()[None, :] - raw_paf(positions, values[selection]))
    assert exact == (96 if case_number < 2 else 248)
    return exact, np.unique(void_keys(np.concatenate(blocks)))


def exact_vector_hash(raw: np.ndarray) -> np.ndarray:
    """Linear one-way filter: equal exact vectors always have equal hashes."""
    result = np.zeros(len(raw), dtype=np.uint64)
    for lane, coefficient in enumerate(LINEAR_HASH_COEFFICIENTS):
        result += raw[:, lane].astype(np.int64).astype(np.uint64) * coefficient
    return result


_SIGN_CACHE: dict[tuple[int, int], np.ndarray] = {}


def sign_patterns(length: int, positive: int) -> np.ndarray:
    key = (length, positive)
    if key not in _SIGN_CACHE:
        choices = list(combinations(range(length), positive))
        values = -np.ones((len(choices), length), dtype=np.int8)
        for row, choice in enumerate(choices):
            values[row, list(choice)] = 1
        _SIGN_CACHE[key] = values
    return _SIGN_CACHE[key]


def exact_s_closure(entries, exact_h_frontier):
    entries_by_word = {b_word: (required, theta) for b_word, required, theta in entries}
    pair_words = [(support, entries[index][0]) for support, index in exact_h_frontier]
    b_words = sorted({b_word for _, b_word in pair_words})
    b_required = {}
    b_counts = {}
    b_hashes = {}
    for b_word in b_words:
        theta = entries_by_word[b_word][1]
        for case_number in range(6):
            exact, required = enumerate_s_b(b_word, theta, case_number)
            b_counts[(b_word, case_number)] = exact
            b_required[(b_word, case_number)] = required
            raw_required = required.view(np.int16).reshape(-1, 20)
            b_hashes[(b_word, case_number)] = np.unique(exact_vector_hash(raw_required))

    by_support: dict[int, list[int]] = defaultdict(list)
    for support, b_word in pair_words:
        by_support[support].append(b_word)

    case_targets = [sum_targets(case)[0] for case in CASES]
    assignment_counts = {}
    survivors = []
    hash_false_positives = 0
    for support_number, (support, words) in enumerate(sorted(by_support.items()), 1):
        positions = [position for position in range(N) if (support >> position) & 1]
        assert len(positions) == 13
        for real_target, imag_target in sorted(set(case_targets)):
            cases = [
                case_number
                for case_number, target in enumerate(case_targets)
                if target == (real_target, imag_target)
            ]
            pending = {(word, case_number) for word in words for case_number in cases}
            if not pending:
                continue
            real = sign_patterns(13, (13 + real_target) // 2)
            imag = sign_patterns(13, (13 + imag_target) // 2)
            assignment_counts[(real_target, imag_target)] = len(real) * len(imag)
            for start in range(0, len(real), 64):
                real_block = real[start : start + 64]
                values = np.empty((len(real_block) * len(imag), 13, 2), dtype=np.int8)
                values[:, :, 0] = np.repeat(real_block, len(imag), axis=0)
                values[:, :, 1] = np.tile(imag, (len(real_block), 1))
                raw = raw_paf(positions, values)
                hashes = exact_vector_hash(raw)
                matched_hashes = {}
                for word, case_number in pending:
                    common = np.intersect1d(
                        hashes, b_hashes[(word, case_number)], assume_unique=False
                    )
                    if common.size:
                        matched_hashes[(word, case_number)] = common
                for pair, common in matched_hashes.items():
                    word, case_number = pair
                    candidate_rows = np.isin(hashes, common)
                    exact_keys = np.unique(void_keys(raw[candidate_rows]))
                    if np.intersect1d(
                        exact_keys, b_required[(word, case_number)], assume_unique=True
                    ).size:
                        survivors.append((case_number, support, word))
                        pending.remove(pair)
                    else:
                        hash_false_positives += int(candidate_rows.sum())
                if not pending:
                    break
        if support_number % 10 == 0:
            print(
                f"completed_exact_s_support={support_number}/{len(by_support)};"
                f"surviving_case_incidences={len(survivors)}",
                file=sys.stderr,
                flush=True,
            )

    assert assignment_counts == {
        (1, -1): 2_944_656,
        (3, -3): 1_656_369,
        (5, -3): 920_205,
        (5, -1): 1_226_940,
    }
    assert not survivors
    return pair_words, b_counts, assignment_counts, hash_false_positives


def frontier_sha(rows: list[tuple[int, int]]) -> str:
    stream = "".join(f"{left},{right}\n" for left, right in sorted(rows)).encode()
    return hashlib.sha256(stream).hexdigest()


def main() -> None:
    directory = Path(__file__).resolve().parent
    module = load_third_order(directory)
    entries, representatives = reconstruct_inputs(module)
    frontiers, by_support, positives, negatives, a_ranges, b_ranges = h_frontiers(
        entries, representatives
    )
    sixth = [(support, entries[index][0]) for support, index in frontiers[0]]
    seventh = [(support, entries[index][0]) for support, index in frontiers[1]]
    exact_h, b_counts, assignment_counts, false_positives = exact_s_closure(
        entries, frontiers[2]
    )

    assert sorted(set(positives)) == [27_072, 28_496]
    assert set(negatives) == {0}
    assert len({support for support, _ in sixth}) == 685
    assert len({word for _, word in sixth}) == 54
    assert len({support for support, _ in seventh}) == 54
    assert len({word for _, word in seventh}) == 14
    assert len({support for support, _ in exact_h}) == 40
    assert len({word for _, word in exact_h}) == 11

    print("input_b_masks=98")
    print("input_labeled_type_pairs=49350")
    print("input_rotation_orbits_per_case=2350")
    print(f"input_unique_a_supports={len(by_support)}")
    print("h_b_positive_center_exact_assignment_counts=27072,28496")
    print("h_b_negative_center_exact_assignments=0")
    print("orientation_h_b_center=+1")
    print("h_a_exact_assignments_per_support=4900")
    print(f"sixth_h_orbit_pairs={len(sixth)}")
    print(f"sixth_h_unique_a_supports={len({a for a, _ in sixth})}")
    print(f"sixth_h_unique_b_masks={len({b for _, b in sixth})}")
    print(f"sixth_h_frontier_sha256={frontier_sha(sixth)}")
    print(f"seventh_h_orbit_pairs={len(seventh)}")
    print(f"seventh_h_unique_a_supports={len({a for a, _ in seventh})}")
    print(f"seventh_h_unique_b_masks={len({b for _, b in seventh})}")
    print(f"seventh_h_frontier_sha256={frontier_sha(seventh)}")
    print(f"exact_h_orbit_pairs={len(exact_h)}")
    print(f"exact_h_unique_a_supports={len({a for a, _ in exact_h})}")
    print(f"exact_h_unique_b_masks={len({b for _, b in exact_h})}")
    print(f"exact_h_frontier_sha256={frontier_sha(exact_h)}")
    print(
        "h_a_fingerprint_ranges="
        + ";".join(f"{min(values)}-{max(values)}" for values in a_ranges)
    )
    print(
        "h_b_fingerprint_ranges="
        + ";".join(f"{min(values)}-{max(values)}" for values in b_ranges)
    )
    print(
        "s_b_exact_assignments_by_case="
        + ",".join(str(next(iter({b_counts[(word, c)] for word in {b for _, b in exact_h}}))) for c in range(6))
    )
    print(
        "s_a_exact_assignments_by_target="
        + ";".join(
            f"{target[0]}+{target[1]}i:{count}"
            for target, count in sorted(assignment_counts.items())
        )
    )
    print(f"exact_s_hash_false_positive_rows={false_positives}")
    print("exact_s_surviving_case_incidences=0")
    print("exact_s_surviving_orbit_pairs=0")
    print("q1_b8_shell=excluded")
    print("independent_definition_level_numpy_certificate=verified")


if __name__ == "__main__":
    main()
