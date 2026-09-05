#!/usr/bin/env python3
"""Independent library-backed check of the seven sharp local witnesses."""

from __future__ import annotations

import base64
import json
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
Q0 = {18: 9, 19: 10, 20: 10, 21: 10, 22: 10, 23: 11, 24: 11}


def main() -> None:
    data = json.loads((HERE / "SHARP_WITNESSES.json").read_text(encoding="utf-8"))
    summaries = []
    for item in data["witnesses"]:
        d = item["d"]
        graph = nx.from_graph6_bytes(base64.b64decode(item["parent_graph6_base64"], validate=True))
        graph.remove_edges_from(map(tuple, item["delete_edges"]))
        assert len(graph) == d
        assert U[d] - graph.number_of_edges() in range(7)
        assert max(dict(graph.degree()).values()) == Q0[d]
        assert max(map(len, nx.find_cliques(graph))) <= 3
        assert max(map(len, nx.find_cliques(nx.complement(graph)))) <= 4
        summaries.append(f"d={d}:e={graph.number_of_edges()}:Delta={max(dict(graph.degree()).values())}")
    print("PASS NetworkX 3.6 independent witnesses " + " ".join(summaries))


if __name__ == "__main__":
    main()
