#!/usr/bin/env python3
"""Exact checker for the transition-closed all-residue a=2 mantle."""

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

PAIR_MODES = (2, 11)
EXISTING_RESIDUES = (1, 10)
EXPECTED_CERTIFICATE_SHA256 = (
    "601a48ad69abef99c6279c8420492c16c9000120069affad74686388d4ccca4e"
)
EXPECTED_SOURCE_SHA256 = (
    "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
)
EXPECTED_TRIMODAL_SHA256 = (
    "532470ffe31ff3e5acb4da51a78c15f172d2d00db6816dd43d5dc44a243bc059"
)
EXPECTED_SEEDS = {
    1: (2, 11, 23), 2: (2, 9, 24), 3: (2, 9, 25),
    4: (2, 9, 26), 5: (2, 9, 27), 6: (2, 9, 28),
    7: (2, 9, 29), 8: (2, 9, 30), 9: (2, 13, 20),
    10: (2, 13, 21), 11: (2, 11, 22),
}


def normalize_cuts(record: dict[str, int]) -> dict[int, int]:
    return {int(mode): cut for mode, cut in record.items()}


def advance(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    require(inserted_mode in cuts, ("missing mode", inserted_mode))
    inserted_cut = cuts[inserted_mode]
    child = grow_once(path, inserted_mode, inserted_cut)
    child_cuts = {
        mode: transported_cut(cut, inserted_cut, inserted_mode)
        for mode, cut in cuts.items()
    }
    for mode, cut in child_cuts.items():
        verify_growth(child, mode, cut)
    return child, child_cuts


def verify_state(
    path: list[int], counts: tuple[int, int, int], cuts: dict[int, int], safe: bool
) -> None:
    verify_realization(path, counts)
    maximum = max(cyclic_length(u, v, len(path)) for u, v in zip(path, path[1:]))
    require(maximum == 11, ("maximum edge length", maximum))
    if safe:
        require(2 * maximum + 13 <= len(path), ("unsafe seed", len(path)))
    for mode, cut in cuts.items():
        verify_growth(path, mode, cut)


def verify_external_provenance(
    data: dict[str, Any], source_path: Path | None, trimodal_path: Path | None
) -> bool:
    if source_path is None and trimodal_path is None:
        return False
    require(source_path is not None and trimodal_path is not None, "supply both provenance files")
    source_raw = source_path.read_bytes()
    trimodal_raw = trimodal_path.read_bytes()
    require(hashlib.sha256(source_raw).hexdigest() == EXPECTED_SOURCE_SHA256, "source bytes")
    require(hashlib.sha256(trimodal_raw).hexdigest() == EXPECTED_TRIMODAL_SHA256, "trimodal bytes")
    source = json.loads(source_raw)
    trimodal = json.loads(trimodal_raw)
    source_by_base = {tuple(case["base"]): case for case in source["cases"]}
    trimodal_by_base = {tuple(case["residue_case"]): case for case in trimodal["cases"]}
    for case in data["cases"]:
        base = tuple(case["residue_case"])
        witness = source_by_base[base]["witnesses"][case["source_witness_index"]]
        stored_source = case["source"]
        require(stored_source["counts"] == witness["counts"], (base, "source counts"))
        require(stored_source["path"] == witness["path"], (base, "source path"))
        for mode, cut in stored_source["selected_growth_cuts"].items():
            require(witness["growth"][mode] == cut, (base, mode, "source cut"))
        if base[2] in EXISTING_RESIDUES:
            stored_seed = trimodal_by_base[base]["safe_seed"]
            require(case["safe_seed"] == stored_seed, (base, "trimodal endpoint"))
        else:
            seed = case["safe_seed"]
            seed_cuts = normalize_cuts(seed["selected_growth_cuts"])
            stored_seed = trimodal_by_base[base]["safe_seed"]
            stored_cuts = normalize_cuts(stored_seed["selected_growth_cuts"])
            require(
                advance(seed["path"], seed_cuts, 1)
                == (stored_seed["path"], stored_cuts),
                (base, "trimodal successor"),
            )
    return True


def verify_certificate(
    path: Path,
    grid: int,
    enforce_pinned_hash: bool = True,
    source_path: Path | None = None,
    trimodal_path: Path | None = None,
) -> dict[str, Any]:
    require(grid >= 1, "grid must be positive")
    raw = path.read_bytes()
    certificate_sha256 = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    require(data["schema"] == "bhr-a2-mantle-v1", "wrong schema")
    require(tuple(data["support"]) == SUPPORT, "wrong support")
    if enforce_pinned_hash:
        require(certificate_sha256 == EXPECTED_CERTIFICATE_SHA256, "unpinned certificate")

    context = data["source_context"]
    require(context["source_certificate_sha256"] == EXPECTED_SOURCE_SHA256, "source hash")
    require(context["trimodal_certificate_sha256"] == EXPECTED_TRIMODAL_SHA256, "trimodal hash")
    require(tuple(context["trimodal_safe_residues_rederived"]) == EXISTING_RESIDUES, "safe residues")
    require(context["trimodal_successor_links_checked"] == 11, "successor link count")
    require(context["previous_coverage"] == 8211, "prior coverage")
    require(context["previous_residual_symbolic_patterns"] == 1333, "prior residual")
    require(
        context["previous_residual_records_sha256"]
        == "00ed42e9e22d87d0a202e6b0e55ddc284cf8a7fff3479cff98df18e7def54b27",
        "prior residual digest",
    )
    external_checked = verify_external_provenance(data, source_path, trimodal_path)

    margin = data["safe_margin"]
    require(tuple(margin["growth_modes"]) == SUPPORT, "wrong family modes")
    require(margin["maximum_edge_length"] == 11, "wrong maximum")
    require(margin["maximum_pair_sum"] == 13, "wrong pair sum")
    require(margin["required_order"] == 35, "wrong required order")
    require(margin["minimum_seed_order"] == 36, "wrong minimum order")

    cases = data["cases"]
    require(len(cases) == 11, "wrong case count")
    require(
        {tuple(case["residue_case"]) for case in cases}
        == {(1, 1, residue) for residue in range(1, 12)},
        "missing or duplicate residue",
    )

    record_hash = hashlib.sha256()
    seed_set_hash = hashlib.sha256()
    source_steps = family_paths = transitions = squares = 0
    provenance_counts = {"a2_source_two_mode_derivation_retaining_mode_1": 0,
                         "rederived_existing_trimodal_safe_seed": 0}
    for case in sorted(cases, key=lambda item: item["residue_case"]):
        base = tuple(case["residue_case"])
        residue = base[2]
        require(case["source_witness_index"] == 0, (base, "source index"))
        expected_provenance = (
            "rederived_existing_trimodal_safe_seed"
            if residue in EXISTING_RESIDUES
            else "a2_source_two_mode_derivation_retaining_mode_1"
        )
        require(case["provenance"] == expected_provenance, (base, "provenance"))
        provenance_counts[expected_provenance] += 1

        source = case["source"]
        source_counts = tuple(source["counts"])
        source_path = source["path"]
        source_cuts = normalize_cuts(source["selected_growth_cuts"])
        expected_modes = SUPPORT if residue in EXISTING_RESIDUES else PAIR_MODES
        require(tuple(source_cuts) == SUPPORT, (base, "source modes"))
        require(source_counts[0] == (1 if residue in EXISTING_RESIDUES else 2), base)
        require(source_counts[1] % 2 == 1, (base, "source parity"))
        require((source_counts[2] - residue) % 11 == 0, (base, "source residue"))
        verify_state(source_path, source_counts, source_cuts, safe=False)

        derivation = case["derivation"]
        require(tuple(derivation["growth_modes_applied_once"]) == expected_modes, base)
        expected_orders = 6 if residue in EXISTING_RESIDUES else 2
        require(derivation["orders_checked"] == expected_orders, (base, "order count"))
        require(derivation["require_identical_endpoints"] is True, base)
        endpoints = []
        for order in itertools.permutations(expected_modes):
            state = (source_path, source_cuts)
            for mode in order:
                state = advance(*state, mode)
                source_steps += 1
            endpoints.append(state)
        require(all(endpoint == endpoints[0] for endpoint in endpoints), (base, "orders"))

        seed = case["safe_seed"]
        seed_counts = tuple(seed["counts"])
        seed_path = seed["path"]
        seed_cuts = normalize_cuts(seed["selected_growth_cuts"])
        require(seed_counts == EXPECTED_SEEDS[residue], (base, "seed counts"))
        expected_counts = tuple(
            count + mode if mode in expected_modes else count
            for count, mode in zip(source_counts, SUPPORT)
        )
        require(seed_counts == expected_counts, (base, "source increment"))
        require(endpoints[0] == (seed_path, seed_cuts), (base, "stored endpoint"))
        verify_state(seed_path, seed_counts, seed_cuts, safe=True)

        family = case["family"]
        require(tuple(family["growth_modes"]) == SUPPORT, base)
        require(family["parameters"] == "p,q,r>=0", base)
        require(
            family["counts"] == ["2+p", f"{seed_counts[1]}+2q", f"{seed_counts[2]}+11r"],
            (base, "family"),
        )
        seed_set_hash.update(
            json.dumps([residue, seed_path], separators=(",", ":")).encode()
        )
        seed_set_hash.update(b"\n")

        family_states: dict[
            tuple[int, int, int], tuple[list[int], dict[int, int]]
        ] = {}
        p_state = (seed_path, seed_cuts)
        for p in range(grid + 2):
            q_state = p_state
            for q in range(grid + 2):
                r_state = q_state
                for r in range(grid + 2):
                    current_path, current_cuts = r_state
                    current_counts = (
                        2 + p, seed_counts[1] + 2 * q, seed_counts[2] + 11 * r
                    )
                    verify_state(current_path, current_counts, current_cuts, safe=True)
                    family_states[p, q, r] = r_state
                    record_hash.update(
                        json.dumps(
                            [residue, p, q, r, current_cuts, current_path],
                            separators=(",", ":"), sort_keys=True,
                        ).encode()
                    )
                    record_hash.update(b"\n")
                    family_paths += 1
                    r_state = advance(*r_state, 11)
                q_state = advance(*q_state, 2)
            p_state = advance(*p_state, 1)

        for p, q, r in itertools.product(range(grid + 1), repeat=3):
            state = family_states[p, q, r]
            for coordinate, mode in enumerate(SUPPORT):
                index = [p, q, r]
                index[coordinate] += 1
                require(
                    advance(*state, mode) == family_states[tuple(index)],
                    (base, p, q, r, mode),
                )
                transitions += 1
            for first, second in itertools.combinations(SUPPORT, 2):
                require(
                    advance(*advance(*state, first), second)
                    == advance(*advance(*state, second), first),
                    (base, p, q, r, first, second),
                )
                squares += 1

    require(provenance_counts == {
        "a2_source_two_mode_derivation_retaining_mode_1": 9,
        "rederived_existing_trimodal_safe_seed": 2,
    }, "provenance totals")
    return {
        "certificate_sha256": certificate_sha256,
        "python": platform.python_version(),
        "residue_classes": len(cases),
        "two_mode_sources": provenance_counts["a2_source_two_mode_derivation_retaining_mode_1"],
        "existing_safe_residues_rederived": provenance_counts["rederived_existing_trimodal_safe_seed"],
        "external_provenance_checked": external_checked,
        "trimodal_successor_links_checked": 11 if external_checked else 0,
        "source_derivation_steps": source_steps,
        "minimum_seed_order": min(sum(counts) + 1 for counts in EXPECTED_SEEDS.values()),
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
    parser.add_argument("--grid", type=int, default=3)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--trimodal", type=Path)
    parser.add_argument("--allow-unpinned", action="store_true")
    args = parser.parse_args()
    result = verify_certificate(
        args.certificate, args.grid, not args.allow_unpinned, args.source, args.trimodal
    )
    for key, value in result.items():
        print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
