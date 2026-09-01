#!/usr/bin/env python3
"""Analyze the exact quotient geometry of the 527-orbit P10 addition.

The input certificates use the C++ generator's canonical representative: the
lexicographically least 15-word state over all 43 cyclic rotations.  This
script reproduces that convention with a single Python integer whose most
significant 64-bit block is C++ word zero.  For a fixed source, all 43 rotated
keys are cached, so canonicalizing each one-edge neighbor requires only 43
XORs and a minimum.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Iterable


ORDER = 43
EDGE_COUNT = ORDER * (ORDER - 1) // 2
WORD_COUNT = (EDGE_COUNT + 63) // 64
ORBIT_SIZE = ORDER


def edge_tables() -> tuple[list[tuple[int, int]], list[list[int]], list[list[int]], list[int]]:
    vertices: list[tuple[int, int]] = []
    edge_id = [[-1] * ORDER for _ in range(ORDER)]
    for a in range(ORDER):
        for b in range(a + 1, ORDER):
            edge_id[a][b] = edge_id[b][a] = len(vertices)
            vertices.append((a, b))
    rotated = [[0] * EDGE_COUNT for _ in range(ORDER)]
    for offset in range(ORDER):
        for index, (a, b) in enumerate(vertices):
            rotated[offset][index] = edge_id[(a + offset) % ORDER][(b + offset) % ORDER]
    reflected = [0] * EDGE_COUNT
    for index, (a, b) in enumerate(vertices):
        reflected[index] = edge_id[(-a) % ORDER][(-b) % ORDER]
    key_bits = [
        1 << (64 * (WORD_COUNT - 1 - index // 64) + index % 64)
        for index in range(EDGE_COUNT)
    ]
    return vertices, rotated, reflected, key_bits


_VERTICES, ROTATED_EDGE, REFLECTED_EDGE, KEY_BIT = edge_tables()


def state_key(edges: Iterable[int]) -> int:
    key = 0
    for edge in edges:
        if not 0 <= edge < EDGE_COUNT:
            raise ValueError(f"invalid edge id {edge}")
        bit = KEY_BIT[edge]
        if key & bit:
            raise ValueError(f"duplicate edge id {edge}")
        key |= bit
    return key


def rotated_keys(edges: Iterable[int]) -> tuple[int, ...]:
    edge_tuple = tuple(edges)
    return tuple(
        sum(KEY_BIT[ROTATED_EDGE[offset][edge]] for edge in edge_tuple)
        for offset in range(ORDER)
    )


def canonical_key(edges: Iterable[int]) -> int:
    return min(rotated_keys(edges))


def histogram(values: Iterable[int]) -> dict[str, int]:
    return {str(key): value for key, value in sorted(Counter(values).items())}


def components(adjacency: list[set[int]]) -> list[list[int]]:
    unseen = set(range(len(adjacency)))
    result: list[list[int]] = []
    while unseen:
        root = min(unseen)
        queue = [root]
        unseen.remove(root)
        component: list[int] = []
        while queue:
            source = queue.pop()
            component.append(source)
            for target in adjacency[source]:
                if target in unseen:
                    unseen.remove(target)
                    queue.append(target)
        result.append(sorted(component))
    result.sort(key=lambda value: (-len(value), value[0]))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frontier", type=Path)
    parser.add_argument("component_fast", type=Path)
    parser.add_argument("component_independent", type=Path)
    args = parser.parse_args()

    frontier_data = json.loads(args.frontier.read_text())
    fast_data = json.loads(args.component_fast.read_text())
    independent_data = json.loads(args.component_independent.read_text())

    frontier_states = frontier_data["objective_ten_rotation_representatives"]
    added_states = fast_data["additional_objective_10_rotation_representatives"]
    independent_added_states = independent_data[
        "complete_threshold_ten_additional_objective_10_rotation_representatives"
    ]
    first_expansion_states = independent_data[
        "newly_exposed_objective_10_rotation_representatives"
    ]

    frontier_keys = {state_key(state) for state in frontier_states}
    added_keys = [state_key(state) for state in added_states]
    added_index = {key: index for index, key in enumerate(added_keys)}
    independent_added_keys = {state_key(state) for state in independent_added_states}
    first_expansion_keys = {state_key(state) for state in first_expansion_states}

    if len(frontier_keys) != len(frontier_states):
        raise RuntimeError("duplicate frontier representative")
    if len(added_index) != len(added_states):
        raise RuntimeError("duplicate added representative")
    if frontier_keys & set(added_keys):
        raise RuntimeError("frontier/addition overlap")
    if set(added_keys) != independent_added_keys:
        raise RuntimeError("optimized and independent added lists disagree")
    if not first_expansion_keys <= set(added_keys):
        raise RuntimeError("first expansion is not contained in complete addition")
    for state, key in zip(added_states, added_keys, strict=True):
        if canonical_key(state) != key:
            raise RuntimeError("noncanonical added representative")

    internal_moves: dict[tuple[int, int], int] = defaultdict(int)
    boundary_moves: dict[tuple[int, int], int] = defaultdict(int)
    frontier_key_to_index: dict[int, int] = {}
    adjacency = [set() for _ in added_states]
    boundary_targets = [set() for _ in added_states]

    for source, state in enumerate(added_states):
        source_rotations = rotated_keys(state)
        for edge in range(EDGE_COUNT):
            target_key = min(
                source_rotations[offset] ^ KEY_BIT[ROTATED_EDGE[offset][edge]]
                for offset in range(ORDER)
            )
            target = added_index.get(target_key)
            if target is not None:
                internal_moves[(source, target)] += 1
                adjacency[source].add(target)
                continue
            if target_key in frontier_keys:
                frontier = frontier_key_to_index.setdefault(
                    target_key, len(frontier_key_to_index)
                )
                boundary_moves[(source, frontier)] += 1
                boundary_targets[source].add(frontier)

    for (source, target), multiplicity in internal_moves.items():
        if internal_moves.get((target, source)) != multiplicity:
            raise RuntimeError("asymmetric internal quotient multiplicity")
    internal_directed_incidence = sum(internal_moves.values())
    boundary_incidence = sum(boundary_moves.values())
    self_directed_incidence = sum(
        multiplicity
        for (source, target), multiplicity in internal_moves.items()
        if source == target
    )
    if self_directed_incidence % 2:
        raise RuntimeError("odd self-orbit directed incidence")
    internal_labeled_edges = ORBIT_SIZE * internal_directed_incidence // 2
    boundary_labeled_edges = ORBIT_SIZE * boundary_incidence
    if internal_labeled_edges != independent_data["additional_internal_edge_count"]:
        raise RuntimeError("internal labeled-edge aggregate mismatch")
    if boundary_labeled_edges != independent_data["additional_to_known_directed_edge_count"]:
        raise RuntimeError("boundary labeled-edge aggregate mismatch")

    distances: list[int | None] = [None] * len(added_states)
    queue: deque[int] = deque()
    for source, targets in enumerate(boundary_targets):
        if targets:
            distances[source] = 1
            queue.append(source)
    while queue:
        source = queue.popleft()
        assert distances[source] is not None
        for target in adjacency[source]:
            if distances[target] is None:
                distances[target] = distances[source] + 1
                queue.append(target)
    if any(distance is None for distance in distances):
        raise RuntimeError("addition contains a component disconnected from the frontier")
    shell_one_keys = {
        added_keys[index] for index, distance in enumerate(distances) if distance == 1
    }
    if shell_one_keys != first_expansion_keys:
        raise RuntimeError("computed first shell disagrees with first-expansion certificate")

    simple_internal_pairs = {
        (min(source, target), max(source, target))
        for source, target in internal_moves
    }
    internal_parallel_excess = sum(
        multiplicity - 1
        for (source, target), multiplicity in internal_moves.items()
        if source < target
    ) + sum(
        multiplicity // 2 - 1
        for (source, target), multiplicity in internal_moves.items()
        if source == target
    )
    simple_boundary_pairs = set(boundary_moves)
    boundary_parallel_excess = sum(value - 1 for value in boundary_moves.values())

    shell_edges: Counter[tuple[int, int]] = Counter()
    shell_simple_edges: Counter[tuple[int, int]] = Counter()
    for source, target in simple_internal_pairs:
        pair = tuple(sorted((int(distances[source]), int(distances[target]))))
        multiplicity = (
            internal_moves[(source, target)]
            if source != target
            else internal_moves[(source, source)] // 2
        )
        shell_edges[pair] += multiplicity
        shell_simple_edges[pair] += 1

    component_list = components(adjacency)
    component_index = {
        vertex: index
        for index, component in enumerate(component_list)
        for vertex in component
    }
    component_profiles = []
    for index, component in enumerate(component_list):
        vertices = set(component)
        simple_edges = sum(
            1
            for source, target in simple_internal_pairs
            if source in vertices and target in vertices
        )
        edge_multiplicity = sum(
            (
                internal_moves[(source, target)]
                if source != target
                else internal_moves[(source, source)] // 2
            )
            for source, target in simple_internal_pairs
            if source in vertices and target in vertices
        )
        boundary = sum(
            multiplicity
            for (source, _target), multiplicity in boundary_moves.items()
            if source in vertices
        )
        component_profiles.append(
            {
                "index": index,
                "added_orbit_count": len(component),
                "simple_internal_edge_count": simple_edges,
                "internal_edge_multiplicity": edge_multiplicity,
                "simple_cycle_rank": simple_edges - len(component) + 1,
                "multigraph_cycle_rank": edge_multiplicity - len(component) + 1,
                "frontier_incidence": boundary,
                "minimum_shell": min(int(distances[v]) for v in component),
                "maximum_shell": max(int(distances[v]) for v in component),
            }
        )

    reflection_partner: list[int] = []
    for state in added_states:
        reflected = [REFLECTED_EDGE[edge] for edge in state]
        partner_key = canonical_key(reflected)
        partner = added_index.get(partner_key)
        if partner is None:
            raise RuntimeError("addition is not reflection invariant")
        reflection_partner.append(partner)
    if any(reflection_partner[reflection_partner[index]] != index for index in range(len(added_states))):
        raise RuntimeError("reflection action is not an involution")
    if any(distances[index] != distances[partner] for index, partner in enumerate(reflection_partner)):
        raise RuntimeError("reflection does not preserve shell distance")
    if any(
        component_index[reflection_partner[vertex]]
        != component_index[reflection_partner[component[0]]]
        for component in component_list
        for vertex in component
    ):
        raise RuntimeError("reflection does not map components to components")
    reflected_components = [
        component_index[reflection_partner[component[0]]]
        for component in component_list
    ]

    added_internal_incidence = [0] * len(added_states)
    added_internal_degree = [0] * len(added_states)
    for source in range(len(added_states)):
        added_internal_incidence[source] = sum(
            multiplicity
            for (candidate, _target), multiplicity in internal_moves.items()
            if candidate == source
        )
        added_internal_degree[source] = len(adjacency[source])
    added_boundary_incidence = [0] * len(added_states)
    for (source, _target), multiplicity in boundary_moves.items():
        added_boundary_incidence[source] += multiplicity
    frontier_incidence = [0] * len(frontier_key_to_index)
    frontier_degree = [0] * len(frontier_key_to_index)
    frontier_neighbors: list[set[int]] = [set() for _ in frontier_key_to_index]
    for (source, target), multiplicity in boundary_moves.items():
        frontier_incidence[target] += multiplicity
        frontier_neighbors[target].add(source)
    frontier_degree = [len(value) for value in frontier_neighbors]

    fixed = [index for index, partner in enumerate(reflection_partner) if index == partner]
    fixed_by_shell = Counter(int(distances[index]) for index in fixed)
    output = {
        "order": ORDER,
        "complete_additional_objective_ten_rotation_orbit_count": len(added_states),
        "first_expansion_rotation_orbit_count": len(first_expansion_keys),
        "shell_distance_histogram": histogram(int(value) for value in distances),
        "maximum_shell_distance_from_original_frontier": max(int(value) for value in distances),
        "internal_directed_quotient_incidence": internal_directed_incidence,
        "simple_internal_quotient_edge_count": len(simple_internal_pairs),
        "internal_quotient_edge_multiplicity": internal_directed_incidence // 2,
        "internal_parallel_edge_excess": internal_parallel_excess,
        "internal_self_orbit_directed_incidence": self_directed_incidence,
        "internal_labeled_edge_count": internal_labeled_edges,
        "frontier_quotient_incidence": boundary_incidence,
        "simple_frontier_quotient_edge_count": len(simple_boundary_pairs),
        "frontier_parallel_incidence_excess": boundary_parallel_excess,
        "frontier_labeled_edge_count": boundary_labeled_edges,
        "distinct_original_frontier_source_orbit_count": len(frontier_key_to_index),
        "added_internal_distinct_degree_histogram": histogram(added_internal_degree),
        "added_internal_incidence_histogram": histogram(added_internal_incidence),
        "added_frontier_distinct_degree_histogram": histogram(len(value) for value in boundary_targets),
        "added_frontier_incidence_histogram": histogram(added_boundary_incidence),
        "original_frontier_added_distinct_degree_histogram": histogram(frontier_degree),
        "original_frontier_added_incidence_histogram": histogram(frontier_incidence),
        "shell_internal_edge_multiplicity": {
            f"{a}-{b}": value for (a, b), value in sorted(shell_edges.items())
        },
        "shell_simple_internal_edge_count": {
            f"{a}-{b}": value for (a, b), value in sorted(shell_simple_edges.items())
        },
        "internal_component_count": len(component_list),
        "internal_component_profiles": component_profiles,
        "reflection_fixed_rotation_orbit_count": len(fixed),
        "reflection_fixed_rotation_orbit_count_by_shell": {
            str(key): value for key, value in sorted(fixed_by_shell.items())
        },
        "dihedral_orbit_count": (len(added_states) + len(fixed)) // 2,
        "reflection_component_partners": reflected_components,
        "method": "exact cyclic quotient-neighbor scan of every one-edge move from all 527 added representatives, with independent first-shell and aggregate checks",
        "scope_note": "Structure of the 527 objective-ten orbits added beyond the original frontier; not a classification of disconnected sublevel-ten components or of the complete objective-eleven frontier.",
    }
    print(json.dumps(output, indent=2, sort_keys=False))


if __name__ == "__main__":
    main()
