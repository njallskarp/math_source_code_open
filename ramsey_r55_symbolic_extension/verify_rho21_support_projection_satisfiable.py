#!/usr/bin/env python3
"""Verify explicit satisfying assignments for the four rho=21 support witnesses.

This checker uses only the Python standard library.  It reconstructs the
selected red and blue K4 clauses from the two public kernel certificates and
then evaluates every literal of every signed extension clause directly.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys


def load(path: pathlib.Path) -> tuple[dict, str]:
    raw = path.read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def main() -> None:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
        "ramsey_r55_symbolic_extension/rho21-support-projection-satisfiable-certificate.json"
    )
    data, digest = load(path)
    support_path = path.parent / data["base_certificate"]
    support, support_digest = load(support_path)
    if support_digest != data["base_certificate_sha256"]:
        raise AssertionError("base support-certificate digest mismatch")
    kernel_path = support_path.parent / support["base_kernel_certificate"]
    kernel, kernel_digest = load(kernel_path)
    if kernel_digest != support["base_kernel_certificate_sha256"]:
        raise AssertionError("base kernel-certificate digest mismatch")

    representatives = {item["name"]: item for item in kernel["representatives"]}
    survivors = {
        (item["kernel_representative"], item["demand_case"]): item
        for item in support["survivors"]
    }
    seen: set[tuple[str, str]] = set()

    for witness in data["witnesses"]:
        key = (witness["kernel_representative"], witness["demand_case"])
        if key in seen or key not in survivors:
            raise AssertionError(f"unknown or duplicate witness key {key}")
        seen.add(key)
        representative = representatives[key[0]]
        survivor = survivors[key]
        edges = [tuple(edge) for edge in representative["edges"]]
        side = set(kernel["side_nodes"])
        pivot = support["pivot_vertex_index"]

        blue_clauses: list[set[int]] = []
        for node in range(kernel["clause_nodes"]):
            clause = {i for i, edge in enumerate(edges) if node in edge}
            if node in side:
                clause.add(pivot)
            if len(clause) != 4:
                raise AssertionError(f"blue support at node {node} is not a K4")
            blue_clauses.append(clause)
        red_clauses = [
            {pivot, *support["distinguished_triangle_edge_indices"]},
            *[set(column) for column in survivor["matchings"]],
        ]

        bits = witness["assignment_bits_v0_through_v41"]
        if len(bits) != 42 or set(bits) - {"0", "1"}:
            raise AssertionError(f"invalid assignment for {key}")
        assignment = [bit == "1" for bit in bits]

        # Red K4 R contributes OR_{v in R} not x_v.  Blue K4 B contributes
        # OR_{v in B} x_v.  Evaluate these clauses without a SAT library.
        bad_red = [sorted(clause) for clause in red_clauses if all(assignment[v] for v in clause)]
        bad_blue = [sorted(clause) for clause in blue_clauses if not any(assignment[v] for v in clause)]
        if bad_red or bad_blue:
            raise AssertionError(f"assignment fails {key}: red={bad_red}, blue={bad_blue}")
        if len(red_clauses) != 21 or len(blue_clauses) != 23:
            raise AssertionError("formula does not have 44 clauses")

    if seen != set(survivors):
        raise AssertionError("certificate does not cover all four public survivors")
    print(
        "verified: all four published rho=21 matching-cover systems are "
        f"satisfiable 44-clause extension CNFs; certificate_sha256={digest}"
    )


if __name__ == "__main__":
    main()
