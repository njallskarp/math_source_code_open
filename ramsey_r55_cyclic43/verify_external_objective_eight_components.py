#!/usr/bin/env python3
"""Independently verify exposed Cyclic(43) sublevel-eight components."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path


ORDER = 43
EDGE_COUNT = ORDER * (ORDER - 1) // 2
RED_LENGTHS = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}


def build_edges() -> tuple[list[tuple[int, int]], list[list[int]], list[list[int]]]:
    edges: list[tuple[int, int]] = []
    edge_id = [[-1] * ORDER for _ in range(ORDER)]
    for a in range(ORDER):
        for b in range(a + 1, ORDER):
            edge_id[a][b] = edge_id[b][a] = len(edges)
            edges.append((a, b))
    rotated_edge = [[0] * EDGE_COUNT for _ in range(ORDER)]
    for offset in range(ORDER):
        for index, (a, b) in enumerate(edges):
            rotated_edge[offset][index] = edge_id[
                (a + offset) % ORDER
            ][(b + offset) % ORDER]
    return edges, edge_id, rotated_edge


def build_five_masks(edge_id: list[list[int]]) -> list[int]:
    result: list[int] = []
    for vertices in combinations(range(ORDER), 5):
        mask = 0
        for a, b in combinations(vertices, 2):
            mask |= 1 << edge_id[a][b]
        result.append(mask)
    if len(result) != 962_598:
        raise RuntimeError("five-set count mismatch")
    return result


def state_from_edges(edge_indices: list[int]) -> int:
    state = 0
    for edge in edge_indices:
        if edge < 0 or edge >= EDGE_COUNT or state & (1 << edge):
            raise RuntimeError("invalid state edge")
        state |= 1 << edge
    return state


def rotate(state: int, mapping: list[int]) -> int:
    result = 0
    bits = state
    while bits:
        bit = bits & -bits
        edge = bit.bit_length() - 1
        result |= 1 << mapping[edge]
        bits ^= bit
    return result


def canonical(state: int, rotated_edge: list[list[int]]) -> int:
    # Match the generator's documented little-endian 64-bit-word ordering.
    # Integer ordering would compare the highest word first and choose a
    # different (though mathematically equivalent) orbit representative.
    def word_key(candidate: int) -> tuple[int, ...]:
        return tuple(
            (candidate >> (64 * word)) & ((1 << 64) - 1)
            for word in range((EDGE_COUNT + 63) // 64)
        )

    return min(
        (rotate(state, mapping) for mapping in rotated_edge), key=word_key
    )


def direct_objective_and_deltas(
    state: int, base_red: int, five_masks: list[int]
) -> tuple[int, list[int]]:
    red = base_red ^ state
    objective = 0
    deltas = [0] * EDGE_COUNT
    for mask in five_masks:
        red_part = red & mask
        count = red_part.bit_count()
        if count == 0 or count == 10:
            objective += 1
            bits = mask
            while bits:
                bit = bits & -bits
                deltas[bit.bit_length() - 1] -= 1
                bits ^= bit
        elif count == 1:
            deltas[red_part.bit_length() - 1] += 1
        elif count == 9:
            blue_part = mask ^ red_part
            deltas[blue_part.bit_length() - 1] += 1
    return objective, deltas


def verify(component_path: Path, seed_path: Path) -> dict[str, object]:
    component = json.loads(component_path.read_text())
    seeds_payload = json.loads(seed_path.read_text())
    summaries = component["components"]
    if len(summaries) != 1:
        raise RuntimeError("verifier currently expects the claimed single component")
    summary = summaries[0]
    representative_lists = summary["rotation_representatives_by_objective"]
    representatives = {
        state_from_edges(item) for item in representative_lists.get("8", [])
    }
    seeds = {
        state_from_edges(item)
        for item in seeds_payload[
            "out_of_component_objective_eight_rotation_representatives"
        ]
    }
    if len(seeds) != 20 or not seeds <= representatives:
        raise RuntimeError("external seed coverage mismatch")

    edges, edge_id, rotated_edge = build_edges()
    base_red = 0
    for index, (a, b) in enumerate(edges):
        delta = (a - b) % ORDER
        distance = min(delta, ORDER - delta)
        if distance in RED_LENGTHS:
            base_red |= 1 << index
    five_masks = build_five_masks(edge_id)

    missing_neighbors = 0
    wrong_objectives = 0
    noncanonical_or_nonfree = 0
    internal_directed = 0
    escape_level: int | None = None
    objective_nine_boundary: set[int] = set()
    objective_nine_directed_incidence = 0

    for state in sorted(representatives):
        rotations = {rotate(state, mapping) for mapping in rotated_edge}
        if canonical(state, rotated_edge) != state or len(rotations) != ORDER:
            noncanonical_or_nonfree += 1
        objective, deltas = direct_objective_and_deltas(
            state, base_red, five_masks
        )
        if objective != 8:
            wrong_objectives += 1
        for edge, delta in enumerate(deltas):
            target_objective = objective + delta
            target = canonical(state ^ (1 << edge), rotated_edge)
            if target_objective <= 8:
                if target not in representatives:
                    missing_neighbors += 1
                else:
                    internal_directed += ORDER
            else:
                if escape_level is None or target_objective < escape_level:
                    escape_level = target_objective
                if target_objective == 9:
                    objective_nine_boundary.add(target)
                    objective_nine_directed_incidence += ORDER

    if internal_directed % 2:
        raise RuntimeError("odd internal directed-edge count")
    result = {
        "independent_direct_recount_representative_count": len(representatives),
        "input_seed_representative_count": len(seeds),
        "additional_closure_representative_count": len(representatives - seeds),
        "all_representatives_have_objective_eight": wrong_objectives == 0,
        "all_representatives_are_canonical_and_free": (
            noncanonical_or_nonfree == 0
        ),
        "missing_objective_at_most_eight_neighbor_count": missing_neighbors,
        "external_component_is_closed": missing_neighbors == 0,
        "external_component_vertex_count": ORDER * len(representatives),
        "external_component_induced_edge_count": internal_directed // 2,
        "exact_one_flip_escape_level": escape_level,
        "objective_nine_boundary_rotation_orbit_count": len(
            objective_nine_boundary
        ),
        "objective_nine_boundary_directed_incidence": (
            objective_nine_directed_incidence
        ),
        "method": (
            "independent Python direct five-set recount, fresh cyclic "
            "canonicalization, and complete one-flip membership check"
        ),
    }
    expected = {
        "independent_direct_recount_representative_count": summary[
            "rotation_orbit_count"
        ],
        "input_seed_representative_count": summary["input_seed_orbit_count"],
        "external_component_vertex_count": summary["vertex_count"],
        "external_component_induced_edge_count": summary["induced_edge_count"],
        "exact_one_flip_escape_level": summary["exact_one_flip_escape_level"],
        "objective_nine_boundary_rotation_orbit_count": summary[
            "objective_nine_boundary_rotation_orbit_count"
        ],
        "objective_nine_boundary_directed_incidence": summary[
            "objective_nine_boundary_directed_incidence"
        ],
    }
    for key, value in expected.items():
        if result[key] != value:
            raise RuntimeError(
                f"claimed summary mismatch for {key}: {result[key]} != {value}"
            )
    if wrong_objectives or noncanonical_or_nonfree or missing_neighbors:
        raise RuntimeError(
            "external component verification failed: "
            f"wrong_objectives={wrong_objectives}, "
            f"noncanonical_or_nonfree={noncanonical_or_nonfree}, "
            f"missing_neighbors={missing_neighbors}"
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("component", type=Path)
    parser.add_argument("seeds", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.component, args.seeds), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
