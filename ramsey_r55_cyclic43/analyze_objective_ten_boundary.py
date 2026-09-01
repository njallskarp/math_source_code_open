#!/usr/bin/env python3
"""Derive exact structural corollaries from the objective-ten certificates."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def state_key(edges: list[int]) -> tuple[int, ...]:
    if edges != sorted(set(edges)):
        raise ValueError("state edge list is not strictly sorted")
    return tuple(edges)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("objective_nine_frontier", type=Path)
    parser.add_argument("objective_nine_component", type=Path)
    parser.add_argument("objective_ten_frontier", type=Path)
    parser.add_argument("objective_ten_independent", type=Path)
    args = parser.parse_args()

    nine_frontier = load(args.objective_nine_frontier)
    nine_component = load(args.objective_nine_component)
    ten_frontier = load(args.objective_ten_frontier)
    independent = load(args.objective_ten_independent)

    first_nine = {
        state_key(state)
        for state in nine_frontier["objective_nine_rotation_representatives"]
    }
    new_nine = nine_component["new_objective_9_rotation_representatives"]
    exceptional_indices = independent[
        "objective_nine_layer_indices_without_objective_ten_exit"
    ]
    if len(first_nine) != 42_661 or len(new_nine) != 42_781:
        raise ValueError("unexpected objective-nine certificate size")
    if len(exceptional_indices) != len(set(exceptional_indices)):
        raise ValueError("duplicate exceptional objective-nine index")
    if any(index < 0 or index >= len(new_nine) for index in exceptional_indices):
        raise ValueError("exceptional objective-nine index out of range")
    exceptional_in_first_frontier = sum(
        state_key(new_nine[index]) in first_nine for index in exceptional_indices
    )

    signatures = ten_frontier[
        "objective_ten_incidence_signatures_2_through_9"
    ]
    targets = ten_frontier["objective_ten_rotation_representatives"]
    if len(signatures) != 128_184 or len(targets) != len(signatures):
        raise ValueError("unexpected objective-ten certificate size")

    minimum_source = Counter()
    maximum_source = Counter()
    support_size = Counter()
    source_coverage = Counter()
    support_masks = Counter()
    for signature in signatures:
        if len(signature) != 8 or any(
            not isinstance(value, int) or value < 0 for value in signature
        ):
            raise ValueError("invalid objective-ten incidence signature")
        support = [
            objective
            for objective, value in zip(range(2, 10), signature, strict=True)
            if value
        ]
        if not support:
            raise ValueError("objective-ten target has empty source support")
        minimum_source[min(support)] += 1
        maximum_source[max(support)] += 1
        support_size[len(support)] += 1
        support_masks[sum(1 << objective for objective in support)] += 1
        source_coverage.update(support)

    cumulative_minimum_source: dict[str, int] = {}
    cumulative = 0
    for objective in range(2, 10):
        cumulative += minimum_source[objective]
        cumulative_minimum_source[str(objective)] = cumulative

    if sum(minimum_source.values()) != 128_184:
        raise ValueError("minimum-source partition does not cover the frontier")
    if independent["simple_quotient_boundary_edge_count"] != 500_397:
        raise ValueError("unexpected simple quotient boundary size")
    if independent["quotient_boundary_incidence_count"] != 500_400:
        raise ValueError("unexpected quotient incidence count")
    if independent["parallel_quotient_incidence_excess"] != 3:
        raise ValueError("unexpected parallel quotient incidence excess")

    result = {
        "objective_nine_sources_without_objective_ten_exit": len(
            exceptional_indices
        ),
        "exceptional_sources_in_first_objective_nine_frontier": (
            exceptional_in_first_frontier
        ),
        "all_exceptional_sources_are_in_first_objective_nine_frontier": (
            exceptional_in_first_frontier == len(exceptional_indices)
        ),
        "minimum_external_objective_histogram": independent[
            "source_minimum_external_objective_histogram"
        ],
        "simple_quotient_boundary_edge_count": independent[
            "simple_quotient_boundary_edge_count"
        ],
        "quotient_boundary_incidence_count": independent[
            "quotient_boundary_incidence_count"
        ],
        "parallel_quotient_incidence_excess": independent[
            "parallel_quotient_incidence_excess"
        ],
        "objective_ten_indices_with_parallel_boundary_incidence": independent[
            "objective_ten_layer_indices_with_parallel_boundary_incidence"
        ],
        "objective_ten_targets_by_minimum_source_objective": {
            str(key): value for key, value in sorted(minimum_source.items())
        },
        "objective_ten_targets_by_maximum_source_objective": {
            str(key): value for key, value in sorted(maximum_source.items())
        },
        "objective_ten_targets_by_number_of_source_objective_layers": {
            str(key): value for key, value in sorted(support_size.items())
        },
        "objective_ten_target_coverage_by_source_objective": {
            str(key): value for key, value in sorted(source_coverage.items())
        },
        "distinct_source_objective_support_patterns": len(support_masks),
        "cumulative_targets_with_minimum_source_objective_at_most": (
            cumulative_minimum_source
        ),
        "method": (
            "exact deterministic intersection and support analysis of the "
            "persisted objective-nine and objective-ten orbit certificates"
        ),
        "scope_note": (
            "This derives structure within the certified primary Cyclic(43) "
            "threshold-nine boundary; it does not classify disconnected "
            "sublevel-nine components or determine R(5,5)."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=False))


if __name__ == "__main__":
    main()
