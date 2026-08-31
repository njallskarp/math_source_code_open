#!/usr/bin/env python3
"""Run bounded rigidity checks around every center of the optimum bridge."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import tempfile
from collections import Counter
from math import comb
from pathlib import Path

from solve_cyclic43 import load_certificate


def analyze_center(
    checker: Path,
    radius: int,
    center_index: int,
    flipped_edges: set[tuple[int, int]],
    directory: Path,
) -> dict[str, object]:
    certificate = directory / f"center-{center_index:02d}.json"
    certificate.write_text(
        json.dumps({"flipped_edges": sorted(flipped_edges)}, sort_keys=True) + "\n"
    )
    completed = subprocess.run(
        [str(checker), str(certificate), str(radius)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"center {center_index} failed with code {completed.returncode}: "
            f"{completed.stderr}"
        )
    payload = json.loads(completed.stdout)
    if payload["improvement_found"]:
        raise AssertionError(f"center {center_index} has an improvement")
    return {
        "center_index": center_index,
        "distance_from_fu_malik": center_index,
        "distance_from_primary": 15 - center_index,
        "seed_red_to_blue_flip_count": len(flipped_edges),
        "base_monochromatic_k5": payload["base_monochromatic_k5"],
        "exact_minimum_through_requested_radius": payload[
            "exact_minimum_through_requested_radius"
        ],
        "expanded_by_depth": payload["expanded_by_depth"],
        "candidate_branches_considered": payload[
            "candidate_branches_considered"
        ],
        "maximum_intermediate_monochromatic_k5_count": payload[
            "maximum_intermediate_monochromatic_k5_count"
        ],
    }


def analyze_bridge(
    checker: Path, bridge_path: Path, radius: int, jobs: int
) -> dict[str, object]:
    bridge = json.loads(bridge_path.read_text())
    root = bridge_path.resolve().parent
    source_path = root / bridge["certificate"]
    target_path = root / bridge["target_certificate"]
    source = load_certificate(source_path)
    target = load_certificate(target_path)

    centers = [source.copy()]
    current = source.copy()
    for step in bridge["steps"]:
        changed = tuple(step["new_reversed_edge"])
        if changed in current:
            current.remove(changed)
        else:
            current.add(changed)
        centers.append(current.copy())
    if current != target:
        raise AssertionError("bridge endpoint does not equal target certificate")
    if len(centers) != 16:
        raise AssertionError(len(centers))

    with tempfile.TemporaryDirectory(prefix="r55-bridge-tube-") as temporary:
        directory = Path(temporary)
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
            futures = [
                executor.submit(
                    analyze_center,
                    checker.resolve(),
                    radius,
                    index,
                    center,
                    directory,
                )
                for index, center in enumerate(centers)
            ]
            results = [future.result() for future in futures]

    results.sort(key=lambda item: item["center_index"])
    minima = {
        item["exact_minimum_through_requested_radius"] for item in results
    }
    if minima != {2}:
        raise AssertionError(minima)
    path_length = len(centers) - 1
    nearest = Counter()
    for mask in range(1 << path_length):
        nearest[
            min(
                (mask ^ ((1 << prefix) - 1)).bit_count()
                for prefix in range(path_length + 1)
            )
        ] += 1
    outside_coordinates = 903 - path_length
    union_size = sum(
        count
        * sum(
            comb(outside_coordinates, extra)
            for extra in range(radius - distance + 1)
        )
        for distance, count in nearest.items()
        if distance <= radius
    )
    return {
        "bridge": bridge_path.name,
        "source_certificate": source_path.name,
        "target_certificate": target_path.name,
        "bridge_edge_count": 15,
        "center_count": len(results),
        "tube_radius": radius,
        "exact_minimum_in_every_closed_ball": 2,
        "distinct_coloring_count_in_ball_union": union_size,
        "single_ball_size": sum(
            comb(903, value) for value in range(radius + 1)
        ),
        "path_coordinate_nearest_prefix_distance_histogram": {
            str(distance): count for distance, count in sorted(nearest.items())
        },
        "total_candidate_branches_considered": sum(
            item["candidate_branches_considered"] for item in results
        ),
        "centers": results,
        "scope_note": (
            "Each center is checked independently by the forced-witness exhaustive "
            "search. The theorem concerns the union of the 16 closed Hamming balls, "
            "not all colorings within a fixed distance of either endpoint."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--bridge", type=Path, default=Path("plateau-bridge.json"))
    parser.add_argument("--radius", type=int, default=5)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze_bridge(args.checker, args.bridge, args.radius, args.jobs)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
