#!/usr/bin/env python3
"""Exact corroboration of two-leaf stability at cyclomatic number two."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json
import platform

import verify_c2_core as c2


def inverse(matrix: c2.Matrix) -> c2.Matrix:
    n = len(matrix)
    a = [
        matrix[i][:] + [Fraction(i == j) for j in range(n)]
        for i in range(n)
    ]
    for column in range(n):
        pivot = next(row for row in range(column, n) if a[row][column])
        a[column], a[pivot] = a[pivot], a[column]
        d = a[column][column]
        a[column] = [value / d for value in a[column]]
        for row in range(n):
            if row == column or not a[row][column]:
                continue
            q = a[row][column]
            a[row] = [
                a[row][j] - q * a[column][j] for j in range(2 * n)
            ]
    return [row[n:] for row in a]


def quadratic(matrix: c2.Matrix, vector: list[Fraction]) -> Fraction:
    return sum(
        vector[i] * matrix[i][j] * vector[j]
        for i in range(len(vector))
        for j in range(len(vector))
    )


def add_two_leaves(g: c2.Graph, x: int, y: int) -> c2.Graph:
    h = [row[:] for row in g]
    for support in (x, y):
        new = c2.add_vertex(h)
        c2.add_edge(h, support, new)
    return h


def pair_delta(g: c2.Graph, x: int, y: int) -> int:
    return c2.line_signature_c2(add_two_leaves(g, x, y)) - c2.line_signature_c2(g)


def two_by_two_signature(a: Fraction, b: Fraction, d: Fraction) -> int:
    return c2.matrix_signature([[a, b], [b, d]])


def predicted_nonsingular_delta(
    response: c2.Matrix, x: int, y: int
) -> int:
    # E has columns e_x,e_y, including the repeated-support case x=y.
    s00 = Fraction(1, 2) + response[x][x]
    s11 = Fraction(1, 2) + response[y][y]
    s01 = response[x][y]
    return -two_by_two_signature(s00, s01, s11)


def null_vector_for_first_cycle(a: int, order: int) -> list[Fraction]:
    z = [Fraction(0) for _ in range(order)]
    for position in range(1, a):
        if position % 2:
            z[position] = Fraction((-1) ** ((position - 1) // 2))
    return z


def main() -> None:
    base_specs = ((4, 5, 1), (4, 5, 3), (5, 5, 1), (5, 5, 3))
    base_distribution: Counter[int] = Counter()
    subdivision_distribution: Counter[int] = Counter()
    base_pair_checks = 0
    subdivision_pair_checks = 0
    rank_two_identity_checks = 0

    for spec in base_specs:
        g, _ = c2.dumbbell(*spec)
        assert c2.line_signature_c2(g) == 1
        nonsingular = c2.inertia(c2.shifted_signless(g))[1] == 0
        response = inverse(c2.shifted_signless(g)) if nonsingular else None
        for x in range(len(g)):
            for y in range(x, len(g)):
                delta = pair_delta(g, x, y)
                assert delta <= 0
                base_distribution[delta] += 1
                base_pair_checks += 1
                if response is not None:
                    assert delta == predicted_nonsingular_delta(response, x, y)
                    rank_two_identity_checks += 1

        for u, v in c2.edges(g):
            h, _ = c2.subdivide_four(g, u, v)
            assert c2.line_signature_c2(h) == 1
            nonsingular_h = c2.inertia(c2.shifted_signless(h))[1] == 0
            response_h = inverse(c2.shifted_signless(h)) if nonsingular_h else None
            for x in range(len(h)):
                for y in range(x, len(h)):
                    delta = pair_delta(h, x, y)
                    assert delta <= 0
                    subdivision_distribution[delta] += 1
                    subdivision_pair_checks += 1
                    if response_h is not None:
                        assert delta == predicted_nonsingular_delta(response_h, x, y)
                        rank_two_identity_checks += 1

    # Check the singular-cycle isotropy well beyond the four minimal bases.
    isotropy_graphs = 0
    isotropy_pairs = 0
    for a in (4, 8, 12):
        for b in (5, 9):
            for bridge_length in (1, 3, 5, 7, 9, 11):
                g, _ = c2.dumbbell(a, b, bridge_length)
                m = c2.shifted_signless(g)
                z = null_vector_for_first_cycle(a, len(g))
                assert any(z)
                assert all(
                    sum(m[i][j] * z[j] for j in range(len(g))) == 0
                    for i in range(len(g))
                )
                # M+zz^T is invertible.  On z-perp, its inverse solves Ma=w.
                lifted = [
                    [m[i][j] + z[i] * z[j] for j in range(len(g))]
                    for i in range(len(g))
                ]
                green = inverse(lifted)
                undefined = [i for i, value in enumerate(z) if value]
                for offset, x in enumerate(undefined):
                    for y in undefined[offset:]:
                        d = [Fraction(0) for _ in range(len(g))]
                        d[x] -= z[y]
                        d[y] += z[x]
                        assert sum(d[i] * z[i] for i in range(len(g))) == 0
                        assert quadratic(green, d) == 0
                        assert pair_delta(g, x, y) <= 0
                        isotropy_pairs += 1
                isotropy_graphs += 1

    record = {
        "arithmetic": "fractions.Fraction",
        "base_delta_distribution": sorted(base_distribution.items()),
        "base_pair_checks": base_pair_checks,
        "isotropy_graphs": isotropy_graphs,
        "isotropy_pairs": isotropy_pairs,
        "python": platform.python_version(),
        "rank_two_identity_checks": rank_two_identity_checks,
        "subdivision_delta_distribution": sorted(subdivision_distribution.items()),
        "subdivision_pair_checks": subdivision_pair_checks,
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print("result_sha256=" + hashlib.sha256(canonical.encode()).hexdigest())
    print("VERIFIED")


if __name__ == "__main__":
    main()
