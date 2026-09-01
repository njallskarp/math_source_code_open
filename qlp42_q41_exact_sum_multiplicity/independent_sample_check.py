#!/usr/bin/env python3
"""Independent sampled check for exact sign-lift multiplicities.

This verifier deliberately replaces the main program's Krawtchouk/Walsh
calculation by fixed-cardinality subset-XOR dynamic programming.  It also
brute-forces selected A-axis sign assignments.
"""

from __future__ import annotations

import hashlib
import importlib.util
import math
import pathlib
import sys

import numpy as np


HERE = pathlib.Path(__file__).resolve().parent
PREVIOUS = HERE.parent / "qlp42_q41_all_sums_fourth_order" / "independent_sample_check.py"
PREVIOUS_SHA256 = "7e5eeb2d68628ef4aad8c431d81f05431b66650fddd299984b7215cc1884b4a0"
EXPECTED_DIGEST = "d9f650cf40abd0460e806d5ebf78cf47941d48b6beffa3730a5bc74f91af9859"
XOR_INDEX = np.arange(1024, dtype=np.int64)


def load_previous():
    data = PREVIOUS.read_bytes()
    assert hashlib.sha256(data).hexdigest() == PREVIOUS_SHA256
    spec = importlib.util.spec_from_file_location("independent_all_sums", PREVIOUS)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def subset_counts_by_size(columns: list[int]) -> np.ndarray:
    """Count subsets by cardinality and XOR, by direct subset DP."""
    dp = np.zeros((len(columns) + 1, 1024), dtype=np.int64)
    dp[0, 0] = 1
    used = 0
    for column in columns:
        used += 1
        for size in range(used, 0, -1):
            dp[size] += dp[size - 1, XOR_INDEX ^ column]
    return dp


