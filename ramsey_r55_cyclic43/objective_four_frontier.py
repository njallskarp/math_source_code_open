#!/usr/bin/env python3
"""Probe the first objective-four frontier outside the Cyclic(43) basin."""

from __future__ import annotations

import argparse
import itertools
import json
from array import array
from collections import Counter
from pathlib import Path

from defect_cycle import position_edge
from escape_component import boundary_positions
from local_rigidity import (
    complete_graph_edges,
    direct_count,
    initial_colors,
    is_monochromatic,
)
from solve_cyclic43 import ORDER, edge, load_certificate


Edge = tuple[int, int]
FlipSet = frozenset[Edge]


def toggle_member(items: set[Edge], item: Edge) -> None:
    if item in items:
        items.remove(item)
    else:
        items.add(item)


def rotate_edge(changed_edge: Edge, offset: int) -> Edge:
    return edge(
        (changed_edge[0] + offset) % ORDER,
        (changed_edge[1] + offset) % ORDER,
    )


def rotate_flips(flips: FlipSet, offset: int) -> FlipSet:
    return frozenset(rotate_edge(changed_edge, offset) for changed_edge in flips)


def rotation_orbit(flips: FlipSet) -> set[FlipSet]:
    return {rotate_flips(flips, offset) for offset in range(ORDER)}


def canonical_rotation(flips: FlipSet) -> tuple[Edge, ...]:
    return min(tuple(sorted(rotated)) for rotated in rotation_orbit(flips))


def cycle_and_boundary_states(
    primary: FlipSet, transport_positions: list[int]
) -> tuple[list[FlipSet], set[FlipSet]]:
    active = set(primary)
    centers = []
    boundaries = set()
    for state_index, transport_position in enumerate(transport_positions):
        center = frozenset(active)
        centers.append(center)
        for exit_position in boundary_positions(state_index):
            boundary = set(center)
            toggle_member(boundary, position_edge(exit_position))
            boundaries.add(frozenset(boundary))
        toggle_member(active, position_edge(transport_position))
    if frozenset(active) != primary:
        raise AssertionError("transport does not close")
    if len(set(centers)) != 86 or len(boundaries) != 731:
        raise AssertionError((len(set(centers)), len(boundaries)))
    return centers, boundaries


class CliqueEngine:
    def __init__(self, primary: FlipSet) -> None:
        self.colors, self.edges = initial_colors(set(primary))
        self.edge_ids, _ = complete_graph_edges()
        self.incident = [array("I") for _ in self.edges]
        self.red_counts = array("b")
        for vertices in itertools.combinations(range(ORDER), 5):
            five_id = len(self.red_counts)
            ids = [
                self.edge_ids[edge(a, b)]
                for a, b in itertools.combinations(vertices, 2)
            ]
            self.red_counts.append(sum(self.colors[edge_id] for edge_id in ids))
            for edge_id in ids:
                self.incident[edge_id].append(five_id)
        self.current_count = sum(
            is_monochromatic(count) for count in self.red_counts
        )
        self.current_flips = set(primary)
        if self.current_count != 2:
            raise AssertionError(self.current_count)

    def resulting_count(self, edge_id: int) -> int:
        delta = -1 if self.colors[edge_id] else 1
        result = self.current_count
        for five_id in self.incident[edge_id]:
            count = self.red_counts[five_id]
            result += is_monochromatic(count + delta) - is_monochromatic(count)
        return result

    def all_resulting_counts(self) -> list[int]:
        return [self.resulting_count(edge_id) for edge_id in range(len(self.edges))]

    def toggle(self, changed_edge: Edge) -> None:
        edge_id = self.edge_ids[changed_edge]
        delta = -1 if self.colors[edge_id] else 1
        for five_id in self.incident[edge_id]:
            count = self.red_counts[five_id]
            self.current_count += (
                is_monochromatic(count + delta) - is_monochromatic(count)
            )
            self.red_counts[five_id] += delta
        self.colors[edge_id] = not self.colors[edge_id]
        toggle_member(self.current_flips, changed_edge)

    def move_to(self, target: FlipSet) -> None:
        for changed_edge in sorted(self.current_flips.symmetric_difference(target)):
            self.toggle(changed_edge)
        if frozenset(self.current_flips) != target:
            raise AssertionError("failed to reach target")


