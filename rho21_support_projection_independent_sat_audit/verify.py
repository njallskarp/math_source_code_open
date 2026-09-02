#!/usr/bin/env python3
"""Independent direct audit of the four published rho=21 support witnesses.

This program deliberately does not import or execute the producer's checker or
its satisfiability certificate.  It reads only the two earlier public incidence
certificates, reconstructs the selected K4 supports from their definitions, and
evaluates independently transcribed assignments.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "ramsey_r55_symbolic_extension"
COVER_PATH = DATA / "rho21-bichromatic-matching-cover-certificate.json"
KERNEL_PATH = DATA / "rho21-global-blue-k5-kernel-certificate.json"

EXPECTED_COVER_SHA256 = "01f6b874013d4a85e86b408dbedd04c56e9f03f87da34fff24d3e2b0972e9424"
EXPECTED_KERNEL_SHA256 = "6f30cd3cc288f6e58feeb57adc8b8f4122740b300c92795930639fbafc8fef87"

ASSIGNMENTS = {
    "q=0 two-link representative": {3, 7, 10, 17, 34, 37, 38, 40, 41},
    "q=1 two-link representative": {3, 7, 10, 17, 36, 38, 39, 40, 41},
}


def read_json(path: Path, expected_sha256: str) -> dict:
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_sha256:
        raise AssertionError(f"{path.name}: SHA-256 {actual}, expected {expected_sha256}")
    return json.loads(raw)


def canonical_formula_hash(red: list[frozenset[int]], blue: list[frozenset[int]]) -> str:
    encoded = json.dumps(
        {
            "red_negative_clauses": sorted(sorted(c) for c in red),
            "blue_positive_clauses": sorted(sorted(c) for c in blue),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def reconstruct_blue(edges: list[tuple[int, int]], side_nodes: set[int], pivot: int) -> list[frozenset[int]]:
    clauses = []
    for node in range(23):
        support = {v for v, edge in enumerate(edges) if node in edge}
        if node in side_nodes:
            support.add(pivot)
        if len(support) != 4:
            raise AssertionError(f"blue node {node} reconstructs support {sorted(support)}")
        clauses.append(frozenset(support))
    if len(set(clauses)) != 23:
        raise AssertionError("the 23 reconstructed blue supports are not distinct")
    return clauses


def reconstruct_red(
    survivor: dict,
    edges: list[tuple[int, int]],
    distinguished: list[int],
    pivot: int,
) -> list[frozenset[int]]:
    if len(distinguished) != 3 or len(set(distinguished)) != 3:
        raise AssertionError("distinguished support must contain three distinct ordinary vertices")
    red = [frozenset({pivot, *distinguished})]
    matchings = survivor["matchings"]
    if len(matchings) != 20:
        raise AssertionError("each survivor must contain 20 residual red clauses")
    for number, matching in enumerate(matchings):
        if len(matching) != 4 or len(set(matching)) != 4:
            raise AssertionError(f"residual red clause {number} is not four distinct edge indices")
        endpoints = [endpoint for v in matching for endpoint in edges[v]]
        if len(set(endpoints)) != 8:
            raise AssertionError(f"residual red clause {number} is not a four-edge matching")
        red.append(frozenset(matching))
    if len(set(red)) != 21:
        raise AssertionError("the 21 reconstructed red supports are not distinct")
    return red


def main() -> None:
    cover = read_json(COVER_PATH, EXPECTED_COVER_SHA256)
    kernel = read_json(KERNEL_PATH, EXPECTED_KERNEL_SHA256)

    if cover["base_kernel_certificate"] != KERNEL_PATH.name:
        raise AssertionError("cover certificate names a different kernel certificate")
    if cover["base_kernel_certificate_sha256"] != EXPECTED_KERNEL_SHA256:
        raise AssertionError("cover certificate records a different kernel digest")
    if (kernel["clause_nodes"], kernel["ordinary_edge_vertices"]) != (23, 41):
        raise AssertionError("unexpected kernel dimensions")
    if (cover["pivot_vertex_index"], cover["selected_red_clauses"]) != (41, 21):
        raise AssertionError("unexpected cover dimensions")

    pivot = 41
    side_nodes = set(kernel["side_nodes"])
    if len(side_nodes) != 10 or not side_nodes <= set(range(23)):
        raise AssertionError("invalid side-node set")

    representatives = {item["name"]: item for item in kernel["representatives"]}
    survivors = cover["survivors"]
    if len(representatives) != 2 or len(survivors) != 4:
        raise AssertionError("expected two kernels and four cover survivors")

    seen: set[tuple[str, str]] = set()
    for survivor in survivors:
        name = survivor["kernel_representative"]
        case = survivor["demand_case"]
        key = (name, case)
        if key in seen:
            raise AssertionError(f"duplicate survivor {key}")
        seen.add(key)

        raw_edges = representatives[name]["edges"]
        if len(raw_edges) != 41:
            raise AssertionError(f"{name}: expected 41 ordinary-vertex edges")
        edges = [tuple(edge) for edge in raw_edges]
        if any(len(e) != 2 or e[0] == e[1] or min(e) < 0 or max(e) >= 23 for e in edges):
            raise AssertionError(f"{name}: invalid loop or endpoint")

        blue = reconstruct_blue(edges, side_nodes, pivot)
        distinguished = cover["distinguished_triangle_edge_indices"]
        distinguished_endpoints = [endpoint for v in distinguished for endpoint in edges[v]]
        if len(set(distinguished_endpoints)) != 6:
            raise AssertionError(f"{name}: distinguished triangle is not a three-edge matching")
        if set(distinguished_endpoints) & side_nodes:
            raise AssertionError(f"{name}: distinguished triangle does not avoid side nodes")
        red = reconstruct_red(
            survivor,
            edges,
            distinguished,
            pivot,
        )
        if set().union(*red, *blue) != set(range(42)):
            raise AssertionError(f"{key}: reconstructed formula does not use exactly vertices 0,...,41")

        # This is an additional reconstruction check, not an assumption used by
        # Boolean evaluation: opposite-color selected K4s meet in at most one vertex.
        if max(len(r & b) for r in red for b in blue) > 1:
            raise AssertionError(f"{key}: cross-color intersection exceeds one")

        true_vertices = ASSIGNMENTS[name]
        if len(true_vertices) != 9 or not true_vertices <= set(range(42)):
            raise AssertionError(f"{name}: malformed independently transcribed assignment")

        # A red K4 produces (OR not x_v), false exactly when all its vertices
        # are true.  A blue K4 produces (OR x_v), false exactly when all are false.
        failed_red = [sorted(c) for c in red if c <= true_vertices]
        failed_blue = [sorted(c) for c in blue if c.isdisjoint(true_vertices)]
        if failed_red or failed_blue:
            raise AssertionError(f"{key}: failed_red={failed_red}, failed_blue={failed_blue}")

        min_red_false = min(len(c - true_vertices) for c in red)
        min_blue_true = min(len(c & true_vertices) for c in blue)
        formula_hash = canonical_formula_hash(red, blue)
        print(
            f"ACCEPT {name}; {case}; red=21 blue=23; "
            f"assignment={sorted(true_vertices)}; "
            f"min_red_false={min_red_false}; min_blue_true={min_blue_true}; "
            f"formula_sha256={formula_hash}"
        )

    expected_keys = {
        (name, case)
        for name in ASSIGNMENTS
        for case in ("exceptional_vertex_in_A", "exceptional_vertex_outside_A")
    }
    if seen != expected_keys:
        raise AssertionError(f"survivor keys differ: got {seen}, expected {expected_keys}")
    print("VERIFIED: all four independently reconstructed signed 44-clause CNFs are satisfiable")


if __name__ == "__main__":
    main()
