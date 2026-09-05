#!/usr/bin/env python3
"""Independent library-backed graph6 and Ramsey-property cross-check."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path

import networkx as nx


EXPECTED_SHA256 = "53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1"
EXPECTED_HISTOGRAM = {50: 13, 51: 96, 52: 211, 53: 211, 54: 96, 55: 13}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    raw = args.catalog.read_bytes()
    if sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError("unexpected catalog SHA-256")

    graphs = [nx.from_graph6_bytes(line) for line in raw.splitlines()]
    if len(graphs) != 640 or any(len(graph) != 15 for graph in graphs):
        raise ValueError("catalog order/count")
    histogram: Counter[int] = Counter()
    checked = 0
    regular = []
    for index, graph in enumerate(graphs):
        histogram[graph.number_of_edges()] += 1
        degrees = [degree for _, degree in graph.degree()]
        if len(set(degrees)) == 1:
            regular.append((index, degrees[0]))
        for vertices in combinations(graph, 4):
            edges = graph.subgraph(vertices).number_of_edges()
            checked += 1
            if edges in (0, 6):
                raise ValueError(f"non-Ramsey four-set in record {index}")
    if dict(histogram) != EXPECTED_HISTOGRAM or regular:
        raise ValueError("histogram/regularity mismatch")
    print(f"networkx={nx.__version__} records={len(graphs)} checked_four_sets={checked}")
    print("edge_histogram=" + ",".join(f"{e}:{histogram[e]}" for e in sorted(histogram)))
    print("VERIFIED independent NetworkX decode finds no regular catalog record")


if __name__ == "__main__":
    main()
