#!/usr/bin/env python3
"""Audit the rho=21 global-kernel criterion for forced blue K5s.

The checker has two independent layers.  First it exhausts all relabeled
pairwise-intersecting multisets of four and five edges, proving the only local
patterns used by the written theorem.  Second it reconstructs the selected
blue graph for each supplied 23-node kernel and compares the three symbolic
conditions with a definition-level search through all five-vertex subsets.
No SAT solver or external package is used.
"""

from __future__ import annotations

import collections
import hashlib
import itertools
import json
import pathlib
import sys


Edge = tuple[int, int]


def intersects(e: Edge, f: Edge) -> bool:
    return bool(set(e) & set(f))


def pairwise_intersecting(family: tuple[Edge, ...]) -> bool:
    return all(intersects(e, f) for e, f in itertools.combinations(family, 2))


def degrees(family: tuple[Edge, ...]) -> collections.Counter[int]:
    result: collections.Counter[int] = collections.Counter()
    for u, v in family:
        result[u] += 1
        result[v] += 1
    return result


def common_centers(family: tuple[Edge, ...]) -> set[int]:
    center = set(family[0])
    for edge in family[1:]:
        center &= set(edge)
    return center


def audit_local_classification(
    label_count: int, maximum_multiplicity: int, maximum_side_side_multiplicity: int
) -> dict:
    labels = range(label_count)
    edge_types = tuple(itertools.combinations(labels, 2))
    five_checked = 0
    four_side_checked = 0

    # Five pairwise-intersecting edge occurrences, under maximum degree four,
    # cannot form a star.  They must be supported on exactly three vertices.
    for family in itertools.combinations_with_replacement(edge_types, 5):
        mult = collections.Counter(family)
        if max(mult.values()) > maximum_multiplicity:
            continue
        deg = degrees(family)
        if max(deg.values()) > 4 or not pairwise_intersecting(family):
            continue
        five_checked += 1
        if common_centers(family):
            raise AssertionError("five-edge star survived maximum degree four")
        if len(set().union(*map(set, family))) != 3:
            raise AssertionError("five-edge intersecting family is not triangular")

    # For a four-edge clique containing w, every edge must touch the ten-node
    # side set.  Exhaust every side marking on six canonical labels.
    for family in itertools.combinations_with_replacement(edge_types, 4):
        mult = collections.Counter(family)
        if max(mult.values()) > maximum_multiplicity:
            continue
        deg = degrees(family)
        if max(deg.values()) > 4 or not pairwise_intersecting(family):
            continue
        used = set().union(*map(set, family))
        for mask in range(1 << label_count):
            side = {i for i in labels if mask & (1 << i)}
            if any(deg[s] > 3 for s in side):
                continue
            if any(mult[e] > maximum_side_side_multiplicity for e in mult if set(e) <= side):
                continue
            if not all(set(edge) & side for edge in family):
                continue
            four_side_checked += 1
            centers = common_centers(family)
            if centers:
                if not any(c not in side and all((set(e) - {c}) <= side for e in family) for c in centers):
                    raise AssertionError("four-edge side-touching star has wrong center")
            else:
                if len(used) != 3 or len(used & side) < 2:
                    raise AssertionError("four-edge side-touching family has wrong triangle")

    if five_checked == 0 or four_side_checked == 0:
        raise AssertionError("local audit was vacuous")
    return {"five_edge_patterns": five_checked, "four_edge_side_markings": four_side_checked}


def kernel_data(node_count: int, raw_edges: list[list[int]]):
    edges: list[Edge] = []
    mult: collections.Counter[Edge] = collections.Counter()
    degree = [0] * node_count
    for raw in raw_edges:
        if len(raw) != 2:
            raise AssertionError(f"not an edge: {raw}")
        u, v = raw
        if not (0 <= u < node_count and 0 <= v < node_count) or u == v:
            raise AssertionError(f"invalid loop or endpoint: {raw}")
        edge = (min(u, v), max(u, v))
        edges.append(edge)
        mult[edge] += 1
        degree[u] += 1
        degree[v] += 1
    return tuple(edges), mult, degree


