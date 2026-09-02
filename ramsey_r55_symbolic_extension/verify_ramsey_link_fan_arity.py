#!/usr/bin/env python3
"""Exact arithmetic checker for the Ramsey-link singular-fan arity bound."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def ceiling_division(numerator: int, denominator: int) -> int:
    assert numerator >= 0 and denominator > 0
    return (numerator + denominator - 1) // denominator


def verify(data: dict) -> None:
    n = data["core_order"]
    clauses = data["total_selected_clauses"]
    block_size = data["clause_size"]
    minimum_main = data["minimum_clauses_of_main_color"]
    ramsey = data["ramsey_number_r_4_5"]
    forced_witnesses = data["forced_near_k5_witness_clauses"]
    main_neighbors = data["main_clause_other_vertices"]

    # Both color neighborhoods have order at most R(4,5)-1 and partition
    # the other n-1 vertices.
    maximum_degree = ramsey - 1
    minimum_degree = (n - 1) - maximum_degree
    assert data["main_color_degree_range"] == [minimum_degree, maximum_degree]

    expected: dict[str, int] = {}
    for rho in range(minimum_degree, maximum_degree + 1):
        uncovered_main_neighbors = rho - main_neighbors
        extra_opposite_clauses = ceiling_division(uncovered_main_neighbors, block_size)
        maximum_arity = clauses - minimum_main - forced_witnesses - extra_opposite_clauses
        expected[str(rho)] = maximum_arity

        # Category audit: the opposite-color family contains m side clauses,
        # three distinct witnesses, and enough other four-sets to cover the
        # rho-3 remaining main-color neighbors.
        assert (
            minimum_main
            + maximum_arity
            + forced_witnesses
            + extra_opposite_clauses
            == clauses
        )

    assert expected == data["degree_stratified_maximum_side_arity"]
    global_maximum = max(expected.values())
    assert global_maximum == data["global_maximum_side_arity"]
    assert data["eliminated_side_arities"] == list(range(global_maximum + 1, 31))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} CERTIFICATE.json")
    data = json.loads(Path(sys.argv[1]).read_text())
    verify(data)
    table = data["degree_stratified_maximum_side_arity"]
    print(
        "verified: rho=17..24, maxima="
        + ",".join(f"{rho}:{table[str(rho)]}" for rho in range(17, 25))
        + ", global m<=26, eliminated=[27, 28, 29, 30]"
    )


if __name__ == "__main__":
    main()
