#!/usr/bin/env python3
"""Exact radius-three rigidity around a certified two-coloring of K43."""

from __future__ import annotations

import argparse
import itertools
import json
from array import array
from pathlib import Path

from local_rigidity import (
    complete_graph_edges,
    direct_count,
    initial_colors,
    is_monochromatic,
)
from solve_cyclic43 import ORDER, edge, load_certificate


def analyze_radius_three(certificate: Path) -> dict[str, object]:
    flips = load_certificate(certificate)
    colors, edges = initial_colors(flips)
    edge_ids = {e: i for i, e in enumerate(edges)}
    edge_count = len(edges)
    base_count, base_witnesses = direct_count(colors, edge_ids)
    if base_count != 2:
        raise ValueError(f"expected an optimum-2 certificate, got {base_count}")

    relevant = sorted(
        {
            edge_ids[edge(a, b)]
            for vertices in base_witnesses
            for a, b in itertools.combinations(vertices, 2)
        }
    )
    relevant_set = set(relevant)
    row_of = {edge_id: row for row, edge_id in enumerate(relevant)}
    single_delta = array("i", [0]) * edge_count
    pair_interaction = array("h", [0]) * (edge_count * edge_count)
    triple_interaction = array("h", [0]) * (
        len(relevant) * edge_count * edge_count
    )

    for vertices in itertools.combinations(range(ORDER), 5):
        ids = [
            edge_ids[edge(a, b)] for a, b in itertools.combinations(vertices, 2)
        ]
        directions = [-1 if colors[edge_id] else 1 for edge_id in ids]
        red_count = sum(colors[edge_id] for edge_id in ids)
        mono0 = is_monochromatic(red_count)
        mono1 = [
            is_monochromatic(red_count + directions[i]) for i in range(10)
        ]
        mono2 = [[0] * 10 for _ in range(10)]

        for i, edge_id in enumerate(ids):
            single_delta[edge_id] += mono1[i] - mono0

        for i in range(10):
            first = ids[i]
            for j in range(i + 1, 10):
                second = ids[j]
                value = is_monochromatic(
                    red_count + directions[i] + directions[j]
                )
                mono2[i][j] = value
                mono2[j][i] = value
                correction = value - mono1[i] - mono1[j] + mono0
                low, high = sorted((first, second))
                pair_interaction[low * edge_count + high] += correction

        for i, first in enumerate(ids):
            row = row_of.get(first)
            if row is None:
                continue
            row_offset = row * edge_count * edge_count
            remaining = [position for position in range(10) if position != i]
            for offset, j in enumerate(remaining):
                second = ids[j]
                for k in remaining[offset + 1 :]:
                    third = ids[k]
                    mono3 = is_monochromatic(
                        red_count + directions[i] + directions[j] + directions[k]
                    )
                    correction = (
                        mono3
                        - mono2[i][j]
                        - mono2[i][k]
                        - mono2[j][k]
                        + mono1[i]
                        + mono1[j]
                        + mono1[k]
                        - mono0
                    )
                    low, high = sorted((second, third))
                    triple_interaction[
                        row_offset + low * edge_count + high
                    ] += correction

    minimum: int | None = None
    minimizer_count = 0
    examined_candidate_count = 0
    sample: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] | None = None

    for anchor in relevant:
        row_offset = row_of[anchor] * edge_count * edge_count
        # Use the least relevant edge in each triple as its unique anchor.
        allowed = [
            candidate
            for candidate in range(edge_count)
            if candidate != anchor
            and not (candidate in relevant_set and candidate < anchor)
        ]
        for offset, second in enumerate(allowed):
            for third in allowed[offset + 1 :]:
                examined_candidate_count += 1
                ids = sorted((anchor, second, third))
                first_id, second_id, third_id = ids
                pair_correction = (
                    pair_interaction[first_id * edge_count + second_id]
                    + pair_interaction[first_id * edge_count + third_id]
                    + pair_interaction[second_id * edge_count + third_id]
                )
                other_low, other_high = sorted((second, third))
                triple_correction = triple_interaction[
                    row_offset + other_low * edge_count + other_high
                ]
                count = (
                    base_count
                    + single_delta[first_id]
                    + single_delta[second_id]
                    + single_delta[third_id]
                    + pair_correction
                    + triple_correction
                )
                if minimum is None or count < minimum:
                    minimum = count
                    minimizer_count = 1
                    sample = (edges[first_id], edges[second_id], edges[third_id])
                elif count == minimum:
                    minimizer_count += 1

    assert minimum is not None and sample is not None
    sample_colors = colors.copy()
    for changed_edge in sample:
        sample_colors[edge_ids[changed_edge]] = not sample_colors[edge_ids[changed_edge]]
    direct_sample_count, witnesses = direct_count(sample_colors, edge_ids)
    if direct_sample_count != minimum:
        raise AssertionError((direct_sample_count, minimum, sample))

    return {
        "certificate": certificate.name,
        "base_monochromatic_k5_count": base_count,
        "base_monochromatic_k5": base_witnesses,
        "complete_graph_edge_count": edge_count,
        "relevant_edge_count": len(relevant),
        "radius_three_minimum": minimum,
        "radius_three_examined_candidate_count": examined_candidate_count,
        "radius_three_examined_minimizer_count": minimizer_count,
        "radius_three_minimizer_sample": sample,
        "radius_three_sample_monochromatic_k5": witnesses,
        "scope_note": (
            "Every examined triple contains an edge of a base monochromatic K5. "
            "Every omitted triple leaves both base K5s monochromatic and cannot "
            "have count below two."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze_radius_three(args.certificate)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
