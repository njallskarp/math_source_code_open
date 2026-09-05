#!/usr/bin/env python3
"""Clean-room degree-sequence audit for the order-(2h+1) classification.

The target checker enumerates cell subsets in selected rectangular hosts.  This
audit instead enumerates integer partitions of 2h+1 as the two bipartite degree
sequences.  For each pair it solves an exact unit-capacity b-matching problem,
allowing an edge uv only when deg(u)+deg(v) >= h+2.  Thus every accepted flow
is exactly a simple bipartite graph whose line graph has minimum degree at
least h.  No target code, solver, third-party package, randomness, or floating
point arithmetic is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass


DegreeSequence = tuple[int, ...]
DegreePair = tuple[DegreeSequence, DegreeSequence]


def partitions(total: int, maximum: int | None = None) -> Iterator[DegreeSequence]:
    """Yield positive integer partitions of total in nonincreasing order."""
    if total < 0:
        raise ValueError("total must be nonnegative")
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


@dataclass
class Edge:
    destination: int
    reverse: int
    capacity: int


class Dinic:
    """Small exact max-flow implementation with integer capacities."""

    def __init__(self, vertices: int) -> None:
        self.graph: list[list[Edge]] = [[] for _ in range(vertices)]

    def add_edge(self, source: int, destination: int, capacity: int) -> None:
        forward = Edge(destination, len(self.graph[destination]), capacity)
        reverse = Edge(source, len(self.graph[source]), 0)
        self.graph[source].append(forward)
        self.graph[destination].append(reverse)

    def maximum_flow(self, source: int, sink: int) -> int:
        flow = 0
        while True:
            level = [-1] * len(self.graph)
            level[source] = 0
            queue = deque([source])
            while queue:
                vertex = queue.popleft()
                for edge in self.graph[vertex]:
                    if edge.capacity and level[edge.destination] < 0:
                        level[edge.destination] = level[vertex] + 1
                        queue.append(edge.destination)
            if level[sink] < 0:
                return flow

            cursor = [0] * len(self.graph)

            def augment(vertex: int, amount: int) -> int:
                if vertex == sink:
                    return amount
                while cursor[vertex] < len(self.graph[vertex]):
                    edge = self.graph[vertex][cursor[vertex]]
                    if edge.capacity and level[edge.destination] == level[vertex] + 1:
                        pushed = augment(edge.destination, min(amount, edge.capacity))
                        if pushed:
                            edge.capacity -= pushed
                            self.graph[edge.destination][edge.reverse].capacity += pushed
                            return pushed
                    cursor[vertex] += 1
                return 0

            while (pushed := augment(source, 10**9)) > 0:
                flow += pushed


def canonical_pair(left: DegreeSequence, right: DegreeSequence) -> DegreePair:
    return min((left, right), (right, left))


def quick_capacity_test(left: DegreeSequence, right: DegreeSequence, h: int) -> bool:
    """Necessary local-capacity checks before the exact b-matching."""
    if sum(left) != 2 * h + 1 or sum(right) != 2 * h + 1:
        return False
    if left[0] > len(right) or right[0] > len(left):
        return False
    for degree in left:
        if sum(other >= h + 2 - degree for other in right) < degree:
            return False
    for degree in right:
        if sum(other >= h + 2 - degree for other in left) < degree:
            return False
    return True


def has_allowed_realization(left: DegreeSequence, right: DegreeSequence, h: int) -> bool:
    """Decide exact simple-bipartite realization under the endpoint-degree rule."""
    if not quick_capacity_test(left, right, h):
        return False

    left_offset = 1
    right_offset = left_offset + len(left)
    sink = right_offset + len(right)
    network = Dinic(sink + 1)
    for index, degree in enumerate(left):
        network.add_edge(0, left_offset + index, degree)
    for left_index, left_degree in enumerate(left):
        for right_index, right_degree in enumerate(right):
            if left_degree + right_degree >= h + 2:
                network.add_edge(left_offset + left_index, right_offset + right_index, 1)
    for index, degree in enumerate(right):
        network.add_edge(right_offset + index, sink, degree)
    return network.maximum_flow(0, sink) == 2 * h + 1


def expected_pairs(h: int) -> set[DegreePair]:
    """Degree-sequence pairs forced by the theorem's four normal forms."""
    line = canonical_pair((2 * h + 1,), (1,) * (2 * h + 1))
    parallel = canonical_pair((h + 1, h), (2,) * h + (1,))
    perpendicular = canonical_pair((h + 1,) + (1,) * h, (h + 1,) + (1,) * h)
    expected = {line, parallel, perpendicular}
    if h == 4:
        expected.add(canonical_pair((3, 3, 3), (3, 3, 3)))
    return expected


def audit(max_h: int) -> dict[str, object]:
    if max_h < 2:
        raise ValueError("max_h must be at least two")
    digest = hashlib.sha256()
    summary: list[dict[str, object]] = []
    total_pairs = 0
    total_local_survivors = 0
    total_realizable = 0

    for h in range(2, max_h + 1):
        all_partitions = tuple(partitions(2 * h + 1))
        realizable: set[DegreePair] = set()
        pairs = 0
        local_survivors = 0
        for left_index, left in enumerate(all_partitions):
            for right in all_partitions[left_index:]:
                pairs += 1
                if not quick_capacity_test(left, right, h):
                    continue
                local_survivors += 1
                if has_allowed_realization(left, right, h):
                    realizable.add(canonical_pair(left, right))

        expected = expected_pairs(h)
        if realizable != expected:
            missing = sorted(expected - realizable)
            unexpected = sorted(realizable - expected)
            raise AssertionError(
                f"h={h}: missing={missing!r}, unexpected={unexpected!r}"
            )
        record = {
            "h": h,
            "partitions": len(all_partitions),
            "pairs": pairs,
            "local_survivors": local_survivors,
            "realizable": len(realizable),
            "degree_pairs": sorted(realizable),
        }
        digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode())
        digest.update(b"\n")
        summary.append(record)
        total_pairs += pairs
        total_local_survivors += local_survivors
        total_realizable += len(realizable)

    return {
        "max_h": max_h,
        "pairs": total_pairs,
        "local_survivors": total_local_survivors,
        "realizable": total_realizable,
        "digest": digest.hexdigest(),
        "summary": summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-h", type=int, default=12)
    args = parser.parse_args()
    result = audit(args.max_h)
    print(f"python: {platform.python_version()}")
    print(f"degree-sequence range: 2 <= h <= {result['max_h']}")
    print(f"unordered partition pairs tested: {result['pairs']}")
    print(f"pairs passing local capacity tests: {result['local_survivors']}")
    print(f"realizable degree-sequence pairs: {result['realizable']}")
    counts = ",".join(
        f"{record['h']}:{record['realizable']}" for record in result["summary"]
    )
    print(f"realizable counts by h: {counts}")
    print(f"audit SHA-256: {result['digest']}")
    print("all degree-sequence classifications matched")


if __name__ == "__main__":
    main()
