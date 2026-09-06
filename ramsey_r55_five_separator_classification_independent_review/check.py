#!/usr/bin/env python3
"""Clean-room check of the dense five-separator Ramsey lemma.

This checker consumes only the target's compact inputs.json.  It does not
import target code.  Its finite connectivity proof enumerates vertex-set
boundaries, rather than either target method (deleted-set traversal or
vertex-splitting flow).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Iterable


TARGET_COMMIT = "e5eff475fe1d86f9bca55649e183637611423e01"
INPUT_SHA256 = "1d025db88615f7dfa93bb33a4179db87137328877d3eea99fc7a80774c0c2105"
EXPECTED_COMPONENT_PROFILES = (
    (2, 17, 3),
    (3, 16, 3),
    (3, 17, 2),
    (4, 15, 3),
    (4, 16, 2),
    (4, 17, 1),
    (5, 14, 3),
    (5, 15, 2),
    (5, 16, 1),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def decode_graph6(record: str) -> tuple[int, ...]:
    """Decode a strict short graph6 record into integer adjacency rows."""
    require(isinstance(record, str) and record != "", "empty graph6 record")
    require(all(63 <= ord(char) <= 126 for char in record), "bad graph6 character")
    values = [ord(char) - 63 for char in record]
    n = values[0]
    require(n <= 62, "only short graph6 records are accepted")
    edge_count = n * (n - 1) // 2
    require(len(values) == 1 + (edge_count + 5) // 6, "bad graph6 length")

    rows = [0] * n
    for index, (low, high) in enumerate(
        (pair for high in range(n) for pair in ((low, high) for low in range(high)))
    ):
        bit = (values[1 + index // 6] >> (5 - index % 6)) & 1
        if bit:
            rows[low] |= 1 << high
            rows[high] |= 1 << low

    for index in range(edge_count, 6 * (len(values) - 1)):
        require(
            ((values[1 + index // 6] >> (5 - index % 6)) & 1) == 0,
            "nonzero graph6 padding",
        )
    return tuple(rows)


def encode_graph6(rows: tuple[int, ...]) -> str:
    """Definition-level encoder used only by the small-graph controls."""
    n = len(rows)
    require(n <= 62, "only short graph6 records are accepted")
    bits = [((rows[low] >> high) & 1) for high in range(n) for low in range(high)]
    bits.extend([0] * (-len(bits) % 6))
    payload = []
    for start in range(0, len(bits), 6):
        value = sum(bits[start + offset] << (5 - offset) for offset in range(6))
        payload.append(chr(63 + value))
    return chr(63 + n) + "".join(payload)


def validate_rows(rows: tuple[int, ...]) -> None:
    n = len(rows)
    full = (1 << n) - 1
    for vertex, row in enumerate(rows):
        require(type(row) is int and 0 <= row <= full, "bad adjacency row")
        require((row >> vertex) & 1 == 0, "loop in graph")
        for other in range(n):
            require(
                ((row >> other) & 1) == ((rows[other] >> vertex) & 1),
                "asymmetric graph",
            )


def connected_after(rows: tuple[int, ...], removed: int = 0) -> bool:
    remaining = ((1 << len(rows)) - 1) & ~removed
    if remaining == 0:
        return True
    reached = remaining & -remaining
    while True:
        frontier = reached
        neighbors = 0
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            neighbors |= rows[bit.bit_length() - 1]
        expanded = reached | (neighbors & remaining)
        if expanded == reached:
            return reached == remaining
        reached = expanded


def edge_digest(rows: tuple[int, ...]) -> str:
    edges = [
        [low, high]
        for low, high in combinations(range(len(rows)), 2)
        if (rows[low] >> high) & 1
    ]
    raw = (json.dumps(edges, separators=(",", ":")) + "\n").encode()
    return sha256(raw)


def forbidden_count(rows: tuple[int, ...], order: int, edge_value: int) -> int:
    count = 0
    for vertices in combinations(range(len(rows)), order):
        if all(((rows[low] >> high) & 1) == edge_value for low, high in combinations(vertices, 2)):
            count += 1
    return count


def remove_vertex(rows: tuple[int, ...], deleted: int) -> tuple[int, ...]:
    kept = [vertex for vertex in range(len(rows)) if vertex != deleted]
    position = {old: new for new, old in enumerate(kept)}
    result = []
    for old in kept:
        row = 0
        for other in kept:
            if (rows[old] >> other) & 1:
                row |= 1 << position[other]
        result.append(row)
    return tuple(result)


def boundary_scan(rows: tuple[int, ...], maximum_component_size: int) -> dict[str, object]:
    """Compute connectivity by exhaustive small-side vertex boundaries.

    For a connected 21-vertex graph, every separator has a component of size
    at most ten.  Therefore enumerating all nonempty subsets of size at most
    ten and evaluating N(C) is complete for vertex connectivity.
    """
    validate_rows(rows)
    n = len(rows)
    full = (1 << n) - 1
    width = (n + 7) // 8
    checked = 0
    proper = 0
    minimum = n - 1 if connected_after(rows) else 0
    minimizer_count = 0
    separator_masks: set[int] = set()
    stream = hashlib.sha256()

    def extend(start: int, subset: int, neighborhood_union: int, size: int) -> None:
        nonlocal checked, proper, minimum, minimizer_count, separator_masks
        for vertex in range(start, n):
            new_subset = subset | (1 << vertex)
            new_union = neighborhood_union | rows[vertex]
            boundary = new_union & full & ~new_subset
            outside = full & ~(new_subset | boundary)
            checked += 1
            stream.update(new_subset.to_bytes(width, "little"))
            stream.update(boundary.to_bytes(width, "little"))
            if outside:
                proper += 1
                boundary_size = boundary.bit_count()
                if boundary_size < minimum:
                    minimum = boundary_size
                    minimizer_count = 1
                    separator_masks = {boundary}
                elif boundary_size == minimum:
                    minimizer_count += 1
                    separator_masks.add(boundary)
            if size < maximum_component_size and vertex + 1 < n:
                extend(vertex + 1, new_subset, new_union, size + 1)

    extend(0, 0, 0, 1)
    return {
        "connectivity": minimum,
        "subsets_checked": checked,
        "proper_boundary_subsets": proper,
        "minimum_boundary_subset_count": minimizer_count,
        "minimum_separator_count": len(separator_masks),
        "boundary_stream_sha256": stream.hexdigest(),
    }


def brute_connectivity(rows: tuple[int, ...]) -> int:
    """Definition-level deletion checker used only on graphs through order five."""
    n = len(rows)
    if not connected_after(rows):
        return 0
    complete = all(row.bit_count() == n - 1 for row in rows)
    if complete:
        return n - 1
    for size in range(1, n):
        for vertices in combinations(range(n), size):
            removed = sum(1 << vertex for vertex in vertices)
            if not connected_after(rows, removed):
                return size
    raise AssertionError("connectivity search exhausted")


def rows_from_mask(n: int, mask: int) -> tuple[int, ...]:
    rows = [0] * n
    for index, (low, high) in enumerate(combinations(range(n), 2)):
        if (mask >> index) & 1:
            rows[low] |= 1 << high
            rows[high] |= 1 << low
    return tuple(rows)


def controls() -> dict[str, int]:
    graphs = comparisons = 0
    for n in range(2, 6):
        for mask in range(1 << (n * (n - 1) // 2)):
            rows = rows_from_mask(n, mask)
            require(decode_graph6(encode_graph6(rows)) == rows, "graph6 control failed")
            observed = boundary_scan(rows, n - 1)["connectivity"]
            require(observed == brute_connectivity(rows), "boundary scan differs from deletion")
            graphs += 1
            comparisons += 1

    bad = ("", "~", "U", "A", "B?x", "A@", "!", "A\n")
    rejected = 0
    for record in bad:
        try:
            decode_graph6(record)
        except (ValueError, IndexError):
            rejected += 1
        else:
            raise ValueError("malformed graph6 accepted")
    return {
        "small_labeled_graphs": graphs,
        "boundary_deletion_comparisons": comparisons,
        "malformed_graph6_rejections": rejected,
    }


def component_profiles() -> list[list[int]]:
    capacities = {1: 3, 2: 8, 3: 17}
    viable: set[tuple[int, ...]] = set()

    def partitions(prefix: tuple[int, ...], lower: int, budget: int) -> None:
        if len(prefix) >= 2 and sum(capacities[item] for item in prefix) >= 17:
            viable.add(prefix)
        for part in range(lower, min(3, budget) + 1):
            partitions(prefix + (part,), part, budget - part)

    partitions((), 1, 4)
    require(viable == {(1, 3)}, "unexpected component independence partition")
    profiles = sorted(
        (separator, 22 - separator - clique, clique)
        for separator in range(6)
        for clique in range(1, 4)
        if 1 <= 22 - separator - clique <= 17
    )
    require(tuple(profiles) == EXPECTED_COMPONENT_PROFILES, "component profiles changed")
    return [list(profile) for profile in profiles]


def check(inputs_path: Path) -> dict[str, object]:
    raw = inputs_path.read_bytes()
    require(sha256(raw) == INPUT_SHA256, "target inputs hash mismatch")
    data = json.loads(raw)
    require(isinstance(data, dict), "target input is not an object")
    representatives = data.get("representatives")
    require(isinstance(representatives, list) and len(representatives) == 13, "wrong class count")
    records = [representative.get("graph6") for representative in representatives]
    require(all(isinstance(record, str) for record in records), "missing graph6 record")
    require(len(set(records)) == 13, "duplicate graph6 record")

    graph_results = []
    boundary_digest = hashlib.sha256()
    total_subsets = 0
    for identifier, record in enumerate(records):
        rows = decode_graph6(record)
        require(len(rows) == 22, "wrong graph order")
        validate_rows(rows)
        degrees = [row.bit_count() for row in rows]
        degree_five = [vertex for vertex, degree in enumerate(degrees) if degree == 5]
        require(len(degree_five) == 1, "degree-five vertex is not unique")
        hub = degree_five[0]
        require(min(degrees[vertex] for vertex in range(22) if vertex != hub) >= 9, "degree gap failed")
        require(sum(degrees) // 2 == 109, "wrong edge count")
        require(forbidden_count(rows, 4, 1) == 0, "red K4 found")
        require(forbidden_count(rows, 5, 0) == 0, "blue K5 found")

        hubless = remove_vertex(rows, hub)
        require(connected_after(hubless), "hubless graph disconnected")
        scan = boundary_scan(hubless, 10)
        require(scan["subsets_checked"] == (1 << 20) - 1, "incomplete boundary scan")
        require(scan["connectivity"] >= 6, "hubless graph is not six-connected")
        total_subsets += int(scan["subsets_checked"])
        boundary_digest.update(bytes.fromhex(str(scan["boundary_stream_sha256"])))

        graph_results.append(
            {
                "id": identifier,
                "hub": hub,
                "edge_sha256": edge_digest(rows),
                "degree_sequence": sorted(degrees),
                "hubless_connectivity": scan["connectivity"],
                "hubless_minimum_separator_count": scan["minimum_separator_count"],
                "hubless_boundary_stream_sha256": scan["boundary_stream_sha256"],
            }
        )

    record_digest = sha256(("\n".join(records) + "\n").encode())
    return {
        "status": "INDEPENDENTLY_VERIFIED_DENSE_FIVE_SEPARATOR_CLASSIFICATION",
        "target_commit": TARGET_COMMIT,
        "target_inputs_sha256": INPUT_SHA256,
        "component_profiles_s_a_b": component_profiles(),
        "class_count": len(graph_results),
        "edge_count": 109,
        "connectivity": 5,
        "five_cuts_per_graph": 1,
        "outside_edges_per_interface": 22 * 20 + 20 * 19 // 2,
        "graph6_record_stream_sha256": record_digest,
        "hubless_boundary_subsets_checked": total_subsets,
        "hubless_boundary_digest_sha256": boundary_digest.hexdigest(),
        "graphs": graph_results,
        "controls": controls(),
    }


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path, help="target inputs.json at the pinned commit")
    parser.add_argument("--output", type=Path, help="also write canonical JSON to this path")
    args = parser.parse_args(argv)
    result = check(args.inputs)
    rendered = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
