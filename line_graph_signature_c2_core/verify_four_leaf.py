#!/usr/bin/env python3
"""Exact proof computation for four simultaneous leaves on extremal c=2 cores.

The proof is mostly structural.  A four-dimensional local-to-global inertia
lemma imports the complete three-port classification.  The only new graph
case is the singular branch with exactly two undefined and two defined port
coordinates.  Marked four-subdivision reduces that branch to the finite grid
checked below.  All arithmetic is exact ``fractions.Fraction`` arithmetic.
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


PortTuple = tuple[int, int, int, int]
MixedType = tuple[Fraction, Fraction, Fraction, Fraction, Fraction, int]


EXPECTED_MIXED_TYPES: set[MixedType] = {
    (Fraction(1), Fraction(1), Fraction(1, 2), Fraction(0), Fraction(0), 0),
    (Fraction(1), Fraction(2), Fraction(1, 2), Fraction(0), Fraction(0), 0),
    (Fraction(1), Fraction(2), Fraction(1, 2), Fraction(0), Fraction(1), 0),
    (Fraction(1), Fraction(2), Fraction(3, 2), Fraction(0), Fraction(0), 0),
    (Fraction(2), Fraction(2), Fraction(3, 2), Fraction(0), Fraction(0), 0),
    (Fraction(2), Fraction(2), Fraction(3, 2), Fraction(0), Fraction(1), 0),
    (Fraction(2), Fraction(2), Fraction(3, 2), Fraction(1), Fraction(1), 1),
}


def determinant_three(matrix: c2.Matrix) -> Fraction:
    assert len(matrix) == 3 and all(len(row) == 3 for row in matrix)
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def determinant_four(matrix: c2.Matrix) -> Fraction:
    assert len(matrix) == 4 and all(len(row) == 4 for row in matrix)
    total = Fraction(0)
    for column in range(4):
        minor = [
            [matrix[i][j] for j in range(4) if j != column]
            for i in range(1, 4)
        ]
        total += (-1) ** column * matrix[0][column] * determinant_three(minor)
    return total


def response_matrix(green: c2.Matrix, ports: PortTuple) -> c2.Matrix:
    return [
        [
            Fraction(i == j, 2) + green[ports[i]][ports[j]]
            for j in range(4)
        ]
        for i in range(4)
    ]


def orthogonal_basis(row: list[Fraction]) -> c2.Matrix:
    """Return a rational column basis for the orthogonal complement of row."""
    pivot = next(i for i, value in enumerate(row) if value)
    columns: list[list[Fraction]] = []
    for j in range(len(row)):
        if j == pivot:
            continue
        column = [Fraction(0) for _ in row]
        column[j] = 1
        column[pivot] = -row[j] / row[pivot]
        assert sum(row[i] * column[i] for i in range(len(row))) == 0
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
    response = response_matrix(green, ports)
    if kernel is None:
        return response, "nonsingular"
    b = [kernel[port] for port in ports]
    undefined = sum(value != 0 for value in b)
    if not undefined:
        return response, "singular_all_range"
    return three.restrict(response, orthogonal_basis(b)), f"singular_u{undefined}"


def predicted_delta(
    green: c2.Matrix,
    kernel: list[Fraction] | None,
    ports: PortTuple,
) -> tuple[int, str, c2.Matrix]:
    effective, branch = effective_response(green, kernel, ports)
    return -c2.matrix_signature(effective), branch, effective


def direct_delta(g: c2.Graph, ports: PortTuple) -> int:
    matrix = c2.shifted_signless(g)
    before = c2.matrix_signature(matrix)
    for port in ports:
        matrix[port][port] += 2
    return c2.matrix_signature(matrix) - before - 4


def check_gap_bounds() -> int:
    checks = 0
    for interior_marks in range(5):
        gap_count = interior_marks + 1
        for gaps in product(range(1, 5), repeat=gap_count):
            total = sum(gaps)
            if interior_marks and total % 4 == 1:
                assert total in (5, 9, 13, 17)
                checks += 1
            if total % 4 == 0:
                assert total in (4, 8, 12, 16, 20)
                checks += 1
            if total % 2 == 1:
                assert total in tuple(range(1, 20, 2))
                checks += 1
    # An unmarked simple cycle stops at C5 or C4 rather than at a loop.
    return checks + 2


def principal_three(matrix: c2.Matrix, drop: int) -> c2.Matrix:
    indices = [i for i in range(4) if i != drop]
    return [[matrix[i][j] for j in indices] for i in indices]


def check_local_to_global_alphabets() -> dict[str, object]:
    """Audit every locally admissible four-port matrix over both alphabets.

    The human proof uses only interlacing and an adjugate argument.  This
    calculation independently checks its conclusion on the two exact response
    alphabets furnished by the three-port classification.
    """
    edge_positions = list(combinations(range(4), 2))
    records: dict[str, object] = {}

    nonsingular_distribution: Counter[tuple[int, int, int]] = Counter()
    nonsingular_count = 0
    for upper in product((-9, -5, -3, -1, 1, 3, 5, 9), repeat=6):
        matrix = [
            [Fraction(7 if i == j else 0) for j in range(4)]
            for i in range(4)
        ]
        for (i, j), value in zip(edge_positions, upper):
            matrix[i][j] = matrix[j][i] = Fraction(value)
        if not all(
            three.nonsingular_type(
                [[value / 8 for value in row] for row in principal_three(matrix, d)]
            )
            in three.NONSINGULAR_TYPES
            for d in range(4)
        ):
            continue
        inertia = c2.inertia(matrix)
        assert inertia[0] >= inertia[2]
        nonsingular_distribution[inertia] += 1
        nonsingular_count += 1

    singular_distribution: Counter[tuple[int, int, int]] = Counter()
    singular_count = 0
    for diagonal in product((2, 4), repeat=4):
        for upper in product((-3, -1, 1, 3), repeat=6):
            integer = [[0 for _ in range(4)] for _ in range(4)]
            for i in range(4):
                integer[i][i] = diagonal[i]
            for (i, j), value in zip(edge_positions, upper):
                integer[i][j] = integer[j][i] = value
            matrix = [[Fraction(value, 2) for value in row] for row in integer]
            if not all(
                three.singular_range_type(principal_three(matrix, d))
                in three.EXPECTED_SINGULAR_RANGE_TYPES
                for d in range(4)
            ):
                continue
            inertia = c2.inertia(matrix)
            assert inertia[0] >= inertia[2]
            singular_distribution[inertia] += 1
            singular_count += 1

    assert nonsingular_count == 1328
    assert singular_count == 1720
    records["nonsingular_local_closures"] = nonsingular_count
    records["nonsingular_local_inertias"] = sorted(nonsingular_distribution.items())
    records["singular_range_local_closures"] = singular_count
    records["singular_range_local_inertias"] = sorted(singular_distribution.items())
    return records


def mixed_type(matrix: c2.Matrix) -> MixedType:
    """Canonical type of [[1,h1,h2],[h1,a,q],[h2,q,d]]."""
    assert matrix[0][0] == 1
    a, d = matrix[1][1], matrix[2][2]
    q = matrix[1][2]
    h1, h2 = matrix[0][1], matrix[0][2]
    sign = 0 if not q * h1 * h2 else (1 if q * h1 * h2 > 0 else -1)
    key = (a, d, abs(q), abs(h1), abs(h2), sign)
    swapped = (d, a, abs(q), abs(h2), abs(h1), sign)
    return min(key, swapped)


def mixed_matrix(
    green: c2.Matrix,
    kernel: list[Fraction],
    undefined: tuple[int, int],
    defined: tuple[int, int],
) -> c2.Matrix:
    u1, u2 = undefined
    d1, d2 = defined
    e1, e2 = kernel[u1], kernel[u2]
    # w=(e2,-e1,0,0) is kernel-orthogonal and has squared norm two.
    h1 = e2 * green[u1][d1] - e1 * green[u2][d1]
    h2 = e2 * green[u1][d2] - e1 * green[u2][d2]
    return [
        [Fraction(1), h1, h2],
        [h1, Fraction(1, 2) + green[d1][d1], green[d1][d2]],
        [h2, green[d1][d2], Fraction(1, 2) + green[d2][d2]],
    ]


def complete_mixed_census() -> dict[str, object]:
    """Check the only new singular branch on the complete four-mark grid."""
    graph_count = 0
    case_count = 0
    types: set[MixedType] = set()
    distribution: Counter[tuple[int, int, int]] = Counter()

    for a in (4, 8, 12, 16, 20):
        for b in (5, 9, 13, 17):
            for bridge in range(1, 20, 2):
                graph, _ = c2.dumbbell(a, b, bridge)
                assert c2.line_signature_c2(graph) == 1
                green, kernel_or_none = three.graph_response_data(graph, a)
                assert kernel_or_none is not None
                kernel = kernel_or_none
                undefined_ports = [i for i, value in enumerate(kernel) if value]
                defined_ports = [i for i, value in enumerate(kernel) if not value]
                for undefined in combinations_with_replacement(undefined_ports, 2):
                    for defined in combinations_with_replacement(defined_ports, 2):
                        matrix = mixed_matrix(green, kernel, undefined, defined)
                        inertia = c2.inertia(matrix)
                        assert inertia[0] >= inertia[2]
                        assert determinant_three(matrix) != 0
                        types.add(mixed_type(matrix))
                        distribution[inertia] += 1
                        case_count += 1
                graph_count += 1

    assert graph_count == 200
    assert case_count == 2_185_340
    assert types == EXPECTED_MIXED_TYPES
    return {
        "mixed_branch_cases": case_count,
        "mixed_branch_graphs": graph_count,
        "mixed_branch_inertias": sorted(distribution.items()),
        "mixed_branch_types": len(types),
    }


def direct_regression() -> dict[str, object]:
    distribution: Counter[int] = Counter()
    branches: set[str] = set()
    checks = 0
    graphs = 0
    mixed_types: set[MixedType] = set()

    for spec in ((4, 5, 1), (4, 5, 3), (5, 5, 1), (5, 5, 3)):
        base, bridge_path = c2.dumbbell(*spec)
        # Every base placement is checked.  On each one-edge subdivision, the
        # four new vertices, the replaced endpoints, and the two dumbbell roots
        # form a targeted port set that exercises marked subdivision locally.
        cases: list[tuple[c2.Graph, int | None, list[int]]] = [
            (base, spec[0] if spec[0] == 4 else None, list(range(len(base))))
        ]
        for u, v in c2.edges(base):
            subdivided, internal = c2.subdivide_four(base, u, v)
            port_set = sorted({u, v, bridge_path[0], bridge_path[-1], *internal})
            cases.append(
                (subdivided, spec[0] if spec[0] == 4 else None, port_set)
            )
        for graph, singular_cycle, port_set in cases:
            green, kernel = three.graph_response_data(graph, singular_cycle)
            for ports in combinations_with_replacement(port_set, 4):
                predicted, branch, effective = predicted_delta(green, kernel, ports)
                actual = direct_delta(graph, ports)
                assert predicted == actual <= 0
                distribution[actual] += 1
                branches.add(branch)
                checks += 1
                if branch == "singular_u2":
                    undefined = tuple(port for port in ports if kernel[port])
                    defined = tuple(port for port in ports if not kernel[port])
                    mixed_types.add(mixed_type(mixed_matrix(green, kernel, undefined, defined)))
            graphs += 1

    assert branches == {
        "nonsingular",
        "singular_all_range",
        "singular_u1",
        "singular_u2",
        "singular_u3",
        "singular_u4",
    }
    assert mixed_types == EXPECTED_MIXED_TYPES
    return {
        "direct_branches": sorted(branches),
        "direct_delta_distribution": sorted(distribution.items()),
        "direct_graphs": graphs,
        "direct_quadruples": checks,
        "direct_mixed_type_coverage": len(mixed_types),
    }


def check_expected_mixed_table() -> list[tuple[object, ...]]:
    rows = []
    for a, d, q, h1, h2, sign in sorted(EXPECTED_MIXED_TYPES):
        # When the triangle product is positive all three nonzero entries may
        # be made positive; if it is zero the nonzero graph is a forest and
        # signs may also be removed by diagonal switching.
        assert sign in (0, 1)
        matrix = [
            [Fraction(1), h1, h2],
            [h1, a, q],
            [h2, q, d],
        ]
        inertia = c2.inertia(matrix)
        assert inertia[0] >= inertia[2]
        rows.append(((a, d, q, h1, h2, sign), determinant_three(matrix), inertia))
    return rows


def main() -> None:
    record = {
        "arithmetic": "fractions.Fraction",
        "gap_reduction_checks": check_gap_bounds(),
        "mixed_type_table": check_expected_mixed_table(),
        "python": platform.python_version(),
        **check_local_to_global_alphabets(),
        **complete_mixed_census(),
        **direct_regression(),
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), default=str)
    print(json.dumps(record, sort_keys=True, indent=2, default=str))
    print("result_sha256=" + hashlib.sha256(canonical.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
