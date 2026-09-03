#!/usr/bin/env python3
"""Clean-room check of the order-23 branched-broom counterexample.

This script imports only the already-proved sibling-leaf count formula.  It
does not use the producer's closed potential formulas or either producer
checker.  Trees are reconstructed as edge sets, distances are obtained by
Floyd--Warshall, and weak-composition counts are evaluated by dynamic
programming rather than ``math.comb``.
"""

from __future__ import annotations

from hashlib import sha256
import json


Graph = list[set[int]]


def graph(vertex_count: int, edges: list[tuple[int, int]]) -> Graph:
    adjacency = [set() for _ in range(vertex_count)]
    for left, right in edges:
        assert 0 <= left < vertex_count and 0 <= right < vertex_count
        assert left != right and right not in adjacency[left]
        adjacency[left].add(right)
        adjacency[right].add(left)
    assert len(edges) == vertex_count - 1

    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                frontier.append(neighbor)
    assert len(reached) == vertex_count
    return adjacency


def branched_broom(d: int, e: int, t: int) -> Graph:
    """Return R(d,e,t), using vertices 0,...,t for its central path."""
    assert d >= 1 and e >= 1 and t >= 1
    edges = [(index, index + 1) for index in range(t)]
    next_vertex = t + 1
    for _ in range(d):
        edges.append((0, next_vertex))
        next_vertex += 1
    for _ in range(e):
        arm = next_vertex
        leaf = next_vertex + 1
        next_vertex += 2
        edges.extend(((t, arm), (arm, leaf)))
    return graph(next_vertex, edges)


def symmetric_double_broom(a: int, ell: int) -> Graph:
    """Return B(a,a,ell), where the two hubs are ell edges apart."""
    assert a >= 1 and ell >= 1
    edges = [(index, index + 1) for index in range(ell)]
    next_vertex = ell + 1
    for hub in (0, ell):
        for _ in range(a):
            edges.append((hub, next_vertex))
            next_vertex += 1
    return graph(next_vertex, edges)


def all_distances(adjacency: Graph) -> list[list[int]]:
    """Compute graph distances by exact Floyd--Warshall relaxation."""
    size = len(adjacency)
    infinity = size + 1
    distance = [[infinity] * size for _ in range(size)]
    for vertex in range(size):
        distance[vertex][vertex] = 0
        for neighbor in adjacency[vertex]:
            distance[vertex][neighbor] = 1
    for middle in range(size):
        for left in range(size):
            through_middle = distance[left][middle]
            for right in range(size):
                candidate = through_middle + distance[middle][right]
                if candidate < distance[left][right]:
                    distance[left][right] = candidate
    assert all(value <= size - 1 for row in distance for value in row)
    return distance


def weak_composition_count(total: int, parts: int) -> int:
    """Count weak compositions by a prefix-sum dynamic program."""
    assert total >= 0 and parts >= 1
    counts = [1] * (total + 1)  # One part.
    for _ in range(1, parts):
        running = 0
        next_counts = []
        for value in counts:
            running += value
            next_counts.append(running)
        counts = next_counts
    return counts[total]


def sibling_leaf_count(adjacency: Graph) -> tuple[int, dict[int, tuple[int, int]]]:
    """Apply the imported sibling-leaf formula directly to a graph."""
    distance = all_distances(adjacency)
    leaves = {vertex for vertex, neighbors in enumerate(adjacency) if len(neighbors) == 1}
    nonleaves = set(range(len(adjacency))) - leaves
    parents = {next(iter(adjacency[leaf])) for leaf in leaves}

    data: dict[int, tuple[int, int]] = {}
    for parent in parents:
        leaf_degree = sum(neighbor in leaves for neighbor in adjacency[parent])
        potential = sum(
            len(adjacency[vertex]) * 2 ** distance[parent][vertex]
            for vertex in nonleaves
        )
        data[parent] = (potential, leaf_degree)

    maximum = max(potential for potential, _ in data.values())
    maximizing = {
        parent: values for parent, values in data.items() if values[0] == maximum
    }
    count = sum(
        weak_composition_count(potential, leaf_degree)
        for potential, leaf_degree in maximizing.values()
    )
    return count, maximizing


def main() -> None:
    candidate_graph = branched_broom(8, 4, 6)
    assert len(candidate_graph) == 23
    candidate_count, candidate_maximizers = sibling_leaf_count(candidate_graph)
    assert candidate_maximizers == {0: (1477, 8)}
    assert candidate_count == 3_100_645_395_776_119_256

    rows = []
    for ell in range(1, 23):
        remainder = 22 - ell
        if remainder > 0 and remainder % 2 == 0:
            a = remainder // 2
            broom = symmetric_double_broom(a, ell)
            assert len(broom) == 23
            count, maximizers = sibling_leaf_count(broom)
            assert len(maximizers) == 2
            assert {leaf_degree for _, leaf_degree in maximizers.values()} == {a}
            rows.append({"a": a, "ell": ell, "count": count})

    assert len(rows) == 10
    best = max(rows, key=lambda row: row["count"])
    assert best == {
        "a": 6,
        "ell": 10,
        "count": 1_111_665_975_462_168_688,
    }
    difference = candidate_count - best["count"]
    assert difference == 1_988_979_420_313_950_568 > 0

    record = {
        "candidate_order": len(candidate_graph),
        "candidate_maximizers": {
            str(parent): list(values)
            for parent, values in candidate_maximizers.items()
        },
        "candidate_count": candidate_count,
        "symmetric_double_brooms": rows,
        "best_symmetric_double_broom": best,
        "difference": difference,
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print(f"record_sha256={sha256(canonical.encode()).hexdigest()}")
    print("status=VERIFIED")


if __name__ == "__main__":
    main()
