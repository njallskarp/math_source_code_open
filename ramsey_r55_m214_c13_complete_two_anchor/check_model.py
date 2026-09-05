#!/usr/bin/env python3
"""Directly check a model of the complete unpinned c=13 two-anchor relaxation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


N = 43
E = frozenset(range(13))
U = 13
V = 14
U_RED = frozenset(range(6)) | frozenset(range(14, 29))
EXPECTED_SHA256 = "bc92dd1f5f1f8827d35a58048ade97a102921f7cab193f6b30706cb5184eed99"


def parse(path: Path) -> set[tuple[int, int]]:
    if hashlib.sha256(path.read_bytes()).hexdigest() != EXPECTED_SHA256:
        raise AssertionError("certificate byte hash mismatch")
    edges: set[tuple[int, int]] = set()
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        fields = raw.split()
        if len(fields) != 2:
            raise ValueError((line_number, raw))
        i, j = map(int, fields)
        if not 0 <= i < j < N or (i, j) in edges:
            raise ValueError((line_number, i, j))
        edges.add((i, j))
    if len(edges) != 445:
        raise AssertionError(len(edges))
    return edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("edge_list", type=Path)
    args = parser.parse_args()
    red_edges = parse(args.edge_list)

    def red(i: int, j: int) -> bool:
        return tuple(sorted((i, j))) in red_edges

    def red_neighbors(vertex: int) -> frozenset[int]:
        return frozenset(other for other in range(N) if other != vertex and red(vertex, other))

    def edge_count(vertices: frozenset[int], colour: bool = True) -> int:
        return sum(red(i, j) == colour for i, j in itertools.combinations(sorted(vertices), 2))

    def cross_count(left: frozenset[int], right: frozenset[int]) -> int:
        return sum(red(i, j) for i in left for j in right)

    def monochromatic_count(vertices: frozenset[int], order: int, colour: bool) -> int:
        return sum(
            all(red(i, j) == colour for i, j in itertools.combinations(subset, 2))
            for subset in itertools.combinations(sorted(vertices), order)
        )

    neighborhoods = {vertex: red_neighbors(vertex) for vertex in range(N)}
    for vertex, neighborhood in neighborhoods.items():
        expected = 20 if vertex in E else 21
        if len(neighborhood) != expected:
            raise AssertionError(("degree", vertex, len(neighborhood), expected))
        e_expected = 8 if vertex == 5 else 6
        if len(neighborhood & E) != e_expected:
            raise AssertionError(("E-incidence", vertex, len(neighborhood & E), e_expected))

    nru = neighborhoods[U]
    nrv = neighborhoods[V]
    nbu = frozenset(range(N)) - {U} - nru
    nbv = frozenset(range(N)) - {V} - nrv
    if nru != U_RED:
        raise AssertionError("anchor normalization")
    if V not in nru or U not in nrv or len(nru & nrv) != 13:
        raise AssertionError("partner or codegree")

    for name, vertices, red_order, blue_order in (
        ("u-red", nru, 4, 5),
        ("u-blue", nbu, 5, 4),
        ("v-red", nrv, 4, 5),
        ("v-blue", nbv, 5, 4),
    ):
        if monochromatic_count(vertices, red_order, True):
            raise AssertionError((name, "red", red_order))
        if monochromatic_count(vertices, blue_order, False):
            raise AssertionError((name, "blue", blue_order))

    if (edge_count(nru), edge_count(nbu, False), edge_count(nrv), edge_count(nbv, False)) != (100, 100, 100, 100):
        raise AssertionError("anchor local totals")

    r = (nru - {V}) & (nrv - {U})
    a = (nru - {V}) - nrv
    b = (nrv - {U}) - nru
    d = frozenset(range(N)) - {U, V} - r - a - b
    cells = (r, a, b, d)
    if tuple(map(len, cells)) != (13, 7, 7, 14):
        raise AssertionError("cell sizes")
    if tuple(len(cell & E) for cell in cells) != (3, 3, 3, 4):
        raise AssertionError("E cell sizes")
    internal = tuple(edge_count(cell) for cell in cells)
    cross = (
        cross_count(r, a), cross_count(r, b), cross_count(a, d),
        cross_count(b, d), cross_count(r, d), cross_count(a, b),
    )
    if internal != (26, 9, 8, 45) or cross != (52, 53, 56, 57, 87, 11):
        raise AssertionError((internal, cross))
    if cross[-2] + cross[-1] != sum(internal) + 10:
        raise AssertionError("diagonal identity")

    all_vertices = frozenset(range(N))
    red_fives = monochromatic_count(all_vertices, 5, True)
    blue_fives = monochromatic_count(all_vertices, 5, False)
    if (red_fives, blue_fives) != (180, 513):
        raise AssertionError((red_fives, blue_fives))

    print("PASS c13_complete_two_anchor_model n=43 edges=445 degrees=20^13,21^30 E_incidence=6^42,8^1")
    print("anchors=u13,v14 codegree=13 local_red_edges=100,100 local_blue_edges=100,100")
    print("cells=R13,A7,B7,D14 E_cells=3,3,3,4 C_cells=10,4,4,10")
    print("internal=eR26,eA9,eB8,eD45 cross=eRA52,eRB53,eAD56,eBD57,eRD87,eAB11")
    print(f"global_outside_obstruction=redK5:{red_fives},blueK5:{blue_fives}")
    print("edge_sha256=" + EXPECTED_SHA256)


if __name__ == "__main__":
    main()
