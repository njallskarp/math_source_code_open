#!/usr/bin/env python3
"""Measure the exact symbolic-coverage gain from the small-a mantle."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

from audit_repaired_coverage import (
    SUPPORT,
    audit_coverage,
    exact_point_or_ray,
    in_completed_c1_slice,
    in_orthant,
    in_strengthened_residual_slab,
    pattern_has_admissible_lift,
)
from verify import require
from verify_small_a_mantle import verify_certificate as verify_mantle

EXPECTED = {
    "previous_coverage": 8151,
    "after_small_a_mantle": 8211,
    "newly_covered": 60,
    "residual_symbolic_patterns": 1333,
    "residual_cases": 22,
    "largest_residual_case": [1, 1, 3],
    "largest_residual_case_count": 102,
    "first_residual_pattern": [[1, 1, 1], [6, 5, 23], [False, False, False]],
    "residual_records_sha256": "00ed42e9e22d87d0a202e6b0e55ddc284cf8a7fff3479cff98df18e7def54b27",
}


def audit_mantle_coverage(
    source_path: Path,
    dead_path: Path,
    trimodal_path: Path,
    slab_path: Path,
    even_b_c1_path: Path,
    target_path: Path,
    small_a_c3_path: Path,
    mantle_path: Path,
) -> dict[str, Any]:
    previous = audit_coverage(
        source_path,
        dead_path,
        trimodal_path,
        slab_path,
        even_b_c1_path,
        target_path,
        small_a_c3_path,
    )
    require(previous["after_small_a_c3_slab"] == 8151, "wrong prior coverage")
    require(previous["residual_symbolic_patterns"] == 1393, "wrong prior residual")
    verify_mantle(mantle_path, 1)

    source = json.loads(source_path.read_bytes())
    dead = json.loads(dead_path.read_bytes())
    trimodal = json.loads(trimodal_path.read_bytes())
    target = json.loads(target_path.read_bytes())
    small_a_c3 = json.loads(small_a_c3_path.read_bytes())
    mantle = json.loads(mantle_path.read_bytes())
    dead_by_base = {
        tuple(record["residue_case"]): tuple(record["boundary_seed"]["counts"])
        for record in dead["repairs"]
    }
    tri_by_base = {
        tuple(record["residue_case"]): tuple(record["safe_seed"]["counts"])
        for record in trimodal["cases"]
    }
    cap_by_base = {
        tuple(record["residue_case"]): tuple(record["cap_seed"]["counts"])
        for record in trimodal["cases"]
    }
    target_seed = tuple(target["seed"]["counts"])
    small_a_c3_seed = tuple(small_a_c3["seed"]["counts"])
    mantle_by_base = {
        tuple(record["residue_case"]): tuple(record["safe_seed"]["counts"])
        for record in mantle["cases"]
    }

    old_residuals = []
    residuals = []
    residual_by_base: dict[tuple[int, int, int], int] = {}
    gains_by_base: dict[tuple[int, int, int], int] = {}
    for case in sorted(source["cases"], key=lambda item: tuple(item["base"])):
        base = tuple(case["base"])
        witnesses = case["witnesses"]
        maxima = tuple(
            max(witness["counts"][coordinate] for witness in witnesses)
            for coordinate in range(3)
        )
        axes = [
            list(range(residue, maximum + 1, step)) + [maximum + step]
            for residue, step, maximum in zip(base, SUPPORT, maxima)
        ]
        for target_counts in itertools.product(*axes):
            high = tuple(
                target_counts[coordinate] > maxima[coordinate]
                for coordinate in range(3)
            )
            if not pattern_has_admissible_lift(target_counts, high):
                continue
            covered = exact_point_or_ray(witnesses, target_counts)
            if not covered and base in dead_by_base:
                covered = in_orthant(target_counts, dead_by_base[base], {1, 2})
            if not covered:
                covered = in_orthant(target_counts, tri_by_base[base], set(SUPPORT))
            if not covered:
                covered = in_orthant(target_counts, cap_by_base[base], set(SUPPORT))
            if not covered and base == (1, 1, 1):
                covered = in_strengthened_residual_slab(target_counts)
            if not covered:
                covered = in_completed_c1_slice(target_counts)
            if not covered:
                covered = in_orthant(target_counts, target_seed, set(SUPPORT))
            if not covered:
                covered = in_orthant(target_counts, small_a_c3_seed, {2, 11})
            if covered:
                continue

            record = (base, target_counts, high)
            old_residuals.append(record)
            mantle_seed = mantle_by_base.get(base)
            if mantle_seed is not None and in_orthant(
                target_counts, mantle_seed, {2, 11}
            ):
                gains_by_base[base] = gains_by_base.get(base, 0) + 1
            else:
                residuals.append(record)
                residual_by_base[base] = residual_by_base.get(base, 0) + 1

    require(len(old_residuals) == 1393, "reconstructed prior residual mismatch")
    canonical = json.dumps(residuals, separators=(",", ":"))
    largest_base, largest_count = max(
        residual_by_base.items(), key=lambda item: (item[1], tuple(-x for x in item[0]))
    )
    summary = {
        "mantle_certificate_sha256": hashlib.sha256(mantle_path.read_bytes()).hexdigest(),
        "previous_coverage": 8151,
        "after_small_a_mantle": 9544 - len(residuals),
        "newly_covered": len(old_residuals) - len(residuals),
        "newly_covered_by_residue": {
            str(base[2]): gains_by_base.get(base, 0)
            for base in sorted(mantle_by_base)
        },
        "residual_symbolic_patterns": len(residuals),
        "residual_cases": len(residual_by_base),
        "largest_residual_case": list(largest_base),
        "largest_residual_case_count": largest_count,
        "first_residual_pattern": [list(value) for value in residuals[0]],
        "residual_records_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
    }
    for key, expected in EXPECTED.items():
        require(summary[key] == expected, (key, summary[key], expected))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_certificate", type=Path)
    parser.add_argument("--dead", type=Path, default=Path("dead_orthant_certificate.json"))
    parser.add_argument("--trimodal", type=Path, default=Path("trimodal_certificate.json"))
    parser.add_argument("--slab", type=Path, default=Path("residual_slab_certificate.json"))
    parser.add_argument("--even-b-c1", type=Path, default=Path("even_b_c1_certificate.json"))
    parser.add_argument("--target", type=Path, default=Path("target_orthant_certificate.json"))
    parser.add_argument("--small-a-c3", type=Path, default=Path("small_a_c3_slab_certificate.json"))
    parser.add_argument("--mantle", type=Path, default=Path("small_a_mantle_certificate.json"))
    args = parser.parse_args()
    result = audit_mantle_coverage(
        args.source_certificate, args.dead, args.trimodal, args.slab,
        args.even_b_c1, args.target, args.small_a_c3, args.mantle,
    )
    for key, value in result.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value, separators=(",", ":"), sort_keys=True)
        print(f"{key}={value}")
    print("AUDITED")


if __name__ == "__main__":
    main()
