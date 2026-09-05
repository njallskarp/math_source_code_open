#!/usr/bin/env python3
"""Verify the c=13 outside-triangle balance certificate from definitions."""

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

    anchor_triangles = tuple(
        local_triangle(vertex, color)
        for vertex in (U, V)
        for color in (True, False)
    )
    if anchor_triangles != (100, 100, 100, 100):
        raise AssertionError(("anchor triangles", anchor_triangles))

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

    k = len(core_e)
    delta = int(pivot[0] == "C")
    x_sum = sum(footprints[x].bit_count() for x in A_LOCAL | B_LOCAL)
    p_sum = sum(
        sum(mask >> i & 1 and mask >> j & 1 for i, j in core_edges)
        for mask in footprints
    )
    q_sum = sum(
        sum(not (mask >> i & 1) and not (mask >> j & 1) for i, j in independent_pairs)
        for mask in footprints
    )

    red_outside_triangles = blue_outside_triangles = 0
    for triple in itertools.combinations(range(OUTSIDE_ORDER), 3):
        colors = tuple(
            pair in outside_edges for pair in itertools.combinations(triple, 2)
        )
        red_outside_triangles += all(colors)
        blue_outside_triangles += not any(colors)
    target_red = 33 + 7 * k + x_sum + p_sum
    target_blue = 119 - 7 * k + 2 * delta + q_sum
    if (target_red, target_blue) != (360, 413):
        raise AssertionError(("balance target", target_red, target_blue))
    if (red_outside_triangles, blue_outside_triangles) != (318, 455):
        raise AssertionError(
            ("outside triangles", red_outside_triangles, blue_outside_triangles)
        )
    if target_red + target_blue != red_outside_triangles + blue_outside_triangles:
        raise AssertionError("monochromatic sum")

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
        raise AssertionError(("capacities", capacities))

    mono = {count: {"red": 0, "blue": 0} for count in range(6)}
    for five in itertools.combinations(range(N), 5):
        colors = tuple(red(i, j) for i, j in itertools.combinations(five, 2))
        if all(colors) or not any(colors):
            outside_count = sum(vertex in OUTSIDE for vertex in five)
            mono[outside_count]["red" if all(colors) else "blue"] += 1
    if any(mono[count][color] for count in (0, 1, 2) for color in ("red", "blue")):
        raise AssertionError(("pairwise scope", mono))

    result = {
        "E_core": k,
        "P": p_sum,
        "Q": q_sum,
        "X": x_sum,
        "actual_outside_triangles": {
            "blue": blue_outside_triangles,
            "red": red_outside_triangles,
        },
        "balance_discrepancy": {
            "blue": blue_outside_triangles - target_blue,
            "red": red_outside_triangles - target_red,
        },
        "capacity_maxima": {
            "cell_core_edge": capacities[2],
            "core_edge": capacities[0],
            "independent_pair_miss": capacities[1],
            "independent_triple_miss": capacities[3],
        },
        "certificate_sha256": certificate_hash,
        "delta": delta,
        "monochromatic_K5_by_outside_count": mono,
        "outside_red_edges": len(outside_edges),
        "status": "VERIFIED C13 OUTSIDE-TRIANGLE BALANCE OBSTRUCTION",
        "target_outside_triangles": {"blue": target_blue, "red": target_red},
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
