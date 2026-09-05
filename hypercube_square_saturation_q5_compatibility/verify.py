#!/usr/bin/env python3
"""Exact corroboration for the Q5 facet-compatibility lemma.

The script checks only elementary finite incidence and capacity statements.
The sharp external input ex(Q_5, C_4) = 56 is recorded, not reproved.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json


DIM = 5
EXTERNAL_Q5_SQUAREFREE_EDGE_CAP = 56

Vertices = tuple(range(1 << DIM))
Edges = tuple((v, i) for i in range(DIM) for v in Vertices if not (v >> i) & 1)
Facets = tuple((j, bit) for j in range(DIM) for bit in (0, 1))
Squares = tuple(
    (v, i, j)
    for i in range(DIM)
    for j in range(i + 1, DIM)
    for v in Vertices
    if not (v >> i) & 1 and not (v >> j) & 1
)


def edge_facets(edge: tuple[int, int]) -> frozenset[tuple[int, int]]:
    """Return the Q4 facets containing a canonical Q5 edge."""

    v, direction = edge
    return frozenset((j, (v >> j) & 1) for j in range(DIM) if j != direction)


EdgeFacets = {edge: edge_facets(edge) for edge in Edges}


def square_edges(square: tuple[int, int, int]) -> frozenset[tuple[int, int]]:
    """Return the four canonical edges of a coordinate square."""

    v, i, j = square
    return frozenset(
        (
            (v, i),
            (v, j),
            (v | (1 << i), j),
            (v | (1 << j), i),
        )
    )


SquareEdges = {square: square_edges(square) for square in Squares}


def allowed_edge_capacity(live_facets: tuple[tuple[int, int], ...]) -> int:
    """Count edges whose four containing facets are all declared live."""

    live = frozenset(live_facets)
    return sum(EdgeFacets[edge] <= live for edge in Edges)


def capacity_distribution(number_live: int) -> dict[int, int]:
    """Return capacity -> number of live-facet sets with that capacity."""

    counts = Counter(
        allowed_edge_capacity(live) for live in combinations(Facets, number_live)
    )
    return dict(sorted(counts.items()))


def certificate() -> dict[str, object]:
    edge_square_multiplicity = Counter(
        edge for square in Squares for edge in SquareEdges[square]
    )
    equality_pairs = [
        (edges, slack)
        for edges in range(25)
        for slack in range(25)
        if 17 * slack == 3 * edges
    ]
    possible_live_counts = [
        live for live in range(1, len(Facets) + 1) if (17 * live) % 4 == 0
    ]
    live4 = capacity_distribution(4)
    live8 = capacity_distribution(8)

    assert len(Vertices) == 32
    assert len(Edges) == 80
    assert len(Squares) == 80
    assert len(Facets) == 10
    assert set(map(len, EdgeFacets.values())) == {4}
    assert set(edge_square_multiplicity.values()) == {4}
    assert equality_pairs == [(0, 0), (17, 3)]
    assert possible_live_counts == [4, 8]
    assert live4 == {0: 130, 1: 80}
    assert live8 == {16: 5, 28: 40}
    assert max(live4) < 17
    assert max(live8) < 34

    # If all ten Q4 facet deficits vanished, a nonempty facet would have
    # (E_H, S_H) = (17, 3).  The incidence equation 17k = 4E_K then gives
    # k in {4,8}; the two capacity bounds above contradict E_K=17k/4.
    strict_delta_lower_bound = 1

    q5_slack_edge_ratio = Fraction(
        12 * EXTERNAL_Q5_SQUAREFREE_EDGE_CAP + strict_delta_lower_bound,
        34 * EXTERNAL_Q5_SQUAREFREE_EDGE_CAP,
    )
    global_slack_coefficient = q5_slack_edge_ratio / 12
    retained_coefficient = 1 - global_slack_coefficient
    asymptotic_constant = Fraction(39984, 22175)
    old_asymptotic_constant = Fraction(119, 66)
    improvement = asymptotic_constant - old_asymptotic_constant

    assert q5_slack_edge_ratio == Fraction(673, 1904)
    assert global_slack_coefficient == Fraction(673, 22848)
    assert retained_coefficient == Fraction(22175, 22848)
    assert improvement == Fraction(119, 1463550)

    return {
        "q5_vertices": len(Vertices),
        "q5_edges": len(Edges),
        "q5_squares": len(Squares),
        "q5_facets": len(Facets),
        "edge_facet_multiplicity": 4,
        "edge_square_multiplicity": 4,
        "q4_equality_pairs_E_S": equality_pairs,
        "possible_live_facet_counts": possible_live_counts,
        "live4_capacity_distribution": live4,
        "live8_capacity_distribution": live8,
        "live4_required_edges": 17,
        "live8_required_edges": 34,
        "strict_q5_delta_lower_bound": strict_delta_lower_bound,
        "external_q5_squarefree_edge_cap": EXTERNAL_Q5_SQUAREFREE_EDGE_CAP,
        "q5_slack_edge_ratio": str(q5_slack_edge_ratio),
        "global_slack_coefficient": str(global_slack_coefficient),
        "bound": "sat(Q_d,Q_2) >= 39984*d*2^d/(22175*d+57793) for d>=5",
        "asymptotic_constant": str(asymptotic_constant),
        "improvement_over_119_66": str(improvement),
    }


def main() -> None:
    data = certificate()
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    print(json.dumps(data, sort_keys=True, indent=2))
    print(f"certificate_sha256={sha256(canonical.encode()).hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
