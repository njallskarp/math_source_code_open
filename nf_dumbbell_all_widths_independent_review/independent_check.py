#!/usr/bin/env python3
"""Independent full-Boolean check of B_(5,m), without orbit types."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys


def dumbbell_facets(m: int) -> frozenset[int]:
    if m < 2:
        raise ValueError("m must be at least 2")
    edges = {
        (1 << left) | (1 << right)
        for left, right in itertools.combinations(range(5), 2)
    }
    edges.update(
        (1 << left) | (1 << right)
        for left, right in itertools.combinations(range(5, m + 5), 2)
    )
    edges.add((1 << 0) | (1 << 5))
    return frozenset(edges)


def delta(facets: frozenset[int], vertex_count: int) -> frozenset[int]:
    allowed = [
        candidate
        for candidate in range(1 << vertex_count)
        if all(candidate & facet != facet for facet in facets)
    ]
    allowed_set = set(allowed)
    return frozenset(
        candidate
        for candidate in allowed
        if all(
            candidate | (1 << bit) not in allowed_set
            for bit in range(vertex_count)
            if candidate & (1 << bit) == 0
        )
    )


def labelled_orbit(m: int, limit: int) -> list[frozenset[int]]:
    initial = dumbbell_facets(m)
    result = [initial]
    current = delta(initial, m + 5)
    while current != initial:
        if len(result) >= limit:
            raise AssertionError(f"no return for m={m} before limit={limit}")
        if current in result:
            raise AssertionError(f"noninitial repetition for m={m}")
        result.append(current)
        current = delta(current, m + 5)
    return result


def is_bipartite_graph(facets: frozenset[int], vertex_count: int) -> bool:
    if any(edge.bit_count() != 2 for edge in facets):
        return False
    neighbors = [set() for _ in range(vertex_count)]
    for edge in facets:
        left, right = [bit for bit in range(vertex_count) if edge & (1 << bit)]
        neighbors[left].add(right)
        neighbors[right].add(left)
    color: dict[int, int] = {}
    for root in range(vertex_count):
        if root in color:
            continue
        color[root] = 0
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other in neighbors[vertex]:
                if other not in color:
                    color[other] = 1 - color[vertex]
                    stack.append(other)
                elif color[other] == color[vertex]:
                    return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=8)
    args = parser.parse_args()
    if not 2 <= args.max_m <= 9:
        parser.error("the full-Boolean check supports 2 <= --max-m <= 9")
    total_states = total_facets = 0
    record: list[tuple[int, list[list[int]]]] = []
    for m in range(2, args.max_m + 1):
        orbit = labelled_orbit(m, limit=m + 8)
        if len(orbit) != m + 7:
            raise AssertionError(f"m={m}: period {len(orbit)}, expected {m + 7}")
        if is_bipartite_graph(orbit[0], m + 5):
            raise AssertionError("B_(5,m) should contain its K_5")
        if not is_bipartite_graph(orbit[1], m + 5):
            raise AssertionError("the first iterate should be bipartite")
        for step, current in enumerate(orbit[2:], start=2):
            if max(mask.bit_count() for mask in current) < 3:
                raise AssertionError(f"m={m}, step={step}: expected a facet of size >=3")
        total_states += len(orbit)
        total_facets += sum(map(len, orbit))
        record.append((m, [sorted(current) for current in orbit]))
    digest = hashlib.sha256(
        json.dumps(record, separators=(",", ":")).encode()
    ).hexdigest()
    print(
        "INDEPENDENT VERIFIED "
        f"B_(5,m), m=2..{args.max_m}; full_boolean_states={total_states}; "
        f"facets_seen_with_multiplicity={total_facets}; labelled_period=m+7; "
        "no earlier isomorphic return"
    )
    print(f"ORBIT_SHA256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
