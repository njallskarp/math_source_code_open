"""Independent NetworkX/object-level replay of the third-anchor core."""
from __future__ import annotations

import base64
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent


def pair(left, right):
    return tuple(sorted((left, right)))


def construct(data):
    red_core = nx.from_graph6_bytes(base64.b64decode(data["red_core_parent_graph6_base64"]))
    red_core.remove_edges_from(data["red_core_delete_edges"])
    blue_core = nx.from_graph6_bytes(base64.b64decode(data["blue_core_graph6_base64"]))
    red = nx.Graph()
    red.add_nodes_from(range(43))
    red.add_edges_from((0, vertex) for vertex in range(1, 23))
    red.add_edges_from((left + 1, right + 1) for left, right in red_core.edges())
    red_blue_side = nx.complement(blue_core)
    red.add_edges_from((left + 23, right + 23) for left, right in red_blue_side.edges())
    red.add_edges_from(
        (left + 1, right + 23)
        for left, row in enumerate(data["cross_rows"])
        for right, value in enumerate(row)
        if value == "1"
    )
    return red


def maximum_clique_order(graph):
    return max(map(len, nx.find_cliques(graph)), default=0)


def main():
    data = json.loads((HERE / "BASE_WITNESS.json").read_text())
    certificate = json.loads((HERE / "CERTIFICATE.json").read_text())
    red = construct(data)
    blue = nx.complement(red)
    assert red.number_of_edges() == 452
    assert Counter(dict(red.degree()).values()) == Counter({20: 8, 21: 26, 22: 9})
    profiles = []
    for root in (0, 3):
        for label, graph, other in (("R", red, blue), ("B", blue, red)):
            vertices = set(graph.neighbors(root))
            same = graph.subgraph(vertices)
            opposite = other.subgraph(vertices)
            assert maximum_clique_order(same) <= 3
            assert maximum_clique_order(opposite) <= 4
            profiles.append([root, label, len(vertices), same.number_of_edges()])

    signatures = {
        vertex: (int(red.has_edge(0, vertex)), int(red.has_edge(3, vertex)))
        for vertex in range(43) if vertex not in (0, 3)
    }
    diagonal = {
        edge for edge in combinations(signatures, 2)
        if all(signatures[edge[0]][index] != signatures[edge[1]][index] for index in range(2))
    }
    assert len(diagonal) == 210
    variables = [tuple(edge) for edge in certificate["variables"]]
    assert set(variables) <= diagonal

    conditions = []
    for record in certificate["constraints"]:
        root_color = record["anchor_color"] == "R"
        forbidden_color = record["forbidden_color"] == "R"
        subset = tuple(record["subset"])
        row = [(pair(1, vertex), root_color) for vertex in subset]
        row.extend((edge, forbidden_color) for edge in combinations(subset, 2))
        assert all(edge in variables or edge not in diagonal for edge, _color in row)
        conditions.append(row)

    violation_counts = Counter()
    for bits in product((False, True), repeat=7):
        assignment = dict(zip(variables, bits))

        def is_red(edge):
            return assignment[edge] if edge in assignment else red.has_edge(*edge)

        violated = [
            index for index, row in enumerate(conditions)
            if all(is_red(edge) == required for edge, required in row)
        ]
        assert violated
        violation_counts[violated[0] + 1] += 1

    print(json.dumps({
        "assignments_checked": 128,
        "diagonal_edges": len(diagonal),
        "first_violation_counts": sorted(violation_counts.items()),
        "profiles": profiles,
        "status": "PASS_NO_VALID_THIRD_ANCHOR_AT_VERTEX_1",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
