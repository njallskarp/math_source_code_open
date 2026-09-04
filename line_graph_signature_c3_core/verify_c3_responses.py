#!/usr/bin/env python3
"""Exact diagonal-response proof computation for the c=3 equality family.

Only Python's standard library is used.  The script checks all eight labeled
modulo-four bases, every vertex/leaf port, and the response transport under a
four-subdivision of every base edge.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json


Matrix = list[list[Fraction]]


def equality_base(
    central_lengths: tuple[int, int], connector_lengths: tuple[int, int]
) -> tuple[list[list[int]], list[str], dict[int, Fraction], list[tuple[int, int]]]:
    """Build a labeled reduced three-cycle chain and its predicted responses."""
    p, q = central_lengths
    r, s = connector_lengths
    assert {p, q} == {1, 3}
    assert r in {1, 3} and s in {1, 3}

    # x,y are the central-cycle attachment vertices; u,v are terminal roots.
    names = ["x", "y", "u", "v"]
    edges: list[tuple[int, int]] = []
    paths: dict[str, list[int]] = {}

    def add_path(label: str, start: int, end: int, length: int) -> None:
        sequence = [start]
        for position in range(1, length):
            sequence.append(len(names))
            names.append(f"{label}:{position}")
        sequence.append(end)
        paths[label] = sequence
        edges.extend(zip(sequence, sequence[1:]))

    add_path("A", 2, 2, 5)
    add_path("B", 3, 3, 5)
    add_path("P", 0, 1, p)
    add_path("Q", 0, 1, q)
    add_path("R", 0, 3, r)
    add_path("S", 1, 2, s)

    normalized = [tuple(sorted(edge)) for edge in edges]
    assert all(a != b for a, b in normalized)
    assert len(normalized) == len(set(normalized))
    adjacency = [[0] * len(names) for _ in names]
    for a, b in normalized:
        adjacency[a][b] = adjacency[b][a] = 1
    assert min(map(sum, adjacency)) >= 2
    assert sum(map(sum, adjacency)) // 2 - len(adjacency) + 1 == 3

    expected: dict[int, Fraction] = {}

    def assign(vertices: list[int], value: Fraction) -> None:
        for vertex in vertices:
            if vertex in expected:
                assert expected[vertex] == value
            expected[vertex] = value

    # The repeated endpoint of each loop is omitted on the second occurrence.
    assign(paths["A"][:-1], Fraction(1, 2))
    assign(paths["B"][:-1], Fraction(1, 2))
    assign(paths["P"], Fraction(3, 2))
    assign(paths["Q"], Fraction(3, 2))
    for label in ("R", "S"):
        for distance, vertex in enumerate(paths[label]):
            value = Fraction(3, 2) if distance % 2 == 0 else Fraction(1, 2)
            if vertex in expected:
                assert expected[vertex] == value
            expected[vertex] = value
    assert len(expected) == len(names)
    return adjacency, names, expected, normalized


def shifted_signless(adjacency: list[list[int]]) -> Matrix:
    size = len(adjacency)
    return [
        [
            Fraction(adjacency[i][j] if i != j else sum(adjacency[i]) - 2)
            for j in range(size)
        ]
        for i in range(size)
    ]


def inverse(matrix: Matrix) -> Matrix:
    size = len(matrix)
    work = [
        row[:] + [Fraction(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next((i for i in range(column, size) if work[i][column]), None)
        assert pivot is not None
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                a - multiple * b for a, b in zip(work[row], work[column])
            ]
    result = [row[size:] for row in work]
    assert multiply(matrix, result) == identity(size)
    return result


def identity(size: int) -> Matrix:
    return [
        [Fraction(i == j) for j in range(size)]
        for i in range(size)
    ]


def multiply(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), Fraction())
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def inertia(matrix: Matrix) -> tuple[int, int, int]:
    """Exact symmetric congruence with one- and two-dimensional pivots."""
    active = [row[:] for row in matrix]
    positive = zero = negative = 0
    while active:
        size = len(active)
        pivot = next((i for i in range(size) if active[i][i]), None)
        if pivot is not None:
            order = [pivot] + [i for i in range(size) if i != pivot]
            active = [[active[i][j] for j in order] for i in order]
            value = active[0][0]
            positive += value > 0
            negative += value < 0
            active = [
                [
                    active[i][j] - active[i][0] * active[0][j] / value
                    for j in range(1, size)
                ]
                for i in range(1, size)
            ]
            continue
        pair = next(
            (
                (i, j)
                for i in range(size)
                for j in range(i + 1, size)
                if active[i][j]
            ),
            None,
        )
        if pair is None:
            zero += size
            break
        first, second = pair
        order = [first, second] + [
            i for i in range(size) if i not in pair
        ]
        active = [[active[i][j] for j in order] for i in order]
        value = active[0][1]
        positive += 1
        negative += 1
        active = [
            [
                active[i][j]
                - (
                    active[i][0] * active[1][j]
                    + active[i][1] * active[0][j]
                )
                / value
                for j in range(2, size)
            ]
            for i in range(2, size)
        ]
    return positive, zero, negative


def add_leaf(adjacency: list[list[int]], port: int) -> list[list[int]]:
    size = len(adjacency)
    result = [row[:] + [0] for row in adjacency]
    result.append([0] * (size + 1))
    result[port][size] = result[size][port] = 1
    return result


def four_subdivide(
    adjacency: list[list[int]], edge: tuple[int, int]
) -> list[list[int]]:
    a, b = edge
    assert adjacency[a][b] == 1
    size = len(adjacency)
    result = [row[:] + [0, 0, 0, 0] for row in adjacency]
    result.extend([[0] * (size + 4) for _ in range(4)])
    result[a][b] = result[b][a] = 0
    path = [a, size, size + 1, size + 2, size + 3, b]
    for u, v in zip(path, path[1:]):
        result[u][v] = result[v][u] = 1
    return result


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    path4 = [
        [Fraction(int(abs(i - j) == 1)) for j in range(4)]
        for i in range(4)
    ]
    path4_inverse = [
        list(map(Fraction, row))
        for row in (
            (0, 1, 0, -1),
            (1, 0, 0, 0),
            (0, 0, 0, 1),
            (-1, 0, 1, 0),
        )
    ]
    assert multiply(path4, path4_inverse) == identity(4)
    assert inertia(path4) == (2, 0, 2)

    records: list[str] = []
    response_counts: Counter[Fraction] = Counter()
    base_assignments = base_vertex_cases = leaf_cases = edge_cases = 0

    for central in ((1, 3), (3, 1)):
        for connectors in ((1, 1), (1, 3), (3, 1), (3, 3)):
            adjacency, names, expected, edges = equality_base(central, connectors)
            matrix = shifted_signless(adjacency)
            matrix_inverse = inverse(matrix)
            diagonal = [matrix_inverse[i][i] for i in range(len(matrix))]
            assert diagonal == [expected[i] for i in range(len(matrix))]
            assert inertia(matrix)[1] == 0
            assert inertia(matrix)[0] - inertia(matrix)[2] - 2 == 2

            base_assignments += 1
            base_vertex_cases += len(adjacency)
            response_counts.update(diagonal)
            for name, response in zip(names, diagonal):
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
            for port in range(len(adjacency)):
                leaf_graph = add_leaf(adjacency, port)
                p, z, n = inertia(shifted_signless(leaf_graph))
                assert z == 0
                assert p - n - 2 == 1
                leaf_cases += 1

            for edge in edges:
                enlarged = four_subdivide(adjacency, edge)
                enlarged_inverse = inverse(shifted_signless(enlarged))
                enlarged_diagonal = [
                    enlarged_inverse[i][i] for i in range(len(enlarged))
                ]
                assert enlarged_diagonal[: len(adjacency)] == diagonal
                u, v = edge
                assert enlarged_diagonal[len(adjacency) :] == [
                    diagonal[v],
                    diagonal[u],
                    diagonal[v],
                    diagonal[u],
                ]
                edge_cases += 1

    assert base_assignments == 8
    assert base_vertex_cases == 128
    assert leaf_cases == 128
    assert edge_cases == 144
    assert response_counts == Counter({Fraction(1, 2): 88, Fraction(3, 2): 40})
    record_digest = hashlib.sha256("\n".join(sorted(records)).encode()).hexdigest()
    result = {
        "algorithm": "exact Fraction inverse and congruence",
        "base_assignments": base_assignments,
        "base_vertex_cases": base_vertex_cases,
        "four_subdivision_edge_cases": edge_cases,
        "leaf_cases": leaf_cases,
        "maximum_response": "3/2",
        "minimum_response": "1/2",
        "record_sha256": record_digest,
        "response_counts": {"1/2": 88, "3/2": 40},
        "status": "VERIFIED",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
