"""Independent NetworkX replay of the three-anchor survivor."""
from __future__ import annotations

import base64
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent


def construct(data):
    red_core = nx.from_graph6_bytes(base64.b64decode(data["red_core_parent_graph6_base64"]))
    red_core.remove_edges_from(data["red_core_delete_edges"])
    blue_core = nx.from_graph6_bytes(base64.b64decode(data["blue_core_graph6_base64"]))
    red = nx.Graph()
    red.add_nodes_from(range(43))
    red.add_edges_from((0, vertex) for vertex in range(1, 23))
    red.add_edges_from((left + 1, right + 1) for left, right in red_core.edges())
    red.add_edges_from(
        (left + 23, right + 23)
        for left, right in nx.complement(blue_core).edges()
    )
    red.add_edges_from(
        (left + 1, right + 23)
        for left, row in enumerate(data["cross_rows"])
        for right, bit in enumerate(row)
        if bit == "1"
    )
    return red


def max_clique_order(graph):
    return max(map(len, nx.find_cliques(graph)), default=0)


def five_sets(graph):
    return {
        subset
        for clique in nx.find_cliques(graph)
        for subset in combinations(sorted(clique), 5)
    }


def main():
    data = json.loads((HERE / "WITNESS.json").read_text())
    anchors = tuple(data["anchors"])
    red = construct(data)
    blue = nx.complement(red)
    assert red.number_of_edges() == 452
    assert Counter(dict(red.degree()).values()) == Counter({20: 8, 21: 26, 22: 9})

    profiles = []
    neighborhoods = []
    for root in anchors:
        for label, graph, other in (("R", red, blue), ("B", blue, red)):
            vertices = set(graph.neighbors(root))
            same = graph.subgraph(vertices)
            opposite = other.subgraph(vertices)
            assert max_clique_order(same) <= 3
            assert max_clique_order(opposite) <= 4
            profiles.append([root, label, len(vertices), same.number_of_edges()])
            neighborhoods.append(vertices)

    outside = sorted(set(range(43)) - set(anchors))
    signatures = {
        vertex: tuple(int(red.has_edge(root, vertex)) for root in anchors)
        for vertex in outside
    }
    omitted = {
        pair for pair in combinations(outside, 2)
        if all(signatures[pair[0]][index] != signatures[pair[1]][index] for index in range(3))
    }
    assert omitted == {
        pair for pair in combinations(outside, 2)
        if all(not ({pair[0], pair[1]} <= neighborhood) for neighborhood in neighborhoods)
    }

    red_fives = {subset for subset in five_sets(red) if not set(subset) & set(anchors)}
    blue_fives = {subset for subset in five_sets(blue) if not set(subset) & set(anchors)}
    assert len(red_fives) == 269 and len(blue_fives) == 200
    profile = Counter()
    rows = []
    for label, family in (("B", blue_fives), ("R", red_fives)):
        for subset in sorted(family):
            width = sum(pair in omitted for pair in combinations(subset, 2))
            profile[(label, width)] += 1
            rows.append(label + ":" + ",".join(map(str, subset)))
    rows.sort(key=lambda row: (tuple(map(int, row[2:].split(","))), row[0]))
    digest = sha256(("\n".join(rows) + "\n").encode()).hexdigest()

    first_red = (4, 12, 14, 24, 31)
    first_blue = (1, 7, 8, 18, 34)
    for graph, subset in ((red, first_red), (blue, first_blue)):
        assert all(graph.has_edge(left, right) for left, right in combinations(subset, 2))
        support = {signatures[vertex] for vertex in subset}
        assert all({bits[index] for bits in support} == {0, 1} for index in range(3))
        assert not any(
            all(left[index] != right[index] for index in range(3))
            for left, right in combinations(support, 2)
        )

    print(json.dumps({
        "defect_digest": digest,
        "defect_profile": [[label, width, profile[(label, width)]] for label, width in sorted(profile)],
        "edges": red.number_of_edges(),
        "omitted_edges": len(omitted),
        "profiles": profiles,
        "status": "PASS_THREE_VALID_ANCHORS_WITH_FULLY_VISIBLE_DEFECTS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
