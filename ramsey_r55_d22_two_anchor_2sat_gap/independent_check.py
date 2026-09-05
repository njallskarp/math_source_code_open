"""Independent NetworkX reconstruction and width audit."""
from __future__ import annotations

import base64
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    data = json.loads((HERE / "WITNESS.json").read_text())
    red_core = nx.from_graph6_bytes(base64.b64decode(data["red_core_parent_graph6_base64"]))
    blue_core = nx.from_graph6_bytes(base64.b64decode(data["blue_core_graph6_base64"]))
    require(len(red_core) == 22 and red_core.number_of_edges() == 114, "red parent")
    require(len(blue_core) == 20 and blue_core.number_of_edges() == 100, "blue core")
    red_core.remove_edges_from(map(tuple, data["red_core_delete_edges"]))

    red = nx.Graph()
    red.add_nodes_from(range(43))
    red.add_edges_from((0, x) for x in range(1, 23))
    red.add_edges_from((a + 1, b + 1) for a, b in red_core.edges())
    red.add_edges_from(
        (a + 23, b + 23)
        for a, b in combinations(range(20), 2)
        if not blue_core.has_edge(a, b)
    )
    red.add_edges_from(
        (i + 1, j + 23)
        for i, row in enumerate(data["cross_rows"])
        for j, bit in enumerate(row)
        if bit == "1"
    )
    blue = nx.complement(red)
    degrees = Counter(dict(red.degree()).values())
    require(red.number_of_edges() == 452, "edge count")
    require(degrees == Counter({21: 26, 22: 9, 20: 8}), "degree profile")

    neighborhoods = []
    local = []
    for root in (0, 3):
        for graph, opposite, label in ((red, blue, "R"), (blue, red, "B")):
            vertices = set(graph.neighbors(root))
            neighborhoods.append(vertices)
            require(max(map(len, nx.find_cliques(graph.subgraph(vertices)))) <= 3, "same-color K4")
            require(max(map(len, nx.find_cliques(opposite.subgraph(vertices)))) <= 4, "opposite-color K5")
            local.append([root, label, len(vertices), graph.subgraph(vertices).number_of_edges()])
    require(local == [[0, "R", 22, 108], [0, "B", 20, 100], [3, "R", 21, 99], [3, "B", 21, 98]], "local profiles")

    outside = [x for x in range(43) if x not in (0, 3)]
    signature = {x: (red.has_edge(0, x), red.has_edge(3, x)) for x in outside}
    diagonal = {
        edge for edge in combinations(outside, 2)
        if signature[edge[0]][0] != signature[edge[1]][0]
        and signature[edge[0]][1] != signature[edge[1]][1]
    }
    require(len(diagonal) == 210, "diagonal count")
    for a, b in combinations(outside, 2):
        unseen = not any(a in neighborhood and b in neighborhood for neighborhood in neighborhoods)
        require(unseen == ((a, b) in diagonal), "unseen interface")

    diagonal_order = sorted(diagonal)
    variable = {edge: index + 1 for index, edge in enumerate(diagonal_order)}
    short_clauses = set()
    for subset in combinations(outside, 5):
        pairs = set(combinations(subset, 2))
        holes = pairs & diagonal
        if not 1 <= len(holes) <= 2:
            continue
        exposed = pairs - holes
        if all(red.has_edge(*edge) for edge in exposed):
            clause = tuple(sorted(-variable[edge] for edge in holes))
            short_clauses.add(clause)
            require(any(edge not in red.edges for edge in holes), "violated short red clause")
        if all(blue.has_edge(*edge) for edge in exposed):
            clause = tuple(sorted(variable[edge] for edge in holes))
            short_clauses.add(clause)
            require(any(edge in red.edges for edge in holes), "violated short blue clause")
    require(len(short_clauses) == 413, "short residual clause count")

    defects = Counter()
    first = {}
    for graph, label in ((red, "R"), (blue, "B")):
        five_sets = sorted({
            tuple(sorted(subset))
            for clique in nx.find_cliques(graph)
            for subset in combinations(clique, 5)
        })
        for subset in five_sets:
            width = sum(edge in diagonal for edge in combinations(subset, 2))
            defects[(label, width)] += 1
            first.setdefault((label, width), list(subset))
    require(
        defects == Counter({("R", 3): 141, ("B", 3): 93, ("B", 6): 58, ("B", 4): 53, ("R", 4): 20, ("R", 6): 1}),
        "defect profile",
    )
    require(min(width for _label, width in defects) == 3, "minimum defect width")
    require(first[("R", 3)] == data["first_red_width3_k5"], "first red defect")
    require(first[("B", 3)] == data["first_blue_width3_k5"], "first blue defect")

    output = {
        "degrees": sorted(degrees.items()),
        "diagonal_edges": len(diagonal),
        "first_blue_width3_k5": data["first_blue_width3_k5"],
        "first_red_width3_k5": data["first_red_width3_k5"],
        "local": local,
        "minimum_defect_width": 3,
        "monochromatic_defects": [[label, width, defects[(label, width)]] for label, width in sorted(defects)],
        "status": "PASS_DEGREE_COMPATIBLE_WIDTH2_SAT",
        "width_at_most_two_clauses": len(short_clauses),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