def symbolic_obstructions(node_count: int, edges: tuple[Edge, ...], side: set[int]):
    mult = collections.Counter(edges)
    triangle5 = []
    side_triangle4 = []
    for a, b, c in itertools.combinations(range(node_count), 3):
        weight = mult[(a, b)] + mult[(a, c)] + mult[(b, c)]
        if weight >= 5:
            triangle5.append((a, b, c, weight))
        if len({a, b, c} & side) >= 2 and weight >= 4:
            side_triangle4.append((a, b, c, weight))
    side_stars = []
    for center in set(range(node_count)) - side:
        value = sum(1 for u, v in edges if (u == center and v in side) or (v == center and u in side))
        if value >= 4:
            side_stars.append((center, value))
    return triangle5, side_triangle4, side_stars


def forced_blue_graph(edges: tuple[Edge, ...], side: set[int]):
    # Ordinary vertices are edge occurrences; the final vertex is w, whose
    # incidence set is the side-node set.
    incidence = [frozenset(edge) for edge in edges] + [frozenset(side)]
    adjacency = [set() for _ in incidence]
    for i, j in itertools.combinations(range(len(incidence)), 2):
        if incidence[i] & incidence[j]:
            adjacency[i].add(j)
            adjacency[j].add(i)
    return adjacency


def find_k5(adjacency: list[set[int]]):
    # Definition-level bounded search, intentionally independent of the
    # weighted-triangle/star implementation.
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        if all(v in adjacency[u] for u, v in itertools.combinations(vertices, 2)):
            return vertices
    return None


def verify_representative(data: dict, representative: dict) -> None:
    n = data["clause_nodes"]
    side = set(data["side_nodes"])
    edges, mult, degree = kernel_data(n, representative["edges"])
    if len(edges) != data["ordinary_edge_vertices"]:
        raise AssertionError("wrong ordinary-edge count")
    if max(mult.values()) > data["maximum_edge_multiplicity"]:
        raise AssertionError("edge multiplicity exceeds three")
    if any(
        value > data["maximum_side_side_edge_multiplicity"]
        for edge, value in mult.items()
        if set(edge) <= side
    ):
        raise AssertionError("side-side edge multiplicity exceeds two")
    for node in range(n):
        expected = data["side_node_ordinary_degree"] if node in side else data["non_side_node_ordinary_degree"]
        if degree[node] != expected:
            raise AssertionError(f"wrong degree at node {node}: {degree[node]} != {expected}")

    symbolic = symbolic_obstructions(n, edges, side)
    symbolic_has_k5 = any(symbolic)
    witness = find_k5(forced_blue_graph(edges, side))
    if symbolic_has_k5 != (witness is not None):
        raise AssertionError("symbolic criterion disagrees with definition-level K5 search")
    if witness is not None:
        raise AssertionError(f"certificate representative unexpectedly forces K5 {witness}")


def main() -> None:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
        "ramsey_r55_symbolic_extension/rho21-global-blue-k5-kernel-certificate.json"
    )
    raw = path.read_bytes()
    data = json.loads(raw)
    local = audit_local_classification(
        data["local_pattern_enumeration_labels"],
        data["maximum_edge_multiplicity"],
        data["maximum_side_side_edge_multiplicity"],
    )
    for representative in data["representatives"]:
        verify_representative(data, representative)

    digest = hashlib.sha256(raw).hexdigest()
    print(
        "verified: forced-blue K5 iff triangle weight>=5, side-heavy triangle "
        ">=4, or non-side four-star into S; "
        f"local_patterns={local}; representatives={len(data['representatives'])}; "
        f"certificate_sha256={digest}"
    )


if __name__ == "__main__":
    main()
