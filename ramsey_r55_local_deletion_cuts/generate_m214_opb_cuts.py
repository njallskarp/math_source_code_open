#!/usr/bin/env python3
"""Emit the controlled |S|<=2 local-deletion cuts for the height-2505 OPB."""

from __future__ import annotations

import argparse
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path


N = 43
EDGE_COUNT = N * (N - 1) // 2
U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}


def edge_id(i: int, j: int) -> int:
    i, j = sorted((i, j))
    if not (0 <= i < j < N):
        raise ValueError((i, j))
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


TRIANGLE_IDS = {
    triple: EDGE_COUNT + rank
    for rank, triple in enumerate(combinations(range(N), 3), 1)
}


def triangle_id(i: int, j: int, k: int) -> int:
    return TRIANGLE_IDS[tuple(sorted((i, j, k)))]


def cut_specs(max_removed: int = 2):
    if not 1 <= max_removed <= 2:
        raise ValueError("the controlled public emitter supports max_removed=1 or 2")
    for root in range(N):
        degree, local_edges = (20, 93) if root < 13 else (21, 100)
        others = tuple(vertex for vertex in range(N) if vertex != root)
        for removed_size in range(1, max_removed + 1):
            remaining_order = degree - removed_size
            if remaining_order not in U:
                continue
            required_incident = local_edges - U[remaining_order]
            if required_incident <= 0:
                continue
            for removed in combinations(others, removed_size):
                yield root, degree, local_edges, removed, required_incident


def cut_line(root: int, local_edges: int, removed: tuple[int, ...], required: int) -> str:
    others = tuple(vertex for vertex in range(N) if vertex != root)
    removed_set = frozenset(removed)
    incident_triangles = (
        triangle_id(root, left, right)
        for left, right in combinations(others, 2)
        if left in removed_set or right in removed_set
    )
    terms = [f"+1 x{variable}" for variable in incident_triangles]
    terms.extend(f"-{local_edges} x{edge_id(root, vertex)}" for vertex in removed)
    rhs = required - local_edges * len(removed)
    return " ".join(terms) + f" >= {rhs} ;"


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


def generate(raw, max_removed: int = 2):
    specs = tuple(cut_specs(max_removed))
    writer = CanonicalWriter(raw)
    writer.line(
        f"* local-deletion cut rows for height-2505 M=214 OPB; "
        f"rows={len(specs)} max_removed={max_removed}"
    )
    counts = {}
    for root, degree, local_edges, removed, required in specs:
        writer.line(cut_line(root, local_edges, removed, required))
        key = f"degree_{degree}_removed_{len(removed)}"
        counts[key] = counts.get(key, 0) + 1
    return {
        "bytes": writer.bytes_written,
        "cut_rows": len(specs),
        "lines": writer.lines_written,
        "max_removed": max_removed,
        "row_counts": counts,
        "sha256": writer.sha256.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-removed", type=int, default=2, choices=(1, 2))
    args = parser.parse_args()
    destination = args.output.resolve()
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()
    try:
        with temporary.open("wb") as raw:
            summary = generate(raw, args.max_removed)
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
