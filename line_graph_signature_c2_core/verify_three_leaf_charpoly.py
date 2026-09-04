#!/usr/bin/env python3
"""Independent definition-level audit for three simultaneous leaves.

Requires SymPy 1.14.x.  This script does not use the response formula or the
production checker's inertia routine.  It constructs line graphs directly,
computes adjacency characteristic polynomials over ZZ[x], and counts signs by
Descartes variations.  The count is exact because all adjacency roots are real.
"""

from __future__ import annotations

from collections import Counter
import hashlib
from itertools import combinations_with_replacement
import json

import sympy
from sympy import Matrix, Poly, Symbol, cancel

import verify_c2_core as c2


X = Symbol("x")


def sign_variations(coefficients: list[sympy.Expr]) -> int:
    signs = [
        1 if coefficient > 0 else -1
        for coefficient in coefficients
        if coefficient
    ]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def direct_line_signature(g: c2.Graph) -> int:
    edges: list[tuple[int, int]] = []
    for u in range(len(g)):
        for v in range(u + 1, len(g)):
            assert g[u][v] in (0, 1), "audit expects a simple graph"
            if g[u][v]:
                edges.append((u, v))
    adjacency = Matrix.zeros(len(edges))
    for i, (a, b) in enumerate(edges):
        for j in range(i):
            c, d = edges[j]
            if len({a, b, c, d}) < 4:
                adjacency[i, j] = adjacency[j, i] = 1

    nullity = adjacency.rows - adjacency.rank()
    characteristic = adjacency.charpoly(X).as_expr()
    nonzero = Poly(cancel(characteristic / X**nullity), X, domain="ZZ")
    positive = sign_variations(nonzero.all_coeffs())
    reflected = Poly(nonzero.as_expr().subs(X, -X), X, domain="ZZ")
    negative = sign_variations(reflected.all_coeffs())
    assert positive + negative + nullity == adjacency.rows
    return positive - negative


def add_three_leaves(g: c2.Graph, ports: tuple[int, int, int]) -> c2.Graph:
    result = [row[:] for row in g]
    for support in ports:
        leaf = c2.add_vertex(result)
        c2.add_edge(result, support, leaf)
    return result


def main() -> None:
    distribution: Counter[int] = Counter()
    checks = 0
    for spec in ((4, 5, 1), (4, 5, 3), (5, 5, 1), (5, 5, 3)):
        g, _ = c2.dumbbell(*spec)
        before = direct_line_signature(g)
        assert before == 1
        for ports in combinations_with_replacement(range(len(g)), 3):
            delta = direct_line_signature(add_three_leaves(g, ports)) - before
            assert delta <= 0
            distribution[delta] += 1
            checks += 1

    assert sorted(distribution.items()) == [(-3, 773), (-2, 213), (-1, 47), (0, 2)]
    record = {
        "coefficient_domain": "ZZ[x]",
        "definition_level_triples": checks,
        "delta_distribution": sorted(distribution.items()),
        "root_count": "Descartes variations for real-rooted characteristic polynomials",
        "sympy": sympy.__version__,
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(canonical.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
