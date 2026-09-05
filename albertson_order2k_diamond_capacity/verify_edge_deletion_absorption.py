#!/usr/bin/env python3
"""Exact checker for the two-leaf edge-deletion absorption dichotomy."""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations


VERTICES = ("v", "w", "p", "q", "ai", "bi", "aj", "bj")
INDEX = {vertex: index for index, vertex in enumerate(VERTICES)}


def edge(x: str, y: str) -> tuple[str, str]:
    return tuple(sorted((x, y)))


FIXED_H = {
    edge(*pair)
    for pair in (
        ("v", "p"),
        ("v", "q"),
        ("p", "q"),
        ("w", "p"),
        ("w", "q"),
        ("v", "ai"),
        ("v", "aj"),
        ("w", "bi"),
        ("w", "bj"),
        ("ai", "bi"),
        ("ai", "bj"),
        ("aj", "bi"),
        ("aj", "bj"),
    )
}

BLOCKER_STATES = (
    ("AA", frozenset(("ai",)), frozenset(("aj",))),
    ("BB", frozenset(("bi",)), frozenset(("bj",))),
    ("FIA", frozenset(("ai", "bi")), frozenset(("aj",))),
    ("FIB", frozenset(("ai", "bi")), frozenset(("bj",))),
    ("AIF", frozenset(("ai",)), frozenset(("aj", "bj"))),
    ("BIF", frozenset(("bi",)), frozenset(("aj", "bj"))),
    ("FF", frozenset(("ai", "bi")), frozenset(("aj", "bj"))),
)

FORCED_G = tuple(
    edge(*pair)
    for pair in (
        ("v", "w"),
        ("v", "bi"),
        ("v", "bj"),
        ("w", "ai"),
        ("w", "aj"),
        ("p", "ai"),
        ("p", "bi"),
        ("p", "aj"),
        ("p", "bj"),
        ("ai", "aj"),
        ("bi", "bj"),
    )
)


def h_edges(qi: frozenset[str], qj: frozenset[str]) -> frozenset[tuple[str, str]]:
    return frozenset(FIXED_H | {edge("q", x) for x in qi | qj})


def is_clique(mask: int, edges: frozenset[tuple[str, str]]) -> bool:
    members = [VERTICES[index] for index in range(8) if mask & (1 << index)]
    return all(edge(x, y) in edges for x, y in combinations(members, 2))


def clique_masks(edges: frozenset[tuple[str, str]]) -> tuple[int, ...]:
    return tuple(mask for mask in range(1, 1 << 8) if is_clique(mask, edges))


def clique_cover_number(edges: frozenset[tuple[str, str]]) -> int:
    cliques = clique_masks(edges)
    by_first: dict[int, list[int]] = {index: [] for index in range(8)}
    for mask in cliques:
        first = (mask & -mask).bit_length() - 1
        by_first[first].append(mask)

    @lru_cache(maxsize=None)
    def cover(mask: int) -> int:
        if mask == 0:
            return 0
        first = (mask & -mask).bit_length() - 1
        return 1 + min(cover(mask ^ clique) for clique in by_first[first] if clique & mask == clique)

    return cover((1 << 8) - 1)


def blocks_are_cover(blocks: tuple[tuple[str, ...], ...], edges: frozenset[tuple[str, str]]) -> bool:
    flat = [vertex for block in blocks for vertex in block]
    if len(flat) != 8 or set(flat) != set(VERTICES):
        return False
    return all(
        edge(x, y) in edges
        for block in blocks
        for x, y in combinations(block, 2)
    )


def swap_indices(name: str) -> str:
    return {"ai": "aj", "aj": "ai", "bi": "bj", "bj": "bi"}.get(name, name)


def swap_sides(name: str) -> str:
    return {
        "v": "w",
        "w": "v",
        "ai": "bi",
        "bi": "ai",
        "aj": "bj",
        "bj": "aj",
    }.get(name, name)


def map_blocks(blocks: tuple[tuple[str, ...], ...], transform) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(transform(vertex) for vertex in block) for block in blocks)