def analyze(
    certificate: Path,
    cycle_path: Path,
    escape_path: Path,
    scan_frontier: bool = False,
    direct_verify: bool = False,
) -> dict[str, object]:
    primary = frozenset(load_certificate(certificate))
    cycle = json.loads(cycle_path.read_text())
    escape = json.loads(escape_path.read_text())
    if not escape.get("full_sublevel_three_component_through_C86_is_closed"):
        raise ValueError("escape certificate does not prove sublevel-three closure")
    centers, boundaries = cycle_and_boundary_states(primary, cycle["edge_positions"])
    center_set = set(centers)

    engine = CliqueEngine(primary)
    orbit_records: dict[tuple[Edge, ...], dict[str, object]] = {}
    low_directed_representatives: list[FlipSet] = []

    def add_seed(frontier_state: FlipSet, source: tuple[object, ...]) -> None:
        canonical = canonical_rotation(frontier_state)
        record = orbit_records.setdefault(
            canonical,
            {
                "representative": frontier_state,
                "low_directed_representatives": [],
            },
        )
        record["low_directed_representatives"].append(source)
        low_directed_representatives.append(frontier_state)

    for parity in range(2):
        engine.move_to(centers[parity])
        if engine.current_count != 2:
            raise AssertionError((parity, engine.current_count))
        center_resulting_counts = engine.all_resulting_counts()
        center_objective_four_ids = [
            edge_id
            for edge_id, count in enumerate(center_resulting_counts)
            if count == 4
        ]
        for edge_id in center_objective_four_ids:
            changed_edge = engine.edges[edge_id]
            frontier = set(engine.current_flips)
            toggle_member(frontier, changed_edge)
            add_seed(frozenset(frontier), ("center", parity, changed_edge))
        for exit_position in boundary_positions(parity):
            exit_edge = position_edge(exit_position)
            engine.toggle(exit_edge)
            if engine.current_count != 3:
                raise AssertionError((parity, exit_position, engine.current_count))
            resulting_counts = engine.all_resulting_counts()
            objective_four_ids = [
                edge_id
                for edge_id, count in enumerate(resulting_counts)
                if count == 4
            ]
            for edge_id in objective_four_ids:
                changed_edge = engine.edges[edge_id]
                frontier = set(engine.current_flips)
                toggle_member(frontier, changed_edge)
                add_seed(
                    frozenset(frontier),
                    ("boundary", parity, exit_position, changed_edge),
                )
            engine.toggle(exit_edge)
            if engine.current_count != 2:
                raise AssertionError(engine.current_count)

    if len(low_directed_representatives) != 138:
        raise AssertionError(len(low_directed_representatives))
    first_frontier_states = set()
    for record in orbit_records.values():
        orbit = rotation_orbit(record["representative"])
        if len(orbit) != ORDER:
            raise AssertionError("objective-four state has rotational stabilizer")
        first_frontier_states.update(orbit)
    if len(first_frontier_states) != ORDER * len(orbit_records):
        raise AssertionError("frontier rotation orbits overlap")

    low_incidence: Counter[FlipSet] = Counter()
    for representative in low_directed_representatives:
        for rotated in rotation_orbit(representative):
            low_incidence[rotated] += 1
    if set(low_incidence) != first_frontier_states:
        raise AssertionError("incidence frontier differs from orbit frontier")
    if sum(low_incidence.values()) != 5_934:
        raise AssertionError(sum(low_incidence.values()))

    result: dict[str, object] = {
        "certificate": certificate.name,
        "cycle_certificate": cycle_path.name,
        "escape_certificate": escape_path.name,
        "order": ORDER,
        "boundary_vertex_count": len(boundaries),
        "objective_four_directed_center_edge_count": 946,
        "objective_four_directed_boundary_edge_count": 4_988,
        "objective_four_directed_low_component_edge_count": 5_934,
        "objective_four_directed_low_component_rotation_representative_count": 138,
        "first_objective_four_frontier_rotation_orbit_count": len(orbit_records),
        "first_objective_four_frontier_vertex_count": len(first_frontier_states),
        "first_objective_four_frontier_low_incidence_histogram": {
            str(incidence): count
            for incidence, count in sorted(Counter(low_incidence.values()).items())
        },
        "first_objective_four_frontier_has_trivial_rotation_stabilizers": True,
    }
    if not scan_frontier:
        result["scope_note"] = (
            "The first objective-four frontier from every objective-two and "
            "objective-three vertex is enumerated, deduplicated, and quotiented "
            "by rotation. Its objective-four closure was not requested."
        )
        return result

    aggregate_neighbor_histogram: Counter[int] = Counter()
    new_low_directed: Counter[int] = Counter()
    new_low_orbits: dict[int, set[tuple[Edge, ...]]] = {
        objective: set() for objective in range(4)
    }
    objective_four_degree_histogram: Counter[int] = Counter()
    objective_four_neighbor_signature_histogram: Counter[
        tuple[tuple[int, int], ...]
    ] = Counter()
    direct_recount_count = 0
    initial_orbit_count = len(orbit_records)
    orbit_queue = sorted(orbit_records)
    orbit_index = 0
    while orbit_index < len(orbit_queue):
        canonical = orbit_queue[orbit_index]
        record = orbit_records[canonical]
        orbit_index += 1
        representative = record["representative"]
        engine.move_to(representative)
        if engine.current_count != 4:
            raise AssertionError((orbit_index, engine.current_count))
        if direct_verify:
            recounted, witnesses = direct_count(engine.colors, engine.edge_ids)
            if recounted != 4:
                raise AssertionError((orbit_index, recounted))
            direct_recount_count += 1
        else:
            witnesses = []
        resulting_counts = engine.all_resulting_counts()
        histogram = Counter(resulting_counts)
        objective_four_neighbor_signature_histogram[
            tuple(sorted(histogram.items()))
        ] += ORDER
        aggregate_neighbor_histogram.update(
            {objective: ORDER * count for objective, count in histogram.items()}
        )
        sublevel_four_degree = sum(
            count for objective, count in histogram.items() if objective <= 4
        )
        objective_four_degree_histogram[sublevel_four_degree] += ORDER
        for edge_id, objective in enumerate(resulting_counts):
            if objective > 4:
                continue
            neighbor = set(representative)
            toggle_member(neighbor, engine.edges[edge_id])
            neighbor_state = frozenset(neighbor)
            known_low = (
                neighbor_state in center_set
                if objective == 2
                else neighbor_state in boundaries
                if objective == 3
                else False
            )
            if objective < 4 and known_low:
                continue
            if objective < 4:
                new_low_directed[objective] += ORDER
                new_low_orbits[objective].add(canonical_rotation(neighbor_state))
            else:
                neighbor_canonical = canonical_rotation(neighbor_state)
                if neighbor_canonical not in orbit_records:
                    neighbor_orbit = rotation_orbit(neighbor_state)
                    if len(neighbor_orbit) != ORDER:
                        raise AssertionError(
                            "objective-four state has rotational stabilizer"
                        )
                    orbit_records[neighbor_canonical] = {
                        "representative": neighbor_state,
                        "low_directed_representatives": [],
                    }
                    orbit_queue.append(neighbor_canonical)

    objective_four_vertex_count = ORDER * len(orbit_records)
    if new_low_directed:
        component_closed = False
    else:
        component_closed = True
    objective_four_induced_edge_count = aggregate_neighbor_histogram[4] // 2
    if aggregate_neighbor_histogram[2] != 946:
        raise AssertionError(aggregate_neighbor_histogram[2])
    if aggregate_neighbor_histogram[3] != 4_988:
        raise AssertionError(aggregate_neighbor_histogram[3])
    if sum(
        degree * count for degree, count in objective_four_degree_histogram.items()
    ) != 5_934 + 2 * objective_four_induced_edge_count:
        raise AssertionError(objective_four_degree_histogram)
    sublevel_four_vertex_count = 817 + objective_four_vertex_count
    sublevel_four_edge_count = (
        1_505
        + aggregate_neighbor_histogram[2]
        + aggregate_neighbor_histogram[3]
        + objective_four_induced_edge_count
    )

    result.update(
        {
            "objective_four_component_rotation_orbit_count": len(orbit_records),
            "objective_four_component_vertex_count": objective_four_vertex_count,
            "additional_objective_four_rotation_orbit_count": (
                len(orbit_records) - initial_orbit_count
            ),
            "objective_four_all_edge_rotation_representative_neighbor_checks": (
                len(orbit_records) * len(engine.edges)
            ),
            "objective_four_symmetry_lifted_neighbor_checks": (
                objective_four_vertex_count * len(engine.edges)
            ),
            "aggregate_objective_four_neighbor_objective_histogram": {
                str(objective): count
                for objective, count in sorted(aggregate_neighbor_histogram.items())
            },
            "new_objective_at_most_three_directed_neighbor_histogram": {
                str(objective): count
                for objective, count in sorted(new_low_directed.items())
            },
            "new_objective_at_most_three_rotation_orbit_histogram": {
                str(objective): len(orbits)
                for objective, orbits in new_low_orbits.items()
            },
            "objective_four_vertex_sublevel_four_degree_histogram": {
                str(degree): count
                for degree, count in sorted(objective_four_degree_histogram.items())
            },
            "objective_four_induced_edge_count": objective_four_induced_edge_count,
            "objective_four_neighbor_spectrum_count": len(
                objective_four_neighbor_signature_histogram
            ),
            "complete_sublevel_four_component_is_closed": component_closed,
            "complete_sublevel_four_component_vertex_count": (
                sublevel_four_vertex_count if component_closed else None
            ),
            "complete_sublevel_four_component_edge_count": (
                sublevel_four_edge_count if component_closed else None
            ),
            "direct_recount_objective_four_representative_count": (
                direct_recount_count
            ),
            "scope_note": (
                "Breadth-first orbit expansion scans all edge reversals at every "
                "objective-four orbit reached from the certified sublevel-three "
                "component. Closure is a complete sublevel-four theorem only when "
                "no new objective-at-most-three neighbor is found."
            ),
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--cycle", type=Path, required=True)
    parser.add_argument("--escape", type=Path, required=True)
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
        scan_frontier=args.scan_frontier,
        direct_verify=args.direct_verify,
    )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
