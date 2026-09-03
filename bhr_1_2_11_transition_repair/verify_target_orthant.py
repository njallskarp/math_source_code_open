#!/usr/bin/env python3
"""Exact checker for the transition-closed BHR orthant from (4,7,23)."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
from typing import Any

from verify import SUPPORT, require
from verify_trimodal import MODES, advance, normalize_cuts, verify_state

EXPECTED_CERTIFICATE_SHA256 = (
    "a236dc2abb827aa6f283baaf686c497ad02f22d9254c1bf590a24b65146899b9"
)
EXPECTED_BEFORE_DIGEST = (
    "3d9510f09dd751cdc1e886ac02941381a88971ca22e26e52417995d6f257932d"
)
SEED_COUNTS = (4, 7, 23)


def increment_counts(
    counts: tuple[int, int, int], increments: tuple[int, int, int]
) -> tuple[int, int, int]:
    return tuple(
        count + mode * increment
        for count, mode, increment in zip(counts, MODES, increments)
    )


def verify_certificate(
    path: Path, grid: int, enforce_pinned_hash: bool = True
) -> dict[str, Any]:
    require(grid >= 1, "grid must be positive")
    raw = path.read_bytes()
    certificate_sha256 = hashlib.sha256(raw).hexdigest()
    if enforce_pinned_hash:
        require(
            certificate_sha256 == EXPECTED_CERTIFICATE_SHA256,
            "unpinned certificate",
        )
    data = json.loads(raw)
    require(data["schema"] == "bhr-target-orthant-v1", "wrong schema")
    require(tuple(data["support"]) == SUPPORT == MODES, "wrong support")

    source = data["source_context"]
    require(source["previous_coverage"] == 8071, "wrong prior coverage")
    require(
        source["previous_residual_symbolic_patterns"] == 1473,
        "wrong prior residual count",
    )
    require(
        source["previous_residual_records_sha256"] == EXPECTED_BEFORE_DIGEST,
        "wrong prior digest",
    )

    generator = data["generator"]
    require(generator["ortools"] == "9.14.6206", "wrong generator version")
    require(generator["num_search_workers"] == 1, "wrong worker count")
    require(generator["random_seed"] == 1, "wrong generator seed")

    margin = data["safe_margin"]
    require(tuple(margin["growth_modes"]) == MODES, "wrong margin modes")
    require(margin["maximum_edge_length"] == 11, "wrong maximum length")
    require(margin["maximum_pair_sum"] == 13, "wrong pair sum")
    require(margin["seed_order"] == 35, "wrong seed order")
    require(2 * 11 + 13 == 35, "invalid exact safe margin")

    seed = data["seed"]
    require(tuple(seed["counts"]) == SEED_COUNTS, "wrong seed counts")
    seed_path = seed["path"]
    seed_cuts = normalize_cuts(seed["selected_growth_cuts"])
    require(seed_cuts == {1: 22, 2: 23, 11: 10}, "wrong seed cuts")
    verify_state(seed_path, SEED_COUNTS, seed_cuts)

    one_each_endpoints: list[tuple[list[int], dict[int, int]]] = []
    source_derivation_steps = 0
    for order in itertools.permutations(MODES):
        current_path, current_cuts = seed_path, seed_cuts
        for mode in order:
            current_path, current_cuts = advance(
                current_path, current_cuts, mode
            )
            source_derivation_steps += 1
        one_each_endpoints.append((current_path, current_cuts))
    require(
        all(endpoint == one_each_endpoints[0] for endpoint in one_each_endpoints),
        "six one-each orders do not agree",
    )

    family: dict[
        tuple[int, int, int], tuple[list[int], dict[int, int]]
    ] = {}
    record_hash = hashlib.sha256()
    family_paths_checked = 0
    coordinate_transitions_checked = 0
    commuting_squares_checked = 0

    p_path, p_cuts = seed_path, seed_cuts
    for p in range(grid + 2):
        q_path, q_cuts = p_path, p_cuts
        for q in range(grid + 2):
            r_path, r_cuts = q_path, q_cuts
            for r in range(grid + 2):
                index = (p, q, r)
                counts = increment_counts(SEED_COUNTS, index)
                verify_state(r_path, counts, r_cuts)
                family[index] = (r_path, r_cuts)
                record_hash.update(
                    json.dumps(
                        [p, q, r, r_cuts, r_path],
                        separators=(",", ":"),
                        sort_keys=True,
                    ).encode()
                )
                record_hash.update(b"\n")
                family_paths_checked += 1
                r_path, r_cuts = advance(r_path, r_cuts, 11)
            q_path, q_cuts = advance(q_path, q_cuts, 2)
        p_path, p_cuts = advance(p_path, p_cuts, 1)

    for p, q, r in itertools.product(range(grid + 1), repeat=3):
        index = (p, q, r)
        current_path, current_cuts = family[index]
        for coordinate, mode in enumerate(MODES):
            child = advance(current_path, current_cuts, mode)
            child_index = [p, q, r]
            child_index[coordinate] += 1
            require(child == family[tuple(child_index)], (index, mode))
            coordinate_transitions_checked += 1
        for first, second in itertools.combinations(MODES, 2):
            path_a, cuts_a = advance(current_path, current_cuts, first)
            final_a = advance(path_a, cuts_a, second)
            path_b, cuts_b = advance(current_path, current_cuts, second)
            final_b = advance(path_b, cuts_b, first)
            require(final_a == final_b, (index, first, second))
            commuting_squares_checked += 1

    return {
        "certificate_sha256": certificate_sha256,
        "python": platform.python_version(),
        "seed_order": len(seed_path),
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
    parser.add_argument("--allow-unpinned", action="store_true")
    args = parser.parse_args()
    summary = verify_certificate(
        args.certificate, args.grid, not args.allow_unpinned
    )
    for key, value in summary.items():
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
