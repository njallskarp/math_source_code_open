#!/usr/bin/env python3
"""Definition-level checker for small dumbbells; imports no orbit formulas."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import sys

State = frozenset[int]


def dumbbell_edges(k: int, m: int) -> State:
    x = range(k)
    y = range(k, k + m)
    edges = {
        (1 << left) | (1 << right)
        for block in (x, y)
        for left, right in itertools.combinations(block, 2)
    }
    edges.add((1 << 0) | (1 << k))
    return frozenset(edges)


def delta_masks(facets: State, vertex_count: int) -> State:
    admissible = {
        candidate
        for candidate in range(1 << vertex_count)
        if not any(candidate & facet == facet for facet in facets)
    }
    return frozenset(
        candidate
        for candidate in admissible
        if all(
            candidate | (1 << bit) not in admissible
            for bit in range(vertex_count)
            if candidate & (1 << bit) == 0
        )
    )


def is_bipartite_graph(facets: State, vertex_count: int) -> bool:
    if any(facet.bit_count() != 2 for facet in facets):
        raise ValueError("state is not a graph")
    adjacency = [set() for _ in range(vertex_count)]
    for edge in facets:
        vertices = [bit for bit in range(vertex_count) if edge & (1 << bit)]
        left, right = vertices
        adjacency[left].add(right)
        adjacency[right].add(left)
    colors: list[int | None] = [None] * vertex_count
    for root in range(vertex_count):
        if colors[root] is not None:
            continue
        colors[root] = 0
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if colors[neighbor] is None:
                    colors[neighbor] = 1 - colors[vertex]
                    stack.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False
    return True


def update_hash(digest: hashlib._Hash, k: int, m: int, step: int, state: State) -> None:
    digest.update(f"{k},{m},{step}:".encode())
    digest.update(",".join(map(str, sorted(state))).encode())
    digest.update(b"\n")


def check_case(k: int, m: int, digest: hashlib._Hash) -> tuple[int, int]:
    vertex_count = k + m
    initial = dumbbell_edges(k, m)
    if is_bipartite_graph(initial, vertex_count):
        raise AssertionError(f"k={k},m={m}: initial dumbbell should contain a triangle")
    state = initial
    seen = {initial}
    states = facets = 0
    for step in range(k + m + 2):
        if step == 1:
            if any(facet.bit_count() != 2 for facet in state):
                raise AssertionError(f"k={k},m={m}: first iterate is not a graph")
            if not is_bipartite_graph(state, vertex_count):
                raise AssertionError(f"k={k},m={m}: first iterate is not bipartite")
        if step >= 2 and max(map(int.bit_count, state)) < 3:
            raise AssertionError(f"k={k},m={m},step={step}: no large facet")
        update_hash(digest, k, m, step, state)
        states += 1
        facets += len(state)
        state = delta_masks(state, vertex_count)
        if step + 1 < k + m + 2 and state in seen:
            raise AssertionError(f"k={k},m={m}: premature labelled repetition")
        seen.add(state)
    if state != initial:
        raise AssertionError(f"k={k},m={m}: wrong labelled period")
    return states, facets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-vertices", type=int, default=11)
    args = parser.parse_args()
    if args.max_vertices < 6:
        parser.error("--max-vertices must be at least 6")
    digest = hashlib.sha256()
    cases = states = facets = 0
    for k in range(3, args.max_vertices + 1):
        for m in range(k, args.max_vertices - k + 1):
            checked_states, checked_facets = check_case(k, m, digest)
            cases += 1
            states += checked_states
            facets += checked_facets
    print(
        "INDEPENDENT VERIFIED full Boolean-lattice dumbbell orbits; "
        f"3<=k<=m; k+m<={args.max_vertices}; cases={cases}; "
        f"states={states}; facets_seen_with_multiplicity={facets}; "
        f"orbit_sha256={digest.hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
