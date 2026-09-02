#!/usr/bin/env python3
"""Exact checker for the terminal binary-proliferation certificate."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

Literal = int
Clause = frozenset[Literal]


def terminal_cycle(p: int) -> tuple[Clause, ...]:
    return tuple(
        frozenset((-index, index % p + 1)) for index in range(1, p + 1)
    )


def common_intersection(clauses: tuple[Clause, ...]) -> Clause:
    result = set(clauses[0])
    for clause in clauses[1:]:
        result &= clause
    return frozenset(result)


def verify_cycle(p: int) -> None:
    clauses = terminal_cycle(p)
    assert len(clauses) == p
    assert len(set(clauses)) == p
    assert all(len(clause) == 2 for clause in clauses)
    frequencies = Counter(literal for clause in clauses for literal in clause)
    assert set(frequencies) == set(range(1, p + 1)) | set(range(-p, 0))
    assert all(multiplicity == 1 for multiplicity in frequencies.values())
    assert common_intersection(clauses) == frozenset()


def verify_certificate(data: dict) -> None:
    original = data["original_clause_length"]
    first_derived = data["first_derived_clause_length"]
    loss = data["maximum_loss_per_later_resolution"]
    expected_floors = [
        min(original, first_derived - max(0, step - 1) * loss)
        for step in range(6)
    ]
    assert expected_floors == data["stage_floor_through_five"]
    assert expected_floors == [4, 4, 4, 4, 3, 2]

    assert data["maximum_binary_clauses_after_step_five"] == 1
    assert data["excluded_p"] == [36, 37]
    assert data["surviving_p_minimum"] == 2
    assert data["surviving_p_maximum"] == data["core_variables"] - 7

    for p in data["terminal_cycle_intersection_checks"]:
        verify_cycle(p)

    # p=37: five steps can leave at most one binary, not 37.
    assert data["core_variables"] - 37 == 5
    assert data["maximum_binary_clauses_after_step_five"] < 37

    # p=36: with a main tail of size >=2, at most one old and one new
    # binary survive. With a singleton main tail, all 36 new binaries would
    # share it, contrary to the directly checked empty cycle intersection.
    assert data["core_variables"] - 36 == 6
    assert data["maximum_binary_clauses_after_step_five"] + 1 < 36


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} CERTIFICATE.json")
    data = json.loads(Path(sys.argv[1]).read_text())
    verify_certificate(data)
    print(
        "verified: "
        f"stage_floors={data['stage_floor_through_five']}, "
        f"excluded={data['excluded_p']}, "
        f"surviving_p={data['surviving_p_minimum']}..{data['surviving_p_maximum']}"
    )


if __name__ == "__main__":
    main()