def xor_convolve(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    out = np.zeros(1024, dtype=np.int64)
    for x in np.flatnonzero(left):
        out[XOR_INDEX ^ int(x)] += int(left[x]) * right
    return out


def exact_fiber(
    columns: list[int], mask: int, real_on_one: bool, target: tuple[int, int]
) -> np.ndarray:
    real: list[int] = []
    imag: list[int] = []
    for i, column in enumerate(columns):
        bit = (mask >> i) & 1
        (real if bool(bit) == real_on_one else imag).append(column)
    real_dp = subset_counts_by_size(real)
    imag_dp = subset_counts_by_size(imag)
    negative_real = (len(real) - target[0]) // 2
    negative_imag = (len(imag) - target[1]) // 2
    if (
        (len(real) - target[0]) & 1
        or (len(imag) - target[1]) & 1
        or not 0 <= negative_real <= len(real)
        or not 0 <= negative_imag <= len(imag)
    ):
        return np.zeros(1024, dtype=np.int64)
    return xor_convolve(real_dp[negative_real], imag_dp[negative_imag])


def signed_sum_count(pair_count: int, target: int) -> int:
    negative = (pair_count - target) // 2
    if (pair_count - target) & 1 or not 0 <= negative <= pair_count:
        return 0
    return math.comb(pair_count, negative)


def exact_a_counts(previous, a: int, signature: int) -> tuple[int, tuple[int, ...]]:
    theta_h, theta_s = previous.theta_masks(a, signature)
    active_h = (~theta_h) & previous.MASK10
    h_real = (active_h & (~a & previous.MASK10)).bit_count()
    h_imag = (active_h & a).bit_count()
    h_inactive = 10 - h_real - h_imag
    h_count = (
        signed_sum_count(h_real, 0)
        * signed_sum_count(h_imag, 0)
        * (1 << h_inactive)
    )

    active_s = (~theta_s) & previous.MASK10
    s_real = (active_s & a).bit_count()
    s_imag = (active_s & (~a & previous.MASK10)).bit_count()
    s_inactive = 10 - s_real - s_imag
    s_counts = []
    for target in previous.S_A_TARGETS:
        count = 0
        for center in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
            rr = target[0] - center[0]
            ri = target[1] - center[1]
            assert rr % 2 == ri % 2 == 0
            count += (
                signed_sum_count(s_real, rr // 2)
                * signed_sum_count(s_imag, ri // 2)
                * (1 << s_inactive)
            )
        s_counts.append(count)
    return h_count, tuple(s_counts)


def brute_h_a(previous, a: int, signature: int) -> int:
    theta_h, _ = previous.theta_masks(a, signature)
    base = previous.a_word(a, theta_h, "H")
    total = 0
    for flips in range(1 << 10):
        word = base.copy()
        for pair in range(10):
            if (flips >> pair) & 1:
                shift = pair + 1
                word[shift] = previous.neg(word[shift])
                word[previous.N - shift] = previous.neg(word[previous.N - shift])
        total += previous.word_sum(word) == (0, 0)
    return total


def brute_s_a(previous, a: int, signature: int, target: tuple[int, int]) -> int:
    _, theta_s = previous.theta_masks(a, signature)
    total = 0
    for center in range(4):
        base = previous.a_word(a, theta_s, "S", center)
        for flips in range(1 << 10):
            word = base.copy()
            for pair in range(10):
                if (flips >> pair) & 1:
                    shift = pair + 1
                    word[shift] = previous.neg(word[shift])
                    word[previous.N - shift] = previous.neg(word[previous.N - shift])
            total += previous.word_sum(word) == target
    return total


def main() -> None:
    previous = load_previous()
    records = previous.parse_sample()
    digest = hashlib.sha256()
    digest.update(b"axis_word\ta_half\tcase\tlifts\n")
    pair_count = 0
    multiplicity_count = 0

    audit_pairs: list[tuple[int, int]] = []
    audit_indices = {0, 7, 31, 63, 95, 127, 131}
    for record_index, record in enumerate(records):
        mask, _orbit_size, _weight, _rank, signature, expected_masks = record
        columns = list(previous.d_columns(mask))
        h_b = exact_fiber(columns, mask, False, (1, 0))
        s_b = [
            exact_fiber(columns, mask, True, target)
            for target in previous.S_B_TARGETS
        ]
        assert np.array_equal(s_b[3], s_b[4])

        h_b_word = previous.b_word(mask, "H")
        s_b_word = previous.b_word(mask, "S")
        h_b_pafs = [previous.paf(h_b_word, shift) for shift in range(1, 11)]
        s_b_pafs = [previous.paf(s_b_word, shift) for shift in range(1, 11)]
        for a in range(1024):
            theta_h, theta_s = previous.theta_masks(a, signature)
            h_axis = previous.a_word(a, theta_h, "H")
            s_axis = previous.a_word(a, theta_s, "S", 0)
            h_residual = previous.residual_syndrome(h_axis, h_b_pafs, "H")
            s_residual = previous.residual_syndrome(s_axis, s_b_pafs, "S")
            h_a, s_a = exact_a_counts(previous, a, signature)
            values: list[int] = []
            for case in range(6):
                values.append(
                    h_a
                    * int(h_b[h_residual])
                    * s_a[case]
                    * int(s_b[case][s_residual])
                )
            expected = sum(
                (((expected_masks[case] >> a) & 1) << case) for case in range(6)
            )
            actual = sum((value > 0) << case for case, value in enumerate(values))
            assert actual == expected
            assert values[3] == values[4]
            for case, value in enumerate(values):
                digest.update(f"{mask:06x}\t{a:03x}\t{case}\t{value}\n".encode())
            pair_count += 1
            multiplicity_count += len(values)

            if record_index in audit_indices and a in (0, 1, 17, 341, 682):
                if len(audit_pairs) < 32:
                    audit_pairs.append((signature, a))

    for signature, a in audit_pairs:
        h_count, s_counts = exact_a_counts(previous, a, signature)
        assert h_count == brute_h_a(previous, a, signature)
        for target in previous.S_A_TARGETS:
            case = previous.S_A_TARGETS.index(target)
            assert s_counts[case] == brute_s_a(previous, a, signature, target)

    observed = digest.hexdigest()
    assert observed == EXPECTED_DIGEST
    print(f"sampled_b_rotation_orbits={len(records)}")
    print(f"sampled_axis_pairs={pair_count}")
    print(f"sampled_case_multiplicities={multiplicity_count}")
    print(f"direct_fixed_cardinality_b_fibers={len(records) * 7 * 1024}")
    print(f"brute_a_multiplicity_audits={len(audit_pairs)}")
    print("all_six_positive_masks_match=verified")
    print("case_3_case_4_multiplicity_identity=verified")
    print(f"sample_axis_multiplicity_stream_sha256={observed}")
    print("independent_sample_certificate=verified")


if __name__ == "__main__":
    main()
