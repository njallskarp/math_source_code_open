#!/usr/bin/env python3
"""Independent NetworkX reconstruction of the d=22 anchor witness."""

from __future__ import annotations

import base64
from collections import Counter
import itertools
import json
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_graph6(encoded: str) -> nx.Graph:
    raw = base64.b64decode(encoded, validate=True)
    return nx.from_graph6_bytes(raw)


def count_fives(graph: nx.Graph) -> tuple[int, int]:
    count = through_zero = 0
    for subset in itertools.combinations(graph.nodes, 5):
        if all(graph.has_edge(left, right) for left, right in itertools.combinations(subset, 2)):
            count += 1
            through_zero += int(0 in subset)
    return count, through_zero


def main() -> None:
    data = json.loads((HERE / "ANCHOR_DATA.json").read_text(encoding="utf-8"))
    a = load_graph6(data["red_anchor_core"]["parent_graph6_base64"])
    require((a.number_of_nodes(), a.number_of_edges()) == (22, 114), "red parent")
    a.remove_edges_from(data["red_anchor_core"]["delete_edges"])
    require((a.number_of_nodes(), a.number_of_edges()) == (22, 108), "red core")

    blue_b = load_graph6(data["blue_anchor_core"]["graph6_base64"])
    require((blue_b.number_of_nodes(), blue_b.number_of_edges()) == (20, 100), "blue core")
    require(max(map(len, nx.find_cliques(a))) <= 3, "red A has no K4")
    require(max(map(len, nx.find_cliques(nx.complement(a)))) <= 4, "blue A has no K5")
    require(max(map(len, nx.find_cliques(blue_b))) <= 3, "blue B has no K4")
    require(max(map(len, nx.find_cliques(nx.complement(blue_b)))) <= 4, "red B has no K5")

    red = nx.Graph()
    red.add_nodes_from(range(43))
    red.add_edges_from((0, 1 + vertex) for vertex in range(22))
    red.add_edges_from((1 + left, 1 + right) for left, right in a.edges)
    red.add_edges_from(
        (23 + left, 23 + right)
        for left, right in itertools.combinations(range(20), 2)
        if not blue_b.has_edge(left, right)
    )
    red.add_edges_from(
        (1 + i, 23 + j)
        for i in range(22)
        for j in range(20)
        if (j - i) % 20 < 10
    )
    blue = nx.complement(red)
    require(red.number_of_edges() == 440 and blue.number_of_edges() == 463, "edge partition")
    red_degrees = Counter(dict(red.degree()).values())
    blue_degrees = Counter(dict(blue.degree()).values())
    require(red_degrees == Counter({19: 7, 20: 10, 21: 25, 22: 1}), "red degree box")
    require(blue_degrees == Counter({20: 1, 21: 25, 22: 10, 23: 7}), "blue degree box")

    high = [vertex for vertex, degree in a.degree() if degree >= 10]
    high_graph = a.subgraph(high)
    require(len(high) == 18 and high_graph.number_of_edges() == 73, "high partners")
    require(max(map(len, nx.find_cliques(nx.complement(high_graph)))) <= 4, "high alpha below five")
    k_distribution = Counter(
        len(set(a.neighbors(left)) & set(a.neighbors(right)))
        for left, right in high_graph.edges
    )
    require(k_distribution == Counter({2: 4, 3: 34, 4: 35}), "triple intersections")

    red_fives, red_anchor = count_fives(red)
    blue_fives, blue_anchor = count_fives(blue)
    require((red_fives, blue_fives) == (206, 1536), "monochromatic K5 counts")
    require((red_anchor, blue_anchor) == (0, 0), "no monochromatic K5 through anchor")
    print("PASS NetworkX graph6 reconstruction")
    print("PASS red_edges=440 blue_edges=463 degree_box=19..23")
    print("PASS high=18 high_edges=73 triple_k=2:4,3:34,4:35")
    print("PASS monochromatic_K5 red=206 blue=1536 through_anchor=0")
    print("SCOPE independent library check of the same compact data and cyclic construction")


if __name__ == "__main__":
    main()
