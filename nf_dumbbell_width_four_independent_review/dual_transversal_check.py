#!/usr/bin/env python3
"""Clean-room NF-orbit checker via incremental minimal transversals.

This checker intentionally does not encode the 16 orbit types, the seven
prefix states, the translating weights, or the wrap states from the target
proof.  It constructs B_(4,m) as an ordinary labelled graph and uses the
duality

    maximal C-free sets = complements of minimal transversals of C

to apply one NF step to a facet clutter C.  Minimal transversals are generated
incrementally (Berge's elementary update), rather than by enumerating the
Boolean lattice as in the target's definition-level checker.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import sys


Clutter = frozenset[int]


def minimalize(masks: set[int]) -> Clutter:
    """Return the inclusion-minimal members of a finite mask family."""
    kept: list[int] = []
    for mask in sorted(masks, key=lambda value: (value.bit_count(), value)):
        if not any(previous & mask == previous for previous in kept):
            kept.append(mask)
    return frozenset(kept)


def minimal_transversals(facets: Clutter) -> Clutter:
    """Generate all minimal hitting sets by processing one facet at a time."""
    transversals: Clutter = frozenset({0})
    for facet in sorted(facets):
        candidates: set[int] = set()
        facet_vertices = [1 << bit for bit in range(facet.bit_length()) if facet & (1 << bit)]
        for transversal in transversals:
            if transversal & facet:
                candidates.add(transversal)
            else:
                candidates.update(transversal | vertex for vertex in facet_vertices)
        transversals = minimalize(candidates)
    return transversals


def nf_dual(facets: Clutter, vertex_count: int) -> Clutter:
    """Apply NF using complements of minimal transversals."""
    universe = (1 << vertex_count) - 1
    return frozenset(universe ^ transversal for transversal in minimal_transversals(facets))


def nf_boolean(facets: Clutter, vertex_count: int) -> Clutter:
    """Small-instance definition-level oracle used only to test nf_dual."""
    free = {
        candidate
        for candidate in range(1 << vertex_count)
        if all(candidate & facet != facet for facet in facets)
    }
    return frozenset(
        candidate
        for candidate in free
        if all(
            candidate | (1 << bit) not in free
            for bit in range(vertex_count)
            if candidate & (1 << bit) == 0
        )
    )


def dumbbell(m: int) -> Clutter:
    """Facet clutter of disjoint K_4 and K_m plus bridge {0,4}."""
    if m < 2:
        raise ValueError("m must be at least 2")
    edges = {
        (1 << left) | (1 << right)
        for left, right in itertools.combinations(range(4), 2)
    }
    edges.update(
        (1 << left) | (1 << right)
        for left, right in itertools.combinations(range(4, m + 4), 2)
    )
    edges.add((1 << 0) | (1 << 4))
    return frozenset(edges)


def orbit(m: int) -> list[Clutter]:
    """Return the labelled orbit up to, but not including, first return."""
    vertex_count = m + 4
    initial = dumbbell(m)
    states = [initial]
    seen = {initial: 0}
    current = nf_dual(initial, vertex_count)
    limit = 4 * m + 40
    while current != initial:
        if current in seen:
            raise AssertionError(
                f"m={m}: noninitial cycle starts at step {seen[current]}"
            )
        if len(states) >= limit:
            raise AssertionError(f"m={m}: no return before {limit} states")
        seen[current] = len(states)
        states.append(current)
        current = nf_dual(current, vertex_count)
    return states


def is_bipartite_graph(facets: Clutter, vertex_count: int) -> bool:
    if any(facet.bit_count() != 2 for facet in facets):
        return False
    neighbors = [set() for _ in range(vertex_count)]
    for edge in facets:
        vertices = [bit for bit in range(vertex_count) if edge & (1 << bit)]
        left, right = vertices
        neighbors[left].add(right)
        neighbors[right].add(left)
    colors: dict[int, int] = {}
    for root in range(vertex_count):
        if root in colors:
            continue
        colors[root] = 0
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor in neighbors[vertex]:
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    stack.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False
    return True


def update_digest(digest: "hashlib._Hash", m: int, states: list[Clutter]) -> None:
    for step, state in enumerate(states):
        digest.update(f"m={m};step={step};".encode())
        digest.update(",".join(f"{facet:x}" for facet in sorted(state)).encode())
        digest.update(b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=9)
    parser.add_argument("--cross-check-max-m", type=int, default=7)
    args = parser.parse_args()
    if args.max_m < 2:
        parser.error("--max-m must be at least 2")
    if not 2 <= args.cross_check_max_m <= args.max_m:
        parser.error("require 2 <= --cross-check-max-m <= --max-m")

    digest = hashlib.sha256()
    total_states = 0
    total_facets = 0
    for m in range(2, args.max_m + 1):
        states = orbit(m)
        expected_period = m + 6
        if len(states) != expected_period:
            raise AssertionError(
                f"m={m}: labelled period {len(states)}, expected {expected_period}"
            )

        # These invariants also exclude any earlier return up to isomorphism:
        # state 0 is a non-bipartite graph, state 1 is bipartite, and every
        # later state has dimension at least two.
        if is_bipartite_graph(states[0], m + 4):
            raise AssertionError(f"m={m}: initial K_4-containing graph is bipartite")
        if not is_bipartite_graph(states[1], m + 4):
            raise AssertionError(f"m={m}: first iterate is not bipartite")
        if any(max(facet.bit_count() for facet in state) < 3 for state in states[2:]):
            raise AssertionError(f"m={m}: a later state is still a graph")

        if m <= args.cross_check_max_m:
            for step, state in enumerate(states):
                direct = nf_boolean(state, m + 4)
                dual = nf_dual(state, m + 4)
                if direct != dual:
                    raise AssertionError(f"m={m}, step={step}: dual/direct mismatch")

        update_digest(digest, m, states)
        total_states += len(states)
        total_facets += sum(len(state) for state in states)
        print(
            f"m={m}: period={len(states)}; "
            f"facets_with_multiplicity={sum(len(state) for state in states)}"
        )

    print(
        f"VERIFIED m=2..{args.max_m}; periods=m+6; states={total_states}; "
        f"facets_with_multiplicity={total_facets}; "
        f"dual_direct_cross_check=2..{args.cross_check_max_m}"
    )
    print(f"orbit_sha256={digest.hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
