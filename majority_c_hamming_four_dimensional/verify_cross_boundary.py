#!/usr/bin/env python3
"""Exact audits for the cyclic cross-boundary rectangle partition.

CPython 3.12+, standard library only.  The universal claims are proved in
CROSS_BOUNDARY_EXCHANGE.md; this checker reconstructs bounded partitions and
audits the stated Hamming criteria and infinite family.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections.abc import Sequence


Cell = tuple[int, ...]
Part = tuple[Cell, ...]


def varying_coordinates(part: Sequence[Cell]) -> tuple[int, ...]:
    return tuple(
        axis
        for axis in range(len(part[0]))
        if len({cell[axis] for cell in part}) > 1
    )


def is_line_part(part: Sequence[Cell]) -> bool:
    return bool(part) and len(varying_coordinates(part)) <= 1


def rectangle_partition(m: int, n: int, s: int) -> list[Part]:
    if s < 2 or m < s or n < s:
        raise ValueError("require s>=2 and m,n>=s")

    u, a = divmod(m, s)
    v, b = divmod(n, s)
    parts: list[Part] = []

    if a == 0:
        for column in range(n):
            for block in range(u):
                parts.append(
                    tuple((row, column) for row in range(block * s, (block + 1) * s))
                )
        return parts

    if b == 0:
        for row in range(m):
            for block in range(v):
                parts.append(
                    tuple((row, column) for column in range(block * s, (block + 1) * s))
                )
        return parts

    row_cut = (u - 1) * s
    for column in range(n):
        for block in range(u - 1):
            parts.append(
                tuple((row, column) for row in range(block * s, (block + 1) * s))
            )

    remaining_rows = tuple(range(row_cut, m))
    col_cut = (v - 1) * s
    for row in remaining_rows:
        for block in range(v - 1):
            parts.append(
                tuple((row, column) for column in range(block * s, (block + 1) * s))
            )

    quotient = (a * b) // s
    selected_columns = b + quotient
    corner_width = s + b
    marked_by_column: list[list[Cell]] = [list() for _ in range(selected_columns)]

    for local_row, row in enumerate(remaining_rows):
        marked = {
            (local_row * b + offset) % selected_columns
            for offset in range(b)
        }
        assert len(marked) == b
        row_part = tuple(
            (row, col_cut + local_column)
            for local_column in range(corner_width)
            if local_column not in marked
        )
        assert len(row_part) == s
        parts.append(row_part)
        for local_column in marked:
            marked_by_column[local_column].append((row, col_cut + local_column))

    column_sizes = [len(marked) for marked in marked_by_column]
    assert min(column_sizes) >= s
    assert max(column_sizes) - min(column_sizes) <= 1
    parts.extend(tuple(marked) for marked in marked_by_column)
    return parts


def check_partition(m: int, n: int, s: int) -> tuple[int, int]:
    parts = rectangle_partition(m, n, s)
    expected = set(itertools.product(range(m), range(n)))
    seen: set[Cell] = set()
    for part in parts:
        assert len(part) >= s
        assert len(set(part)) == len(part)
        assert is_line_part(part)
        assert seen.isdisjoint(part)
        seen.update(part)
    assert seen == expected
    assert len(parts) == (m * n) // s
    return len(parts), len(seen)


def audit_rectangles(max_s: int, quotient_margin: int) -> tuple[int, int, int, int]:
    instances = 0
    parts = 0
    cells = 0
    switches = 0
    for s in range(2, max_s + 1):
        for m in range(s, quotient_margin * s + 1):
            for n in range(s, quotient_margin * s + 1):
                count, volume = check_partition(m, n, s)
                instances += 1
                parts += count
                cells += volume
                if m % s and n % s:
                    switches += 1
    return instances, parts, cells, switches


def qualifying_pair(sides: Sequence[int], s: int) -> tuple[int, int, int] | None:
    if s < 2:
        return None
    for first, second in itertools.combinations(range(3), 2):
        remaining = 3 - first - second
        if sides[first] < s or sides[second] < s:
            continue
        remainder = (sides[first] * sides[second]) % s
        if sides[remaining] * remainder < s:
            return first, second, remaining
    return None


def previous_exact(sides: Sequence[int], s: int) -> bool:
    residues = [side % s for side in sides]
    volume = math.prod(residues)
    if volume < s:
        return True
    if (
        s <= volume < 2 * s
        and sum(residues) >= s + len(sides) - 1
    ):
        return True
    return s == 3 and residues == [2, 2, 2]


def audit_parameters(max_side: int) -> tuple[int, int, int]:
    near_triangle = 0
    exchange = 0
    genuinely_new = 0
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
                    if qualifying_pair(sides, s) is None:
                        continue
                    exchange += 1
                    if not previous_exact(sides, s):
                        genuinely_new += 1
    return near_triangle, exchange, genuinely_new


def embedded_minor_partition(sides: Sequence[int], s: int) -> list[Part]:
    pair = qualifying_pair(sides, s)
    if pair is None:
        raise ValueError("pair-remainder criterion is false")
    first, second, remaining = pair
    rectangle = rectangle_partition(sides[first], sides[second], s)
    parts: list[Part] = []
    for fixed in range(sides[remaining]):
        for rectangle_part in rectangle:
            embedded: list[Cell] = []
            for left, right in rectangle_part:
                cell = [0, 0, 0]
                cell[first] = left
                cell[second] = right
                cell[remaining] = fixed
                embedded.append(tuple(cell))
            parts.append(tuple(embedded))
    return parts


def audit_hamming_constructions(max_side: int) -> tuple[int, int, int]:
    instances = 0
    parts_checked = 0
    cells_checked = 0
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
                    if qualifying_pair(sides, s) is None:
                        continue
                    parts = embedded_minor_partition(sides, s)
                    expected = set(itertools.product(*(range(side) for side in sides)))
                    seen: set[Cell] = set()
                    for part in parts:
                        assert len(part) >= s
                        assert len(set(part)) == len(part)
                        assert is_line_part(part)
                        assert deficits[0] + len(part) - 1 >= h
                        assert seen.isdisjoint(part)
                        seen.update(part)
                    assert seen == expected
                    assert len(parts) == math.prod(sides) // s
                    instances += 1
                    parts_checked += len(parts)
                    cells_checked += len(seen)
    return instances, parts_checked, cells_checked


def audit_infinite_family(max_k: int, reconstruct_max_k: int) -> tuple[int, int, int]:
    checked = 0
    reconstructed = 0
    reconstructed_parts = 0
    for k in range(2, max_k + 1):
        s = k * k
        orders = [s + 2 * k + 3, s + k, s + k, s + 2]
        assert orders == sorted(orders, reverse=True)
        deficits = [order - 1 for order in orders]
        h = (sum(deficits) + 1) // 2
        assert h == 2 * s + 2 * k + 1
        assert h - deficits[0] + 1 == s
        residues = [order % s for order in orders[1:]]
        assert residues == [k, k, 2]
        assert math.prod(residues) == 2 * s
        assert orders[1] % s and orders[2] % s and orders[3] % s
        assert (orders[1] * orders[2]) % s == 0
        expected = (k + 1) ** 2 * (s + 2)
        assert math.prod(orders[1:]) // s == expected
        checked += 1

        if k <= reconstruct_max_k:
            parts = embedded_minor_partition(orders[1:], s)
            assert len(parts) == expected
            assert all(len(part) >= s and is_line_part(part) for part in parts)
            reconstructed += 1
            reconstructed_parts += len(parts)
    return checked, reconstructed, reconstructed_parts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rectangle-max-s", type=int, default=18)
    parser.add_argument("--rectangle-quotient-margin", type=int, default=3)
    parser.add_argument("--parameter-max-side", type=int, default=60)
    parser.add_argument("--hamming-max-side", type=int, default=16)
    parser.add_argument("--family-max-k", type=int, default=10000)
    parser.add_argument("--family-reconstruct-max-k", type=int, default=5)
    args = parser.parse_args()

    rectangle = audit_rectangles(
        args.rectangle_max_s, args.rectangle_quotient_margin
    )
    parameters = audit_parameters(args.parameter_max_side)
    hamming = audit_hamming_constructions(args.hamming_max_side)
    family = audit_infinite_family(
        args.family_max_k, args.family_reconstruct_max_k
    )

    print(f"rectangle partitions reconstructed: {rectangle[0]}")
    print(f"rectangle line parts checked: {rectangle[1]}")
    print(f"rectangle cells checked: {rectangle[2]}")
    print(f"cyclic corner switches checked: {rectangle[3]}")
    print(f"four-dimensional near-triangle parameters checked: {parameters[0]}")
    print(f"pair-remainder parameters detected: {parameters[1]}")
    print(f"genuinely new pair-exchange parameters detected: {parameters[2]}")
    print(f"lifted Hamming partitions reconstructed: {hamming[0]}")
    print(f"lifted Hamming line parts checked: {hamming[1]}")
    print(f"lifted Hamming minor cells checked: {hamming[2]}")
    print(f"explicit infinite-family indices checked: {family[0]}")
    print(f"explicit family partitions reconstructed: {family[1]}")
    print(f"explicit family line parts checked: {family[2]}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
