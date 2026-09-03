#!/usr/bin/env python3
"""Derive the eleven-case a=2 mantle from the two pinned certificates."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from audit_source_certificate import transported_cut
from verify import grow_once, require, verify_growth, verify_realization

SUPPORT = (1, 2, 11)
FAMILY_MODES = (2, 11)
SOURCE_SHA256 = "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
TRIMODAL_SHA256 = "532470ffe31ff3e5acb4da51a78c15f172d2d00db6816dd43d5dc44a243bc059"
EXISTING_SAFE_RESIDUES = (1, 10)


def normalize_cuts(record: dict[str, int], modes: tuple[int, ...]) -> dict[int, int]:
    return {mode: record[str(mode)] for mode in modes}


def advance(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    inserted_cut = cuts[inserted_mode]
    child = grow_once(path, inserted_mode, inserted_cut)
    child_cuts = {
        mode: transported_cut(cut, inserted_cut, inserted_mode)
        for mode, cut in cuts.items()
    }
    for mode, cut in child_cuts.items():
        verify_growth(child, mode, cut)
    return child, child_cuts


def pinned_json(path: Path, expected_sha256: str, label: str) -> dict[str, object]:
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == expected_sha256, f"unpinned {label}")
    return json.loads(raw)


def build(source_path: Path, trimodal_path: Path) -> dict[str, object]:
    source = pinned_json(source_path, SOURCE_SHA256, "source certificate")
    trimodal = pinned_json(trimodal_path, TRIMODAL_SHA256, "trimodal certificate")
    source_by_base = {tuple(case["base"]): case for case in source["cases"]}
    trimodal_by_base = {
        tuple(case["residue_case"]): case for case in trimodal["cases"]
    }
    cases = []
    for c_residue in range(1, 12):
        base = (1, 1, c_residue)
        witness_index = 0
        witness = source_by_base[base]["witnesses"][witness_index]
        derivation_modes = SUPPORT if c_residue in EXISTING_SAFE_RESIDUES else FAMILY_MODES
        counts = tuple(witness["counts"])
        require(
            counts[0] == (1 if c_residue in EXISTING_SAFE_RESIDUES else 2),
            (base, "source a"),
        )
        require(set(SUPPORT).issubset(witness["grow"]), (base, "source modes"))
        path = witness["path"]
        cuts = normalize_cuts(witness["growth"], SUPPORT)
        verify_realization(path, counts)
        for mode in SUPPORT:
            verify_growth(path, mode, cuts[mode])

        endpoints = []
        for order in itertools.permutations(derivation_modes):
            state = (path, cuts)
            for mode in order:
                state = advance(*state, mode)
            endpoints.append(state)
        require(all(endpoint == endpoints[0] for endpoint in endpoints), (base, "orders"))
        seed_path, seed_cuts = endpoints[0]
        seed_counts = tuple(
            count + mode if mode in derivation_modes else count
            for count, mode in zip(counts, SUPPORT)
        )
        require(seed_counts[0] == 2, (base, "seed a"))
        verify_realization(seed_path, seed_counts)
        require(2 * 11 + sum(FAMILY_MODES) <= len(seed_path), (base, "unsafe seed"))

        provenance = "a2_source_two_mode_derivation_retaining_mode_1"
        stored = trimodal_by_base[base]["safe_seed"]
        stored_cuts = {int(mode): cut for mode, cut in stored["selected_growth_cuts"].items()}
        if c_residue in EXISTING_SAFE_RESIDUES:
            require(
                (seed_path, seed_cuts) == (stored["path"], stored_cuts),
                (base, "trimodal provenance mismatch"),
            )
            provenance = "rederived_existing_trimodal_safe_seed"
        else:
            require(
                advance(seed_path, seed_cuts, 1) == (stored["path"], stored_cuts),
                (base, "trimodal successor mismatch"),
            )

        cases.append(
            {
                "residue_case": list(base),
                "provenance": provenance,
                "source_witness_index": witness_index,
                "source": {
                    "counts": list(counts),
                    "path": path,
                    "selected_growth_cuts": {str(k): v for k, v in cuts.items()},
                },
                "derivation": {
                    "growth_modes_applied_once": list(derivation_modes),
                    "orders_checked": len(list(itertools.permutations(derivation_modes))),
                    "require_identical_endpoints": True,
                },
                "safe_seed": {
                    "counts": list(seed_counts),
                    "path": seed_path,
                    "selected_growth_cuts": {str(k): v for k, v in seed_cuts.items()},
                },
                "family": {
                    "growth_modes": list(SUPPORT),
                    "counts": ["2+p", f"{seed_counts[1]}+2q", f"{seed_counts[2]}+11r"],
                    "parameters": "p,q,r>=0",
                },
            }
        )

    return {
        "schema": "bhr-a2-mantle-v1",
        "support": list(SUPPORT),
        "source_context": {
            "source_certificate_sha256": SOURCE_SHA256,
            "trimodal_certificate_sha256": TRIMODAL_SHA256,
            "trimodal_safe_residues_rederived": list(EXISTING_SAFE_RESIDUES),
            "trimodal_successor_links_checked": 11,
            "source_role": (
                "Every starting path is copied from the pinned source and rechecked; "
                "all three cuts are tracked through the derivation, and the two existing "
                "seeds are also required to equal the pinned trimodal endpoints."
            ),
            "previous_coverage": 8211,
            "previous_residual_symbolic_patterns": 1333,
            "previous_residual_records_sha256": (
                "00ed42e9e22d87d0a202e6b0e55ddc284cf8a7fff3479cff98df18e7def54b27"
            ),
        },
        "safe_margin": {
            "growth_modes": list(SUPPORT),
            "maximum_edge_length": 11,
            "maximum_pair_sum": sum(FAMILY_MODES),
            "required_order": 2 * 11 + sum(FAMILY_MODES),
            "minimum_seed_order": min(len(case["safe_seed"]["path"]) for case in cases),
        },
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_certificate", type=Path)
    parser.add_argument("trimodal_certificate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    data = build(args.source_certificate, args.trimodal_certificate)
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print(f"cases={len(data['cases'])}")
    print(f"sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")
    print("BUILT")


if __name__ == "__main__":
    main()
