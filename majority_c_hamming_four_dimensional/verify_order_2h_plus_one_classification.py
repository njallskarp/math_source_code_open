#!/usr/bin/env python3
"""Exact audit for the order-(2h+1) Hamming-core classification.

CPython 3.12+, standard library only.  The universal proof is in
ORDER_2H_PLUS_ONE_CLASSIFICATION.md.  This checker works directly with cells
of two-dimensional Hamming graphs, equivalently edges of bipartite graphs.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections.abc import Iterable, Sequence


Cell = tuple[int, int]
Job = tuple[int, int, int]


DEFAULT_JOBS: tuple[Job, ...] = (
    (3, 3, 2),
    (3, 3, 3),
    (3, 3, 4),
    (4, 3, 2),
    (4, 3, 3),
    (4, 3, 4),
    (4, 4, 2),
    (4, 4, 3),
    (4, 4, 4),
    (4, 4, 5),
    (5, 3, 2),
    (5, 3, 3),
    (5, 3, 4),
    (5, 4, 2),
    (5, 4, 3),
    (5, 4, 4),
    (5, 4, 5),
    (5, 5, 2),
    (5, 5, 3),
    (5, 5, 4),
    (5, 5, 5),
)


def line_degrees(cells: Sequence[Cell], rows: int, columns: int) -> tuple[list[int], list[int]]:
    if not cells:
        raise ValueError("the selected cell set must be nonempty")
    if len(set(cells)) != len(cells):
        raise ValueError("selected cells must be distinct")
    row_degrees = [0] * rows
    column_degrees = [0] * columns
    for row, column in cells:
        if not (0 <= row < rows and 0 <= column < columns):
            raise ValueError("selected cell outside the declared host")
        row_degrees[row] += 1
        column_degrees[column] += 1
    return row_degrees, column_degrees


def minimum_degree(cells: Sequence[Cell], rows: int, columns: int) -> int:
    row_degrees, column_degrees = line_degrees(cells, rows, columns)
    return min(row_degrees[row] + column_degrees[column] - 2 for row, column in cells)


def classify_core(cells: Sequence[Cell], h: int, rows: int, columns: int) -> str:
    if h < 2:
        raise ValueError("h must be at least two")
    if len(cells) != 2 * h + 1:
        return "wrong_order"
    row_degrees, column_degrees = line_degrees(cells, rows, columns)
    if any(row_degrees[row] + column_degrees[column] - 2 < h for row, column in cells):
        return "not_core"

    active_rows = [row for row, degree in enumerate(row_degrees) if degree]
    active_columns = [column for column, degree in enumerate(column_degrees) if degree]
    if len(active_rows) == 1 or len(active_columns) == 1:
        return "line"

    chosen = set(cells)
    for row in active_rows:
        if row_degrees[row] != h + 1:
            continue
        for column in active_columns:
            if column_degrees[column] != h + 1 or (row, column) not in chosen:
                continue
            if all(other_row == row or other_column == column for other_row, other_column in cells):
                return "perpendicular"

    if len(active_rows) == 2 and sorted((row_degrees[row] for row in active_rows)) == [h, h + 1]:
        supports = [
            {column for other_row, column in cells if other_row == row}
            for row in active_rows
        ]
        if supports[0] <= supports[1] or supports[1] <= supports[0]:
            return "parallel"

    if len(active_columns) == 2 and sorted(
        column_degrees[column] for column in active_columns
    ) == [h, h + 1]:
        supports = [
            {row for row, other_column in cells if other_column == column}
            for column in active_columns
        ]
        if supports[0] <= supports[1] or supports[1] <= supports[0]:
            return "parallel"

    if (
        h == 4
        and len(active_rows) == 3
        and len(active_columns) == 3
        and all(row_degrees[row] == 3 for row in active_rows)
        and all(column_degrees[column] == 3 for column in active_columns)
    ):
        return "grid"

    return "unknown"


def feasible_direction_pairs(h: int) -> tuple[tuple[int, int], ...]:
    pairs: list[tuple[int, int]] = []
    for larger in range(1, h):
        for smaller in range(1, larger + 1):
            if larger + smaller < h:
                continue
            doubled_bound = 2 * (1 + larger + smaller)
            doubled_bound += larger * (h - larger) + smaller * (h - smaller)
            if doubled_bound <= 2 * (2 * h + 1):
                pairs.append((larger, smaller))
    return tuple(pairs)


def expected_direction_pairs(h: int) -> set[tuple[int, int]]:
    if h == 2:
        return {(1, 1)}
    if h == 3:
        return {(2, 1), (2, 2)}
    if h == 4:
        return {(3, 1), (2, 2)}
    return {(h - 1, 1)}


def audit_profiles(max_h: int) -> dict[str, int | str]:
    tested = 0
    survivors = 0
    digest = hashlib.sha256()
    for h in range(2, max_h + 1):
        pairs = feasible_direction_pairs(h)
        expected = expected_direction_pairs(h)
        if set(pairs) != expected:
            raise AssertionError(f"unexpected direction pairs for h={h}: {pairs}")
        tested += sum(
            1
            for larger in range(1, h)
            for smaller in range(1, larger + 1)
            if larger + smaller >= h
        )
        survivors += len(pairs)
        digest.update(json.dumps((h, pairs), separators=(",", ":")).encode("ascii") + b"\n")
    return {"tested": tested, "survivors": survivors, "digest": digest.hexdigest()}


def family_instances(h: int) -> dict[str, tuple[Cell, ...]]:
    line = tuple((0, column) for column in range(2 * h + 1))
    parallel = tuple((0, column) for column in range(h + 1)) + tuple(
        (1, column) for column in range(h)
    )
    perpendicular = tuple((0, column) for column in range(h + 1)) + tuple(
        (row, 0) for row in range(1, h + 1)
    )
    result = {"line": line, "parallel": parallel, "perpendicular": perpendicular}
    if h == 4:
        result["grid"] = tuple(itertools.product(range(3), repeat=2))
    return result


def host_size(cells: Sequence[Cell]) -> tuple[int, int]:
    return max(row for row, _ in cells) + 1, max(column for _, column in cells) + 1


def audit_families(max_h: int) -> dict[str, int | str]:
    checked = 0
    digest = hashlib.sha256()
    for h in range(2, max_h + 1):
        for expected, cells in family_instances(h).items():
            rows, columns = host_size(cells)
            actual = classify_core(cells, h, rows, columns)
            if actual != expected:
                raise AssertionError(f"normal form {expected} misclassified as {actual} for h={h}")
            if minimum_degree(cells, rows, columns) < h:
                raise AssertionError(f"normal form {expected} misses its degree target for h={h}")
            checked += 1
            digest.update(json.dumps((h, expected, cells), separators=(",", ":")).encode("ascii") + b"\n")
    return {"checked": checked, "digest": digest.hexdigest()}


def audit_exhaustive(jobs: Iterable[Job] = DEFAULT_JOBS) -> dict[str, int | str]:
    totals: dict[str, int | str] = {
        "jobs": 0,
        "subsets": 0,
        "cores": 0,
        "parallel": 0,
        "perpendicular": 0,
        "grid": 0,
    }
    digest = hashlib.sha256()
    for rows, columns, h in jobs:
        order = 2 * h + 1
        positions = tuple(itertools.product(range(rows), range(columns)))
        if order > len(positions):
            raise ValueError(f"job {(rows, columns, h)} has too few host cells")
        totals["jobs"] += 1
        for indices in itertools.combinations(range(len(positions)), order):
            totals["subsets"] += 1
            row_degrees = [0] * rows
            column_degrees = [0] * columns
            for index in indices:
                row, column = positions[index]
                row_degrees[row] += 1
                column_degrees[column] += 1
            if sum(degree > 0 for degree in row_degrees) < 2:
                continue
            if sum(degree > 0 for degree in column_degrees) < 2:
                continue
            if any(
                row_degrees[positions[index][0]] + column_degrees[positions[index][1]] < h + 2
                for index in indices
            ):
                continue

            cells = tuple(positions[index] for index in indices)
            family = classify_core(cells, h, rows, columns)
            if family not in {"parallel", "perpendicular", "grid"}:
                raise AssertionError(
                    f"unclassified core in host {(rows, columns)}, h={h}: {cells}"
                )
            totals["cores"] += 1
            totals[family] += 1
            digest.update(
                json.dumps((rows, columns, h, family, cells), separators=(",", ":")).encode("ascii")
                + b"\n"
            )
    totals["digest"] = digest.hexdigest()
    return totals


def audit_mutations() -> int:
    rejected = 0

    parallel = list(family_instances(5)["parallel"])
    parallel[-1] = (1, 6)
    if classify_core(tuple(parallel), 5, 2, 7) == "not_core":
        rejected += 1

    perpendicular = list(family_instances(5)["perpendicular"])
    perpendicular[-1] = (5, 1)
    if classify_core(tuple(perpendicular), 5, 6, 6) == "not_core":
        rejected += 1

    grid = list(family_instances(4)["grid"])
    grid[-1] = (3, 3)
    if classify_core(tuple(grid), 4, 4, 4) == "not_core":
        rejected += 1

    try:
        line_degrees((), 1, 1)
    except ValueError:
        rejected += 1

    try:
        line_degrees(((0, 0), (0, 0)), 1, 1)
    except ValueError:
        rejected += 1

    if rejected != 5:
        raise AssertionError(f"mutation/control audit rejected {rejected}, expected five")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-max-h", type=int, default=300)
    parser.add_argument("--family-max-h", type=int, default=100)
    args = parser.parse_args()
    if args.profile_max_h < 5 or args.family_max_h < 5:
        parser.error("both maxima must be at least five")

    exhaustive = audit_exhaustive()
    profiles = audit_profiles(args.profile_max_h)
    families = audit_families(args.family_max_h)
    rejected = audit_mutations()

    print(f"two-flat parameter jobs exhausted: {exhaustive['jobs']}")
    print(f"fixed-order subsets checked: {exhaustive['subsets']}")
    print(f"nonlinear h-cores classified: {exhaustive['cores']}")
    print(f"nested-parallel witnesses: {exhaustive['parallel']}")
    print(f"perpendicular-line witnesses: {exhaustive['perpendicular']}")
    print(f"exceptional 3-by-3 grids: {exhaustive['grid']}")
    print(f"classification-witness SHA-256: {exhaustive['digest']}")
    print(f"direction pairs audited through h={args.profile_max_h}: {profiles['tested']}")
    print(f"direction pairs surviving the shell bound: {profiles['survivors']}")
    print(f"direction-pair SHA-256: {profiles['digest']}")
    print(f"normal-form instances through h={args.family_max_h}: {families['checked']}")
    print(f"normal-form SHA-256: {families['digest']}")
    print(f"mutations/controls rejected: {rejected}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
