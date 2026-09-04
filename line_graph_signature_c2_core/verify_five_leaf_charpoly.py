#!/usr/bin/env python3
"""Independent exact audit for five-leaf stability.

Requires SymPy 1.14.x. This script imports no response or inertia routine from
the production checker. It independently enumerates the two full response
alphabets, computes every 5-by-5 inertia from its characteristic polynomial
over ZZ[x], and constructs line graphs directly for every five-leaf placement
on the four minimal cores plus the sharp one-subdivision equality witness.
"""

from __future__ import annotations

from collections import Counter
import hashlib
from itertools import combinations, combinations_with_replacement, permutations, product
import json

import sympy
from sympy import Matrix, Poly, Symbol, cancel

import verify_c2_core as c2


X = Symbol("x")

NS_TRIANGLES = {
    ((1, 1, 3), 1),
    ((1, 1, 5), -1),
    ((1, 3, 9), 1),
    ((3, 3, 3), 1),
    ((3, 3, 5), -1),
    ((3, 5, 5), 1),
    ((3, 9, 9), 1),
}

SINGULAR_REPRESENTATIVES = (
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


def sign_variations(coefficients: list[sympy.Expr]) -> int:
    signs = [
        1 if coefficient > 0 else -1
        for coefficient in coefficients
        if coefficient
    ]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def charpoly_inertia(integer: list[list[int]]) -> tuple[int, int, int]:
    matrix = Matrix(integer)
    zero = matrix.rows - matrix.rank()
    characteristic = matrix.charpoly(X).as_expr()
    nonzero = Poly(cancel(characteristic / X**zero), X, domain="ZZ")
    positive = sign_variations(nonzero.all_coeffs())
    reflected = Poly(nonzero.as_expr().subs(X, -X), X, domain="ZZ")
    negative = sign_variations(reflected.all_coeffs())
    assert positive + zero + negative == matrix.rows
    return positive, zero, negative


def nonsingular_triangle_key(
    matrix: list[list[int]], vertices: tuple[int, int, int]
) -> tuple[tuple[int, int, int], int]:
    i, j, k = vertices
    edges = (matrix[i][j], matrix[i][k], matrix[j][k])
    magnitudes = tuple(sorted(abs(value) for value in edges))
    return magnitudes, (1 if edges[0] * edges[1] * edges[2] > 0 else -1)


def singular_triangle_key(integer: tuple[tuple[int, ...], ...]) -> tuple[object, ...]:
    keys = []
    for order in permutations(range(3)):
        diagonal = tuple(integer[order[i]][order[i]] for i in range(3))
        edges = tuple(
            abs(integer[order[i]][order[j]])
            for i, j in ((0, 1), (0, 2), (1, 2))
        )
        product_sign = (
            integer[order[0]][order[1]]
            * integer[order[0]][order[2]]
            * integer[order[1]][order[2]]
        )
        keys.append((diagonal, edges, 1 if product_sign > 0 else -1))
    return min(keys)


SINGULAR_TRIANGLES = {
    singular_triangle_key(representative)
    for representative in SINGULAR_REPRESENTATIVES
}


def response_alphabet_audit() -> dict[str, object]:
    remaining = list(combinations(range(1, 5), 2))
    nonsingular: Counter[tuple[int, int, int]] = Counter()
    singular: Counter[tuple[int, int, int]] = Counter()

    matrix = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        matrix[i][i] = 7

    def recurse_nonsingular(position: int) -> None:
        if position == len(remaining):
            inertia = charpoly_inertia(matrix)
            assert inertia[0] >= inertia[2]
            nonsingular[inertia] += 1
            return
        i, j = remaining[position]
        for value in (-9, -5, -3, -1, 1, 3, 5, 9):
            matrix[i][j] = matrix[j][i] = value
            if all(
                not (matrix[k][i] and matrix[k][j])
                or nonsingular_triangle_key(matrix, (k, i, j)) in NS_TRIANGLES
                for k in range(5)
                if k not in (i, j)
            ):
                recurse_nonsingular(position + 1)
        matrix[i][j] = matrix[j][i] = 0

    for star in product((1, 3, 5, 9), repeat=4):
        for j, value in enumerate(star, 1):
            matrix[0][j] = matrix[j][0] = value
        recurse_nonsingular(0)

    for diagonal in product((2, 4), repeat=5):
        integer = [[0 for _ in range(5)] for _ in range(5)]
        for i in range(5):
            integer[i][i] = diagonal[i]

        def recurse_singular(position: int) -> None:
            if position == len(remaining):
                inertia = charpoly_inertia(integer)
                assert inertia[0] >= inertia[2]
                singular[inertia] += 1
                return
            i, j = remaining[position]
            for value in (-3, -1, 1, 3):
                integer[i][j] = integer[j][i] = value
                allowed = True
                for k in range(5):
                    if k in (i, j) or not (integer[k][i] and integer[k][j]):
                        continue
                    vertices = (k, i, j)
                    triangle = tuple(
                        tuple(integer[x][y] for y in vertices) for x in vertices
                    )
                    if singular_triangle_key(triangle) not in SINGULAR_TRIANGLES:
                        allowed = False
                        break
                if allowed:
                    recurse_singular(position + 1)
            integer[i][j] = integer[j][i] = 0

        for star in product((1, 3), repeat=4):
            for j, value in enumerate(star, 1):
                integer[0][j] = integer[j][0] = value
            recurse_singular(0)

    assert nonsingular == Counter({
        (3, 0, 2): 552,
        (4, 0, 1): 1_045,
        (5, 0, 0): 81,
    })
    assert singular == Counter({
        (3, 0, 2): 612,
        (3, 1, 1): 140,
        (4, 0, 1): 1_301,
        (4, 1, 0): 15,
        (5, 0, 0): 92,
    })
    return {
        "nonsingular_response_inertias": sorted(nonsingular.items()),
        "nonsingular_response_matrices": sum(nonsingular.values()),
        "singular_range_response_inertias": sorted(singular.items()),
        "singular_range_response_matrices": sum(singular.values()),
    }


def direct_line_signature(graph: c2.Graph) -> int:
    edges: list[tuple[int, int]] = []
    for u in range(len(graph)):
        for v in range(u + 1, len(graph)):
            assert graph[u][v] in (0, 1), "audit expects a simple graph"
            if graph[u][v]:
                edges.append((u, v))
    adjacency = [[0 for _ in edges] for _ in edges]
    for i, (a, b) in enumerate(edges):
        for j in range(i):
            c, d = edges[j]
            if len({a, b, c, d}) < 4:
                adjacency[i][j] = adjacency[j][i] = 1
    positive, _, negative = charpoly_inertia(adjacency)
    return positive - negative


def add_five_leaves(graph: c2.Graph, ports: tuple[int, ...]) -> c2.Graph:
    result = [row[:] for row in graph]
    for support in ports:
        leaf = c2.add_vertex(result)
        c2.add_edge(result, support, leaf)
    return result


def definition_level_audit() -> dict[str, object]:
    distribution: Counter[int] = Counter()
    checks = 0
    for spec in ((4, 5, 1), (4, 5, 3), (5, 5, 1), (5, 5, 3)):
        graph, _ = c2.dumbbell(*spec)
        before = direct_line_signature(graph)
        assert before == 1
        for ports in combinations_with_replacement(range(len(graph)), 5):
            delta = direct_line_signature(add_five_leaves(graph, ports)) - before
            assert delta <= 0
            distribution[delta] += 1
            checks += 1

    assert distribution == Counter({
        -5: 5_616,
        -4: 2_195,
        -3: 2_501,
        -2: 329,
        -1: 19,
    })

    base, _ = c2.dumbbell(4, 5, 1)
    subdivided, _ = c2.subdivide_four(base, 0, 4)
    equality_ports = (1, 9, 10, 11, 12)
    equality_delta = (
        direct_line_signature(add_five_leaves(subdivided, equality_ports))
        - direct_line_signature(subdivided)
    )
    assert equality_delta == 0
    return {
        "definition_level_base_checks": checks,
        "definition_level_delta_distribution": sorted(distribution.items()),
        "equality_ports": equality_ports,
        "equality_subdivided_edge": (0, 4),
    }


def main() -> None:
    record = {
        "coefficient_domain": "ZZ[x]",
        "root_count": "Descartes variations for real-rooted characteristic polynomials",
        "sympy": sympy.__version__,
        **response_alphabet_audit(),
        **definition_level_audit(),
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(canonical.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