def witness(added: tuple[str, str], edges: frozenset[tuple[str, str]]) -> tuple[tuple[str, ...], ...]:
    representatives: dict[tuple[str, str], tuple[tuple[str, ...], ...]] = {
        edge("v", "w"): (("v", "w", "p", "q"), ("ai", "bi"), ("aj", "bj")),
        edge("v", "bi"): (("v", "ai", "bi"), ("w", "p", "q"), ("aj", "bj")),
        edge("ai", "aj"): (("v", "p", "q"), ("w", "bi"), ("ai", "aj", "bj")),
    }
    if added in representatives:
        return representatives[added]

    transformed = edge(*(swap_indices(x) for x in added))
    if transformed in representatives:
        return map_blocks(representatives[transformed], swap_indices)

    transformed = edge(*(swap_sides(x) for x in added))
    if transformed in representatives:
        return map_blocks(representatives[transformed], swap_sides)

    twice = edge(*(swap_indices(swap_sides(x)) for x in added))
    if twice in representatives:
        return map_blocks(map_blocks(representatives[twice], swap_sides), swap_indices)

    # The p--pair orbit uses the blocker in that same pair.
    x, y = added
    pair_vertex = y if x == "p" else x
    if "p" not in added:
        raise AssertionError(f"no witness template for {added}")
    if pair_vertex in ("aj", "bj"):
        base_edge = edge("p", swap_indices(pair_vertex))
        return map_blocks(witness(base_edge, frozenset(edge(swap_indices(a), swap_indices(b)) for a, b in edges)), swap_indices)
    if pair_vertex == "ai":
        if edge("q", "ai") in edges:
            return (("v", "p", "q", "ai"), ("w", "bi"), ("aj", "bj"))
        return (("v", "p", "ai"), ("w", "q", "bi"), ("aj", "bj"))
    if pair_vertex == "bi":
        if edge("q", "bi") in edges:
            return (("w", "p", "q", "bi"), ("v", "ai"), ("aj", "bj"))
        return (("w", "p", "bi"), ("v", "q", "ai"), ("aj", "bj"))
    raise AssertionError(f"unexpected p-edge {added}")


def main() -> None:
    records: list[str] = []
    absorption_count = 0
    gap_count = 0
    all_pairs = {edge(x, y) for x, y in combinations(VERTICES, 2)}

    assert len(BLOCKER_STATES) == 7
    assert len(FORCED_G) == 11

    for state_name, qi, qj in BLOCKER_STATES:
        assert qi and qj
        assert len(qi) + len(qj) >= 3 or (qi, qj) in (
            (frozenset(("ai",)), frozenset(("aj",))),
            (frozenset(("bi",)), frozenset(("bj",))),
        )
        base_edges = h_edges(qi, qj)
        assert set(FORCED_G).isdisjoint(base_edges)

        for added in FORCED_G:
            augmented = frozenset(set(base_edges) | {added})
            blocks = witness(added, augmented)
            assert blocks_are_cover(blocks, augmented)
            theta = clique_cover_number(augmented)
            assert theta == 3
            absorption_count += 1
            records.append(f"A|{state_name}|{'-'.join(added)}|theta={theta}")

        gaps = sorted(
            edge("q", x)
            for x in ("ai", "bi", "aj", "bj")
            if edge("q", x) not in base_edges
        )
        assert all(gap in all_pairs - base_edges for gap in gaps)
        for added in gaps:
            theta = clique_cover_number(frozenset(set(base_edges) | {added}))
            assert theta == 4
            gap_count += 1
            records.append(f"D|{state_name}|{'-'.join(added)}|theta={theta}")

    assert absorption_count == 77
    assert gap_count == 8
    digest = sha256(("\n".join(records) + "\n").encode()).hexdigest()
    print(f"blocker_states={len(BLOCKER_STATES)}")
    print(f"forced_G_edges={len(FORCED_G)}")
    print(f"forced_absorptions={absorption_count} all_three_clique=yes")
    print(f"blocker_gap_instances={gap_count} theta_all=4 external_escape=yes")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
