#!/usr/bin/env python3
"""Exact checker for the four-block odd-b, c=1 BHR family."""

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

EXPECTED_BEFORE_DIGEST = (
    "29dc950cba5a9d65ca59bb860568321ef2580e1a825175e14fabd89f1e4a2f1f"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "8031d3eda5e24ee5609effe05cd1da7998d944a60f64c677e4251909c4c28d8b"
)


def residual_slab_path(p: int, q: int) -> list[int]:
    """Return the four-block path P[p,q] from the written construction."""
    require(p >= -1 and q >= -6, ("parameter range", p, q))
    require(25 + p + 2 * q >= 22, ("order below 22", p, q))
    return (
        list(range(p + 1, p + 14 + 2 * q, 2))
        + list(range(p + 14 + 2 * q, p + 25 + 2 * q, 2))
        + list(range(0, p + 1))
        + list(range(p + 2, p + 13 + 2 * q, 2))
        + list(range(p + 23 + 2 * q, p + 14 + 2 * q, -2))
    )


def verify_formula_state(path: list[int], p: int, q: int) -> None:
    verify_realization(path, (2 + p, 21 + 2 * q, 1))
    maximum = max(
        cyclic_length(u, v, len(path)) for u, v in zip(path, path[1:])
    )
    require(maximum == 11, ("maximum edge length", maximum))


def verify_state(path: list[int], p: int, q: int) -> None:
    """Check the original transition-closed p,q>=0 slab."""
    require(p >= 0 and q >= 0, ("transition range", p, q))
    verify_formula_state(path, p, q)
    maximum = 11
    require(2 * maximum + 1 + 2 <= len(path), ("unsafe margin", len(path)))
    verify_growth(path, 1, 0)
    verify_growth(path, 2, p + 1)


def verify_certificate(
    path: Path, grid: int, enforce_pinned_hash: bool = True
) -> dict[str, Any]:
    require(grid >= 1, "grid must be positive")
    raw = path.read_bytes()
    certificate_sha256 = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    require(data["schema"] == "bhr-residual-slab-v1", "wrong schema")
    require(tuple(data["support"]) == SUPPORT, "wrong support")
    source = data["source_context"]
    require(source["residual_symbolic_patterns_before"] == 1492, "wrong prior count")
    require(
        source["residual_records_before_sha256"] == EXPECTED_BEFORE_DIGEST,
        "wrong prior digest",
    )
    generator = data["generator"]
    require(generator["ortools"] == "9.14.6206", "wrong generator version")
    require(generator["num_search_workers"] == 1, "wrong worker count")
    require(generator["random_seed"] == 1, "wrong generator seed")

    seed = data["seed"]
    require(tuple(seed["counts"]) == (2, 21, 1), "wrong seed counts")
    require(
        {int(mode): cut for mode, cut in seed["selected_growth_cuts"].items()}
        == {1: 0, 2: 1},
        "wrong seed cuts",
    )
    require(seed["path"] == residual_slab_path(0, 0), "wrong seed path")

    extended_formula_states_checked = 0
    for p in range(-1, grid + 2):
        for q in range(-6, grid + 2):
            if 25 + p + 2 * q < 22:
                continue
            verify_formula_state(residual_slab_path(p, q), p, q)
            extended_formula_states_checked += 1

    family: dict[tuple[int, int], list[int]] = {}
    record_hash = hashlib.sha256()
    family_paths_checked = 0
    coordinate_transitions_checked = 0
    commuting_squares_checked = 0

    for p in range(grid + 2):
        for q in range(grid + 2):
            current = residual_slab_path(p, q)
            verify_state(current, p, q)
            family[p, q] = current
            record_hash.update(
                json.dumps([p, q, current], separators=(",", ":")).encode()
            )
            record_hash.update(b"\n")
            family_paths_checked += 1

    for p in range(grid + 1):
        for q in range(grid + 1):
            current = family[p, q]
            require(
                grow_once(current, 1, 0) == family[p + 1, q],
                ("1-transition", p, q),
            )
            require(
                grow_once(current, 2, p + 1) == family[p, q + 1],
                ("2-transition", p, q),
            )
            coordinate_transitions_checked += 2
            first_one = grow_once(current, 1, 0)
            one_then_two = grow_once(first_one, 2, p + 2)
            first_two = grow_once(current, 2, p + 1)
            two_then_one = grow_once(first_two, 1, 0)
            require(
                one_then_two == two_then_one == family[p + 1, q + 1],
                ("commuting square", p, q),
            )
            commuting_squares_checked += 1

    if enforce_pinned_hash:
        require(
            certificate_sha256 == EXPECTED_CERTIFICATE_SHA256,
            "unpinned certificate",
        )
    return {
        "certificate_sha256": certificate_sha256,
        "python": platform.python_version(),
        "grid": grid,
        "extended_formula_states_checked": extended_formula_states_checked,
        "family_paths_checked": family_paths_checked,
        "coordinate_transitions_checked": coordinate_transitions_checked,
        "commuting_squares_checked": commuting_squares_checked,
        "record_sha256": record_hash.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=24)
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
