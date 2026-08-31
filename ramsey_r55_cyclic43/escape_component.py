#!/usr/bin/env python3
"""Classify the objective-at-most-three component around the Cyclic(43) C86."""

from __future__ import annotations

import argparse
import itertools
import json
from array import array
from collections import Counter
from pathlib import Path

from defect_cycle import edge_position, position_edge
from local_rigidity import (
    complete_graph_edges,
    direct_count,
    initial_colors,
    is_monochromatic,
)
from solve_cyclic43 import ORDER, cyclic_distance, edge, load_certificate


def boundary_positions(state_index: int) -> list[int]:
    """Return the certified objective-three exit positions at a C86 state."""
    if not 0 <= state_index < 2 * ORDER:
        raise ValueError(state_index)
    k = state_index // 2
    last = k if state_index % 2 else k - 1
    return sorted(17 * j % ORDER for j in range(k - 8, last + 1))


def cycle_state_masks(transport_positions: list[int]) -> list[int]:
    """Encode the 86 cycle states relative to the primary certificate."""
    if len(transport_positions) != 2 * ORDER:
        raise ValueError(len(transport_positions))
    states = []
    mask = 0
    for position in transport_positions:
        states.append(mask)
        mask ^= 1 << position
    if mask:
        raise AssertionError("transport does not return to the primary state")
    if len(set(states)) != 2 * ORDER:
        raise AssertionError("cycle states are not distinct")
    return states


def mask_components(
    masks: set[int], adjacency: dict[int, list[int]]
) -> list[set[int]]:
    unseen = masks.copy()
    components = []
    while unseen:
        start = next(iter(unseen))
        component = {start}
        stack = [start]
        unseen.remove(start)
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        components.append(component)
    return components


def reflection_orbits(positions: list[int], center: int) -> list[list[int]]:
    """Orbits of length-one edges under the vertex reflection x -> center-x."""
    position_set = set(positions)
    unseen = position_set.copy()
    orbits = []
    while unseen:
        position = min(unseen)
        partner = (center - 1 - position) % ORDER
        if partner not in position_set:
            raise AssertionError((position, partner))
        orbit = sorted({position, partner})
        unseen.difference_update(orbit)
        orbits.append(orbit)
    return orbits


