#!/usr/bin/env python3
"""Build the compact certificate for the complete Cyclic(43) q=12 boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def require_equal(name: str, left: Any, right: Any) -> None:
    if left != right:
        raise ValueError(f"independent mismatch for {name}: {left!r} != {right!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("optimized_summary", type=Path)
    parser.add_argument("direct_summary", type=Path)
    parser.add_argument("full_targets", type=Path)
    parser.add_argument("optimized_q11_frontier", type=Path)
    parser.add_argument("direct_q11_frontier", type=Path)
    args = parser.parse_args()

    optimized = json.loads(args.optimized_summary.read_text())
    direct = json.loads(args.direct_summary.read_text())
    comparisons = {
        "frontier_rotation_orbit_count": (
            optimized["objective_twelve_frontier_rotation_orbit_count"],
            direct["direct_frontier_rotation_orbit_count"],
        ),
        "frontier_quotient_incidence": (
            optimized["frontier_quotient_incidence"],
            direct["direct_frontier_quotient_incidence"],
        ),
        "distinct_source_target_pairs": (
            optimized["distinct_source_target_pairs"],
            direct["direct_distinct_source_target_pairs"],
        ),
        "source_target_parallel_edge_excess": (
            optimized["source_target_parallel_edge_excess"],
            direct["direct_source_target_parallel_edge_excess"],
        ),
        "q11_derived_target_count": (
            optimized["q11_derived_target_count"],
            direct["direct_q11_derived_target_count"],
        ),
        "lower_only_target_count": (
            optimized["lower_only_target_count"],
            direct["direct_lower_only_target_count"],
        ),
        "q11_only_target_count": (
            optimized["q11_only_target_count"],
            direct["direct_q11_only_target_count"],
        ),
        "mixed_lower_q11_target_count": (
            optimized["mixed_lower_q11_target_count"],
            direct["direct_mixed_lower_q11_target_count"],
        ),
        "raw_incidence_by_source_objective": (
            optimized["raw_incidence_by_source_objective"],
            direct["raw_incidence_by_source_objective"],
        ),
        "distinct_pair_count_by_source_objective": (
            optimized["distinct_pair_count_by_source_objective"],
            direct["distinct_pair_count_by_source_objective"],
        ),
        "source_distinct_target_degree_histogram_by_objective": (
            optimized["source_distinct_target_degree_histogram_by_objective"],
            direct["source_distinct_target_degree_histogram_by_objective"],
        ),
    }
    for name, (left, right) in comparisons.items():
        require_equal(name, left, right)
    if not optimized["all_internal_checks_pass"]:
        raise ValueError("optimized internal checks failed")
    if not direct["all_direct_checks_pass"]:
        raise ValueError("direct checks failed")

    certificate = {
        "order": optimized["order"],
        "edge_count": optimized["edge_count"],
        "primary_sublevel_ten_source_rotation_orbit_count": optimized[
            "primary_sublevel_ten_source_rotation_orbit_count"
        ],
        "complete_objective_eleven_source_rotation_orbit_count": optimized[
            "complete_objective_eleven_source_rotation_orbit_count"
        ],
        "total_source_rotation_orbit_count": direct[
            "direct_source_rotation_orbit_count"
        ],
        "objective_twelve_frontier_rotation_orbit_count": optimized[
            "objective_twelve_frontier_rotation_orbit_count"
        ],
        "objective_twelve_frontier_vertex_count": optimized[
            "objective_twelve_frontier_vertex_count"
        ],
        "frontier_quotient_incidence": optimized["frontier_quotient_incidence"],
        "frontier_labeled_incidence": optimized["frontier_labeled_incidence"],
        "distinct_source_target_pairs": optimized[
            "distinct_source_target_pairs"
        ],
        "source_target_parallel_edge_excess": optimized[
            "source_target_parallel_edge_excess"
        ],
        "lower_derived_target_count": direct["direct_lower_derived_target_count"],
        "q11_derived_target_count": optimized["q11_derived_target_count"],
        "lower_only_target_count": optimized["lower_only_target_count"],
        "q11_only_target_count": optimized["q11_only_target_count"],
        "mixed_lower_q11_target_count": optimized[
            "mixed_lower_q11_target_count"
        ],
        "all_boundary_targets_adjacent_to_q11_layer": optimized[
            "all_boundary_targets_adjacent_to_q11_layer"
        ],
        "first_frontier_only_q11_target_count": optimized[
            "first_frontier_only_q11_target_count"
        ],
        "addition_only_q11_target_count": optimized[
            "addition_only_q11_target_count"
        ],
        "mixed_first_addition_q11_target_count": optimized[
            "mixed_first_addition_q11_target_count"
        ],
        "shadow_boundary_target_count_expected": optimized[
            "shadow_boundary_target_count_expected"
        ],
        "shadow_boundary_target_count_found": optimized[
            "shadow_boundary_target_count_found"
        ],
        "source_count_by_objective": optimized["source_count_by_objective"],
        "raw_incidence_by_source_objective": optimized[
            "raw_incidence_by_source_objective"
        ],
        "distinct_pair_count_by_source_objective": optimized[
            "distinct_pair_count_by_source_objective"
        ],
        "target_source_degree_histogram": optimized[
            "target_source_degree_histogram"
        ],
        "target_q11_source_degree_histogram": optimized[
            "target_q11_source_degree_histogram"
        ],
        "target_lower_source_degree_histogram": optimized[
            "target_lower_source_degree_histogram"
        ],
        "target_minimum_source_objective_histogram": optimized[
            "target_minimum_source_objective_histogram"
        ],
        "lower_only_target_minimum_source_objective_histogram": optimized[
            "lower_only_target_minimum_source_objective_histogram"
        ],
        "lower_only_target_source_degree_histogram": optimized[
            "lower_only_target_source_degree_histogram"
        ],
        "q11_boundary_bipartite_components": optimized[
            "q11_boundary_bipartite_components"
        ],
        "full_boundary_bipartite_components": optimized[
            "full_boundary_bipartite_components"
        ],
        "source_degree_histograms_sha256_canonical_json": canonical_json_sha256(
            optimized["source_distinct_target_degree_histogram_by_objective"]
        ),
        "optimized_summary_sha256": sha256(args.optimized_summary),
        "direct_summary_sha256": sha256(args.direct_summary),
        "temporary_full_target_file_sha256": sha256(args.full_targets),
        "optimized_q11_frontier_input_sha256": sha256(
            args.optimized_q11_frontier
        ),
        "direct_q11_frontier_input_sha256": sha256(args.direct_q11_frontier),
        "direct_five_set_evaluations": (
            direct["direct_source_rotation_orbit_count"] * 962_598
        ),
        "direct_unexpected_targets": direct["unexpected_targets"],
        "direct_omitted_targets": direct["omitted_targets"],
        "direct_objective_errors": direct["objective_errors"],
        "direct_nonfree_target_encounters": direct[
            "nonfree_target_encounters"
        ],
        "independently_agreed_fields": sorted(comparisons),
        "all_optimized_checks_pass": optimized["all_internal_checks_pass"],
        "all_direct_checks_pass": direct["all_direct_checks_pass"],
        "scope_note": optimized["scope_note"],
    }
    json.dump(certificate, fp=__import__("sys").stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
