#!/usr/bin/env python3
"""Exact corroboration for the Q6 live-Q5-facet lift.

The program checks all 2^12 live-facet sets against the structural capacity
formula and verifies the exact rational arithmetic in the global bound.  The
external theorem ex(Q_6, C_4) = 132 is recorded, not reproved.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import comb
import json


DIM = 6
EXTERNAL_Q6_SQUAREFREE_EDGE_CAP = 132

VERTICES = tuple(range(1 << DIM))
EDGES = tuple((v, i) for i in range(DIM) for v in VERTICES if not (v >> i) & 1)
FACETS = tuple((j, bit) for j in range(DIM) for bit in (0, 1))
Q3_SUBCUBE_COUNT = comb(DIM, 3) * (1 << (DIM - 3))
SQUARES = tuple(
    (v, i, j)
    for i in range(DIM)
    for j in range(i + 1, DIM)
    for v in VERTICES
    if not (v >> i) & 1 and not (v >> j) & 1
)


def edge_facets(edge: tuple[int, int]) -> frozenset[tuple[int, int]]:
    """Return the five Q5 facets containing a canonical Q6 edge."""

    vertex, direction = edge
    return frozenset(
        (j, (vertex >> j) & 1) for j in range(DIM) if j != direction
    )


EDGE_FACETS = {edge: edge_facets(edge) for edge in EDGES}


def square_edges(square: tuple[int, int, int]) -> frozenset[tuple[int, int]]:
    """Return the four canonical edges of a coordinate square."""

    vertex, i, j = square
    return frozenset(
        (
            (vertex, i),
            (vertex, j),
            (vertex | (1 << i), j),
            (vertex | (1 << j), i),
        )
    )


SQUARE_EDGES = {square: square_edges(square) for square in SQUARES}


def live_facets(mask: int) -> frozenset[tuple[int, int]]:
    """Decode a 12-bit mask in the canonical FACETS order."""

    if not 0 <= mask < 1 << len(FACETS):
        raise ValueError("facet mask must be a 12-bit nonnegative integer")
    return frozenset(facet for index, facet in enumerate(FACETS) if mask >> index & 1)


def pair_profile(live: frozenset[tuple[int, int]]) -> tuple[int, int, int]:
    """Return counts (a,b,c) of double, single, and empty opposite pairs."""

    multiplicities = Counter(
        int((coordinate, 0) in live) + int((coordinate, 1) in live)
        for coordinate in range(DIM)
    )
    return multiplicities[2], multiplicities[1], multiplicities[0]


def structural_capacity(a: int, b: int, c: int) -> int:
    """Capacity dictated by the opposite-facet pair profile."""

    if min(a, b, c) < 0 or a + b + c != DIM:
        raise ValueError("(a,b,c) must partition the six coordinate pairs")
    if c >= 2:
        return 0
    if c == 1:
        # The edge direction must be the unique empty coordinate; the a
        # double pairs leave a free position bits.
        return 1 << a
    # With no empty coordinate, a double-pair direction contributes 2^(a-1)
    # edges and a single-pair direction contributes 2^a edges.
    double_directions = 0 if a == 0 else a * (1 << (a - 1))
    single_directions = b * (1 << a)
    return double_directions + single_directions


def enumerated_capacity(live: frozenset[tuple[int, int]]) -> int:
    """Count Q6 edges whose five containing facets are all live."""

    return sum(EDGE_FACETS[edge] <= live for edge in EDGES)


def capacity_audit() -> tuple[dict[int, int], str]:
    """Check all live-facet sets and hash the entry-level audit."""

    maximum_by_live_count = {live_count: 0 for live_count in range(13)}
    rows: list[tuple[int, int, int, int, int, int]] = []
    for mask in range(1 << len(FACETS)):
        live = live_facets(mask)
        a, b, c = pair_profile(live)
        actual = enumerated_capacity(live)
        predicted = structural_capacity(a, b, c)
        assert actual == predicted
        k = len(live)
        maximum_by_live_count[k] = max(maximum_by_live_count[k], actual)
        rows.append((mask, a, b, c, actual, predicted))

    canonical = json.dumps(rows, separators=(",", ":"))
    return maximum_by_live_count, sha256(canonical.encode()).hexdigest()


def certificate() -> dict[str, object]:
    edge_square_multiplicity = Counter(
        edge for square in SQUARES for edge in SQUARE_EDGES[square]
    )
    support_maxima, support_audit_hash = capacity_audit()
    expected_maxima = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 1,
        6: 6,
        7: 11,
        8: 20,
        9: 36,
        10: 64,
        11: 112,
        12: 192,
    }

    assert len(VERTICES) == 64
    assert len(EDGES) == 192
    assert len(SQUARES) == 240
    assert len(FACETS) == 12
    assert Q3_SUBCUBE_COUNT == 160
    assert set(map(len, EDGE_FACETS.values())) == {5}
    assert set(edge_square_multiplicity.values()) == {5}
    assert support_maxima == expected_maxima
    assert all(support_maxima[k] <= 11 * k for k in range(12))
    assert EXTERNAL_Q6_SQUAREFREE_EDGE_CAP == 11 * 12

    deficit_per_edge = Fraction(1, 11)
    q6_slack_edge_ratio = (60 + deficit_per_edge) / 102
    global_slack_coefficient = q6_slack_edge_ratio / 20
    retained_coefficient = 1 - global_slack_coefficient
    asymptotic_constant = Fraction(39270, 21779)
    preceding_constant = Fraction(39984, 22175)
    asymptotic_improvement = asymptotic_constant - preceding_constant

    assert q6_slack_edge_ratio == Fraction(661, 1122)
    assert global_slack_coefficient == Fraction(661, 22440)
    assert retained_coefficient == Fraction(21779, 22440)
    assert asymptotic_improvement == Fraction(714, 482949325)
    assert 39270 * 22175 - 39984 * 21779 == 714
    assert 39270 * 57793 - 39984 * 56761 == -714

    return {
        "q6_vertices": len(VERTICES),
        "q6_edges": len(EDGES),
        "q6_squares": len(SQUARES),
        "q6_q5_facets": len(FACETS),
        "q6_q3_subcubes": Q3_SUBCUBE_COUNT,
        "edge_q5_facet_multiplicity": 5,
        "edge_square_multiplicity": 5,
        "live_facet_sets_checked": 1 << len(FACETS),
        "support_capacity_max_by_live_count": support_maxima,
        "support_audit_sha256": support_audit_hash,
        "external_q6_squarefree_edge_cap": EXTERNAL_Q6_SQUAREFREE_EDGE_CAP,
        "q6_deficit_per_edge": str(deficit_per_edge),
        "q6_slack_edge_ratio": str(q6_slack_edge_ratio),
        "global_slack_coefficient": str(global_slack_coefficient),
        "bound": "sat(Q_d,Q_2) >= 39270*d*2^d/(21779*d+56761) for d>=6",
        "asymptotic_constant": str(asymptotic_constant),
        "improvement_over_39984_22175": str(asymptotic_improvement),
        "finite_bound_cross_difference": "714*(d-1)",
    }


def main() -> None:
    data = certificate()
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    print(json.dumps(data, sort_keys=True, indent=2))
    print(f"certificate_sha256={sha256(canonical.encode()).hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
