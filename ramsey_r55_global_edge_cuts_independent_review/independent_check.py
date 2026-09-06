#!/usr/bin/env python3
"""Clean-room audit of the strict-gap cut argument used in the R(5,5) lemma.

No certificate or source file from the reviewed contribution is read.  The
script derives the numerical bounds from the stated hypotheses and exhausts
all labelled graphs through order six to test the abstract minimizer lemmas
and the necessity of their strict inequalities.
"""

from __future__ import annotations

import hashlib
import itertools
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def balanced_turan_4_edges(order: int) -> int:
    quotient, remainder = divmod(order, 4)
    parts = [quotient + (i < remainder) for i in range(4)]
    return sum(parts[i] * parts[j] for i in range(4) for j in range(i + 1, 4))


def graph_data(order: int, graph_mask: int):
    pairs = list(itertools.combinations(range(order), 2))
    edges = [pair for index, pair in enumerate(pairs) if graph_mask >> index & 1]
    adjacency = [0] * order
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return pairs, edges, adjacency


def connected(adjacency: list[int], vertex_mask: int | None = None) -> bool:
    order = len(adjacency)
    if vertex_mask is None:
        vertex_mask = (1 << order) - 1
    if not vertex_mask:
        return True
    reached = 0
    frontier = vertex_mask & -vertex_mask
    while frontier:
        reached |= frontier
        neighbours = 0
        scan = frontier
        while scan:
            bit = scan & -scan
            scan ^= bit
            neighbours |= adjacency[bit.bit_length() - 1]
        frontier = neighbours & vertex_mask & ~reached
    return reached == vertex_mask


def cut_mask(pairs: list[tuple[int, int]], side: int) -> int:
    result = 0
    for index, (u, v) in enumerate(pairs):
        if ((side >> u) ^ (side >> v)) & 1:
            result |= 1 << index
    return result


def partition_cut_sets(
    pairs: list[tuple[int, int]],
    adjacency: list[int],
    graph_mask: int,
    restricted: bool,
) -> set[int]:
    order = len(adjacency)
    full = (1 << order) - 1
    candidates: set[int] = set()
    # Requiring vertex 0 on one side selects one representative per bipartition.
    for side in range(1, full):
        if not side & 1:
            continue
        other = full ^ side
        if restricted:
            if any(not (adjacency[v] & side) for v in range(order) if side >> v & 1):
                continue
            if any(not (adjacency[v] & other) for v in range(order) if other >> v & 1):
                continue
        candidates.add(cut_mask(pairs, side) & graph_mask)
    return candidates


def boundary_floor(
    pairs: list[tuple[int, int]], graph_mask: int, order: int, minimum_side: int
) -> int | None:
    full = (1 << order) - 1
    values = []
    for side in range(1, full):
        if not side & 1:
            continue
        other = full ^ side
        if side.bit_count() >= minimum_side and other.bit_count() >= minimum_side:
            values.append((cut_mask(pairs, side) & graph_mask).bit_count())
    return min(values, default=None)


def edge_boundary_sets(
    pairs: list[tuple[int, int]], edges: list[tuple[int, int]], graph_mask: int
) -> set[int]:
    return {cut_mask(pairs, (1 << u) | (1 << v)) & graph_mask for u, v in edges}


def component_count_after_cut(
    order: int, pairs: list[tuple[int, int]], graph_mask: int, deleted: int
) -> int:
    adjacency = [0] * order
    for index, (u, v) in enumerate(pairs):
        if graph_mask >> index & 1 and not (deleted >> index & 1):
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    unseen = (1 << order) - 1
    count = 0
    while unseen:
        seed = unseen & -unseen
        reached = 0
        frontier = seed
        while frontier:
            reached |= frontier
            neighbours = 0
            scan = frontier
            while scan:
                bit = scan & -scan
                scan ^= bit
                neighbours |= adjacency[bit.bit_length() - 1]
            frontier = neighbours & ~reached
        unseen &= ~reached
        count += 1
    return count


