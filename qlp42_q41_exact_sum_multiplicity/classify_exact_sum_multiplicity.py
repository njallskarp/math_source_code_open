#!/usr/bin/env python3
"""Exact sign-lift multiplicities after all q=41 fourth-order sum constraints."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
from collections import defaultdict
from math import comb
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ALL_SUMS_SOURCE = (
    HERE.parent / "qlp42_q41_all_sums_fourth_order" / "classify_all_sums.py"
)
ALL_SUMS_SOURCE_SHA256 = "71b701a7bf25cc2e9a9fe83edb80f425b8fd81bcfe89c2c13f4113524d21cb30"
EXPECTED_AXIS_COUNTS = (
    (217_261_758, 10_345_798),
    (193_424_322, 9_210_682),
    (192_720_234, 9_177_154),
    (159_187_665, 7_580_365),
    (159_187_665, 7_580_365),
    (146_998_278, 6_999_918),
)
MASK10 = (1 << 10) - 1
H_TARGET = (1, 0)


def load_all_sums():
    assert hashlib.sha256(ALL_SUMS_SOURCE.read_bytes()).hexdigest() == ALL_SUMS_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location("q41_all_sums", ALL_SUMS_SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def krawtchouk_values(n: int, choose: int) -> np.ndarray:
    values = []
    for marked in range(n + 1):
        total = 0
        for selected_marked in range(choose + 1):
            selected_unmarked = choose - selected_marked
            if selected_marked > marked or selected_unmarked > n - marked:
                continue
            term = comb(marked, selected_marked) * comb(n - marked, selected_unmarked)
            total += -term if selected_marked & 1 else term
        values.append(total)
    return np.array(values, dtype=np.int64)


KRAWTCHOUK = {
    (n, choose): krawtchouk_values(n, choose)
    for n in range(22)
    for choose in range(n + 1)
}


def walsh_in_place(values: np.ndarray) -> None:
    assert values.shape == (7, 1 << 10) and values.dtype == np.int64
    for width in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512):
        view = values.reshape(7, -1, 2, width)
        left = view[:, :, 0, :].copy()
        right = view[:, :, 1, :].copy()
        view[:, :, 0, :] = left + right
        view[:, :, 1, :] = left - right


def target_transform(
    real_count: int,
    imag_count: int,
    target: tuple[int, int],
    marked_real: np.ndarray,
    marked_imag: np.ndarray,
) -> np.ndarray:
    if (real_count - target[0]) & 1 or (imag_count - target[1]) & 1:
        return np.zeros(1 << 10, dtype=np.int64)
    negative_real = (real_count - target[0]) // 2
    negative_imag = (imag_count - target[1]) // 2
    if not (0 <= negative_real <= real_count and 0 <= negative_imag <= imag_count):
        return np.zeros(1 << 10, dtype=np.int64)
    return (
        KRAWTCHOUK[(real_count, negative_real)][marked_real]
        * KRAWTCHOUK[(imag_count, negative_imag)][marked_imag]
    )


def bit_support(values: np.ndarray) -> int:
    result = 0
    for syndrome in np.flatnonzero(values):
        result |= 1 << int(syndrome)
    return result


def exact_b_fibers(previous, q, b) -> np.ndarray:
    columns = q.d_columns(b.mask)
    rows = [0] * 10
    for position, column in enumerate(columns):
        for bit in range(10):
            rows[bit] |= ((column >> bit) & 1) << position
    pullback = np.zeros(1 << 10, dtype=np.uint32)
    for character in range(1, 1 << 10):
        least = character & -character
        pullback[character] = pullback[character ^ least] ^ rows[least.bit_length() - 1]
    marked_one = np.fromiter(
        (int(value & b.mask).bit_count() for value in pullback),
        dtype=np.int16,
        count=1 << 10,
    )
    marked_total = np.fromiter(
        (int(value).bit_count() for value in pullback),
        dtype=np.int16,
        count=1 << 10,
    )
    marked_zero = marked_total - marked_one
    weight = b.weight
    transforms = np.empty((7, 1 << 10), dtype=np.int64)
    transforms[0] = target_transform(
        21 - weight, weight, H_TARGET, marked_zero, marked_one
    )
    for case, target in enumerate(previous.S_B_TARGETS if hasattr(previous, "S_B_TARGETS") else (
        (4, -5), (4, -3), (0, -5), (4, -1), (4, 1), (0, -3)
    )):
        transforms[case + 1] = target_transform(
            weight, 21 - weight, target, marked_one, marked_zero
        )
    walsh_in_place(transforms)
    assert np.all(transforms % (1 << 10) == 0)
    transforms //= 1 << 10
    assert np.all(transforms >= 0)
    assert all(bit_support(transforms[case + 1]) == b.supports[case] for case in range(6))
    even_image = sum(
        1 << syndrome
        for syndrome in range(1 << 10)
        if ((b.image >> syndrome) & 1) and syndrome.bit_count() % 2 == 0
    )
    assert bit_support(transforms[0]) == even_image
    return transforms


def signed_sum_count(pair_count: int, target: int) -> int:
    negative = (pair_count - target) // 2
    if (pair_count - target) & 1 or not 0 <= negative <= pair_count:
        return 0
    return comb(pair_count, negative)


def exact_a_counts(previous, q, a_half: int, signature: int) -> tuple[int, tuple[int, ...]]:
    theta_h, theta_s = q.theta_masks(a_half, signature)
    active_h = (~theta_h) & MASK10
    h_real = (active_h & (~a_half & MASK10)).bit_count()
    h_imag = (active_h & a_half).bit_count()
    h_inactive = 10 - h_real - h_imag
    h_count = (
        signed_sum_count(h_real, 0)
        * signed_sum_count(h_imag, 0)
        * (1 << h_inactive)
    )

    active_s = (~theta_s) & MASK10
    s_real = (active_s & a_half).bit_count()
    s_imag = (active_s & (~a_half & MASK10)).bit_count()
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


def classify(previous, q, grouped):
    systems, affine_data = q.a_systems()
    histograms = [defaultdict(lambda: [0, 0]) for _ in range(6)]
    rank_lifts = defaultdict(lambda: [0, 0])
    weight_lifts = defaultdict(lambda: [0, 0])
    axis_counts = [[0, 0] for _ in range(6)]
    fiber_checks = 0
    a_count_checks = 0
    sampled_masks = previous.sample_masks(grouped)
    sample_digest = hashlib.sha256()
    sample_digest.update(b"axis_word\ta_half\tcase\tlifts\n")

    for signature in sorted(grouped):
        records = previous.a_records(q, systems, affine_data, signature)
        a_counts = []
        for a_half, (_h_value, _s_value, h_possible, s_case_mask) in enumerate(records):
            h_count, s_counts = exact_a_counts(previous, q, a_half, signature)
            assert (h_count > 0) == h_possible
            assert sum((count > 0) << case for case, count in enumerate(s_counts)) == s_case_mask
            a_counts.append((h_count, s_counts))
            a_count_checks += 7

        for b in grouped[signature]:
            fibers = exact_b_fibers(previous, q, b)
            fiber_checks += 7 * (1 << 10)
            for a_half, (h_value, s_value, _h_possible, _s_case_mask) in enumerate(records):
                h_a_count, s_a_counts = a_counts[a_half]
                h_b_count = int(fibers[0, h_value])
                h_factor = h_a_count * h_b_count
                for case in range(6):
                    lifts = h_factor * s_a_counts[case] * int(fibers[case + 1, s_value])
                    if b.mask in sampled_masks:
                        sample_digest.update(
                            f"{b.mask:06x}\t{a_half:03x}\t{case}\t{lifts}\n".encode("ascii")
                        )
                    if lifts == 0:
                        continue
                    axis_counts[case][0] += b.orbit_size
                    axis_counts[case][1] += 1
                    histograms[case][lifts][0] += b.orbit_size
                    histograms[case][lifts][1] += 1
                    rank_lifts[(case, b.rank)][0] += b.orbit_size * lifts
                    rank_lifts[(case, b.rank)][1] += lifts
                    weight_lifts[(case, b.weight)][0] += b.orbit_size * lifts
                    weight_lifts[(case, b.weight)][1] += lifts

    assert tuple(map(tuple, axis_counts)) == EXPECTED_AXIS_COUNTS
    assert histograms[3] == histograms[4]
    return (
        histograms,
        rank_lifts,
        weight_lifts,
        axis_counts,
        fiber_checks,
        a_count_checks,
        sample_digest.hexdigest(),
        len(sampled_masks),
    )


def stream_digest(histograms) -> str:
    digest = hashlib.sha256()
    digest.update(b"case\tlifts_per_axis_pair\tlabeled_axis_pairs\tb_rotation_axis_orbits\n")
    for case, histogram in enumerate(histograms):
        for lifts, (labeled, orbits) in sorted(histogram.items()):
            digest.update(f"{case}\t{lifts}\t{labeled}\t{orbits}\n".encode("ascii"))
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--s-b-binary", type=Path, required=True)
    parser.add_argument("--table", action="store_true")
    args = parser.parse_args()
    previous = load_all_sums()
    q = previous.load_fourth_order()
    grouped, b_digest = previous.read_b_orbits(args.s_b_binary.resolve(), q)
    (
        histograms,
        rank_lifts,
        weight_lifts,
        axis_counts,
        fiber_checks,
        a_checks,
        sample_digest,
        sample_count,
    ) = classify(previous, q, grouped)
    if args.table:
        print("case\tlifts_per_axis_pair\tlabeled_axis_pairs\tb_rotation_axis_orbits")
        for case, histogram in enumerate(histograms):
            for lifts, (labeled, orbits) in sorted(histogram.items()):
                print(case, lifts, labeled, orbits, sep="\t")
        return

    print(f"all_sums_source_sha256={ALL_SUMS_SOURCE_SHA256}")
    print(f"s_b_stream_sha256={b_digest}")
    print(f"exact_b_fiber_entries_checked={fiber_checks}")
    print(f"exact_a_counts_checked={a_checks}")
    for case, histogram in enumerate(histograms):
        labeled_lifts = sum(lifts * counts[0] for lifts, counts in histogram.items())
        orbit_lifts = sum(lifts * counts[1] for lifts, counts in histogram.items())
        print(f"case_{case}_axis_pairs={axis_counts[case][0]},{axis_counts[case][1]}")
        print(f"case_{case}_multiplicity_classes={len(histogram)}")
        print(f"case_{case}_min_max_lifts={min(histogram)},{max(histogram)}")
        print(f"case_{case}_labeled_sign_lifts={labeled_lifts}")
        print(f"case_{case}_b_rotation_sign_lifts={orbit_lifts}")
        ranks = ",".join(
            f"{rank}:{rank_lifts[(case, rank)][0]}:{rank_lifts[(case, rank)][1]}"
            for rank in range(11)
            if rank_lifts[(case, rank)] != [0, 0]
        )
        weights = ",".join(
            f"{weight}:{weight_lifts[(case, weight)][0]}:{weight_lifts[(case, weight)][1]}"
            for weight in range(0, 22, 4)
            if weight_lifts[(case, weight)] != [0, 0]
        )
        print(f"case_{case}_rank_sign_lifts={ranks}")
        print(f"case_{case}_weight_sign_lifts={weights}")
    print(f"multiplicity_table_stream_sha256={stream_digest(histograms)}")
    print(f"sampled_b_rotation_orbits={sample_count}")
    print(f"sample_axis_multiplicity_stream_sha256={sample_digest}")
    print("case_3_case_4_multiplicity_identity=verified")
    print("certificate=verified")


if __name__ == "__main__":
    main()
