#!/usr/bin/env python3
"""Enumerate the first objective-six frontier around the Cyclic(43) basin."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from defect_cycle import position_edge
from escape_component import boundary_positions
from local_rigidity import direct_count
from objective_five_frontier import toggled_state
from objective_four_frontier import (
    CliqueEngine,
    Edge,
    FlipSet,
    canonical_rotation,
    cycle_and_boundary_states,
    rotation_orbit,
)
from solve_cyclic43 import ORDER, load_certificate


def analyze(
    certificate: Path,
    cycle_path: Path,
    escape_path: Path,
    objective_four_path: Path,
    objective_five_path: Path,
    direct_verify_strata: bool = False,
) -> dict[str, object]:
    primary = frozenset(load_certificate(certificate))
    cycle = json.loads(cycle_path.read_text())
    escape = json.loads(escape_path.read_text())
    objective_four = json.loads(objective_four_path.read_text())
    objective_five = json.loads(objective_five_path.read_text())
    if not escape.get("full_sublevel_three_component_through_C86_is_closed"):
        raise ValueError("escape certificate does not prove sublevel-three closure")
    if not objective_four.get("complete_sublevel_four_component_is_closed"):
        raise ValueError("objective-four certificate does not prove closure")
    if not objective_five.get("complete_sublevel_five_component_is_closed"):
        raise ValueError("objective-five certificate does not prove closure")

    centers, boundaries = cycle_and_boundary_states(primary, cycle["edge_positions"])
    engine = CliqueEngine(primary)
    objective_four_orbits: dict[tuple[Edge, ...], FlipSet] = {}
    objective_five_orbits: dict[tuple[Edge, ...], FlipSet] = {}
    objective_six_directed_representatives: list[tuple[int, FlipSet]] = []

    def add_objective_four(state: FlipSet) -> None:
        objective_four_orbits.setdefault(canonical_rotation(state), state)

    def add_objective_five(state: FlipSet) -> None:
        objective_five_orbits.setdefault(canonical_rotation(state), state)

    def add_objective_six(source_objective: int, state: FlipSet) -> None:
        objective_six_directed_representatives.append((source_objective, state))

    for parity in range(2):
        engine.move_to(centers[parity])
        if engine.current_count != 2:
            raise AssertionError((parity, engine.current_count))
        for edge_id, objective in enumerate(engine.all_resulting_counts()):
            if objective not in (4, 5, 6):
                continue
            state = toggled_state(engine.current_flips, engine.edges[edge_id])
            if objective == 4:
                add_objective_four(state)
            elif objective == 5:
                add_objective_five(state)
            else:
                add_objective_six(2, state)

        for exit_position in boundary_positions(parity):
            exit_edge = position_edge(exit_position)
            engine.toggle(exit_edge)
            if engine.current_count != 3:
                raise AssertionError((parity, exit_position, engine.current_count))
            for edge_id, objective in enumerate(engine.all_resulting_counts()):
                if objective not in (4, 5, 6):
                    continue
                state = toggled_state(engine.current_flips, engine.edges[edge_id])
                if objective == 4:
                    add_objective_four(state)
                elif objective == 5:
                    add_objective_five(state)
                else:
                    add_objective_six(3, state)
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
        for edge_id, objective in enumerate(engine.all_resulting_counts()):
            if objective not in (4, 5, 6):
                continue
            state = toggled_state(representative, engine.edges[edge_id])
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
                add_objective_five(state)
            else:
                add_objective_six(4, state)

    if len(objective_four_orbits) != 78:
        raise AssertionError(len(objective_four_orbits))
    if len(objective_five_orbits) != 306:
        raise AssertionError(len(objective_five_orbits))

    known_sublevel_four_states = set(centers) | boundaries
    for representative in objective_four_orbits.values():
        known_sublevel_four_states.update(rotation_orbit(representative))
    if len(known_sublevel_four_states) != 4_171:
        raise AssertionError(len(known_sublevel_four_states))

    objective_five_states: set[FlipSet] = set()
    for representative in objective_five_orbits.values():
        orbit = rotation_orbit(representative)
        if len(orbit) != ORDER:
            raise AssertionError("objective-five state has rotational stabilizer")
        objective_five_states.update(orbit)
    if len(objective_five_states) != 13_158:
        raise AssertionError(len(objective_five_states))

    for orbit_index, canonical in enumerate(sorted(objective_five_orbits), start=1):
        representative = objective_five_orbits[canonical]
        engine.move_to(representative)
        if engine.current_count != 5:
            raise AssertionError((orbit_index, engine.current_count))
        for edge_id, objective in enumerate(engine.all_resulting_counts()):
            if objective > 6:
                continue
            state = toggled_state(representative, engine.edges[edge_id])
            if objective <= 4:
                if state not in known_sublevel_four_states:
                    raise AssertionError(
                        ("new objective-at-most-four state", orbit_index, objective)
                    )
            elif objective == 5:
                if state not in objective_five_states:
                    raise AssertionError(("new objective-five state", orbit_index))
            else:
                add_objective_six(5, state)

    source_representative_histogram = Counter(
        source for source, _ in objective_six_directed_representatives
    )
    if source_representative_histogram[5] * ORDER != 76_282:
        raise AssertionError(source_representative_histogram)

    objective_six_orbits: dict[tuple[Edge, ...], FlipSet] = {}
    for _, state in objective_six_directed_representatives:
        objective_six_orbits.setdefault(canonical_rotation(state), state)
    frontier_states: set[FlipSet] = set()
    for representative in objective_six_orbits.values():
        orbit = rotation_orbit(representative)
        if len(orbit) != ORDER:
            raise AssertionError("objective-six state has rotational stabilizer")
        frontier_states.update(orbit)
    if len(frontier_states) != ORDER * len(objective_six_orbits):
        raise AssertionError("objective-six rotation orbits overlap")

    source_incidence: dict[FlipSet, Counter[int]] = {
        state: Counter() for state in frontier_states
    }
    for source_objective, representative in objective_six_directed_representatives:
        for rotated in rotation_orbit(representative):
            source_incidence[rotated][source_objective] += 1
    incidence_signature_histogram = Counter(
        tuple(counts.get(source, 0) for source in (2, 3, 4, 5))
        for counts in source_incidence.values()
    )
    directed_count = sum(sum(counts.values()) for counts in source_incidence.values())
    if directed_count != ORDER * len(objective_six_directed_representatives):
        raise AssertionError(directed_count)

    direct_recount_count = 0
    if direct_verify_strata:
        representatives_by_signature: dict[tuple[int, ...], FlipSet] = {}
        for state, counts in source_incidence.items():
            signature = tuple(counts.get(source, 0) for source in (2, 3, 4, 5))
            representatives_by_signature.setdefault(signature, state)
        for signature, state in sorted(representatives_by_signature.items()):
            engine.move_to(state)
            if engine.current_count != 6:
                raise AssertionError((signature, engine.current_count))
            recounted, _ = direct_count(engine.colors, engine.edge_ids)
            if recounted != 6:
                raise AssertionError((signature, recounted))
            direct_recount_count += 1

    return {
        "certificate": certificate.name,
        "cycle_certificate": cycle_path.name,
        "escape_certificate": escape_path.name,
        "objective_four_certificate": objective_four_path.name,
        "objective_five_certificate": objective_five_path.name,
        "order": ORDER,
        "sublevel_five_source_rotation_type_count": 403,
        "sublevel_five_all_edge_rotation_representative_neighbor_checks": 403
        * len(engine.edges),
        "sublevel_five_symmetry_lifted_neighbor_checks": 17_329
        * len(engine.edges),
        "objective_six_directed_source_edge_histogram": {
            str(source): ORDER * count
            for source, count in sorted(source_representative_histogram.items())
        },
        "objective_six_directed_source_rotation_representative_histogram": {
            str(source): count
            for source, count in sorted(source_representative_histogram.items())
        },
        "objective_six_directed_sublevel_five_edge_count": directed_count,
        "objective_six_directed_rotation_representative_count": len(
            objective_six_directed_representatives
        ),
        "objective_six_frontier_rotation_orbit_count": len(objective_six_orbits),
        "objective_six_frontier_vertex_count": len(frontier_states),
        "objective_six_frontier_has_trivial_rotation_stabilizers": True,
        "objective_six_frontier_source_incidence_signature_histogram": {
            ",".join(map(str, signature)): count
            for signature, count in sorted(incidence_signature_histogram.items())
        },
        "direct_recount_objective_six_incidence_signature_count": (
            direct_recount_count
        ),
        "scope_note": (
            "Every objective-six edge from the complete certified sublevel-five "
            "component is enumerated using its 403 rotational source types, then "
            "deduplicated under all 43 rotations. One objective-six representative "
            "per lower-incidence signature is directly recounted when requested. "
            "The objective-six frontier's own neighbors are not scanned."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--cycle", type=Path, required=True)
    parser.add_argument("--escape", type=Path, required=True)
    parser.add_argument("--objective-four", type=Path, required=True)
    parser.add_argument("--objective-five", type=Path, required=True)
    parser.add_argument("--direct-verify-strata", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(
        args.certificate,
        args.cycle,
        args.escape,
        args.objective_four,
        args.objective_five,
        direct_verify_strata=args.direct_verify_strata,
    )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
