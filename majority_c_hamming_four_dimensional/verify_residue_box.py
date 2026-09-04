#!/usr/bin/env python3
"""Exact audits for one-box residue absorption.

CPython 3.12+, standard library only.  This checker reconstructs every bounded
partition it counts and checks Hamming adjacency directly.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections.abc import Sequence


Cell = tuple[int, ...]


def hamming_adjacent(left: Cell, right: Cell) -> bool:
    return sum(a != b for a, b in zip(left, right, strict=True)) == 1


def minimum_degree(cells: Sequence[Cell]) -> int:
    return min(
        sum(hamming_adjacent(vertex, other) for other in cells)
        for vertex in cells
    )


def strip_exact_blocks(
    sides: Sequence[int], s: int
) -> tuple[list[tuple[Cell, ...]], tuple[Cell, ...]]:
    if not sides or min(sides) < 1 or s < 1:
        raise ValueError("positive sides and s are required")

    active = [list(range(side)) for side in sides]
    line_classes: list[tuple[Cell, ...]] = []
    for axis, side in enumerate(sides):
        quotient, remainder = divmod(side, s)
        other_axes = [j for j in range(len(sides)) if j != axis]
        for fixed in itertools.product(*(active[j] for j in other_axes)):
            base = dict(zip(other_axes, fixed, strict=True))
            for block in range(quotient):
                cells = tuple(
                    tuple(
                        value if j == axis else base[j]
                        for j in range(len(sides))
                    )
                    for value in range(block * s, (block + 1) * s)
                )
                line_classes.append(cells)
        active[axis] = list(range(side - remainder, side))

    residue_box = tuple(itertools.product(*active))
    return line_classes, residue_box


def residue_hypothesis(sides: Sequence[int], s: int) -> bool:
    residues = [side % s for side in sides]
    volume = math.prod(residues)
    return (
        s <= volume < 2 * s
        and sum(residues) >= s + len(sides) - 1
    )


def check_partition(sides: Sequence[int], s: int) -> tuple[int, int]:
    if not residue_hypothesis(sides, s):
        raise ValueError("residue-box hypotheses are false")

    lines, residue = strip_exact_blocks(sides, s)
    expected = set(itertools.product(*(range(side) for side in sides)))
    seen: set[Cell] = set()
    for line in lines:
        assert len(line) == s
        assert minimum_degree(line) == s - 1
        assert seen.isdisjoint(line)
        seen.update(line)

    residues = [side % s for side in sides]
    assert len(residue) == math.prod(residues)
    assert minimum_degree(residue) == sum(value - 1 for value in residues)
    assert minimum_degree(residue) >= s - 1
    assert seen.isdisjoint(residue)
    seen.update(residue)
    assert seen == expected

    number_of_parts = len(lines) + 1
    assert number_of_parts == math.prod(sides) // s
    return number_of_parts, len(lines)


def audit_generic(max_side: int, max_dimension: int) -> tuple[int, int, int]:
    instances = 0
    parts = 0
    line_classes = 0
    for dimension in range(2, max_dimension + 1):
        for sides in itertools.product(range(1, max_side + 1), repeat=dimension):
            for s in range(2, max(sides) + 1):
                if not residue_hypothesis(sides, s):
                    continue
                count, lines = check_partition(sides, s)
                instances += 1
                parts += count
                line_classes += lines
    return instances, parts, line_classes


def audit_parameters(max_side: int) -> tuple[int, int, int]:
    near_triangle = 0
    complementary = 0
    old_mixed_radix = 0
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    deficits = [n1 - 1, n2 - 1, n3 - 1, n4 - 1]
                    h = (sum(deficits) + 1) // 2
                    if h < deficits[0]:
                        continue
                    near_triangle += 1
                    s = h - deficits[0] + 1
                    sides = [n2, n3, n4]
                    residues = [side % s for side in sides]
                    product = math.prod(residues)
                    if product < s:
                        old_mixed_radix += 1
                    if residue_hypothesis(sides, s):
                        assert product >= s
                        complementary += 1
    return near_triangle, old_mixed_radix, complementary


def audit_hamming_constructions(max_side: int) -> tuple[int, int]:
    instances = 0
    colour_classes = 0
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    deficits = [n1 - 1, n2 - 1, n3 - 1, n4 - 1]
                    h = (sum(deficits) + 1) // 2
                    if h < deficits[0]:
                        continue
                    s = h - deficits[0] + 1
                    sides = [n2, n3, n4]
                    if not residue_hypothesis(sides, s):
                        continue
                    lines, residue = strip_exact_blocks(sides, s)
                    for part in [*lines, residue]:
                        assert (n1 - 1) + minimum_degree(part) >= h
                    assert len(lines) + 1 == math.prod(sides) // s
                    instances += 1
                    colour_classes += len(lines) + 1
    return instances, colour_classes


def audit_infinite_family(max_s: int) -> int:
    checked = 0
    for s in range(3, max_s + 1):
        n1, n2, n3, n4 = 2 * s + 2, 2 * s - 1, s + 2, s + 1
        assert n1 >= n2 >= n3 >= n4 >= 2
        deficits = [n1 - 1, n2 - 1, n3 - 1, n4 - 1]
        h = (sum(deficits) + 1) // 2
        assert h == 3 * s
        assert h - deficits[0] + 1 == s
        sides = [n2, n3, n4]
        assert [side % s for side in sides] == [s - 1, 2, 1]
        assert residue_hypothesis(sides, s)
        assert math.prod(sides) // s == 2 * s * s + 5 * s
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generic-max-side", type=int, default=8)
    parser.add_argument("--generic-max-dimension", type=int, default=4)
    parser.add_argument("--parameter-max-side", type=int, default=60)
    parser.add_argument("--hamming-max-side", type=int, default=14)
    parser.add_argument("--family-max-s", type=int, default=10000)
    args = parser.parse_args()

    generic, parts, lines = audit_generic(
        args.generic_max_side, args.generic_max_dimension
    )
    near, old, complementary = audit_parameters(args.parameter_max_side)
    hamming, colours = audit_hamming_constructions(args.hamming_max_side)
    family = audit_infinite_family(args.family_max_s)

    print(f"generic residue-box partitions checked: {generic}")
    print(f"generic partition parts checked: {parts}")
    print(f"generic exact line classes checked: {lines}")
    print(f"four-dimensional near-triangle parameters checked: {near}")
    print(f"previous mixed-radix parameters detected: {old}")
    print(f"new complementary parameters detected: {complementary}")
    print(f"lifted Hamming constructions checked: {hamming}")
    print(f"lifted majority-C colour classes checked: {colours}")
    print(f"explicit infinite-family indices checked: {family}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
