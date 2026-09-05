#!/usr/bin/env python3
"""Exact checker for the thin (2,2,2) cross-boundary construction.

CPython 3.12+, standard library only.  Coordinates are zero based.  The
universal result is proved in CROSS_BOUNDARY_222.md; this program reconstructs
bounded instances and audits every defining property directly.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections.abc import Sequence


Cell = tuple[int, int, int]
Part = tuple[Cell, ...]


def base_core() -> list[Part]:
    """Return the explicit 19-part partition of [7] x [7] x [2]."""
    parts: list[Part] = [
        tuple((x, 0, z) for x in range(4) for z in range(2))
    ]
    for z in range(2):
        for x in range(7):
            exceptional_row = 1 if x < 2 else 2 if x < 4 else 0
            rows = (3, 4, 5, 6, exceptional_row)
            parts.append(tuple((x, y, z) for y in rows))
        parts.append(tuple((x, 1, z) for x in (2, 3, 4, 5, 6)))
        parts.append(tuple((x, 2, z) for x in (0, 1, 4, 5, 6)))
    return parts


def translate(part: Sequence[Cell], dx: int, dy: int) -> Part:
    return tuple((x + dx, y + dy, z) for x, y, z in part)


def construct(a: int, b: int) -> tuple[tuple[int, int, int], list[Part]]:
    """Construct the partition of (5a+2) x (5b+2) x 2."""
    if a < 1 or b < 1:
        raise ValueError("a and b must be positive")
    m, n, p = 5 * a + 2, 5 * b + 2, 2
    x_offset, y_offset = 5 * (a - 1), 5 * (b - 1)
    parts: list[Part] = []

    for block in range(a - 1):
        for y in range(n):
            for z in range(p):
                parts.append(
                    tuple((x, y, z) for x in range(5 * block, 5 * block + 5))
                )

    for x in range(x_offset, m):
        for block in range(b - 1):
            for z in range(p):
                parts.append(
                    tuple((x, y, z) for y in range(5 * block, 5 * block + 5))
                )

    parts.extend(translate(part, x_offset, y_offset) for part in base_core())
    return (m, n, p), parts


def hamming_degree(part: Sequence[Cell], vertex: Cell) -> int:
    return sum(
        sum(left != right for left, right in zip(vertex, other, strict=True)) == 1
        for other in part
    )


def is_line(part: Sequence[Cell]) -> bool:
    return sum(len({cell[axis] for cell in part}) > 1 for axis in range(3)) == 1


def expected_count(a: int, b: int) -> int:
    return 10 * a * b + 4 * a + 4 * b + 1


def validate(a: int, b: int, sides: Sequence[int], parts: Sequence[Part]) -> dict[str, int]:
    m, n, p = sides
    assert (m, n, p) == (5 * a + 2, 5 * b + 2, 2)
    expected_cells = set(itertools.product(range(m), range(n), range(p)))
    owners: dict[Cell, int] = {}
    line_parts = 0
    nonlinear_parts = 0
    nonlinear_vertices = 0

    for part_index, part in enumerate(parts):
        assert len(set(part)) == len(part)
        assert len(part) >= 5
        assert min(hamming_degree(part, vertex) for vertex in part) >= 4
        if is_line(part):
            assert len(part) == 5
            line_parts += 1
        else:
            assert len(part) == 8
            nonlinear_parts += 1
            nonlinear_vertices += len(part)
        for cell in part:
            assert cell not in owners
            owners[cell] = part_index

    assert set(owners) == expected_cells
    assert len(parts) == expected_count(a, b)
    assert len(parts) == m * n * p // 5
    assert line_parts == len(parts) - 1
    assert nonlinear_parts == 1
    assert nonlinear_vertices == 8
    line_ceiling = 2 * (m * n // 5)
    assert line_ceiling == len(parts) - 1
    return {
        "parts": len(parts),
        "line_parts": line_parts,
        "nonlinear_parts": nonlinear_parts,
        "cells": len(expected_cells),
    }


def certificate_digest(parts: Sequence[Part]) -> str:
    canonical = sorted(sorted(part) for part in parts)
    payload = json.dumps(canonical, separators=(",", ":"), sort_keys=False).encode()
    return hashlib.sha256(payload).hexdigest()


def audit_cell_instances(max_parameter: int) -> dict[str, int]:
    totals = {"instances": 0, "parts": 0, "line_parts": 0, "cells": 0}
    for a in range(1, max_parameter + 1):
        for b in range(1, max_parameter + 1):
            sides, parts = construct(a, b)
            stats = validate(a, b, sides, parts)
            totals["instances"] += 1
            totals["parts"] += stats["parts"]
            totals["line_parts"] += stats["line_parts"]
            totals["cells"] += stats["cells"]
    return totals


def audit_formulas(max_parameter: int) -> tuple[int, int]:
    boxes = 0
    hamming_graphs = 0
    for a in range(1, max_parameter + 1):
        for b in range(1, max_parameter + 1):
            m, n = 5 * a + 2, 5 * b + 2
            quotient = 2 * m * n // 5
            line_ceiling = 2 * (m * n // 5)
            assert quotient == expected_count(a, b)
            assert line_ceiling == quotient - 1
            boxes += 1

    for a in range(2, max_parameter + 1):
        for b in range(2, a + 1):
            n1, n2, n3, n4 = 5 * (a + b) - 4, 5 * a + 2, 5 * b + 2, 2
            assert n1 >= n2 >= n3 >= n4
            deficits = (n1 - 1, n2 - 1, n3 - 1, n4 - 1)
            assert sum(deficits) % 2 == 0
            h = sum(deficits) // 2
            assert h == 5 * a + 5 * b - 1
            assert h - deficits[0] + 1 == 5
            assert deficits[0] + 4 == h
            assert n2 * n3 * n4 // 5 == expected_count(a, b)
            hamming_graphs += 1
    return boxes, hamming_graphs


def audit_mutations() -> int:
    sides, parts = construct(1, 1)
    rejected = 0

    missing = list(parts)
    missing[0] = missing[0][:-1]
    try:
        validate(1, 1, sides, missing)
    except AssertionError:
        rejected += 1

    duplicate = list(parts)
    duplicate[1] = duplicate[1][:-1] + (duplicate[2][0],)
    try:
        validate(1, 1, sides, duplicate)
    except AssertionError:
        rejected += 1

    low_degree = list(parts)
    low_degree[0] = tuple((x, 0, 0) for x in range(7)) + ((0, 1, 1),)
    try:
        validate(1, 1, sides, low_degree)
    except AssertionError:
        rejected += 1

    assert rejected == 3
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cell-max", type=int, default=8)
    parser.add_argument("--formula-max", type=int, default=500)
    args = parser.parse_args()
    if args.cell_max < 1 or args.formula_max < 2:
        parser.error("need cell-max>=1 and formula-max>=2")

    base_sides, base_parts = construct(1, 1)
    base_stats = validate(1, 1, base_sides, base_parts)
    digest = certificate_digest(base_parts)
    cell_totals = audit_cell_instances(args.cell_max)
    formula_boxes, hamming_graphs = audit_formulas(args.formula_max)
    mutations = audit_mutations()

    print(f"base parts: {base_stats['parts']}")
    print(f"base line/nonlinear parts: {base_stats['line_parts']}/{base_stats['nonlinear_parts']}")
    print(f"base certificate SHA-256: {digest}")
    print(f"cell-level box instances through a,b={args.cell_max}: {cell_totals['instances']}")
    print(f"cell-level parts checked: {cell_totals['parts']}")
    print(f"cell-level line parts checked: {cell_totals['line_parts']}")
    print(f"cell-level cells checked: {cell_totals['cells']}")
    print(f"formula box instances through a,b={args.formula_max}: {formula_boxes}")
    print(f"ordered Hamming family instances: {hamming_graphs}")
    print(f"mutated certificates rejected: {mutations}")
    print("K_16 square K_12 square K_12 square K_2: exact 57; line ceiling 56")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
