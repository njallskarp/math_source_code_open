#!/usr/bin/env python3
"""Independent Boolean-lattice replay of small all-width hub-chain orbits."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json


def delta(facets: frozenset[int], vertices: int) -> frozenset[int]:
    allowed = [
        mask for mask in range(1 << vertices)
        if not any(mask & facet == facet for facet in facets)
    ]
    allowed_set = set(allowed)
    return frozenset(
        mask for mask in allowed
        if all(mask | (1 << v) not in allowed_set for v in range(vertices) if not mask >> v & 1)
    )


def graph_facets(n: int, m: int, ell: int) -> frozenset[int]:
    offsets = (0, n, n + m)
    sizes = (n, m, ell)
    edges: set[int] = set()
    for offset, size in zip(offsets, sizes, strict=True):
        for u, v in itertools.combinations(range(offset, offset + size), 2):
            edges.add((1 << u) | (1 << v))
    edges.add((1 << offsets[0]) | (1 << offsets[1]))
    edges.add((1 << offsets[1]) | (1 << offsets[2]))
    return frozenset(edges)


def orbit(n: int, m: int, ell: int) -> list[frozenset[int]]:
    start = graph_facets(n, m, ell)
    result: list[frozenset[int]] = []
    state = start
    while state not in result:
        result.append(state)
        state = delta(state, n + m + ell)
    if state != start:
        raise AssertionError("first repeat did not return to the graph")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cases", nargs="*", default=["3,3,3", "3,3,4"],
        help="comma-separated clique widths",
    )
    args = parser.parse_args()
    parsed = [tuple(map(int, item.split(","))) for item in args.cases]
    if any(len(case) != 3 or min(case) < 3 for case in parsed):
        raise SystemExit("each case must be n,m,ell with all widths at least 3")
    records = []
    total_states = total_facets = 0
    for n, m, ell in parsed:
        states = orbit(n, m, ell)
        expected = n + m + ell + 2
        if len(states) != expected:
            raise AssertionError(f"period mismatch for {n,m,ell}")
        if not all(any(mask.bit_count() >= 3 for mask in state) for state in states[1:]):
            raise AssertionError(f"early isomorphic graph return possible at {n,m,ell}")
        records.append(
            [[mask for mask in sorted(state)] for state in states]
        )
        total_states += len(states)
        total_facets += sum(map(len, states))
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    print(
        "INDEPENDENT VERIFIED Boolean-lattice hubbed three-clique orbits; "
        f"cases={len(parsed)}; states={total_states}; "
        f"facets_with_multiplicity={total_facets}; labelled_period=n+m+ell+2; "
        "no earlier isomorphic return"
    )
    print(f"ORBIT_SHA256={digest}")


if __name__ == "__main__":
    main()
