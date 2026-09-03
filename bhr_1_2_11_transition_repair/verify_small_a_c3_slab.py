#!/usr/bin/env python3
"""Exact checker for the transition-closed BHR slab from (1,9,25)."""

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

MODES = (2, 11)
SOURCE_COUNTS = (1, 7, 14)
SEED_COUNTS = (1, 9, 25)
EXPECTED_CERTIFICATE_SHA256 = (
    "1e2af60896b1f3e5970c877cb630fe8d4171eb0b1e5335d063689767b9187e1f"
)
EXPECTED_SOURCE_SHA256 = (
    "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
)
EXPECTED_BEFORE_DIGEST = (
    "09c1f72e2be4010c8783418c46464547e6fffe20fdddd137ebb46443da4a8b0d"
)


def normalize_cuts(record: dict[str, int]) -> dict[int, int]:
    return {int(mode): cut for mode, cut in record.items()}


def advance(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    """Apply one selected growth and transport both selected cuts."""
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


def verify_safe_state(
    path: list[int], counts: tuple[int, int, int], cuts: dict[int, int]
) -> None:
    verify_realization(path, counts)
    maximum = max(
        cyclic_length(u, v, len(path)) for u, v in zip(path, path[1:])
    )
    require(maximum == 11, ("maximum edge length", maximum))
    require(2 * maximum + sum(MODES) <= len(path), ("unsafe pair", len(path)))
    for mode in MODES:
        verify_growth(path, mode, cuts[mode])


def verify_certificate(
    path: Path, grid: int, enforce_pinned_hash: bool = True
) -> dict[str, Any]:
    require(grid >= 1, "grid must be positive")
    raw = path.read_bytes()
    certificate_sha256 = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    require(data["schema"] == "bhr-small-a-c3-slab-v1", "wrong schema")
    require(tuple(data["support"]) == SUPPORT, "wrong support")

    context = data["source_context"]
    require(
        context["source_certificate_sha256"] == EXPECTED_SOURCE_SHA256,
        "wrong source hash",
    )
    require(tuple(context["residue_case"]) == (1, 1, 3), "wrong residue")
    require(context["source_witness_index"] == 1, "wrong source index")
    require(context["previous_coverage"] == 8139, "wrong prior coverage")
    require(
        context["previous_residual_symbolic_patterns"] == 1405,
        "wrong prior residual count",
    )
    require(
        context["previous_residual_records_sha256"] == EXPECTED_BEFORE_DIGEST,
        "wrong prior residual digest",
    )

    derivation = data["derivation"]
    require(tuple(derivation["counts"]) == SOURCE_COUNTS, "wrong source counts")
    source_path = derivation["path"]
    source_cuts = normalize_cuts(derivation["selected_growth_cuts"])
    require(source_cuts == {2: 2, 11: 11}, "wrong source cuts")
    require(tuple(derivation["growth_modes_applied_once"]) == MODES, "wrong modes")
    require(derivation["orders_checked"] == 2, "wrong order count")
    require(derivation["require_identical_endpoints"] is True, "endpoint flag")
    verify_realization(source_path, SOURCE_COUNTS)
    for mode in MODES:
        verify_growth(source_path, mode, source_cuts[mode])

    endpoints: list[tuple[list[int], dict[int, int]]] = []
    source_derivation_steps = 0
    for order in itertools.permutations(MODES):
        current_path, current_cuts = source_path, source_cuts
        for mode in order:
            current_path, current_cuts = advance(current_path, current_cuts, mode)
            source_derivation_steps += 1
        endpoints.append((current_path, current_cuts))
    require(endpoints[0] == endpoints[1], "two derivation orders disagree")

    margin = data["safe_margin"]
    require(tuple(margin["growth_modes"]) == MODES, "wrong margin modes")
    require(margin["maximum_edge_length"] == 11, "wrong maximum length")
    require(margin["maximum_pair_sum"] == 13, "wrong pair sum")
    require(margin["seed_order"] == 36, "wrong seed order")
    require(2 * 11 + 13 <= 36, "invalid safe margin")

    seed = data["seed"]
    require(tuple(seed["counts"]) == SEED_COUNTS, "wrong seed counts")
    seed_path = seed["path"]
    seed_cuts = normalize_cuts(seed["selected_growth_cuts"])
    require(seed_cuts == {2: 2, 11: 13}, "wrong seed cuts")
    require(endpoints[0] == (seed_path, seed_cuts), "stored endpoint mismatch")
    verify_safe_state(seed_path, SEED_COUNTS, seed_cuts)

    family: dict[tuple[int, int], tuple[list[int], dict[int, int]]] = {}
    record_hash = hashlib.sha256()
    family_paths_checked = 0
    coordinate_transitions_checked = 0
    commuting_squares_checked = 0

    q_path, q_cuts = seed_path, seed_cuts
    for q in range(grid + 2):
        r_path, r_cuts = q_path, q_cuts
        for r in range(grid + 2):
            counts = (1, 9 + 2 * q, 25 + 11 * r)
            verify_safe_state(r_path, counts, r_cuts)
            family[q, r] = (r_path, r_cuts)
            record_hash.update(
                json.dumps(
                    [q, r, r_cuts, r_path], separators=(",", ":"), sort_keys=True
                ).encode()
            )
            record_hash.update(b"\n")
            family_paths_checked += 1
            r_path, r_cuts = advance(r_path, r_cuts, 11)
        q_path, q_cuts = advance(q_path, q_cuts, 2)

    for q, r in itertools.product(range(grid + 1), repeat=2):
        current_path, current_cuts = family[q, r]
        require(
            advance(current_path, current_cuts, 2) == family[q + 1, r],
            ("2-transition", q, r),
        )
        require(
            advance(current_path, current_cuts, 11) == family[q, r + 1],
            ("11-transition", q, r),
        )
        coordinate_transitions_checked += 2
        first_two = advance(current_path, current_cuts, 2)
        two_then_eleven = advance(*first_two, 11)
        first_eleven = advance(current_path, current_cuts, 11)
        eleven_then_two = advance(*first_eleven, 2)
        require(
            two_then_eleven == eleven_then_two == family[q + 1, r + 1],
            ("commuting square", q, r),
        )
        commuting_squares_checked += 1

    if enforce_pinned_hash:
        require(certificate_sha256 == EXPECTED_CERTIFICATE_SHA256, "unpinned certificate")
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
    parser.add_argument("--grid", type=int, default=6)
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
