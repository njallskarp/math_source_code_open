#!/usr/bin/env python3
"""Classify lower-objective islands exposed by the Cyclic(43) q<=9 closure."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path


ORDER = 43
EDGE_COUNT = ORDER * (ORDER - 1) // 2
WORD_COUNT = (EDGE_COUNT + 63) // 64
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
    masks: list[int] = []
    for vertices in combinations(range(ORDER), 5):
        mask = 0
        for a, b in combinations(vertices, 2):
            mask |= 1 << edge_id[a][b]
        masks.append(mask)
    if len(masks) != 962_598:
        raise RuntimeError("five-set count mismatch")
    return masks


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
        result |= 1 << mapping[bit.bit_length() - 1]
        bits ^= bit
    return result


def word_key(state: int) -> tuple[int, ...]:
    return tuple(
        (state >> (64 * word)) & ((1 << 64) - 1)
        for word in range(WORD_COUNT)
    )


def canonical_with_offset(
    state: int, rotated_edge: list[list[int]]
) -> tuple[int, int]:
    candidates = [rotate(state, mapping) for mapping in rotated_edge]
    offset, representative = min(
        enumerate(candidates), key=lambda item: word_key(item[1])
    )
    return representative, offset


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


def load_set(payload: dict[str, object], key: str) -> set[int]:
    return {state_from_edges(item) for item in payload[key]}


def classify(
    component_path: Path,
    known_external_path: Path,
    objective_eight_path: Path,
    objective_seven_path: Path,
    lower_path: Path,
) -> dict[str, object]:
    component = json.loads(component_path.read_text())
    known_external = json.loads(known_external_path.read_text())
    objective_eight = json.loads(objective_eight_path.read_text())
    objective_seven = json.loads(objective_seven_path.read_text())
    lower = json.loads(lower_path.read_text())

    new_by_objective = {
        objective: load_set(
            component, f"new_objective_{objective}_rotation_representatives"
        )
        for objective in (7, 8)
    }
    new_states = new_by_objective[7] | new_by_objective[8]
    if len(new_by_objective[7]) != 1 or len(new_by_objective[8]) != 33:
        raise RuntimeError("unexpected lower-layer input counts")

    primary_by_objective = {
        objective: load_set(
            lower, f"objective_{objective}_rotation_representatives"
        )
        for objective in range(2, 7)
    }
    primary_by_objective[7] = load_set(
        objective_seven, "objective_seven_component_rotation_representatives"
    )
    primary_by_objective[8] = load_set(
        objective_eight, "objective_eight_component_rotation_representatives"
    )
    known_external_states = {
        state_from_edges(item)
        for values in known_external["components"]
        for states in values["rotation_representatives_by_objective"].values()
        for item in states
    }
    if len(known_external_states) != 21 or not known_external_states <= new_states:
        raise RuntimeError("known external island is not contained")

    edges, edge_id, rotated_edge = build_edges()
    base_red = 0
    for index, (a, b) in enumerate(edges):
        distance = min((a - b) % ORDER, (b - a) % ORDER)
        if distance in RED_LENGTHS:
            base_red |= 1 << index
    five_masks = build_five_masks(edge_id)

    adjacency: dict[int, set[int]] = {state: set() for state in new_states}
    voltage_edges: dict[int, list[tuple[int, int]]] = defaultdict(list)
    target_objective: dict[int, int] = {}
    boundary_nine: dict[int, set[int]] = defaultdict(set)
    boundary_nine_incidence: Counter[int] = Counter()
    escape_level: dict[int, int] = {}
    internal_directed: Counter[int] = Counter()
    primary_incidence = 0
    missing_accepted = 0

    for state in sorted(new_states, key=word_key):
        representative, _ = canonical_with_offset(state, rotated_edge)
        rotations = {rotate(state, mapping) for mapping in rotated_edge}
        if representative != state or len(rotations) != ORDER:
            raise RuntimeError("noncanonical or nonfree lower representative")
        expected = 7 if state in new_by_objective[7] else 8
        objective, deltas = direct_objective_and_deltas(
            state, base_red, five_masks
        )
        if objective != expected:
            raise RuntimeError("lower representative objective mismatch")
        target_objective[state] = objective
        for edge, delta in enumerate(deltas):
            neighbor_objective = objective + delta
            neighbor, canonical_offset = canonical_with_offset(
                state ^ (1 << edge), rotated_edge
            )
            if neighbor_objective <= 8:
                if neighbor in new_states:
                    adjacency[state].add(neighbor)
                    # If y=rot(raw,c), then raw=rot(y,-c), so the lifted
                    # edge sends rotation t of state to rotation t-c of y.
                    voltage_edges[state].append(
                        (neighbor, (-canonical_offset) % ORDER)
                    )
                    internal_directed[state] += 1
                elif neighbor in primary_by_objective.get(
                    neighbor_objective, set()
                ):
                    primary_incidence += 1
                else:
                    missing_accepted += 1
            else:
                escape_level[state] = min(
                    escape_level.get(state, neighbor_objective),
                    neighbor_objective,
                )
                if neighbor_objective == 9:
                    boundary_nine[state].add(neighbor)
                    boundary_nine_incidence[state] += 1

    if primary_incidence or missing_accepted:
        raise RuntimeError(
            "lower-island closure failed: "
            f"primary_incidence={primary_incidence}, "
            f"missing_accepted={missing_accepted}"
        )

    unseen = set(new_states)
    components: list[set[int]] = []
    while unseen:
        root = min(unseen, key=word_key)
        found = {root}
        queue = deque([root])
        unseen.remove(root)
        while queue:
            state = queue.popleft()
            for neighbor in adjacency[state]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    found.add(neighbor)
                    queue.append(neighbor)
        components.append(found)

    summaries: list[dict[str, object]] = []
    for states in components:
        root = min(states, key=word_key)
        potentials = {root: 0}
        queue = deque([root])
        has_nonzero_cycle_voltage = False
        while queue:
            state = queue.popleft()
            for neighbor, voltage in voltage_edges[state]:
                expected = (potentials[state] + voltage) % ORDER
                if neighbor not in potentials:
                    potentials[neighbor] = expected
                    queue.append(neighbor)
                elif potentials[neighbor] != expected:
                    has_nonzero_cycle_voltage = True
        if len(potentials) != len(states):
            raise RuntimeError("voltage traversal missed a quotient vertex")
        lifted_component_count = 1 if has_nonzero_cycle_voltage else ORDER
        quotient_orbits = len(states)
        labeled_states = {
            rotate(state, mapping)
            for state in states
            for mapping in rotated_edge
        }
        labeled_unseen = set(labeled_states)
        labeled_components: list[set[int]] = []
        labeled_component_edge_counts: list[int] = []
        while labeled_unseen:
            labeled_root = next(iter(labeled_unseen))
            labeled_found = {labeled_root}
            labeled_queue = deque([labeled_root])
            labeled_unseen.remove(labeled_root)
            labeled_directed = 0
            while labeled_queue:
                labeled_state = labeled_queue.popleft()
                for edge in range(EDGE_COUNT):
                    neighbor = labeled_state ^ (1 << edge)
                    if neighbor not in labeled_states:
                        continue
                    labeled_directed += 1
                    if neighbor in labeled_unseen:
                        labeled_unseen.remove(neighbor)
                        labeled_found.add(neighbor)
                        labeled_queue.append(neighbor)
            if labeled_directed % 2:
                raise RuntimeError("odd labeled internal directed count")
            labeled_components.append(labeled_found)
            labeled_component_edge_counts.append(labeled_directed // 2)
        labeled_component_sizes = sorted(map(len, labeled_components))
        labeled_component_edge_counts.sort()
        if len(labeled_components) != lifted_component_count:
            raise RuntimeError("voltage and explicit labeled BFS disagree")
        all_boundary = set().union(*(boundary_nine[state] for state in states))
        summary = {
            "rotation_quotient_component_orbit_count": quotient_orbits,
            "rotation_orbit_count_by_objective": dict(
                sorted(Counter(target_objective[state] for state in states).items())
            ),
            "known_21_orbit_island_overlap": len(states & known_external_states),
            "lifted_labeled_component_count": lifted_component_count,
            "explicit_labeled_component_vertex_counts": labeled_component_sizes,
            "explicit_labeled_component_edge_counts": (
                labeled_component_edge_counts
            ),
            "total_labeled_vertex_count": ORDER * quotient_orbits,
            "total_induced_edge_count": (
                ORDER * sum(internal_directed[state] for state in states) // 2
            ),
            "exact_one_flip_escape_level": min(
                escape_level[state] for state in states
            ),
            "objective_nine_boundary_rotation_orbit_count": len(all_boundary),
            "objective_nine_boundary_directed_labeled_incidence": (
                ORDER * sum(boundary_nine_incidence[state] for state in states)
            ),
            "nonzero_cycle_voltage_found": has_nonzero_cycle_voltage,
        }
        summaries.append(summary)

    summaries.sort(
        key=lambda item: (
            -int(item["known_21_orbit_island_overlap"]),
            -int(item["rotation_quotient_component_orbit_count"]),
        )
    )
    return {
        "independent_direct_recount_lower_rotation_orbit_count": len(new_states),
        "lower_rotation_orbit_count_by_objective": {
            "7": len(new_by_objective[7]),
            "8": len(new_by_objective[8]),
        },
        "primary_sublevel_eight_incidence_count": primary_incidence,
        "missing_objective_at_most_eight_neighbor_count": missing_accepted,
        "complete_rotation_quotient_component_count": len(summaries),
        "components": summaries,
        "method": (
            "independent Python direct five-set recount, fresh cyclic "
            "canonicalization, exhaustive threshold-eight membership checks, "
            "and Z/43Z voltage-cover connectivity classification"
        ),
        "scope_note": (
            "Classifies exactly the lower-objective orbits newly exposed by "
            "the certified primary threshold-nine closure; unrelated "
            "sublevel-eight components remain out of scope."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("component", type=Path)
    parser.add_argument("known_external", type=Path)
    parser.add_argument("objective_eight", type=Path)
    parser.add_argument("objective_seven", type=Path)
    parser.add_argument("lower", type=Path)
    args = parser.parse_args()
    print(
        json.dumps(
            classify(
                args.component,
                args.known_external,
                args.objective_eight,
                args.objective_seven,
                args.lower,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
