#!/usr/bin/env python3
"""Independent certificate audit for the dense degree-five R(4,5;22) census."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pathlib
import urllib.request

import networkx as nx


TARGET_COMMIT = "8bf27902fba404e35593c90cbc7d2991abeda510"
TARGET_CERTIFICATE = (
    "https://raw.githubusercontent.com/njallskarp/math_source_code_open/"
    f"{TARGET_COMMIT}/ramsey_r55_degree_five_classification/certificate.json"
)
TARGET_CERTIFICATE_SHA256 = (
    "905518c06dcd9fc4008dd5caf70eece7dbb67c77e6cd6d708388fca3d22a9da1"
)
CATALOGUE = "https://users.cecs.anu.edu.au/~bdm/data/r44_16.g6"
CATALOGUE_SHA256 = (
    "b9a7c89cf999d64c976c877891d06f828ce2e846f5ddfa72bb402f2ddd57b927"
)


def read_bytes(location: str) -> bytes:
    if location.startswith(("https://", "http://")):
        request = urllib.request.Request(
            location, headers={"User-Agent": "degree-five-independent-review/1"}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()
    return pathlib.Path(location).read_bytes()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def decode_graph6(record: str) -> nx.Graph:
    graph = nx.from_graph6_bytes(record.strip().encode("ascii"))
    require(
        set(graph.nodes) == set(range(graph.number_of_nodes())),
        "graph6 decoder returned unexpected labels",
    )
    return graph


def is_complete(graph: nx.Graph, vertices: tuple[int, ...]) -> bool:
    return all(graph.has_edge(u, v) for u, v in itertools.combinations(vertices, 2))


def has_clique(graph: nx.Graph, order: int) -> bool:
    return any(
        is_complete(graph, vertices)
        for vertices in itertools.combinations(graph.nodes, order)
    )


def graph_from_edges(order: int, edges: list[list[int]]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(order))
    graph.add_edges_from((int(u), int(v)) for u, v in edges)
    return graph


def eligible_neighbor_classes() -> tuple[int, list[nx.Graph]]:
    pairs = list(itertools.combinations(range(5), 2))
    labeled_count = 0
    classes: list[nx.Graph] = []
    for mask in range(1 << len(pairs)):
        graph = nx.Graph()
        graph.add_nodes_from(range(5))
        graph.add_edges_from(pair for bit, pair in enumerate(pairs) if mask >> bit & 1)
        if graph.number_of_edges() < 4 or has_clique(graph, 3):
            continue
        labeled_count += 1
        if not any(nx.is_isomorphic(graph, representative) for representative in classes):
            classes.append(graph)
    return labeled_count, classes


def automorphisms(graph: nx.Graph) -> list[dict[int, int]]:
    matcher = nx.algorithms.isomorphism.GraphMatcher(graph, graph)
    return list(matcher.isomorphisms_iter())


def transport_columns(
    columns: tuple[int, ...],
    core_map: dict[int, int],
    neighbor_map: dict[int, int],
) -> tuple[int, ...]:
    transported = [0] * 5
    for old_neighbor, column in enumerate(columns):
        new_column = 0
        for old_core in range(16):
            if column >> old_core & 1:
                new_column |= 1 << core_map[old_core]
        transported[neighbor_map[old_neighbor]] = new_column
    return tuple(transported)


def assemble(
    core: nx.Graph, neighbor: nx.Graph, columns: tuple[int, ...]
) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(22))
    graph.add_edges_from(core.edges)
    graph.add_edges_from((16 + u, 16 + v) for u, v in neighbor.edges)
    for s, column in enumerate(columns):
        graph.add_edges_from(
            (a, 16 + s) for a in range(16) if column >> a & 1
        )
    graph.add_edges_from((16 + s, 21) for s in range(5))
    return graph


def edge_signature(graph: nx.Graph) -> set[tuple[int, int]]:
    return {tuple(sorted(edge)) for edge in graph.edges}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", default=TARGET_CERTIFICATE)
    parser.add_argument("--catalogue", default=CATALOGUE)
    args = parser.parse_args()

    certificate_bytes = read_bytes(args.certificate)
    catalogue_bytes = read_bytes(args.catalogue)
    require(
        sha256(certificate_bytes) == TARGET_CERTIFICATE_SHA256,
        "pinned target certificate hash mismatch",
    )
    require(
        sha256(catalogue_bytes) == CATALOGUE_SHA256,
        "primary catalogue hash mismatch",
    )
    certificate = json.loads(certificate_bytes)
    require(certificate["catalogue_url"] == CATALOGUE, "catalogue URL mismatch")
    require(
        certificate["catalogue_sha256"] == CATALOGUE_SHA256,
        "certificate catalogue hash mismatch",
    )

    catalogue_records = [line.decode("ascii") for line in catalogue_bytes.splitlines() if line]
    require(catalogue_records == certificate["catalogue_records"], "catalogue records differ")
    require(len(catalogue_records) == 2, "catalogue does not contain two records")
    cores = [decode_graph6(record) for record in catalogue_records]
    for core in cores:
        require(core.number_of_nodes() == 16, "wrong core order")
        require(core.number_of_edges() == 60, "wrong core edge count")
        require(not has_clique(core, 4), "core has a 4-clique")
        require(not has_clique(nx.complement(core), 4), "core has an independent 4-set")
    require(not nx.is_isomorphic(cores[0], cores[1]), "catalogue cores are isomorphic")
    core_automorphisms = [automorphisms(core) for core in cores]
    require([len(group) for group in core_automorphisms] == [8, 8], "core automorphism counts")
    degree_seven_triangle_counts = []
    for core in cores:
        degree_seven = [vertex for vertex, degree in core.degree if degree == 7]
        induced = core.subgraph(degree_seven)
        degree_seven_triangle_counts.append(sum(nx.triangles(induced).values()) // 3)
    require(degree_seven_triangle_counts == [0, 4], "core distinguishing invariant")

    labeled_neighbor_count, neighbor_classes = eligible_neighbor_classes()
    require(len(neighbor_classes) == 7, "wrong neighbor isomorphism-class count")
    cases: dict[tuple[int, int], dict] = {}
    neighbors_by_type: dict[int, nx.Graph] = {}
    for case in certificate["cases"]:
        key = (int(case["core"]), int(case["type"]))
        require(key not in cases, "duplicate case")
        require(key[0] in (0, 1), "unknown core index")
        neighbor = graph_from_edges(5, case["s_edges"])
        require(neighbor.number_of_edges() >= 4, "sparse neighbor case")
        require(not has_clique(neighbor, 3), "neighbor case has a triangle")
        if key[1] in neighbors_by_type:
            require(
                edge_signature(neighbor) == edge_signature(neighbors_by_type[key[1]]),
                "same type has inconsistent labeled edges",
            )
        else:
            neighbors_by_type[key[1]] = neighbor
        cases[key] = case
    require(len(cases) == 14, "wrong case count")
    require(len(neighbors_by_type) == 7, "wrong number of neighbor types")
    supplied_neighbors = list(neighbors_by_type.values())
    require(
        all(
            sum(nx.is_isomorphic(graph, supplied) for supplied in supplied_neighbors) == 1
            for graph in neighbor_classes
        ),
        "certificate neighbor types do not equal the exhaustive seven classes",
    )
    require(
        all((core, type_code) in cases for core in (0, 1) for type_code in neighbors_by_type),
        "incomplete core/neighbor cross-product",
    )

    representatives: list[nx.Graph] = []
    orbit_sums = {key: 0 for key in cases}
    clique_checks = 0
    independent_checks = 0
    for record in certificate["representatives"]:
        core_index = int(record["core"])
        type_code = int(record["type"])
        key = (core_index, type_code)
        require(key in cases, "representative has unknown case")
        core = cores[core_index]
        neighbor = neighbors_by_type[type_code]
        columns = tuple(int(value) for value in record["columns"])
        require(len(columns) == 5, "representative does not have five columns")
        require(all(0 <= value < (1 << 16) for value in columns), "column mask range")
        graph = assemble(core, neighbor, columns)
        encoded = decode_graph6(record["graph6"])
        require(edge_signature(graph) == edge_signature(encoded), "graph6/column mismatch")
        require(graph.number_of_edges() == 109, "representative edge count")
        require([v for v, degree in graph.degree if degree == 5] == [21], "degree-five uniqueness")
        require(not has_clique(graph, 4), "representative has a 4-clique")
        require(not has_clique(nx.complement(graph), 5), "representative has an independent 5-set")
        clique_checks += len(list(itertools.combinations(range(22), 4)))
        independent_checks += len(list(itertools.combinations(range(22), 5)))

        m = neighbor.number_of_edges()
        sizes = [column.bit_count() for column in columns]
        require(all(6 <= size <= 8 for size in sizes), "column size outside reduction")
        require(sum(8 - size for size in sizes) == m - 4, "density defect identity")

        neighbor_automorphisms = automorphisms(neighbor)
        orbit = {
            transport_columns(columns, core_map, neighbor_map)
            for core_map in core_automorphisms[core_index]
            for neighbor_map in neighbor_automorphisms
        }
        require(len(orbit) == int(record["orbit"]), "reported orbit size mismatch")
        require(columns == min(orbit), "representative is not orbit-minimal")
        orbit_sums[key] += len(orbit)
        representatives.append(graph)

    require(len(representatives) == 13, "wrong representative count")
    nonisomorphic_pairs = 0
    for left, right in itertools.combinations(representatives, 2):
        require(not nx.is_isomorphic(left, right), "two representatives are isomorphic")
        nonisomorphic_pairs += 1
    require(nonisomorphic_pairs == 78, "wrong pair count")
    require(
        all(orbit_sums[key] == int(case["solutions"]) for key, case in cases.items()),
        "representative orbit sums do not equal reported case totals",
    )

    result = {
        "catalogue": {
            "automorphism_orders": [len(group) for group in core_automorphisms],
            "degree7_triangle_invariant": degree_seven_triangle_counts,
            "graphs": len(cores),
            "sha256": sha256(catalogue_bytes),
        },
        "certificate_sha256": sha256(certificate_bytes),
        "neighbor_census": {
            "case_records": len(cases),
            "isomorphism_classes": len(neighbor_classes),
            "labeled_graphs": labeled_neighbor_count,
        },
        "representatives": {
            "clique_subsets_checked": clique_checks,
            "edge_counts": sorted({graph.number_of_edges() for graph in representatives}),
            "graphs": len(representatives),
            "independent_subsets_checked": independent_checks,
            "orbit_sum": sum(orbit_sums.values()),
            "pairwise_nonisomorphic_pairs": nonisomorphic_pairs,
            "unique_degree_five": sum(
                [v for v, degree in graph.degree if degree == 5] == [21]
                for graph in representatives
            ),
        },
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
