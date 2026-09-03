#!/usr/bin/env python3
"""Audit cross-growth transitions in the pinned finite BHR certificate.

The upstream checker verifies each advertised growth mode separately and then
uses a coordinatewise coverage predicate.  This audit performs the missing
transition check: after every advertised growth operation it tests every
advertised mode again, both at the naturally transported cut and at every
legal cut.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from verify import grow_once, growth_cuts, require, verify_growth, verify_realization

EXPECTED_SOURCE_SHA256 = (
    "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
)
EXPECTED_COUNTS = {
    "cases": 22,
    "witnesses": 628,
    "transition_obligations": 1093,
    "predicted_cut_failures": 18,
    "total_mode_losses": 11,
    "affected_witnesses": 8,
    "dead_first_interior_targets": 8,
    "uniquely_covered_dead_targets": 8,
}


def transported_cut(tested_cut: int, inserted_cut: int, inserted_size: int) -> int:
    """Transport a cut through the order-preserving gap insertion."""
    return tested_cut if tested_cut <= inserted_cut else tested_cut + inserted_size


def abstractly_covers(witness: dict[str, Any], target: tuple[int, int, int]) -> bool:
    """Reproduce the upstream coordinatewise coverage predicate."""
    grow = set(witness["grow"])
    for start, end, mode in zip(witness["counts"], target, (1, 2, 11)):
        if mode in grow:
            if end < start or (end - start) % mode:
                return False
        elif end != start:
            return False
    return True


def audit_certificate(path: Path, enforce_pinned_hash: bool = True) -> dict[str, Any]:
    raw = path.read_bytes()
    source_sha256 = hashlib.sha256(raw).hexdigest()
    if enforce_pinned_hash:
        require(source_sha256 == EXPECTED_SOURCE_SHA256, "unpinned source certificate")
    data = json.loads(raw)
    require(tuple(data["underlying_set"]) == (1, 2, 11), "wrong support")

    witnesses = 0
    obligations = 0
    predicted_failures: list[dict[str, Any]] = []
    total_losses: list[dict[str, Any]] = []

    for case in data["cases"]:
        residue_case = list(case["base"])
        for witness_index, witness in enumerate(case["witnesses"]):
            witnesses += 1
            counts = tuple(witness["counts"])
            path0 = witness["path"]
            advertised = tuple(witness["grow"])
            cuts = {int(x): m for x, m in witness["growth"].items()}
            verify_realization(path0, counts)
            require(set(advertised) == set(cuts), (residue_case, witness_index, "cuts"))
            for inserted_mode in advertised:
                inserted_cut = cuts[inserted_mode]
                verify_growth(path0, inserted_mode, inserted_cut)
                grown = grow_once(path0, inserted_mode, inserted_cut)
                enlarged = list(counts)
                enlarged[(1, 2, 11).index(inserted_mode)] += inserted_mode
                verify_realization(grown, tuple(enlarged))
                for tested_mode in advertised:
                    obligations += 1
                    predicted_cut = transported_cut(
                        cuts[tested_mode], inserted_cut, inserted_mode
                    )
                    surviving_cuts = growth_cuts(grown, tested_mode)
                    if predicted_cut not in surviving_cuts:
                        record = {
                            "residue_case": residue_case,
                            "witness_index": witness_index,
                            "counts": list(counts),
                            "inserted_mode": inserted_mode,
                            "tested_mode": tested_mode,
                            "inserted_cut": inserted_cut,
                            "old_tested_cut": cuts[tested_mode],
                            "predicted_cut": predicted_cut,
                            "surviving_cuts": surviving_cuts,
                        }
                        predicted_failures.append(record)
                        if not surviving_cuts:
                            total_losses.append(record)

    affected = {
        (tuple(r["residue_case"]), r["witness_index"]) for r in total_losses
    }
    cases_by_base = {tuple(case["base"]): case for case in data["cases"]}
    dead_targets: list[dict[str, Any]] = []
    for residue_case, witness_index in sorted(affected):
        case = cases_by_base[residue_case]
        witness = case["witnesses"][witness_index]
        require(set(witness["grow"]) == {1, 2}, (residue_case, witness_index, "modes"))
        target = tuple(
            count + increment for count, increment in zip(witness["counts"], (1, 2, 0))
        )
        covering_indices = [
            index
            for index, candidate in enumerate(case["witnesses"])
            if abstractly_covers(candidate, target)
        ]
        dead_targets.append(
            {
                "residue_case": list(residue_case),
                "witness_index": witness_index,
                "boundary_counts": witness["counts"],
                "first_interior_target": list(target),
                "abstract_covering_witness_indices": covering_indices,
            }
        )
    summary: dict[str, Any] = {
        "source_sha256": source_sha256,
        "cases": len(data["cases"]),
        "witnesses": witnesses,
        "transition_obligations": obligations,
        "predicted_cut_failures": len(predicted_failures),
        "total_mode_losses": len(total_losses),
        "affected_witnesses": len(affected),
        "dead_first_interior_targets": len(dead_targets),
        "uniquely_covered_dead_targets": sum(
            record["abstract_covering_witness_indices"] == [record["witness_index"]]
            for record in dead_targets
        ),
        "dead_targets": dead_targets,
        "failures": predicted_failures,
    }
    canonical = json.dumps(predicted_failures, separators=(",", ":"), sort_keys=True)
    summary["failure_records_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    for key, expected in EXPECTED_COUNTS.items():
        require(summary[key] == expected, (key, summary[key], expected))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument(
        "--allow-unpinned",
        action="store_true",
        help="audit another certificate without enforcing the reference SHA-256",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = audit_certificate(args.certificate, not args.allow_unpinned)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for key in (
            "source_sha256",
            "cases",
            "witnesses",
            "transition_obligations",
            "predicted_cut_failures",
            "total_mode_losses",
            "affected_witnesses",
            "dead_first_interior_targets",
            "uniquely_covered_dead_targets",
            "failure_records_sha256",
        ):
            print(f"{key}={result[key]}")
        print("AUDITED")


if __name__ == "__main__":
    main()
