#!/usr/bin/env python3
"""Exact audits for balanced stars and the thin-coordinate obstruction.

CPython 3.12+, standard library only. Universal claims are proved in
BALANCED_STARS_THIN_OBSTRUCTION.md; this checker reconstructs bounded
partitions and checks the stated exact identities.
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


def hamming_adjacent(left: Cell, right: Cell) -> bool:
    return sum(a != b for a, b in zip(left, right, strict=True)) == 1


def minimum_degree(part: Sequence[Cell]) -> int:
    return min(
        sum(hamming_adjacent(cell, other) for other in part)
        for cell in part
    )


def balanced_rectangle_partition(m: int, n: int, s: int) -> list[Part]:
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
    column_cut = (v - 1) * s
    for row in remaining_rows:
        for block in range(v - 1):
            parts.append(
                tuple(
                    (row, column)
                    for column in range(block * s, (block + 1) * s)
                )
            )

    corner_height = s + a
    corner_width = s + b
    q0, t = divmod(a * b, s)
    selected_columns = b + q0
    rho = max(0, t - selected_columns)
    row_mark_counts = [b - 1] * rho + [b] * (corner_height - rho)
    marked_by_column: list[list[Cell]] = [
        [] for _ in range(selected_columns)
    ]

    cursor = 0
    for row, mark_count in zip(remaining_rows, row_mark_counts, strict=True):
        marked = {
            (cursor + offset) % selected_columns
            for offset in range(mark_count)
        }
        cursor += mark_count
        assert len(marked) == mark_count
        parts.append(
            tuple(
                (row, column_cut + local_column)
                for local_column in range(corner_width)
                if local_column not in marked
            )
        )
        for local_column in marked:
            marked_by_column[local_column].append(
                (row, column_cut + local_column)
            )

    parts.extend(tuple(marked) for marked in marked_by_column)
    return parts


def check_balanced_rectangle(m: int, n: int, s: int) -> tuple[int, int, int]:
    parts = balanced_rectangle_partition(m, n, s)
    expected = set(itertools.product(range(m), range(n)))
    seen: set[Cell] = set()
    for part in parts:
        assert len(part) in (s, s + 1)
        assert len(set(part)) == len(part)
        assert is_line_part(part)
        assert seen.isdisjoint(part)
        seen.update(part)
    quotient, remainder = divmod(m * n, s)
    assert seen == expected
    assert len(parts) == quotient
    assert sum(len(part) == s + 1 for part in parts) == remainder
    return len(parts), len(seen), remainder


def audit_rectangles(max_s: int, quotient_margin: int) -> tuple[int, int, int, int]:
    instances = 0
    parts = 0
    cells = 0
    large_parts = 0
    for s in range(2, max_s + 1):
        for m in range(s, quotient_margin * s + 1):
            for n in range(s, quotient_margin * s + 1):
                count, volume, large = check_balanced_rectangle(m, n, s)
                instances += 1
                parts += count
                cells += volume
                large_parts += large
    return instances, parts, cells, large_parts


def thin_partition(m: int, n: int, p: int, s: int) -> list[Part]:
    if not 1 <= p < s:
        raise ValueError("require 1<=p<s")
    rectangle = balanced_rectangle_partition(m, n, s)
    return [
        tuple((row, column, layer) for row, column in part)
        for layer in range(p)
        for part in rectangle
    ]


def check_thin_partition(m: int, n: int, p: int, s: int) -> tuple[int, int]:
    parts = thin_partition(m, n, p, s)
    seen: set[Cell] = set()
    for part in parts:
        assert len(part) in (s, s + 1)
        assert is_line_part(part)
        assert len({cell[2] for cell in part}) == 1
        assert seen.isdisjoint(part)
        seen.update(part)
    assert seen == set(itertools.product(range(m), range(n), range(p)))
    line_optimum = p * ((m * n) // s)
    quotient = (m * n * p) // s
    deficit = (p * ((m * n) % s)) // s
    assert len(parts) == line_optimum
    assert quotient - line_optimum == deficit
    return len(parts), deficit


def audit_thin_reconstructions(
    max_s: int, quotient_margin: int
) -> tuple[int, int, int]:
    instances = 0
    parts = 0
    positive_deficits = 0
    for s in range(2, max_s + 1):
        for m in range(s, quotient_margin * s + 1):
            for n in range(s, quotient_margin * s + 1):
                for p in range(1, s):
                    count, deficit = check_thin_partition(m, n, p, s)
                    instances += 1
                    parts += count
                    positive_deficits += deficit > 0
    return instances, parts, positive_deficits


def audit_thin_formulas(max_s: int, residue_cycles: int) -> tuple[int, int, int]:
    identities = 0
    carry_obstructions = 0
    total_deficit = 0
    for s in range(2, max_s + 1):
        for tau in range(s):
            # Several complete quotient cycles confirm independence from them.
            mn = s * residue_cycles + tau
            for p in range(1, s):
                layer_count = p * (mn // s)
                quotient = (p * mn) // s
                deficit = (p * tau) // s
                assert quotient - layer_count == deficit
                identities += 1
                carry_obstructions += deficit > 0
                total_deficit += deficit
    return identities, carry_obstructions, total_deficit


def strip_exact_blocks(sides: Sequence[int], s: int) -> tuple[list[Part], Part]:
    active = [list(range(side)) for side in sides]
    lines: list[Part] = []
    for axis, side in enumerate(sides):
        quotient, remainder = divmod(side, s)
        other_axes = [index for index in range(len(sides)) if index != axis]
        for fixed in itertools.product(*(active[index] for index in other_axes)):
            base = dict(zip(other_axes, fixed, strict=True))
            for block in range(quotient):
                lines.append(
                    tuple(
                        tuple(
                            value if index == axis else base[index]
                            for index in range(len(sides))
                        )
                        for value in range(block * s, (block + 1) * s)
                    )
                )
        active[axis] = list(range(side - remainder, side))
    return lines, tuple(itertools.product(*active))


def check_hamming_family_partition(s: int) -> tuple[int, int, int]:
    sides = (s + 2, s + 1, s - 1)
    lines, residue = strip_exact_blocks(sides, s)
    parts = [*lines, residue]
    expected = set(itertools.product(*(range(side) for side in sides)))
    seen: set[Cell] = set()
    for part in parts:
        assert minimum_degree(part) >= s - 1
        assert seen.isdisjoint(part)
        seen.update(part)
    assert seen == expected
    exact = s * s + 2 * s - 2
    line_bound = (s - 1) * (s + 3)
    assert len(parts) == exact
    assert line_bound == exact - 1
    return len(parts), len(lines), len(residue)


def audit_hamming_family(max_s: int, reconstruct_max_s: int) -> tuple[int, int, int, int]:
    symbolic = 0
    reconstructed = 0
    reconstructed_parts = 0
    residue_cells = 0
    for s in range(3, max_s + 1):
        orders = (s + 2, s + 2, s + 1, s - 1)
        deficits = tuple(order - 1 for order in orders)
        h = (sum(deficits) + 1) // 2
        assert sum(deficits) == 4 * s
        assert h == 2 * s
        assert h - deficits[0] + 1 == s
        sides = orders[1:]
        assert tuple(side % s for side in sides) == (2, 1, s - 1)
        assert s <= math.prod(side % s for side in sides) < 2 * s
        assert sum(side % s for side in sides) == s + 2
        exact = math.prod(sides) // s
        assert exact == s * s + 2 * s - 2
        assert (s - 1) * ((s + 2) * (s + 1) // s) == exact - 1
        symbolic += 1

        if s <= reconstruct_max_s:
            count, _, residue = check_hamming_family_partition(s)
            assert count == exact
            reconstructed += 1
            reconstructed_parts += count
            residue_cells += residue
    return symbolic, reconstructed, reconstructed_parts, residue_cells


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rectangle-max-s", type=int, default=18)
    parser.add_argument("--rectangle-quotient-margin", type=int, default=3)
    parser.add_argument("--thin-reconstruct-max-s", type=int, default=10)
    parser.add_argument("--thin-reconstruct-margin", type=int, default=2)
    parser.add_argument("--thin-formula-max-s", type=int, default=300)
    parser.add_argument("--thin-formula-residue-cycles", type=int, default=7)
    parser.add_argument("--family-max-s", type=int, default=10000)
    parser.add_argument("--family-reconstruct-max-s", type=int, default=14)
    args = parser.parse_args()

    rectangles = audit_rectangles(
        args.rectangle_max_s, args.rectangle_quotient_margin
    )
    reconstructed = audit_thin_reconstructions(
        args.thin_reconstruct_max_s, args.thin_reconstruct_margin
    )
    formulas = audit_thin_formulas(
        args.thin_formula_max_s, args.thin_formula_residue_cycles
    )
    family = audit_hamming_family(
        args.family_max_s, args.family_reconstruct_max_s
    )

    print(f"balanced rectangle partitions reconstructed: {rectangles[0]}")
    print(f"balanced rectangle line parts checked: {rectangles[1]}")
    print(f"balanced rectangle cells checked: {rectangles[2]}")
    print(f"balanced rectangle size-(s+1) parts checked: {rectangles[3]}")
    print(f"thin-box partitions reconstructed: {reconstructed[0]}")
    print(f"thin-box line parts checked: {reconstructed[1]}")
    print(f"thin-box positive-deficit instances reconstructed: {reconstructed[2]}")
    print(f"thin-coordinate identities checked: {formulas[0]}")
    print(f"thin-coordinate carry obstructions checked: {formulas[1]}")
    print(f"thin-coordinate accumulated deficit: {formulas[2]}")
    print(f"Hamming separation-family indices checked: {family[0]}")
    print(f"Hamming family partitions reconstructed: {family[1]}")
    print(f"Hamming family colour classes checked: {family[2]}")
    print(f"Hamming family nonlinear residue cells checked: {family[3]}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
