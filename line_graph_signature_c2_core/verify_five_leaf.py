#!/usr/bin/env python3
"""Exact proof computation for five simultaneous leaves on extremal c=2 cores.

The universal proof reduces the two full five-port branches to finite response
alphabets already established by the three-port theorem. Diagonal switching
normalizes the first response row, and triangle-constrained backtracking
enumerates every locally admissible 5-by-5 matrix. Singular compressed
branches are handled structurally; the only nontrivial four-dimensional
compression is independently over-enumerated from the three- and four-port
alphabets. Exact direct regressions check the general inertia identity.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
import platform

import verify_c2_core as c2
import verify_three_leaf as three
import verify_four_leaf as four


PortTuple = tuple[int, int, int, int, int]


def principal(matrix: c2.Matrix, indices: tuple[int, ...]) -> c2.Matrix:
    return [[matrix[i][j] for j in indices] for i in indices]


def check_nonsingular_full_alphabet() -> dict[str, object]:
    """Enumerate every switching-normalized five-port nonsingular response."""
    labels = (-9, -5, -3, -1, 1, 3, 5, 9)
    matrix = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        matrix[i][i] = 7
    remaining = list(combinations(range(1, 5), 2))
    distribution: Counter[tuple[int, int, int]] = Counter()
    complete = 0
    nodes = 0

    def triangle_allowed(i: int, j: int, k: int) -> bool:
        response = [
            [Fraction(matrix[x][y], 8) for y in (i, j, k)]
            for x in (i, j, k)
        ]
        return three.nonsingular_type(response) in three.NONSINGULAR_TYPES

    def recurse(position: int) -> None:
        nonlocal complete, nodes
        if position == len(remaining):
            inertia = c2.inertia(
                [[Fraction(value) for value in row] for row in matrix]
            )
            assert inertia[0] >= inertia[2]
            distribution[inertia] += 1
            complete += 1
            return
        i, j = remaining[position]
        for value in labels:
            matrix[i][j] = matrix[j][i] = value
            nodes += 1
            if all(
                not (matrix[k][i] and matrix[k][j]) or triangle_allowed(k, i, j)
                for k in range(5)
                if k not in (i, j)
            ):
                recurse(position + 1)
        matrix[i][j] = matrix[j][i] = 0

    # All off-diagonal entries are nonzero. A unique diagonal switching modulo
    # the global sign makes the first row positive.
    for star in product((1, 3, 5, 9), repeat=4):
        for j, value in enumerate(star, 1):
            matrix[0][j] = matrix[j][0] = value
        recurse(0)

    assert complete == 1_678
    assert distribution == Counter({
        (3, 0, 2): 552,
        (4, 0, 1): 1_045,
        (5, 0, 0): 81,
    })
    return {
        "nonsingular_full_backtracking_nodes": nodes,
        "nonsingular_full_matrices": complete,
        "nonsingular_full_inertias": sorted(distribution.items()),
    }


def check_singular_range_full_alphabet() -> dict[str, object]:
    """Enumerate every switching-normalized five-port all-range response."""
    labels = (-3, -1, 1, 3)
    remaining = list(combinations(range(1, 5), 2))
    distribution: Counter[tuple[int, int, int]] = Counter()
    complete = 0
    nodes = 0

    for diagonal in product((2, 4), repeat=5):
        matrix = [[0 for _ in range(5)] for _ in range(5)]
        for i in range(5):
            matrix[i][i] = diagonal[i]

        def triangle_allowed(i: int, j: int, k: int) -> bool:
            response = [
                [Fraction(matrix[x][y], 2) for y in (i, j, k)]
                for x in (i, j, k)
            ]
            return (
                three.singular_range_type(response)
                in three.EXPECTED_SINGULAR_RANGE_TYPES
            )

        def recurse(position: int) -> None:
            nonlocal complete, nodes
            if position == len(remaining):
                inertia = c2.inertia(
                    [[Fraction(value) for value in row] for row in matrix]
                )
                assert inertia[0] >= inertia[2]
                distribution[inertia] += 1
                complete += 1
                return
            i, j = remaining[position]
            for value in labels:
                matrix[i][j] = matrix[j][i] = value
                nodes += 1
                if all(
                    not (matrix[k][i] and matrix[k][j])
                    or triangle_allowed(k, i, j)
                    for k in range(5)
                    if k not in (i, j)
                ):
                    recurse(position + 1)
            matrix[i][j] = matrix[j][i] = 0

        for star in product((1, 3), repeat=4):
            for j, value in enumerate(star, 1):
                matrix[0][j] = matrix[j][0] = value
            recurse(0)

    assert complete == 2_160
    assert distribution == Counter({
        (3, 0, 2): 612,
        (3, 1, 1): 140,
        (4, 0, 1): 1_301,
        (4, 1, 0): 15,
        (5, 0, 0): 92,
    })
    return {
        "singular_range_full_backtracking_nodes": nodes,
        "singular_range_full_matrices": complete,
        "singular_range_full_inertias": sorted(distribution.items()),
    }


def check_singular_u2_alphabet() -> dict[str, object]:
    """Over-enumerate the u=2 compression from its principal response types."""
    distribution: Counter[tuple[int, int, int]] = Counter()
    complete = 0
    candidate_count = 0

    for diagonal in product((Fraction(1), Fraction(2)), repeat=3):
        for upper in product(
            (Fraction(-3, 2), Fraction(-1, 2), Fraction(1, 2), Fraction(3, 2)),
            repeat=3,
        ):
            defined = [[Fraction(0) for _ in range(3)] for _ in range(3)]
            for i in range(3):
                defined[i][i] = diagonal[i]
            for (i, j), value in zip(combinations(range(3), 2), upper):
                defined[i][j] = defined[j][i] = value
            if (
                three.singular_range_type(defined)
                not in three.EXPECTED_SINGULAR_RANGE_TYPES
            ):
                continue

            for cross in product((Fraction(-1), Fraction(0), Fraction(1)), repeat=3):
                candidate_count += 1
                matrix = [[Fraction(1), *cross]] + [
                    [cross[i], *defined[i]] for i in range(3)
                ]
                if not all(
                    four.mixed_type(principal(matrix, (0, i, j)))
                    in four.EXPECTED_MIXED_TYPES
                    for i, j in combinations(range(1, 4), 2)
                ):
                    continue
                inertia = c2.inertia(matrix)
                assert inertia[0] >= inertia[2]
                distribution[inertia] += 1
                complete += 1

    assert complete == 344
    assert distribution == Counter({
        (3, 0, 1): 216,
        (3, 1, 0): 28,
        (4, 0, 0): 100,
    })
    return {
        "singular_u2_candidates": candidate_count,
        "singular_u2_local_closures": complete,
        "singular_u2_local_inertias": sorted(distribution.items()),
    }


def orthogonal_basis(row: list[Fraction]) -> c2.Matrix:
    pivot = next(i for i, value in enumerate(row) if value)
    columns: list[list[Fraction]] = []
    for j in range(len(row)):
        if j == pivot:
            continue
        column = [Fraction(0) for _ in row]
        column[j] = 1
        column[pivot] = -row[j] / row[pivot]
        columns.append(column)
    return [
        [columns[j][i] for j in range(len(columns))]
        for i in range(len(row))
    ]


def effective_response(
    green: c2.Matrix,
    kernel: list[Fraction] | None,
    ports: PortTuple,
) -> tuple[c2.Matrix, str]:
    response = [
        [
            Fraction(i == j, 2) + green[ports[i]][ports[j]]
            for j in range(5)
        ]
        for i in range(5)
    ]
    if kernel is None:
        return response, "nonsingular"
    row = [kernel[port] for port in ports]
    undefined = sum(value != 0 for value in row)
    if not undefined:
        return response, "singular_all_range"
    return three.restrict(response, orthogonal_basis(row)), f"singular_u{undefined}"


def direct_delta(graph: c2.Graph, ports: PortTuple) -> int:
    matrix = c2.shifted_signless(graph)
    before = c2.matrix_signature(matrix)
    for port in ports:
        matrix[port][port] += 2
    return c2.matrix_signature(matrix) - before - 5


def direct_regression() -> dict[str, object]:
    distribution: Counter[int] = Counter()
    branches: set[str] = set()
    checks = 0
    graphs = 0

    for spec in ((4, 5, 1), (4, 5, 3), (5, 5, 1), (5, 5, 3)):
        base, _ = c2.dumbbell(*spec)
        cases: list[tuple[c2.Graph, int | None, list[int]]] = [
            (base, spec[0] if spec[0] == 4 else None, list(range(len(base))))
        ]
        for u, v in c2.edges(base):
            subdivided, internal = c2.subdivide_four(base, u, v)
            # This local set exercises every new path coordinate and both old
            # endpoints. Completeness comes from the response alphabets, not
            # from these direct regression samples.
            port_set = sorted({u, v, *internal})
            cases.append(
                (subdivided, spec[0] if spec[0] == 4 else None, port_set)
            )

        for graph, singular_cycle, port_set in cases:
            green, kernel = three.graph_response_data(graph, singular_cycle)
            for ports in combinations_with_replacement(port_set, 5):
                effective, branch = effective_response(green, kernel, ports)
                predicted = -c2.matrix_signature(effective)
                actual = direct_delta(graph, ports)
                assert predicted == actual <= 0
                distribution[actual] += 1
                branches.add(branch)
                checks += 1
            graphs += 1

    # The first boundary case from the complete one-subdivision search; its
    # ports are not all in one local regression set above.
    base, _ = c2.dumbbell(4, 5, 1)
    graph, _ = c2.subdivide_four(base, 0, 4)
    ports = (1, 9, 10, 11, 12)
    green, kernel = three.graph_response_data(graph, 4)
    effective, branch = effective_response(green, kernel, ports)
    predicted = -c2.matrix_signature(effective)
    actual = direct_delta(graph, ports)
    assert branch == "singular_u1"
    assert c2.inertia(effective) == (2, 0, 2)
    assert predicted == actual == 0
    distribution[actual] += 1
    branches.add(branch)
    checks += 1

    assert branches == {
        "nonsingular",
        "singular_all_range",
        "singular_u1",
        "singular_u2",
        "singular_u3",
        "singular_u4",
        "singular_u5",
    }
    return {
        "direct_branches": sorted(branches),
        "direct_checks": checks,
        "direct_delta_distribution": sorted(distribution.items()),
        "direct_graphs": graphs,
        "equality_witness": {
            "base_specification": (4, 5, 1),
            "effective_inertia": (2, 0, 2),
            "ports": ports,
            "subdivided_edge": (0, 4),
        },
    }


def main() -> None:
    record = {
        "arithmetic": "fractions.Fraction",
        "python": platform.python_version(),
        "switching_orbit_size": 16,
        **check_nonsingular_full_alphabet(),
        **check_singular_range_full_alphabet(),
        **check_singular_u2_alphabet(),
        **direct_regression(),
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(canonical.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
