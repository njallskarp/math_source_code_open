#!/usr/bin/env python3
"""Exact audits for the mixed-radix line-partition theorem.

CPython 3.12+, standard library only.  All arithmetic is integral and every
constructed bounded partition is checked at cell level.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections.abc import Iterable, Sequence


Cell = tuple[int, ...]


def mixed_radix_count(sides: Sequence[int], s: int, order: Sequence[int]) -> int:
    """Return Q in the telescoping mixed-radix identity."""
    prefix_remainders = 1
    total = 0
    for position, axis in enumerate(order):
        quotient, remainder = divmod(sides[axis], s)
        later_product = math.prod(sides[j] for j in order[position + 1 :])
        total += prefix_remainders * quotient * later_product
        prefix_remainders *= remainder
    return total


def line_partition(sides: Sequence[int], s: int) -> list[tuple[Cell, ...]]:
    """Construct the line partition when the residue product is below s."""
    if not sides or s < 1 or min(sides) < 1:
        raise ValueError("positive sides and s are required")
    eligible = [axis for axis, side in enumerate(sides) if side >= s]
    if not eligible:
        raise ValueError("at least one side must be at least s")
    if math.prod(side % s for side in sides) >= s:
        raise ValueError("the residue-product hypothesis is false")

    last = eligible[-1]
    order = [axis for axis in range(len(sides)) if axis != last] + [last]
    active_values = [list(range(side)) for side in sides]
    classes: list[tuple[Cell, ...]] = []

    for axis in order[:-1]:
        quotient, remainder = divmod(sides[axis], s)
        other_axes = [j for j in range(len(sides)) if j != axis]
        for fixed in itertools.product(*(active_values[j] for j in other_axes)):
            base = dict(zip(other_axes, fixed, strict=True))
            for block in range(quotient):
                cells = []
                for value in range(block * s, (block + 1) * s):
                    cell = tuple(value if j == axis else base[j] for j in range(len(sides)))
                    cells.append(cell)
                classes.append(tuple(cells))
        active_values[axis] = list(range(sides[axis] - remainder, sides[axis]))

    axis = last
    quotient, remainder = divmod(sides[axis], s)
    other_axes = [j for j in range(len(sides)) if j != axis]
    for fixed in itertools.product(*(active_values[j] for j in other_axes)):
        base = dict(zip(other_axes, fixed, strict=True))
        start = 0
        for block in range(quotient):
            stop = start + s
            if block == quotient - 1:
                stop += remainder
            cells = []
            for value in range(start, stop):
                cell = tuple(value if j == axis else base[j] for j in range(len(sides)))
                cells.append(cell)
            classes.append(tuple(cells))
            start = stop
        if start != sides[axis]:
            raise AssertionError("final line was not exhausted")
    return classes


def varying_axes(cells: Iterable[Cell]) -> int:
    cells = tuple(cells)
    return sum(len({cell[axis] for cell in cells}) > 1 for axis in range(len(cells[0])))


def check_partition(sides: Sequence[int], s: int) -> int:
    classes = line_partition(sides, s)
    expected_cells = set(itertools.product(*(range(side) for side in sides)))
    seen: set[Cell] = set()
    for cells in classes:
        assert len(cells) >= s
        assert varying_axes(cells) <= 1
        assert len(set(cells)) == len(cells)
        assert seen.isdisjoint(cells)
        seen.update(cells)
    assert seen == expected_cells
    assert len(classes) == math.prod(sides) // s
    return len(classes)


def audit_identity(max_side: int, max_dimension: int) -> tuple[int, int]:
    tuples = 0
    qualifying = 0
    for dimension in range(1, max_dimension + 1):
        for sides in itertools.product(range(1, max_side + 1), repeat=dimension):
            for s in range(1, max(sides) + 1):
                last = max(range(dimension), key=sides.__getitem__)
                order = [axis for axis in range(dimension) if axis != last] + [last]
                q = mixed_radix_count(sides, s, order)
                residue_product = math.prod(side % s for side in sides)
                assert math.prod(sides) == s * q + residue_product
                tuples += 1
                if residue_product < s:
                    assert q == math.prod(sides) // s
                    qualifying += 1
    return tuples, qualifying


def hamming_parameters(max_side: int) -> tuple[int, int, int]:
    near_triangle = 0
    qualifying = 0
    genuinely_nondivisible = 0
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
                    assert s <= n3
                    residues = [n2 % s, n3 % s, n4 % s]
                    if math.prod(residues) < s:
                        qualifying += 1
                        if all(residues):
                            genuinely_nondivisible += 1
    return near_triangle, qualifying, genuinely_nondivisible


def audit_constructed_hamming(max_side: int) -> tuple[int, int]:
    instances = 0
    classes = 0
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
                    if math.prod(side % s for side in sides) >= s:
                        continue
                    partition = line_partition(sides, s)
                    assert len(partition) == math.prod(sides) // s
                    expected_cells = set(itertools.product(*(range(side) for side in sides)))
                    seen: set[Cell] = set()
                    for line_class in partition:
                        assert len(line_class) >= s
                        assert varying_axes(line_class) <= 1
                        assert (n1 - 1) + len(line_class) - 1 >= h
                        assert seen.isdisjoint(line_class)
                        seen.update(line_class)
                    assert seen == expected_cells
                    instances += 1
                    classes += len(partition)
    return instances, classes


def audit_generic_partitions(max_side: int) -> tuple[int, int]:
    instances = 0
    classes = 0
    for sides in itertools.product(range(1, max_side + 1), repeat=3):
        for s in range(1, max(sides) + 1):
            if math.prod(side % s for side in sides) >= s:
                continue
            classes += check_partition(sides, s)
            instances += 1
    return instances, classes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--identity-max-side", type=int, default=10)
    parser.add_argument("--identity-max-dimension", type=int, default=4)
    parser.add_argument("--parameter-max-side", type=int, default=60)
    parser.add_argument("--partition-max-side", type=int, default=9)
    parser.add_argument("--hamming-construction-max-side", type=int, default=12)
    args = parser.parse_args()

    identity, identity_qualifying = audit_identity(
        args.identity_max_side, args.identity_max_dimension
    )
    near, qualifying, nondivisible = hamming_parameters(args.parameter_max_side)
    generic, generic_classes = audit_generic_partitions(args.partition_max_side)
    hamming, hamming_classes = audit_constructed_hamming(
        args.hamming_construction_max_side
    )

    print(f"mixed-radix identities checked: {identity}")
    print(f"qualifying identities checked: {identity_qualifying}")
    print(f"four-dimensional near-triangle parameters checked: {near}")
    print(f"residue-product families detected: {qualifying}")
    print(f"genuinely nondivisible families detected: {nondivisible}")
    print(f"generic cell-level partitions checked: {generic}")
    print(f"generic line classes checked: {generic_classes}")
    print(f"lifted Hamming partitions checked: {hamming}")
    print(f"lifted Hamming colour classes checked: {hamming_classes}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
