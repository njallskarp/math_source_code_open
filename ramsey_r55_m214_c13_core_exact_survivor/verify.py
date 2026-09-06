#!/usr/bin/env python3
"""Definition-level verifier for the core-exact c=13 survivor."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


N = 43
CORE_ORDER = 13
OUTSIDE_ORDER = 28
U, V = 0, 1
CORE = tuple(range(2, 15))
OUTSIDE = tuple(range(15, 43))
A_LOCAL = frozenset(range(7))
B_LOCAL = frozenset(range(7, 14))
CORE_DIFFERENCES = frozenset((1, 5, 8, 12))
OUTSIDE_PAIRS = tuple(itertools.combinations(range(OUTSIDE_ORDER), 2))


def core_edge(i: int, j: int) -> bool:
    return i != j and (i - j) % CORE_ORDER in CORE_DIFFERENCES


def parse(path: Path) -> tuple[dict[str, object], str]:
    raw = path.read_bytes()
    data = json.loads(raw)
    expected = {"core_e", "footprints", "outside_e", "outside_red_bits", "pivot"}
    if not isinstance(data, dict) or set(data) != expected:
        raise ValueError("certificate fields")
    return data, hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    data, certificate_hash = parse(args.certificate)

    core_e_data = data["core_e"]
    outside_e_data = data["outside_e"]
    footprint_data = data["footprints"]
    bits_text = data["outside_red_bits"]
    pivot = data["pivot"]
    if not isinstance(core_e_data, list) or core_e_data != sorted(set(core_e_data)):
        raise ValueError("core_e")
    if not isinstance(outside_e_data, list) or outside_e_data != sorted(set(outside_e_data)):
        raise ValueError("outside_e")
    if any(not isinstance(i, int) or not 0 <= i < CORE_ORDER for i in core_e_data):
        raise ValueError("core_e member")
    if any(not isinstance(x, int) or not 0 <= x < OUTSIDE_ORDER for x in outside_e_data):
        raise ValueError("outside_e member")
    core_e = frozenset(core_e_data)
    outside_e = frozenset(outside_e_data)
    if len(core_e) + len(outside_e) != 13:
        raise AssertionError("mark count")

    if not isinstance(footprint_data, list) or len(footprint_data) != OUTSIDE_ORDER:
        raise ValueError("footprints")
    footprints: list[int] = []
    for text in footprint_data:
        if not isinstance(text, str) or len(text) != 4 or text != text.lower():
            raise ValueError("footprint syntax")
        mask = int(text, 16)
        if mask >= 1 << CORE_ORDER:
            raise ValueError("footprint range")
        footprints.append(mask)

    if (
        not isinstance(bits_text, str)
        or len(bits_text) != 95
        or bits_text != bits_text.lower()
        or any(character not in "0123456789abcdef" for character in bits_text)
    ):
        raise ValueError("outside bits")
    outside_bits = int(bits_text, 16)
    if outside_bits >= 1 << len(OUTSIDE_PAIRS):
        raise ValueError("outside bits range")
    outside_edges = frozenset(
        pair for rank, pair in enumerate(OUTSIDE_PAIRS) if outside_bits >> rank & 1
    )

    if not isinstance(pivot, str) or len(pivot) < 2 or pivot[0] not in "CD":
        raise ValueError("pivot")
    pivot_index = int(pivot[1:])
    if pivot[0] == "C":
        if pivot_index not in core_e:
            raise AssertionError("unmarked core pivot")
        pivot_global = CORE[pivot_index]
    else:
        if pivot_index not in outside_e:
            raise AssertionError("unmarked outside pivot")
        pivot_global = OUTSIDE[pivot_index]

    def red(i: int, j: int) -> bool:
        if i > j:
            i, j = j, i
        if (i, j) == (U, V):
            return True
        if i in (U, V) and j in CORE:
            return True
        if i in CORE and j in CORE:
            return core_edge(i - CORE[0], j - CORE[0])
        if i == U and j in OUTSIDE:
            return j - OUTSIDE[0] in A_LOCAL
        if i == V and j in OUTSIDE:
            return j - OUTSIDE[0] in B_LOCAL
        if i in CORE and j in OUTSIDE:
            return bool(footprints[j - OUTSIDE[0]] >> (i - CORE[0]) & 1)
        if i in OUTSIDE and j in OUTSIDE:
            return (i - OUTSIDE[0], j - OUTSIDE[0]) in outside_edges
        raise AssertionError((i, j))

    marked = frozenset(CORE[i] for i in core_e) | frozenset(
        OUTSIDE[x] for x in outside_e
    )
    neighborhoods = tuple(
        frozenset(other for other in range(N) if other != vertex and red(vertex, other))
        for vertex in range(N)
    )
    degrees = tuple(map(len, neighborhoods))
    expected_degrees = tuple(20 if vertex in marked else 21 for vertex in range(N))
    if degrees != expected_degrees:
        raise AssertionError("degree sequence")
    incidences = tuple(len(neighborhood & marked) for neighborhood in neighborhoods)
    expected_incidences = tuple(8 if vertex == pivot_global else 6 for vertex in range(N))
    if incidences != expected_incidences:
        raise AssertionError("E incidence")

    def local_triangle(vertex: int, color: bool) -> int:
        neighbors = [
            other for other in range(N) if other != vertex and red(vertex, other) == color
        ]
        return sum(
            red(i, j) == color for i, j in itertools.combinations(neighbors, 2)
        )

    local_triangles = tuple(
        (local_triangle(vertex, True), local_triangle(vertex, False))
        for vertex in range(N)
    )
    expected_triangles = tuple(
        (
            93 if vertex in marked else 100,
            105 if vertex == pivot_global else 107 if vertex in marked else 100,
        )
        for vertex in range(N)
    )
    if local_triangles[:15] != expected_triangles[:15]:
        raise AssertionError("anchor/core triangles")
    outside_exact = tuple(
        vertex
        for vertex in OUTSIDE
        if local_triangles[vertex] == expected_triangles[vertex]
    )
    if outside_exact != (35, 36, 40):
        raise AssertionError(("outside exact set", outside_exact))
    deviations = tuple(
        (
            vertex,
            local_triangles[vertex][0] - expected_triangles[vertex][0],
            local_triangles[vertex][1] - expected_triangles[vertex][1],
        )
        for vertex in OUTSIDE
        if local_triangles[vertex] != expected_triangles[vertex]
    )
    deviation_hash = hashlib.sha256(
        json.dumps(deviations, separators=(",", ":")).encode()
    ).hexdigest()

    global_triangles = (
        sum(values[0] for values in local_triangles) // 3,
        sum(values[1] for values in local_triangles) // 3,
    )
    if global_triangles != (1403, 1463):
        raise AssertionError(("global triangles", global_triangles))

    core_edges = tuple(
        pair for pair in itertools.combinations(range(CORE_ORDER), 2) if core_edge(*pair)
    )
    independent_pairs = tuple(
        pair for pair in itertools.combinations(range(CORE_ORDER), 2) if not core_edge(*pair)
    )
    independent_triples = tuple(
        triple
        for triple in itertools.combinations(range(CORE_ORDER), 3)
        if all(not core_edge(i, j) for i, j in itertools.combinations(triple, 2))
    )
    if (len(core_edges), len(independent_pairs), len(independent_triples)) != (26, 52, 78):
        raise AssertionError("core census")

    x_sum = sum(footprints[x].bit_count() for x in A_LOCAL | B_LOCAL)
    p_sum = sum(
        sum(mask >> i & 1 and mask >> j & 1 for i, j in core_edges)
        for mask in footprints
    )
    q_sum = sum(
        sum(not (mask >> i & 1) and not (mask >> j & 1) for i, j in independent_pairs)
        for mask in footprints
    )
    if (x_sum, p_sum, q_sum) != (96, 231, 294):
        raise AssertionError(("footprint statistics", x_sum, p_sum, q_sum))

    red_outside_triangles = blue_outside_triangles = 0
    for triple in itertools.combinations(range(OUTSIDE_ORDER), 3):
        colors = tuple(
            pair in outside_edges for pair in itertools.combinations(triple, 2)
        )
        red_outside_triangles += all(colors)
        blue_outside_triangles += not any(colors)
    if (red_outside_triangles, blue_outside_triangles) != (360, 413):
        raise AssertionError("outside triangle balance")

    forced_red = forced_blue = 0
    for x, y in OUTSIDE_PAIRS:
        union = footprints[x] | footprints[y]
        misses_triple = any(
            all(not (union >> h & 1) for h in triple)
            for triple in independent_triples
        )
        if misses_triple:
            forced_red += 1
            if (x, y) not in outside_edges:
                raise AssertionError(("forced red", x, y))
        same_anchor_cell = (x in A_LOCAL and y in A_LOCAL) or (
            x in B_LOCAL and y in B_LOCAL
        )
        intersection = footprints[x] & footprints[y]
        contains_edge = any(
            intersection >> i & 1 and intersection >> j & 1
            for i, j in core_edges
        )
        if same_anchor_cell and contains_edge:
            forced_blue += 1
            if (x, y) in outside_edges:
                raise AssertionError(("forced blue", x, y))
    if (forced_red, forced_blue) != (53, 16):
        raise AssertionError(("forced pair census", forced_red, forced_blue))

    red_edge_loads = [
        sum((footprints[x] >> i & 1) and (footprints[x] >> j & 1) for x in range(28))
        for i, j in core_edges
    ]
    blue_pair_miss_loads = [
        sum(not (footprints[x] >> i & 1) and not (footprints[x] >> j & 1) for x in range(28))
        for i, j in independent_pairs
    ]
    cell_edge_loads = [
        sum((footprints[x] >> i & 1) and (footprints[x] >> j & 1) for x in cell)
        for cell in (A_LOCAL, B_LOCAL)
        for i, j in core_edges
    ]
    triple_miss_loads = [
        sum(all(not (footprints[x] >> i & 1) for i in triple) for x in range(28))
        for triple in independent_triples
    ]
    capacities = (
        max(red_edge_loads),
        max(blue_pair_miss_loads),
        max(cell_edge_loads),
        max(triple_miss_loads),
    )
    if capacities != (12, 8, 3, 3):
        raise AssertionError(("capacity maxima", capacities))

    block_names = ("AA", "AB", "AO", "BB", "BO", "OO")
    blocks = dict.fromkeys(block_names, 0)

    def cell_name(vertex: int) -> str:
        return "A" if vertex < 7 else "B" if vertex < 14 else "O"

    for x, y in outside_edges:
        blocks["".join(sorted((cell_name(x), cell_name(y))))] += 1
    expected_blocks = {"AA": 12, "AB": 18, "AO": 43, "BB": 14, "BO": 41, "OO": 55}
    if blocks != expected_blocks:
        raise AssertionError(("block edges", blocks))

    mono = {count: {"red": 0, "blue": 0} for count in range(6)}
    for five in itertools.combinations(range(N), 5):
        colors = tuple(red(i, j) for i, j in itertools.combinations(five, 2))
        if all(colors) or not any(colors):
            outside_count = sum(vertex in OUTSIDE for vertex in five)
            mono[outside_count]["red" if all(colors) else "blue"] += 1
    expected_mono = {
        0: {"red": 0, "blue": 0},
        1: {"red": 0, "blue": 0},
        2: {"red": 0, "blue": 0},
        3: {"red": 184, "blue": 43},
        4: {"red": 162, "blue": 173},
        5: {"red": 35, "blue": 67},
    }
    if mono != expected_mono:
        raise AssertionError(("K5 census", mono))

    result = {
        "anchor_core_exact_vertices": 15,
        "block_red_edges": blocks,
        "capacity_maxima": {
            "cell_core_edge": capacities[2],
            "core_edge": capacities[0],
            "independent_pair_miss": capacities[1],
            "independent_triple_miss": capacities[3],
        },
        "certificate_sha256": certificate_hash,
        "deviation_sha256": deviation_hash,
        "global_triangles": {"blue": global_triangles[1], "red": global_triangles[0]},
        "monochromatic_K5_by_outside_count": mono,
        "outside_exact_vertices": list(outside_exact),
        "outside_red_edges": len(outside_edges),
        "outside_triangle_counts": {
            "blue": blue_outside_triangles,
            "red": red_outside_triangles,
        },
        "pairwise_forced_colors": {"blue": forced_blue, "red": forced_red},
        "status": "VERIFIED CORE-EXACT C13 RELAXATION SURVIVOR",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
