#!/usr/bin/env python3
"""Decompose the objective-eleven boundary contributed by the P10 addition.

The complete objective-eleven frontier certificate records incidence by source
objective, but it does not distinguish the original 128,184-orbit objective-ten
frontier from the 527 orbits added during closure.  This script rescans all
one-edge moves from those 527 representatives in the exact cyclic quotient,
intersects them with the complete objective-eleven certificate, and subtracts
their incidences target by target.  It also resolves the result by the 21
components, four distance shells, and reflection action certified for the
addition.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path
from typing import Iterable

from analyze_objective_ten_component_structure import (
    EDGE_COUNT,
    KEY_BIT,
    ORDER,
    REFLECTED_EDGE,
    ROTATED_EDGE,
    canonical_key,
    components,
    histogram,
    rotated_keys,
    state_key,
)


def pair_histogram(values: Iterable[tuple[int, ...]]) -> dict[str, int]:
    return {
        ",".join(map(str, key)): count
        for key, count in sorted(Counter(values).items())
    }


def connected_component_count(adjacency: list[set[int]]) -> int:
    unseen = set(range(len(adjacency)))
    count = 0
    while unseen:
        count += 1
        queue = [unseen.pop()]
        while queue:
            source = queue.pop()
            for target in adjacency[source]:
                if target in unseen:
                    unseen.remove(target)
                    queue.append(target)
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("objective_eleven_frontier", type=Path)
    parser.add_argument("objective_ten_frontier", type=Path)
    parser.add_argument("objective_ten_component", type=Path)
    parser.add_argument("objective_ten_component_independent", type=Path)
    parser.add_argument("objective_ten_component_structure", type=Path)
    parser.add_argument(
        "--independent-objective-eleven-frontier", type=Path
    )
    args = parser.parse_args()

    eleven = json.loads(args.objective_eleven_frontier.read_text())
    ten_frontier = json.loads(args.objective_ten_frontier.read_text())
    ten_component = json.loads(args.objective_ten_component.read_text())
    ten_independent = json.loads(
        args.objective_ten_component_independent.read_text()
    )
    ten_structure = json.loads(args.objective_ten_component_structure.read_text())

    eleven_states = eleven["objective_eleven_rotation_representatives"]
    eleven_signatures = eleven[
        "objective_eleven_incidence_signatures_2_through_10"
    ]
    if len(eleven_states) != len(eleven_signatures):
        raise RuntimeError("objective-eleven representative/signature mismatch")
    eleven_keys = [state_key(state) for state in eleven_states]
    eleven_index = {key: index for index, key in enumerate(eleven_keys)}
    if len(eleven_index) != len(eleven_keys):
        raise RuntimeError("duplicate objective-eleven representative")
    independent_global_agreement = False
    if args.independent_objective_eleven_frontier is not None:
        independent_eleven = json.loads(
            args.independent_objective_eleven_frontier.read_text()
        )
        checked_fields = (
            "complete_sublevel_ten_source_rotation_orbit_count",
            "complete_sublevel_ten_source_vertex_count",
            "objective_eleven_first_frontier_rotation_orbit_count",
            "objective_eleven_first_frontier_vertex_count",
            "directed_labeled_incidence_by_source_objective",
            "total_directed_labeled_incidence",
            "incidence_signature_count",
            "incidence_degree_histogram",
            "minimum_incident_source_objective_histogram",
            "incidence_signature_histogram",
            "objective_eleven_rotation_representatives",
            "objective_eleven_incidence_signatures_2_through_10",
        )
        if any(eleven[field] != independent_eleven[field] for field in checked_fields):
            raise RuntimeError(
                "optimized and independent objective-eleven frontiers disagree"
            )
        independent_global_agreement = True

    frontier_states = ten_frontier["objective_ten_rotation_representatives"]
    added_states = ten_component[
        "additional_objective_10_rotation_representatives"
    ]
    first_expansion_states = ten_independent[
        "newly_exposed_objective_10_rotation_representatives"
    ]
    frontier_keys = {state_key(state) for state in frontier_states}
    added_keys = [state_key(state) for state in added_states]
    added_index = {key: index for index, key in enumerate(added_keys)}
    first_expansion_keys = {state_key(state) for state in first_expansion_states}
    if len(frontier_keys) != 128_184 or len(added_index) != 527:
        raise RuntimeError("unexpected objective-ten certificate size")
    if frontier_keys & set(added_keys):
        raise RuntimeError("objective-ten frontier/addition overlap")

    added_adjacency = [set() for _ in added_states]
    boundary_targets = [set() for _ in added_states]
    addition_eleven_moves: dict[tuple[int, int], int] = defaultdict(int)
    for source, state in enumerate(added_states):
        source_rotations = rotated_keys(state)
        for edge in range(EDGE_COUNT):
            target_key = min(
                source_rotations[offset] ^ KEY_BIT[ROTATED_EDGE[offset][edge]]
                for offset in range(ORDER)
            )
            added_target = added_index.get(target_key)
            if added_target is not None:
                added_adjacency[source].add(added_target)
            elif target_key in frontier_keys:
                boundary_targets[source].add(target_key)
            eleven_target = eleven_index.get(target_key)
            if eleven_target is not None:
                addition_eleven_moves[(source, eleven_target)] += 1

    distances: list[int | None] = [None] * len(added_states)
    queue: deque[int] = deque()
    for source, targets in enumerate(boundary_targets):
        if targets:
            distances[source] = 1
            queue.append(source)
    while queue:
        source = queue.popleft()
        assert distances[source] is not None
        for target in added_adjacency[source]:
            if distances[target] is None:
                distances[target] = distances[source] + 1
                queue.append(target)
    if any(distance is None for distance in distances):
        raise RuntimeError("unreached objective-ten addition orbit")
    if {
        added_keys[index]
        for index, distance in enumerate(distances)
        if distance == 1
    } != first_expansion_keys:
        raise RuntimeError("first addition shell mismatch")
    distance_histogram = histogram(int(distance) for distance in distances)
    if distance_histogram != ten_structure["shell_distance_histogram"]:
        raise RuntimeError("addition shell histogram mismatch")

    component_list = components(added_adjacency)
    if len(component_list) != ten_structure["internal_component_count"]:
        raise RuntimeError("addition component-count mismatch")
    component_index = {
        vertex: index
        for index, component in enumerate(component_list)
        for vertex in component
    }
    if [len(component) for component in component_list] != [
        profile["added_orbit_count"]
        for profile in ten_structure["internal_component_profiles"]
    ]:
        raise RuntimeError("addition component profile mismatch")

    target_sources: dict[int, set[int]] = defaultdict(set)
    target_components: dict[int, set[int]] = defaultdict(set)
    target_shells: dict[int, set[int]] = defaultdict(set)
    target_addition_incidence: Counter[int] = Counter()
    source_target_sets = [set() for _ in added_states]
    source_incidence = [0] * len(added_states)
    for (source, target), multiplicity in addition_eleven_moves.items():
        target_sources[target].add(source)
        target_components[target].add(component_index[source])
        target_shells[target].add(int(distances[source]))
        target_addition_incidence[target] += multiplicity
        source_target_sets[source].add(target)
        source_incidence[source] += multiplicity

    touched_targets = set(target_sources)
    quotient_incidence = sum(target_addition_incidence.values())
    expected_labeled_incidence = ten_independent[
        "additional_neighbor_objective_histogram_by_source_objective"
    ]["10"]["11"]
    if ORDER * quotient_incidence != expected_labeled_incidence:
        raise RuntimeError("objective-eleven addition incidence mismatch")

    preaddition_incidence: dict[int, int] = {}
    original_ten_incidence: dict[int, int] = {}
    for target in touched_targets:
        signature = eleven_signatures[target]
        if len(signature) != 9:
            raise RuntimeError("invalid objective-eleven incidence signature")
        added = target_addition_incidence[target]
        original_ten = signature[8] - added
        if original_ten < 0:
            raise RuntimeError("addition incidence exceeds global signature")
        original_ten_incidence[target] = original_ten
        preaddition_incidence[target] = sum(signature[:8]) + original_ten
    exclusive_targets = {
        target for target in touched_targets if preaddition_incidence[target] == 0
    }
    shared_targets = touched_targets - exclusive_targets
    if any(
        any(eleven_signatures[target][index] for index in range(8))
        or original_ten_incidence[target]
        for target in exclusive_targets
    ):
        raise RuntimeError("exclusive target has a pre-addition incidence")

    parallel_source_target_excess = sum(
        multiplicity - 1 for multiplicity in addition_eleven_moves.values()
    )
    target_component_support_histogram = histogram(
        len(value) for value in target_components.values()
    )
    target_shell_support_histogram = pair_histogram(
        tuple(sorted(value)) for value in target_shells.values()
    )
    exclusive_target_shell_support_histogram = pair_histogram(
        tuple(sorted(target_shells[target])) for target in exclusive_targets
    )

    component_intersection = [set() for _ in component_list]
    component_pair_target_counts: Counter[tuple[int, int]] = Counter()
    for target, support in target_components.items():
        for first, second in combinations(sorted(support), 2):
            component_intersection[first].add(second)
            component_intersection[second].add(first)
            component_pair_target_counts[(first, second)] += 1
    intersection_components = components(component_intersection)

    component_profiles = []
    for index, component in enumerate(component_list):
        incident_targets = {
            target
            for source in component
            for target in source_target_sets[source]
        }
        component_profiles.append(
            {
                "index": index,
                "source_orbit_count": len(component),
                "objective_eleven_quotient_incidence": sum(
                    source_incidence[source] for source in component
                ),
                "distinct_objective_eleven_target_orbit_count": len(
                    incident_targets
                ),
                "exclusive_target_orbit_count": len(
                    incident_targets & exclusive_targets
                ),
                "shared_target_orbit_count": len(incident_targets & shared_targets),
                "other_component_neighbor_count": len(
                    component_intersection[index]
                ),
            }
        )

    reflected_target: dict[int, int] = {}
    for target in touched_targets:
        reflected_key = canonical_key(
            REFLECTED_EDGE[edge] for edge in eleven_states[target]
        )
        partner = eleven_index.get(reflected_key)
        if partner is None or partner not in touched_targets:
            raise RuntimeError("touched objective-eleven boundary is not reflection invariant")
        reflected_target[target] = partner
    if any(reflected_target[reflected_target[target]] != target for target in touched_targets):
        raise RuntimeError("objective-eleven reflection is not an involution")
    if {reflected_target[target] for target in exclusive_targets} != exclusive_targets:
        raise RuntimeError("exclusive objective-eleven boundary is not reflection invariant")
    fixed_targets = {
        target for target, partner in reflected_target.items() if target == partner
    }
    fixed_exclusive_targets = fixed_targets & exclusive_targets

    global_incidence = sum(sum(signature) for signature in eleven_signatures)
    output = {
        "order": ORDER,
        "complete_objective_eleven_frontier_rotation_orbit_count": len(
            eleven_states
        ),
        "complete_objective_eleven_frontier_quotient_incidence": global_incidence,
        "optimized_and_independent_global_frontiers_agree": independent_global_agreement,
        "preaddition_objective_eleven_frontier_rotation_orbit_count": len(
            eleven_states
        )
        - len(exclusive_targets),
        "preaddition_objective_eleven_quotient_incidence": global_incidence
        - quotient_incidence,
        "preaddition_objective_eleven_labeled_incidence": ORDER
        * (global_incidence - quotient_incidence),
        "objective_ten_addition_source_rotation_orbit_count": len(added_states),
        "addition_touched_objective_eleven_target_rotation_orbit_count": len(
            touched_targets
        ),
        "addition_objective_eleven_quotient_incidence": quotient_incidence,
        "addition_objective_eleven_labeled_incidence": ORDER * quotient_incidence,
        "addition_source_target_parallel_incidence_excess": parallel_source_target_excess,
        "addition_exclusive_objective_eleven_target_rotation_orbit_count": len(
            exclusive_targets
        ),
        "addition_shared_objective_eleven_target_rotation_orbit_count": len(
            shared_targets
        ),
        "addition_exclusive_objective_eleven_target_vertex_count": ORDER
        * len(exclusive_targets),
        "addition_source_distinct_target_degree_histogram": histogram(
            len(targets) for targets in source_target_sets
        ),
        "addition_source_incidence_histogram": histogram(source_incidence),
        "target_distinct_addition_source_degree_histogram": histogram(
            len(value) for value in target_sources.values()
        ),
        "target_addition_incidence_histogram": histogram(
            target_addition_incidence.values()
        ),
        "target_preaddition_incidence_histogram": histogram(
            preaddition_incidence.values()
        ),
        "target_component_support_size_histogram": target_component_support_histogram,
        "target_shell_support_histogram": target_shell_support_histogram,
        "exclusive_target_shell_support_histogram": exclusive_target_shell_support_histogram,
        "targets_incident_to_multiple_addition_components": sum(
            len(value) > 1 for value in target_components.values()
        ),
        "addition_component_intersection_simple_edge_count": sum(
            len(value) for value in component_intersection
        )
        // 2,
        "addition_component_intersection_connected_component_count": connected_component_count(
            component_intersection
        ),
        "addition_component_intersection_component_size_histogram": histogram(
            len(component) for component in intersection_components
        ),
        "addition_component_intersection_cycle_rank": sum(
            len(value) for value in component_intersection
        )
        // 2
        - len(component_intersection)
        + len(intersection_components),
        "addition_component_pair_shared_target_count": {
            f"{first}-{second}": count
            for (first, second), count in sorted(
                component_pair_target_counts.items()
            )
        },
        "addition_component_objective_eleven_profiles": component_profiles,
        "reflection_fixed_touched_target_rotation_orbit_count": len(fixed_targets),
        "reflection_fixed_exclusive_target_rotation_orbit_count": len(
            fixed_exclusive_targets
        ),
        "touched_target_dihedral_orbit_count": (
            len(touched_targets) + len(fixed_targets)
        )
        // 2,
        "exclusive_target_dihedral_orbit_count": (
            len(exclusive_targets) + len(fixed_exclusive_targets)
        )
        // 2,
        "method": "exact cyclic canonicalization of every one-edge move from all 527 added objective-ten representatives, targetwise subtraction from the complete objective-eleven incidence certificate, and exact shell/component/reflection analysis",
        "scope_note": "Classifies the part of the complete first objective-eleven frontier incident to the 527-orbit threshold-ten addition; it does not assert threshold-eleven closure or classify disconnected sublevel-ten components.",
    }
    print(json.dumps(output, indent=2, sort_keys=False))


if __name__ == "__main__":
    main()
