#!/usr/bin/env python3
"""Exact sign-lift multiplicities for the QLP-42 q=41 pi^4 layer."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEPENDENCY = ROOT.parent / "qlp42_q41_fourth_order_rank" / "verify_q41_fourth_order_rank.py"
DEPENDENCY_SHA256 = "cefc2f614980396aaecc9894733e3e8840658966b5d33e1ae6811a7bcc4b3d69"


def load_dependency():
    assert hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest() == DEPENDENCY_SHA256
    spec = importlib.util.spec_from_file_location("q41_pi4_rank", DEPENDENCY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def log2_power_of_two(value: int) -> int:
    assert value > 0 and value & (value - 1) == 0
    return value.bit_length() - 1


def affine_rank(left_orthogonal: int, right_orthogonal: int) -> int:
    intersection_size = (left_orthogonal & right_orthogonal).bit_count()
    return 10 - log2_power_of_two(intersection_size)


def classify(base):
    systems, affine_data = base.a_systems()
    groups, representatives, rank_counts = base.enumerate_b_orbits()
    base.verify_affine_predictions(systems, affine_data, representatives)

    histogram: dict[tuple[int, int, int], list[int]] = defaultdict(lambda: [0, 0])
    rank_histogram: dict[tuple[int, int, int, int], list[int]] = defaultdict(lambda: [0, 0])

    for (d_rank, signature, parity, b_orthogonal), (labeled_b, orbit_b) in groups.items():
        if d_rank == 10:
            labeled_pairs = labeled_b * (1 << 10)
            orbit_pairs = orbit_b * (1 << 10)
            histogram[(10, 10, 4)][0] += labeled_pairs
            histogram[(10, 10, 4)][1] += orbit_pairs
            rank_histogram[(10, 10, 10, 4)][0] += labeled_pairs
            rank_histogram[(10, 10, 10, 4)][1] += orbit_pairs
            continue

        for a_half in range(1 << 10):
            h_orthogonal, s_orthogonal = systems[a_half]
            h_data, s_data = affine_data[a_half]
            h_value = base.affine_value(h_data[0], h_data[1:], signature, parity)
            if not base.in_sum_space(h_value, h_orthogonal, b_orthogonal):
                continue

            s_bases = s_data[0]
            s_columns = s_data[1:]
            valid_centers = sum(
                base.in_sum_space(
                    base.affine_value(center_base, s_columns, signature, parity),
                    s_orthogonal,
                    b_orthogonal,
                )
                for center_base in s_bases
            )
            if valid_centers == 0:
                continue

            h_rank = affine_rank(h_orthogonal, b_orthogonal)
            s_rank = affine_rank(s_orthogonal, b_orthogonal)
            histogram[(h_rank, s_rank, valid_centers)][0] += labeled_b
            histogram[(h_rank, s_rank, valid_centers)][1] += orbit_b
            rank_histogram[(d_rank, h_rank, s_rank, valid_centers)][0] += labeled_b
            rank_histogram[(d_rank, h_rank, s_rank, valid_centers)][1] += orbit_b

    return histogram, rank_histogram, rank_counts


def histogram_rows(histogram: dict[tuple[int, int, int], list[int]]) -> list[dict[str, str]]:
    rows = []
    for (h_rank, s_rank, centers), (labeled, orbits) in sorted(histogram.items()):
        binary_exponent = 62 - h_rank - s_rank
        lifts_per_pair = centers << binary_exponent
        rows.append(
            {
                "h_rank": str(h_rank),
                "s_rank": str(s_rank),
                "valid_center_phases": str(centers),
                "binary_exponent": str(binary_exponent),
                "sign_lifts_per_axis_pair": str(lifts_per_pair),
                "labeled_axis_pairs": str(labeled),
                "b_rotation_axis_orbits": str(orbits),
                "labeled_sign_lifts": str(labeled * lifts_per_pair),
                "b_rotation_sign_lifts": str(orbits * lifts_per_pair),
            }
        )
    return rows


def rank_rows(rank_histogram: dict[tuple[int, int, int, int], list[int]]) -> list[dict[str, str]]:
    rows = []
    for (d_rank, h_rank, s_rank, centers), (labeled, orbits) in sorted(rank_histogram.items()):
        rows.append(
            {
                "d_rank": str(d_rank),
                "h_rank": str(h_rank),
                "s_rank": str(s_rank),
                "valid_center_phases": str(centers),
                "labeled_axis_pairs": str(labeled),
                "b_rotation_axis_orbits": str(orbits),
            }
        )
    return rows


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    base = load_dependency()
    histogram, rank_histogram, _rank_counts = classify(base)
    rows = histogram_rows(histogram)
    detailed_rows = rank_rows(rank_histogram)

    assert rows == read_tsv(ROOT / "multiplicity_table.tsv")
    assert detailed_rows == read_tsv(ROOT / "rank_multiplicity_table.tsv")

    labeled_pairs = sum(int(row["labeled_axis_pairs"]) for row in rows)
    orbit_pairs = sum(int(row["b_rotation_axis_orbits"]) for row in rows)
    labeled_lifts = sum(int(row["labeled_sign_lifts"]) for row in rows)
    orbit_lifts = sum(int(row["b_rotation_sign_lifts"]) for row in rows)
    assert labeled_pairs == 1_717_504_656
    assert orbit_pairs == 81_785_936
    assert labeled_lifts == 37_834_587_347_152_206_299_136
    assert orbit_lifts == 1_801_647_016_531_057_442_816
    assert len(rows) == len(detailed_rows) == 5
    assert all(
        row["d_rank"] == row["h_rank"] == row["s_rank"]
        and row["valid_center_phases"] == "4"
        for row in detailed_rows
    )

    center_values = sorted({int(row["valid_center_phases"]) for row in rows})
    lift_values = sorted({int(row["sign_lifts_per_axis_pair"]) for row in rows})
    print(f"dependency_sha256={DEPENDENCY_SHA256}")
    print(f"multiplicity_classes={len(rows)}")
    print(f"rank_refined_classes={len(detailed_rows)}")
    print("valid_center_phase_counts=" + ",".join(map(str, center_values)))
    print("distinct_lifts_per_axis_pair=" + ",".join(map(str, lift_values)))
    print(f"surviving_labeled_axis_pairs={labeled_pairs}")
    print(f"surviving_b_rotation_axis_orbits={orbit_pairs}")
    print(f"total_labeled_sign_lifts={labeled_lifts}")
    print(f"total_b_rotation_sign_lifts={orbit_lifts}")
    print("multiplicity_table=verified")
    print("rank_multiplicity_table=verified")
    print("certificate=verified")


if __name__ == "__main__":
    main()
