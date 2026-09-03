#!/usr/bin/env python3
"""Audit conservative symbolic coverage after all transition repairs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

from audit_source_certificate import audit_certificate
from verify import SUPPORT, require
from verify_cap_orthants import verify_certificate as verify_cap_orthants
from verify_dead_orthants import verify_certificate as verify_dead_orthants
from verify_even_b_c1 import verify_certificate as verify_even_b_c1
from verify_residual_slab import verify_certificate as verify_residual_slab
from verify_small_a_c3_slab import verify_certificate as verify_small_a_c3_slab
from verify_target_orthant import verify_certificate as verify_target_orthant

EXPECTED_DEAD_SHA256 = (
    "33d53244922865533b379d8f40d91063e1758f5997362e940f5d1ea503e7686d"
)
EXPECTED_COUNTS = {
    "admissible_symbolic_patterns": 9544,
    "after_exact_points_and_rays": 3273,
    "after_eight_dead_orthants": 3457,
    "after_twenty_two_trimodal_cores": 5999,
    "after_twenty_two_cap_orthants": 8052,
    "after_first_residual_slab": 8071,
    "after_even_b_c1_completion": 8105,
    "after_target_orthant": 8139,
    "after_small_a_c3_slab": 8151,
    "residual_symbolic_patterns": 1393,
}


def admissible(counts: tuple[int, int, int]) -> bool:
    a, b, _ = counts
    order = sum(counts) + 1
    return order >= 22 and (order % 11 != 0 or a + b >= 10)


def pattern_has_admissible_lift(
    counts: tuple[int, int, int], high: tuple[bool, bool, bool]
) -> bool:
    if not any(high):
        return admissible(counts)
    if high[0] or high[1]:
        return True
    a, b, _ = counts
    return (sum(counts) + 1) % 11 != 0 or a + b >= 10


def exact_point_or_ray(
    witnesses: list[dict[str, Any]], target: tuple[int, int, int]
) -> bool:
    for witness in witnesses:
        start = tuple(witness["counts"])
        if target == start:
            return True
        for mode in witness["grow"]:
            coordinate = SUPPORT.index(mode)
            if all(
                target[index] == start[index]
                for index in range(3)
                if index != coordinate
            ) and target[coordinate] >= start[coordinate]:
                if (target[coordinate] - start[coordinate]) % mode == 0:
                    return True
    return False


def in_orthant(
    target: tuple[int, int, int],
    seed: tuple[int, int, int],
    varying_modes: set[int],
) -> bool:
    for coordinate, mode in enumerate(SUPPORT):
        if mode in varying_modes:
            if target[coordinate] < seed[coordinate]:
                return False
            if (target[coordinate] - seed[coordinate]) % mode:
                return False
        elif target[coordinate] != seed[coordinate]:
            return False
    return True


def in_strengthened_residual_slab(target: tuple[int, int, int]) -> bool:
    """Test the explicit odd-b, c=1 four-block formula."""
    a, b, c = target
    return c == 1 and a >= 1 and b >= 9 and b % 2 == 1 and a + b >= 20


def in_completed_c1_slice(target: tuple[int, int, int]) -> bool:
    """Test the now-complete admissible positive c=1 slice."""
    a, b, c = target
    return c == 1 and a >= 1 and b >= 1 and a + b >= 20


def audit_coverage(
    source_path: Path,
    dead_path: Path,
    trimodal_path: Path,
    slab_path: Path,
    even_b_c1_path: Path,
    target_path: Path,
    small_a_c3_path: Path,
    verify_inputs: bool = True,
) -> dict[str, Any]:
    source_raw = source_path.read_bytes()
    dead_raw = dead_path.read_bytes()
    trimodal_raw = trimodal_path.read_bytes()
    slab_raw = slab_path.read_bytes()
    even_b_c1_raw = even_b_c1_path.read_bytes()
    target_raw = target_path.read_bytes()
    small_a_c3_raw = small_a_c3_path.read_bytes()
    if verify_inputs:
        audit_certificate(source_path)
        require(
            hashlib.sha256(dead_raw).hexdigest() == EXPECTED_DEAD_SHA256,
            "unpinned dead-orthant certificate",
        )
        verify_dead_orthants(dead_path, 1)
        verify_cap_orthants(trimodal_path, 1)
        verify_residual_slab(slab_path, 1)
        verify_even_b_c1(even_b_c1_path, 1)
        verify_target_orthant(target_path, 1)
        verify_small_a_c3_slab(small_a_c3_path, 1)

    source = json.loads(source_raw)
    dead = json.loads(dead_raw)
    trimodal = json.loads(trimodal_raw)
    slab = json.loads(slab_raw)
    target_orthant = json.loads(target_raw)
    small_a_c3 = json.loads(small_a_c3_raw)
    require(tuple(source["underlying_set"]) == SUPPORT, "wrong source support")
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
    slab_seed = tuple(slab["seed"]["counts"])
    require(slab_seed == (2, 21, 1), "wrong residual slab seed")
    target_seed = tuple(target_orthant["seed"]["counts"])
    require(target_seed == (4, 7, 23), "wrong target orthant seed")
    small_a_c3_seed = tuple(small_a_c3["seed"]["counts"])
    require(small_a_c3_seed == (1, 9, 25), "wrong small-a c3 slab seed")

    counts = {key: 0 for key in EXPECTED_COUNTS if key != "residual_symbolic_patterns"}
    residuals: list[tuple[tuple[int, int, int], tuple[int, int, int], tuple[bool, bool, bool]]] = []
    residual_by_base: dict[tuple[int, int, int], int] = {}

    for case in sorted(source["cases"], key=lambda item: tuple(item["base"])):
        base = tuple(case["base"])
        witnesses = case["witnesses"]
        maxima = tuple(
            max(witness["counts"][coordinate] for witness in witnesses)
            for coordinate in range(3)
        )
        axes = []
        for residue, step, maximum in zip(base, SUPPORT, maxima):
            axes.append(list(range(residue, maximum + 1, step)) + [maximum + step])

        for target in itertools.product(*axes):
            high = tuple(
                target[coordinate] > maxima[coordinate] for coordinate in range(3)
            )
            if not pattern_has_admissible_lift(target, high):
                continue
            counts["admissible_symbolic_patterns"] += 1
            covered = exact_point_or_ray(witnesses, target)
            if covered:
                counts["after_exact_points_and_rays"] += 1
            if not covered and base in dead_by_base:
                covered = in_orthant(target, dead_by_base[base], {1, 2})
            if covered:
                counts["after_eight_dead_orthants"] += 1
            if not covered:
                covered = in_orthant(target, tri_by_base[base], set(SUPPORT))
            if covered:
                counts["after_twenty_two_trimodal_cores"] += 1
            if not covered:
                covered = in_orthant(target, cap_by_base[base], set(SUPPORT))
            if covered:
                counts["after_twenty_two_cap_orthants"] += 1
            if not covered and base == (1, 1, 1):
                covered = in_strengthened_residual_slab(target)
            if covered:
                counts["after_first_residual_slab"] += 1
            if not covered:
                covered = in_completed_c1_slice(target)
            if covered:
                counts["after_even_b_c1_completion"] += 1
            if not covered:
                covered = in_orthant(target, target_seed, set(SUPPORT))
            if covered:
                counts["after_target_orthant"] += 1
            if not covered:
                covered = in_orthant(target, small_a_c3_seed, {2, 11})
            if covered:
                counts["after_small_a_c3_slab"] += 1
            else:
                residuals.append((base, target, high))
                residual_by_base[base] = residual_by_base.get(base, 0) + 1

    counts["residual_symbolic_patterns"] = len(residuals)
    for key, expected in EXPECTED_COUNTS.items():
        require(counts[key] == expected, (key, counts[key], expected))
    canonical = json.dumps(residuals, separators=(",", ":"))
    largest_base, largest_count = max(
        residual_by_base.items(), key=lambda item: (item[1], tuple(-x for x in item[0]))
    )
    return {
        "source_sha256": hashlib.sha256(source_raw).hexdigest(),
        "dead_orthant_sha256": hashlib.sha256(dead_raw).hexdigest(),
        "trimodal_sha256": hashlib.sha256(trimodal_raw).hexdigest(),
        "residual_slab_sha256": hashlib.sha256(slab_raw).hexdigest(),
        "even_b_c1_sha256": hashlib.sha256(even_b_c1_raw).hexdigest(),
        "target_orthant_sha256": hashlib.sha256(target_raw).hexdigest(),
        "small_a_c3_slab_sha256": hashlib.sha256(small_a_c3_raw).hexdigest(),
        **counts,
        "residual_cases": len(residual_by_base),
        "largest_residual_case": list(largest_base),
        "largest_residual_case_count": largest_count,
        "first_residual_pattern": [list(value) for value in residuals[0]],
        "residual_records_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_certificate", type=Path)
    parser.add_argument("--dead", type=Path, default=Path("dead_orthant_certificate.json"))
    parser.add_argument("--trimodal", type=Path, default=Path("trimodal_certificate.json"))
    parser.add_argument(
        "--slab", type=Path, default=Path("residual_slab_certificate.json")
    )
    parser.add_argument(
        "--even-b-c1", type=Path, default=Path("even_b_c1_certificate.json")
    )
    parser.add_argument(
        "--target", type=Path, default=Path("target_orthant_certificate.json")
    )
    parser.add_argument(
        "--small-a-c3", type=Path, default=Path("small_a_c3_slab_certificate.json")
    )
    args = parser.parse_args()
    summary = audit_coverage(
        args.source_certificate,
        args.dead,
        args.trimodal,
        args.slab,
        args.even_b_c1,
        args.target,
        args.small_a_c3,
    )
    for key, value in summary.items():
        if isinstance(value, list):
            value = json.dumps(value, separators=(",", ":"))
        print(f"{key}={value}")
    print("AUDITED")


if __name__ == "__main__":
    main()
