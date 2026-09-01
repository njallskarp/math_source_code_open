#!/usr/bin/env python3
"""Independently reconstruct q=12 boundary components from a binary edge stream."""

from __future__ import annotations

import argparse
from array import array
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def union_stream(
    records: np.ndarray,
    source_base: int,
    source_count: int,
    target_count: int,
) -> np.ndarray:
    """Return fully compressed parents for the selected contiguous source range."""
    node_count = source_count + target_count
    parent_storage = array("I", range(node_count))
    parent = memoryview(parent_storage)
    rank = bytearray(node_count)
    flat = records.reshape(-1)
    for position in range(0, flat.size, 2):
        global_source = int(flat[position])
        if global_source < source_base:
            continue
        source = global_source - source_base
        if source >= source_count:
            continue
        target = source_count + int(flat[position + 1])

        left = source
        while parent[left] != left:
            parent[left] = parent[parent[left]]
            left = parent[left]
        right = target
        while parent[right] != right:
            parent[right] = parent[parent[right]]
            right = parent[right]
        if left == right:
            continue
        if rank[left] < rank[right]:
            left, right = right, left
        parent[right] = left
        if rank[left] == rank[right]:
            rank[left] += 1

    parents = np.frombuffer(parent_storage, dtype=np.uint32)
    while True:
        grandparents = parents[parents]
        if np.array_equal(grandparents, parents):
            break
        parents[:] = grandparents
    return parents.copy()


def component_profiles(
    records: np.ndarray,
    source_base: int,
    source_count: int,
    target_count: int,
) -> tuple[list[dict[str, int]], np.ndarray, np.ndarray, np.ndarray]:
    parents = union_stream(records, source_base, source_count, target_count)
    selected = records[records[:, 0] >= source_base]
    selected = selected[selected[:, 0] < source_base + source_count]
    active_sources = np.unique(selected[:, 0]).astype(np.uint32)
    active_targets = np.unique(selected[:, 1]).astype(np.uint32)
    source_roots = parents[active_sources - source_base]
    target_roots = parents[source_count + active_targets]
    edge_roots = parents[selected[:, 0] - source_base]

    source_counts = np.bincount(source_roots, minlength=parents.size)
    target_counts = np.bincount(target_roots, minlength=parents.size)
    edge_counts = np.bincount(edge_roots, minlength=parents.size)
    roots = np.flatnonzero(target_counts)
    profiles = []
    for root in roots:
        sources = int(source_counts[root])
        targets = int(target_counts[root])
        edges = int(edge_counts[root])
        profiles.append(
            {
                "source_vertices": sources,
                "target_vertices": targets,
                "edges": edges,
                "cycle_rank": edges - sources - targets + 1,
                "root": int(root),
            }
        )
    profiles.sort(
        key=lambda item: (
            item["source_vertices"] + item["target_vertices"],
            item["edges"],
        ),
        reverse=True,
    )
    return profiles, active_sources, source_roots, target_roots


def without_roots(profiles: list[dict[str, int]]) -> list[dict[str, int]]:
    return [
        {key: value for key, value in profile.items() if key != "root"}
        for profile in profiles
    ]


def decode_state(words: np.ndarray) -> list[int]:
    edges: list[int] = []
    for word_index, raw_word in enumerate(words):
        word = int(raw_word)
        while word:
            low_bit = word & -word
            bit = low_bit.bit_length() - 1
            edge = 64 * word_index + bit
            if edge < 903:
                edges.append(edge)
            word ^= low_bit
    return edges


def edge_vertices(edge: int, order: int = 43) -> list[int]:
    """Invert the lexicographic K_order edge numbering used by the C++ code."""
    cursor = 0
    for left in range(order):
        row_size = order - left - 1
        if edge < cursor + row_size:
            return [left, left + 1 + edge - cursor]
        cursor += row_size
    raise ValueError(f"edge id {edge} is outside K_{order}")


