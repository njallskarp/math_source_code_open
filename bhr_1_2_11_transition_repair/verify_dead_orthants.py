#!/usr/bin/env python3
"""Definition-level checker for the eight dead-orthant repair certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
from typing import Any

from audit_source_certificate import transported_cut
from verify import (
    SUPPORT,
    cyclic_length,
    grow_once,
    growth_cuts,
    require,
    verify_growth,
    verify_realization,
)

EXPECTED_SOURCE_SHA256 = (
    "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
)
EXPECTED_SOURCE_COMMIT = "8fcd1e624b3d668794e3179787d0965137365286"
EXPECTED_AUDIT = {
    "transition_obligations": 1093,
    "predicted_cut_failures": 18,
    "total_mode_losses": 11,
    "affected_witnesses": 8,
    "dead_first_interior_targets": 8,
    "uniquely_covered_dead_targets": 8,
    "failure_records_sha256": (
        "0a604cbf19537c855faa04a8d31b4a5985603ec6f1464ddb6f9e60a357795b03"
    ),
}
MODES = (1, 2)
MAXIMUM_LENGTH = 11


def normalize_cuts(record: dict[str, int]) -> dict[int, int]:
    return {int(x): m for x, m in record.items()}


def advance(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    inserted_cut = cuts[inserted_mode]
    child = grow_once(path, inserted_mode, inserted_cut)
    child_cuts = {
        tested_mode: transported_cut(
            cuts[tested_mode], inserted_cut, inserted_mode
        )
        for tested_mode in MODES
    }
    for tested_mode in MODES:
        verify_growth(child, tested_mode, child_cuts[tested_mode])
    return child, child_cuts


def verify_safe_state(
    path: list[int], counts: tuple[int, int, int], cuts: dict[int, int]
) -> None:
    verify_realization(path, counts)
    actual_maximum = max(
        cyclic_length(u, v, len(path)) for u, v in zip(path, path[1:])
    )
    require(actual_maximum == MAXIMUM_LENGTH, ("maximum length", actual_maximum))
    require(
        2 * actual_maximum + sum(MODES) <= len(path),
        ("safe margin", len(path), actual_maximum),
    )
    for mode in MODES:
        verify_growth(path, mode, cuts[mode])


def verify_certificate(path: Path, grid: int) -> dict[str, Any]:
    require(grid >= 1, "grid must be positive")
    raw = path.read_bytes()
    data = json.loads(raw)
    require(data["schema"] == "bhr-dead-orthant-repair-v1", "wrong schema")
    require(tuple(data["support"]) == SUPPORT, "wrong support")
    source = data["source_artifact"]
    require(source["repository_commit"] == EXPECTED_SOURCE_COMMIT, "wrong source commit")
    require(source["certificate_sha256"] == EXPECTED_SOURCE_SHA256, "wrong source hash")
    for key, value in EXPECTED_AUDIT.items():
        require(source[key] == value, ("wrong audit metadata", key))
    margin = data["safe_margin"]
    require(margin["maximum_edge_length"] == MAXIMUM_LENGTH, "wrong D")
    require(tuple(margin["growth_modes"]) == MODES, "wrong modes")
    require(margin["seed_order"] == 25, "wrong seed order")
    require(2 * MAXIMUM_LENGTH + sum(MODES) <= margin["seed_order"], "bad margin")
    require(len(data["repairs"]) == 8, "wrong repair count")

    boundary_losses = 0
    record_hash = hashlib.sha256()
    interior_paths_checked = 0
    commuting_squares_checked = 0
    seen_sources: set[tuple[tuple[int, int, int], int]] = set()

    for repair_index, repair in enumerate(data["repairs"]):
        residue_case = tuple(repair["residue_case"])
        source_key = (residue_case, repair["source_witness_index"])
        require(source_key not in seen_sources, ("duplicate source", source_key))
        seen_sources.add(source_key)

        boundary = repair["boundary_seed"]
        boundary_counts = tuple(boundary["counts"])
        boundary_path = boundary["path"]
        boundary_cuts = normalize_cuts(boundary["selected_growth_cuts"])
        verify_realization(boundary_path, boundary_counts)
        require(set(boundary_cuts) == set(MODES), (source_key, "boundary modes"))
        for mode in MODES:
            verify_growth(boundary_path, mode, boundary_cuts[mode])
        actual_losses: list[list[int]] = []
        for inserted_mode in MODES:
            grown = grow_once(boundary_path, inserted_mode, boundary_cuts[inserted_mode])
            for tested_mode in MODES:
                if not growth_cuts(grown, tested_mode):
                    actual_losses.append([inserted_mode, tested_mode])
        expected_losses = boundary["lost_ordered_mode_pairs"]
        require(actual_losses == expected_losses, (source_key, actual_losses, expected_losses))
        require(all(a != b for a, b in actual_losses), (source_key, "self loss"))
        boundary_losses += len(actual_losses)

        interior = repair["interior_seed"]
        interior_counts = tuple(interior["counts"])
        require(
            interior_counts
            == (boundary_counts[0] + 1, boundary_counts[1] + 2, boundary_counts[2]),
            (source_key, "not first interior point"),
        )
        require(sum(interior_counts) + 1 == 25, (source_key, "seed order"))
        seed_path = interior["path"]
        seed_cuts = normalize_cuts(interior["selected_growth_cuts"])
        require(set(seed_cuts) == set(MODES), (source_key, "interior modes"))
        recorded_all = {
            int(mode): cuts for mode, cuts in interior["all_growth_cuts"].items()
        }
        require(
            recorded_all == {mode: growth_cuts(seed_path, mode) for mode in MODES},
            (source_key, "all seed cuts"),
        )
        require(
            all(seed_cuts[mode] in recorded_all[mode] for mode in MODES),
            (source_key, "selected seed cut"),
        )
        verify_safe_state(seed_path, interior_counts, seed_cuts)

        family: dict[tuple[int, int], tuple[list[int], dict[int, int]]] = {}
        row_path, row_cuts = seed_path, seed_cuts
        for p in range(grid + 2):
            current_path, current_cuts = row_path, row_cuts
            for q in range(grid + 2):
                counts = (
                    interior_counts[0] + p,
                    interior_counts[1] + 2 * q,
                    interior_counts[2],
                )
                verify_safe_state(current_path, counts, current_cuts)
                family[p, q] = (current_path, current_cuts)
                record = [repair_index, p, q, current_cuts, current_path]
                record_hash.update(
                    json.dumps(record, separators=(",", ":"), sort_keys=True).encode()
                )
                record_hash.update(b"\n")
                interior_paths_checked += 1
                current_path, current_cuts = advance(current_path, current_cuts, 2)
            row_path, row_cuts = advance(row_path, row_cuts, 1)

        for p in range(grid + 1):
            for q in range(grid + 1):
                current_path, current_cuts = family[p, q]
                one_path, one_cuts = advance(current_path, current_cuts, 1)
                two_path, two_cuts = advance(current_path, current_cuts, 2)
                require((one_path, one_cuts) == family[p + 1, q], (source_key, p, q, 1))
                require((two_path, two_cuts) == family[p, q + 1], (source_key, p, q, 2))
                one_two = advance(one_path, one_cuts, 2)
                two_one = advance(two_path, two_cuts, 1)
                require(one_two == two_one, (source_key, p, q, "noncommuting"))
                commuting_squares_checked += 1

    require(boundary_losses == 11, ("boundary losses", boundary_losses))
    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "python": platform.python_version(),
        "repairs": len(data["repairs"]),
        "boundary_losses_reproduced": boundary_losses,
        "grid": grid,
        "interior_paths_checked": interior_paths_checked,
        "commuting_squares_checked": commuting_squares_checked,
        "record_sha256": record_hash.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=10)
    args = parser.parse_args()
    summary = verify_certificate(args.certificate, args.grid)
    for key, value in summary.items():
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
