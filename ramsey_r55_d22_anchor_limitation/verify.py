#!/usr/bin/env python3
"""Exact checker for the d=22 one-anchor limitation witness."""

from __future__ import annotations

import base64
from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
CELL_ORDER = (
    (1, 1, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def edge(left: int, right: int) -> tuple[int, int]:
    require(left != right, "no loops")
    return (left, right) if left < right else (right, left)


def decode_graph6(record: bytes) -> tuple[int, set[tuple[int, int]]]:
    data = record.strip()
    require(bool(data) and not data.startswith(b">"), "one small graph6 record")
    n = data[0] - 63
    require(0 <= n <= 62, "small graph6 order")
    bits: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        require(0 <= value < 64, "graph6 alphabet")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    require(len(bits) >= n * (n - 1) // 2, "complete graph6 payload")
    edges: set[tuple[int, int]] = set()
    position = 0
    for right in range(1, n):
        for left in range(right):
            if bits[position]:
                edges.add((left, right))
            position += 1
    return n, edges


def degree_sequence(n: int, edges: Iterable[tuple[int, int]]) -> list[int]:
    degrees = [0] * n
    for left, right in edges:
        require(0 <= left < right < n, "canonical simple edge")
        degrees[left] += 1
        degrees[right] += 1
    return degrees


def has_clique(
    vertices: Iterable[int],
    edges: set[tuple[int, int]],
    order: int,
    *,
    complement: bool = False,
) -> bool:
    for subset in itertools.combinations(vertices, order):
        flags = [edge(left, right) in edges for left, right in itertools.combinations(subset, 2)]
        if (not complement and all(flags)) or (complement and not any(flags)):
            return True
    return False


def load_data() -> dict[str, Any]:
    return json.loads((HERE / "ANCHOR_DATA.json").read_text(encoding="utf-8"))


def construct(
    data: dict[str, Any],
) -> tuple[set[tuple[int, int]], set[tuple[int, int]], set[tuple[int, int]]]:
    require(data["format"] == "r55-d22-anchor-limitation-v1", "data format")
    red_spec = data["red_anchor_core"]
    blue_spec = data["blue_anchor_core"]
    cross_spec = data["red_cross_rule"]

    n_a, a_edges = decode_graph6(
        base64.b64decode(red_spec["parent_graph6_base64"], validate=True)
    )
    require(n_a == red_spec["order"] == 22, "red anchor core order")
    require(len(a_edges) == red_spec["parent_edges"] == 114, "red parent edge count")
    for raw in red_spec["delete_edges"]:
        deleted = edge(*raw)
        require(deleted in a_edges, "listed red-core deletion exists")
        a_edges.remove(deleted)

    n_b, blue_b_edges = decode_graph6(
        base64.b64decode(blue_spec["graph6_base64"], validate=True)
    )
    require(n_b == blue_spec["order"] == 20, "blue anchor core order")
    require(len(blue_b_edges) == blue_spec["edges"] == 100, "blue core edge count")
    require(cross_spec["modulus"] == 20 and cross_spec["width"] == 10, "cross rule")

    red: set[tuple[int, int]] = set()
    anchor = 0
    a_vertices = range(1, 23)
    b_vertices = range(23, 43)

    for vertex in a_vertices:
        red.add(edge(anchor, vertex))
    for left, right in a_edges:
        red.add(edge(1 + left, 1 + right))
    for left, right in itertools.combinations(range(20), 2):
        if (left, right) not in blue_b_edges:
            red.add(edge(23 + left, 23 + right))
    for i in range(22):
        for j in range(20):
            if (j - i) % 20 < 10:
                red.add(edge(1 + i, 23 + j))

    return red, a_edges, blue_b_edges


def count_monochromatic_fives(
    red: set[tuple[int, int]],
) -> tuple[int, int, int, int]:
    red_count = blue_count = red_anchor = blue_anchor = 0
    for subset in itertools.combinations(range(43), 5):
        flags = [edge(left, right) in red for left, right in itertools.combinations(subset, 2)]
        if all(flags):
            red_count += 1
            red_anchor += int(0 in subset)
        elif not any(flags):
            blue_count += 1
            blue_anchor += int(0 in subset)
    return red_count, blue_count, red_anchor, blue_anchor


def joint_partner_audit(
    red: set[tuple[int, int]],
    a_edges: set[tuple[int, int]],
) -> tuple[int, int, Counter[int], str]:
    local_degrees = degree_sequence(22, a_edges)
    high = [vertex for vertex, degree in enumerate(local_degrees) if degree >= 10]
    require(len(high) >= 5, "five high-codegree partners")
    require(
        not has_clique(high, a_edges, 5, complement=True),
        "every five high partners contain an edge",
    )

    global_degrees = degree_sequence(43, red)
    rows = [
        "v\tw\tp\tr\ta\tb\tq_vw\tk\t111\t110\t101\t011\t100\t010\t001\t000"
    ]
    k_distribution: Counter[int] = Counter()
    high_edges = 0
    for v, w in itertools.combinations(high, 2):
        if edge(v, w) not in a_edges:
            continue
        high_edges += 1
        gv, gw = 1 + v, 1 + w
        p, r = global_degrees[gv], global_degrees[gw]
        a, b = local_degrees[v], local_degrees[w]
        q_vw = sum(
            edge(gv, x) in red and edge(gw, x) in red
            for x in range(43)
            if x not in (gv, gw)
        )
        k = sum(
            edge(0, x) in red and edge(gv, x) in red and edge(gw, x) in red
            for x in range(43)
            if x not in (0, gv, gw)
        )
        require(k <= 4, "triple common neighborhood cap")
        k_distribution[k] += 1

        formula = (
            k,
            a - 1 - k,
            b - 1 - k,
            q_vw - 1 - k,
            22 - a - b + k,
            p - a - q_vw + k,
            r - b - q_vw + k,
            43 - 22 - p - r + a + b + q_vw - k,
        )
        require(min(formula) >= 0 and sum(formula) == 40, "nonnegative eight-cell formula")
        actual = Counter()
        for x in range(43):
            if x in (0, gv, gw):
                continue
            signature = (
                int(edge(0, x) in red),
                int(edge(gv, x) in red),
                int(edge(gw, x) in red),
            )
            actual[signature] += 1
        require(tuple(actual[key] for key in CELL_ORDER) == formula, "eight-cell identity")
        rows.append("\t".join(map(str, (v, w, p, r, a, b, q_vw, k, *formula))))

    require(high_edges > 0, "an eligible high-partner edge")
    payload = ("\n".join(rows) + "\n").encode("ascii")
    return len(high), high_edges, k_distribution, sha256(payload).hexdigest()


def audit(data: dict[str, Any]) -> dict[str, Any]:
    red, a_edges, blue_b_edges = construct(data)
    require(len(red) == 440, "global red edge count")

    require(len(a_edges) == 108, "red anchor core has 108 edges")
    require(
        data["red_anchor_core"]["extremal_edge_bound"] - len(a_edges) == 6,
        "red anchor deficiency six",
    )
    require(not has_clique(range(22), a_edges, 4), "red A is K4-free")
    require(not has_clique(range(22), a_edges, 5, complement=True), "red A has alpha below five")
    require(not has_clique(range(20), blue_b_edges, 4), "blue B is K4-free")
    require(
        not has_clique(range(20), blue_b_edges, 5, complement=True),
        "blue B has alpha below five",
    )

    red_degrees = degree_sequence(43, red)
    blue_degrees = [42 - degree for degree in red_degrees]
    require(Counter(red_degrees) == Counter({19: 7, 20: 10, 21: 25, 22: 1}), "red degrees")
    require(Counter(blue_degrees) == Counter({20: 1, 21: 25, 22: 10, 23: 7}), "blue degrees")
    require(red_degrees[0] == 22 and blue_degrees[0] == 20, "anchor degree split")

    red_fives, blue_fives, red_anchor, blue_anchor = count_monochromatic_fives(red)
    require((red_anchor, blue_anchor) == (0, 0), "no monochromatic K5 through anchor")
    require((red_fives, blue_fives) == (206, 1536), "full monochromatic K5 counts")

    high, high_edges, k_distribution, cell_hash = joint_partner_audit(red, a_edges)
    require(high == 18 and high_edges == 73, "high-partner census")
    require(k_distribution == Counter({2: 4, 3: 34, 4: 35}), "triple-intersection census")
    return {
        "cell_hash": cell_hash,
        "high": high,
        "high_edges": high_edges,
        "k_distribution": k_distribution,
        "red_fives": red_fives,
        "blue_fives": blue_fives,
    }


def main() -> None:
    result = audit(load_data())
    print("PASS anchor blocks A=22 B=20 red_A_edges=108 deficiency=6 blue_B_edges=100")
    print("PASS degree box red=19^7,20^10,21^25,22 blue=20,21^25,22^10,23^7")
    print("PASS no monochromatic K5 through anchor=0")
    print("PASS joint partners high=18 high_edges=73 triple_k=2:4,3:34,4:35")
    print(f"TRIANGLE_CELL_SHA256 {result['cell_hash']}")
    print(
        "PASS full coloring monochromatic K5 "
        f"red={result['red_fives']} blue={result['blue_fives']} all_avoid_anchor=yes"
    )
    print("SCOPE exact one-anchor limitation witness; not an R(5,5;43) graph")


if __name__ == "__main__":
    main()
