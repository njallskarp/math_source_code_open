#!/usr/bin/env python3
"""Generate the canonical complete normalized OPB formulation of the M=214 branch."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path


N = 43
EXCEPTIONAL = tuple(range(13))
ANCHOR = 13
ANCHOR_RED_EXCEPTIONAL = frozenset(range(6))
ANCHOR_RED_CENTRAL = frozenset(range(14, 29))
ANCHOR_RED = ANCHOR_RED_EXCEPTIONAL | ANCHOR_RED_CENTRAL
EDGE_COUNT = N * (N - 1) // 2
TRIANGLE_COUNT = N * (N - 1) * (N - 2) // 6
VARIABLE_COUNT = EDGE_COUNT + TRIANGLE_COUNT
FIVE_SET_COUNT = N * (N - 1) * (N - 2) * (N - 3) * (N - 4) // 120
EQUALITY_COUNT = 2 * N + (N - 1)
CONSTRAINT_COUNT = (
    2 * FIVE_SET_COUNT
    + 4 * TRIANGLE_COUNT
    + N  # degree equalities
    + N  # red-neighborhood edge-count equalities
    + N  # at least six red neighbors in the exceptional class
    + (N - 1)  # normalized anchor incidences
)


class CanonicalWriter:
    def __init__(self, raw):
        self.raw = raw
        self.sha256 = hashlib.sha256()
        self.bytes_written = 0
        self.lines_written = 0

    def line(self, text: str) -> None:
        data = (text + "\n").encode("ascii")
        self.raw.write(data)
        self.sha256.update(data)
        self.bytes_written += len(data)
        self.lines_written += 1


def edge_id(i: int, j: int) -> int:
    if not (0 <= i < j < N):
        raise ValueError(f"invalid edge ({i},{j})")
    before = i * (2 * N - i - 1) // 2
    return before + (j - i - 1) + 1


def build_triangle_ids() -> dict[tuple[int, int, int], int]:
    return {
        triple: EDGE_COUNT + rank
        for rank, triple in enumerate(itertools.combinations(range(N), 3), 1)
    }


def constraint(terms: list[tuple[int, int]], relation: str, rhs: int) -> str:
    if relation not in {">=", "="}:
        raise ValueError("canonical OPB uses only >= and =")
    if not terms:
        raise ValueError("empty constraint")
    return " ".join(f"{coefficient:+d} x{variable}" for coefficient, variable in terms) + f" {relation} {rhs} ;"


def generate(raw) -> dict[str, int | str]:
    triangle_ids = build_triangle_ids()
    writer = CanonicalWriter(raw)
    writer.line(
        f"* #variable= {VARIABLE_COUNT} #constraint= {CONSTRAINT_COUNT} "
        f"#equal= {EQUALITY_COUNT} intsize= 64"
    )

    emitted = 0

    # No blue K5 and no red K5, respectively, for every labeled five-set.
    for vertices in itertools.combinations(range(N), 5):
        edges = [edge_id(i, j) for i, j in itertools.combinations(vertices, 2)]
        writer.line(constraint([(1, edge) for edge in edges], ">=", 1))
        writer.line(constraint([(-1, edge) for edge in edges], ">=", -9))
        emitted += 2

    # z_ijk is equivalent to the conjunction of the three red edge bits.
    for triangle, z in triangle_ids.items():
        edges = [edge_id(i, j) for i, j in itertools.combinations(triangle, 2)]
        for edge in edges:
            writer.line(constraint([(-1, z), (1, edge)], ">=", 0))
        writer.line(constraint([(1, z)] + [(-1, edge) for edge in edges], ">=", -2))
        emitted += 4

    # Canonically label vertices 0..12 as degree 20 and 13..42 as degree 21.
    for vertex in range(N):
        incident = [edge_id(*sorted((vertex, other))) for other in range(N) if other != vertex]
        degree = 20 if vertex in EXCEPTIONAL else 21
        writer.line(constraint([(1, edge) for edge in incident], "=", degree))
        emitted += 1

    # Every red color-neighborhood is exactly seven below U(20)=100 or U(21)=107.
    for vertex in range(N):
        others = [other for other in range(N) if other != vertex]
        triangles = [triangle_ids[tuple(sorted((vertex, i, j)))] for i, j in itertools.combinations(others, 2)]
        local_red_edges = 93 if vertex in EXCEPTIONAL else 100
        writer.line(constraint([(1, z) for z in triangles], "=", local_red_edges))
        emitted += 1

    # Via the degree-neighborhood identity, these are exactly the blue hard-branch caps.
    for vertex in range(N):
        exceptional_neighbors = [
            edge_id(*sorted((vertex, other))) for other in EXCEPTIONAL if other != vertex
        ]
        writer.line(constraint([(1, edge) for edge in exceptional_neighbors], ">=", 6))
        emitted += 1

    # A doubly exact degree-21 anchor exists. Relabel within the two degree classes
    # so its red split is E:6+7 and C\{anchor}:15+14.
    for other in range(N):
        if other == ANCHOR:
            continue
        value = 1 if other in ANCHOR_RED else 0
        writer.line(constraint([(1, edge_id(*sorted((ANCHOR, other))))], "=", value))
        emitted += 1

    if emitted != CONSTRAINT_COUNT:
        raise AssertionError((emitted, CONSTRAINT_COUNT))
    if writer.lines_written != CONSTRAINT_COUNT + 1:
        raise AssertionError(writer.lines_written)
    return {
        "bytes": writer.bytes_written,
        "constraints": emitted,
        "five_sets": FIVE_SET_COUNT,
        "lines": writer.lines_written,
        "sha256": writer.sha256.hexdigest(),
        "triangle_variables": TRIANGLE_COUNT,
        "variables": VARIABLE_COUNT,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True, help="OPB destination (generated state; do not commit)")
    args = parser.parse_args()
    destination = args.output.resolve()
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()
    try:
        with temporary.open("wb") as raw:
            summary = generate(raw)
            raw.flush()
            os.fsync(raw.fileno())
        os.replace(temporary, destination)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