def build_structure(certificate: Path, cycle_path: Path) -> dict[str, object]:
    cycle = json.loads(cycle_path.read_text())
    required = {
        "full_one_flip_neutral_component_is_cycle_C86": True,
        "off_component_neighbor_minimum": 3,
        "off_component_minimizers_follow_modular_window": True,
    }
    for field, expected in required.items():
        if cycle.get(field) != expected:
            raise ValueError(f"{cycle_path} lacks required field {field}")

    transport_positions = cycle["edge_positions"]
    center_masks = cycle_state_masks(transport_positions)
    center_mask_set = set(center_masks)

    boundary_metadata: dict[int, tuple[int, int]] = {}
    for state_index, center_mask in enumerate(center_masks):
        for exit_position in boundary_positions(state_index):
            boundary_mask = center_mask ^ (1 << exit_position)
            if boundary_mask in boundary_metadata:
                raise AssertionError(
                    (boundary_mask, boundary_metadata[boundary_mask], state_index)
                )
            boundary_metadata[boundary_mask] = (state_index, exit_position)
    boundary_masks = set(boundary_metadata)
    if len(boundary_masks) != 731:
        raise AssertionError(len(boundary_masks))
    if boundary_masks & center_mask_set:
        raise AssertionError("boundary intersects C86")

    center_adjacency = {
        mask: [mask ^ (1 << position) for position in range(ORDER)
               if mask ^ (1 << position) in center_mask_set]
        for mask in center_mask_set
    }
    if Counter(map(len, center_adjacency.values())) != Counter({2: 86}):
        raise AssertionError("center masks do not induce C86")

    boundary_adjacency = {
        mask: [mask ^ (1 << position) for position in range(ORDER)
               if mask ^ (1 << position) in boundary_masks]
        for mask in boundary_masks
    }
    boundary_degree_histogram = Counter(map(len, boundary_adjacency.values()))
    if boundary_degree_histogram != Counter({1: 86, 2: 645}):
        raise AssertionError(boundary_degree_histogram)

    components = mask_components(boundary_masks, boundary_adjacency)
    component_size_histogram = Counter(map(len, components))
    if component_size_histogram != Counter({17: 43}):
        raise AssertionError(component_size_histogram)
    component_exit_positions = []
    for component in components:
        degree_histogram = Counter(len(boundary_adjacency[mask]) for mask in component)
        if degree_histogram != Counter({1: 2, 2: 15}):
            raise AssertionError(degree_histogram)
        exits = {boundary_metadata[mask][1] for mask in component}
        if len(exits) != 1:
            raise AssertionError(exits)
        component_exit_positions.append(next(iter(exits)))
    if set(component_exit_positions) != set(range(ORDER)):
        raise AssertionError(component_exit_positions)

    center_neighbors_per_boundary = Counter()
    for boundary_mask in boundary_masks:
        count = sum(
            boundary_mask ^ (1 << position) in center_mask_set
            for position in range(ORDER)
        )
        center_neighbors_per_boundary[count] += 1
    if center_neighbors_per_boundary != Counter({1: 731}):
        raise AssertionError(center_neighbors_per_boundary)

    primary_positions = {
        edge_position(changed_edge) for changed_edge in load_certificate(certificate)
    }
    if any(cyclic_distance(*changed_edge) != 1
           for changed_edge in load_certificate(certificate)):
        raise AssertionError("primary certificate has a non-length-one flip")
    state_positions = [
        primary_positions.symmetric_difference(
            position for position in range(ORDER) if mask >> position & 1
        )
        for mask in center_masks
    ]
    even_base = state_positions[0]
    odd_base = state_positions[1]
    for k in range(ORDER):
        rotation = 17 * k % ORDER
        if state_positions[2 * k] != {(p + rotation) % ORDER for p in even_base}:
            raise AssertionError(("even rotation", k))
        if state_positions[2 * k + 1] != {
            (p + rotation) % ORDER for p in odd_base
        }:
            raise AssertionError(("odd rotation", k))

    reflection_centers = [20, 37]
    bases = [even_base, odd_base]
    for parity, (base, reflection_center) in enumerate(
        zip(bases, reflection_centers, strict=True)
    ):
        reflected = {
            (reflection_center - 1 - position) % ORDER for position in base
        }
        if reflected != base:
            raise AssertionError(("reflection", parity))

    dihedral_orbits = [
        reflection_orbits(boundary_positions(parity), reflection_centers[parity])
        for parity in range(2)
    ]
    if list(map(len, dihedral_orbits)) != [4, 5]:
        raise AssertionError(dihedral_orbits)

    boundary_edge_count = sum(boundary_degree_histogram[degree] * degree
                              for degree in boundary_degree_histogram) // 2
    vertex_degree_histogram = Counter({2: 86, 3: 645, 10: 43, 11: 43})
    return {
        "certificate": certificate.name,
        "cycle_certificate": cycle_path.name,
        "order": ORDER,
        "objective_two_vertex_count": len(center_masks),
        "objective_three_boundary_vertex_count": len(boundary_masks),
        "boundary_vertices_are_distinct": True,
        "boundary_center_neighbor_histogram": {"1": 731},
        "boundary_induced_degree_histogram": {
            str(degree): count
            for degree, count in sorted(boundary_degree_histogram.items())
        },
        "boundary_component_count": len(components),
        "boundary_component_size_histogram": {
            str(size): count
            for size, count in sorted(component_size_histogram.items())
        },
        "boundary_components_are_P17": True,
        "boundary_component_exit_positions": sorted(component_exit_positions),
        "boundary_induced_edge_count": boundary_edge_count,
        "center_boundary_edge_count": len(boundary_masks),
        "center_induced_edge_count": len(center_masks),
        "candidate_sublevel_three_vertex_count": (
            len(center_masks) + len(boundary_masks)
        ),
        "candidate_sublevel_three_edge_count": (
            len(center_masks) + len(boundary_masks) + boundary_edge_count
        ),
        "candidate_sublevel_three_degree_histogram": {
            str(degree): count
            for degree, count in sorted(vertex_degree_histogram.items())
        },
        "even_states_are_rotations_of_state_zero": True,
        "odd_states_are_rotations_of_state_one": True,
        "rotation_step": 17,
        "even_center_reflection": "x -> 20-x mod 43",
        "odd_center_reflection": "x -> 37-x mod 43",
        "even_exit_dihedral_orbits": dihedral_orbits[0],
        "odd_exit_dihedral_orbits": dihedral_orbits[1],
        "boundary_rotation_orbit_count": 17,
        "boundary_dihedral_orbit_count": 9,
        "structural_scope_note": (
            "The P17 decomposition follows exactly from the certified modular "
            "exit windows and 43-bit length-one masks. Full sublevel-three "
            "closure additionally requires the representative all-edge scan."
        ),
        "_center_masks": center_masks,
        "_boundary_masks": boundary_masks,
        "_boundary_metadata": boundary_metadata,
        "_boundary_adjacency": boundary_adjacency,
    }


