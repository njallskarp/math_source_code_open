#!/usr/bin/env python3
"""Exact certificate for the sharp Q4 facet-slack ratio.

The proof reduces a possible violation to a Q4 whose first Q3 facet is one
of 48 labeled positive-objective patterns.  Two deterministic searches then
rule out every compatible violation using different state representations:
whole-facet gluing and one-edge-at-a-time branching.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json

import verify


WITNESS_MASK = 0x2313FF54
FULL_EDGE_MASK = (1 << len(verify.EDGES)) - 1
FACET_ORDER = (0, 2, 4, 6, 1, 3, 5, 7)


def facet_patterns() -> tuple[tuple[tuple[int, int, int, int], ...], ...]:
    """Return (mask, lambda, edge_count, twice_sigma) for every local state."""
    result = []
    for facet in verify.FACETS:
        patterns = []
        for mask in verify.local_masks(facet):
            try:
                _, _, _, twice_sigma = verify.local_statistics(mask, facet)
            except ValueError:
                continue
            edge_count = mask.bit_count()
            objective = 2 * edge_count - 17 * twice_sigma
            patterns.append((mask, objective, edge_count, twice_sigma))
        result.append(tuple(sorted(patterns, key=lambda item: (-item[1], item[0]))))
    return tuple(result)


def direct_q4_statistics(mask: int) -> tuple[int, int, int, int]:
    """Return (E,T,P,S4) directly from edges and square witnesses."""
    missing_witnesses = []
    for square in verify.SQUARES:
        present = sum((mask >> edge) & 1 for edge in square)
        if present == 4:
            raise ValueError("pattern is not square-free")
        if present == 3:
            missing_witnesses.append(
                next(edge for edge in square if not (mask >> edge) & 1)
            )
    multiplicities = Counter(missing_witnesses)
    witness_pairs = sum(count * (count - 1) // 2 for count in multiplicities.values())
    edge_count = mask.bit_count()
    active_count = len(missing_witnesses)
    slack = 6 * edge_count - 7 * active_count + 2 * witness_pairs
    twice_facet_slack = sum(
        verify.local_statistics(mask, facet)[3] for facet in verify.FACETS
    )
    assert twice_facet_slack == 2 * slack
    return edge_count, active_count, witness_pairs, slack


def facet_gluing_certificate(
    patterns: tuple[tuple[tuple[int, int, int, int], ...], ...]
) -> dict[str, int]:
    """Search for a positive total objective by gluing complete facet masks."""
    assigned_before = []
    assigned = 0
    for facet_index in FACET_ORDER:
        assigned_before.append(assigned)
        assigned |= verify.FACETS[facet_index].edge_mask

    indexes = {}
    for depth, facet_index in enumerate(FACET_ORDER):
        overlap = verify.FACETS[facet_index].edge_mask & assigned_before[depth]
        by_overlap = defaultdict(list)
        for pattern in patterns[facet_index]:
            by_overlap[pattern[0] & overlap].append(pattern)
        indexes[depth] = (
            overlap,
            {key: tuple(value) for key, value in by_overlap.items()},
        )

    positive_first_facets = tuple(pattern for pattern in patterns[0] if pattern[1] > 0)
    local_maximum = max(pattern[1] for pattern in patterns[0])
    nodes = 0
    pruned = 0
    violating_leaves = []

    def visit(depth: int, values: int, objective: int) -> None:
        nonlocal nodes, pruned
        nodes += 1
        remaining = len(FACET_ORDER) - depth
        if objective + local_maximum * remaining <= 0:
            pruned += 1
            return
        if depth == len(FACET_ORDER):
            violating_leaves.append((values, objective))
            return

        facet_index = FACET_ORDER[depth]
        if depth == 0:
            choices = positive_first_facets
        else:
            overlap, by_overlap = indexes[depth]
            choices = by_overlap.get(values & overlap, ())
        facet_mask = verify.FACETS[facet_index].edge_mask
        for pattern, contribution, _, _ in choices:
            visit(
                depth + 1,
                (values & ~facet_mask) | pattern,
                objective + contribution,
            )

    visit(0, 0, 0)
    assert not violating_leaves
    return {
        "nodes": nodes,
        "pruned": pruned,
        "violating_leaves": len(violating_leaves),
    }


def edge_branch_certificate(
    patterns: tuple[tuple[tuple[int, int, int, int], ...], ...]
) -> dict[str, int]:
    """Independently search by assigning the 20 edges outside the first facet."""
    positive_first_facets = tuple(pattern for pattern in patterns[0] if pattern[1] > 0)
    first_facet_mask = verify.FACETS[0].edge_mask
    nodes = 0
    pruned = 0
    violating_leaves = []

    def visit(
        assigned: int,
        values: int,
        candidates: tuple[tuple[tuple[int, int, int, int], ...], ...],
    ) -> None:
        nonlocal nodes, pruned
        nodes += 1
        # Candidate tuples are sorted by decreasing objective.
        if sum(facet_candidates[0][1] for facet_candidates in candidates) <= 0:
            pruned += 1
            return
        if assigned == FULL_EDGE_MASK:
            objective = sum(facet_candidates[0][1] for facet_candidates in candidates)
            violating_leaves.append((values, objective))
            return

        edge = next(
            edge for edge in range(len(verify.EDGES)) if not (assigned >> edge) & 1
        )
        for bit in (0, 1):
            next_candidates = list(candidates)
            compatible = True
            for facet_index in verify.EDGE_FACETS[edge]:
                next_candidates[facet_index] = tuple(
                    pattern
                    for pattern in next_candidates[facet_index]
                    if ((pattern[0] >> edge) & 1) == bit
                )
                if not next_candidates[facet_index]:
                    compatible = False
                    break
            if compatible:
                visit(
                    assigned | (1 << edge),
                    values | (bit << edge),
                    tuple(next_candidates),
                )

    for first_pattern in positive_first_facets:
        first_mask = first_pattern[0]
        candidates = []
        for facet_index, facet in enumerate(verify.FACETS):
            if facet_index == 0:
                candidates.append((first_pattern,))
                continue
            overlap = facet.edge_mask & first_facet_mask
            candidates.append(
                tuple(
                    pattern
                    for pattern in patterns[facet_index]
                    if ((pattern[0] ^ first_mask) & overlap) == 0
                )
            )
        visit(first_facet_mask, first_mask, tuple(candidates))

    assert not violating_leaves
    return {
        "nodes": nodes,
        "pruned": pruned,
        "violating_leaves": len(violating_leaves),
    }


def verify_ratio() -> dict[str, object]:
    patterns = facet_patterns()
    assert all(len(facet_patterns_) == 2902 for facet_patterns_ in patterns)

    representative = patterns[0]
    positive = tuple(pattern for pattern in representative if pattern[1] > 0)
    assert len(positive) == 48
    assert {(pattern[2], pattern[3], pattern[1]) for pattern in positive} == {(7, 0, 14)}
    assert max(pattern[1] for pattern in representative) == 14
    assert max(
        pattern[1] for pattern in representative if pattern[0] != 0 and pattern[1] <= 0
    ) == -1

    gluing = facet_gluing_certificate(patterns)
    edge_branch = edge_branch_certificate(patterns)
    assert gluing == {"nodes": 140515, "pruned": 120236, "violating_leaves": 0}
    assert edge_branch == {"nodes": 9455, "pruned": 4340, "violating_leaves": 0}

    witness_statistics = direct_q4_statistics(WITNESS_MASK)
    assert witness_statistics == (17, 15, 3, 3)
    witness_facets = []
    for facet in verify.FACETS:
        t, q, b, twice_sigma = verify.local_statistics(WITNESS_MASK, facet)
        edge_count = (WITNESS_MASK & facet.edge_mask).bit_count()
        witness_facets.append((edge_count, t, q, b, twice_sigma))
    assert Counter(witness_facets) == Counter(
        {(7, 4, 0, 2, 0): 6, (9, 6, 3, 0, 6): 1, (0, 0, 0, 0, 0): 1}
    )

    local_table = Counter(
        (pattern[2], pattern[3], pattern[1]) for pattern in representative
    )
    certificate = {
        "edge_labels": verify.EDGES,
        "facet_order": FACET_ORDER,
        "local_table": [(*key, count) for key, count in sorted(local_table.items())],
        "gluing": gluing,
        "edge_branch": edge_branch,
        "witness_mask": f"0x{WITNESS_MASK:08x}",
        "witness_statistics": witness_statistics,
        "witness_facets": witness_facets,
    }
    certificate_hash = hashlib.sha256(
        json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()

    return {
        "q3_squarefree_patterns": len(representative),
        "q3_positive_objective_patterns": len(positive),
        "q3_positive_objective_signature": "(edges=7,twice_sigma=0,lambda=14)",
        "facet_gluing_nodes": gluing["nodes"],
        "facet_gluing_pruned": gluing["pruned"],
        "facet_gluing_violations": gluing["violating_leaves"],
        "edge_branch_nodes": edge_branch["nodes"],
        "edge_branch_pruned": edge_branch["pruned"],
        "edge_branch_violations": edge_branch["violating_leaves"],
        "witness_mask": f"0x{WITNESS_MASK:08x}",
        "witness_edges": witness_statistics[0],
        "witness_active_squares": witness_statistics[1],
        "witness_pairs": witness_statistics[2],
        "witness_slack": witness_statistics[3],
        "witness_ratio": str(Fraction(witness_statistics[3], witness_statistics[0])),
        "certificate_sha256": certificate_hash,
        "bound": "sat(Q_d,Q_2) >= 119*d*2^d/(66*d+172) for d>=4",
        "asymptotic_constant": "119/66",
        "improvement_over_7/4": "7/132",
    }


def main() -> None:
    for key, value in verify_ratio().items():
        print(f"{key}={value}")
    print("status=PASS")


if __name__ == "__main__":
    main()
