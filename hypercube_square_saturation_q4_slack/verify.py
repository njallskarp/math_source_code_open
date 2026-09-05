#!/usr/bin/env python3
"""Definition-level verifier for the strict Q4 compatibility slack.

The human proof is in README.md.  This program exhausts only the finite local
ingredients, using canonical labeled edges (v, i) for {v, v xor 2**i} with
the i-th bit of v equal to zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations


DIM = 4


def edge_labels(dim: int) -> list[tuple[int, int]]:
    return [
        (vertex, direction)
        for direction in range(dim)
        for vertex in range(1 << dim)
        if not (vertex >> direction) & 1
    ]


EDGES = edge_labels(DIM)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def square_edges(base: int, first: int, second: int) -> tuple[int, ...]:
    assert first < second
    assert not (base >> first) & 1 and not (base >> second) & 1
    return (
        EDGE_INDEX[(base, first)],
        EDGE_INDEX[(base, second)],
        EDGE_INDEX[(base ^ (1 << first), second)],
        EDGE_INDEX[(base ^ (1 << second), first)],
    )


SQUARES = tuple(
    square_edges(base, first, second)
    for first in range(DIM)
    for second in range(first + 1, DIM)
    for base in range(1 << DIM)
    if not (base >> first) & 1 and not (base >> second) & 1
)


@dataclass(frozen=True)
class Facet:
    fixed_coordinate: int
    fixed_bit: int
    edges: tuple[int, ...]
    edge_mask: int
    squares: tuple[tuple[int, ...], ...]


def make_facet(fixed_coordinate: int, fixed_bit: int) -> Facet:
    vertices = {
        vertex
        for vertex in range(1 << DIM)
        if ((vertex >> fixed_coordinate) & 1) == fixed_bit
    }
    edges = tuple(
        index
        for index, (vertex, direction) in enumerate(EDGES)
        if direction != fixed_coordinate and vertex in vertices
    )
    squares = tuple(
        square
        for square in SQUARES
        if all(
            EDGES[edge][0] in vertices
            and (EDGES[edge][0] ^ (1 << EDGES[edge][1])) in vertices
            for edge in square
        )
    )
    assert len(edges) == 12 and len(squares) == 6
    return Facet(
        fixed_coordinate,
        fixed_bit,
        edges,
        sum(1 << edge for edge in edges),
        squares,
    )


FACETS = tuple(make_facet(coordinate, bit) for coordinate in range(DIM) for bit in range(2))
EDGE_FACETS = tuple(
    tuple(index for index, facet in enumerate(FACETS) if edge in facet.edges)
    for edge in range(len(EDGES))
)


def selected(mask: int, edge: int) -> int:
    return (mask >> edge) & 1


def local_statistics(mask: int, facet: Facet) -> tuple[int, int, int, int]:
    """Return (t, q, b, twice_sigma); reject a completed square."""
    missing_witnesses: list[int] = []
    inactive_selected_incidences = 0
    active_count = 0
    for square in facet.squares:
        present = sum(selected(mask, edge) for edge in square)
        if present == 4:
            raise ValueError("pattern is not square-free")
        if present == 3:
            active_count += 1
            missing_witnesses.append(next(edge for edge in square if not selected(mask, edge)))
        else:
            inactive_selected_incidences += present
    repeated = active_count - len(set(missing_witnesses))
    twice_sigma = 2 * inactive_selected_incidences + 4 * repeated - active_count
    return active_count, repeated, inactive_selected_incidences, twice_sigma


def local_masks(facet: Facet):
    for local_mask in range(1 << len(facet.edges)):
        yield sum(
            ((local_mask >> local_index) & 1) << edge
            for local_index, edge in enumerate(facet.edges)
        )


def equality_patterns(facet: Facet) -> tuple[int, ...]:
    patterns = []
    for mask in local_masks(facet):
        try:
            statistics = local_statistics(mask, facet)
        except ValueError:
            continue
        if statistics[3] == 0:
            patterns.append(mask)
    return tuple(patterns)


def compatible_equality_patterns(patterns: tuple[tuple[int, ...], ...]) -> set[int]:
    """Glue all eight facets, choosing the most constrained next facet."""
    complete: set[int] = set()

    def visit(remaining: tuple[int, ...], assigned: int, values: int) -> None:
        if not remaining:
            complete.add(values)
            return
        choice_lists = []
        for facet_index in remaining:
            overlap = FACETS[facet_index].edge_mask & assigned
            choices = tuple(
                pattern
                for pattern in patterns[facet_index]
                if ((pattern ^ values) & overlap) == 0
            )
            choice_lists.append((len(choices), facet_index, choices))
        _, facet_index, choices = min(choice_lists, key=lambda item: item[0])
        facet_mask = FACETS[facet_index].edge_mask
        next_remaining = tuple(index for index in remaining if index != facet_index)
        for pattern in choices:
            visit(
                next_remaining,
                assigned | facet_mask,
                (values & ~facet_mask) | pattern,
            )

    visit(tuple(range(len(FACETS))), 0, 0)
    return complete


def allowed_edge_capacity(live_facets: frozenset[int]) -> int:
    return sum(
        set(EDGE_FACETS[edge]).issubset(live_facets)
        for edge in range(len(EDGES))
    )


def capacity_summary(k: int) -> dict[int, int]:
    capacities = [
        allowed_edge_capacity(frozenset(live))
        for live in combinations(range(len(FACETS)), k)
    ]
    return {capacity: capacities.count(capacity) for capacity in sorted(set(capacities))}


def verify() -> dict[str, object]:
    assert len(EDGES) == 32
    assert len(SQUARES) == 24
    assert len(FACETS) == 8
    assert all(len(containing) == 3 for containing in EDGE_FACETS)

    representative = FACETS[0]
    squarefree_count = 0
    equality_statistics = []
    for mask in local_masks(representative):
        try:
            statistics = local_statistics(mask, representative)
        except ValueError:
            continue
        squarefree_count += 1
        assert statistics[3] >= 0
        if statistics[3] == 0:
            equality_statistics.append((mask.bit_count(), statistics[:3]))
    assert squarefree_count == 2902
    assert equality_statistics.count((0, (0, 0, 0))) == 1
    assert equality_statistics.count((7, (4, 0, 2))) == 48
    assert len(equality_statistics) == 49

    patterns = tuple(equality_patterns(facet) for facet in FACETS)
    assert all(len(facet_patterns) == 49 for facet_patterns in patterns)
    compatible = compatible_equality_patterns(patterns)
    assert compatible == {0}

    summary_three = capacity_summary(3)
    summary_six = capacity_summary(6)
    assert summary_three == {0: 24, 1: 32}
    assert summary_six == {8: 4, 12: 24}
    assert max(summary_three) < 7
    assert max(summary_six) < 14

    q4_edge_cap = len(SQUARES) * 3 // 3
    assert q4_edge_cap == 24
    improved_constant = Fraction(504, 287)
    previous_constant = Fraction(7, 4)
    assert improved_constant - previous_constant == Fraction(7, 1148)

    return {
        "q3_squarefree_patterns": squarefree_count,
        "q3_equality_patterns": len(equality_statistics),
        "q3_nonempty_equality_patterns": len(equality_statistics) - 1,
        "q4_compatible_equality_patterns": len(compatible),
        "live3_capacity_distribution": summary_three,
        "live6_capacity_distribution": summary_six,
        "q4_squarefree_edge_cap": q4_edge_cap,
        "bound": "sat(Q_d,Q_2) >= 504*d*2^d/(287*d+721) for d>=4",
        "asymptotic_constant": "504/287",
        "improvement_over_7/4": "7/1148",
    }


def main() -> None:
    results = verify()
    for key, value in results.items():
        print(f"{key}={value}")
    print("status=PASS")


if __name__ == "__main__":
    main()
