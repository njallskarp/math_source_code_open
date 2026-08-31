#!/usr/bin/env python3
"""Find and directly verify a constant-two edge-reversal path in K43."""

from __future__ import annotations

import argparse
import itertools
import json
from array import array
from pathlib import Path

from local_rigidity import complete_graph_edges, is_monochromatic, initial_colors
from solve_cyclic43 import ORDER, edge, load_certificate


def find_plateau_path(
    certificate: Path, radius: int, target: Path | None = None
) -> dict[str, object]:
    flips = load_certificate(certificate)
    colors, edges = initial_colors(flips)
    edge_ids, _ = complete_graph_edges()
    incident = [array("I") for _ in edges]
    five_edges = array("H")
    five_vertices = array("B")
    red_counts = array("b")

    for vertices in itertools.combinations(range(ORDER), 5):
        five_id = len(red_counts)
        ids = [
            edge_ids[edge(a, b)] for a, b in itertools.combinations(vertices, 2)
        ]
        five_vertices.extend(vertices)
        five_edges.extend(ids)
        red_counts.append(sum(colors[edge_id] for edge_id in ids))
        for edge_id in ids:
            incident[edge_id].append(five_id)

    if len(red_counts) != 962_598:
        raise AssertionError(len(red_counts))
    if any(len(indexes) != 10_660 for indexes in incident):
        raise AssertionError("incorrect edge/five-set incidence")

    changed: list[int] = []
    steps: list[dict[str, object]] = []

    def witnesses() -> list[list[int]]:
        result = []
        for five_id, red_count in enumerate(red_counts):
            if is_monochromatic(red_count):
                offset = five_id * 5
                result.append(list(five_vertices[offset : offset + 5]))
        return result

    def toggle(edge_id: int) -> None:
        delta = -1 if colors[edge_id] else 1
        colors[edge_id] = not colors[edge_id]
        for five_id in incident[edge_id]:
            red_counts[five_id] += delta

    base_witnesses = witnesses()
    if len(base_witnesses) != 2:
        raise ValueError(f"expected two base witnesses, got {len(base_witnesses)}")

    for depth in range(1, radius + 1):
        accepted = None
        changed_set = set(changed)
        for edge_id in range(len(edges)):
            if edge_id in changed_set:
                continue
            old_mono = 0
            new_mono = 0
            delta = -1 if colors[edge_id] else 1
            for five_id in incident[edge_id]:
                count = red_counts[five_id]
                old_mono += is_monochromatic(count)
                new_mono += is_monochromatic(count + delta)
            if 2 - old_mono + new_mono == 2:
                accepted = edge_id
                toggle(edge_id)
                changed.append(edge_id)
                current_witnesses = witnesses()
                if len(current_witnesses) != 2:
                    raise AssertionError((depth, len(current_witnesses)))
                steps.append(
                    {
                        "radius": depth,
                        "new_reversed_edge": edges[edge_id],
                        "monochromatic_k5": current_witnesses,
                    }
                )
                break
        if accepted is None:
            raise RuntimeError(f"greedy plateau search stopped at radius {depth - 1}")

    changed_edges = {edges[item] for item in changed}
    result: dict[str, object] = {
        "certificate": certificate.name,
        "base_monochromatic_k5": base_witnesses,
        "requested_radius": radius,
        "path_found": True,
        "monochromatic_k5_count_at_every_step": 2,
        "steps": steps,
        "scope_note": (
            "This is an explicit upper-bound witness on each exact-radius sphere. "
            "The separate bounded exhaustive search supplies the lower bound "
            "through radius six."
        ),
    }
    if target is not None:
        target_flips = load_certificate(target)
        symmetric_difference = flips ^ target_flips
        result["target_certificate"] = target.name
        result["source_target_hamming_distance"] = len(symmetric_difference)
        result["path_endpoint_matches_target"] = changed_edges == symmetric_difference
        result["source_target_differing_edges"] = sorted(symmetric_difference)
        if radius == len(symmetric_difference) and changed_edges != symmetric_difference:
            raise AssertionError("requested geodesic does not reach target certificate")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--radius", type=int, default=6)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = find_plateau_path(args.certificate, args.radius, args.target)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
