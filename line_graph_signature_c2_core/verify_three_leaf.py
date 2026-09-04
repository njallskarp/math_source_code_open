#!/usr/bin/env python3
"""Exact proof computation for three simultaneous leaves on extremal c=2 cores.

The mathematical proof reduces every marked dumbbell to the length grids below
by smoothing leaf-free four-subdivisions.  This checker exhausts those grids
with exact Fraction arithmetic, verifies the effective response criterion, and
performs a direct full-matrix regression on the four bases and all of their
one-edge four-subdivisions.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations_with_replacement, permutations, product
import json
import platform

import verify_c2_core as c2
from verify_two_leaf import inverse


PortTriple = tuple[int, int, int]


NONSINGULAR_TYPES = {
    ((1, 1, 3), 1),
    ((1, 1, 5), -1),
    ((1, 3, 9), 1),
    ((3, 3, 3), 1),
    ((3, 3, 5), -1),
    ((3, 5, 5), 1),
    ((3, 9, 9), 1),
}


SINGULAR_RANGE_REPRESENTATIVES = (
    ((2, -3, -3), (-3, 4, 3), (-3, 3, 4)),
    ((2, -3, -1), (-3, 4, 1), (-1, 1, 2)),
    ((2, -3, -1), (-3, 4, 3), (-1, 3, 2)),
    ((2, -3, -1), (-3, 4, 3), (-1, 3, 4)),
    ((2, -1, -1), (-1, 2, -1), (-1, -1, 2)),
    ((2, -1, -1), (-1, 2, -1), (-1, -1, 4)),
    ((2, -1, -1), (-1, 2, 1), (-1, 1, 2)),
    ((2, -1, -1), (-1, 2, 1), (-1, 1, 4)),
    ((2, -1, -1), (-1, 4, 3), (-1, 3, 4)),
    ((4, -3, -3), (-3, 4, 3), (-3, 3, 4)),
)


def matmul(left: c2.Matrix, right: c2.Matrix) -> c2.Matrix:
    if not left:
        return []
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix: c2.Matrix) -> c2.Matrix:
    return [list(column) for column in zip(*matrix)]


def response_matrix(green: c2.Matrix, ports: PortTriple) -> c2.Matrix:
    return [
        [
            Fraction(i == j, 2) + green[ports[i]][ports[j]]
            for j in range(3)
        ]
        for i in range(3)
    ]


def orthogonal_basis(row: list[Fraction]) -> c2.Matrix:
    """Return a 3-by-2 rational basis matrix for the orthogonal complement."""
    pivot = next(i for i, value in enumerate(row) if value)
    columns: list[list[Fraction]] = []
    for j in range(3):
        if j == pivot:
            continue
        column = [Fraction(0) for _ in range(3)]
        column[j] = 1
        column[pivot] = -row[j] / row[pivot]
        assert sum(row[i] * column[i] for i in range(3)) == 0
        columns.append(column)
    return [[columns[j][i] for j in range(2)] for i in range(3)]


def restrict(matrix: c2.Matrix, basis: c2.Matrix) -> c2.Matrix:
    return matmul(transpose(basis), matmul(matrix, basis))


def nonsingular_type(matrix: c2.Matrix) -> tuple[tuple[int, int, int], int]:
    assert all(matrix[i][i] == Fraction(7, 8) for i in range(3))
    off_diagonal = [matrix[0][1], matrix[0][2], matrix[1][2]]
    assert all(value and (8 * value).denominator == 1 for value in off_diagonal)
    magnitudes = tuple(sorted(abs(int(8 * value)) for value in off_diagonal))
    sign = 1 if off_diagonal[0] * off_diagonal[1] * off_diagonal[2] > 0 else -1
    return magnitudes, sign


def singular_range_type(matrix: c2.Matrix) -> tuple[object, ...]:
    scaled = [[2 * matrix[i][j] for j in range(3)] for i in range(3)]
    assert all(value.denominator == 1 for row in scaled for value in row)
    integer = [[int(value) for value in row] for row in scaled]
    keys = []
    for order in permutations(range(3)):
        diagonal = tuple(integer[order[i]][order[i]] for i in range(3))
        edges = tuple(
            abs(integer[order[i]][order[j]])
            for i, j in ((0, 1), (0, 2), (1, 2))
        )
        edge_product = (
            integer[order[0]][order[1]]
            * integer[order[0]][order[2]]
            * integer[order[1]][order[2]]
        )
        assert edge_product
        keys.append((diagonal, edges, 1 if edge_product > 0 else -1))
    return min(keys)


EXPECTED_SINGULAR_RANGE_TYPES = {
    singular_range_type([[Fraction(value, 2) for value in row] for row in matrix])
    for matrix in SINGULAR_RANGE_REPRESENTATIVES
}


def graph_response_data(
    g: c2.Graph, singular_cycle_length: int | None
) -> tuple[c2.Matrix, list[Fraction] | None]:
    matrix = c2.shifted_signless(g)
    if singular_cycle_length is None:
        assert c2.inertia(matrix)[1] == 0
        return inverse(matrix), None
    z = one_dimensional_kernel_vector(matrix)
    assert any(z)
    assert all(
        sum(matrix[i][j] * z[j] for j in range(len(g))) == 0
        for i in range(len(g))
    )
    lifted = [
        [matrix[i][j] + z[i] * z[j] for j in range(len(g))]
        for i in range(len(g))
    ]
    return inverse(lifted), z


def one_dimensional_kernel_vector(matrix: c2.Matrix) -> list[Fraction]:
    """Return a canonical exact generator, asserting nullity exactly one."""
    reduced = [row[:] for row in matrix]
    row = 0
    pivots: list[int] = []
    for column in range(len(matrix)):
        pivot = next(
            (i for i in range(row, len(matrix)) if reduced[i][column]), None
        )
        if pivot is None:
            continue
        reduced[row], reduced[pivot] = reduced[pivot], reduced[row]
        scale = reduced[row][column]
        reduced[row] = [value / scale for value in reduced[row]]
        for i in range(len(matrix)):
            if i == row or not reduced[i][column]:
                continue
            scale = reduced[i][column]
            reduced[i] = [
                reduced[i][j] - scale * reduced[row][j]
                for j in range(len(matrix))
            ]
        pivots.append(column)
        row += 1
    free = [column for column in range(len(matrix)) if column not in pivots]
    assert len(free) == 1
    vector = [Fraction(0) for _ in matrix]
    vector[free[0]] = 1
    for i in range(len(pivots) - 1, -1, -1):
        column = pivots[i]
        vector[column] = -sum(
            reduced[i][j] * vector[j] for j in range(column + 1, len(matrix))
        )
    assert all(
        sum(matrix[i][j] * vector[j] for j in range(len(matrix))) == 0
        for i in range(len(matrix))
    )
    return vector


def predicted_delta(
    green: c2.Matrix,
    kernel: list[Fraction] | None,
    ports: PortTriple,
) -> tuple[int, str, c2.Matrix]:
    response = response_matrix(green, ports)
    if kernel is None:
        return -c2.matrix_signature(response), "nonsingular", response

    kernel_row = [kernel[port] for port in ports]
    if not any(kernel_row):
        return -c2.matrix_signature(response), "singular_all_range", response

    basis = orthogonal_basis(kernel_row)
    effective = restrict(response, basis)
    response_part = [
        [green[ports[i]][ports[j]] for j in range(3)] for i in range(3)
    ]
    if all(kernel_row):
        # The cycle-image lemma says the range response vanishes identically
        # on the kernel-orthogonal port subspace.
        assert restrict(response_part, basis) == [
            [Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(0)],
        ]
        branch = "singular_all_undefined"
    else:
        defined_index = next(i for i, value in enumerate(kernel_row) if not value)
        assert response[defined_index][defined_index] > 0
        branch = "singular_mixed"
    return -c2.matrix_signature(effective), branch, effective


def direct_delta(g: c2.Graph, ports: PortTriple) -> int:
    matrix = c2.shifted_signless(g)
    before = c2.matrix_signature(matrix)
    for port in ports:
        matrix[port][port] += 2
    return c2.matrix_signature(matrix) - before - 3


def check_gap_bounds() -> int:
    checks = 0
    for interior_marks in range(4):
        arc_count = interior_marks + 1
        for gaps in product(range(1, 5), repeat=arc_count):
            total = sum(gaps)
            if interior_marks and total % 4 == 1:
                assert total in (5, 9, 13)
                checks += 1
            if total % 4 == 0:
                assert total in (4, 8, 12, 16)
                checks += 1
            if total % 2 == 1:
                assert total in tuple(range(1, 16, 2))
                checks += 1
    # An unmarked simple cycle stops at C5 or C4 rather than at a loop.
    checks += 2
    return checks


def complete_marked_census() -> dict[str, object]:
    distribution: Counter[int] = Counter()
    branches: Counter[str] = Counter()
    nonsingular_types: set[tuple[tuple[int, int, int], int]] = set()
    singular_range_types: set[tuple[object, ...]] = set()
    graph_count = 0
    triple_count = 0

    specifications: list[tuple[int, int, int, int | None]] = []
    for a in (5, 9, 13):
        for b in (5, 9, 13):
            for bridge in range(1, 16, 2):
                specifications.append((a, b, bridge, None))
    for a in (4, 8, 12, 16):
        for b in (5, 9, 13):
            for bridge in range(1, 16, 2):
                specifications.append((a, b, bridge, a))

    for a, b, bridge, singular_cycle in specifications:
        g, _ = c2.dumbbell(a, b, bridge)
        assert c2.line_signature_c2(g) == 1
        green, kernel = graph_response_data(g, singular_cycle)
        for ports in combinations_with_replacement(range(len(g)), 3):
            delta, branch, effective = predicted_delta(green, kernel, ports)
            assert delta <= 0
            distribution[delta] += 1
            branches[branch] += 1
            triple_count += 1
            if branch == "nonsingular":
                nonsingular_types.add(nonsingular_type(effective))
            elif branch == "singular_all_range":
                singular_range_types.add(singular_range_type(effective))
        graph_count += 1

    assert nonsingular_types == NONSINGULAR_TYPES
    assert singular_range_types == EXPECTED_SINGULAR_RANGE_TYPES
    return {
        "branch_counts": sorted(branches.items()),
        "delta_distribution": sorted(distribution.items()),
        "marked_graphs": graph_count,
        "marked_triples": triple_count,
        "nonsingular_response_types": len(nonsingular_types),
        "singular_all_range_types": len(singular_range_types),
    }


def direct_regression() -> dict[str, object]:
    distribution: Counter[int] = Counter()
    checks = 0
    graph_count = 0
    base_branches: set[str] = set()
    base_nonsingular_types: set[tuple[tuple[int, int, int], int]] = set()
    base_singular_range_types: set[tuple[object, ...]] = set()
    for spec in ((4, 5, 1), (4, 5, 3), (5, 5, 1), (5, 5, 3)):
        base, _ = c2.dumbbell(*spec)
        cases = [(base, spec[0] if spec[0] == 4 else None, True)]
        cases.extend(
            (
                c2.subdivide_four(base, u, v)[0],
                spec[0] if spec[0] == 4 else None,
                False,
            )
            for u, v in c2.edges(base)
        )
        for g, singular_cycle, is_base in cases:
            green, kernel = graph_response_data(g, singular_cycle)
            for ports in combinations_with_replacement(range(len(g)), 3):
                predicted, branch, effective = predicted_delta(green, kernel, ports)
                actual = direct_delta(g, ports)
                assert predicted == actual <= 0
                distribution[actual] += 1
                checks += 1
                if is_base:
                    base_branches.add(branch)
                    if branch == "nonsingular":
                        base_nonsingular_types.add(nonsingular_type(effective))
                    elif branch == "singular_all_range":
                        base_singular_range_types.add(singular_range_type(effective))
            graph_count += 1
    assert base_branches == {
        "nonsingular",
        "singular_all_range",
        "singular_all_undefined",
        "singular_mixed",
    }
    assert base_nonsingular_types == NONSINGULAR_TYPES
    assert base_singular_range_types == EXPECTED_SINGULAR_RANGE_TYPES
    return {
        "direct_base_response_type_coverage": [
            len(base_nonsingular_types),
            len(base_singular_range_types),
        ],
        "direct_delta_distribution": sorted(distribution.items()),
        "direct_graphs": graph_count,
        "direct_triples": checks,
    }


def main() -> None:
    record = {
        "arithmetic": "fractions.Fraction",
        "gap_reduction_checks": check_gap_bounds(),
        "python": platform.python_version(),
        **complete_marked_census(),
        **direct_regression(),
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(canonical.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
