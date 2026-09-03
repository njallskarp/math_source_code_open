#!/usr/bin/env python3
"""Exact checker for all eleven transition-closed small-a mantle slabs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
from typing import Any

from audit_source_certificate import transported_cut
from verify import SUPPORT, cyclic_length, grow_once, require, verify_growth, verify_realization

MODES = (2, 11)
EXPECTED_CERTIFICATE_SHA256 = (
    "7669175bf86a2ad4938bc1cd8a1aae8e7a64b5e59bcfc4904b6e6b4d7646a192"
)
EXPECTED_SOURCE_SHA256 = (
    "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
)
EXPECTED_SOURCE_INDICES = {1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
                           7: 1, 8: 1, 9: 1, 10: 0, 11: 1}
EXPECTED_SEED_COUNTS = {
    1: (1, 11, 23), 2: (1, 11, 24), 3: (1, 9, 25),
    4: (1, 9, 26), 5: (1, 9, 27), 6: (1, 9, 28),
    7: (1, 9, 29), 8: (1, 9, 30), 9: (1, 15, 20),
    10: (1, 13, 21), 11: (1, 13, 22),
}


def normalize_cuts(record: dict[str, int]) -> dict[int, int]:
    return {int(mode): cut for mode, cut in record.items()}


def advance(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    require(set(cuts) == set(MODES), ("cut modes", cuts))
    inserted_cut = cuts[inserted_mode]
    child = grow_once(path, inserted_mode, inserted_cut)
    child_cuts = {
        mode: transported_cut(cut, inserted_cut, inserted_mode)
        for mode, cut in cuts.items()
    }
    for mode in MODES:
        verify_growth(child, mode, child_cuts[mode])
    return child, child_cuts


def verify_state(
    path: list[int], counts: tuple[int, int, int], cuts: dict[int, int], safe: bool
) -> None:
    verify_realization(path, counts)
    maximum = max(cyclic_length(u, v, len(path)) for u, v in zip(path, path[1:]))
    require(maximum == 11, ("maximum edge length", maximum))
    if safe:
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
    require(data["schema"] == "bhr-small-a-mantle-v1", "wrong schema")
    require(tuple(data["support"]) == SUPPORT, "wrong support")
    if enforce_pinned_hash:
        require(certificate_sha256 == EXPECTED_CERTIFICATE_SHA256, "unpinned certificate")

    context = data["source_context"]
    require(context["source_certificate_sha256"] == EXPECTED_SOURCE_SHA256, "source hash")
    require(context["previous_coverage"] == 8151, "prior coverage")
    require(context["previous_residual_symbolic_patterns"] == 1393, "prior residual")
    require(
        context["previous_residual_records_sha256"]
        == "3d0e81150a2e5147b0b47e3a8ffdc3bb10085a54430e7562fac84bcace348e1a",
        "prior residual digest",
    )

    margin = data["safe_margin"]
    require(tuple(margin["growth_modes"]) == MODES, "wrong modes")
    require(margin["maximum_edge_length"] == 11, "wrong maximum")
    require(margin["maximum_pair_sum"] == 13, "wrong pair sum")
    require(margin["required_order"] == 35, "wrong required order")
    require(margin["minimum_seed_order"] == 36, "wrong minimum order")

    cases = data["cases"]
    require(len(cases) == 11, "wrong case count")
    require(
        {tuple(case["residue_case"]) for case in cases}
        == {(1, 1, c) for c in range(1, 12)},
        "missing or duplicate residue",
    )

    record_hash = hashlib.sha256()
    seed_set_hash = hashlib.sha256()
    source_steps = family_paths = transitions = squares = 0
    minimum_order = 10**9
    for case in sorted(cases, key=lambda item: item["residue_case"]):
        base = tuple(case["residue_case"])
        c_residue = base[2]
        require(case["source_witness_index"] == EXPECTED_SOURCE_INDICES[c_residue], base)
        source = case["source"]
        source_counts = tuple(source["counts"])
        source_path = source["path"]
        source_cuts = normalize_cuts(source["selected_growth_cuts"])
        require(source_counts[0] == 1, (base, "source a"))
        require(source_counts[1] % 2 == 1, (base, "source parity"))
        require((source_counts[2] - c_residue) % 11 == 0, (base, "source residue"))
        require(set(source_cuts) == set(MODES), (base, "source modes"))
        verify_state(source_path, source_counts, source_cuts, safe=False)

        derivation = case["derivation"]
        require(tuple(derivation["growth_modes_applied_once"]) == MODES, base)
        require(derivation["orders_checked"] == 2, base)
        require(derivation["require_identical_endpoints"] is True, base)
        endpoints = []
        for order in itertools.permutations(MODES):
            state = (source_path, source_cuts)
            for mode in order:
                state = advance(*state, mode)
                source_steps += 1
            endpoints.append(state)
        require(endpoints[0] == endpoints[1], (base, "derivation orders"))

        seed = case["safe_seed"]
        seed_counts = tuple(seed["counts"])
        seed_path = seed["path"]
        seed_cuts = normalize_cuts(seed["selected_growth_cuts"])
        require(seed_counts == EXPECTED_SEED_COUNTS[c_residue], (base, "seed counts"))
        require(seed_counts == (source_counts[0], source_counts[1] + 2, source_counts[2] + 11), base)
        require(endpoints[0] == (seed_path, seed_cuts), (base, "stored endpoint"))
        verify_state(seed_path, seed_counts, seed_cuts, safe=True)
        minimum_order = min(minimum_order, len(seed_path))
        seed_set_hash.update(
            json.dumps([c_residue, seed_path], separators=(",", ":")).encode()
        )
        seed_set_hash.update(b"\n")
        require(case["family"]["parameters"] == "q,r>=0", base)
        require(
            case["family"]["counts"]
            == [1, f"{seed_counts[1]}+2q", f"{seed_counts[2]}+11r"],
            (base, "family"),
        )

        family: dict[tuple[int, int], tuple[list[int], dict[int, int]]] = {}
        q_state = (seed_path, seed_cuts)
        for q in range(grid + 2):
            r_state = q_state
            for r in range(grid + 2):
                current_path, current_cuts = r_state
                current_counts = (1, seed_counts[1] + 2 * q, seed_counts[2] + 11 * r)
                verify_state(current_path, current_counts, current_cuts, safe=True)
                family[q, r] = r_state
                record_hash.update(
                    json.dumps(
                        [c_residue, q, r, current_cuts, current_path],
                        separators=(",", ":"), sort_keys=True,
                    ).encode()
                )
                record_hash.update(b"\n")
                family_paths += 1
                r_state = advance(*r_state, 11)
            q_state = advance(*q_state, 2)

        for q, r in itertools.product(range(grid + 1), repeat=2):
            state = family[q, r]
            require(advance(*state, 2) == family[q + 1, r], (base, q, r, 2))
            require(advance(*state, 11) == family[q, r + 1], (base, q, r, 11))
            require(
                advance(*advance(*state, 2), 11)
                == advance(*advance(*state, 11), 2)
                == family[q + 1, r + 1],
                (base, q, r, "square"),
            )
            transitions += 2
            squares += 1

    require(minimum_order == margin["minimum_seed_order"], "minimum order mismatch")
    return {
        "certificate_sha256": certificate_sha256,
        "python": platform.python_version(),
        "residue_classes": len(cases),
        "source_derivation_steps": source_steps,
        "minimum_seed_order": minimum_order,
        "seed_paths_sha256": seed_set_hash.hexdigest(),
        "grid": grid,
        "family_paths_checked": family_paths,
        "coordinate_transitions_checked": transitions,
        "commuting_squares_checked": squares,
        "record_sha256": record_hash.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=6)
    parser.add_argument("--allow-unpinned", action="store_true")
    args = parser.parse_args()
    result = verify_certificate(args.certificate, args.grid, not args.allow_unpinned)
    for key, value in result.items():
        if isinstance(value, dict):
            value = json.dumps(value, separators=(",", ":"), sort_keys=True)
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
