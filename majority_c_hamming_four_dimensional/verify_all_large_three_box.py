#!/usr/bin/env python3
"""Exact audits for anchored rectangles and all-large three-box partitions.

CPython 3.12+, standard library only. Universal claims are proved in
ALL_LARGE_THREE_BOX.md; this checker reconstructs bounded instances and
audits the Hamming consequence and explicit first-carry family.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections.abc import Sequence
from dataclasses import dataclass


Cell = tuple[int, ...]
Part = list[Cell]


def varying_coordinates(part: Sequence[Cell]) -> tuple[int, ...]:
    return tuple(
        axis
        for axis in range(len(part[0]))
        if len({cell[axis] for cell in part}) > 1
    )


def is_line_part(part: Sequence[Cell]) -> bool:
    return bool(part) and len(varying_coordinates(part)) <= 1


@dataclass
class RectangleWitness:
    parts: list[Part]
    large_part_by_column: dict[int, int]
    anchor_row: int
    corner_columns: tuple[int, ...]


def anchored_rectangle_partition(
    m: int, n: int, s: int, large_offset: int = 0
) -> RectangleWitness:
    if s < 2 or m < s or n < s:
        raise ValueError("require s>=2 and m,n>=s")

    u, a = divmod(m, s)
    v, b = divmod(n, s)
    parts: list[Part] = []

    if a == 0 or b == 0:
        if a == 0:
            for column in range(n):
                for block in range(u):
                    parts.append(
                        [(row, column) for row in range(block * s, (block + 1) * s)]
                    )
        else:
            for row in range(m):
                for block in range(v):
                    parts.append(
                        [(row, column) for column in range(block * s, (block + 1) * s)]
                    )
        return RectangleWitness(parts, {}, 0, tuple(range(n)))

    row_cut = (u - 1) * s
    for column in range(n):
        for block in range(u - 1):
            parts.append(
                [(row, column) for row in range(block * s, (block + 1) * s)]
            )

    corner_rows = tuple(range(row_cut, m))
    column_cut = (v - 1) * s
    for row in corner_rows:
        for block in range(v - 1):
            parts.append(
                [
                    (row, column)
                    for column in range(block * s, (block + 1) * s)
                ]
            )

    corner_columns = tuple(range(column_cut, n))
    corner_width = len(corner_columns)
    q, remainder = divmod(a * b, s)
    sparse_count = a + q
    full_count = s - q
    assert sparse_count + full_count == len(corner_rows)

    sparse_rows = corner_rows[:sparse_count]
    full_rows = corner_rows[sparse_count:]
    assert full_rows
    anchor_row = full_rows[0]

    rotation = large_offset % corner_width
    relabeled_columns = tuple(
        corner_columns[(local + rotation) % corner_width]
        for local in range(corner_width)
    )
    marked_by_local_column: list[list[Cell]] = [
        [] for _ in range(corner_width)
    ]

    cursor = 0
    for row in sparse_rows:
        marked_local = {
            (cursor + offset) % corner_width for offset in range(b)
        }
        cursor += b
        assert len(marked_local) == b
        parts.append(
            [
                (row, relabeled_columns[local])
                for local in range(corner_width)
                if local not in marked_local
            ]
        )
        for local in marked_local:
            marked_by_local_column[local].append(
                (row, relabeled_columns[local])
            )

    for row in full_rows:
        for local, column in enumerate(relabeled_columns):
            marked_by_local_column[local].append((row, column))

    large_part_by_column: dict[int, int] = {}
    for local, marked in enumerate(marked_by_local_column):
        part_index = len(parts)
        parts.append(marked)
        if local < remainder:
            large_part_by_column[relabeled_columns[local]] = part_index

    return RectangleWitness(
        parts, large_part_by_column, anchor_row, corner_columns
    )


def check_rectangle(m: int, n: int, s: int, offset: int) -> tuple[int, int, int]:
    witness = anchored_rectangle_partition(m, n, s, offset)
    expected = set(itertools.product(range(m), range(n)))
    seen: set[Cell] = set()
    quotient, remainder = divmod(m * n, s)
    assert len(witness.parts) == quotient
    assert len(witness.large_part_by_column) == remainder

    large_indices = set(witness.large_part_by_column.values())
    for index, part in enumerate(witness.parts):
        assert len(part) in (s, s + 1)
        assert (len(part) == s + 1) == (index in large_indices)
        assert is_line_part(part)
        assert seen.isdisjoint(part)
        seen.update(part)
    assert seen == expected

    for column, index in witness.large_part_by_column.items():
        assert (witness.anchor_row, column) in witness.parts[index]
    return len(witness.parts), len(seen), len(large_indices)


def audit_rectangles(max_s: int, margin: int) -> tuple[int, int, int, int]:
    instances = 0
    parts = 0
    cells = 0
    anchored_large_parts = 0
    for s in range(2, max_s + 1):
        for m in range(s, margin * s + 1):
            for n in range(s, margin * s + 1):
                offsets = (0, 1, n + 1)
                for offset in offsets:
                    count, volume, large = check_rectangle(m, n, s, offset)
                    instances += 1
                    parts += count
                    cells += volume
                    anchored_large_parts += large
    return instances, parts, cells, anchored_large_parts


def all_large_three_box_partition(m: int, n: int, p: int, s: int) -> list[Part]:
    if min(m, n, p) < s or s < 2:
        raise ValueError("require m,n,p>=s>=2")

    slab_count, residual_layers = divmod(p, s)
    pair_quotient, pair_remainder = divmod(m * n, s)
    parts: list[Part] = []
    first_vertical_index: dict[tuple[int, int], int] = {}

    for row in range(m):
        for column in range(n):
            for block in range(slab_count):
                index = len(parts)
                parts.append(
                    [
                        (row, column, layer)
                        for layer in range(block * s, (block + 1) * s)
                    ]
                )
                if block == 0:
                    first_vertical_index[(row, column)] = index

    donor_slots: list[tuple[int, Cell, int]] = []
    anchor_row: int | None = None
    corner_width: int | None = None
    for residual in range(residual_layers):
        witness = anchored_rectangle_partition(
            m, n, s, residual * pair_remainder
        )
        if anchor_row is None:
            anchor_row = witness.anchor_row
            corner_width = len(witness.corner_columns)
        assert witness.anchor_row == anchor_row
        assert len(witness.corner_columns) == corner_width

        embedded_index: dict[int, int] = {}
        layer = slab_count * s + residual
        for base_index, base_part in enumerate(witness.parts):
            embedded_index[base_index] = len(parts)
            parts.append([(row, column, layer) for row, column in base_part])

        if pair_remainder:
            assert corner_width is not None
            for local in range(pair_remainder):
                global_slot = residual * pair_remainder + local
                local_column = global_slot % corner_width
                column = witness.corner_columns[local_column]
                base_part_index = witness.large_part_by_column[column]
                donor = (anchor_row, column, layer)
                donor_slots.append(
                    (embedded_index[base_part_index], donor, column)
                )

    if residual_layers == 0 or pair_remainder == 0:
        assert len(parts) == (m * n * p) // s
        return parts

    assert anchor_row is not None
    carry_count = (residual_layers * pair_remainder) // s
    assert carry_count < s
    new_parts: list[Part] = []
    for group in range(carry_count):
        donors = donor_slots[group * s : (group + 1) * s]
        assert len(donors) == s
        assert len({column for _, _, column in donors}) == s
        displaced: Part = []
        for donor_part_index, donor, column in donors:
            parts[donor_part_index].remove(donor)
            vertical_index = first_vertical_index[(anchor_row, column)]
            displaced_cell = (anchor_row, column, group)
            parts[vertical_index].remove(displaced_cell)
            parts[vertical_index].append(donor)
            displaced.append(displaced_cell)
        new_parts.append(displaced)
    parts.extend(new_parts)

    expected_count = slab_count * m * n + residual_layers * pair_quotient
    expected_count += carry_count
    assert len(parts) == expected_count == (m * n * p) // s
    return parts


def check_three_box(m: int, n: int, p: int, s: int) -> tuple[int, int, int, int]:
    parts = all_large_three_box_partition(m, n, p, s)
    expected = set(itertools.product(range(m), range(n), range(p)))
    seen: set[Cell] = set()
    quotient, remainder = divmod(m * n * p, s)
    large = 0
    for part in parts:
        assert len(part) in (s, s + 1)
        large += len(part) == s + 1
        assert is_line_part(part)
        assert len(set(part)) == len(part)
        assert seen.isdisjoint(part)
        seen.update(part)
    assert seen == expected
    assert len(parts) == quotient
    assert large == remainder
    carries = ((p % s) * ((m * n) % s)) // s
    return len(parts), len(seen), large, carries


def audit_three_boxes(max_s: int, margin: int) -> tuple[int, int, int, int, int]:
    instances = 0
    parts = 0
    cells = 0
    positive_carries = 0
    total_carries = 0
    for s in range(2, max_s + 1):
        for m in range(s, margin * s + 1):
            for n in range(s, margin * s + 1):
                for p in range(s, margin * s + 1):
                    count, volume, _, carries = check_three_box(m, n, p, s)
                    instances += 1
                    parts += count
                    cells += volume
                    positive_carries += carries > 0
                    total_carries += carries
    return instances, parts, cells, positive_carries, total_carries


def audit_maximum_carry(max_s: int) -> tuple[int, int, int]:
    instances = 0
    exchanges = 0
    parts_checked = 0
    for s in range(2, max_s + 1):
        m, n, p = s + 1, 2 * s - 1, 2 * s - 1
        count, _, _, carries = check_three_box(m, n, p, s)
        assert carries == max(0, s - 2)
        instances += 1
        exchanges += carries
        parts_checked += count
    return instances, exchanges, parts_checked


def previous_exact(sides: Sequence[int], s: int) -> bool:
    residues = [side % s for side in sides]
    product = math.prod(residues)
    if product < s:
        return True
    if s <= product < 2 * s and sum(residues) >= s + 2:
        return True
    if s == 3 and residues == [2, 2, 2]:
        return True
    for first, second in itertools.combinations(range(3), 2):
        remaining = 3 - first - second
        if sides[first] < s or sides[second] < s:
            continue
        pair_remainder = (sides[first] * sides[second]) % s
        if (sides[remaining] % s) * pair_remainder < s:
            return True
    return False


def audit_hamming_parameters(max_side: int) -> tuple[int, int, int]:
    near_triangle = 0
    all_large = 0
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
                    if s < 2 or min(sides) < s:
                        continue
                    all_large += 1
                    if not previous_exact(sides, s):
                        genuinely_new += 1
    return near_triangle, all_large, genuinely_new


def audit_lifted_hamming(max_side: int) -> tuple[int, int, int]:
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
                    if s < 2 or min(sides) < s:
                        continue
                    parts = all_large_three_box_partition(*sides, s)
                    for part in parts:
                        assert deficits[0] + len(part) - 1 >= h
                    assert len(parts) == math.prod(sides) // s
                    instances += 1
                    parts_checked += len(parts)
                    cells_checked += math.prod(sides)
    return instances, parts_checked, cells_checked


def audit_first_carry_family(max_k: int, reconstruct_max_k: int) -> tuple[int, int, int]:
    symbolic = 0
    reconstructed = 0
    reconstructed_parts = 0
    for k in range(3, max_k + 1):
        s = k * k - k
        orders = [k * k + 2 * k, k * k, k * k, k * k]
        deficits = [order - 1 for order in orders]
        h = (sum(deficits) + 1) // 2
        assert h == 2 * k * k + k - 2
        assert h - deficits[0] + 1 == s
        sides = orders[1:]
        assert [side % s for side in sides] == [k, k, k]
        assert (sides[0] * sides[1]) % s == k
        assert s <= k * k < 2 * s
        assert math.prod(side % s for side in sides) >= 2 * s
        assert not previous_exact(sides, s)
        exact = math.prod(sides) // s
        assert exact == k**4 + k**3 + k**2 + k + 1
        symbolic += 1

        if k <= reconstruct_max_k:
            parts = all_large_three_box_partition(*sides, s)
            assert len(parts) == exact
            assert all(len(part) >= s and is_line_part(part) for part in parts)
            reconstructed += 1
            reconstructed_parts += len(parts)
    return symbolic, reconstructed, reconstructed_parts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rectangle-max-s", type=int, default=14)
    parser.add_argument("--rectangle-margin", type=int, default=3)
    parser.add_argument("--three-box-max-s", type=int, default=7)
    parser.add_argument("--three-box-margin", type=int, default=2)
    parser.add_argument("--maximum-carry-max-s", type=int, default=60)
    parser.add_argument("--parameter-max-side", type=int, default=60)
    parser.add_argument("--lift-max-side", type=int, default=13)
    parser.add_argument("--family-max-k", type=int, default=10000)
    parser.add_argument("--family-reconstruct-max-k", type=int, default=5)
    args = parser.parse_args()

    rectangles = audit_rectangles(args.rectangle_max_s, args.rectangle_margin)
    boxes = audit_three_boxes(args.three_box_max_s, args.three_box_margin)
    maximum_carry = audit_maximum_carry(args.maximum_carry_max_s)
    parameters = audit_hamming_parameters(args.parameter_max_side)
    lifted = audit_lifted_hamming(args.lift_max_side)
    family = audit_first_carry_family(
        args.family_max_k, args.family_reconstruct_max_k
    )

    print(f"anchored rectangle instances reconstructed: {rectangles[0]}")
    print(f"anchored rectangle line parts checked: {rectangles[1]}")
    print(f"anchored rectangle cells checked: {rectangles[2]}")
    print(f"anchored size-(s+1) parts checked: {rectangles[3]}")
    print(f"all-large three-box partitions reconstructed: {boxes[0]}")
    print(f"all-large three-box line parts checked: {boxes[1]}")
    print(f"all-large three-box cells checked: {boxes[2]}")
    print(f"positive-carry three-boxes reconstructed: {boxes[3]}")
    print(f"cross-slab exchanges checked: {boxes[4]}")
    print(f"maximum-carry stress instances reconstructed: {maximum_carry[0]}")
    print(f"maximum-carry stress exchanges checked: {maximum_carry[1]}")
    print(f"maximum-carry stress line parts checked: {maximum_carry[2]}")
    print(f"four-dimensional near-triangle parameters checked: {parameters[0]}")
    print(f"all-large-minor parameters detected: {parameters[1]}")
    print(f"new parameters beyond preceding criteria: {parameters[2]}")
    print(f"lifted Hamming partitions reconstructed: {lifted[0]}")
    print(f"lifted Hamming colour classes checked: {lifted[1]}")
    print(f"lifted Hamming minor cells checked: {lifted[2]}")
    print(f"first-carry family indices checked: {family[0]}")
    print(f"first-carry family partitions reconstructed: {family[1]}")
    print(f"first-carry family line parts checked: {family[2]}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
