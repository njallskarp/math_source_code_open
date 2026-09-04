#!/usr/bin/env python3
"""Independent set-based audit of the Hall-compression theorem."""

from __future__ import annotations

import hashlib
import itertools
import json


def quotient(mask: int, order: int) -> list[set[int]]:
    out = [set() for _ in range(order)]
    bit = 0
    for first in range(order):
        for second in range(first + 1, order):
            if mask & (1 << bit):
                out[first].add(second)
            else:
                out[second].add(first)
            bit += 1
    return out


def expanded_graph(out: list[set[int]], sizes: tuple[int, ...]) -> tuple[list[set[int]], list[int]]:
    clusters: list[list[int]] = []
    next_vertex = 0
    for size in sizes:
        clusters.append(list(range(next_vertex, next_vertex + size)))
        next_vertex += size
    arcs = [set() for _ in range(next_vertex)]
    for cluster in clusters:
        for position, source in enumerate(cluster):
            arcs[source].update(cluster[position + 1 :])
    for source_cluster, targets in enumerate(out):
        for target_cluster in targets:
            for source in clusters[source_cluster]:
                arcs[source].update(clusters[target_cluster])
    return arcs, [cluster[-1] for cluster in clusters]


def second_neighbors(arcs: list[set[int]], vertex: int) -> set[int]:
    first = arcs[vertex]
    reached = set().union(*(arcs[head] for head in first)) if first else set()
    return reached.difference(first, {vertex})


def hall_strong(arcs: list[set[int]], vertex: int) -> bool:
    """Use Hall subsets directly, not a matching algorithm."""
    first = tuple(sorted(arcs[vertex]))
    second = second_neighbors(arcs, vertex)
    for subset_mask in range(1 << len(first)):
        subset = [first[index] for index in range(len(first)) if subset_mask >> index & 1]
        neighbors = set().union(*(arcs[source] & second for source in subset)) if subset else set()
        if len(neighbors) < len(subset):
            return False
    return True


def compressed_clusters(out: list[set[int]], sizes: tuple[int, ...]) -> list[int]:
    answer = []
    for root in range(len(out)):
        first = sorted(out[root])
        reached = set().union(*(out[head] for head in first)) if first else set()
        second = reached.difference(first, {root})
        succeeds = True
        for subset_mask in range(1 << len(first)):
            chosen = [first[index] for index in range(len(first)) if subset_mask >> index & 1]
            neighbors = {
                target for target in second if any(target in out[source] for source in chosen)
            }
            if sum(sizes[source] for source in chosen) > sum(sizes[target] for target in neighbors):
                succeeds = False
                break
        if succeeds:
            answer.append(root)
    return answer


def left_maximum_defect(out: list[set[int]], sizes: tuple[int, ...], root: int) -> int:
    first = sorted(out[root])
    reached = set().union(*(out[head] for head in first)) if first else set()
    second = reached.difference(first, {root})
    defects = []
    for count in range(len(first) + 1):
        for chosen_tuple in itertools.combinations(first, count):
            chosen = set(chosen_tuple)
            neighbors = {
                target for target in second if any(target in out[source] for source in chosen)
            }
            defects.append(
                sum(sizes[source] for source in chosen)
                - sum(sizes[target] for target in neighbors)
            )
    return max(defects)


def right_maximum_defect(out: list[set[int]], sizes: tuple[int, ...], root: int) -> int:
    first = sorted(out[root])
    reached = set().union(*(out[head] for head in first)) if first else set()
    second = sorted(reached.difference(first, {root}))
    defects = []
    for count in range(len(second) + 1):
        for right_tuple in itertools.combinations(second, count):
            right = set(right_tuple)
            forced = {
                source for source in first if (out[source] & set(second)).issubset(right)
            }
            defects.append(
                sum(sizes[source] for source in forced)
                - sum(sizes[target] for target in right)
            )
    return max(defects)


PUBLISHED_OUT = [
    {1, 4, 5},
    {3, 4, 5},
    {0, 1, 3},
    {0, 4},
    {2, 5},
    {2, 3},
]
PUBLISHED_SIZES = (7, 3, 11, 3, 9, 3)
PUBLISHED_LEFT = ({1, 4, 5}, {4, 5}, {0, 1, 3}, {0}, {2, 5}, {2})


def main() -> None:
    digest = hashlib.sha256()
    cases = 0
    vertices = 0
    for order in range(1, 5):
        for mask in range(1 << (order * (order - 1) // 2)):
            out = quotient(mask, order)
            for sizes in itertools.product((1, 2), repeat=order):
                arcs, terminals = expanded_graph(out, sizes)
                direct = [vertex for vertex in range(len(arcs)) if hall_strong(arcs, vertex)]
                compressed = [terminals[cluster] for cluster in compressed_clusters(out, sizes)]
                if direct != compressed:
                    raise AssertionError((order, mask, sizes, direct, compressed))
                for root in range(order):
                    left_defect = left_maximum_defect(out, sizes, root)
                    right_defect = right_maximum_defect(out, sizes, root)
                    if left_defect != right_defect:
                        raise AssertionError(
                            (order, mask, sizes, root, left_defect, right_defect)
                        )
                digest.update(f"{order}|{mask}|{sizes}|{direct}\n".encode("ascii"))
                cases += 1
                vertices += len(arcs)

    margins = []
    for root, chosen in enumerate(PUBLISHED_LEFT):
        first = PUBLISHED_OUT[root]
        reached = set().union(*(PUBLISHED_OUT[head] for head in first)) if first else set()
        second = reached.difference(first, {root})
        neighbors = {
            target for target in second if any(target in PUBLISHED_OUT[source] for source in chosen)
        }
        margins.append(
            sum(PUBLISHED_SIZES[source] for source in chosen)
            - sum(PUBLISHED_SIZES[target] for target in neighbors)
        )
    if margins != [1] * 6 or compressed_clusters(PUBLISHED_OUT, PUBLISHED_SIZES):
        raise AssertionError("published certificate check failed")

    print(
        json.dumps(
            {
                "audit_sha256": digest.hexdigest(),
                "cases": cases,
                "published_defect_margins": margins,
                "published_strong_clusters": [],
                "quotient_orders": [1, 2, 3, 4],
                "status": "INDEPENDENT HALL-CUT DUALITY VERIFIED",
                "vertex_instances": vertices,
                "weight_values": [1, 2],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
