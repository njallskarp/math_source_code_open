#!/usr/bin/env python3
"""Exact audits for the multi-box barrier and its s=3 exception.

CPython 3.12+, standard library only.  The universal result is the proof in
MULTIBOX_OBSTRUCTION.md; these bounded checks audit its identities and the
explicit constructions.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections.abc import Iterable, Sequence


Cell = tuple[int, ...]


def hamming_adjacent(left: Cell, right: Cell) -> bool:
    return sum(a != b for a, b in zip(left, right, strict=True)) == 1


def minimum_degree(cells: Sequence[Cell]) -> int:
    return min(
        sum(hamming_adjacent(vertex, other) for other in cells)
        for vertex in cells
    )


def shell_bound(profile: Sequence[int], h: int) -> int:
    total = sum(profile)
    numerator = 2 * (1 + total) + sum(a * (h - a) for a in profile)
    return (numerator + 1) // 2


def audit_shell_profiles(max_s: int, max_dimension: int) -> int:
    checked = 0
    for s in range(3, max_s + 1):
        h = s - 1
        for dimension in range(2, max_dimension + 1):
            for profile in itertools.product(range(h), repeat=dimension):
                if sum(profile) < h:
                    continue
                assert shell_bound(profile, h) >= 2 * h
                checked += 1
    return checked


def box_cells(sides: Sequence[int]) -> tuple[Cell, ...]:
    return tuple(itertools.product(*(range(side) for side in sides)))


def induced_minimum_degree_mask(cells: Sequence[Cell], mask: int) -> int:
    chosen = [cells[i] for i in range(len(cells)) if mask & (1 << i)]
    return minimum_degree(chosen)


def nondecreasing_boxes(s: int, max_volume: int) -> Iterable[tuple[int, int, int]]:
    for a in range(1, s):
        for b in range(a, s):
            for c in range(b, s):
                if a * b * c <= max_volume:
                    yield a, b, c


def audit_small_subsets(max_s: int, max_volume: int) -> tuple[int, int]:
    boxes = 0
    subsets = 0
    for s in range(3, max_s + 1):
        for sides in nondecreasing_boxes(s, max_volume):
            cells = box_cells(sides)
            boxes += 1
            for mask in range(1, 1 << len(cells)):
                if mask.bit_count() < 2 * s - 2:
                    assert induced_minimum_degree_mask(cells, mask) < s - 1
                subsets += 1
    return boxes, subsets


def audit_volume_obstruction(max_s: int) -> int:
    checked = 0
    for s in range(4, max_s + 1):
        for r2 in range(1, s):
            for r3 in range(1, s):
                for r4 in range(1, s):
                    volume = r2 * r3 * r4
                    quotient = volume // s
                    if quotient < 2:
                        continue
                    assert quotient * (2 * s - 2) >= (quotient + 1) * s
                    assert volume < (quotient + 1) * s
                    checked += 1
    return checked


def strip_exact_blocks(
    sides: Sequence[int], s: int
) -> tuple[list[tuple[Cell, ...]], tuple[Cell, ...]]:
    active = [list(range(side)) for side in sides]
    lines: list[tuple[Cell, ...]] = []
    for axis, side in enumerate(sides):
        quotient, remainder = divmod(side, s)
        other_axes = [j for j in range(len(sides)) if j != axis]
        for fixed in itertools.product(*(active[j] for j in other_axes)):
            base = dict(zip(other_axes, fixed, strict=True))
            for block in range(quotient):
                lines.append(
                    tuple(
                        tuple(
                            value if j == axis else base[j]
                            for j in range(len(sides))
                        )
                        for value in range(block * s, (block + 1) * s)
                    )
                )
        active[axis] = list(range(side - remainder, side))
    return lines, tuple(itertools.product(*active))


def exceptional_partition(
    sides: Sequence[int], s: int = 3
) -> list[tuple[Cell, ...]]:
    if [side % s for side in sides] != [2, 2, 2]:
        raise ValueError("the exceptional construction requires residues (2,2,2)")
    lines, residue = strip_exact_blocks(sides, s)
    face_values = sorted({cell[0] for cell in residue})
    assert len(face_values) == 2
    faces = [tuple(cell for cell in residue if cell[0] == value) for value in face_values]
    return [*lines, *faces]


def check_exceptional_partition(sides: Sequence[int]) -> int:
    parts = exceptional_partition(sides)
    expected = set(box_cells(sides))
    seen: set[Cell] = set()
    for part in parts:
        assert minimum_degree(part) >= 2
        assert seen.isdisjoint(part)
        seen.update(part)
    assert seen == expected
    assert len(parts) == math.prod(sides) // 3
    return len(parts)


def audit_exceptional_partitions(max_q: int) -> tuple[int, int]:
    instances = 0
    parts = 0
    for q2 in range(max_q + 1):
        for q3 in range(max_q + 1):
            for q4 in range(max_q + 1):
                sides = [3 * q2 + 2, 3 * q3 + 2, 3 * q4 + 2]
                parts += check_exceptional_partition(sides)
                instances += 1
    return instances, parts


def audit_hamming_families(max_q: int) -> int:
    checked = 0
    for q2 in range(max_q + 1):
        for q3 in range(q2 + 1):
            for q4 in range(q3 + 1):
                if q3 + q4 < 1:
                    continue
                q_sum = q2 + q3 + q4
                for epsilon in (0, 1):
                    orders = [
                        3 * q_sum + epsilon,
                        3 * q2 + 2,
                        3 * q3 + 2,
                        3 * q4 + 2,
                    ]
                    assert orders == sorted(orders, reverse=True)
                    deficits = [order - 1 for order in orders]
                    h = (sum(deficits) + 1) // 2
                    assert h == 3 * q_sum + epsilon + 1
                    assert h - deficits[0] + 1 == 3
                    assert [order % 3 for order in orders[1:]] == [2, 2, 2]
                    expected = (
                        9 * q2 * q3 * q4
                        + 6 * (q2 * q3 + q2 * q4 + q3 * q4)
                        + 4 * q_sum
                        + 2
                    )
                    assert math.prod(orders[1:]) // 3 == expected
                    checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-max-s", type=int, default=10)
    parser.add_argument("--profile-max-dimension", type=int, default=5)
    parser.add_argument("--subset-max-s", type=int, default=5)
    parser.add_argument("--subset-max-volume", type=int, default=12)
    parser.add_argument("--obstruction-max-s", type=int, default=100)
    parser.add_argument("--partition-max-q", type=int, default=3)
    parser.add_argument("--family-max-q", type=int, default=100)
    args = parser.parse_args()

    profiles = audit_shell_profiles(
        args.profile_max_s, args.profile_max_dimension
    )
    boxes, subsets = audit_small_subsets(
        args.subset_max_s, args.subset_max_volume
    )
    obstruction = audit_volume_obstruction(args.obstruction_max_s)
    partitions, parts = audit_exceptional_partitions(args.partition_max_q)
    families = audit_hamming_families(args.family_max_q)

    print(f"capped shell profiles checked: {profiles}")
    print(f"small residue boxes checked exhaustively: {boxes}")
    print(f"small residue subsets checked exhaustively: {subsets}")
    print(f"multi-box volume contradictions checked: {obstruction}")
    print(f"exceptional residue partitions reconstructed: {partitions}")
    print(f"exceptional partition parts checked: {parts}")
    print(f"explicit Hamming-family parameters checked: {families}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
