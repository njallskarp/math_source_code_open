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
    certificate: Path,
    radius: int,
    target: Path | None = None,
    allow_partial: bool = False,
    greedy_minimum: bool = False,
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
    terminal_candidate_histogram: dict[int, int] | None = None
    terminal_minimum_count: int | None = None
    terminal_minimum_edges: list[tuple[int, int]] = []

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

    current_count = len(base_witnesses)
    objective_sequence = [current_count]

    for depth in range(1, radius + 1):
        accepted = None
        candidate_histogram: dict[int, int] = {}
        candidate_minimum: int | None = None
        candidate_minimizers: list[tuple[int, int]] = []
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
            resulting_count = current_count - old_mono + new_mono
            candidate_histogram[resulting_count] = (
                candidate_histogram.get(resulting_count, 0) + 1
            )
            if candidate_minimum is None or resulting_count < candidate_minimum:
                candidate_minimum = resulting_count
                candidate_minimizers = [edges[edge_id]]
            elif resulting_count == candidate_minimum:
                candidate_minimizers.append(edges[edge_id])
            if not greedy_minimum and resulting_count == 2:
                accepted = edge_id
                break
        if greedy_minimum and candidate_minimizers:
            accepted = edge_ids[candidate_minimizers[0]]
        if accepted is None:
            if not allow_partial:
                raise RuntimeError(
                    f"greedy plateau search stopped at radius {depth - 1}"
                )
            terminal_candidate_histogram = candidate_histogram
            terminal_minimum_count = candidate_minimum
            terminal_minimum_edges = candidate_minimizers
            break
        toggle(accepted)
        changed.append(accepted)
        current_witnesses = witnesses()
        current_count = len(current_witnesses)
        objective_sequence.append(current_count)
        if not greedy_minimum and current_count != 2:
            raise AssertionError((depth, current_count))
        step: dict[str, object] = {
            "radius": depth,
            "new_reversed_edge": edges[accepted],
            "monochromatic_k5": current_witnesses,
        }
        if greedy_minimum:
            step["monochromatic_k5_count"] = current_count
        steps.append(step)

    changed_edges = {edges[item] for item in changed}
    result: dict[str, object] = {
        "certificate": certificate.name,
        "base_monochromatic_k5": base_witnesses,
        "requested_radius": radius,
        "achieved_radius": len(steps),
        "path_found": len(steps) == radius,
        "monochromatic_k5_count_at_every_step": (
            2 if all(count == 2 for count in objective_sequence) else None
        ),
        "steps": steps,
        "scope_note": (
            "This is an explicit upper-bound witness on each exact-radius sphere. "
            "The separate bounded exhaustive search supplies the lower bound "
            "through radius six."
        ),
    }
    if greedy_minimum:
        result["objective_sequence_including_base"] = objective_sequence
    if terminal_candidate_histogram is not None:
        result["terminal_unused_edge_result_count_histogram"] = {
            str(count): terminal_candidate_histogram[count]
            for count in sorted(terminal_candidate_histogram)
        }
        result["terminal_has_unused_constant_two_extension"] = False
        result["terminal_unused_edge_minimum_count"] = terminal_minimum_count
        result["terminal_unused_edge_minimizers"] = terminal_minimum_edges
    if target is not None:
        target_flips = load_certificate(target)
        symmetric_difference = flips ^ target_flips
        result["target_certificate"] = target.name
        result["source_target_hamming_distance"] = len(symmetric_difference)
        result["path_endpoint_matches_target"] = changed_edges == symmetric_difference
        result["source_target_differing_edges"] = sorted(symmetric_difference)
        if (
            len(steps) == radius == len(symmetric_difference)
            and changed_edges != symmetric_difference
        ):
            raise AssertionError("requested geodesic does not reach target certificate")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--radius", type=int, default=6)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--allow-partial", action="store_true")
    parser.add_argument("--greedy-minimum", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = find_plateau_path(
        args.certificate,
        args.radius,
        args.target,
        args.allow_partial,
        args.greedy_minimum,
    )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
