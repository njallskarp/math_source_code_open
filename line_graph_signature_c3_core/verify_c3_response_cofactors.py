#!/usr/bin/env python3
"""Independent determinant/cofactor replay of c=3 equality responses.

This file does not import the primary checker.  It reconstructs the eight
labeled bases and computes every inverse diagonal as a principal cofactor
divided by the determinant, using fraction-free Bareiss elimination.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json


def build_base(
    central_lengths: tuple[int, int], connector_lengths: tuple[int, int]
) -> tuple[list[list[int]], list[str]]:
    names = ["x", "y", "u", "v"]
    edge_list: list[tuple[int, int]] = []

    def append_path(label: str, endpoints: tuple[int, int], length: int) -> None:
        start, finish = endpoints
        walk = [start]
        for position in range(1, length):
            walk.append(len(names))
            names.append(f"{label}:{position}")
        walk.append(finish)
        edge_list.extend((walk[i], walk[i + 1]) for i in range(length))

    append_path("A", (2, 2), 5)
    append_path("B", (3, 3), 5)
    append_path("P", (0, 1), central_lengths[0])
    append_path("Q", (0, 1), central_lengths[1])
    append_path("R", (0, 3), connector_lengths[0])
    append_path("S", (1, 2), connector_lengths[1])

    adjacency = [[0] * len(names) for _ in names]
    for a, b in edge_list:
        assert not adjacency[a][b]
        adjacency[a][b] = adjacency[b][a] = 1
    return adjacency, names


def shifted_signless(adjacency: list[list[int]]) -> list[list[int]]:
    return [
        [
            adjacency[i][j] if i != j else sum(adjacency[i]) - 2
            for j in range(len(adjacency))
        ]
        for i in range(len(adjacency))
    ]


def determinant_bareiss(matrix: list[list[int]]) -> int:
    """Exact integer determinant by fraction-free elimination."""
    size = len(matrix)
    if size == 0:
        return 1
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot_row = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot_row is None:
            return 0
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, size):
            for target in range(column + 1, size):
                numerator = (
                    work[row][target] * pivot
                    - work[row][column] * work[column][target]
                )
                quotient, remainder = divmod(numerator, previous)
                assert remainder == 0
                work[row][target] = quotient
            work[row][column] = 0
        previous = pivot
    return sign * work[-1][-1]


def principal_minor(matrix: list[list[int]], omitted: int) -> list[list[int]]:
    return [
        [entry for column, entry in enumerate(row) if column != omitted]
        for index, row in enumerate(matrix)
        if index != omitted
    ]


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    assert determinant_bareiss([]) == 1
    assert determinant_bareiss([[7]]) == 7
    assert determinant_bareiss([[0, 1], [1, 0]]) == -1
    assert determinant_bareiss([[1, 2], [2, 4]]) == 0

    records: list[str] = []
    determinant_counts: Counter[int] = Counter()
    response_counts: Counter[Fraction] = Counter()
    vertex_cases = 0

    for central in ((1, 3), (3, 1)):
        for connectors in ((1, 1), (1, 3), (3, 1), (3, 3)):
            adjacency, names = build_base(central, connectors)
            matrix = shifted_signless(adjacency)
            determinant = determinant_bareiss(matrix)
            expected_determinant = -4 * (-1) ** sum(length == 3 for length in connectors)
            assert determinant == expected_determinant
            determinant_counts[determinant] += 1

            for vertex, name in enumerate(names):
                cofactor = determinant_bareiss(principal_minor(matrix, vertex))
                response = Fraction(cofactor, determinant)
                assert response in {Fraction(1, 2), Fraction(3, 2)}
                response_counts[response] += 1
                vertex_cases += 1
                records.append(
                    ":".join(
                        (
                            str(central[0]),
                            str(central[1]),
                            str(connectors[0]),
                            str(connectors[1]),
                            name,
                            fraction_text(response),
                        )
                    )
                )

    assert vertex_cases == 128
    assert determinant_counts == Counter({-4: 4, 4: 4})
    assert response_counts == Counter({Fraction(1, 2): 88, Fraction(3, 2): 40})
    record_digest = hashlib.sha256("\n".join(sorted(records)).encode()).hexdigest()
    assert record_digest == "3f35404094eee97889596aa8fa4387782aef8a329fb3ec58b5d6651deeae5651"

    result = {
        "algorithm": "integer Bareiss determinants and principal cofactors",
        "base_assignments": 8,
        "determinant_counts": {"-4": 4, "4": 4},
        "maximum_response": "3/2",
        "minimum_response": "1/2",
        "record_sha256": record_digest,
        "response_counts": {"1/2": 88, "3/2": 40},
        "status": "VERIFIED",
        "vertex_cases": vertex_cases,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
