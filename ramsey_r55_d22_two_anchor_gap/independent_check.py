"""Independent NetworkX reconstruction and edge-first forcing audit."""
from __future__ import annotations

import base64
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent


def fail_unless(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    data = json.loads((HERE / "WITNESS.json").read_text())
    h = nx.from_graph6_bytes(base64.b64decode(data["red_core_parent_graph6_base64"]))
    j = nx.from_graph6_bytes(base64.b64decode(data["blue_core_graph6_base64"]))
    fail_unless(len(h) == 22 and h.number_of_edges() == 114, "red parent")
    fail_unless(len(j) == 20 and j.number_of_edges() == 100, "blue core")
    h.remove_edges_from(map(tuple, data["red_core_delete_edges"]))

    red = nx.Graph()
    red.add_nodes_from(range(43))
    red.add_edges_from((0, x) for x in range(1, 23))
    red.add_edges_from((a + 1, b + 1) for a, b in h.edges())
    red.add_edges_from(
        (a + 23, b + 23) for a, b in combinations(range(20), 2) if not j.has_edge(a, b)
    )
    red.add_edges_from(
        (i + 1, k + 23)
        for i, row in enumerate(data["cross_rows"])
        for k, bit in enumerate(row)
        if bit == "1"
    )
    blue = nx.complement(red)
    fail_unless(red.number_of_edges() == 452, "edge count")
    fail_unless(Counter(dict(red.degree()).values()) == Counter({20: 8, 21: 26, 22: 9}), "degrees")

    local = []
    neighborhoods = []
    for root in (0, 3):
        for graph, label in ((red, "R"), (blue, "B")):
            vertices = set(graph.neighbors(root))
            neighborhoods.append(vertices)
            same = graph.subgraph(vertices).number_of_edges()
            opposite = blue if graph is red else red
            fail_unless(max(map(len, nx.find_cliques(graph.subgraph(vertices)))) <= 3, "same K4")
            fail_unless(max(map(len, nx.find_cliques(opposite.subgraph(vertices)))) <= 4, "opposite K5")
            local.append([root, label, len(vertices), same])
    fail_unless(local == [[0, "R", 22, 108], [0, "B", 20, 100], [3, "R", 21, 95], [3, "B", 21, 101]], "local profiles")

    outside = [x for x in range(43) if x not in (0, 3)]
    signature = {x: (red.has_edge(0, x), red.has_edge(3, x)) for x in outside}
    diagonal = {
        tuple(sorted((a, b)))
        for a, b in combinations(outside, 2)
        if signature[a][0] != signature[b][0] and signature[a][1] != signature[b][1]
    }
    fail_unless(len(diagonal) == 210, "diagonal size")
    for a, b in combinations(outside, 2):
        edge = (a, b)
        unseen = not any(a in neighborhood and b in neighborhood for neighborhood in neighborhoods)
        fail_unless(unseen == (edge in diagonal), "neighborhood coverage")

    # Edge-first enumeration is deliberately different from verify.py's
    # five-set-first residual-CNF construction.
    unit_red = Counter()
    unit_blue = Counter()
    for hole in sorted(diagonal):
        remaining = [x for x in outside if x not in hole]
        for triple in combinations(remaining, 3):
            subset = tuple(sorted(hole + triple))
            all_pairs = set(combinations(subset, 2))
            if (all_pairs & diagonal) != {hole}:
                continue
            pairs = all_pairs - {hole}
            if all(red.has_edge(*edge) for edge in pairs):
                unit_red[hole] += 1
            if all(blue.has_edge(*edge) for edge in pairs):
                unit_blue[hole] += 1
    fail_unless(sum(unit_red.values()) == 8 and len(unit_red) == 7, "red unit census")
    fail_unless(sum(unit_blue.values()) == 16 and len(unit_blue) == 13, "blue unit census")
    fail_unless(not (set(unit_red) & set(unit_blue)), "opposite unit conflict")

    coupled = list(map(tuple, data["coupled_diagonal_edges"]))
    fail_unless(coupled == [(4, 32), (4, 35)], "coupled edges")
    for subset, hole in zip(data["blue_unit_five_sets"], coupled):
        pairs = set(combinations(subset, 2))
        fail_unless((pairs & diagonal) == {hole}, "blue unit hole")
        fail_unless(all(blue.has_edge(*edge) for edge in pairs - {hole}), "blue unit support")
        fail_unless(hole in unit_blue, "blue unit detected")
    red_subset = data["red_binary_five_set"]
    red_pairs = set(combinations(red_subset, 2))
    fail_unless((red_pairs & diagonal) == set(coupled), "red binary holes")
    fail_unless(all(red.has_edge(*edge) for edge in red_pairs - set(coupled)), "red binary support")

    defects = Counter()
    for graph, label in ((red, "R"), (blue, "B")):
        five_sets = {
            tuple(sorted(subset))
            for clique in nx.find_cliques(graph)
            for subset in combinations(clique, 5)
        }
        defects[label] = len(five_sets)
    fail_unless(defects == Counter({"R": 336, "B": 223}), "full-coloring defects")
    output = {
        "blue_unit_occurrences": sum(unit_blue.values()),
        "blue_unit_variables": len(unit_blue),
        "certificate": ["x_4_32>=1", "x_4_35>=1", "x_4_32+x_4_35<=1"],
        "degrees": sorted(Counter(dict(red.degree()).values()).items()),
        "diagonal_edges": len(diagonal),
        "full_coloring_defects": dict(sorted(defects.items())),
        "local": local,
        "red_unit_occurrences": sum(unit_red.values()),
        "red_unit_variables": len(unit_red),
        "status": "PASS_UNIT_SAT_BINARY_UNSAT",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
