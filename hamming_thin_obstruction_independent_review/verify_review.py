#!/usr/bin/env python3
"""Independent exact checks for the thin-coordinate Hamming obstruction.

CPython 3.11+, standard library only.  The original source uses a cyclic
cursor and stores an ordered list of parts.  This checker instead realizes
the required corner degrees with a generic integral max-flow and validates a
cell-to-owner map.  Finite computation corroborates the proof in README.md;
it does not prove its universal quantifiers.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
from collections.abc import Hashable, Iterable, Sequence
from dataclasses import dataclass


Cell = tuple[int, ...]
Label = tuple[Hashable, ...]


@dataclass
class Edge:
    to: int
    reverse: int
    capacity: int


class Dinic:
    """Small deterministic integer max-flow implementation."""

    def __init__(self, vertices: int) -> None:
        self.graph: list[list[Edge]] = [[] for _ in range(vertices)]

    def add_edge(self, source: int, destination: int, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("capacity must be nonnegative")
        forward = Edge(destination, len(self.graph[destination]), capacity)
        reverse = Edge(source, len(self.graph[source]), 0)
        self.graph[source].append(forward)
        self.graph[destination].append(reverse)

    def maximum_flow(self, source: int, sink: int) -> int:
        total = 0
        while True:
            level = [-1] * len(self.graph)
            level[source] = 0
            queue = deque([source])
            while queue:
                vertex = queue.popleft()
                for edge in self.graph[vertex]:
                    if edge.capacity and level[edge.to] < 0:
                        level[edge.to] = level[vertex] + 1
                        queue.append(edge.to)
            if level[sink] < 0:
                return total

            cursor = [0] * len(self.graph)

            def send(vertex: int, amount: int) -> int:
                if vertex == sink:
                    return amount
                while cursor[vertex] < len(self.graph[vertex]):
                    edge = self.graph[vertex][cursor[vertex]]
                    if edge.capacity and level[edge.to] == level[vertex] + 1:
                        pushed = send(edge.to, min(amount, edge.capacity))
                        if pushed:
                            edge.capacity -= pushed
                            self.graph[edge.to][edge.reverse].capacity += pushed
                            return pushed
                    cursor[vertex] += 1
                return 0

            while pushed := send(source, 1 << 60):
                total += pushed


def bipartite_incidence(
    row_degrees: Sequence[int], column_degrees: Sequence[int]
) -> set[tuple[int, int]]:
    """Realize a simple bipartite degree sequence by integral max-flow."""

    if sum(row_degrees) != sum(column_degrees):
        raise ValueError("degree sums differ")
    rows, columns = len(row_degrees), len(column_degrees)
    if any(not 0 <= degree <= columns for degree in row_degrees):
        raise ValueError("invalid row degree")
    if any(not 0 <= degree <= rows for degree in column_degrees):
        raise ValueError("invalid column degree")

    source = 0
    row_offset = 1
    column_offset = row_offset + rows
    sink = column_offset + columns
    network = Dinic(sink + 1)
    for row, degree in enumerate(row_degrees):
        network.add_edge(source, row_offset + row, degree)
    for row in range(rows):
        for column in range(columns):
            network.add_edge(row_offset + row, column_offset + column, 1)
    for column, degree in enumerate(column_degrees):
        network.add_edge(column_offset + column, sink, degree)

    required = sum(row_degrees)
    if network.maximum_flow(source, sink) != required:
        raise AssertionError("claimed corner degrees are not realizable")

    incidence: set[tuple[int, int]] = set()
    for row in range(rows):
        for edge in network.graph[row_offset + row]:
            if column_offset <= edge.to < sink and edge.capacity == 0:
                incidence.add((row, edge.to - column_offset))
    assert [sum(i == row for i, _ in incidence) for row in range(rows)] == list(
        row_degrees
    )
    assert [
        sum(j == column for _, j in incidence) for column in range(columns)
    ] == list(column_degrees)
    return incidence


def assign(
    owner: dict[Cell, Label], label: Label, cells: Iterable[Cell]
) -> None:
    cells = tuple(cells)
    if not cells:
        raise AssertionError(f"empty part {label}")
    for cell in cells:
        if cell in owner:
            raise AssertionError(f"cell {cell} has two owners")
        owner[cell] = label


def invert_owner(owner: dict[Cell, Label]) -> dict[Label, tuple[Cell, ...]]:
    buckets: dict[Label, list[Cell]] = {}
    for cell, label in owner.items():
        buckets.setdefault(label, []).append(cell)
    return {label: tuple(sorted(cells)) for label, cells in buckets.items()}


def owner_sha256(owner: dict[Cell, Label]) -> str:
    rows = [
        {"cell": cell, "owner": owner[cell]}
        for cell in sorted(owner)
    ]
    return hashlib.sha256(
        json.dumps(rows, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()


def line_axis(part: Sequence[Cell]) -> int | None:
    varying = [
        axis
        for axis in range(len(part[0]))
        if len({cell[axis] for cell in part}) > 1
    ]
    if len(varying) > 1:
        raise AssertionError("part is not contained in a coordinate line")
    return varying[0] if varying else None


def hamming_degree(cell: Cell, part: Sequence[Cell]) -> int:
    return sum(
        sum(left != right for left, right in zip(cell, other, strict=True)) == 1
        for other in part
    )


def minimum_hamming_degree(part: Sequence[Cell]) -> int:
    return min(hamming_degree(cell, part) for cell in part)


def balanced_rectangle_owner(m: int, n: int, s: int) -> dict[Cell, Label]:
    """Construct a balanced rectangle partition via a flow-realized corner."""

    if s < 2 or m < s or n < s:
        raise ValueError("require s>=2 and m,n>=s")
    u, a = divmod(m, s)
    v, b = divmod(n, s)
    owner: dict[Cell, Label] = {}

    if a == 0:
        for column in range(n):
            for block in range(u):
                assign(
                    owner,
                    ("column-block", column, block),
                    ((row, column) for row in range(block * s, (block + 1) * s)),
                )
        return owner
    if b == 0:
        for row in range(m):
            for block in range(v):
                assign(
                    owner,
                    ("row-block", row, block),
                    ((row, column) for column in range(block * s, (block + 1) * s)),
                )
        return owner

    row_cut = (u - 1) * s
    column_cut = (v - 1) * s
    for column in range(n):
        for block in range(u - 1):
            assign(
                owner,
                ("outer-column", column, block),
                ((row, column) for row in range(block * s, (block + 1) * s)),
            )
    for row in range(row_cut, m):
        for block in range(v - 1):
            assign(
                owner,
                ("outer-row", row, block),
                (
                    (row, column)
                    for column in range(block * s, (block + 1) * s)
                ),
            )

    height, width = s + a, s + b
    quotient, remainder = divmod(a * b, s)
    selected = b + quotient
    large_rows = max(0, remainder - selected)
    large_columns = remainder - large_rows

    # Use the final rows/columns for the exceptional degrees.  The original
    # checker uses initial rows and a cyclic cursor; max-flow chooses the cells.
    row_marks = [b] * (height - large_rows) + [b - 1] * large_rows
    column_marks = [s] * (selected - large_columns) + [s + 1] * large_columns
    marks = bipartite_incidence(row_marks, column_marks)
    selected_columns = tuple(range(width - selected, width))

    for local_row in range(height):
        row = row_cut + local_row
        marked_columns = {
            selected_columns[local_column]
            for mark_row, local_column in marks
            if mark_row == local_row
        }
        assign(
            owner,
            ("corner-row", row),
            (
                (row, column_cut + local_column)
                for local_column in range(width)
                if local_column not in marked_columns
            ),
        )
    for local_column, corner_column in enumerate(selected_columns):
        assign(
            owner,
            ("corner-column", column_cut + corner_column),
            (
                (row_cut + local_row, column_cut + corner_column)
                for local_row in range(height)
                if (local_row, local_column) in marks
            ),
        )
    return owner


def check_balanced_rectangle(m: int, n: int, s: int) -> tuple[int, int, int]:
    owner = balanced_rectangle_owner(m, n, s)
    expected = set(itertools.product(range(m), range(n)))
    assert set(owner) == expected
    parts = invert_owner(owner)
    for part in parts.values():
        line_axis(part)
        assert len(part) in (s, s + 1)
    quotient, remainder = divmod(m * n, s)
    assert len(parts) == quotient
    assert sum(len(part) == s + 1 for part in parts.values()) == remainder
    return len(parts), len(owner), remainder


def thin_owner(m: int, n: int, p: int, s: int) -> dict[Cell, Label]:
    if not 1 <= p < s:
        raise ValueError("require 1<=p<s")
    rectangle = balanced_rectangle_owner(m, n, s)
    owner: dict[Cell, Label] = {}
    for layer in range(p):
        for (row, column), label in rectangle.items():
            cell = (row, column, layer)
            owner[cell] = ("layer", layer, *label)
    return owner


def check_thin_box(m: int, n: int, p: int, s: int) -> tuple[int, int, int]:
    owner = thin_owner(m, n, p, s)
    assert set(owner) == set(itertools.product(range(m), range(n), range(p)))
    parts = invert_owner(owner)
    for part in parts.values():
        axis = line_axis(part)
        assert axis != 2
        assert len(part) in (s, s + 1)
        assert len({cell[2] for cell in part}) == 1
    line_optimum = p * (m * n // s)
    global_quotient = m * n * p // s
    deficit = p * (m * n % s) // s
    assert len(parts) == line_optimum
    assert global_quotient - line_optimum == deficit
    return len(parts), len(owner), deficit


def hamming_family_minor_owner(s: int) -> dict[Cell, Label]:
    """Explicit line blocks plus one nonlinear (2,1,s-1) residue box."""

    if s < 3:
        raise ValueError("require s>=3")
    owner: dict[Cell, Label] = {}
    for y in range(s + 1):
        for z in range(s - 1):
            assign(
                owner,
                ("x-line", y, z),
                ((x, y, z) for x in range(s)),
            )
    for x in (s, s + 1):
        for z in range(s - 1):
            assign(
                owner,
                ("y-line", x, z),
                ((x, y, z) for y in range(s)),
            )
    assign(
        owner,
        ("nonlinear-residue",),
        ((x, s, z) for x in (s, s + 1) for z in range(s - 1)),
    )
    return owner


def check_hamming_family(s: int, full_lift: bool = False) -> tuple[int, int, int]:
    owner = hamming_family_minor_owner(s)
    sides = (s + 2, s + 1, s - 1)
    assert set(owner) == set(itertools.product(*(range(side) for side in sides)))
    parts = invert_owner(owner)
    nonlinear = parts[("nonlinear-residue",)]
    assert len(nonlinear) == 2 * (s - 1)
    assert minimum_hamming_degree(nonlinear) == s - 1
    for label, part in parts.items():
        assert minimum_hamming_degree(part) >= s - 1
        if label != ("nonlinear-residue",):
            assert len(part) == s
            line_axis(part)

    exact = s * s + 2 * s - 2
    line_ceiling = (s - 1) * ((s + 2) * (s + 1) // s)
    assert len(parts) == exact
    assert line_ceiling == exact - 1

    if full_lift:
        lifted: dict[Cell, Label] = {}
        for minor_cell, label in owner.items():
            for first in range(s + 2):
                lifted[(first, *minor_cell)] = label
        assert set(lifted) == set(
            itertools.product(range(s + 2), *(range(side) for side in sides))
        )
        lifted_parts = invert_owner(lifted)
        assert len(lifted_parts) == exact
        threshold = 2 * s
        for part in lifted_parts.values():
            assert minimum_hamming_degree(part) >= threshold
    return len(parts), line_ceiling, len(nonlinear)


def audit_shell_bound(max_s: int) -> tuple[int, int, int]:
    """Definition-level audit of the inherited class-size lower bound."""

    profiles = 0
    equality_profiles = 0
    digest = hashlib.sha256()
    for s in range(3, max_s + 1):
        capacities = (s + 1, s + 1, s, s - 2)
        threshold = 2 * s
        target_twice = 2 * s * (s + 2)
        for profile in itertools.product(*(range(capacity + 1) for capacity in capacities)):
            total = sum(profile)
            if total < threshold:
                continue
            lower_twice = 2 + 2 * total + sum(
                value * (threshold - value) for value in profile
            )
            assert lower_twice >= target_twice
            profiles += 1
            if lower_twice == target_twice:
                equality_profiles += 1
                digest.update(f"{s}:{profile}\n".encode())
    return profiles, equality_profiles, int.from_bytes(digest.digest()[:8], "big")


def audit_rectangles(max_s: int, margin: int) -> tuple[int, int, int, int]:
    boxes = parts = cells = large = 0
    for s in range(2, max_s + 1):
        for m in range(s, margin * s + 1):
            for n in range(s, margin * s + 1):
                count, volume, remainder = check_balanced_rectangle(m, n, s)
                boxes += 1
                parts += count
                cells += volume
                large += remainder
    return boxes, parts, cells, large


def audit_thin_boxes(max_s: int, margin: int) -> tuple[int, int, int, int]:
    boxes = parts = cells = positive = 0
    for s in range(2, max_s + 1):
        for m in range(s, margin * s + 1):
            for n in range(s, margin * s + 1):
                for p in range(1, s):
                    count, volume, deficit = check_thin_box(m, n, p, s)
                    boxes += 1
                    parts += count
                    cells += volume
                    positive += deficit > 0
    return boxes, parts, cells, positive


def audit_boundary_identities(max_s: int) -> tuple[int, int, int, str]:
    states = positive = accumulated = 0
    digest = hashlib.sha256()
    for s in range(2, max_s + 1):
        for remainder in range(s):
            for residual_layers in range(1, s):
                deficit = residual_layers * remainder // s
                # The complete-slab quotient is irrelevant; use two unrelated
                # values to ensure its cancellation is represented exactly.
                for quotient_cycles in (0, s + 3):
                    mn = quotient_cycles * s + remainder
                    for complete_slabs in (0, 2):
                        side = complete_slabs * s + residual_layers
                        no_crossing = complete_slabs * mn + residual_layers * (
                            mn // s
                        )
                        assert mn * side // s - no_crossing == deficit
                        states += 1
                if deficit:
                    positive += 1
                    accumulated += deficit
                    digest.update(f"{s},{remainder},{residual_layers},{deficit}\n".encode())
    return states, positive, accumulated, digest.hexdigest()


def audit_hamming_family(max_s: int, reconstruct_max_s: int) -> tuple[int, int, int, str]:
    symbolic = reconstructed = classes = 0
    digest = hashlib.sha256()
    for s in range(3, max_s + 1):
        deficits = (s + 1, s + 1, s, s - 2)
        assert sum(deficits) == 4 * s
        assert (sum(deficits) + 1) // 2 == 2 * s
        residues = (2, 1, s - 1)
        assert s <= residues[0] * residues[1] * residues[2] < 2 * s
        assert sum(residues) == s + 2
        volume = (s + 2) * (s + 1) * (s - 1)
        exact = volume // s
        assert exact == s * s + 2 * s - 2
        assert (s - 1) * (s + 3) == exact - 1
        symbolic += 1
        digest.update(f"{s},{volume},{exact}\n".encode())
        if s <= reconstruct_max_s:
            count, _, _ = check_hamming_family(s, full_lift=(s == 3))
            assert count == exact
            reconstructed += 1
            classes += count
    return symbolic, reconstructed, classes, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rectangle-max-s", type=int, default=16)
    parser.add_argument("--rectangle-margin", type=int, default=3)
    parser.add_argument("--thin-max-s", type=int, default=10)
    parser.add_argument("--thin-margin", type=int, default=2)
    parser.add_argument("--boundary-max-s", type=int, default=128)
    parser.add_argument("--shell-max-s", type=int, default=28)
    parser.add_argument("--family-max-s", type=int, default=10000)
    parser.add_argument("--family-reconstruct-max-s", type=int, default=18)
    args = parser.parse_args()

    rectangles = audit_rectangles(args.rectangle_max_s, args.rectangle_margin)
    thin = audit_thin_boxes(args.thin_max_s, args.thin_margin)
    boundaries = audit_boundary_identities(args.boundary_max_s)
    shell = audit_shell_bound(args.shell_max_s)
    family = audit_hamming_family(
        args.family_max_s, args.family_reconstruct_max_s
    )
    base = check_hamming_family(3, full_lift=True)
    base_minor = hamming_family_minor_owner(3)
    base_lifted = {
        (first, *minor_cell): label
        for minor_cell, label in base_minor.items()
        for first in range(5)
    }
    base_minimum_degree = min(
        minimum_hamming_degree(part)
        for part in invert_owner(base_lifted).values()
    )

    report = {
        "base_case": {
            "exact_colours": base[0],
            "full_vertices_checked": 5 * 5 * 4 * 2,
            "lifted_owner_sha256": owner_sha256(base_lifted),
            "line_lift_ceiling": base[1],
            "minimum_same_colour_degree": base_minimum_degree,
            "nonlinear_minor_cells": base[2],
        },
        "boundary_identity_audit": {
            "accumulated_positive_deficit": boundaries[2],
            "max_s": args.boundary_max_s,
            "positive_residue_pairs": boundaries[1],
            "sha256": boundaries[3],
            "states": boundaries[0],
        },
        "flow_rectangle_audit": {
            "boxes": rectangles[0],
            "cells": rectangles[2],
            "large_parts": rectangles[3],
            "max_s": args.rectangle_max_s,
            "parts": rectangles[1],
        },
        "hamming_family_audit": {
            "classes": family[2],
            "max_s": args.family_max_s,
            "reconstructed": family[1],
            "sha256": family[3],
            "symbolic": family[0],
        },
        "shell_bound_audit": {
            "equality_profiles": shell[1],
            "max_s": args.shell_max_s,
            "profile_digest_u64": shell[2],
            "profiles": shell[0],
        },
        "thin_owner_audit": {
            "boxes": thin[0],
            "cells": thin[2],
            "max_s": args.thin_max_s,
            "parts": thin[1],
            "positive_deficit_boxes": thin[3],
        },
        "verdict": "ACCEPT",
    }
    canonical = json.dumps(report, indent=2, sort_keys=True)
    print(canonical)
    print(f"certificate_sha256={hashlib.sha256(canonical.encode()).hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
