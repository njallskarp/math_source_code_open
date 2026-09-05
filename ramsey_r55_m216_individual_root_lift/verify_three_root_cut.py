#!/usr/bin/env python3
"""Exact solver-free verifier for the M=216 three-root cell cut."""

from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT_SHA256 = "61c0953591ffe94ee2d61efeeab5f9d60cbc5f6278f1cc4fa7ab468a66968372"


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


@lru_cache(None)
def upper(red, blue):
    if min(red, blue) == 1:
        return 1
    left, right = upper(red - 1, blue), upper(red, blue - 1)
    return left + right - int(left % 2 == right % 2 == 0)


def decode_core(order, mask):
    pairs = tuple(combinations(range(order), 2))
    require(type(mask) is int and 0 <= mask < 1 << len(pairs), "core mask range")
    adjacency = [set() for _ in range(order)]
    for bit, (left, right) in enumerate(pairs):
        if mask >> bit & 1:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return tuple(frozenset(row) for row in adjacency)


def clique(adjacency, vertices, red):
    return all((right in adjacency[left]) == red for left, right in combinations(vertices, 2))


def rooted_side(adjacency, cells, red_root, blue_root):
    red = frozenset(red_root)
    blue = frozenset(blue_root)
    require(red and not red & blue, "disjoint nonempty red root")
    require(clique(adjacency, red, True), "red root clique")
    require(clique(adjacency, blue, False), "blue root clique")
    fixed = frozenset(
        vertex for vertex in range(len(adjacency)) if vertex not in red | blue
        and red <= adjacency[vertex] and not blue & adjacency[vertex]
    )
    selected = frozenset(
        mask for mask in cells
        if all(mask >> vertex & 1 for vertex in red)
        and all(not (mask >> vertex & 1) for vertex in blue)
    )
    return fixed, selected, 5 - len(red), 5 - len(blue)


