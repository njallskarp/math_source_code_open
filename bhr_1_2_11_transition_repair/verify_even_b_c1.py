#!/usr/bin/env python3
"""Exact checker for the two even-b, c=1 BHR boundary families."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
from typing import Any

from verify import (
    SUPPORT,
    cyclic_length,
    grow_once,
    require,
    verify_growth,
    verify_realization,
)

EXPECTED_CERTIFICATE_SHA256 = (
    "15516e949d8a480593a23629a2977bee9b234ae5ed41ffe790eb250efc2a5578"
)
EXPECTED_SOURCE_SHA256 = (
    "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
)


def family_a_path(q: int) -> list[int]:
    """Return A_q, realizing (1, 20+2q, 1)."""
    require(q >= 0, ("parameter range", q))
    return (
        list(range(8 + 2 * q, -1, -2))
        + list(range(21 + 2 * q, 12 + 2 * q, -2))
        + list(range(1, 12 + 2 * q, 2))
        + list(range(10 + 2 * q, 23 + 2 * q, 2))
    )


def family_b_path(q: int) -> list[int]:
    """Return B_q, realizing (2, 18+2q, 1)."""
    require(q >= 0, ("parameter range", q))
    return (
        list(range(8 + 2 * q, -1, -2))
        + list(range(20 + 2 * q, 11 + 2 * q, -2))
        + list(range(11 + 2 * q, 22 + 2 * q, 2))
        + [10 + 2 * q]
        + list(range(9 + 2 * q, 0, -2))
    )


def verify_state(path: list[int], counts: tuple[int, int, int]) -> None:
    verify_realization(path, counts)
    maximum = max(
        cyclic_length(u, v, len(path)) for u, v in zip(path, path[1:])
    )
    require(maximum == 11, ("maximum edge length", maximum))
    verify_growth(path, 2, 1)


def verify_certificate(
    path: Path, grid: int, enforce_pinned_hash: bool = True
) -> dict[str, Any]:
    require(grid >= 1, "grid must be positive")
    raw = path.read_bytes()
    certificate_sha256 = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    require(data["schema"] == "bhr-even-b-c1-completion-v1", "wrong schema")
    require(tuple(data["support"]) == SUPPORT, "wrong support")
    source = data["source_context"]
    require(
        source["source_certificate_sha256"] == EXPECTED_SOURCE_SHA256,
        "wrong source hash",
    )
    require(tuple(source["residue_case"]) == (1, 2, 1), "wrong residue case")
    require(source["source_witness_indices"] == [5, 13], "wrong source indices")

    records = data["families"]
    require([record["name"] for record in records] == ["A", "B"], "wrong families")
    formulas = (family_a_path, family_b_path)
    seed_counts = ((1, 20, 1), (2, 18, 1))
    record_hash = hashlib.sha256()
    family_paths_checked = 0
    transitions_checked = 0

    for record, formula, initial_counts in zip(records, formulas, seed_counts):
        require(tuple(record["counts_at_q_zero"]) == initial_counts, "wrong counts")
        selection = record["selected_growth_cut"]
        require(selection == {"mode": 2, "cut": 1}, "wrong growth selection")
        require(record["path_at_q_zero"] == formula(0), "wrong seed path")
        for q in range(grid + 2):
            current = formula(q)
            counts = (initial_counts[0], initial_counts[1] + 2 * q, 1)
            verify_state(current, counts)
            record_hash.update(
                json.dumps([record["name"], q, current], separators=(",", ":")).encode()
            )
            record_hash.update(b"\n")
            family_paths_checked += 1
            if q <= grid:
                require(
                    grow_once(current, 2, 1) == formula(q + 1),
                    ("2-transition", record["name"], q),
                )
                transitions_checked += 1

    if enforce_pinned_hash:
        require(certificate_sha256 == EXPECTED_CERTIFICATE_SHA256, "unpinned certificate")
    return {
        "certificate_sha256": certificate_sha256,
        "python": platform.python_version(),
        "grid": grid,
        "family_paths_checked": family_paths_checked,
        "transitions_checked": transitions_checked,
        "record_sha256": record_hash.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=64)
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
