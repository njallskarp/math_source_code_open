#!/usr/bin/env python3
"""Third-language verification of the Cyclic(43) threshold-twelve closure."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import time
from typing import Iterable

import numpy as np


ORDER = 43
EDGE_COUNT = ORDER * (ORDER - 1) // 2
WORD_COUNT = (EDGE_COUNT + 63) // 64
FIVE_SET_COUNT = 962_598
EXPECTED_FRONTIER_COUNT = 1_041_887
SEED_DISTANCES = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def state_key(edges: Iterable[int]) -> tuple[int, ...]:
    words = [0] * WORD_COUNT
    for edge in edges:
        words[int(edge) // 64] |= 1 << (int(edge) % 64)
    return tuple(words)


class Model:
    def __init__(self) -> None:
        self.edge_id = np.full((ORDER, ORDER), -1, dtype=np.int16)
        edge_vertices: list[tuple[int, int]] = []
        seed_red = np.zeros(EDGE_COUNT, dtype=np.bool_)
        next_edge = 0
        for left in range(ORDER):
            for right in range(left + 1, ORDER):
                self.edge_id[left, right] = next_edge
                self.edge_id[right, left] = next_edge
                edge_vertices.append((left, right))
                distance = min(right - left, ORDER - (right - left))
                seed_red[next_edge] = distance in SEED_DISTANCES
                next_edge += 1
        if next_edge != EDGE_COUNT:
            raise AssertionError("edge count mismatch")
        self.seed_red = seed_red

        self.rotation = np.empty((ORDER, EDGE_COUNT), dtype=np.uint16)
        for offset in range(ORDER):
            for edge, (left, right) in enumerate(edge_vertices):
                moved_left = (left + offset) % ORDER
                moved_right = (right + offset) % ORDER
                self.rotation[offset, edge] = self.edge_id[
                    moved_left, moved_right
                ]

        self.five_edges = np.empty((FIVE_SET_COUNT, 10), dtype=np.uint16)
        row = 0
        for vertices in combinations(range(ORDER), 5):
            position = 0
            for left_index in range(5):
                for right_index in range(left_index + 1, 5):
                    self.five_edges[row, position] = self.edge_id[
                        vertices[left_index], vertices[right_index]
                    ]
                    position += 1
            row += 1
        if row != FIVE_SET_COUNT:
            raise AssertionError("five-set count mismatch")

    def canonical_key(self, edges: Iterable[int]) -> tuple[int, ...]:
        edge_array = np.fromiter(edges, dtype=np.uint16)
        best: tuple[int, ...] | None = None
        for offset in range(ORDER):
            candidate = state_key(self.rotation[offset, edge_array])
            if best is None or candidate < best:
                best = candidate
        if best is None:
            return (0,) * WORD_COUNT
        return best

    def rotate_one_key(self, edges: Iterable[int]) -> tuple[int, ...]:
        edge_array = np.fromiter(edges, dtype=np.uint16)
        return state_key(self.rotation[1, edge_array])

    def analyze(self, state_edges: list[int]) -> tuple[int, np.ndarray]:
        toggled = np.zeros(EDGE_COUNT, dtype=np.bool_)
        toggled[state_edges] = True
        red = self.seed_red != toggled
        colors = red[self.five_edges]
        red_counts = np.count_nonzero(colors, axis=1)

        all_blue = np.flatnonzero(red_counts == 0)
        all_red = np.flatnonzero(red_counts == 10)
        objective = int(all_blue.size + all_red.size)
        delta = np.zeros(EDGE_COUNT, dtype=np.int32)

        monochromatic = np.concatenate((all_blue, all_red))
        if monochromatic.size:
            delta -= np.bincount(
                self.five_edges[monochromatic].reshape(-1),
                minlength=EDGE_COUNT,
            ).astype(np.int32)

        almost_blue = np.flatnonzero(red_counts == 1)
        if almost_blue.size:
            almost_blue_colors = colors[almost_blue]
            minority_positions = np.argmax(almost_blue_colors, axis=1)
            minority_edges = self.five_edges[
                almost_blue, minority_positions
            ]
            delta += np.bincount(
                minority_edges, minlength=EDGE_COUNT
            ).astype(np.int32)

        almost_red = np.flatnonzero(red_counts == 9)
        if almost_red.size:
            almost_red_colors = colors[almost_red]
            minority_positions = np.argmin(almost_red_colors, axis=1)
            minority_edges = self.five_edges[almost_red, minority_positions]
            delta += np.bincount(
                minority_edges, minlength=EDGE_COUNT
            ).astype(np.int32)

        return objective, delta


def toggled_edges(state: list[int], edge: int) -> list[int]:
    neighbor = set(state)
    if edge in neighbor:
        neighbor.remove(edge)
    else:
        neighbor.add(edge)
    return sorted(neighbor)


def scan_frontier(
    path: Path, wanted: set[tuple[int, ...]]
) -> tuple[int, set[tuple[int, ...]], bool]:
    """Stream inner integer arrays from the large single-array JSON file."""
    payload = path.read_bytes()
    key_position = payload.find(b'"objective_twelve_rotation_representatives"')
    if key_position < 0:
        raise ValueError("missing objective-twelve representative array")
    array_position = payload.find(b"[", key_position)
    if array_position < 0:
        raise ValueError("malformed objective-twelve representative array")

    found: set[tuple[int, ...]] = set()
    previous: tuple[int, ...] | None = None
    strictly_sorted = True
    count = 0
    pattern = re.compile(rb"\[([0-9,]*)\]")
    for match in pattern.finditer(payload, array_position + 1):
        raw = match.group(1)
        edges = [] if not raw else [int(value) for value in raw.split(b",")]
        key = state_key(edges)
        if previous is not None and not previous < key:
            strictly_sorted = False
        previous = key
        if key in wanted:
            found.add(key)
        count += 1
        if count == EXPECTED_FRONTIER_COUNT:
            break
    return count, found, strictly_sorted


def histogram(counter: Counter[int]) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frontier_targets", type=Path)
    parser.add_argument("frontier_certificate", type=Path)
    parser.add_argument("first_expansion", type=Path)
    parser.add_argument("component", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    started = time.perf_counter()
    frontier_certificate = json.loads(args.frontier_certificate.read_text())
    first_expansion = json.loads(args.first_expansion.read_text())
    component = json.loads(args.component.read_text())
    additions: list[list[int]] = component[
        "complete_additional_objective_12_rotation_representatives"
    ]
    seeds: list[list[int]] = first_expansion[
        "new_objective_12_rotation_representatives"
    ]
    if len(additions) != 238 or len(seeds) != 229:
        raise ValueError("closure representative count mismatch")

    frontier_hash = sha256(args.frontier_targets)
    expected_frontier_hash = frontier_certificate[
        "temporary_full_target_file_sha256"
    ]
    if frontier_hash != expected_frontier_hash:
        raise ValueError("objective-twelve frontier hash mismatch")

    model = Model()
    addition_keys = {state_key(state) for state in additions}
    seed_keys = {state_key(state) for state in seeds}
    if len(addition_keys) != 238 or len(seed_keys) != 229:
        raise ValueError("duplicate closure representatives")
    if not seed_keys <= addition_keys:
        raise ValueError("first-expansion seeds are not contained in closure")

    canonical_errors = 0
    nonfree_errors = 0
    objective_errors = 0
    lower_neighbor_count = 0
    neighbor_objectives: Counter[int] = Counter()
    minimum_neighbors: Counter[int] = Counter()
    external_minimums: Counter[int] = Counter()
    q13_exit_degrees: Counter[int] = Counter()
    q13_degree_by_source: dict[tuple[int, ...], int] = {}
    q12_moves: list[tuple[tuple[int, ...], tuple[int, ...]]] = []

    for source_index, source in enumerate(additions):
        source_key = state_key(source)
        if model.canonical_key(source) != source_key:
            canonical_errors += 1
        if model.rotate_one_key(source) == source_key:
            nonfree_errors += 1

        objective, delta = model.analyze(source)
        if objective != 12:
            objective_errors += 1
        objectives = objective + delta
        minimum_neighbors[int(objectives.min())] += 1
        for value, count in zip(*np.unique(objectives, return_counts=True)):
            neighbor_objectives[int(value)] += int(count)
        external = objectives[objectives > 12]
        if external.size:
            external_minimums[int(external.min())] += 1
        q13_degree = int(np.count_nonzero(objectives == 13))
        q13_exit_degrees[q13_degree] += 1
        q13_degree_by_source[source_key] = q13_degree

        for edge in np.flatnonzero(objectives <= 12):
            neighbor_objective = int(objectives[edge])
            if neighbor_objective < 12:
                lower_neighbor_count += 1
                continue
            neighbor = toggled_edges(source, int(edge))
            target_key = model.canonical_key(neighbor)
            q12_moves.append((source_key, target_key))

        if (source_index + 1) % 25 == 0:
            elapsed = time.perf_counter() - started
            print(
                f"NumPy closure verification: {source_index + 1}/238 "
                f"sources in {elapsed:.1f}s",
                flush=True,
            )

    frontier_candidates = {
        target for _, target in q12_moves if target not in addition_keys
    }
    frontier_count, found_frontier, frontier_strictly_sorted = scan_frontier(
        args.frontier_targets, frontier_candidates
    )
    missing_frontier_targets = frontier_candidates - found_frontier

    addition_adjacency: dict[
        tuple[int, ...], set[tuple[int, ...]]
    ] = defaultdict(set)
    to_addition = 0
    to_frontier = 0
    omitted_sublevel = 0
    source_frontier_degrees: Counter[tuple[int, ...]] = Counter()
    source_addition_degrees: Counter[tuple[int, ...]] = Counter()
    frontier_target_degrees: Counter[tuple[int, ...]] = Counter()
    addition_pair_multiplicity: Counter[
        tuple[tuple[int, ...], tuple[int, ...]]
    ] = Counter()
    for source, target in q12_moves:
        if target in addition_keys:
            to_addition += 1
            addition_adjacency[source].add(target)
            source_addition_degrees[source] += 1
            addition_pair_multiplicity[source, target] += 1
        elif target in found_frontier:
            to_frontier += 1
            source_frontier_degrees[source] += 1
            frontier_target_degrees[target] += 1
        else:
            omitted_sublevel += 1

    undirected_pair_directed_multiplicity: Counter[
        tuple[tuple[int, ...], tuple[int, ...]]
    ] = Counter()
    for (source, target), multiplicity in addition_pair_multiplicity.items():
        pair = (source, target) if source <= target else (target, source)
        undirected_pair_directed_multiplicity[pair] += multiplicity
    self_orbit_directed_moves = sum(
        multiplicity
        for (source, target), multiplicity in (
            undirected_pair_directed_multiplicity.items()
        )
        if source == target
    )
    asymmetric_pair_errors = sum(
        1
        for source, target in undirected_pair_directed_multiplicity
        if source != target
        and addition_pair_multiplicity[source, target]
        != addition_pair_multiplicity[target, source]
    )
    undirected_pair_multiplicity = {
        pair: (multiplicity if pair[0] == pair[1] else multiplicity // 2)
        for pair, multiplicity in undirected_pair_directed_multiplicity.items()
    }
    undirected_edges_with_multiplicity = sum(
        undirected_pair_multiplicity.values()
    )

    undirected_adjacency: dict[
        tuple[int, ...], set[tuple[int, ...]]
    ] = {vertex: set() for vertex in addition_keys}
    for source, target in undirected_pair_multiplicity:
        if source != target:
            undirected_adjacency[source].add(target)
            undirected_adjacency[target].add(source)

    component_profiles = []
    unvisited = set(addition_keys)
    while unvisited:
        start = next(iter(unvisited))
        vertices = {start}
        component_queue = [start]
        unvisited.remove(start)
        while component_queue:
            source = component_queue.pop()
            for target in undirected_adjacency[source]:
                if target in unvisited:
                    unvisited.remove(target)
                    vertices.add(target)
                    component_queue.append(target)
        edges = sum(
            multiplicity
            for (source, target), multiplicity in (
                undirected_pair_multiplicity.items()
            )
            if source in vertices and target in vertices
        )
        component_profiles.append(
            {
                "vertices": len(vertices),
                "edges": edges,
                "cycle_rank": edges - len(vertices) + 1,
                "seed_vertices": len(vertices & seed_keys),
                "final_shell_vertices": len(vertices - seed_keys),
            }
        )
    component_profiles.sort(
        key=lambda profile: (
            profile["vertices"],
            profile["edges"],
            profile["final_shell_vertices"],
            profile["seed_vertices"],
        ),
        reverse=True,
    )
    addition_total_cycle_rank = sum(
        profile["cycle_rank"] for profile in component_profiles
    )
    final_shell_keys = addition_keys - seed_keys
    zero_frontier_keys = {
        source
        for source in addition_keys
        if source_frontier_degrees.get(source, 0) == 0
    }
    final_shell_equals_zero_frontier = final_shell_keys == zero_frontier_keys

    reached = set(seed_keys)
    queue = deque(seed_keys)
    while queue:
        source = queue.popleft()
        for target in addition_adjacency[source]:
            if target not in reached:
                reached.add(target)
                queue.append(target)

    expected_above_twelve = len(additions) * EDGE_COUNT - len(q12_moves)
    all_checks = (
        frontier_count == EXPECTED_FRONTIER_COUNT
        and frontier_strictly_sorted
        and not missing_frontier_targets
        and len(reached) == 238
        and len(reached - seed_keys) == 9
        and final_shell_equals_zero_frontier
        and canonical_errors == 0
        and nonfree_errors == 0
        and objective_errors == 0
        and lower_neighbor_count == 0
        and omitted_sublevel == 0
        and to_frontier
        == component["added_to_first_frontier_quotient_incidence"]
        and to_addition
        == component["directed_inside_addition_quotient_incidence"]
        and undirected_edges_with_multiplicity
        == component["undirected_inside_addition_quotient_edges"]
        and asymmetric_pair_errors == 0
        and expected_above_twelve
        == component["directed_outside_above_twelve_from_addition"]
        and histogram(minimum_neighbors)
        == component["added_source_minimum_neighbor_objective_histogram"]
        and histogram(external_minimums)
        == component["added_source_external_minimum_objective_histogram"]
    )

    output = {
        "order": ORDER,
        "edge_count": EDGE_COUNT,
        "five_set_count": FIVE_SET_COUNT,
        "verified_addition_source_count": len(additions),
        "verified_seed_count": len(seeds),
        "newly_reached_after_seeds": len(reached - seed_keys),
        "reachable_addition_count": len(reached),
        "frontier_target_count_streamed": frontier_count,
        "frontier_strictly_sorted_and_unique": frontier_strictly_sorted,
        "frontier_candidate_target_count": len(frontier_candidates),
        "missing_frontier_target_count": len(missing_frontier_targets),
        "directed_to_first_frontier": to_frontier,
        "directed_inside_addition": to_addition,
        "distinct_directed_pairs_inside_addition": len(
            addition_pair_multiplicity
        ),
        "undirected_edges_inside_addition_with_multiplicity": (
            undirected_edges_with_multiplicity
        ),
        "distinct_undirected_pairs_inside_addition": len(
            undirected_pair_multiplicity
        ),
        "undirected_parallel_edge_excess_inside_addition": (
            undirected_edges_with_multiplicity
            - len(undirected_pair_multiplicity)
        ),
        "self_orbit_directed_moves_inside_addition": (
            self_orbit_directed_moves
        ),
        "asymmetric_inside_pair_errors": asymmetric_pair_errors,
        "addition_component_count": len(component_profiles),
        "addition_total_cycle_rank": addition_total_cycle_rank,
        "components_meeting_final_shell": sum(
            profile["final_shell_vertices"] > 0
            for profile in component_profiles
        ),
        "addition_component_profiles": component_profiles,
        "final_shell_equals_zero_frontier_sources": (
            final_shell_equals_zero_frontier
        ),
        "final_shell_addition_degree_histogram": histogram(
            Counter(
                source_addition_degrees.get(source, 0)
                for source in final_shell_keys
            )
        ),
        "final_shell_q13_exit_degree_histogram": histogram(
            Counter(q13_degree_by_source[source] for source in final_shell_keys)
        ),
        "source_frontier_degree_histogram": histogram(
            Counter(
                source_frontier_degrees.get(source, 0)
                for source in addition_keys
            )
        ),
        "source_addition_degree_histogram": histogram(
            Counter(
                source_addition_degrees.get(source, 0)
                for source in addition_keys
            )
        ),
        "frontier_target_degree_histogram": histogram(
            Counter(frontier_target_degrees.values())
        ),
        "directed_above_twelve": expected_above_twelve,
        "q13_exit_degree_histogram": histogram(q13_exit_degrees),
        "directed_neighbor_objective_histogram": histogram(
            neighbor_objectives
        ),
        "minimum_neighbor_objective_histogram": histogram(minimum_neighbors),
        "external_minimum_objective_histogram": histogram(external_minimums),
        "canonical_errors": canonical_errors,
        "nonfree_errors": nonfree_errors,
        "objective_errors": objective_errors,
        "lower_neighbor_count": lower_neighbor_count,
        "omitted_sublevel_neighbor_count": omitted_sublevel,
        "frontier_targets_sha256": frontier_hash,
        "frontier_certificate_sha256": sha256(args.frontier_certificate),
        "first_expansion_sha256": sha256(args.first_expansion),
        "component_sha256": sha256(args.component),
        "all_numpy_closure_checks_pass": all_checks,
        "method": (
            "independent Python/NumPy enumeration of all K5 edge sets, "
            "vectorized exact monochromatic-count deltas, separately built "
            "C43 rotation maps and canonical words, streamed frontier "
            "membership, and reachability from the 229 certified seeds"
        ),
        "scope_note": (
            "This independently checks every move from the persisted 238 "
            "closure representatives and proves their reachability from the "
            "229 seeds; it relies on the hash-pinned complete frontier array "
            "and the persisted representative lists."
        ),
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    if not all_checks:
        raise SystemExit("NumPy closure checks failed")


if __name__ == "__main__":
    main()
