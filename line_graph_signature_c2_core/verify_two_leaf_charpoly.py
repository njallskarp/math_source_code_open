#!/usr/bin/env python3
"""Independent exact line-graph/characteristic-polynomial audit.

Requires SymPy 1.14.x.  Unlike the production checker, this constructs every
line graph from the definition and works with characteristic polynomials in
ZZ[x].  Descartes sign variations are exact because adjacency matrices are
real symmetric, so the nonzero characteristic roots are all real.
"""

from __future__ import annotations

import hashlib
import json

import sympy
from sympy import Matrix, Poly, Symbol, cancel

import verify_c2_core as c2
import verify_two_leaf as two


X = Symbol("x")


def sign_variations(coefficients: list[sympy.Expr]) -> int:
    signs = [1 if coefficient > 0 else -1 for coefficient in coefficients if coefficient]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def direct_line_signature(g: c2.Graph) -> int:
    edges: list[tuple[int, int]] = []
    for u in range(len(g)):
        for v in range(u + 1, len(g)):
            assert g[u][v] in (0, 1), "definition-level audit expects a simple graph"
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
    nonzero_part = Poly(cancel(characteristic / X**nullity), X, domain="ZZ")
    positive = sign_variations(nonzero_part.all_coeffs())
    negative_part = Poly(nonzero_part.as_expr().subs(X, -X), X, domain="ZZ")
    negative = sign_variations(negative_part.all_coeffs())
    assert positive + negative + nullity == adjacency.rows
    return positive - negative


def main() -> None:
    checks = 0
    delta_distribution: dict[int, int] = {}
    for spec in ((4, 5, 1), (4, 5, 3), (5, 5, 1), (5, 5, 3)):
        g, _ = c2.dumbbell(*spec)
        base = direct_line_signature(g)
        assert base == 1
        for x in range(len(g)):
            for y in range(x, len(g)):
                h = two.add_two_leaves(g, x, y)
                delta = direct_line_signature(h) - base
                assert delta == two.pair_delta(g, x, y)
                assert delta <= 0
                delta_distribution[delta] = delta_distribution.get(delta, 0) + 1
                checks += 1

    record = {
        "coefficient_domain": "ZZ[x]",
        "definition_level_pair_checks": checks,
        "delta_distribution": sorted(delta_distribution.items()),
        "root_count": "Descartes variations for real-rooted characteristic polynomials",
        "sympy": sympy.__version__,
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(canonical.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