def verify_document(document):
    require(document["format"] == "r55-double19-external-root-lift-v1", "input format")
    record = document["record"]
    require(record["M"] == 216 and record["core_mask"] == 409383, "source witness")
    require(record["exceptional_degrees"] == [19, 19, 20, 20, 20, 20, 20], "profile")
    cells = dict(record["cells"])
    require(sum(cells.values()) == 36 and len(cells) == 19, "complete cell vector")
    edge_counts = {
        (left, right): value for left, right, value in document["aggregate_edges"]
    }

    adjacency = decode_core(7, record["core_mask"])
    blue_root = (0, 4)
    definitions = (
        ("VW", (6,), frozenset((70, 74, 98, 108)), 7),
        ("UV", (2, 3), frozenset((14, 108)), 5),
        ("UW", (1,), frozenset((14, 70, 74, 98)), 8),
    )
    sides = {}
    for name, red_root, expected_cells, expected_order in definitions:
        fixed, selected, p, q = rooted_side(adjacency, cells, red_root, blue_root)
        require(not fixed, f"{name} has no fixed exceptional vertices")
        require(selected == expected_cells, f"{name} selected signature cells")
        order = sum(cells[mask] for mask in selected)
        require(order == expected_order, f"{name} side order")
        sides[name] = (selected, order, p, q)

    U = frozenset((14,))
    V = frozenset((108,))
    W = frozenset((70, 74, 98))
    require(cells[14] == 3 and cells[108] == 2, "U and V orders")
    require(sum(cells[mask] for mask in W) == 5, "W order")
    require(sides["VW"][0] == V | W, "VW partition")
    require(sides["UV"][0] == U | V, "UV partition")
    require(sides["UW"][0] == U | W, "UW partition")
    require(all(not (14 >> vertex & 1) for vertex in blue_root), "U is blue to the common blue root")
    require(all(14 >> vertex & 1 for vertex in (2, 3)), "U is red to the UV red root")
    require(14 >> 1 & 1, "U is red to the UW red root")
    require(not (14 >> 6 & 1), "U lies outside the VW rooted side")

    # Root VW is a (4,3)-side of order 7.  A U vertex is blue to B,
    # so it has at most U(4,2)-1=3 blue neighbors, hence at least 4 red.
    lower_vw = sides["VW"][1] - (upper(4, 2) - 1)
    require(lower_vw == 4, "VW red-degree lower bound")

    # Root UV is a (3,3)-side of order 5 and U lies inside it.  The red
    # and blue degree caps are both 2, hence the red degree is exactly 2.
    uv_red_cap = upper(2, 3) - 1
    uv_blue_cap = upper(3, 2) - 1
    require(uv_red_cap == uv_blue_cap == 2, "UV exact degree")
    require(sides["UV"][1] - 1 - uv_blue_cap == uv_red_cap, "UV complementary bounds meet")

    # Root UW is a (4,3)-side of order 8 and U lies inside it.
    upper_uw = upper(3, 3) - 1
    require(upper_uw == 5, "UW red-degree upper bound")

    # Put a=d_R(u,U), v=d_R(u,V), w=d_R(u,W).  The three root bounds give
    # a+v=2, v+w>=4, a+w<=5.  Therefore
    # 2a=(a+v)+(a+w)-(v+w)<=2+5-4=3, and integrality gives a<=1.
    twice_a_bound = uv_red_cap + upper_uw - lower_vw
    require(twice_a_bound == 3, "three-root combination")
    individual_a_cap = twice_a_bound // 2
    require(individual_a_cap == 1, "integral rounding")
    aggregate_internal_cap = cells[14] * individual_a_cap // 2
    require(aggregate_internal_cap == 1, "handshaking cell cut")

    recorded_internal_edges = edge_counts[(14, 14)]
    require(recorded_internal_edges == 2, "height-2703 internal U quota")
    require(recorded_internal_edges > aggregate_internal_cap, "three-root cut contradiction")

    # Sharp abstract boundary: with one U-edge, take U-degrees a=(1,1,0),
    # V-degrees (1,1,2), and W-degrees (3,3,2).
    sharp = ((1, 1, 3), (1, 1, 3), (0, 2, 2))
    for a, v, w in sharp:
        require(a + v == 2 and v + w >= 4 and a + w <= 5, "sharp degree fixture")
    require(sum(a for a, _, _ in sharp) == 2, "sharp fixture has one internal edge")

    return {
        "cell_order": cells[14],
        "recorded_internal_edges": recorded_internal_edges,
        "cut_cap": aggregate_internal_cap,
        "side_orders": tuple(sides[name][1] for name in ("VW", "UV", "UW")),
    }


def mutation_tests(document):
    mutants = [deepcopy(document) for _ in range(4)]
    mutants[0]["record"]["core_mask"] ^= 1
    mutants[1]["record"]["cells"][1][1] += 1
    for triple in mutants[2]["aggregate_edges"]:
        if triple[:2] == [14, 14]:
            triple[2] = 1
            break
    mutants[3]["record"]["M"] += 1
    for mutant in mutants:
        try:
            verify_document(mutant)
        except (KeyError, ValueError):
            continue
        raise ValueError("altered input accepted")


def main():
    input_path = HERE / "AGGREGATE_INPUT.json"
    raw = input_path.read_bytes()
    require(sha256(raw).hexdigest() == INPUT_SHA256, "height-2703 source hash")
    document = json.loads(raw)
    result = verify_document(document)
    mutation_tests(document)
    print("PASS pinned height-2703 aggregate witness and literal exceptional core")
    print(f"PASS three rooted sides have orders {result['side_orders']} and signature partitions VW, UV, UW")
    print("PASS pointwise bounds a+v=2, v+w>=4, a+w<=5 imply integral a<=1")
    print(f"PASS handshaking cut z_14,14<={result['cut_cap']} contradicts recorded value {result['recorded_internal_edges']}")
    print("PASS sharp abstract one-internal-edge degree fixture")
    print("PASS four altered inputs rejected")
    print("THEOREM the height-2703 M=216 aggregate pseudomodel has no pointwise external-root lift")
    print("SCOPE cuts this pseudomodel, not the complete M=216 degree profile")


if __name__ == "__main__":
    main()
