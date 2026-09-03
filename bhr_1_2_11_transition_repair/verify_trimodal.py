#!/usr/bin/env python3
"""Exact checker for 22 transition-closed {1,2,11} BHR cores."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
from typing import Any

from audit_source_certificate import transported_cut
from verify import (
    SUPPORT,
    cyclic_length,
    grow_once,
    require,
    verify_growth,
    verify_realization,
)

MODES = (1, 2, 11)
MAXIMUM_LENGTH = 11
EXPECTED_SOURCE_COMMIT = "8fcd1e624b3d668794e3179787d0965137365286"
EXPECTED_SOURCE_SHA256 = (
    "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
)


def normalize_cuts(record: dict[str, int]) -> dict[int, int]:
    return {int(mode): cut for mode, cut in record.items()}


def advance(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    """Apply one growth and transport every selected cut."""
    require(set(cuts) == set(MODES), ("cut modes", cuts))
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


def verify_state(
    path: list[int], counts: tuple[int, int, int], cuts: dict[int, int]
) -> None:
    verify_realization(path, counts)
    maximum = max(
        cyclic_length(u, v, len(path)) for u, v in zip(path, path[1:])
    )
    require(maximum == MAXIMUM_LENGTH, ("maximum edge length", maximum))
    for first, second in itertools.combinations(MODES, 2):
        require(
            2 * maximum + first + second <= len(path),
            ("unsafe pair", len(path), maximum, first, second),
        )
    for mode in MODES:
        verify_growth(path, mode, cuts[mode])


def expected_bases() -> set[tuple[int, int, int]]:
    return {(1, b, c) for b in (1, 2) for c in range(1, 12)}


def verify_certificate(path: Path, grid: int) -> dict[str, Any]:
    require(grid >= 1, "grid must be positive")
    raw = path.read_bytes()
    data = json.loads(raw)
    require(data["schema"] == "bhr-trimodal-safe-cores-v1", "wrong schema")
    require(tuple(data["support"]) == SUPPORT == MODES, "wrong support")
    source = data["source_artifact"]
    require(source["repository_commit"] == EXPECTED_SOURCE_COMMIT, "wrong source commit")
    require(source["certificate_sha256"] == EXPECTED_SOURCE_SHA256, "wrong source hash")
    require(source["cap_witnesses"] == 22, "wrong source cap count")
    derivation = data["derivation"]
    require(tuple(derivation["growth_modes_applied_once"]) == MODES, "wrong derivation")
    require(derivation["orders_checked"] == 6, "wrong order count")
    require(derivation["require_identical_endpoints"] is True, "endpoint flag")
    margin = data["safe_margin"]
    require(margin["maximum_edge_length"] == MAXIMUM_LENGTH, "wrong D")
    require(tuple(margin["growth_modes"]) == MODES, "wrong margin modes")
    require(margin["minimum_seed_order"] == 37, "wrong minimum seed order")
    require(margin["maximum_pair_sum"] == 13, "wrong pair sum")
    require(2 * MAXIMUM_LENGTH + 13 <= 37, "invalid margin")
    require(len(data["cases"]) == 22, "wrong case count")
    require(
        {tuple(case["residue_case"]) for case in data["cases"]} == expected_bases(),
        "missing or duplicate residue case",
    )

    source_derivation_steps = 0
    family_paths_checked = 0
    coordinate_transitions_checked = 0
    commuting_squares_checked = 0
    record_hash = hashlib.sha256()

    for case_index, case in enumerate(data["cases"]):
        base = tuple(case["residue_case"])
        cap = case["cap_seed"]
        require(cap["source_witness_index"] == 0, (base, "cap index"))
        cap_counts = tuple(cap["counts"])
        require(
            all((count - residue) % mode == 0 for count, residue, mode in zip(cap_counts, base, MODES)),
            (base, "cap residue"),
        )
        cap_path = cap["path"]
        cap_cuts = normalize_cuts(cap["selected_growth_cuts"])
        verify_realization(cap_path, cap_counts)
        require(set(cap_cuts) == set(MODES), (base, "cap modes"))
        for mode in MODES:
            verify_growth(cap_path, mode, cap_cuts[mode])

        endpoints: list[tuple[list[int], dict[int, int]]] = []
        for order in itertools.permutations(MODES):
            current_path, current_cuts = cap_path, cap_cuts
            for mode in order:
                current_path, current_cuts = advance(current_path, current_cuts, mode)
                source_derivation_steps += 1
            endpoints.append((current_path, current_cuts))
        require(all(endpoint == endpoints[0] for endpoint in endpoints), (base, "six orders"))

        seed = case["safe_seed"]
        seed_counts = tuple(seed["counts"])
        require(
            seed_counts
            == tuple(count + increment for count, increment in zip(cap_counts, MODES)),
            (base, "safe seed counts"),
        )
        require(sum(seed_counts) + 1 >= 37, (base, "safe seed order"))
        seed_path = seed["path"]
        seed_cuts = normalize_cuts(seed["selected_growth_cuts"])
        require(endpoints[0] == (seed_path, seed_cuts), (base, "stored endpoint"))
        verify_state(seed_path, seed_counts, seed_cuts)

        family: dict[
            tuple[int, int, int], tuple[list[int], dict[int, int]]
        ] = {}
        p_path, p_cuts = seed_path, seed_cuts
        for p in range(grid + 2):
            q_path, q_cuts = p_path, p_cuts
            for q in range(grid + 2):
                r_path, r_cuts = q_path, q_cuts
                for r in range(grid + 2):
                    counts = (
                        seed_counts[0] + p,
                        seed_counts[1] + 2 * q,
                        seed_counts[2] + 11 * r,
                    )
                    verify_state(r_path, counts, r_cuts)
                    family[p, q, r] = (r_path, r_cuts)
                    record = [case_index, p, q, r, r_cuts, r_path]
                    record_hash.update(
                        json.dumps(record, separators=(",", ":"), sort_keys=True).encode()
                    )
                    record_hash.update(b"\n")
                    family_paths_checked += 1
                    r_path, r_cuts = advance(r_path, r_cuts, 11)
                q_path, q_cuts = advance(q_path, q_cuts, 2)
            p_path, p_cuts = advance(p_path, p_cuts, 1)

        for p, q, r in itertools.product(range(grid + 1), repeat=3):
            current_path, current_cuts = family[p, q, r]
            for coordinate, mode in enumerate(MODES):
                child = advance(current_path, current_cuts, mode)
                index = [p, q, r]
                index[coordinate] += 1
                require(child == family[tuple(index)], (base, p, q, r, mode))
                coordinate_transitions_checked += 1
            for first, second in itertools.combinations(MODES, 2):
                path_a, cuts_a = advance(current_path, current_cuts, first)
                final_a = advance(path_a, cuts_a, second)
                path_b, cuts_b = advance(current_path, current_cuts, second)
                final_b = advance(path_b, cuts_b, first)
                require(final_a == final_b, (base, p, q, r, first, second))
                commuting_squares_checked += 1

    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "python": platform.python_version(),
        "cases": len(data["cases"]),
        "source_derivation_steps": source_derivation_steps,
        "grid": grid,
        "family_paths_checked": family_paths_checked,
        "coordinate_transitions_checked": coordinate_transitions_checked,
        "commuting_squares_checked": commuting_squares_checked,
        "record_sha256": record_hash.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=3)
    args = parser.parse_args()
    summary = verify_certificate(args.certificate, args.grid)
    for key, value in summary.items():
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
