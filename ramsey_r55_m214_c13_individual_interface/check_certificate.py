#!/usr/bin/env python3
"""Definition-level checker for an individual M=214,c=13 interface witness."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


CORE_ORDER = 13
OUTSIDE_ORDER = 28
N = 43
U, V = 0, 1
CORE = tuple(range(2, 15))
D = tuple(range(15, 43))
A_LOCAL = tuple(range(0, 7))
B_LOCAL = tuple(range(7, 14))
O_LOCAL = tuple(range(14, 28))
CORE_DIFFERENCES = frozenset((1, 5, 8, 12))


def core_edge(i: int, j: int) -> bool:
    return i != j and ((i - j) % CORE_ORDER) in CORE_DIFFERENCES


def independent_core_sets(size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        subset
        for subset in itertools.combinations(range(CORE_ORDER), size)
        if all(not core_edge(i, j) for i, j in itertools.combinations(subset, 2))
    )


def parse(path: Path) -> tuple[dict[str, object], str]:
    raw = path.read_bytes()
    data = json.loads(raw)
    expected = {"core_e", "footprints", "outside_e", "outside_red_edges", "pivot"}
    if not isinstance(data, dict) or set(data) != expected:
        raise ValueError("certificate fields")
    return data, hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    data, certificate_hash = parse(args.certificate)

    core_e_list = data["core_e"]
    outside_e_list = data["outside_e"]
    footprints_text = data["footprints"]
    edge_list = data["outside_red_edges"]
    pivot = data["pivot"]
    if not isinstance(core_e_list, list) or len(set(core_e_list)) != len(core_e_list):
        raise ValueError("core_e")
    if not isinstance(outside_e_list, list) or len(set(outside_e_list)) != len(outside_e_list):
        raise ValueError("outside_e")
    if any(not isinstance(i, int) or not 0 <= i < CORE_ORDER for i in core_e_list):
        raise ValueError("core_e member")
    if any(not isinstance(x, int) or not 0 <= x < OUTSIDE_ORDER for x in outside_e_list):
        raise ValueError("outside_e member")
    core_e = frozenset(core_e_list)
    outside_e = frozenset(outside_e_list)
    if len(core_e) + len(outside_e) != 13:
        raise AssertionError("mark count")

    if not isinstance(footprints_text, list) or len(footprints_text) != OUTSIDE_ORDER:
        raise ValueError("footprints")
    footprints: list[int] = []
    for text in footprints_text:
        if not isinstance(text, str) or len(text) != 4 or text != text.lower():
            raise ValueError("footprint encoding")
        mask = int(text, 16)
        if not 0 <= mask < 1 << CORE_ORDER:
            raise ValueError("footprint range")
        footprints.append(mask)

    outside_edges: set[tuple[int, int]] = set()
    if not isinstance(edge_list, list):
        raise ValueError("edge list")
    previous = None
    for pair in edge_list:
        if (not isinstance(pair, list) or len(pair) != 2
                or any(not isinstance(x, int) for x in pair)):
            raise ValueError("edge")
        x, y = pair
        if not 0 <= x < y < OUTSIDE_ORDER or previous is not None and (x, y) <= previous:
            raise ValueError("edge ordering")
        previous = (x, y)
        outside_edges.add((x, y))

    if not isinstance(pivot, str) or len(pivot) < 2 or pivot[0] not in "CD":
        raise ValueError("pivot")
    pivot_index = int(pivot[1:])
    if pivot[0] == "C":
        if pivot_index not in core_e:
            raise AssertionError("unmarked core pivot")
        pivot_global = CORE[pivot_index]
    else:
        if pivot_index not in A_LOCAL or pivot_index not in outside_e:
            raise AssertionError("invalid outside pivot")
        pivot_global = D[pivot_index]

    def red(i: int, j: int) -> bool:
        if i == j:
            return False
        if i > j:
            i, j = j, i
        if (i, j) == (U, V):
            return True
        if i in (U, V) and j in CORE:
            return True
        if i in CORE and j in CORE:
            return core_edge(i - CORE[0], j - CORE[0])
        if i == U and j in D:
            return j - D[0] in A_LOCAL
        if i == V and j in D:
            return j - D[0] in B_LOCAL
        if i in CORE and j in D:
            return bool(footprints[j - D[0]] >> (i - CORE[0]) & 1)
        if i in D and j in D:
            return (i - D[0], j - D[0]) in outside_edges
        raise AssertionError((i, j))

    marked = frozenset(CORE[i] for i in core_e) | frozenset(D[x] for x in outside_e)
    if len(marked) != 13 or U in marked or V in marked:
        raise AssertionError("global marks")

    core_edges = tuple(
        pair for pair in itertools.combinations(range(CORE_ORDER), 2) if core_edge(*pair)
    )
    triples = independent_core_sets(3)
    fours = independent_core_sets(4)
    if (len(core_edges), len(triples), len(fours)) != (26, 78, 39):
        raise AssertionError("core census")
    for x, mask in enumerate(footprints):
        if any(not mask & sum(1 << i for i in four) for four in fours):
            raise AssertionError(("nontransversal", x))

    # Check the compressed pairwise interface directly from masks and colors.
    red_forbidden = blue_forbidden = 0
    for x, y in itertools.combinations(range(OUTSIDE_ORDER), 2):
        xy_red = (x, y) in outside_edges
        if not xy_red and any(
            all(not (footprints[x] >> i & 1) and not (footprints[y] >> i & 1) for i in triple)
            for triple in triples
        ):
            blue_forbidden += 1
        same_anchor_cell = (x in A_LOCAL and y in A_LOCAL) or (x in B_LOCAL and y in B_LOCAL)
        if xy_red and same_anchor_cell and any(
            all(footprints[z] >> i & 1 for z in (x, y) for i in pair)
            for pair in core_edges
        ):
            red_forbidden += 1
    if red_forbidden or blue_forbidden:
        raise AssertionError(("pairwise interface", red_forbidden, blue_forbidden))

    degrees = [sum(red(i, j) for j in range(N) if j != i) for i in range(N)]
    expected_degrees = [20 if i in marked else 21 for i in range(N)]
    if degrees != expected_degrees:
        raise AssertionError(("degrees", [(i, degrees[i], expected_degrees[i]) for i in range(N) if degrees[i] != expected_degrees[i]]))
    e_incidence = [sum(j in marked and red(i, j) for j in range(N) if j != i) for i in range(N)]
    expected_e = [8 if i == pivot_global else 6 for i in range(N)]
    if e_incidence != expected_e:
        raise AssertionError(("E incidence", [(i, e_incidence[i], expected_e[i]) for i in range(N) if e_incidence[i] != expected_e[i]]))

    def triangle_count(vertex: int, color: bool) -> int:
        neighbors = [other for other in range(N) if other != vertex and red(vertex, other) == color]
        return sum(red(i, j) == color for i, j in itertools.combinations(neighbors, 2))

    anchor_triangles = {
        "u_blue": triangle_count(U, False),
        "u_red": triangle_count(U, True),
        "v_blue": triangle_count(V, False),
        "v_red": triangle_count(V, True),
    }
    if set(anchor_triangles.values()) != {100}:
        raise AssertionError(("anchor triangles", anchor_triangles))

    mono_by_outside_count = {k: {"blue": 0, "red": 0} for k in range(6)}
    for five in itertools.combinations(range(N), 5):
        colors = [red(i, j) for i, j in itertools.combinations(five, 2)]
        if all(colors) or not any(colors):
            key = "red" if all(colors) else "blue"
            outside_count = sum(vertex in D for vertex in five)
            mono_by_outside_count[outside_count][key] += 1
    if any(mono_by_outside_count[k][color] for k in range(3) for color in ("red", "blue")):
        raise AssertionError(("interface incompleteness", mono_by_outside_count))

    triangle_mismatches = []
    for vertex in range(N):
        red_triangles = triangle_count(vertex, True)
        blue_triangles = triangle_count(vertex, False)
        expected = 93 if vertex in marked else 100
        if red_triangles != expected or blue_triangles != expected:
            triangle_mismatches.append([vertex, red_triangles, blue_triangles, expected])

    result = {
        "anchor_triangles": anchor_triangles,
        "certificate_sha256": certificate_hash,
        "core_independent_fours": len(fours),
        "core_independent_triples": len(triples),
        "global_blue_K5": sum(row["blue"] for row in mono_by_outside_count.values()),
        "global_red_K5": sum(row["red"] for row in mono_by_outside_count.values()),
        "marked_core": len(core_e),
        "marked_outside": len(outside_e),
        "monochromatic_K5_by_outside_count": mono_by_outside_count,
        "outside_red_edges": len(outside_edges),
        "pivot": pivot,
        "degree_mismatch_vertices": 0,
        "E_incidence_mismatch_vertices": 0,
        "status": "VERIFIED INDIVIDUAL PAIRWISE-INTERFACE WITNESS",
        "triangle_mismatch_vertices": len(triangle_mismatches),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
