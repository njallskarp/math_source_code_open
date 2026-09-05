#!/usr/bin/env python3
"""Exact checker for the first-carry equality-boundary classification.

CPython 3.12+, standard library only.  Coordinates are zero based.  The
universal iff theorem is proved in FIRST_CARRY_EQUALITY_CLASSIFICATION.md;
this program checks its arithmetic/orientation reduction and directly
constructs bounded members of both infinite families.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections.abc import Iterable, Sequence


Cell = tuple[int, int, int]
Part = tuple[Cell, ...]


def hamming_degree(part: Sequence[Cell], vertex: Cell) -> int:
    return sum(
        sum(a != b for a, b in zip(vertex, other, strict=True)) == 1
        for other in part
    )


def line_axis(part: Sequence[Cell]) -> int | None:
    """Return the varying coordinate of a coordinate-line set, if any."""
    varying = [axis for axis in range(3) if len({v[axis] for v in part}) > 1]
    return varying[0] if len(varying) == 1 else None


def is_prism(part: Sequence[Cell], s: int) -> bool:
    """Recognize a coordinate copy of K_(s-1) square K_2."""
    if len(part) != 2 * s - 2 or len(set(part)) != len(part):
        return False
    values = [sorted({v[axis] for v in part}) for axis in range(3)]
    sizes = sorted(len(axis_values) for axis_values in values)
    if sizes != sorted((1, 2, s - 1)):
        return False
    return set(part) == set(itertools.product(*values))


def _line_x(xs: Iterable[int], y: int, z: int) -> Part:
    return tuple((x, y, z) for x in xs)


def _line_y(x: int, ys: Iterable[int], z: int) -> Part:
    return tuple((x, y, z) for y in ys)


def construct_short_thin_factor(s: int, m: int, n: int) -> list[Part]:
    """Construct the p=2, (m mod s)(n mod s)=s-1 family."""
    r, u = m % s, n % s
    if s < 3 or m < s or n < s or r * u != s - 1:
        raise ValueError("need s>=3, m,n>=s, and residue product s-1")

    p = 2
    x0 = m - (s + r)
    y0 = n - (s + u)
    assert x0 >= 0 and y0 >= 0 and x0 % s == y0 % s == 0
    parts: list[Part] = []

    # Strip all but a terminal (s+r)-by-(s+u) core.
    for xb in range(0, x0, s):
        for y in range(n):
            for z in range(p):
                parts.append(_line_x(range(xb, xb + s), y, z))
    for x in range(x0, m):
        for yb in range(0, y0, s):
            for z in range(p):
                parts.append(_line_y(x, range(yb, yb + s), z))

    ordinary_rows = tuple(range(y0, y0 + s))
    omitted_row = ordinary_rows[0]
    selected_rows = tuple(range(y0 + s, n))
    omitted_columns = tuple(range(x0, x0 + s - 1))
    omitted_set = set(omitted_columns)
    assert len(selected_rows) == u and len(omitted_columns) == r * u

    # In each layer, column lines cover the ordinary rows, with r columns
    # diverted to each selected row.  One horizontal line closes each such
    # selected row.
    for z in range(p):
        for x in range(x0, m):
            if x in omitted_set:
                group = (x - x0) // r
                ys = tuple(y for y in ordinary_rows if y != omitted_row) + (
                    selected_rows[group],
                )
            else:
                ys = ordinary_rows
            parts.append(_line_y(x, ys, z))

        for group, y in enumerate(selected_rows):
            diverted = set(range(x0 + group * r, x0 + (group + 1) * r))
            xs = tuple(x for x in range(x0, m) if x not in diverted)
            assert len(xs) == s
            parts.append(_line_x(xs, y, z))

    parts.append(
        tuple((x, omitted_row, z) for x in omitted_columns for z in range(p))
    )
    return parts


def construct_long_thin_factor(s: int, m: int, n: int) -> list[Part]:
    """Construct the p=s-1, (m mod s)(n mod s)=2 family."""
    r, u = m % s, n % s
    if s < 3 or m < s or n < s or r * u != 2:
        raise ValueError("need s>=3, m,n>=s, and residue product 2")

    p = s - 1
    parts: list[Part] = []
    for xb in range(0, m - r, s):
        for y in range(n):
            for z in range(p):
                parts.append(_line_x(range(xb, xb + s), y, z))
    for x in range(m - r, m):
        for yb in range(0, n - u, s):
            for z in range(p):
                parts.append(_line_y(x, range(yb, yb + s), z))

    parts.append(
        tuple(
            (x, y, z)
            for x in range(m - r, m)
            for y in range(n - u, n)
            for z in range(p)
        )
    )
    return parts


def validate_partition(
    s: int, sides: tuple[int, int, int], parts: Sequence[Part]
) -> dict[str, int]:
    """Check every defining property of a constructed partition."""
    m, n, p = sides
    expected = set(itertools.product(range(m), range(n), range(p)))
    owners: dict[Cell, int] = {}
    line_parts = 0
    nonlinear_parts = 0
    checked_degrees = 0

    for index, part in enumerate(parts):
        if len(set(part)) != len(part):
            raise AssertionError("a part repeats a vertex")
        if not all(0 <= x < m and 0 <= y < n and 0 <= z < p for x, y, z in part):
            raise AssertionError("a vertex lies outside the box")

        axis = line_axis(part)
        if axis is not None:
            if len(part) != s:
                raise AssertionError("a line part has the wrong size")
            line_parts += 1
        elif is_prism(part, s):
            nonlinear_parts += 1
        else:
            raise AssertionError("a nonlinear part is not the forced prism")

        for vertex in part:
            if hamming_degree(part, vertex) < s - 1:
                raise AssertionError("minimum-degree condition failed")
            checked_degrees += 1
            if vertex in owners:
                raise AssertionError("two parts overlap")
            owners[vertex] = index

    if set(owners) != expected:
        raise AssertionError("partition does not cover the box")
    if nonlinear_parts != 1 or line_parts != len(parts) - 1:
        raise AssertionError("wrong line/nonlinear part counts")

    quotient = m * n * p // s
    line_ceiling = p * (m * n // s)
    if len(parts) != quotient or line_ceiling != quotient - 1:
        raise AssertionError("quotient or line-deficit formula failed")
    return {
        "cells": len(expected),
        "parts": len(parts),
        "line_parts": line_parts,
        "nonlinear_parts": nonlinear_parts,
        "degrees": checked_degrees,
    }


def admissible_orientations(s: int, r: int, u: int, p: int) -> tuple[tuple[int, int], ...]:
    """Return prism axis roles compatible with layer divisibility.

    Each pair is (axis carrying s-1 symbols, axis carrying 2 symbols), with
    axes 0,1,2 corresponding to m,n,p.  This checks only the necessary layer
    divisibility after the unique prism is removed.
    """
    sides = (s + r, s + u, p)
    layer_size = sides[0] * sides[1]
    good: list[tuple[int, int]] = []
    for long_axis in range(3):
        for short_axis in range(3):
            if long_axis == short_axis:
                continue
            if sides[long_axis] < s - 1 or sides[short_axis] < 2:
                continue
            if long_axis == 2:
                removed = [2] * (s - 1) + [0] * (p - (s - 1))
            elif short_axis == 2:
                removed = [s - 1] * 2 + [0] * (p - 2)
            else:
                removed = [2 * s - 2] + [0] * (p - 1)
            if all((layer_size - count) % s == 0 for count in removed):
                good.append((long_axis, short_axis))
    return tuple(good)


def predicted(s: int, r: int, u: int, p: int) -> bool:
    return (p == 2 and r * u == s - 1) or (p == s - 1 and r * u == 2)


def boundary_patterns(max_s: int) -> list[tuple[int, int, int, int]]:
    patterns: list[tuple[int, int, int, int]] = []
    for s in range(3, max_s + 1):
        target = 2 * s - 2
        for r in range(1, s):
            for u in range(1, (s - 1) // r + 1):
                product = r * u
                if target % product:
                    continue
                p = target // product
                if 2 <= p < s:
                    patterns.append((s, r, u, p))
    return patterns


def audit_orientations(max_s: int) -> dict[str, int | str]:
    patterns = boundary_patterns(max_s)
    constructive = 0
    excluded = 0
    orientations = 0
    digest = hashlib.sha256()
    for pattern in patterns:
        s, r, u, p = pattern
        good = admissible_orientations(s, r, u, p)
        if bool(good) != predicted(s, r, u, p):
            raise AssertionError(f"orientation classification failed at {pattern}")
        if good:
            constructive += 1
        else:
            excluded += 1
        orientations += len(good)
        digest.update(
            json.dumps((pattern, good), separators=(",", ":")).encode("ascii") + b"\n"
        )
    return {
        "patterns": len(patterns),
        "constructive": constructive,
        "excluded": excluded,
        "orientations": orientations,
        "digest": digest.hexdigest(),
    }


def partition_digest(parts: Sequence[Part]) -> str:
    canonical = sorted(sorted(part) for part in parts)
    payload = json.dumps(canonical, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def audit_constructions(max_s: int, max_multiplier: int) -> dict[str, int | str]:
    totals = {
        "instances": 0,
        "short": 0,
        "long": 0,
        "cells": 0,
        "parts": 0,
        "degrees": 0,
    }
    digest = hashlib.sha256()
    for s in range(3, max_s + 1):
        for r in range(1, s):
            if (s - 1) % r:
                continue
            u = (s - 1) // r
            if u >= s:
                continue
            for a in range(1, max_multiplier + 1):
                for b in range(1, max_multiplier + 1):
                    m, n = a * s + r, b * s + u
                    parts = construct_short_thin_factor(s, m, n)
                    stats = validate_partition(s, (m, n, 2), parts)
                    totals["instances"] += 1
                    totals["short"] += 1
                    totals["cells"] += stats["cells"]
                    totals["parts"] += stats["parts"]
                    totals["degrees"] += stats["degrees"]
                    digest.update(
                        f"S:{s}:{m}:{n}:{partition_digest(parts)}\n".encode("ascii")
                    )

        for r, u in ((1, 2), (2, 1)):
            if r >= s or u >= s:
                continue
            for a in range(1, max_multiplier + 1):
                for b in range(1, max_multiplier + 1):
                    m, n = a * s + r, b * s + u
                    parts = construct_long_thin_factor(s, m, n)
                    stats = validate_partition(s, (m, n, s - 1), parts)
                    totals["instances"] += 1
                    totals["long"] += 1
                    totals["cells"] += stats["cells"]
                    totals["parts"] += stats["parts"]
                    totals["degrees"] += stats["degrees"]
                    digest.update(
                        f"L:{s}:{m}:{n}:{partition_digest(parts)}\n".encode("ascii")
                    )
    totals["digest"] = digest.hexdigest()
    return totals


def audit_mutations() -> int:
    s, m, n = 7, 9, 10
    parts = construct_short_thin_factor(s, m, n)
    rejected = 0

    missing = list(parts)
    missing[0] = missing[0][:-1]
    try:
        validate_partition(s, (m, n, 2), missing)
    except AssertionError:
        rejected += 1

    overlap = list(parts)
    overlap[1] = overlap[1][:-1] + (overlap[0][0],)
    try:
        validate_partition(s, (m, n, 2), overlap)
    except AssertionError:
        rejected += 1

    malformed = list(parts)
    prism = list(malformed[-1])
    prism[-1] = (prism[-1][0], prism[-1][1] + 1, prism[-1][2])
    malformed[-1] = tuple(prism)
    try:
        validate_partition(s, (m, n, 2), malformed)
    except AssertionError:
        rejected += 1

    try:
        construct_short_thin_factor(7, 9, 9)
    except ValueError:
        rejected += 1

    try:
        construct_long_thin_factor(7, 9, 10)
    except ValueError:
        rejected += 1

    if rejected != 5:
        raise AssertionError("mutation rejection audit failed")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orientation-max-s", type=int, default=1000)
    parser.add_argument("--construction-max-s", type=int, default=18)
    parser.add_argument("--multiplier-max", type=int, default=2)
    args = parser.parse_args()
    if args.orientation_max_s < 3 or args.construction_max_s < 3:
        parser.error("both s bounds must be at least 3")
    if args.multiplier_max < 1:
        parser.error("multiplier-max must be positive")

    orientation = audit_orientations(args.orientation_max_s)
    construction = audit_constructions(args.construction_max_s, args.multiplier_max)
    mutations = audit_mutations()

    print(f"equality-boundary patterns through s={args.orientation_max_s}: {orientation['patterns']}")
    print(f"constructive/excluded patterns: {orientation['constructive']}/{orientation['excluded']}")
    print(f"layer-divisible ordered prism orientations: {orientation['orientations']}")
    print(f"orientation certificate SHA-256: {orientation['digest']}")
    print(f"constructed instances through s={args.construction_max_s}: {construction['instances']}")
    print(f"short/long thin-factor instances: {construction['short']}/{construction['long']}")
    print(f"constructed cells checked: {construction['cells']}")
    print(f"constructed parts checked: {construction['parts']}")
    print(f"induced degrees checked: {construction['degrees']}")
    print(f"construction certificate SHA-256: {construction['digest']}")
    print(f"mutated/invalid inputs rejected: {mutations}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
