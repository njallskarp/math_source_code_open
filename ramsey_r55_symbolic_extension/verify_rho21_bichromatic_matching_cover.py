#!/usr/bin/env python3
"""Verify the exact rho=21 bichromatic demand-matching-cover certificate.

The universal equivalence is the written proof. This checker independently
audits its finite arithmetic and the four supplied partial-support witnesses:
kernel incidence, cover demands, cross-color compatibility, selected-support
degrees, and definition-level forced-K5 searches in both colors.
"""

from __future__ import annotations

import collections
import hashlib
import itertools
import json
import pathlib
import sys


def load_json(path: pathlib.Path) -> tuple[dict, str]:
    raw = path.read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def support_graph(vertex_count: int, clauses: list[set[int]]) -> list[set[int]]:
    adjacency = [set() for _ in range(vertex_count)]
    for clause in clauses:
        if len(clause) != 4:
            raise AssertionError(f"non-four-clause {sorted(clause)}")
        for u, v in itertools.combinations(clause, 2):
            adjacency[u].add(v)
            adjacency[v].add(u)
    return adjacency


def find_k5(adjacency: list[set[int]]) -> tuple[int, ...] | None:
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        if all(v in adjacency[u] for u, v in itertools.combinations(vertices, 2)):
            return vertices
    return None


def blue_clauses(edges: list[tuple[int, int]], side: set[int], pivot: int) -> list[set[int]]:
    clauses: list[set[int]] = []
    for node in range(23):
        support = {i for i, edge in enumerate(edges) if node in edge}
        if node in side:
            support.add(pivot)
        clauses.append(support)
    return clauses


def demand_vector(case: str, edge_count: int, a_edges: set[int], exceptional: int) -> list[int]:
    result = [2] * edge_count
    if case == "exceptional_vertex_in_A":
        if exceptional not in a_edges:
            raise AssertionError("in-A exceptional edge is not in A")
        for edge in a_edges:
            result[edge] = 1
        result[exceptional] = 2
    elif case == "exceptional_vertex_outside_A":
        if exceptional in a_edges:
            raise AssertionError("outside-A exceptional edge lies in A")
        for edge in a_edges:
            result[edge] = 1
        result[exceptional] = 3
    else:
        raise AssertionError(f"unknown demand case {case}")
    if sum(result) != 80:
        raise AssertionError("residual red demand does not total 20*4")
    return result


def verify_survivor(data: dict, base: dict, survivor: dict) -> dict:
    representatives = {item["name"]: item for item in base["representatives"]}
    representative = representatives[survivor["kernel_representative"]]
    edges = [tuple(edge) for edge in representative["edges"]]
    edge_count = data["ordinary_vertices"]
    if len(edges) != edge_count:
        raise AssertionError("wrong kernel edge count")

    side = set(base["side_nodes"])
    pivot = data["pivot_vertex_index"]
    a_edges = set(data["distinguished_triangle_edge_indices"])
    if len(a_edges) != 3:
        raise AssertionError("A does not have three vertices")
    a_endpoints: set[int] = set()
    for index in a_edges:
        if set(edges[index]) & side:
            raise AssertionError("A edge meets a side-clause node")
        if set(edges[index]) & a_endpoints:
            raise AssertionError("A is not a matching in D")
        a_endpoints.update(edges[index])

    case = survivor["demand_case"]
    exceptional = data["demand_cases"][case]["exceptional_edge_index"]
    target = demand_vector(case, edge_count, a_edges, exceptional)
    matchings = [tuple(sorted(matching)) for matching in survivor["matchings"]]
    if len(matchings) != data["residual_red_clauses"]:
        raise AssertionError("wrong residual red-clause count")
    if len(set(matchings)) != len(matchings):
        raise AssertionError("duplicate residual red support")

    observed = [0] * edge_count
    for matching in matchings:
        if len(matching) != data["residual_clause_size"] or len(set(matching)) != 4:
            raise AssertionError(f"invalid four-edge matching {matching}")
        endpoints: set[int] = set()
        for index in matching:
            if not 0 <= index < edge_count:
                raise AssertionError("matching edge index out of range")
            if set(edges[index]) & endpoints:
                raise AssertionError(f"column is not a matching: {matching}")
            endpoints.update(edges[index])
            observed[index] += 1
    if observed != target:
        raise AssertionError("matching cover has wrong demand vector")

    blue = blue_clauses(edges, side, pivot)
    red = [{pivot, *a_edges}] + [set(matching) for matching in matchings]
    if len({tuple(sorted(clause)) for clause in blue}) != len(blue):
        raise AssertionError("duplicate selected blue clause")
    if len({tuple(sorted(clause)) for clause in red}) != len(red):
        raise AssertionError("duplicate selected red clause")
    if any(len(r & b) > 1 for r in red for b in blue):
        raise AssertionError("opposite-color supports intersect in more than one vertex")

    blue_degree = collections.Counter(x for clause in blue for x in clause)
    red_degree = collections.Counter(x for clause in red for x in clause)
    if blue_degree[pivot] != 10 or any(blue_degree[x] != 2 for x in range(edge_count)):
        raise AssertionError("wrong selected-blue degree profile")
    if red_degree[pivot] != 1 or red_degree[exceptional] != 3:
        raise AssertionError("wrong exceptional selected-red degrees")
    if any(red_degree[x] != 2 for x in range(edge_count) if x != exceptional):
        raise AssertionError("wrong ordinary selected-red degree")

    red_k5 = find_k5(support_graph(42, red))
    blue_k5 = find_k5(support_graph(42, blue))
    if red_k5 is not None or blue_k5 is not None:
        raise AssertionError(f"selected supports force K5: red={red_k5}, blue={blue_k5}")
    return {"kernel": representative["name"], "case": case}


def main() -> None:
    here = pathlib.Path(__file__).resolve().parent
    certificate_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else (
        here / "rho21-bichromatic-matching-cover-certificate.json"
    )
    data, certificate_digest = load_json(certificate_path)
    base_path = certificate_path.parent / data["base_kernel_certificate"]
    base, base_digest = load_json(base_path)
    if base_digest != data["base_kernel_certificate_sha256"]:
        raise AssertionError("base kernel certificate digest mismatch")

    case_names = set(data["demand_cases"])
    exact_cases = {"exceptional_vertex_in_A", "exceptional_vertex_outside_A"}
    if case_names != exact_cases:
        raise AssertionError("demand-case classification is not exact")
    seen = set()
    reports = []
    for survivor in data["survivors"]:
        key = (survivor["kernel_representative"], survivor["demand_case"])
        if key in seen:
            raise AssertionError("duplicate survivor case")
        seen.add(key)
        reports.append(verify_survivor(data, base, survivor))
    expected = {
        (representative["name"], case)
        for representative in base["representatives"]
        for case in case_names
    }
    if seen != expected:
        raise AssertionError("not every representative/demand case has a witness")

    print(
        "verified: exact two-case red-demand matching-cover grammar; "
        f"joint_survivors={len(reports)}; selected_red_and_blue_forced_k5=0; "
        f"certificate_sha256={certificate_digest}"
    )


if __name__ == "__main__":
    main()