def has_k5(order: int, adjacency: list[int]) -> bool:
    for vertices in itertools.combinations(range(order), 5):
        if all(adjacency[u] >> v & 1 for u, v in itertools.combinations(vertices, 2)):
            return True
    return False


def inspect_graph(order: int, graph_mask: int, counters: dict[str, int]) -> None:
    pairs, edges, adjacency = graph_data(order, graph_mask)
    if not has_k5(order, adjacency):
        counters[f"turan_max_{order}"] = max(
            counters.get(f"turan_max_{order}", 0), len(edges)
        )

    if not connected(adjacency):
        return
    counters["connected_graphs"] += 1
    degrees = [row.bit_count() for row in adjacency]
    delta = min(degrees)

    ordinary = partition_cut_sets(pairs, adjacency, graph_mask, restricted=False)
    ordinary_value = min(value.bit_count() for value in ordinary)
    ordinary_minima = {value for value in ordinary if value.bit_count() == ordinary_value}
    l2 = boundary_floor(pairs, graph_mask, order, 2)
    if l2 is not None and delta < l2:
        expected = {
            cut_mask(pairs, 1 << vertex) & graph_mask
            for vertex, degree in enumerate(degrees)
            if degree == delta
        }
        require(ordinary_minima == expected, "ordinary strict-gap classification failed")
        counters["ordinary_strict_gap_cases"] += 1

    if order < 6 or delta < 3 or not edges:
        return
    l3 = boundary_floor(pairs, graph_mask, order, 3)
    edge_boundaries = edge_boundary_sets(pairs, edges, graph_mask)
    edge_value = min(value.bit_count() for value in edge_boundaries)
    restricted = partition_cut_sets(pairs, adjacency, graph_mask, restricted=True)
    if l3 is not None and edge_value < l3:
        restricted_value = min(value.bit_count() for value in restricted)
        restricted_minima = {
            value for value in restricted if value.bit_count() == restricted_value
        }
        expected = {
            value for value in edge_boundaries if value.bit_count() == edge_value
        }
        require(restricted_value == edge_value, "restricted cut value failed")
        require(restricted_minima == expected, "restricted minimizer classification failed")
        require(
            all(
                component_count_after_cut(order, pairs, graph_mask, value) == 2
                for value in restricted_minima
            ),
            "a classified minimum restricted cut has more than two components",
        )
        counters["restricted_strict_gap_cases"] += 1


def graph_mask_from_edges(order: int, selected: set[tuple[int, int]]) -> int:
    pairs = list(itertools.combinations(range(order), 2))
    normalized = {tuple(sorted(edge)) for edge in selected}
    return sum(1 << index for index, edge in enumerate(pairs) if edge in normalized)


def equality_controls() -> dict[str, object]:
    c4_edges = {(0, 1), (1, 2), (2, 3), (0, 3)}
    c4_mask = graph_mask_from_edges(4, c4_edges)
    c4_pairs, _, c4_adjacency = graph_data(4, c4_mask)
    c4_cuts = partition_cut_sets(c4_pairs, c4_adjacency, c4_mask, restricted=False)
    c4_value = min(value.bit_count() for value in c4_cuts)
    c4_singletons = {
        cut_mask(c4_pairs, 1 << vertex) & c4_mask for vertex in range(4)
    }

    parts = ({0, 1}, {2, 3}, {4, 5})
    k222_edges = {
        tuple(sorted((u, v)))
        for i, left in enumerate(parts)
        for right in parts[i + 1 :]
        for u in left
        for v in right
    }
    k222_mask = graph_mask_from_edges(6, k222_edges)
    k222_pairs, k222_edge_list, k222_adjacency = graph_data(6, k222_mask)
    k222_restricted = partition_cut_sets(
        k222_pairs, k222_adjacency, k222_mask, restricted=True
    )
    k222_value = min(value.bit_count() for value in k222_restricted)
    k222_minima = {
        value for value in k222_restricted if value.bit_count() == k222_value
    }
    k222_edge_boundaries = edge_boundary_sets(
        k222_pairs, k222_edge_list, k222_mask
    )
    k222_edge_value = min(value.bit_count() for value in k222_edge_boundaries)

    return {
        "ordinary_equality_control": {
            "graph": "C4",
            "delta": 2,
            "L2": boundary_floor(c4_pairs, c4_mask, 4, 2),
            "lambda": c4_value,
            "has_nonvertex_minimum_cut": bool(
                {value for value in c4_cuts if value.bit_count() == c4_value}
                - c4_singletons
            ),
        },
        "restricted_equality_control": {
            "graph": "K(2,2,2)",
            "edge_boundary_minimum": k222_edge_value,
            "L3": boundary_floor(k222_pairs, k222_mask, 6, 3),
            "lambda_prime": k222_value,
            "has_nonedge_boundary_minimum_cut": bool(
                k222_minima
                - {
                    value
                    for value in k222_edge_boundaries
                    if value.bit_count() == k222_edge_value
                }
            ),
        },
    }


