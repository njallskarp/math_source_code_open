#!/usr/bin/env python3
"""Independent checks for the six-cluster Strong Seymour minimum.

This program imports no C++ code.  It constructs quotient-tournament orbits by
set partition rather than canonical scanning and computes bipartite matchings
with Hopcroft--Karp rather than the verifier's one-path-at-a-time algorithm.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from math import comb

Sizes = tuple[int, int, int, int, int, int]

PAIRS = tuple((i, j) for i in range(6) for j in range(i + 1, 6))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
PUBLISHED_OUT = (
    (1, 4, 5),
    (3, 4, 5),
    (0, 1, 3),
    (0, 4),
    (2, 5),
    (2, 3),
)
PUBLISHED_SIZES: Sizes = (7, 3, 11, 3, 9, 3)


def relabel(mask: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    for bit, (i, j) in enumerate(PAIRS):
        source, target = (i, j) if mask >> bit & 1 else (j, i)
        source, target = permutation[source], permutation[target]
        low, high = sorted((source, target))
        if source == low:
            answer |= 1 << PAIR_INDEX[(low, high)]
    return answer


def quotient_orbit_representatives() -> list[int]:
    permutations = tuple(itertools.permutations(range(6)))
    remaining = set(range(1 << 15))
    representatives: list[int] = []
    while remaining:
        representative = min(remaining)
        orbit = {relabel(representative, permutation) for permutation in permutations}
        if representative != min(orbit) or not orbit <= remaining:
            raise AssertionError("quotient tournament orbit partition failed")
        remaining.difference_update(orbit)
        representatives.append(representative)
    return representatives


def published_quotient() -> int:
    answer = 0
    out = [set(row) for row in PUBLISHED_OUT]
    for bit, (i, j) in enumerate(PAIRS):
        if j in out[i]:
            answer |= 1 << bit
        elif i not in out[j]:
            raise AssertionError("published quotient is not a tournament")
    return answer


def blowup(sizes: Sizes, quotient: int) -> list[int]:
    if min(sizes) < 1:
        raise ValueError("cluster sizes must be positive")
    starts: list[int] = []
    n = 0
    for size in sizes:
        starts.append(n)
        n += size
    if n > 63:
        raise ValueError("this bitset checker supports at most 63 vertices")
    rows = [0] * n
    for cluster, size in enumerate(sizes):
        for first in range(starts[cluster], starts[cluster] + size):
            for second in range(first + 1, starts[cluster] + size):
                rows[first] |= 1 << second
    for bit, (i, j) in enumerate(PAIRS):
        source, target = (i, j) if quotient >> bit & 1 else (j, i)
        target_mask = ((1 << sizes[target]) - 1) << starts[target]
        for vertex in range(starts[source], starts[source] + sizes[source]):
            rows[vertex] |= target_mask
    return rows


def check_tournament(rows: list[int]) -> None:
    n = len(rows)
    for i in range(n):
        if rows[i] >> i & 1:
            raise AssertionError("loop")
        for j in range(i + 1, n):
            if ((rows[i] >> j) & 1) + ((rows[j] >> i) & 1) != 1:
                raise AssertionError("not a tournament")


def maximum_matching(rows: list[int], left_mask: int, right_mask: int) -> int:
    left = [vertex for vertex in range(len(rows)) if left_mask >> vertex & 1]
    right = [vertex for vertex in range(len(rows)) if right_mask >> vertex & 1]
    pair_left = {vertex: -1 for vertex in left}
    pair_right = {vertex: -1 for vertex in right}
    distance: dict[int, int] = {}

    def bfs() -> bool:
        queue: deque[int] = deque()
        for vertex in left:
            if pair_left[vertex] == -1:
                distance[vertex] = 0
                queue.append(vertex)
            else:
                distance[vertex] = -1
        found = False
        while queue:
            vertex = queue.popleft()
            for head in right:
                if not (rows[vertex] >> head & 1):
                    continue
                mate = pair_right[head]
                if mate == -1:
                    found = True
                elif distance[mate] == -1:
                    distance[mate] = distance[vertex] + 1
                    queue.append(mate)
        return found

    def dfs(vertex: int) -> bool:
        for head in right:
            if not (rows[vertex] >> head & 1):
                continue
            mate = pair_right[head]
            if mate == -1 or (distance.get(mate) == distance[vertex] + 1 and dfs(mate)):
                pair_left[vertex] = head
                pair_right[head] = vertex
                return True
        distance[vertex] = -1
        return False

    matching = 0
    while bfs():
        for vertex in left:
            if pair_left[vertex] == -1 and dfs(vertex):
                matching += 1
    return matching


def strong_vertices(rows: list[int]) -> list[int]:
    universe = (1 << len(rows)) - 1
    result: list[int] = []
    for x, first in enumerate(rows):
        reachable = 0
        for y in range(len(rows)):
            if first >> y & 1:
                reachable |= rows[y]
        second = reachable & ~(first | (1 << x)) & universe
        if maximum_matching(rows, first, second) == first.bit_count():
            result.append(x)
    return result


def has_no_strong_vertex(rows: list[int]) -> bool:
    universe = (1 << len(rows)) - 1
    for x, first in enumerate(rows):
        reachable = 0
        work = first
        while work:
            bit = work & -work
            work ^= bit
            reachable |= rows[bit.bit_length() - 1]
        second = reachable & ~(first | (1 << x)) & universe
        if maximum_matching(rows, first, second) == first.bit_count():
            return False
    return True


def main() -> None:
    representatives = quotient_orbit_representatives()
    if len(representatives) != 56:
        raise AssertionError("there must be 56 unlabeled six-vertex tournaments")
    representative_bytes = "".join(f"{mask}\n" for mask in representatives).encode("ascii")

    published = blowup(PUBLISHED_SIZES, published_quotient())
    check_tournament(published)
    if strong_vertices(published):
        raise AssertionError("published order-36 blow-up must have no strong vertex")

    shell_counts: list[int] = []
    for removed_cluster in range(-1, 6):
        sizes = list(PUBLISHED_SIZES)
        if removed_cluster >= 0:
            sizes[removed_cluster] -= 1
        count = 0
        for quotient in range(1 << 15):
            count += has_no_strong_vertex(blowup(tuple(sizes), quotient))
        shell_counts.append(count)
    if shell_counts != [6, 0, 0, 0, 0, 0, 0]:
        raise AssertionError(f"unexpected nearest-shell counts: {shell_counts}")

    configuration_count = sum(comb(total - 1, 5) * 56 for total in range(6, 36))
    if configuration_count != 90_896_960:
        raise AssertionError("composition/orbit product count failed")

    print(
        json.dumps(
            {
                "all_six_cluster_configurations_through_35": configuration_count,
                "published_order": len(published),
                "published_strong_vertices": [],
                "quotient_classes": len(representatives),
                "quotient_representatives_sha256": hashlib.sha256(representative_bytes).hexdigest(),
                "shell_no_strong_counts": shell_counts,
                "status": "INDEPENDENT VERIFIED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
