#!/usr/bin/env python3
"""Definitionally verify the c=13 one-neighborhood counterexample."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


N = 21
H = frozenset(range(20))
R = frozenset(range(13))
A = frozenset(range(13, 20))
V = 20
EXPECTED_EDGE_SHA256 = "df51657665a58646c8cd53f74bf723b5e000b8e39d1d063a88347aacaab55160"
EXPECTED_GRAPH6 = "Ts`?XGRQR@B`Kcqk\\Ve~kPpq`N\\`mOjnJ~}?"


def parse(path: Path) -> set[tuple[int, int]]:
    if hashlib.sha256(path.read_bytes()).hexdigest() != EXPECTED_EDGE_SHA256:
        raise AssertionError("certificate byte hash mismatch")
    edges: set[tuple[int, int]] = set()
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        fields = raw.split()
        if len(fields) != 2:
            raise ValueError((line_number, raw))
        i, j = map(int, fields)
        if not 0 <= i < j < 20 or (i, j) in edges:
            raise ValueError((line_number, i, j))
        edges.add((i, j))
    if len(edges) != 87:
        raise AssertionError(len(edges))
    edges.update((i, V) for i in R)
    return edges


def graph6(edges: set[tuple[int, int]]) -> str:
    bits = []
    for j in range(1, N):
        for i in range(j):
            bits.append(int((i, j) in edges))
    bits.extend([0] * ((-len(bits)) % 6))
    return chr(N + 63) + "".join(
        chr(63 + sum(bits[offset + bit] << (5 - bit) for bit in range(6)))
        for offset in range(0, len(bits), 6)
    )


def all_red(edges: set[tuple[int, int]], vertices: tuple[int, ...]) -> bool:
    return all(tuple(sorted(pair)) in edges for pair in itertools.combinations(vertices, 2))


def all_blue(edges: set[tuple[int, int]], vertices: tuple[int, ...]) -> bool:
    return all(tuple(sorted(pair)) not in edges for pair in itertools.combinations(vertices, 2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("edge_list", type=Path)
    args = parser.parse_args()
    edges = parse(args.edge_list)

    if graph6(edges) != EXPECTED_GRAPH6:
        raise AssertionError(graph6(edges))
    if any(all_red(edges, subset) for subset in itertools.combinations(range(N), 4)):
        raise AssertionError("red K4")
    if any(all_blue(edges, subset) for subset in itertools.combinations(range(N), 5)):
        raise AssertionError("blue K5")
    if {i for i in H if tuple(sorted((i, V))) in edges} != R:
        raise AssertionError("partner neighborhood")
    if any(all_red(edges, subset) for subset in itertools.combinations(R, 3)):
        raise AssertionError("red triangle in R")
    if any(all_blue(edges, subset) for subset in itertools.combinations(R, 5)):
        raise AssertionError("blue K5 in R")
    if any(all_red(edges, subset) for subset in itertools.combinations(A, 4)):
        raise AssertionError("red K4 in A")
    if any(all_blue(edges, subset) for subset in itertools.combinations(A, 4)):
        raise AssertionError("blue K4 in A")

    red_triangles = sum(all_red(edges, subset) for subset in itertools.combinations(range(N), 3))
    blue_fours = sum(all_blue(edges, subset) for subset in itertools.combinations(range(N), 4))
    degrees = sorted((sum(tuple(sorted((i, j))) in edges for j in range(N) if j != i) for i in range(N)), reverse=True)
    print(
        "PASS c13_one_neighborhood_counterexample "
        f"n={N} edges={len(edges)} h_edges=87 partner_degree=13 "
        f"red_triangles={red_triangles} blue_independent_4sets={blue_fours}"
    )
    print("degree_sequence=" + ",".join(map(str, degrees)))
    print("graph6=" + EXPECTED_GRAPH6)
    print("edge_sha256=" + EXPECTED_EDGE_SHA256)


if __name__ == "__main__":
    main()
