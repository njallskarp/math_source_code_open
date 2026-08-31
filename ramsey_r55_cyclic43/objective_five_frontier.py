#!/usr/bin/env python3
"""Enumerate the first objective-five frontier around the Cyclic(43) basin."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from defect_cycle import position_edge
from escape_component import boundary_positions
from objective_four_frontier import (
    CliqueEngine,
    Edge,
    FlipSet,
    canonical_rotation,
    cycle_and_boundary_states,
    rotation_orbit,
    toggle_member,
)
from local_rigidity import direct_count
from solve_cyclic43 import ORDER, load_certificate


def toggled_state(flips: set[Edge] | FlipSet, changed_edge: Edge) -> FlipSet:
    result = set(flips)
    toggle_member(result, changed_edge)
    return frozenset(result)


def analyze(
    certificate: Path,
    cycle_path: Path,
    escape_path: Path,
    objective_four_path: Path,
    scan_frontier: bool = False,
    direct_verify: bool = False,
) -> dict[str, object]:
    primary = frozenset(load_certificate(certificate))
    cycle = json.loads(cycle_path.read_text())
    escape = json.loads(escape_path.read_text())
    objective_four = json.loads(objective_four_path.read_text())
    if not escape.get("full_sublevel_three_component_through_C86_is_closed"):
        raise ValueError("escape certificate does not prove sublevel-three closure")
    if not objective_four.get("complete_sublevel_four_component_is_closed"):
        raise ValueError("objective-four certificate does not prove closure")

    centers, boundaries = cycle_and_boundary_states(primary, cycle["edge_positions"])
    engine = CliqueEngine(primary)
    objective_four_orbits: dict[tuple[Edge, ...], FlipSet] = {}
    objective_five_directed_representatives: list[tuple[int, FlipSet]] = []

    def add_objective_four(state: FlipSet) -> None:
        canonical = canonical_rotation(state)
        objective_four_orbits.setdefault(canonical, state)

    def add_objective_five(source_objective: int, state: FlipSet) -> None:
        objective_five_directed_representatives.append((source_objective, state))

    for parity in range(2):
        engine.move_to(centers[parity])
        if engine.current_count != 2:
            raise AssertionError((parity, engine.current_count))
        center_counts = engine.all_resulting_counts()
        for edge_id, objective in enumerate(center_counts):
            state = toggled_state(engine.current_flips, engine.edges[edge_id])
            if objective == 4:
                add_objective_four(state)
            elif objective == 5:
                add_objective_five(2, state)

        for exit_position in boundary_positions(parity):
            exit_edge = position_edge(exit_position)
            engine.toggle(exit_edge)
            if engine.current_count != 3:
                raise AssertionError((parity, exit_position, engine.current_count))
            boundary_counts = engine.all_resulting_counts()
            for edge_id, objective in enumerate(boundary_counts):
                state = toggled_state(engine.current_flips, engine.edges[edge_id])
                if objective == 4:
                    add_objective_four(state)
                elif objective == 5:
                    add_objective_five(3, state)
            engine.toggle(exit_edge)
            if engine.current_count != 2:
                raise AssertionError(engine.current_count)

    objective_four_queue = sorted(objective_four_orbits)
    queue_index = 0
    while queue_index < len(objective_four_queue):
        canonical = objective_four_queue[queue_index]
        queue_index += 1
        representative = objective_four_orbits[canonical]
        engine.move_to(representative)
        if engine.current_count != 4:
            raise AssertionError((queue_index, engine.current_count))
        resulting_counts = engine.all_resulting_counts()
        for edge_id, objective in enumerate(resulting_counts):
            state = toggled_state(engine.current_flips, engine.edges[edge_id])
            if objective == 4:
                neighbor_canonical = canonical_rotation(state)
                if neighbor_canonical not in objective_four_orbits:
                    if len(rotation_orbit(state)) != ORDER:
                        raise AssertionError(
                            "objective-four state has rotational stabilizer"
                        )
                    objective_four_orbits[neighbor_canonical] = state
                    objective_four_queue.append(neighbor_canonical)
            elif objective == 5:
                add_objective_five(4, state)

    if len(objective_four_orbits) != 78:
        raise AssertionError(len(objective_four_orbits))

    representative_source_histogram = Counter(
        source for source, _ in objective_five_directed_representatives
    )
    expected_representatives = Counter({2: 42, 3: 182, 4: 463})
    if representative_source_histogram != expected_representatives:
        raise AssertionError(representative_source_histogram)

    objective_five_orbits: dict[tuple[Edge, ...], FlipSet] = {}
    for _, state in objective_five_directed_representatives:
        objective_five_orbits.setdefault(canonical_rotation(state), state)
    frontier_states = set()
    for representative in objective_five_orbits.values():
        orbit = rotation_orbit(representative)
        if len(orbit) != ORDER:
            raise AssertionError("objective-five state has rotational stabilizer")
        frontier_states.update(orbit)
    if len(frontier_states) != ORDER * len(objective_five_orbits):
        raise AssertionError("objective-five rotation orbits overlap")

    source_incidence: dict[FlipSet, Counter[int]] = {
        state: Counter() for state in frontier_states
    }
    for source_objective, representative in objective_five_directed_representatives:
        for rotated in rotation_orbit(representative):
            source_incidence[rotated][source_objective] += 1
    directed_count = sum(sum(counts.values()) for counts in source_incidence.values())
    if directed_count != 29_541:
        raise AssertionError(directed_count)
    incidence_signature_histogram = Counter(
        tuple(counts.get(source, 0) for source in (2, 3, 4))
        for counts in source_incidence.values()
    )

    result: dict[str, object] = {
        "certificate": certificate.name,
        "cycle_certificate": cycle_path.name,
        "escape_certificate": escape_path.name,
        "objective_four_certificate": objective_four_path.name,
        "order": ORDER,
        "objective_five_directed_center_edge_count": 1_806,
        "objective_five_directed_boundary_edge_count": 7_826,
        "objective_five_directed_objective_four_edge_count": 19_909,
        "objective_five_directed_low_component_edge_count": directed_count,
        "objective_five_directed_rotation_representative_count": len(
            objective_five_directed_representatives
        ),
        "objective_five_frontier_rotation_orbit_count": len(objective_five_orbits),
        "objective_five_frontier_vertex_count": len(frontier_states),
        "objective_five_frontier_source_incidence_signature_histogram": {
            f"{signature[0]},{signature[1]},{signature[2]}": count
            for signature, count in sorted(incidence_signature_histogram.items())
        },
        "objective_five_frontier_has_trivial_rotation_stabilizers": True,
        "direct_recount_objective_five_representative_count": 0,
        "scope_note": (
            "Every objective-five edge from the complete certified sublevel-four "
            "component is enumerated using its 97 rotational source types, then "
            "deduplicated under all 43 rotations. The objective-five frontier's "
            "own neighbors are not scanned in this certificate."
        ),
    }

    if not scan_frontier:
        return result

    known_sublevel_four_states = set(centers) | boundaries
    for representative in objective_four_orbits.values():
        known_sublevel_four_states.update(rotation_orbit(representative))
    if len(known_sublevel_four_states) != 4_171:
        raise AssertionError(len(known_sublevel_four_states))

    aggregate_neighbor_histogram: Counter[int] = Counter()
    known_low_directed: Counter[int] = Counter()
    new_low_directed: Counter[int] = Counter()
    new_low_orbits: dict[int, set[tuple[Edge, ...]]] = {
        objective: set() for objective in range(5)
    }
    known_frontier_directed = 0
    new_objective_five_directed = 0
    new_objective_five_orbits: set[tuple[Edge, ...]] = set()
    direct_recount_count = 0
    for orbit_index, canonical in enumerate(sorted(objective_five_orbits), start=1):
        representative = objective_five_orbits[canonical]
        engine.move_to(representative)
        if engine.current_count != 5:
            raise AssertionError((orbit_index, engine.current_count))
        if direct_verify:
            recounted, _ = direct_count(engine.colors, engine.edge_ids)
            if recounted != 5:
                raise AssertionError((orbit_index, recounted))
            direct_recount_count += 1
        resulting_counts = engine.all_resulting_counts()
        aggregate_neighbor_histogram.update(
            {
                objective: ORDER * count
                for objective, count in Counter(resulting_counts).items()
            }
        )
        for edge_id, objective in enumerate(resulting_counts):
            if objective > 5:
                continue
            neighbor = toggled_state(representative, engine.edges[edge_id])
            if objective <= 4:
                if neighbor in known_sublevel_four_states:
                    known_low_directed[objective] += ORDER
                else:
                    new_low_directed[objective] += ORDER
                    new_low_orbits[objective].add(canonical_rotation(neighbor))
            elif neighbor in frontier_states:
                known_frontier_directed += ORDER
            else:
                new_objective_five_directed += ORDER
                new_objective_five_orbits.add(canonical_rotation(neighbor))

    expected_known_low = Counter({2: 1_806, 3: 7_826, 4: 19_909})
    if known_low_directed != expected_known_low:
        raise AssertionError(known_low_directed)
    if known_frontier_directed % 2:
        raise AssertionError(known_frontier_directed)
    component_closed = not new_low_directed and not new_objective_five_directed
    frontier_induced_edge_count = known_frontier_directed // 2
    if component_closed and not aggregate_neighbor_histogram[6]:
        raise AssertionError("closed sublevel-five component has no level-six exit")
    sublevel_five_vertex_count = 4_171 + len(frontier_states)
    sublevel_five_edge_count = (
        10_621 + directed_count + frontier_induced_edge_count
    )

    result.update(
        {
            "objective_five_frontier_all_edge_rotation_representative_neighbor_checks": (
                len(objective_five_orbits) * len(engine.edges)
            ),
            "objective_five_frontier_symmetry_lifted_neighbor_checks": (
                len(frontier_states) * len(engine.edges)
            ),
            "aggregate_objective_five_frontier_neighbor_objective_histogram": {
                str(objective): count
                for objective, count in sorted(aggregate_neighbor_histogram.items())
            },
            "known_sublevel_four_directed_neighbor_histogram": {
                str(objective): count
                for objective, count in sorted(known_low_directed.items())
            },
            "new_objective_at_most_four_directed_neighbor_histogram": {
                str(objective): count
                for objective, count in sorted(new_low_directed.items())
            },
            "new_objective_at_most_four_rotation_orbit_histogram": {
                str(objective): len(orbits)
                for objective, orbits in sorted(new_low_orbits.items())
            },
            "objective_five_frontier_induced_edge_count": (
                frontier_induced_edge_count
            ),
            "new_objective_five_directed_neighbor_count": (
                new_objective_five_directed
            ),
            "new_objective_five_rotation_orbit_count": len(
                new_objective_five_orbits
            ),
            "direct_recount_objective_five_representative_count": (
                direct_recount_count
            ),
            "complete_sublevel_five_component_is_closed": component_closed,
            "complete_sublevel_five_component_vertex_count": (
                sublevel_five_vertex_count if component_closed else None
            ),
            "complete_sublevel_five_component_edge_count": (
                sublevel_five_edge_count if component_closed else None
            ),
            "exact_one_flip_escape_level_from_sublevel_five_component": (
                6 if component_closed else None
            ),
            "scope_note": (
                "Every objective-five edge from the complete certified sublevel-four "
                "component is enumerated using its 97 rotational source types and "
                "deduplicated under all 43 rotations. Every edge reversal at each "
                "of the resulting 306 objective-five frontier representatives is "
                "also evaluated. When no new objective-at-most-five endpoint is "
                "found, this closes the entire connected sublevel-five component."
            ),
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--cycle", type=Path, required=True)
    parser.add_argument("--escape", type=Path, required=True)
    parser.add_argument("--objective-four", type=Path, required=True)
    parser.add_argument("--scan-frontier", action="store_true")
    parser.add_argument("--direct-verify", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.direct_verify and not args.scan_frontier:
        parser.error("--direct-verify requires --scan-frontier")
    result = analyze(
        args.certificate,
        args.cycle,
        args.escape,
        args.objective_four,
        scan_frontier=args.scan_frontier,
        direct_verify=args.direct_verify,
    )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
