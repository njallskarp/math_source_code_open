#!/usr/bin/env python3
"""Exact structural and three-port checks for c=3 equality cores."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json

from verify_c3_responses import (
    equality_base,
    four_subdivide,
    inertia,
    inverse,
    shifted_signless,
)


LOW = Fraction(1, 2)
HIGH = Fraction(3, 2)


def signature(inertia_triple: tuple[int, int, int]) -> int:
    positive, _, negative = inertia_triple
    return positive - negative


def edge_list(adjacency: list[list[int]]) -> list[tuple[int, int]]:
    return [
        (first, second)
        for first in range(len(adjacency))
        for second in range(first + 1, len(adjacency))
        if adjacency[first][second]
    ]


def check_same_class_invariant(
    matrix_inverse: list[list[Fraction]],
    classes: list[Fraction],
    edges: list[tuple[int, int]],
) -> None:
    for first in range(len(classes)):
        for second in range(first, len(classes)):
            if classes[first] != classes[second]:
                continue
            bound = classes[first]
            assert abs(matrix_inverse[first][second]) <= bound

    for first, second in edges:
        if classes[first] != classes[second]:
            continue
        value = matrix_inverse[first][second]
        if classes[first] == LOW:
            assert value == LOW
        else:
            assert -LOW <= value <= HIGH


def check_transport(
    old_inverse: list[list[Fraction]],
    new_inverse: list[list[Fraction]],
    edge: tuple[int, int],
) -> None:
    first, second = edge
    size = len(old_inverse)
    assert [row[:size] for row in new_inverse[:size]] == old_inverse

    for vertex in range(size):
        assert new_inverse[size][vertex] == old_inverse[second][vertex]
        assert new_inverse[size + 1][vertex] == -old_inverse[first][vertex]
        assert new_inverse[size + 2][vertex] == -old_inverse[second][vertex]
        assert new_inverse[size + 3][vertex] == old_inverse[first][vertex]

    g_first = old_inverse[first][first]
    g_second = old_inverse[second][second]
    cross = old_inverse[first][second]
    expected = [
        [g_second, 1 - cross, -g_second, cross - 1],
        [1 - cross, g_first, cross, -g_first],
        [-g_second, cross, g_second, 1 - cross],
        [cross - 1, -g_first, 1 - cross, g_first],
    ]
    assert [row[size:] for row in new_inverse[size:]] == expected


def add_three_leaves(
    adjacency: list[list[int]], ports: tuple[int, int, int]
) -> list[list[int]]:
    size = len(adjacency)
    result = [row[:] + [0, 0, 0] for row in adjacency]
    result.extend([[0] * (size + 3) for _ in range(3)])
    for offset, port in enumerate(ports):
        leaf = size + offset
        result[port][leaf] = result[leaf][port] = 1
    return result


def main() -> None:
    same_class_values = {LOW: Counter(), HIGH: Counter()}
    same_class_edge_values = {LOW: Counter(), HIGH: Counter()}
    same_class_records: list[str] = []
    triple_inertias: Counter[tuple[int, int, int]] = Counter()
    line_signatures: Counter[int] = Counter()
    transport_cases = triple_cases = 0
    sharp_witness_seen = False

    for central in ((1, 3), (3, 1)):
        for connectors in ((1, 1), (1, 3), (3, 1), (3, 3)):
            adjacency, names, expected, edges = equality_base(central, connectors)
            matrix = shifted_signless(adjacency)
            matrix_inverse = inverse(matrix)
            classes = [expected[index] for index in range(len(adjacency))]
            base_inertia = inertia(matrix)
            assert signature(base_inertia) - 2 == 2
            check_same_class_invariant(matrix_inverse, classes, edges)

            for first in range(len(adjacency)):
                for second in range(first, len(adjacency)):
                    if classes[first] != classes[second]:
                        continue
                    value = matrix_inverse[first][second]
                    same_class_values[classes[first]][value] += 1
                    same_class_records.append(
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
                    same_class_edge_values[classes[first]][
                        matrix_inverse[first][second]
                    ] += 1

            for edge in edges:
                enlarged = four_subdivide(adjacency, edge)
                enlarged_inverse = inverse(shifted_signless(enlarged))
                check_transport(matrix_inverse, enlarged_inverse, edge)
                first, second = edge
                enlarged_classes = classes + [
                    classes[second],
                    classes[first],
                    classes[second],
                    classes[first],
                ]
                check_same_class_invariant(
                    enlarged_inverse, enlarged_classes, edge_list(enlarged)
                )
                transport_cases += 1

            for first in range(len(adjacency)):
                for second in range(first, len(adjacency)):
                    for third in range(second, len(adjacency)):
                        ports = (first, second, third)
                        response = [
                            [
                                Fraction(row == column, 2)
                                + matrix_inverse[ports[row]][ports[column]]
                                for column in range(3)
                            ]
                            for row in range(3)
                        ]
                        response_inertia = inertia(response)
                        assert response_inertia[0] >= 2
                        assert signature(response_inertia) >= 1

                        augmented = add_three_leaves(adjacency, ports)
                        augmented_inertia = inertia(shifted_signless(augmented))
                        assert (
                            signature(augmented_inertia) - signature(base_inertia)
                            == -signature(response_inertia)
                        )
                        line_signature = signature(augmented_inertia) - 2
                        assert line_signature <= 1
                        triple_inertias[response_inertia] += 1
                        line_signatures[line_signature] += 1
                        triple_cases += 1

                        if (
                            central == (1, 3)
                            and connectors == (1, 3)
                            and tuple(names[index] for index in ports)
                            == ("x", "S:1", "S:2")
                        ):
                            assert response == [
                                [2, 0, 0],
                                [0, 1, Fraction(3, 2)],
                                [0, Fraction(3, 2), 2],
                            ]
                            assert response_inertia == (2, 0, 1)
                            assert line_signature == 1
                            sharp_witness_seen = True

    assert transport_cases == 144
    assert triple_cases == 6664
    assert sharp_witness_seen
    assert same_class_values == {
        LOW: Counter({0: 242, LOW: 184, -LOW: 104}),
        HIGH: Counter({HIGH: 48, 0: 42, -HIGH: 24, 1: 8}),
    }
    assert same_class_edge_values == {
        LOW: Counter({LOW: 80}),
        HIGH: Counter({0: 24, 1: 8}),
    }
    assert triple_inertias == Counter(
        {(3, 0, 0): 6424, (2, 0, 1): 136, (2, 1, 0): 104}
    )
    assert line_signatures == Counter({-1: 6424, 1: 136, 0: 104})

    record_digest = hashlib.sha256(
        "\n".join(sorted(same_class_records)).encode()
    ).hexdigest()
    result = {
        "algorithm": "exact Green-function invariant and rank-three inertia",
        "base_assignments": 8,
        "four_subdivision_transport_cases": transport_cases,
        "line_signature_counts": {
            str(key): value for key, value in sorted(line_signatures.items())
        },
        "same_class_record_sha256": record_digest,
        "status": "VERIFIED",
        "triple_cases": triple_cases,
        "triple_inertia_counts": {
            ",".join(map(str, key)): value
            for key, value in sorted(triple_inertias.items())
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