def scan_boundary_representatives(
    certificate: Path,
    structure: dict[str, object],
    direct_verify: bool,
) -> dict[str, object]:
    flips = load_certificate(certificate)
    colors, edges = initial_colors(flips)
    edge_ids, _ = complete_graph_edges()
    incident = [array("I") for _ in edges]
    red_counts = array("b")

    for vertices in itertools.combinations(range(ORDER), 5):
        five_id = len(red_counts)
        ids = [
            edge_ids[edge(a, b)] for a, b in itertools.combinations(vertices, 2)
        ]
        red_counts.append(sum(colors[edge_id] for edge_id in ids))
        for edge_id in ids:
            incident[edge_id].append(five_id)
    current_count = sum(is_monochromatic(count) for count in red_counts)
    if current_count != 2:
        raise AssertionError(current_count)

    def resulting_count(edge_id: int) -> int:
        delta = -1 if colors[edge_id] else 1
        result = current_count
        for five_id in incident[edge_id]:
            count = red_counts[five_id]
            result += is_monochromatic(count + delta) - is_monochromatic(count)
        return result

    def toggle(edge_id: int) -> None:
        nonlocal current_count
        delta = -1 if colors[edge_id] else 1
        for five_id in incident[edge_id]:
            count = red_counts[five_id]
            current_count += (
                is_monochromatic(count + delta) - is_monochromatic(count)
            )
            red_counts[five_id] += delta
        colors[edge_id] = not colors[edge_id]

    center_masks = structure["_center_masks"]
    boundary_masks = structure["_boundary_masks"]
    boundary_adjacency = structure["_boundary_adjacency"]
    representative_records = []
    aggregate_histogram: Counter[int] = Counter()
    signature_by_type: dict[tuple[int, int], tuple[tuple[int, int], ...]] = {}
    direct_recount_count = 0

    for parity in range(2):
        for exit_position in boundary_positions(parity):
            exit_id = edge_ids[position_edge(exit_position)]
            toggle(exit_id)
            if current_count != 3:
                raise AssertionError((parity, exit_position, current_count))
            if direct_verify:
                recounted, witnesses = direct_count(colors, edge_ids)
                if recounted != current_count:
                    raise AssertionError((parity, exit_position, recounted))
                direct_recount_count += 1
            else:
                witnesses = []

            resulting_counts = [
                resulting_count(edge_id) for edge_id in range(len(edges))
            ]
            histogram = Counter(resulting_counts)
            signature = tuple(sorted(histogram.items()))
            aggregate_histogram.update(
                {objective: ORDER * count for objective, count in histogram.items()}
            )
            objective_two_ids = [
                edge_id for edge_id, count in enumerate(resulting_counts) if count == 2
            ]
            if objective_two_ids != [exit_id]:
                raise AssertionError((parity, exit_position, objective_two_ids))

            boundary_mask = center_masks[parity] ^ (1 << exit_position)
            objective_three_masks = set()
            for edge_id, count in enumerate(resulting_counts):
                if count != 3:
                    continue
                changed_edge = edges[edge_id]
                if cyclic_distance(*changed_edge) != 1:
                    raise AssertionError((parity, exit_position, changed_edge))
                neighbor = boundary_mask ^ (1 << edge_position(changed_edge))
                if neighbor not in boundary_masks:
                    raise AssertionError((parity, exit_position, changed_edge))
                objective_three_masks.add(neighbor)
            expected_neighbors = set(boundary_adjacency[boundary_mask])
            if objective_three_masks != expected_neighbors:
                raise AssertionError(
                    (parity, exit_position, objective_three_masks, expected_neighbors)
                )

            reflection_center = [20, 37][parity]
            partner = (reflection_center - 1 - exit_position) % ORDER
            signature_by_type[(parity, exit_position)] = signature
            representative_records.append(
                {
                    "center_parity": parity,
                    "exit_position": exit_position,
                    "reflection_partner": partner,
                    "objective_two_neighbor_count": histogram[2],
                    "objective_three_neighbor_count": histogram[3],
                    "neighbor_objective_histogram": {
                        str(objective): count
                        for objective, count in sorted(histogram.items())
                    },
                    "direct_recount_witnesses": witnesses,
                }
            )
            toggle(exit_id)
            if current_count != 2:
                raise AssertionError(current_count)

        if parity == 0:
            toggle(edge_ids[position_edge(42)])
            if current_count != 2:
                raise AssertionError(current_count)

    toggle(edge_ids[position_edge(42)])
    if current_count != 2:
        raise AssertionError(current_count)

    for record in representative_records:
        key = (record["center_parity"], record["exit_position"])
        partner_key = (record["center_parity"], record["reflection_partner"])
        if signature_by_type[key] != signature_by_type[partner_key]:
            raise AssertionError((key, partner_key))

    dihedral_records = []
    for record in representative_records:
        exit_position = record["exit_position"]
        partner = record["reflection_partner"]
        if exit_position > partner:
            continue
        compact_record = {
            key: value
            for key, value in record.items()
            if key not in {"exit_position", "reflection_partner"}
        }
        compact_record["exit_position_orbit"] = sorted({exit_position, partner})
        dihedral_records.append(compact_record)
    if len(dihedral_records) != 9:
        raise AssertionError(len(dihedral_records))

    if sum(aggregate_histogram.values()) != 731 * len(edges):
        raise AssertionError(sum(aggregate_histogram.values()))
    return {
        "all_edge_rotation_representative_count": len(representative_records),
        "all_edge_rotation_representative_neighbor_checks": (
            len(representative_records) * len(edges)
        ),
        "symmetry_lifted_boundary_neighbor_checks": 731 * len(edges),
        "boundary_dihedral_representative_records": dihedral_records,
        "aggregate_boundary_neighbor_objective_histogram": {
            str(objective): count
            for objective, count in sorted(aggregate_histogram.items())
        },
        "each_boundary_vertex_has_unique_objective_two_neighbor": True,
        "all_objective_three_neighbors_remain_in_boundary_paths": True,
        "full_sublevel_three_component_through_C86_is_closed": True,
        "full_sublevel_three_component_through_C86_is_C86_plus_43_P17": True,
        "direct_recount_representative_count": direct_recount_count,
        "enumeration_scope_note": (
            "All 903 edge reversals are checked for 17 rotational boundary "
            "representatives. Proven rotations lift this to all 731 boundary "
            "vertices. The scan finds no additional objective-at-most-three "
            "neighbor, so the 817-vertex candidate is the complete connected "
            "sublevel-three component through C86."
        ),
    }


def analyze(
    certificate: Path,
    cycle_path: Path,
    all_edge_neighbors: bool = False,
    direct_verify: bool = False,
) -> dict[str, object]:
    structure = build_structure(certificate, cycle_path)
    private_fields = [key for key in structure if key.startswith("_")]
    result = {
        key: value for key, value in structure.items() if key not in private_fields
    }
    if all_edge_neighbors:
        result.update(
            scan_boundary_representatives(certificate, structure, direct_verify)
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--cycle", type=Path, required=True)
    parser.add_argument("--all-edge-neighbors", action="store_true")
    parser.add_argument("--direct-verify", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.direct_verify and not args.all_edge_neighbors:
        parser.error("--direct-verify requires --all-edge-neighbors")
    result = analyze(
        args.certificate,
        args.cycle,
        all_edge_neighbors=args.all_edge_neighbors,
        direct_verify=args.direct_verify,
    )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
