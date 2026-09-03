#!/usr/bin/env python3
"""Derive the eleven-case small-a mantle certificate from the pinned source."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from audit_source_certificate import transported_cut
from verify import grow_once, require, verify_growth, verify_realization

SOURCE_SHA256 = "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
MODES = (2, 11)
SELECTED_WITNESS = {1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
                    7: 1, 8: 1, 9: 1, 10: 0, 11: 1}


def normalize_cuts(record: dict[str, int]) -> dict[int, int]:
    return {int(mode): cut for mode, cut in record.items() if int(mode) in MODES}


def advance(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    inserted_cut = cuts[inserted_mode]
    child = grow_once(path, inserted_mode, inserted_cut)
    child_cuts = {
        mode: transported_cut(cut, inserted_cut, inserted_mode)
        for mode, cut in cuts.items()
    }
    for mode in MODES:
        verify_growth(child, mode, child_cuts[mode])
    return child, child_cuts


def build(source_path: Path) -> dict[str, object]:
    raw = source_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "unpinned source")
    source = json.loads(raw)
    by_base = {tuple(case["base"]): case for case in source["cases"]}
    cases = []
    for c_residue in range(1, 12):
        base = (1, 1, c_residue)
        index = SELECTED_WITNESS[c_residue]
        witness = by_base[base]["witnesses"][index]
        counts = tuple(witness["counts"])
        path = witness["path"]
        cuts = normalize_cuts(witness["growth"])
        require(counts[0] == 1 and set(cuts) == set(MODES), (base, index))
        verify_realization(path, counts)
        for mode in MODES:
            verify_growth(path, mode, cuts[mode])

        endpoints = []
        for order in itertools.permutations(MODES):
            state = (path, cuts)
            for mode in order:
                state = advance(*state, mode)
            endpoints.append(state)
        require(endpoints[0] == endpoints[1], (base, "noncommuting derivation"))
        seed_path, seed_cuts = endpoints[0]
        seed_counts = (counts[0], counts[1] + 2, counts[2] + 11)
        verify_realization(seed_path, seed_counts)
        require(2 * 11 + sum(MODES) <= len(seed_path), (base, "unsafe seed"))
        cases.append(
            {
                "residue_case": list(base),
                "source_witness_index": index,
                "source": {
                    "counts": list(counts),
                    "path": path,
                    "selected_growth_cuts": {str(k): v for k, v in cuts.items()},
                },
                "derivation": {
                    "growth_modes_applied_once": list(MODES),
                    "orders_checked": 2,
                    "require_identical_endpoints": True,
                },
                "safe_seed": {
                    "counts": list(seed_counts),
                    "path": seed_path,
                    "selected_growth_cuts": {
                        str(k): v for k, v in seed_cuts.items()
                    },
                },
                "family": {
                    "counts": [1, f"{seed_counts[1]}+2q", f"{seed_counts[2]}+11r"],
                    "parameters": "q,r>=0",
                },
            }
        )

    return {
        "schema": "bhr-small-a-mantle-v1",
        "support": [1, 2, 11],
        "source_context": {
            "source_certificate_sha256": SOURCE_SHA256,
            "source_role": (
                "Selected paths are copied from the pinned finite certificate; "
                "every mathematical property used below is rechecked directly."
            ),
            "previous_coverage": 8151,
            "previous_residual_symbolic_patterns": 1393,
            "previous_residual_records_sha256": (
                "3d0e81150a2e5147b0b47e3a8ffdc3bb10085a54430e7562fac84bcace348e1a"
            ),
        },
        "safe_margin": {
            "growth_modes": list(MODES),
            "maximum_edge_length": 11,
            "maximum_pair_sum": sum(MODES),
            "required_order": 2 * 11 + sum(MODES),
            "minimum_seed_order": min(len(case["safe_seed"]["path"]) for case in cases),
        },
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_certificate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    data = build(args.source_certificate)
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print(f"cases={len(data['cases'])}")
    print(f"sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")
    print("BUILT")


if __name__ == "__main__":
    main()
