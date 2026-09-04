#!/usr/bin/env python3
"""Definition-level audit of weighted Hall compression for transitive blow-ups."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections.abc import Iterable, Sequence


def tournament(mask: int, order: int) -> tuple[frozenset[int], ...]:
    """Decode one bit per unordered pair; bit 1 orients low -> high."""
    if order < 1 or mask < 0 or mask >= 1 << (order * (order - 1) // 2):
        raise ValueError("invalid tournament encoding")
    out = [set() for _ in range(order)]
    bit = 0
    for low in range(order):
        for high in range(low + 1, order):
            source, target = (low, high) if mask >> bit & 1 else (high, low)
            out[source].add(target)
            bit += 1
    return tuple(frozenset(row) for row in out)


def validate_quotient(out: Sequence[frozenset[int]]) -> None:
    order = len(out)
    if order < 1:
        raise ValueError("the quotient must be nonempty")
    for first in range(order):
        if first in out[first] or any(second < 0 or second >= order for second in out[first]):
            raise ValueError("invalid quotient arc")
        for second in range(first + 1, order):
            if (second in out[first]) + (first in out[second]) != 1:
                raise ValueError("the quotient must be a tournament")


def blowup(out: Sequence[frozenset[int]], sizes: Sequence[int]) -> tuple[int, ...]:
    """Build Q[TT_s0,...,TT_sq-1] as bitset out-neighborhood rows."""
    validate_quotient(out)
    if len(sizes) != len(out) or any(size < 1 for size in sizes):
        raise ValueError("cluster sizes must be positive and match the quotient")
    starts: list[int] = []
    total = 0
    for size in sizes:
        starts.append(total)
        total += size
    rows = [0] * total
    for cluster, size in enumerate(sizes):
        start = starts[cluster]
        for vertex in range(start, start + size):
            rows[vertex] |= ((1 << (start + size)) - 1) ^ ((1 << (vertex + 1)) - 1)
    for source, targets in enumerate(out):
        for target in targets:
            target_mask = ((1 << sizes[target]) - 1) << starts[target]
            for vertex in range(starts[source], starts[source] + sizes[source]):
                rows[vertex] |= target_mask
    return tuple(rows)


def exact_second(rows: Sequence[int], vertex: int) -> int:
    first = rows[vertex]
    reachable = 0
    work = first
    while work:
        bit = work & -work
        work ^= bit
        reachable |= rows[bit.bit_length() - 1]
    universe = (1 << len(rows)) - 1
    return reachable & ~(first | (1 << vertex)) & universe


def maximum_matching(rows: Sequence[int], left_mask: int, right_mask: int) -> int:
    matched_to = [-1] * len(rows)

    def augment(left: int, seen: int) -> tuple[bool, int]:
        candidates = rows[left] & right_mask & ~seen
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            seen |= bit
            right = bit.bit_length() - 1
            if matched_to[right] == -1:
                matched_to[right] = left
                return True, seen
            success, seen = augment(matched_to[right], seen)
            if success:
                matched_to[right] = left
                return True, seen
        return False, seen

    matching = 0
    work = left_mask
    while work:
        bit = work & -work
        work ^= bit
        success, _ = augment(bit.bit_length() - 1, 0)
        matching += success
    return matching


def direct_strong_vertices(rows: Sequence[int]) -> tuple[int, ...]:
    result: list[int] = []
    for vertex, first in enumerate(rows):
        second = exact_second(rows, vertex)
        if maximum_matching(rows, first, second) == first.bit_count():
            result.append(vertex)
    return tuple(result)


def second_quotient_clusters(
    out: Sequence[frozenset[int]], cluster: int
) -> frozenset[int]:
    first = out[cluster]
    reachable = set().union(*(out[head] for head in first)) if first else set()
    return frozenset(reachable.difference(first, {cluster}))


def quotient_hall_defects(
    out: Sequence[frozenset[int]], sizes: Sequence[int], cluster: int
) -> tuple[tuple[tuple[int, ...], tuple[int, ...], int], ...]:
    """Return (left cluster set, neighbor cluster set, weight defect)."""
    validate_quotient(out)
    if len(sizes) != len(out) or any(size < 1 for size in sizes):
        raise ValueError("cluster sizes must be positive and match the quotient")
    first = sorted(out[cluster])
    second = second_quotient_clusters(out, cluster)
    defects = []
    for subset_mask in range(1 << len(first)):
        left = tuple(first[index] for index in range(len(first)) if subset_mask >> index & 1)
        neighbors = tuple(
            target for target in sorted(second) if any(target in out[source] for source in left)
        )
        defect = sum(sizes[source] for source in left) - sum(sizes[target] for target in neighbors)
        defects.append((left, neighbors, defect))
    return tuple(defects)


def compressed_strong_clusters(
    out: Sequence[frozenset[int]], sizes: Sequence[int]
) -> tuple[int, ...]:
    return tuple(
        cluster
        for cluster in range(len(out))
        if max(defect for _, _, defect in quotient_hall_defects(out, sizes, cluster)) <= 0
    )


def terminal_vertices(sizes: Sequence[int]) -> tuple[int, ...]:
    terminals = []
    total = 0
    for size in sizes:
        total += size
        terminals.append(total - 1)
    return tuple(terminals)


PUBLISHED_OUT = (
    frozenset((1, 4, 5)),
    frozenset((3, 4, 5)),
    frozenset((0, 1, 3)),
    frozenset((0, 4)),
    frozenset((2, 5)),
    frozenset((2, 3)),
)
PUBLISHED_SIZES = (7, 3, 11, 3, 9, 3)
PUBLISHED_WITNESS_SUBSETS = ((1, 4, 5), (4, 5), (0, 1, 3), (0,), (2, 5), (2,))


def published_certificate() -> tuple[dict[str, object], ...]:
    rows = []
    for cluster, expected_left in enumerate(PUBLISHED_WITNESS_SUBSETS):
        lookup = {
            left: (neighbors, defect)
            for left, neighbors, defect in quotient_hall_defects(
                PUBLISHED_OUT, PUBLISHED_SIZES, cluster
            )
        }
        neighbors, defect = lookup[expected_left]
        rows.append(
            {
                "cluster": cluster,
                "left": expected_left,
                "neighbors": neighbors,
                "left_weight": sum(PUBLISHED_SIZES[index] for index in expected_left),
                "neighbor_weight": sum(PUBLISHED_SIZES[index] for index in neighbors),
                "defect": defect,
            }
        )
    return tuple(rows)


def all_sizes(order: int, maximum: int) -> Iterable[tuple[int, ...]]:
    return itertools.product(range(1, maximum + 1), repeat=order)


def main() -> None:
    digest = hashlib.sha256()
    cases = 0
    vertex_instances = 0
    for order in range(1, 5):
        edge_count = order * (order - 1) // 2
        for mask in range(1 << edge_count):
            out = tournament(mask, order)
            for sizes in all_sizes(order, 3):
                rows = blowup(out, sizes)
                direct = direct_strong_vertices(rows)
                terminals = terminal_vertices(sizes)
                compressed = tuple(terminals[index] for index in compressed_strong_clusters(out, sizes))
                if direct != compressed:
                    raise AssertionError(
                        f"compression mismatch: order={order}, mask={mask}, sizes={sizes}, "
                        f"direct={direct}, compressed={compressed}"
                    )
                digest.update(f"{order}|{mask}|{sizes}|{direct}\n".encode("ascii"))
                cases += 1
                vertex_instances += len(rows)

    certificate = published_certificate()
    if any(row["defect"] != 1 for row in certificate):
        raise AssertionError("the six published Hall obstructions must each have margin one")
    if compressed_strong_clusters(PUBLISHED_OUT, PUBLISHED_SIZES):
        raise AssertionError("the published quotient-weight pair must have no strong cluster")
    if direct_strong_vertices(blowup(PUBLISHED_OUT, PUBLISHED_SIZES)):
        raise AssertionError("the published order-36 blow-up must have no strong vertex")

    print(
        "VERIFIED QUOTIENT-WEIGHT HALL COMPRESSION; "
        f"orders=1..4 weight_max=3 cases={cases} vertex_instances={vertex_instances} "
        f"audit_sha256={digest.hexdigest()}"
    )
    print(json.dumps(certificate, separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()