def cycle_edge_position(pair: list[int], order: int = 43) -> int | None:
    """Return the C_order edge position, or None for a non-cycle edge."""
    left, right = pair
    if right == left + 1:
        return left
    if left == 0 and right == order - 1:
        return order - 1
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("incidences", type=Path)
    parser.add_argument("source_states", type=Path)
    parser.add_argument("source_objectives", type=Path)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    metadata: dict[str, Any] = json.loads(args.metadata.read_text())
    certificate: dict[str, Any] = json.loads(args.certificate.read_text())
    source_count = int(metadata["source_count"])
    lower_source_count = int(metadata["lower_source_count"])
    q11_source_count = int(metadata["q11_source_count"])
    target_count = int(metadata["target_count"])
    incidence_count = int(metadata["incidence_count"])

    if args.incidences.stat().st_size != 8 * incidence_count:
        raise ValueError("incidence stream size mismatch")
    if args.source_states.stat().st_size != source_count * 15 * 8:
        raise ValueError("source-state stream size mismatch")
    if args.source_objectives.stat().st_size != source_count:
        raise ValueError("source-objective stream size mismatch")

    records = np.memmap(
        args.incidences, mode="r", dtype="<u4", shape=(incidence_count, 2)
    )
    if int(records[:, 0].max()) >= source_count:
        raise ValueError("source id outside declared range")
    if int(records[:, 1].max()) >= target_count:
        raise ValueError("target id outside declared range")

    full_profiles, active_sources, full_source_roots, full_target_roots = (
        component_profiles(records, 0, source_count, target_count)
    )
    q11_profiles, q11_active_sources, _, _ = component_profiles(
        records, lower_source_count, q11_source_count, target_count
    )
    public_full_profiles = without_roots(full_profiles)
    public_q11_profiles = without_roots(q11_profiles)

    source_states = np.memmap(
        args.source_states, mode="r", dtype="<u8", shape=(source_count, 15)
    )
    source_objectives = np.memmap(
        args.source_objectives, mode="r", dtype="u1", shape=(source_count,)
    )
    all_target_ids = np.arange(target_count, dtype=np.uint32)
    stars = []
    for profile in full_profiles:
        if profile["source_vertices"] != 1 or profile["cycle_rank"] != 0:
            continue
        root = profile["root"]
        source_matches = active_sources[full_source_roots == root]
        target_matches = all_target_ids[full_target_roots == root]
        if source_matches.size != 1:
            raise ValueError("star source recovery mismatch")
        source_id = int(source_matches[0])
        state_edges = decode_state(source_states[source_id])
        state_edge_pairs = [edge_vertices(edge) for edge in state_edges]
        cycle_positions = [
            cycle_edge_position(pair) for pair in state_edge_pairs
        ]
        stars.append(
            {
                "source_id": source_id,
                "source_objective": int(source_objectives[source_id]),
                "source_state_edges": state_edges,
                "source_state_edge_pairs": state_edge_pairs,
                "source_state_uses_only_cycle_edges": all(
                    position is not None for position in cycle_positions
                ),
                "source_cycle_edge_positions": cycle_positions,
                "target_ids_in_sorted_frontier": [
                    int(value) for value in target_matches
                ],
                "target_count": int(target_matches.size),
                "edge_count": profile["edges"],
            }
        )
    stars.sort(key=lambda item: item["target_count"], reverse=True)
    star_state_symmetric_difference = sorted(
        set(stars[0]["source_state_edges"])
        ^ set(stars[1]["source_state_edges"])
    )

    expected_full = certificate["full_boundary_bipartite_components"]
    expected_q11 = certificate["q11_boundary_bipartite_components"]
    full_cycle_rank = sum(item["cycle_rank"] for item in public_full_profiles)
    q11_cycle_rank = sum(item["cycle_rank"] for item in public_q11_profiles)
    full_profile_match = public_full_profiles == expected_full["components"]
    q11_summary_match = (
        len(public_q11_profiles) == expected_q11["component_count"]
        and q11_cycle_rank == expected_q11["cycle_rank"]
        and public_q11_profiles[0]["source_vertices"]
        == expected_q11["largest_component_source_vertices"]
        and public_q11_profiles[0]["target_vertices"]
        == expected_q11["largest_component_target_vertices"]
        and public_q11_profiles[0]["edges"]
        == expected_q11["largest_component_edges"]
        and public_q11_profiles[0]["cycle_rank"]
        == expected_q11["largest_component_cycle_rank"]
    )
    all_checks = (
        metadata["all_stream_checks_pass"]
        and full_profile_match
        and q11_summary_match
        and len(active_sources) == 563_783
        and len(q11_active_sources) == 372_716
        and sum(item["target_vertices"] for item in public_full_profiles)
        == target_count
        and sum(item["edges"] for item in public_full_profiles)
        == incidence_count
        and full_cycle_rank == expected_full["cycle_rank"]
        and len(stars) == 2
        and [item["target_count"] for item in stars] == [15, 12]
        and [item["source_objective"] for item in stars] == [8, 8]
        and all(item["source_state_uses_only_cycle_edges"] for item in stars)
        and len(star_state_symmetric_difference) == 7
    )

    output = {
        "order": 43,
        "edge_count": 903,
        "source_count": source_count,
        "active_source_count": int(len(active_sources)),
        "inactive_source_count": source_count - int(len(active_sources)),
        "target_count": target_count,
        "incidence_count": incidence_count,
        "full_component_count": len(public_full_profiles),
        "full_cycle_rank": full_cycle_rank,
        "full_components": public_full_profiles,
        "q11_active_source_count": int(len(q11_active_sources)),
        "q11_inactive_source_count": q11_source_count
        - int(len(q11_active_sources)),
        "q11_component_count": len(public_q11_profiles),
        "q11_cycle_rank": q11_cycle_rank,
        "q11_largest_component": public_q11_profiles[0],
        "exceptional_star_components": stars,
        "exceptional_source_state_symmetric_difference": (
            star_state_symmetric_difference
        ),
        "exceptional_source_state_hamming_distance": len(
            star_state_symmetric_difference
        ),
        "full_profile_match": full_profile_match,
        "q11_summary_match": q11_summary_match,
        "incidence_stream_sha256": sha256(args.incidences),
        "source_states_sha256": sha256(args.source_states),
        "source_objectives_sha256": sha256(args.source_objectives),
        "stream_metadata_sha256": sha256(args.metadata),
        "all_independent_topology_checks_pass": all_checks,
        "method": (
            "independent Python union-find over the complete little-endian "
            "incidence stream, with NumPy memory maps and vectorized final "
            "path compression; no C++ disjoint-set code is reused"
        ),
        "scope_note": (
            "This independently reconstructs the persisted q12 boundary "
            "topology and identifies its two star sources; endpoint "
            "enumeration still uses the certified C++ incidence streamer."
        ),
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    if not all_checks:
        raise SystemExit("independent topology checks failed")


if __name__ == "__main__":
    main()
