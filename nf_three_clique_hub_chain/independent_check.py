#!/usr/bin/env python3
"""Definition-level Boolean-lattice replay for small hubbed clique chains."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys


def graph_facets(m: int) -> frozenset[int]:
    """Edges of K3--Km--K3 with both bridges incident to middle vertex 3."""
    if m < 3:
        raise ValueError("m must be at least 3")
    left = range(3)
    middle = range(3, m + 3)
    right = range(m + 3, m + 6)
    edges = {
        (1 << u) | (1 << v)
        for clique in (left, middle, right)
        for u, v in itertools.combinations(clique, 2)
    }
    edges.add((1 << 0) | (1 << 3))
    edges.add((1 << 3) | (1 << (m + 3)))
    return frozenset(edges)


def delta(facets: frozenset[int], vertex_count: int) -> frozenset[int]:
    """Apply the definition: maximal subsets containing no input facet."""
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


def labelled_orbit(m: int) -> list[frozenset[int]]:
    vertex_count = m + 6
    initial = graph_facets(m)
    result: list[frozenset[int]] = []
    seen: dict[frozenset[int], int] = {}
    current = initial
    limit = m + 10
    while current not in seen:
        if len(result) >= limit:
            raise AssertionError(f"m={m}: no return before {limit}")
        seen[current] = len(result)
        result.append(current)
        current = delta(current, vertex_count)
    if seen[current] != 0:
        raise AssertionError(f"m={m}: first repeat did not return to start")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=6)
    args = parser.parse_args()
    if not 3 <= args.max_m <= 7:
        parser.error("the Boolean replay supports 3 <= --max-m <= 7")

    cases = states = facets_seen = 0
    record: list[tuple[int, list[list[int]]]] = []
    for m in range(3, args.max_m + 1):
        orbit = labelled_orbit(m)
        if len(orbit) != m + 8:
            raise AssertionError(
                f"m={m}: labelled period {len(orbit)}, expected {m + 8}"
            )
        if any(mask.bit_count() != 2 for mask in orbit[0]):
            raise AssertionError("initial facets must be graph edges")
        for step, state in enumerate(orbit[1:], start=1):
            if all(mask.bit_count() == 2 for mask in state):
                raise AssertionError(f"m={m}, step={step}: early graph state")
        cases += 1
        states += len(orbit)
        facets_seen += sum(map(len, orbit))
        record.append((m, [sorted(state) for state in orbit]))

    digest = hashlib.sha256(
        json.dumps(record, separators=(",", ":")).encode()
    ).hexdigest()
    print(
        "INDEPENDENT VERIFIED Boolean-lattice hubbed K3--Km--K3 orbits; "
        f"m=3..{args.max_m}; cases={cases}; states={states}; "
        f"facets_seen_with_multiplicity={facets_seen}; labelled_period=m+8; "
        "no earlier isomorphic return"
    )
    print(f"ORBIT_SHA256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
