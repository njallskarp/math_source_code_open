#!/usr/bin/env python3
"""Independent NF check for the all-width dumbbell orbit.

The reviewed source computes NF in a type-poset quotient and its small
definition-level checker scans every subset.  This checker instead computes
minimal transversals incrementally (Berge's update), complements them, and
compares the resulting labelled facets entry-for-entry with a separate,
literal expansion of the claimed orbit templates.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import sys
from collections.abc import Iterable

Type = tuple[int, int, int, int]
TypeState = frozenset[Type]
MaskState = frozenset[int]


def is_subset(left: int, right: int) -> bool:
    return left & right == left


def inclusion_minimal(masks: Iterable[int]) -> MaskState:
    """Return the inclusion-minimal distinct masks by a transparent scan."""
    kept: list[int] = []
    for mask in sorted(set(masks), key=lambda value: (value.bit_count(), value)):
        if not any(is_subset(candidate, mask) for candidate in kept):
            kept.append(mask)
    return frozenset(kept)


def minimal_transversals(facets: MaskState) -> MaskState:
    """Compute all inclusion-minimal hitting sets by incremental extension."""
    transversals: MaskState = frozenset({0})
    for facet in sorted(facets, key=lambda value: (value.bit_count(), value)):
        updated: list[int] = []
        for transversal in transversals:
            if transversal & facet:
                updated.append(transversal)
            else:
                remaining = facet
                while remaining:
                    bit = remaining & -remaining
                    updated.append(transversal | bit)
                    remaining -= bit
        transversals = inclusion_minimal(updated)

    # Definition-level audit of the generated certificate.
    for transversal in transversals:
        if any(transversal & facet == 0 for facet in facets):
            raise AssertionError("generated set does not hit every facet")
        remaining = transversal
        while remaining:
            bit = remaining & -remaining
            smaller = transversal ^ bit
            if all(smaller & facet for facet in facets):
                raise AssertionError("generated transversal is not minimal")
            remaining -= bit
    return transversals


def delta_dual(facets: MaskState, vertex_count: int) -> MaskState:
    """NF facets are complements of the inclusion-minimal transversals."""
    universe = (1 << vertex_count) - 1
    return frozenset(universe ^ cover for cover in minimal_transversals(facets))


def dumbbell_edges(k: int, m: int) -> MaskState:
    x_vertices = range(k)
    y_vertices = range(k, k + m)
    edges = {
        (1 << left) | (1 << right)
        for block in (x_vertices, y_vertices)
        for left, right in itertools.combinations(block, 2)
    }
    edges.add((1 << 0) | (1 << k))
    return frozenset(edges)


def is_bipartite_graph(facets: MaskState, vertex_count: int) -> bool:
    if any(edge.bit_count() != 2 for edge in facets):
        raise ValueError("facets do not define a graph")
    adjacency = [set() for _ in range(vertex_count)]
    for edge in facets:
        vertices = [index for index in range(vertex_count) if edge & (1 << index)]
        left, right = vertices
        adjacency[left].add(right)
        adjacency[right].add(left)
    color: list[int | None] = [None] * vertex_count
    for root in range(vertex_count):
        if color[root] is not None:
            continue
        color[root] = 0
        pending = [root]
        while pending:
            vertex = pending.pop()
            for neighbor in adjacency[vertex]:
                if color[neighbor] is None:
                    color[neighbor] = 1 - color[vertex]
                    pending.append(neighbor)
                elif color[neighbor] == color[vertex]:
                    return False
    return True


def type_leq(left: Type, right: Type) -> bool:
    return all(x <= y for x, y in zip(left, right, strict=True))


def clip_maximal(k: int, m: int, displayed: Iterable[Type]) -> TypeState:
    """Clip to the type box, then take maximal elements by brute force."""
    inside = frozenset(
        (a, i, b, j)
        for a, i, b, j in displayed
        if a in (0, 1) and 0 <= i < k and b in (0, 1) and 0 <= j < m
    )
    return frozenset(
        value
        for value in inside
        if not any(value != other and type_leq(value, other) for other in inside)
    )


def prefix(k: int, m: int, t: int) -> TypeState:
    q = m - 1
    if t == 0:
        # Clipping makes the same display valid at the reviewed k>=3 range
        # and at the independently checked k=2 boundary.
        return clip_maximal(
            k,
            m,
            {
                (0, 0, 0, 2),
                (0, 0, 1, 1),
                (0, 2, 0, 0),
                (1, 0, 1, 0),
                (1, 1, 0, 0),
            },
        )
    if t == 1:
        return frozenset({(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1)})
    if t == 2:
        return frozenset({(0, 0, 1, q), (1, 0, 1, 0), (1, k - 1, 0, 0)})
    if t == 3:
        return frozenset(
            {(0, k - 1, 0, q), (0, k - 1, 1, q - 1), (1, k - 2, 0, q)}
        )
    if not 4 <= t <= k + 2:
        raise ValueError("invalid prefix index")
    u = k - t + 4
    displayed: list[Type] = []
    displayed.extend((0, i, 0, q - (i - u)) for i in range(u, k))
    displayed.append((0, u - 2, 1, q))
    displayed.extend((0, i, 1, q - (i - u + 1)) for i in range(u, k))
    displayed.extend((1, i, 0, q - (i - u + 1)) for i in range(u - 1, k - 1))
    displayed.append((1, k - 1, 0, q - (t - 3)))
    displayed.extend((1, i, 1, q - (i - u + 3)) for i in range(u - 3, k))
    return clip_maximal(k, m, displayed)


def wave_weight(k: int, a: int, i: int, b: int) -> int:
    if a == 0 and b == 0:
        return k if i == 0 else k - i - 1
    if a == 0 and b == 1:
        return k - 1 if i == 0 else k - i - 2
    if a == 1 and b == 0:
        return -2 if i == k - 1 else k - i - 2
    return k - i - 4


def wave(k: int, m: int, s: int) -> TypeState:
    return clip_maximal(
        k,
        m,
        (
            (a, i, b, s + wave_weight(k, a, i, b))
            for a, i, b in itertools.product((0, 1), range(k), (0, 1))
        ),
    )


def tail(k: int, m: int, r: int) -> TypeState:
    displayed: list[Type] = [(0, 0, 0, r + 2), (0, r + 2, 0, 0)]
    displayed.extend((0, i, 0, r + 1 - i) for i in range(1, r + 1))
    displayed.append((0, 0, 1, r + 1))
    displayed.extend((0, i, 1, r - i) for i in range(1, r + 1))
    displayed.extend((1, i, 0, r - i) for i in range(r))
    displayed.append((1, r + 1, 0, 0))
    displayed.extend((1, i, 1, r - 2 - i) for i in range(r - 1))
    return clip_maximal(k, m, displayed)


def claimed_types(k: int, m: int) -> list[TypeState]:
    """Literal expansion of the claimed construction, plus its k=2 limit."""
    if not 2 <= k <= m or m < 3:
        raise ValueError("require 2 <= k <= m and m >= 3")
    q = m - 1
    states = [prefix(k, m, t) for t in range(k + 3)]
    states.extend(wave(k, m, s) for s in range(q - k + 2, 0, -1))
    if k >= 3:
        states.extend(tail(k, m, r) for r in range(k - 2, 0, -1))
    return states


def expand_type(value: Type, k: int, m: int) -> Iterable[int]:
    a, i, b, j = value
    ordinary_x = range(1, k)
    ordinary_y = range(k + 1, k + m)
    fixed = (a << 0) | (b << k)
    for x_choice in itertools.combinations(ordinary_x, i):
        x_mask = sum(1 << vertex for vertex in x_choice)
        for y_choice in itertools.combinations(ordinary_y, j):
            yield fixed | x_mask | sum(1 << vertex for vertex in y_choice)


def expand_state(types: TypeState, k: int, m: int) -> MaskState:
    return frozenset(
        mask for value in types for mask in expand_type(value, k, m)
    )


def update_digest(
    digest: hashlib._Hash, k: int, m: int, step: int, facets: MaskState
) -> None:
    digest.update(f"{k},{m},{step}:".encode())
    digest.update(",".join(map(str, sorted(facets))).encode())
    digest.update(b"\n")


def check_case(k: int, m: int, digest: hashlib._Hash) -> tuple[int, int]:
    vertex_count = k + m
    claimed = claimed_types(k, m)
    if len(claimed) != k + m + 2:
        raise AssertionError(f"B_({k},{m}): wrong claimed period {len(claimed)}")
    if len(set(claimed)) != len(claimed):
        raise AssertionError(f"B_({k},{m}): repeated type state before return")

    actual = dumbbell_edges(k, m)
    if is_bipartite_graph(actual, vertex_count):
        raise AssertionError(f"B_({k},{m}): initial graph should contain a triangle")
    seen = {actual}
    facets_seen = 0
    for step, type_state in enumerate(claimed):
        expected = expand_state(type_state, k, m)
        if actual != expected:
            missing = sorted(expected - actual)[:3]
            extra = sorted(actual - expected)[:3]
            raise AssertionError(
                f"B_({k},{m}), step {step}: template mismatch; "
                f"missing={missing}, extra={extra}"
            )
        if step == 1:
            if any(edge.bit_count() != 2 for edge in actual):
                raise AssertionError(f"B_({k},{m}): first iterate is not a graph")
            if not is_bipartite_graph(actual, vertex_count):
                raise AssertionError(f"B_({k},{m}): first iterate is not bipartite")
        if step >= 2 and max(mask.bit_count() for mask in actual) < 3:
            raise AssertionError(f"B_({k},{m}), step {step}: unexpectedly a graph")
        update_digest(digest, k, m, step, actual)
        facets_seen += len(actual)
        actual = delta_dual(actual, vertex_count)
        if step + 1 < len(claimed) and actual in seen:
            raise AssertionError(f"B_({k},{m}): premature labelled repetition")
        seen.add(actual)
    if actual != dumbbell_edges(k, m):
        raise AssertionError(f"B_({k},{m}): orbit does not close")
    return len(claimed), facets_seen


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-vertices", type=int, default=12)
    args = parser.parse_args()
    if args.max_vertices < 6:
        parser.error("--max-vertices must be at least 6")

    digest = hashlib.sha256()
    cases = states = facets = k2_cases = 0
    for k in range(2, args.max_vertices + 1):
        for m in range(max(3, k), args.max_vertices - k + 1):
            case_states, case_facets = check_case(k, m, digest)
            cases += 1
            states += case_states
            facets += case_facets
            k2_cases += k == 2
    print(
        "DUAL VERIFIED dumbbell templates and k=2 specialization; "
        f"2<=k<=m; m>=3; k+m<={args.max_vertices}; cases={cases}; "
        f"k2_cases={k2_cases}; states={states}; "
        f"facets_seen_with_multiplicity={facets}; "
        f"orbit_sha256={digest.hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
