#!/usr/bin/env python3
"""Check the exact rho=21 two-link kernel grammar and its representatives.

The proof of universality is the suppression argument in the research note.
This checker independently audits its integer consequences, the two claimed
X-link cases, both converse reconstructions, and a concrete nonempty member
of each abstract kernel family.  It deliberately does not check whether a
kernel is realizable inside a two-colored K5-free Ramsey graph.
"""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import sys


def fail(message: str) -> None:
    raise AssertionError(message)


def edge_data(node_count: int, edges: list[list[int]], maximum: int):
    degree = [0] * node_count
    multiplicity: collections.Counter[tuple[int, int]] = collections.Counter()
    for raw in edges:
        if len(raw) != 2:
            fail(f"not an edge: {raw}")
        u, v = raw
        if not (0 <= u < node_count and 0 <= v < node_count):
            fail(f"endpoint outside 0..{node_count - 1}: {raw}")
        if u == v:
            fail(f"loop found: {raw}")
        e = (min(u, v), max(u, v))
        multiplicity[e] += 1
        degree[u] += 1
        degree[v] += 1
    if multiplicity and max(multiplicity.values()) > maximum:
        fail("edge multiplicity exceeds the certificate bound")
    return degree, multiplicity


def reconstruct_supports(
    node_count: int, edges: list[list[int]], half_edge_nodes: list[int]
) -> tuple[list[frozenset[str]], collections.Counter[str]]:
    supports: list[set[str]] = [set() for _ in range(node_count)]
    vertex_degree: collections.Counter[str] = collections.Counter()
    for i, (u, v) in enumerate(edges):
        name = f"e{i}"
        supports[u].add(name)
        supports[v].add(name)
        vertex_degree[name] = 2
    for i, node in enumerate(half_edge_nodes):
        name = f"h{i}"
        supports[node].add(name)
        vertex_degree[name] = 1
    return [frozenset(s) for s in supports], vertex_degree


def verify_x_link(data: dict) -> None:
    n = data["projected_clause_nodes"]
    q = data["mixed_k3_node"]
    assert n == 10 and data["k4_nodes"] == 9 and data["mixed_k3_nodes"] == 1
    assert data["ordinary_vertices"] == 18 and data["degree_one_vertices"] == 3
    assert data["ordinary_edges"] == 18 and data["half_edges"] == 3

    # A red triangle meets any blue clique in at most one vertex.  Therefore
    # q_A=|Q cap A| can only be zero or one, and the two derived degree
    # sequences below exhaust that integer choice.
    derived = {}
    for q_a in (0, 1):
        degrees = [4] * 9 + [3]
        # Put Q first.  Each of the three distinct A half-edges subtracts one
        # ordinary incidence, q_a of them at Q and the rest at K4 nodes.
        degrees = [3 - q_a] + [3] * (3 - q_a) + [4] * (6 + q_a)
        derived[bool(q_a)] = sorted(degrees)

    if len(data["cases"]) != 2:
        fail("the X-link certificate must contain exactly two cases")
    seen = set()
    for case in data["cases"]:
        meets = case["mixed_triangle_meets_A"]
        if meets in seen:
            fail("duplicate X-link case")
        seen.add(meets)
        half = case["half_edge_nodes"]
        if len(half) != 3 or len(set(half)) != 3:
            fail("the three A half-edges must attach to distinct nodes")
        if (q in half) != meets:
            fail("mixed-triangle/A incidence disagrees with the case label")
        edges = case["representative_edges"]
        if len(edges) != 18:
            fail("an X-link representative must have 18 ordinary edges")
        degree, _ = edge_data(n, edges, data["maximum_edge_multiplicity"])
        if degree != case["ordinary_degrees"]:
            fail(f"wrong labeled X-link degrees in {case['name']}: {degree}")
        if sorted(degree) != derived[meets]:
            fail(f"wrong X-link degree multiset in {case['name']}")

        supports, vertex_degree = reconstruct_supports(n, edges, half)
        required_sizes = [3] + [4] * 9
        if [len(s) for s in supports] != required_sizes:
            fail(f"reconstructed X supports have wrong sizes in {case['name']}")
        if len(set(supports[1:])) != 9:
            fail(f"duplicate reconstructed internal K4 support in {case['name']}")
        if sorted(vertex_degree.values()).count(1) != 3:
            fail("wrong count of degree-one X vertices")
        if sorted(vertex_degree.values()).count(2) != 18:
            fail("wrong count of degree-two X vertices")

    assert seen == {False, True}


def verify_y_link(data: dict) -> None:
    n = data["triangle_occurrence_nodes"]
    side = set(data["side_nodes"])
    witness = set(data["witness_nodes"])
    half_node = data["half_edge_node"]
    assert n == 13 and len(side) == 10 and len(witness) == 3
    assert side.isdisjoint(witness) and side | witness == set(range(n))
    assert data["ordinary_vertices"] == 19 and data["degree_one_vertices"] == 1
    assert data["ordinary_edges"] == 19 and data["half_edges"] == 1

    edges = data["representative_edges"]
    if len(edges) != 19:
        fail("the Y-link representative must have 19 ordinary edges")
    degree, multiplicity = edge_data(n, edges, data["maximum_edge_multiplicity"])
    if degree != data["ordinary_degrees"]:
        fail(f"wrong labeled Y-link degrees: {degree}")
    if degree[half_node] != 2 or any(degree[i] != 3 for i in range(n) if i != half_node):
        fail("Y-link ordinary degrees are not 2,3^12")
    for (u, v), mult in multiplicity.items():
        if u in side and v in side and mult == 3:
            fail("two side nodes encode the same selected triangle")

    supports, vertex_degree = reconstruct_supports(n, edges, [half_node])
    if any(len(s) != 3 for s in supports):
        fail("reconstructed Y supports are not all triangles")
    if len({supports[i] for i in side}) != 10:
        fail("the ten reconstructed side-triangle supports are not distinct")
    if sorted(vertex_degree.values()).count(1) != 1:
        fail("wrong count of degree-one Y triangle-incidence vertices")
    if sorted(vertex_degree.values()).count(2) != 19:
        fail("wrong count of degree-two Y triangle-incidence vertices")

    # The mixed 3+1 clause supplies the missing second occurrence of the
    # half-edge vertex and touches no other Y vertex.
    completed = vertex_degree.copy()
    completed["h0"] += 1
    if set(completed.values()) != {2} or len(completed) != 20:
        fail("adding the mixed singleton does not give exact Y degree two")


def main() -> None:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
        "ramsey_r55_symbolic_extension/rho21-two-link-kernel-certificate.json"
    )
    raw = path.read_bytes()
    data = json.loads(raw)
    assert data["rho"] == 21
    assert data["red_neighborhood_size"] == 21
    assert data["blue_neighborhood_size"] == 20
    verify_x_link(data["x_link"])
    verify_y_link(data["y_link"])
    digest = hashlib.sha256(raw).hexdigest()
    print(
        "verified: rho=21 two-link kernel grammar has exactly two X degree "
        "families and one Y degree family; all representatives reconstruct; "
        f"certificate_sha256={digest}"
    )


if __name__ == "__main__":
    main()
