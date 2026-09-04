#!/usr/bin/env python3
"""Independent cofactor replay of the c=3 same-response-class bounds."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json


LOW = Fraction(1, 2)
HIGH = Fraction(3, 2)


def build_base(
    central_lengths: tuple[int, int], connector_lengths: tuple[int, int]
) -> tuple[list[str], list[tuple[int, int]], list[Fraction]]:
    names = ["x", "y", "u", "v"]
    classes = [HIGH, HIGH, LOW, LOW]
    edges: list[tuple[int, int]] = []

    def append_path(
        label: str,
        start: int,
        finish: int,
        length: int,
        internal_classes: list[Fraction],
    ) -> None:
        walk = [start]
        assert len(internal_classes) == length - 1
        for position, response_class in enumerate(internal_classes, start=1):
            walk.append(len(names))
            names.append(f"{label}:{position}")
            classes.append(response_class)
        walk.append(finish)
        edges.extend((walk[index], walk[index + 1]) for index in range(length))

    append_path("A", 2, 2, 5, [LOW] * 4)
    append_path("B", 3, 3, 5, [LOW] * 4)
    append_path("P", 0, 1, central_lengths[0], [HIGH] * (central_lengths[0] - 1))
    append_path("Q", 0, 1, central_lengths[1], [HIGH] * (central_lengths[1] - 1))
    append_path(
        "R",
        0,
        3,
        connector_lengths[0],
        [LOW if position % 2 else HIGH for position in range(1, connector_lengths[0])],
    )
    append_path(
        "S",
        1,
        2,
        connector_lengths[1],
        [LOW if position % 2 else HIGH for position in range(1, connector_lengths[1])],
    )
    normalized = [tuple(sorted(edge)) for edge in edges]
    assert len(normalized) == len(set(normalized))
    return names, normalized, classes


def shifted_signless(
    vertex_count: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    adjacency = [[0] * vertex_count for _ in range(vertex_count)]
    for first, second in edges:
        adjacency[first][second] = adjacency[second][first] = 1
    return [
        [
            adjacency[row][column]
            if row != column
            else sum(adjacency[row]) - 2
            for column in range(vertex_count)
        ]
        for row in range(vertex_count)
    ]


def determinant_bareiss(matrix: list[list[int]]) -> int:
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


def deleted_minor(
    matrix: list[list[int]], omitted_row: int, omitted_column: int
) -> list[list[int]]:
    return [
        [entry for column, entry in enumerate(row) if column != omitted_column]
        for index, row in enumerate(matrix)
        if index != omitted_row
    ]


def inverse_entry(
    matrix: list[list[int]], determinant: int, row: int, column: int
) -> Fraction:
    cofactor = (-1) ** (row + column) * determinant_bareiss(
        deleted_minor(matrix, column, row)
    )
    return Fraction(cofactor, determinant)


def inertia(matrix: list[list[int]]) -> tuple[int, int, int]:
    active = [[Fraction(entry) for entry in row] for row in matrix]
    positive = zero = negative = 0
    while active:
        size = len(active)
        pivot = next((index for index in range(size) if active[index][index]), None)
        if pivot is not None:
            order = [pivot] + [index for index in range(size) if index != pivot]
            active = [[active[row][column] for column in order] for row in order]
            value = active[0][0]
            positive += value > 0
            negative += value < 0
            active = [
                [
                    active[row][column]
                    - active[row][0] * active[0][column] / value
                    for column in range(1, size)
                ]
                for row in range(1, size)
            ]
            continue
        pair = next(
            (
                (first, second)
                for first in range(size)
                for second in range(first + 1, size)
                if active[first][second]
            ),
            None,
        )
        if pair is None:
            zero += size
            break
        first, second = pair
        order = [first, second] + [
            index for index in range(size) if index not in pair
        ]
        active = [[active[row][column] for column in order] for row in order]
        value = active[0][1]
        positive += 1
        negative += 1
        active = [
            [
                active[row][column]
                - (
                    active[row][0] * active[1][column]
                    + active[row][1] * active[0][column]
                )
                / value
                for column in range(2, size)
            ]
            for row in range(2, size)
        ]
    return positive, zero, negative


def line_graph_adjacency(edges: list[tuple[int, int]]) -> list[list[int]]:
    adjacency = [[0] * len(edges) for _ in edges]
    for first in range(len(edges)):
        for second in range(first + 1, len(edges)):
            if set(edges[first]) & set(edges[second]):
                adjacency[first][second] = adjacency[second][first] = 1
    return adjacency


def main() -> None:
    same_class_values = {LOW: Counter(), HIGH: Counter()}
    same_class_edge_values = {LOW: Counter(), HIGH: Counter()}
    records: list[str] = []

    for central in ((1, 3), (3, 1)):
        for connectors in ((1, 1), (1, 3), (3, 1), (3, 3)):
            names, edges, classes = build_base(central, connectors)
            matrix = shifted_signless(len(names), edges)
            determinant = determinant_bareiss(matrix)
            assert determinant in {-4, 4}

            for first in range(len(names)):
                diagonal = inverse_entry(matrix, determinant, first, first)
                assert diagonal == classes[first]
                for second in range(first, len(names)):
                    if classes[first] != classes[second]:
                        continue
                    value = inverse_entry(matrix, determinant, first, second)
                    assert abs(value) <= classes[first]
                    same_class_values[classes[first]][value] += 1
                    records.append(
                        ":".join(
                            (
                                str(central[0]),
                                str(central[1]),
                                str(connectors[0]),
                                str(connectors[1]),
                                names[first],
                                names[second],
                                f"{value.numerator}/{value.denominator}",
                            )
                        )
                    )

            for first, second in edges:
                if classes[first] == classes[second]:
                    value = inverse_entry(matrix, determinant, first, second)
                    same_class_edge_values[classes[first]][value] += 1

    assert same_class_values == {
        LOW: Counter({0: 242, LOW: 184, -LOW: 104}),
        HIGH: Counter({HIGH: 48, 0: 42, -HIGH: 24, 1: 8}),
    }
    assert same_class_edge_values == {
        LOW: Counter({LOW: 80}),
        HIGH: Counter({0: 24, 1: 8}),
    }

    # Definition-level sharpness check on H(5,5;1,3;1,3), ports x,S:1,S:2.
    names, edges, _ = build_base((1, 3), (1, 3))
    base_line_inertia = inertia(line_graph_adjacency(edges))
    assert base_line_inertia == (10, 0, 8)
    ports = tuple(names.index(name) for name in ("x", "S:1", "S:2"))
    augmented_edges = edges + [
        (port, len(names) + offset) for offset, port in enumerate(ports)
    ]
    augmented_line_inertia = inertia(line_graph_adjacency(augmented_edges))
    assert augmented_line_inertia == (11, 0, 10)

    record_digest = hashlib.sha256("\n".join(sorted(records)).encode()).hexdigest()
    result = {
        "algorithm": "integer Bareiss mixed cofactors plus direct line graph",
        "base_assignments": 8,
        "base_line_inertia": list(base_line_inertia),
        "same_class_record_sha256": record_digest,
        "sharp_augmented_line_inertia": list(augmented_line_inertia),
        "status": "VERIFIED",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
