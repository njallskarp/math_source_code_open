#!/usr/bin/env python3
"""Exact checks for cyclomatic-two line-graph core stability.

The program uses only Python's arbitrary-precision integers and Fraction.
It is corroborative: the accompanying proof supplies the four-subdivision
congruence and the finite topological reduction.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json
import platform


Matrix = list[list[Fraction]]
Graph = list[list[int]]  # symmetric adjacency multiplicities


def empty_graph(n: int) -> Graph:
    return [[0 for _ in range(n)] for _ in range(n)]


def add_vertex(g: Graph) -> int:
    n = len(g)
    for row in g:
        row.append(0)
    g.append([0 for _ in range(n + 1)])
    return n


def add_edge(g: Graph, u: int, v: int, multiplicity: int = 1) -> None:
    assert u != v and multiplicity > 0
    g[u][v] += multiplicity
    g[v][u] += multiplicity


def cycle_at_root(g: Graph, root: int, length: int) -> None:
    assert length >= 3
    last = root
    for _ in range(length - 1):
        new = add_vertex(g)
        add_edge(g, last, new)
        last = new
    add_edge(g, last, root)


def rose(a: int, b: int) -> Graph:
    g = empty_graph(1)
    cycle_at_root(g, 0, a)
    cycle_at_root(g, 0, b)
    return g


def theta(lengths: tuple[int, int, int]) -> Graph:
    """May have parallel terminal edges after reduction modulo four."""
    g = empty_graph(2)
    for length in lengths:
        assert length >= 1
        last = 0
        for _ in range(length - 1):
            new = add_vertex(g)
            add_edge(g, last, new)
            last = new
        add_edge(g, last, 1)
    return g


def dumbbell(a: int, b: int, bridge_length: int) -> tuple[Graph, list[int]]:
    assert a >= 3 and b >= 3 and bridge_length >= 1
    g = empty_graph(1)
    cycle_at_root(g, 0, a)
    path = [0]
    last = 0
    for _ in range(bridge_length):
        new = add_vertex(g)
        add_edge(g, last, new)
        path.append(new)
        last = new
    cycle_at_root(g, last, b)
    return g, path


def shifted_signless(g: Graph) -> Matrix:
    n = len(g)
    return [
        [
            Fraction(sum(g[i]) - 2 if i == j else g[i][j])
            for j in range(n)
        ]
        for i in range(n)
    ]


def inertia(matrix: Matrix) -> tuple[int, int, int]:
    """Exact symmetric congruence elimination, returning (positive,zero,negative)."""
    a = [row[:] for row in matrix]
    positive = zero = negative = 0
    while a:
        n = len(a)
        pivot = next((i for i in range(n) if a[i][i] != 0), None)
        if pivot is not None:
            order = [pivot] + [i for i in range(n) if i != pivot]
            a = [[a[i][j] for j in order] for i in order]
            d = a[0][0]
            if d > 0:
                positive += 1
            else:
                negative += 1
            a = [
                [a[i][j] - a[i][0] * a[0][j] / d for j in range(1, n)]
                for i in range(1, n)
            ]
            continue

        pair = next(
            ((i, j) for i in range(n) for j in range(i + 1, n) if a[i][j]),
            None,
        )
        if pair is None:
            zero += n
            break
        i, j = pair
        order = [i, j] + [k for k in range(n) if k not in pair]
        a = [[a[r][s] for s in order] for r in order]
        d = a[0][1]
        positive += 1
        negative += 1
        a = [
            [
                a[r][s]
                - (a[r][0] * a[1][s] + a[r][1] * a[0][s]) / d
                for s in range(2, n)
            ]
            for r in range(2, n)
        ]
    return positive, zero, negative


def matrix_signature(matrix: Matrix) -> int:
    p, _, n = inertia(matrix)
    return p - n


def line_signature_c2(g: Graph) -> int:
    # For c=2, s(L(G)) = sig(Q(G)-2I)-c+1 = sig(M)-1.
    return matrix_signature(shifted_signless(g)) - 1


def coordinate_response(matrix: Matrix, x: int) -> Fraction | None:
    """Return y_x for My=e_x, or None when e_x is outside col(M)."""
    n = len(matrix)
    a = [matrix[i][:] + [Fraction(i == x)] for i in range(n)]
    pivot_row = 0
    pivot_columns: list[int] = []
    for column in range(n):
        pivot = next((r for r in range(pivot_row, n) if a[r][column]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        d = a[pivot_row][column]
        a[pivot_row] = [v / d for v in a[pivot_row]]
        for r in range(n):
            if r == pivot_row or not a[r][column]:
                continue
            q = a[r][column]
            a[r] = [a[r][j] - q * a[pivot_row][j] for j in range(n + 1)]
        pivot_columns.append(column)
        pivot_row += 1
    if any(all(row[j] == 0 for j in range(n)) and row[n] for row in a):
        return None
    solution = [Fraction(0) for _ in range(n)]
    for r, column in enumerate(pivot_columns):
        solution[column] = a[r][n]
    return solution[x]


def all_responses(g: Graph) -> list[Fraction | None]:
    m = shifted_signless(g)
    return [coordinate_response(m, x) for x in range(len(g))]


def add_leaf(g: Graph, x: int) -> Graph:
    h = [row[:] for row in g]
    new = add_vertex(h)
    add_edge(h, x, new)
    return h


def subdivide_four(g: Graph, u: int, v: int) -> tuple[Graph, list[int]]:
    assert g[u][v] > 0
    h = [row[:] for row in g]
    h[u][v] -= 1
    h[v][u] -= 1
    path = []
    last = u
    for _ in range(4):
        new = add_vertex(h)
        path.append(new)
        add_edge(h, last, new)
        last = new
    add_edge(h, last, v)
    return h, path


def edges(g: Graph) -> list[tuple[int, int]]:
    return [(i, j) for i in range(len(g)) for j in range(i + 1, len(g)) if g[i][j]]


def text_fraction(value: Fraction | None) -> str:
    return "undefined" if value is None else str(value)


def main() -> None:
    cycle_representative = {0: 4, 1: 5, 2: 6, 3: 3}
    path_representative = {0: 4, 1: 1, 2: 2, 3: 3}

    rose_distribution = Counter()
    for a in range(4):
        for b in range(4):
            rose_distribution[line_signature_c2(rose(cycle_representative[a], cycle_representative[b]))] += 1
    assert max(rose_distribution) <= 0

    theta_distribution = Counter()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                g = theta(
                    (
                        path_representative[a],
                        path_representative[b],
                        path_representative[c],
                    )
                )
                theta_distribution[line_signature_c2(g)] += 1
    assert max(theta_distribution) <= 0

    expected_even = (
        (0, 0, -1, -1),
        (0, 0, -1, 0),
        (-1, -1, -1, -1),
        (-1, 0, -1, -2),
    )
    expected_odd = (
        (0, 1, 0, -1),
        (1, 1, 0, -1),
        (0, 0, -1, -2),
        (-1, -1, -2, -2),
    )
    dumbbell_tables = []
    for bridge_residue in range(4):
        table = tuple(
            tuple(
                line_signature_c2(
                    dumbbell(
                        cycle_representative[a],
                        cycle_representative[b],
                        path_representative[bridge_residue],
                    )[0]
                )
                for b in range(4)
            )
            for a in range(4)
        )
        assert table == (expected_odd if bridge_residue % 2 else expected_even)
        dumbbell_tables.append(table)

    base_specs = (
        (4, 5, 1),
        (4, 5, 3),
        (5, 5, 1),
        (5, 5, 3),
    )
    base_records = []
    subdivision_checks = 0
    leaf_checks = 0
    for spec in base_specs:
        g, _ = dumbbell(*spec)
        assert line_signature_c2(g) == 1
        responses = all_responses(g)
        defined = sorted({text_fraction(v) for v in responses if v is not None})
        undefined = sum(v is None for v in responses)
        expected_defined = ["1/2", "3/2"] if spec[0] == 4 else ["3/8"]
        assert defined == expected_defined
        assert all(v is None or v >= Fraction(-1, 2) for v in responses)
        for x in range(len(g)):
            assert line_signature_c2(add_leaf(g, x)) <= 1
            leaf_checks += 1

        for u, v in edges(g):
            h, internal = subdivide_four(g, u, v)
            old = all_responses(g)
            new = all_responses(h)
            assert inertia(shifted_signless(h)) == (
                inertia(shifted_signless(g))[0] + 2,
                inertia(shifted_signless(g))[1],
                inertia(shifted_signless(g))[2] + 2,
            )
            assert new[: len(g)] == old
            assert [new[w] for w in internal] == [old[v], old[u], old[v], old[u]]
            assert line_signature_c2(h) == 1
            for x in range(len(h)):
                assert line_signature_c2(add_leaf(h, x)) <= 1
                leaf_checks += 1
            subdivision_checks += 1
        base_records.append(
            {
                "lengths": spec,
                "defined_responses": defined,
                "undefined_vertices": undefined,
            }
        )

    # The scope is sharp: the non-extremal C4--C5 dumbbell with a two-edge
    # bridge has response -3/4 at the internal bridge vertex, and a leaf raises
    # its line-graph signature from 0 to 1.
    witness, bridge_path = dumbbell(4, 5, 2)
    internal = bridge_path[1]
    witness_response = coordinate_response(shifted_signless(witness), internal)
    assert witness_response == Fraction(-3, 4)
    assert line_signature_c2(witness) == 0
    assert line_signature_c2(add_leaf(witness, internal)) == 1

    record = {
        "arithmetic": "fractions.Fraction",
        "base_responses": base_records,
        "dumbbell_even_bridge_table": expected_even,
        "dumbbell_odd_bridge_table": expected_odd,
        "leaf_checks": leaf_checks,
        "nonextremal_sharpness_witness": {
            "lengths": [4, 5, 2],
            "response": str(witness_response),
            "signature_before_after_leaf": [0, 1],
        },
        "python": platform.python_version(),
        "rose_reduced_classes": 16,
        "rose_signature_distribution": sorted(rose_distribution.items()),
        "subdivision_checks": subdivision_checks,
        "theta_reduced_classes": 64,
        "theta_signature_distribution": sorted(theta_distribution.items()),
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(canonical.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
