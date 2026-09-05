#!/usr/bin/env python3
"""Streaming audit of the controlled M=214 deletion-cut OPB rows."""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path


N = 43
EDGE_COUNT = 903
U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}


def edge_id(i: int, j: int) -> int:
    i, j = min(i, j), max(i, j)
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


def triangle_ids():
    return {triple: EDGE_COUNT + rank for rank, triple in enumerate(combinations(range(N), 3), 1)}


def expected_specs():
    for root in range(N):
        degree, total = (20, 93) if root < 13 else (21, 100)
        vertices = tuple(v for v in range(N) if v != root)
        for size in (1, 2):
            required = total - U[degree - size]
            if required <= 0:
                continue
            yield root, total, required, combinations(vertices, size)


def parse_row(line: str):
    tokens = line.split()
    if len(tokens) < 6 or tokens[-3] != ">=" or tokens[-1] != ";":
        raise ValueError("row grammar")
    terms = {}
    for position in range(0, len(tokens) - 3, 2):
        coefficient = int(tokens[position])
        variable = int(tokens[position + 1][1:])
        if variable in terms:
            raise ValueError("duplicate variable")
        terms[variable] = coefficient
    return terms, int(tokens[-2])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stream", type=Path)
    args = parser.parse_args()
    triangle = triangle_ids()
    rows = 0
    coefficients = 0
    with args.stream.open() as source:
        header = source.readline().rstrip("\n")
        if header != "* local-deletion cut rows for height-2505 M=214 OPB; rows=37569 max_removed=2":
            raise ValueError("header")
        for root, total, required, subsets in expected_specs():
            universe = tuple(v for v in range(N) if v != root)
            for removed in subsets:
                line = source.readline()
                if not line:
                    raise ValueError("truncated stream")
                actual, rhs = parse_row(line)
                removed_set = set(removed)
                expected = {
                    triangle[tuple(sorted((root, left, right)))]: 1
                    for left, right in combinations(universe, 2)
                    if left in removed_set or right in removed_set
                }
                expected.update({edge_id(root, v): -total for v in removed})
                if actual != expected:
                    raise ValueError(("terms", root, removed))
                if rhs != required - total * len(removed):
                    raise ValueError(("rhs", root, removed))
                rows += 1
                coefficients += len(actual)
        if source.read():
            raise ValueError("trailing stream")
    if rows != 37569 or coefficients != 3095841:
        raise ValueError((rows, coefficients))
    print(f"PASS {rows} M=214 guarded cut rows and {coefficients} coefficients")


if __name__ == "__main__":
    main()