def main() -> None:
    order = 43
    minimum_degree = 18
    maximum_degree = 24
    q = {
        size: minimum_degree * size - 2 * balanced_turan_4_edges(size)
        for size in range(1, order // 2 + 1)
    }
    require(balanced_turan_4_edges(21) == 165, "unexpected t_4(21)")
    require(min(q[size] for size in range(2, 22)) == 34, "two-side floor failed")
    require(min(q[size] for size in range(3, 22)) == 48, "three-side floor failed")
    require(
        [size for size in range(3, 22) if q[size] == 48] == [3, 21],
        "equality-size classification failed",
    )
    require(maximum_degree < 34, "ordinary gap is not strict")
    require(2 * maximum_degree - 2 < 48, "restricted gap is not strict")

    counters = {
        "all_labelled_graphs": 0,
        "connected_graphs": 0,
        "ordinary_strict_gap_cases": 0,
        "restricted_strict_gap_cases": 0,
    }
    for small_order in range(2, 7):
        edge_count = small_order * (small_order - 1) // 2
        for graph_mask in range(1 << edge_count):
            counters["all_labelled_graphs"] += 1
            inspect_graph(small_order, graph_mask, counters)

    turan_observed = {
        str(small_order): counters.pop(f"turan_max_{small_order}")
        for small_order in range(2, 7)
    }
    turan_expected = {
        str(small_order): balanced_turan_4_edges(small_order)
        for small_order in range(2, 7)
    }
    require(turan_observed == turan_expected, "small Turan maxima failed")

    core = {
        "status": "INDEPENDENTLY_VERIFIED_R55_GLOBAL_EDGE_CUT_GAPS",
        "hypotheses": {
            "order": order,
            "degree_interval_each_colour": [minimum_degree, maximum_degree],
            "induced_clique_number_at_most": 4,
        },
        "derived": {
            "q_by_smaller_side_size_1_to_21": [q[size] for size in range(1, 22)],
            "partition_lower_bound_sides_at_least_2": 34,
            "partition_lower_bound_sides_at_least_3": 48,
            "q_equals_48_at_sizes": [3, 21],
            "vertex_boundary_upper_bound": maximum_degree,
            "edge_boundary_upper_bound": 2 * maximum_degree - 2,
            "ordinary_strict_gap": 34 - maximum_degree,
            "restricted_strict_gap": 48 - (2 * maximum_degree - 2),
        },
        "exhaustive_small_graph_checks": {
            **counters,
            "orders": [2, 3, 4, 5, 6],
            "turan_maxima_observed": turan_observed,
            "turan_maxima_expected": turan_expected,
        },
        "strictness_controls": equality_controls(),
        "trust_boundary": (
            "CPython integer/bit operations and exhaustive enumeration through order six; "
            "R(4,5)=25 and the Motzkin-Straus/Turan theorem are imported, not reproved"
        ),
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode()
    result = {**core, "evidence_sha256": hashlib.sha256(canonical).hexdigest()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
