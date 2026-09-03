#!/usr/bin/env python3
"""Exact checker for 22 complete transition-closed BHR cap orthants."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
from typing import Any

from audit_source_certificate import transported_cut
from verify import cyclic_length, grow_once, require, verify_growth, verify_realization
from verify_trimodal import (
    EXPECTED_SOURCE_COMMIT,
    EXPECTED_SOURCE_SHA256,
    MAXIMUM_LENGTH,
    MODES,
    advance,
    expected_bases,
    normalize_cuts,
)

EXPECTED_TRIMODAL_SHA256 = (
    "532470ffe31ff3e5acb4da51a78c15f172d2d00db6816dd43d5dc44a243bc059"
)


def increment_counts(
    counts: tuple[int, int, int], increments: dict[int, int]
) -> tuple[int, int, int]:
    return tuple(
        count + mode * increments.get(mode, 0)
        for count, mode in zip(counts, MODES)
    )


def advance_selected(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    """Grow in one selected mode and transport exactly the selected cuts."""
    require(inserted_mode in cuts, ("unselected insertion", inserted_mode, cuts))
    inserted_cut = cuts[inserted_mode]
    child = grow_once(path, inserted_mode, inserted_cut)
    child_cuts = {
        tested_mode: transported_cut(
            cuts[tested_mode], inserted_cut, inserted_mode
        )
        for tested_mode in cuts
    }
    for tested_mode, tested_cut in child_cuts.items():
        verify_growth(child, tested_mode, tested_cut)
    return child, child_cuts


def verify_selected_state(
    path: list[int],
    counts: tuple[int, int, int],
    cuts: dict[int, int],
) -> None:
    """Check a one- or two-mode safe-margin state from definitions."""
    verify_realization(path, counts)
    maximum = max(
        cyclic_length(u, v, len(path)) for u, v in zip(path, path[1:])
    )
    require(maximum == MAXIMUM_LENGTH, ("maximum edge length", maximum))
    for first, second in itertools.combinations(cuts, 2):
        require(
            2 * maximum + first + second <= len(path),
            ("unsafe pair", len(path), maximum, first, second),
        )
    for mode, cut in cuts.items():
        verify_growth(path, mode, cut)


def verify_certificate(
    path: Path, grid: int, enforce_pinned_hash: bool = True
) -> dict[str, Any]:
    require(grid >= 1, "grid must be positive")
    raw = path.read_bytes()
    certificate_sha256 = hashlib.sha256(raw).hexdigest()
    if enforce_pinned_hash:
        require(certificate_sha256 == EXPECTED_TRIMODAL_SHA256, "unpinned certificate")
    data = json.loads(raw)
    require(data["schema"] == "bhr-trimodal-safe-cores-v1", "wrong schema")
    require(tuple(data["support"]) == MODES, "wrong support")
    source = data["source_artifact"]
    require(source["repository_commit"] == EXPECTED_SOURCE_COMMIT, "wrong source commit")
    require(source["certificate_sha256"] == EXPECTED_SOURCE_SHA256, "wrong source hash")
    require(len(data["cases"]) == 22, "wrong case count")
    require(
        {tuple(case["residue_case"]) for case in data["cases"]} == expected_bases(),
        "missing or duplicate residue case",
    )

    face_seeds = 0
    face_derivation_steps = 0
    tri_seed_links_checked = 0
    ray_paths_checked = 0
    face_family_paths_checked = 0
    face_coordinate_transitions_checked = 0
    face_commuting_squares_checked = 0
    record_hash = hashlib.sha256()

    for case_index, case in enumerate(data["cases"]):
        base = tuple(case["residue_case"])
        cap = case["cap_seed"]
        cap_counts = tuple(cap["counts"])
        require(
            all(
                (count - residue) % mode == 0
                for count, residue, mode in zip(cap_counts, base, MODES)
            ),
            (base, "cap residue"),
        )
        cap_path = cap["path"]
        cap_cuts = normalize_cuts(cap["selected_growth_cuts"])
        verify_realization(cap_path, cap_counts)
        require(set(cap_cuts) == set(MODES), (base, "cap modes"))
        for mode in MODES:
            verify_growth(cap_path, mode, cap_cuts[mode])

        safe = case["safe_seed"]
        safe_endpoint = (
            safe["path"],
            normalize_cuts(safe["selected_growth_cuts"]),
        )
        require(
            tuple(safe["counts"])
            == increment_counts(cap_counts, {mode: 1 for mode in MODES}),
            (base, "safe seed counts"),
        )

        # The three one-mode boundary rays start directly at the cap.
        for mode in MODES:
            ray_path = cap_path
            ray_cuts = {mode: cap_cuts[mode]}
            for k in range(grid + 2):
                counts = increment_counts(cap_counts, {mode: k})
                verify_selected_state(ray_path, counts, ray_cuts)
                record = ["ray", case_index, mode, k, ray_cuts, ray_path]
                record_hash.update(
                    json.dumps(record, separators=(",", ":"), sort_keys=True).encode()
                )
                record_hash.update(b"\n")
                ray_paths_checked += 1
                ray_path, ray_cuts = advance_selected(ray_path, ray_cuts, mode)

        # Each pairwise face begins after one growth in each of its modes.
        for pair in itertools.combinations(MODES, 2):
            endpoints: list[tuple[list[int], dict[int, int]]] = []
            for order in (pair, pair[::-1]):
                current_path, current_cuts = cap_path, cap_cuts
                for mode in order:
                    current_path, current_cuts = advance(
                        current_path, current_cuts, mode
                    )
                    face_derivation_steps += 1
                endpoints.append((current_path, current_cuts))
            require(endpoints[0] == endpoints[1], (base, pair, "two orders"))
            face_path, all_face_cuts = endpoints[0]
            face_cuts = {mode: all_face_cuts[mode] for mode in pair}
            face_counts = increment_counts(cap_counts, {mode: 1 for mode in pair})
            verify_selected_state(face_path, face_counts, face_cuts)
            require(
                len(face_path) >= 2 * MAXIMUM_LENGTH + sum(pair),
                (base, pair, "face margin"),
            )
            face_seeds += 1

            # Adding the missing mode links each face to the stored tri-modal seed.
            missing_mode = next(mode for mode in MODES if mode not in pair)
            require(
                advance(face_path, all_face_cuts, missing_mode) == safe_endpoint,
                (base, pair, "tri seed link"),
            )
            tri_seed_links_checked += 1

            family: dict[
                tuple[int, int], tuple[list[int], dict[int, int]]
            ] = {}
            first, second = pair
            first_path, first_cuts = face_path, face_cuts
            for p in range(grid + 2):
                second_path, second_cuts = first_path, first_cuts
                for q in range(grid + 2):
                    counts = increment_counts(
                        face_counts, {first: p, second: q}
                    )
                    verify_selected_state(second_path, counts, second_cuts)
                    family[p, q] = (second_path, second_cuts)
                    record = [
                        "face",
                        case_index,
                        list(pair),
                        p,
                        q,
                        second_cuts,
                        second_path,
                    ]
                    record_hash.update(
                        json.dumps(
                            record, separators=(",", ":"), sort_keys=True
                        ).encode()
                    )
                    record_hash.update(b"\n")
                    face_family_paths_checked += 1
                    second_path, second_cuts = advance_selected(
                        second_path, second_cuts, second
                    )
                first_path, first_cuts = advance_selected(
                    first_path, first_cuts, first
                )

            for p, q in itertools.product(range(grid + 1), repeat=2):
                current_path, current_cuts = family[p, q]
                for coordinate, mode in enumerate(pair):
                    child = advance_selected(current_path, current_cuts, mode)
                    index = [p, q]
                    index[coordinate] += 1
                    require(child == family[tuple(index)], (base, pair, p, q, mode))
                    face_coordinate_transitions_checked += 1
                path_a, cuts_a = advance_selected(
                    current_path, current_cuts, first
                )
                final_a = advance_selected(path_a, cuts_a, second)
                path_b, cuts_b = advance_selected(
                    current_path, current_cuts, second
                )
                final_b = advance_selected(path_b, cuts_b, first)
                require(final_a == final_b, (base, pair, p, q, "square"))
                face_commuting_squares_checked += 1

    return {
        "certificate_sha256": certificate_sha256,
        "python": platform.python_version(),
        "cap_orthants": len(data["cases"]),
        "partition_strata": 8 * len(data["cases"]),
        "face_seeds": face_seeds,
        "face_derivation_steps": face_derivation_steps,
        "tri_seed_links_checked": tri_seed_links_checked,
        "grid": grid,
        "ray_paths_checked": ray_paths_checked,
        "face_family_paths_checked": face_family_paths_checked,
        "face_coordinate_transitions_checked": face_coordinate_transitions_checked,
        "face_commuting_squares_checked": face_commuting_squares_checked,
        "record_sha256": record_hash.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=3)
    parser.add_argument(
        "--allow-unpinned",
        action="store_true",
        help="check a modified certificate without enforcing its SHA-256",
    )
    args = parser.parse_args()
    summary = verify_certificate(
        args.certificate, args.grid, not args.allow_unpinned
    )
    for key, value in summary.items():
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
