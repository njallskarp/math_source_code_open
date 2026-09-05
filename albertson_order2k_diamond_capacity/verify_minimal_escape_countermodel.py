#!/usr/bin/env python3
"""Exact checker for the minimal endpoint-escape countermodel.

Python 3.10+; standard library only.  All graph and clique-cover calculations
use finite sets and integer bit masks.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations


VERTICES = ("v", "w", "p", "q", "a2", "b2", "a3", "b3", "a4", "b4", "a5", "b5")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def edge(x: str, y: str) -> frozenset[str]:
    require(x != y, "loops are not graph edges")
    return frozenset((x, y))


H_EDGES = {
    edge(*xy)
    for xy in (
        ("v", "p"), ("v", "q"), ("p", "q"), ("w", "p"), ("w", "q"),
        ("v", "a2"), ("a2", "b2"), ("v", "a3"), ("a3", "b3"),
        ("v", "a4"), ("a4", "b4"), ("v", "a5"), ("a5", "b5"),
        ("w", "b2"), ("w", "b3"), ("a2", "b3"), ("a3", "b2"),
        ("q", "a2"), ("q", "a3"),
        ("p", "a4"), ("w", "a5"), ("b4", "b5"),
    )
}
ALL_EDGES = {edge(x, y) for x, y in combinations(VERTICES, 2)}
G_EDGES = ALL_EDGES - H_EDGES

BASE_COVER = (
    ("v",), ("w", "p", "q"), ("a2", "b2"), ("a3", "b3"),
    ("a4", "b4"), ("a5", "b5"),
)
ENDPOINT_COVER = (
    ("q",), ("v", "p", "a4"), ("w", "a5"), ("a2", "b2"),
    ("a3", "b3"), ("b4", "b5"),
)
DELETION_COVERS = {
    "v": (("w", "p", "q"), ("a2", "b2"), ("a3", "b3"), ("a4", "b4"), ("a5", "b5")),
    "w": (("v", "p", "q"), ("a2", "b2"), ("a3", "b3"), ("a4", "b4"), ("a5", "b5")),
    "p": (("v", "q", "a2"), ("w", "b2"), ("a3", "b3"), ("a4", "b4"), ("a5", "b5")),
    "q": (("v", "p", "a4"), ("w", "a5"), ("a2", "b2"), ("a3", "b3"), ("b4", "b5")),
    "a2": (("v", "p", "q"), ("w", "b2"), ("a3", "b3"), ("a4", "b4"), ("a5", "b5")),
    "b2": (("v", "a2"), ("w", "p", "q"), ("a3", "b3"), ("a4", "b4"), ("a5", "b5")),
    "a3": (("v", "p", "q"), ("w", "b2"), ("a2", "b3"), ("a4", "b4"), ("a5", "b5")),
    "b3": (("v", "a2"), ("w", "p", "q"), ("b2", "a3"), ("a4", "b4"), ("a5", "b5")),
    "a4": (("v", "a5"), ("w", "p", "q"), ("a2", "b2"), ("a3", "b3"), ("b4", "b5")),
    "b4": (("v", "a4"), ("w", "p", "q"), ("a2", "b2"), ("a3", "b3"), ("a5", "b5")),
    "a5": (("v", "a4"), ("w", "p", "q"), ("a2", "b2"), ("a3", "b3"), ("b4", "b5")),
    "b5": (("v", "a5"), ("w", "p", "q"), ("a2", "b2"), ("a3", "b3"), ("a4", "b4")),
}


def is_clique(block: tuple[str, ...], edges: set[frozenset[str]]) -> bool:
    return all(edge(x, y) in edges for x, y in combinations(block, 2))


def check_partition(cover: tuple[tuple[str, ...], ...], omitted: str | None = None) -> None:
    flat = [x for block in cover for x in block]
    target = set(VERTICES) - ({omitted} if omitted is not None else set())
    require(len(flat) == len(set(flat)) and set(flat) == target, f"bad partition omitting {omitted}")
    require(all(is_clique(block, H_EDGES) for block in cover), f"nonclique block omitting {omitted}")


def connected(vertices: set[str], edges: set[frozenset[str]]) -> bool:
    seen = {next(iter(vertices))}
    while True:
        grown = seen | {
            y
            for x in seen
            for y in vertices - seen
            if edge(x, y) in edges
        }
        if grown == seen:
            return seen == vertices
        seen = grown


def clique_cover_number(omitted: str | None = None) -> int:
    verts = tuple(x for x in VERTICES if x != omitted)
    n = len(verts)
    clique_masks = []
    for mask in range(1, 1 << n):
        block = tuple(verts[i] for i in range(n) if mask >> i & 1)
        if is_clique(block, H_EDGES):
            clique_masks.append(mask)
    by_pivot = [[] for _ in range(n)]
    for mask in clique_masks:
        for i in range(n):
            if mask >> i & 1:
                by_pivot[i].append(mask)
    inf = n + 1
    dp = [inf] * (1 << n)
    dp[0] = 0
    for mask in range(1, 1 << n):
        pivot = (mask & -mask).bit_length() - 1
        dp[mask] = 1 + min(dp[mask ^ c] for c in by_pivot[pivot] if c & mask == c)
    return dp[-1]


def overlay_components(
    left: tuple[tuple[str, ...], ...], right: tuple[tuple[str, ...], ...]
) -> list[dict[str, object]]:
    left_of = {x: i for i, block in enumerate(left) for x in block}
    right_of = {x: j for j, block in enumerate(right) for x in block}
    nodes = {("L", i) for i in range(len(left))} | {("R", j) for j in range(len(right))}
    incidence = {x: (("L", left_of[x]), ("R", right_of[x])) for x in VERTICES}
    remaining = set(nodes)
    result = []
    while remaining:
        seen = {min(remaining)}
        while True:
            grown = seen | {
                endpoint
                for _, endpoints in incidence.items()
                if endpoints[0] in seen or endpoints[1] in seen
                for endpoint in endpoints
            }
            if grown == seen:
                break
            seen = grown
        remaining -= seen
        labels = sorted(x for x, endpoints in incidence.items() if endpoints[0] in seen)
        degrees = sorted(
            (sum(node in endpoints for endpoints in incidence.values()) for node in seen),
            reverse=True,
        )
        result.append({
            "left": sum(side == "L" for side, _ in seen),
            "right": sum(side == "R" for side, _ in seen),
            "vertices": labels,
            "degrees": degrees,
        })
    return sorted(result, key=lambda item: (len(item["vertices"]), item["vertices"]))


def main() -> None:
    require(len(H_EDGES) == 22, "wrong H edge count")
    require(connected(set(VERTICES), H_EDGES), "H is disconnected")
    check_partition(BASE_COVER)
    check_partition(ENDPOINT_COVER)
    for omitted, cover in DELETION_COVERS.items():
        check_partition(cover, omitted)

    triangles = sorted(
        tuple(sorted(block))
        for block in combinations(VERTICES, 3)
        if is_clique(block, H_EDGES)
    )
    expected_triangles = sorted(
        tuple(sorted(block))
        for block in (("v", "p", "q"), ("v", "p", "a4"), ("v", "q", "a2"),
                      ("v", "q", "a3"), ("w", "p", "q"))
    )
    require(triangles == expected_triangles, "unexpected triangle list")
    require(not any(is_clique(block, H_EDGES) for block in combinations(VERTICES, 4)), "H contains K4")
    theta = clique_cover_number()
    deletion_theta = {x: clique_cover_number(x) for x in VERTICES}
    require(theta == 6 and set(deletion_theta.values()) == {5}, "criticality calculation failed")

    n_g_v = {x for x in VERTICES if x != "v" and edge("v", x) in G_EDGES}
    require(n_g_v == {"w", "b2", "b3", "b4", "b5"}, "wrong G-neighbourhood of v")
    j_edges = sorted(tuple(sorted(e)) for e in H_EDGES if e <= n_g_v)
    require(j_edges == [("b2", "w"), ("b3", "w"), ("b4", "b5")], "wrong J edges")
    availability = {}
    for i in ("2", "3"):
        availability[i] = sorted(
            s for s in ("p", "q")
            if all(edge(*xy) in G_EDGES for xy in (("w", "a" + i), ("a" + i, s), (s, "b" + i)))
        )
    require(availability == {"2": ["p"], "3": ["p"]}, "wrong availability sets")

    components = overlay_components(BASE_COVER, ENDPOINT_COVER)
    require(components == [
        {"left": 1, "right": 1, "vertices": ["a2", "b2"], "degrees": [2, 2]},
        {"left": 1, "right": 1, "vertices": ["a3", "b3"], "degrees": [2, 2]},
        {"left": 4, "right": 4, "vertices": ["a4", "a5", "b4", "b5", "p", "q", "v", "w"],
         "degrees": [3, 3, 2, 2, 2, 2, 1, 1]},
    ], "wrong overlay decomposition")

    branches = {"v", "w", "b2", "b3", "b4", "b5"}
    special_paths = (("w", "a4", "b2"), ("w", "a2", "a5", "b3"), ("b4", "a3", "b5"))
    missing_branch_edges = {
        edge(x, y) for x, y in combinations(sorted(branches), 2) if edge(x, y) not in G_EDGES
    }
    require(missing_branch_edges == {edge(path[0], path[-1]) for path in special_paths},
            "wrong missing branch edges")
    interiors = [set(path[1:-1]) for path in special_paths]
    require(all(all(edge(x, y) in G_EDGES for x, y in zip(path, path[1:])) for path in special_paths),
            "a displayed subdivision path is not in G")
    require(not (set().union(*interiors) & branches), "a path interior meets the branch set")
    require(sum(map(len, interiors)) == len(set().union(*interiors)), "path interiors are not disjoint")

    certificate = {
        "availability": availability,
        "deletion_theta": deletion_theta,
        "exceptional_overlay": components[-1],
        "h_connected": True,
        "h_edges": len(H_EDGES),
        "j_edges": j_edges,
        "theta_h": theta,
        "tk6_paths": special_paths,
        "triangles_h": triangles,
        "vertices": len(VERTICES),
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest()
    print("vertices=12 edges_H=22 connected_H=yes theta_H=6")
    print("deletion_theta=all_5")
    print("availability=S2:{p};S3:{p}")
    print("overlay_components=2,2,8 exceptional_sides=4x4")
    print("TK6_subdivision=valid")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
