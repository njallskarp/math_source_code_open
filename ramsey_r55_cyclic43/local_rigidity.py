#!/usr/bin/env python3
"""Exact radius-one and radius-two rigidity around a certified K43 coloring.

For a fixed two-coloring, toggling two edges has an exactly decomposable effect
on the monochromatic-K5 count: the two single-edge deltas plus a correction from
five-sets containing both edges.  This script computes every required delta and
correction by enumerating the 962,598 five-sets once, then checks every edge
toggle and every relevant edge pair exactly.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from solve_cyclic43 import ORDER, edge, load_certificate, red_edge_variables


def complete_graph_edges() -> tuple[dict[tuple[int, int], int], list[tuple[int, int]]]:
    edges = [(a, b) for a in range(ORDER) for b in range(a + 1, ORDER)]
    return {e: i for i, e in enumerate(edges)}, edges


def initial_colors(flips: set[tuple[int, int]]) -> tuple[list[bool], list[tuple[int, int]]]:
    red_variables, _ = red_edge_variables()
    _, edges = complete_graph_edges()
    return [e in red_variables and e not in flips for e in edges], edges


def is_monochromatic(red_count: int) -> int:
    return int(red_count == 0 or red_count == 10)


def direct_count(colors: list[bool], edge_ids: dict[tuple[int, int], int]) -> tuple[int, list[tuple[int, ...]]]:
    witnesses: list[tuple[int, ...]] = []
    for vertices in itertools.combinations(range(ORDER), 5):
        red_count = sum(
            colors[edge_ids[edge(a, b)]]
            for a, b in itertools.combinations(vertices, 2)
        )
        if is_monochromatic(red_count):
            witnesses.append(vertices)
    return len(witnesses), witnesses


def analyze(certificate: Path) -> dict[str, object]:
    flips = load_certificate(certificate)
    colors, edges = initial_colors(flips)
    edge_ids = {e: i for i, e in enumerate(edges)}
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
    row_of = {edge_id: row for row, edge_id in enumerate(relevant)}
    single_delta = [0] * len(edges)
    interaction = [[0] * len(edges) for _ in relevant]

    for vertices in itertools.combinations(range(ORDER), 5):
        ids = [
            edge_ids[edge(a, b)] for a, b in itertools.combinations(vertices, 2)
        ]
        red_count = sum(colors[edge_id] for edge_id in ids)
        base_mono = is_monochromatic(red_count)
        directions = {
            edge_id: (-1 if colors[edge_id] else 1) for edge_id in ids
        }
        single_mono = {
            edge_id: is_monochromatic(red_count + directions[edge_id])
            for edge_id in ids
        }

        for edge_id in ids:
            single_delta[edge_id] += single_mono[edge_id] - base_mono

        for first in ids:
            row = row_of.get(first)
            if row is None:
                continue
            for second in ids:
                if first == second:
                    continue
                both_mono = is_monochromatic(
                    red_count + directions[first] + directions[second]
                )
                interaction[row][second] += (
                    both_mono
                    - single_mono[first]
                    - single_mono[second]
                    + base_mono
                )

    radius_one_counts = [base_count + delta for delta in single_delta]
    radius_one_minimum = min(radius_one_counts)
    radius_one_minimizers = [
        edges[i] for i, count in enumerate(radius_one_counts) if count == radius_one_minimum
    ]

    radius_two_minimum: int | None = None
    radius_two_minimizers: list[tuple[tuple[int, int], tuple[int, int]]] = []
    radius_two_examined_candidate_count = 0
    relevant_set = set(relevant)
    for first in range(len(edges)):
        for second in range(first + 1, len(edges)):
            if first not in relevant_set and second not in relevant_set:
                # Such a pair leaves both base monochromatic K5s intact, so it
                # cannot improve on the base count of two.
                continue
            radius_two_examined_candidate_count += 1
            if first in row_of:
                correction = interaction[row_of[first]][second]
            else:
                correction = interaction[row_of[second]][first]
            count = (
                base_count
                + single_delta[first]
                + single_delta[second]
                + correction
            )
            if radius_two_minimum is None or count < radius_two_minimum:
                radius_two_minimum = count
                radius_two_minimizers = [(edges[first], edges[second])]
            elif count == radius_two_minimum:
                radius_two_minimizers.append((edges[first], edges[second]))

    assert radius_two_minimum is not None
    sample_pair = radius_two_minimizers[0]
    sample_colors = colors.copy()
    for changed_edge in sample_pair:
        sample_colors[edge_ids[changed_edge]] = not sample_colors[edge_ids[changed_edge]]
    direct_sample_count, direct_sample_witnesses = direct_count(sample_colors, edge_ids)
    if direct_sample_count != radius_two_minimum:
        raise AssertionError((direct_sample_count, radius_two_minimum, sample_pair))

    return {
        "certificate": certificate.name,
        "base_monochromatic_k5_count": base_count,
        "base_monochromatic_k5": base_witnesses,
        "complete_graph_edge_count": len(edges),
        "relevant_edge_count": len(relevant),
        "radius_one_minimum": radius_one_minimum,
        "radius_one_minimizer_count": len(radius_one_minimizers),
        "radius_one_minimizers": radius_one_minimizers,
        "radius_two_minimum": radius_two_minimum,
        "radius_two_examined_candidate_count": radius_two_examined_candidate_count,
        "radius_two_examined_minimizer_count": len(radius_two_minimizers),
        "radius_two_minimizer_sample": sample_pair,
        "radius_two_sample_monochromatic_k5": direct_sample_witnesses,
        "scope_note": (
            "The radius-two improvement search examines only pairs touching a "
            "base monochromatic K5. Every omitted pair leaves both base K5s "
            "monochromatic and therefore cannot have count below two."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(args.certificate)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
