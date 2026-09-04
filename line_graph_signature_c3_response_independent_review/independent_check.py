#!/usr/bin/env python3
"""Independent exact audit of the c=3 equality-response lemma.

This checker imports no target code.  It represents the equality graphs as
sets of named edges, uses SymPy's exact DomainMatrix inverse for the diagonal
Green responses, and verifies the leaf conclusion from the definition by
constructing the line graph and counting the signs of its exact
characteristic-polynomial roots.  The latter count is exact because an
integer symmetric matrix has only real eigenvalues.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json

import sympy as sp


Edge = tuple[str, str]


def make_edge(a: str, b: str) -> Edge:
    assert a != b
    return tuple(sorted((a, b)))


def equality_base(
    central: tuple[int, int], connectors: tuple[int, int]
) -> tuple[list[str], list[Edge], dict[str, sp.Rational]]:
    """Construct a reduced equality graph directly from six named paths."""
    p, q = central
    r, s = connectors
    assert {p, q} == {1, 3}
    assert r in {1, 3} and s in {1, 3}

    vertices = ["x", "y", "u", "v"]
    edges: list[Edge] = []
    paths: dict[str, list[str]] = {}

    def path(label: str, start: str, finish: str, length: int) -> None:
        walk = [start]
        for position in range(1, length):
            name = f"{label}:{position}"
            vertices.append(name)
            walk.append(name)
        walk.append(finish)
        paths[label] = walk
        edges.extend(make_edge(a, b) for a, b in zip(walk, walk[1:]))

    path("A", "u", "u", 5)
    path("B", "v", "v", 5)
    path("P", "x", "y", p)
    path("Q", "x", "y", q)
    path("R", "x", "v", r)
    path("S", "y", "u", s)
    assert len(edges) == len(set(edges))

    half = sp.Rational(1, 2)
    three_halves = sp.Rational(3, 2)
    expected: dict[str, sp.Rational] = {}

    def assign(names: list[str], value: sp.Rational) -> None:
        for name in names:
            if name in expected:
                assert expected[name] == value
            expected[name] = value

    assign(paths["A"][:-1], half)
    assign(paths["B"][:-1], half)
    assign(paths["P"], three_halves)
    assign(paths["Q"], three_halves)
    for label in ("R", "S"):
        for distance, name in enumerate(paths[label]):
            assign([name], three_halves if distance % 2 == 0 else half)
    assert set(expected) == set(vertices)
    return vertices, edges, expected


def adjacency(vertices: list[str], edges: list[Edge]) -> sp.Matrix:
    index = {name: i for i, name in enumerate(vertices)}
    matrix = sp.zeros(len(vertices))
    for a, b in edges:
        i, j = index[a], index[b]
        assert matrix[i, j] == 0
        matrix[i, j] = matrix[j, i] = 1
    return matrix


def shifted_signless(vertices: list[str], edges: list[Edge]) -> sp.Matrix:
    adj = adjacency(vertices, edges)
    degrees = [sum(int(adj[i, j]) for j in range(len(vertices))) for i in range(len(vertices))]
    assert min(degrees) >= 2
    assert len(edges) - len(vertices) + 1 == 3
    return adj + sp.diag(*degrees) - 2 * sp.eye(len(vertices))


def line_graph_adjacency(edges: list[Edge]) -> sp.Matrix:
    """Definition-level line graph: root edges are the new vertices."""
    matrix = sp.zeros(len(edges))
    endpoint_sets = [set(edge) for edge in edges]
    for i in range(len(edges)):
        for j in range(i):
            if endpoint_sets[i] & endpoint_sets[j]:
                matrix[i, j] = matrix[j, i] = 1
    return matrix


def sign_variations(values: list[sp.Expr]) -> int:
    signs = [sp.sign(value) for value in values if value != 0]
    assert all(sign in (-1, 1) for sign in signs)
    return sum(a != b for a, b in zip(signs, signs[1:]))


def symmetric_inertia(matrix: sp.Matrix) -> tuple[int, int, int]:
    """Count eigenvalue signs from an exact real-rooted characteristic polynomial."""
    coefficients = matrix.charpoly().all_coeffs()
    nullity = 0
    while coefficients[-1] == 0:
        coefficients.pop()
        nullity += 1
    degree = len(coefficients) - 1
    positive = sign_variations(coefficients)
    at_negative = [
        coefficient * (-1) ** (degree - i)
        for i, coefficient in enumerate(coefficients)
    ]
    negative = sign_variations(at_negative)
    assert positive + nullity + negative == matrix.rows
    return positive, nullity, negative


def add_leaf_star(edges: list[Edge], port: str, count: int) -> list[Edge]:
    assert count >= 1
    result = list(edges)
    result.extend(make_edge(port, f"leaf:{i}") for i in range(count))
    assert len(result) == len(set(result))
    return result


def transport_certificate() -> None:
    """Verify the universal four-subdivision Schur-complement identity."""
    path4 = sp.Matrix(
        [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
    )
    claimed_inverse = sp.Matrix(
        [[0, 1, 0, -1], [1, 0, 0, 0], [0, 0, 0, 1], [-1, 0, 1, 0]]
    )
    assert path4 * claimed_inverse == sp.eye(4)
    incidence = sp.Matrix([[1, 0, 0, 0], [0, 0, 0, 1]])
    removed_edge = sp.Matrix([[0, 1], [1, 0]])
    assert incidence * claimed_inverse * incidence.T == -removed_edge


def fraction_text(value: sp.Rational) -> str:
    return f"{value.p}/{value.q}"


def main() -> None:
    transport_certificate()
    records: list[str] = []
    determinant_counts: Counter[int] = Counter()
    response_counts: Counter[str] = Counter()
    base_signatures: Counter[int] = Counter()
    one_leaf_checks = 0
    same_port_star_checks = 0

    for central in ((1, 3), (3, 1)):
        for connectors in ((1, 1), (1, 3), (3, 1), (3, 3)):
            vertices, edges, expected = equality_base(central, connectors)
            shifted = shifted_signless(vertices, edges)
            inverse = shifted.inv(method="DM")
            determinant_counts[int(shifted.det(method="domain-ge"))] += 1

            base_inertia = symmetric_inertia(line_graph_adjacency(edges))
            base_signatures[base_inertia[0] - base_inertia[2]] += 1
            assert base_inertia[0] - base_inertia[2] == 2
            assert base_inertia[1] == 0

            representatives: dict[sp.Rational, str] = {}
            for index, name in enumerate(vertices):
                response = inverse[index, index]
                assert response == expected[name]
                response_text = fraction_text(response)
                response_counts[response_text] += 1
                representatives.setdefault(response, name)
                records.append(
                    ":".join(
                        (
                            str(central[0]),
                            str(central[1]),
                            str(connectors[0]),
                            str(connectors[1]),
                            name,
                            response_text,
                        )
                    )
                )

                leaf_inertia = symmetric_inertia(
                    line_graph_adjacency(add_leaf_star(edges, name, 1))
                )
                assert leaf_inertia[0] - leaf_inertia[2] == 1
                assert leaf_inertia[1] == 0
                one_leaf_checks += 1

            # The general same-port k-leaf corollary is proved by the block
            # identity in the README.  These are definition-level spot checks
            # at both possible response roles for k=2,...,6.
            assert set(representatives) == {sp.Rational(1, 2), sp.Rational(3, 2)}
            for name in representatives.values():
                for count in range(2, 7):
                    star_inertia = symmetric_inertia(
                        line_graph_adjacency(add_leaf_star(edges, name, count))
                    )
                    assert star_inertia[0] - star_inertia[2] == 2 - count
                    assert star_inertia[1] == 0
                    same_port_star_checks += 1

    record_sha256 = hashlib.sha256("\n".join(sorted(records)).encode()).hexdigest()
    assert record_sha256 == "3f35404094eee97889596aa8fa4387782aef8a329fb3ec58b5d6651deeae5651"
    assert determinant_counts == Counter({-4: 4, 4: 4})
    assert response_counts == Counter({"1/2": 88, "3/2": 40})
    assert base_signatures == Counter({2: 8})
    assert one_leaf_checks == 128
    assert same_port_star_checks == 80

    result = {
        "algorithm": "SymPy DomainMatrix inverse plus direct line-graph charpoly",
        "base_assignments": 8,
        "base_signature_checks": 8,
        "determinant_counts": {"-4": 4, "4": 4},
        "one_leaf_signature_checks": one_leaf_checks,
        "record_sha256": record_sha256,
        "response_counts": {"1/2": 88, "3/2": 40},
        "same_port_star_checks_k2_through_k6": same_port_star_checks,
        "status": "VERIFIED",
        "sympy": sp.__version__,
        "transport_schur_identity": "VERIFIED",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
