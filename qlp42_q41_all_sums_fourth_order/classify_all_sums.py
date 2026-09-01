#!/usr/bin/env python3
"""Exact four-sum intersection of the QLP-42 q=41 fourth-order layer."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOURTH_ORDER = (
    HERE.parent / "qlp42_q41_fourth_order_rank" / "verify_q41_fourth_order_rank.py"
)
S_B_SOURCE = HERE.parent / "qlp42_q41_s_b_syndromes" / "classify_s_b_syndromes.cpp"
FOURTH_ORDER_SHA256 = "cefc2f614980396aaecc9894733e3e8840658966b5d33e1ae6811a7bcc4b3d69"
S_B_SOURCE_SHA256 = "066d6eccfc32041a99eb8b2b095f7f4614d9c2f3be7be5ff54824dd694a6e22e"
S_B_STREAM_SHA256 = "1e0d2790039844e52c0fb93fd008b6420d7476691676552c5140da22bc90696b"

MASK10 = (1 << 10) - 1
ALL_SYNDROMES = (1 << 1024) - 1
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)
S_A_TARGETS = tuple((p + q, q - p) for p, q, _x, _y in CASES)


@dataclass(frozen=True)
class BOrbit:
    mask: int
    orbit_size: int
    weight: int
    rank: int
    image: int
    supports: tuple[int, ...]


def load_fourth_order():
    assert hashlib.sha256(FOURTH_ORDER.read_bytes()).hexdigest() == FOURTH_ORDER_SHA256
    assert hashlib.sha256(S_B_SOURCE.read_bytes()).hexdigest() == S_B_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location("q41_fourth_order", FOURTH_ORDER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LOW_MASKS = []
for _bit in range(10):
    _width = 1 << _bit
    _block = (1 << _width) - 1
    _mask = 0
    for _start in range(0, 1024, 2 * _width):
        _mask |= _block << _start
    LOW_MASKS.append(_mask)
LOW_MASKS = tuple(LOW_MASKS)


def translate(bits: int, shift: int) -> int:
    for bit, low_mask in enumerate(LOW_MASKS):
        if (shift >> bit) & 1:
            width = 1 << bit
            bits = ((bits & low_mask) << width) | ((bits >> width) & low_mask)
    return bits


def image_support(columns: tuple[int, ...]) -> int:
    support = 1
    for column in columns:
        support |= translate(support, column)
    return support


def read_b_orbits(binary: Path, q) -> tuple[dict[int, list[BOrbit]], str]:
    process = subprocess.Popen(
        [str(binary), "--stream"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert process.stdout is not None
    digest = hashlib.sha256()
    header = process.stdout.readline()
    digest.update(header)
    assert header == b"axis_word\torbit_size\tweight\trank\tcase\tsupport\n"

    grouped: dict[int, list[BOrbit]] = defaultdict(list)
    orbit_count = 0
    word_count = 0
    while True:
        records = []
        for _ in range(6):
            line = process.stdout.readline()
            if not line:
                break
            digest.update(line)
            fields = line.decode("ascii").rstrip("\n").split("\t")
            assert len(fields) == 6
            records.append(fields)
        if not records:
            break
        assert len(records) == 6
        mask = int(records[0][0], 16)
        orbit_size = int(records[0][1])
        weight = int(records[0][2])
        rank = int(records[0][3])
        assert [int(record[4]) for record in records] == list(range(6))
        assert all(record[:4] == records[0][:4] for record in records)
        columns = q.d_columns(mask)
        image = image_support(columns)
        assert image.bit_count() == 1 << rank
        signature = q.autocorrelation_signature(mask)
        supports = tuple(int(record[5], 16) for record in records)
        assert all(support & ~image == 0 for support in supports)
        grouped[signature].append(
            BOrbit(mask, orbit_size, weight, rank, image, supports)
        )
        orbit_count += 1
        word_count += orbit_size

    stderr = process.stderr.read().decode("utf-8", errors="replace")
    return_code = process.wait()
    assert return_code == 0, stderr
    stream_digest = digest.hexdigest()
    assert stream_digest == S_B_STREAM_SHA256
    assert orbit_count == 24_946
    assert word_count == 523_776
    assert len(grouped) == 512
    return grouped, stream_digest


def attainable(pair_count: int, target: int) -> bool:
    return abs(target) <= pair_count and (target - pair_count) % 2 == 0


def s_a_sum_possible(a_half: int, theta_s: int, target: tuple[int, int]) -> bool:
    active = (~theta_s) & MASK10
    # S_A axes complement H_A axes: a one is real in S_A.
    real_pairs = (active & a_half).bit_count()
    imaginary_pairs = (active & (~a_half & MASK10)).bit_count()
    for center in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        residual_real = target[0] - center[0]
        residual_imag = target[1] - center[1]
        assert residual_real % 2 == residual_imag % 2 == 0
        if attainable(real_pairs, residual_real // 2) and attainable(
            imaginary_pairs, residual_imag // 2
        ):
            return True
    return False


def h_a_sum_zero_possible(a_half: int, theta_h: int) -> bool:
    active = (~theta_h) & MASK10
    real_pairs = (active & (~a_half & MASK10)).bit_count()
    imaginary_pairs = (active & a_half).bit_count()
    return real_pairs % 2 == 0 and imaginary_pairs % 2 == 0


def affine_value(base: int, columns: tuple[int, ...], mask: int) -> int:
    value = base
    while mask:
        least = mask & -mask
        value ^= columns[least.bit_length() - 1]
        mask ^= least
    return value


def a_records(q, systems, affine_data, signature: int):
    records = []
    for a_half in range(1 << 10):
        h_orthogonal, s_orthogonal = systems[a_half]
        # Exact reflected-pair flips vanish in the pi^4 residual system.
        assert h_orthogonal == s_orthogonal == ALL_SYNDROMES
        h_data, s_data = affine_data[a_half]
        s_bases = s_data[0]
        assert isinstance(s_bases, tuple) and len(set(s_bases)) == 1
        h_value = affine_value(h_data[0], h_data[1:], signature)
        s_value = affine_value(s_bases[0], s_data[1:], signature)
        theta_h0, theta_s0 = q.theta_masks(a_half, 0)
        theta_h = theta_h0 ^ signature
        theta_s = theta_s0 ^ signature
        assert q.theta_masks(a_half, signature) == (theta_h, theta_s)
        s_case_mask = 0
        for case, target in enumerate(S_A_TARGETS):
            if s_a_sum_possible(a_half, theta_s, target):
                s_case_mask |= 1 << case
        records.append(
            (
                h_value,
                s_value,
                h_a_sum_zero_possible(a_half, theta_h),
                s_case_mask,
            )
        )
    return records


def sample_masks(grouped: dict[int, list[BOrbit]]) -> set[int]:
    result = set()
    seen_ranks = set()
    ordered = sorted((orbit for values in grouped.values() for orbit in values), key=lambda x: x.mask)
    for index, orbit in enumerate(ordered):
        if index % 199 == 0 or orbit.rank not in seen_ranks:
            result.add(orbit.mask)
            seen_ranks.add(orbit.rank)
    assert seen_ranks == {0, 3, 4, 6, 7, 9, 10}
    return result


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_tables(rank_counts, weight_counts) -> None:
    rank_rows = []
    for case, representative in enumerate(CASES):
        for rank in range(11):
            labeled, orbits = rank_counts[(case, rank)]
            if labeled == orbits == 0:
                continue
            rank_rows.append(
                {
                    "case": str(case),
                    "representative": "(" + ",".join(map(str, representative)) + ")",
                    "s_a_target": "(" + ",".join(map(str, S_A_TARGETS[case])) + ")",
                    "s_b_target": "("
                    + ",".join(
                        map(
                            str,
                            (
                                representative[2] + representative[3] - 1,
                                representative[3] - representative[2],
                            ),
                        )
                    )
                    + ")",
                    "rank": str(rank),
                    "labeled_axis_pairs": str(labeled),
                    "b_rotation_axis_orbits": str(orbits),
                }
            )
    weight_rows = []
    for case in range(6):
        for weight in range(0, 22, 4):
            labeled, orbits = weight_counts[(case, weight)]
            if labeled == orbits == 0:
                continue
            weight_rows.append(
                {
                    "case": str(case),
                    "b_weight": str(weight),
                    "labeled_axis_pairs": str(labeled),
                    "b_rotation_axis_orbits": str(orbits),
                }
            )
    assert rank_rows == read_tsv(HERE / "case_rank_table.tsv")
    assert weight_rows == read_tsv(HERE / "case_weight_table.tsv")


def classify(q, grouped, emit_mode: str):
    systems, affine_data = q.a_systems()
    by_case_rank: dict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0])
    by_case_weight: dict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0])
    stream_digest = hashlib.sha256()
    sample_digest = hashlib.sha256()
    header = (
        b"axis_word\torbit_size\tweight\trank\tsignature\t"
        b"case_0_a_mask\tcase_1_a_mask\tcase_2_a_mask\t"
        b"case_3_a_mask\tcase_4_a_mask\tcase_5_a_mask\n"
    )
    stream_digest.update(header)
    sample_digest.update(header)
    selected_masks = sample_masks(grouped)
    if emit_mode in ("full", "sample"):
        print(header.decode("ascii"), end="")

    processed_orbits = 0
    processed_words = 0
    zero_direction_checks = 0
    equal_center_checks = 0
    for signature in sorted(grouped):
        records = a_records(q, systems, affine_data, signature)
        zero_direction_checks += 2 * (1 << 10)
        equal_center_checks += 1 << 10
        for b in grouped[signature]:
            good_masks = [0] * 6
            for a_half, (h_value, s_value, h_possible, s_case_mask) in enumerate(records):
                if not h_possible or (h_value.bit_count() & 1):
                    continue
                if not ((b.image >> h_value) & 1):
                    continue
                for case in range(6):
                    if ((s_case_mask >> case) & 1) and (
                        (b.supports[case] >> s_value) & 1
                    ):
                        good_masks[case] |= 1 << a_half

            for case, mask in enumerate(good_masks):
                count = mask.bit_count()
                by_case_rank[(case, b.rank)][0] += count * b.orbit_size
                by_case_rank[(case, b.rank)][1] += count
                by_case_weight[(case, b.weight)][0] += count * b.orbit_size
                by_case_weight[(case, b.weight)][1] += count
            assert good_masks[3] == good_masks[4]
            line = (
                f"{b.mask:06x}\t{b.orbit_size}\t{b.weight}\t{b.rank}\t{signature:03x}\t"
                + "\t".join(f"{mask:0256x}" for mask in good_masks)
                + "\n"
            ).encode("ascii")
            stream_digest.update(line)
            if b.mask in selected_masks:
                sample_digest.update(line)
            if emit_mode == "full" or (emit_mode == "sample" and b.mask in selected_masks):
                print(line.decode("ascii"), end="")
            processed_orbits += 1
            processed_words += b.orbit_size

    assert processed_orbits == 24_946
    assert processed_words == 523_776
    assert all(
        values == [0, 0]
        for (case, rank), values in by_case_rank.items()
        if rank <= 7
    )
    return (
        by_case_rank,
        by_case_weight,
        stream_digest.hexdigest(),
        sample_digest.hexdigest(),
        len(selected_masks),
        zero_direction_checks,
        equal_center_checks,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--s-b-binary", type=Path, required=True)
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--stream", action="store_true")
    output.add_argument("--sample-stream", action="store_true")
    args = parser.parse_args()
    q = load_fourth_order()
    grouped, b_digest = read_b_orbits(args.s_b_binary.resolve(), q)
    emit_mode = "full" if args.stream else "sample" if args.sample_stream else "none"
    rank_counts, weight_counts, digest, sample_digest, sample_count, zero_checks, center_checks = classify(
        q, grouped, emit_mode
    )
    if emit_mode != "none":
        return

    verify_tables(rank_counts, weight_counts)

    print(f"fourth_order_dependency_sha256={FOURTH_ORDER_SHA256}")
    print(f"s_b_source_sha256={S_B_SOURCE_SHA256}")
    print(f"s_b_stream_sha256={b_digest}")
    print("b_words_wt_0_mod_4=523776")
    print("b_rotation_orbits_wt_0_mod_4=24946")
    print(f"a_zero_direction_checks={zero_checks}")
    print(f"a_center_residual_identity_checks={center_checks}")
    for case in range(6):
        labeled = sum(rank_counts[(case, rank)][0] for rank in range(11))
        orbits = sum(rank_counts[(case, rank)][1] for rank in range(11))
        ranks = ",".join(
            f"{rank}:{rank_counts[(case, rank)][0]}:{rank_counts[(case, rank)][1]}"
            for rank in range(11)
            if rank_counts[(case, rank)] != [0, 0]
        )
        weights = ",".join(
            f"{weight}:{weight_counts[(case, weight)][0]}:{weight_counts[(case, weight)][1]}"
            for weight in range(0, 22, 4)
            if weight_counts[(case, weight)] != [0, 0]
        )
        print(f"case_{case}_labeled_axis_pairs={labeled}")
        print(f"case_{case}_b_rotation_axis_orbits={orbits}")
        print(f"case_{case}_rank_counts={ranks}")
        print(f"case_{case}_weight_counts={weights}")
    assert all(rank_counts[(3, rank)] == rank_counts[(4, rank)] for rank in range(11))
    assert all(weight_counts[(3, weight)] == weight_counts[(4, weight)] for weight in range(22))
    print(f"canonical_axis_survivor_stream_sha256={digest}")
    print(f"sampled_b_rotation_orbits={sample_count}")
    print(f"sample_axis_survivor_stream_sha256={sample_digest}")
    print("rank_at_most_7_elimination=verified")
    print("case_3_case_4_identity=verified")
    print("case_rank_table=verified")
    print("case_weight_table=verified")
    print("certificate=verified")


if __name__ == "__main__":
    main()
