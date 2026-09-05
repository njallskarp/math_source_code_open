#!/usr/bin/env python3
"""Exact checker for the standard-branch separation family.

Python 3.10+; standard library only.  It checks formula-level certificates at
k=6,7,8,29 and performs exact clique-cover DP for k=6,7,8.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def edge(x: str, y: str) -> frozenset[str]:
    require(x != y, "loops are not edges")
    return frozenset((x, y))


CORE_DELETION_COVERS = {
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


def vertices(k: int) -> tuple[str, ...]:
    require(k >= 6, "the construction requires k>=6")
    return ("v", "w", "p", "q") + tuple(z + str(i) for i in range(2, k) for z in ("a", "b"))


def h_edges(k: int) -> set[frozenset[str]]:
    pairs: list[tuple[str, str]] = [
        ("v", "p"), ("v", "q"), ("p", "q"), ("w", "p"), ("w", "q"),
        ("w", "b2"), ("w", "b3"), ("a2", "b3"), ("a3", "b2"),
        ("q", "a2"), ("q", "a3"),
        ("p", "a4"), ("w", "a5"), ("b4", "b5"),
        ("a2", "a4"), ("a3", "a4"), ("w", "a4"), ("q", "b4"),
    ]
    for i in range(2, k):
        pairs.extend((("v", f"a{i}"), (f"a{i}", f"b{i}")))
    for i in range(6, k):
        pairs.extend((("q", f"b{i}"), ("w", f"a{i}"), ("a2", f"a{i}"),
                      ("a3", f"a{i}"), ("b4", f"a{i}")))
    return {edge(*pair) for pair in pairs}


def is_clique(block: tuple[str, ...] | set[str], edges: set[frozenset[str]]) -> bool:
    return all(edge(x, y) in edges for x, y in combinations(block, 2))


def check_partition(
    cover: tuple[tuple[str, ...], ...], verts: tuple[str, ...], edges: set[frozenset[str]],
    omitted: str | None = None,
) -> None:
    flat = [x for block in cover for x in block]
    target = set(verts) - ({omitted} if omitted else set())
    require(len(flat) == len(set(flat)) and set(flat) == target, f"bad partition omitting {omitted}")
    require(all(is_clique(block, edges) for block in cover), f"nonclique block omitting {omitted}")


def connected(verts: tuple[str, ...], edges: set[frozenset[str]]) -> bool:
    seen = {verts[0]}
    while True:
        grown = seen | {y for x in seen for y in set(verts) - seen if edge(x, y) in edges}
        if grown == seen:
            return len(seen) == len(verts)
        seen = grown


def base_cover(k: int) -> tuple[tuple[str, ...], ...]:
    return (("v",), ("w", "p", "q")) + tuple((f"a{i}", f"b{i}") for i in range(2, k))


def endpoint_cover(k: int) -> tuple[tuple[str, ...], ...]:
    return (("q",), ("v", "p", "a4"), ("w", "a5"), ("a2", "b2"),
            ("a3", "b3"), ("b4", "b5")) + tuple((f"a{i}", f"b{i}") for i in range(6, k))


def deletion_cover(k: int, omitted: str) -> tuple[tuple[str, ...], ...]:
    tails = tuple((f"a{i}", f"b{i}") for i in range(6, k))
    if omitted in CORE_DELETION_COVERS:
        return CORE_DELETION_COVERS[omitted] + tails
    index = int(omitted[1:])
    other_tails = tuple(block for block in tails if index not in {int(block[0][1:])})
    if omitted.startswith("a"):
        return CORE_DELETION_COVERS["q"] + (("q", f"b{index}"),) + other_tails
    return CORE_DELETION_COVERS["v"] + (("v", f"a{index}"),) + other_tails


def overlay_components(
    left: tuple[tuple[str, ...], ...], right: tuple[tuple[str, ...], ...], verts: tuple[str, ...]
) -> list[dict[str, object]]:
    left_of = {x: i for i, block in enumerate(left) for x in block}
    right_of = {x: i for i, block in enumerate(right) for x in block}
    nodes = {("L", i) for i in range(len(left))} | {("R", i) for i in range(len(right))}
    incidence = {x: (("L", left_of[x]), ("R", right_of[x])) for x in verts}
    remaining = set(nodes)
    result = []
    while remaining:
        seen = {min(remaining)}
        while True:
            grown = seen | {node for endpoints in incidence.values()
                            if endpoints[0] in seen or endpoints[1] in seen for node in endpoints}
            if grown == seen:
                break
            seen = grown
        remaining -= seen
        labels = sorted(x for x, endpoints in incidence.items() if endpoints[0] in seen)
        result.append({"left": sum(side == "L" for side, _ in seen),
                       "right": sum(side == "R" for side, _ in seen),
                       "labels": labels})
    return sorted(result, key=lambda item: (len(item["labels"]), item["labels"]))


def clique_cover_number(verts: tuple[str, ...], edges: set[frozenset[str]], omitted: str | None = None) -> int:
    active = tuple(x for x in verts if x != omitted)
    n = len(active)
    by_pivot: list[list[int]] = [[] for _ in range(n)]
    for mask in range(1, 1 << n):
        inds = [i for i in range(n) if mask >> i & 1]
        if all(edge(active[i], active[j]) in edges for i, j in combinations(inds, 2)):
            for i in inds:
                by_pivot[i].append(mask)
    inf = n + 1
    dp = [inf] * (1 << n)
    dp[0] = 0
    for mask in range(1, 1 << n):
        pivot = (mask & -mask).bit_length() - 1
        dp[mask] = 1 + min(dp[mask ^ c] for c in by_pivot[pivot] if c & mask == c)
    return dp[-1]


def verify(k: int, exhaustive: bool) -> dict[str, object]:
    verts = vertices(k)
    h = h_edges(k)
    all_edges = {edge(x, y) for x, y in combinations(verts, 2)}
    g = all_edges - h
    require(len(verts) == 2 * k and len(h) == 7 * k - 16, f"size formula failed at k={k}")
    require(connected(verts, h), f"H disconnected at k={k}")
    check_partition(base_cover(k), verts, h)
    check_partition(endpoint_cover(k), verts, h)
    for x in verts:
        cover = deletion_cover(k, x)
        require(len(cover) == k - 1, f"wrong deletion-cover size at k={k}, x={x}")
        check_partition(cover, verts, h, x)

    degrees_h = {x: sum(x in e for e in h) for x in verts}
    require(all(degrees_h[x] == k for x in ("v", "w", "q")), f"named low degrees failed at k={k}")
    if k >= 7:
        require({x for x, d in degrees_h.items() if d == k} == {"v", "w", "q"},
                f"unexpected low vertex at k={k}")
        require(max(degrees_h.values()) == k, f"minimum-degree certificate failed at k={k}")

    bset = {"w"} | {f"b{i}" for i in range(2, k)}
    j_edges = {e for e in h if e <= bset}
    require(j_edges == {edge("w", "b2"), edge("w", "b3"), edge("b4", "b5")},
            f"wrong representative graph at k={k}")
    for i in (2, 3):
        available = [s for s in ("p", "q") if all(edge(*xy) in g for xy in
                     (("w", f"a{i}"), (f"a{i}", s), (s, f"b{i}")))]
        require(available == ["p"], f"wrong availability at k={k}, i={i}")

    components = overlay_components(base_cover(k), endpoint_cover(k), verts)
    exceptional = [c for c in components if len(c["labels"]) == 8]
    require(len(exceptional) == 1 and exceptional[0]["left"] == exceptional[0]["right"] == 4,
            f"wrong exceptional overlay at k={k}")
    require(exceptional[0]["labels"] == ["a4", "a5", "b4", "b5", "p", "q", "v", "w"],
            f"wrong exceptional labels at k={k}")

    triangles = [set(block) for block in combinations(verts, 3) if is_clique(block, h)]
    expected = [
        {"v", "p", "q"}, {"v", "p", "a4"}, {"v", "q", "a2"}, {"v", "q", "a3"},
        {"v", "a2", "a4"}, {"v", "a3", "a4"}, {"w", "p", "q"}, {"w", "p", "a4"},
    ] + [{"v", a, f"a{i}"} for i in range(6, k) for a in ("a2", "a3")]
    require({frozenset(t) for t in triangles} == {frozenset(t) for t in expected},
            f"triangle classification failed at k={k}")
    require(not any(is_clique(block, h) for block in combinations(verts, 4)), f"K4 found at k={k}")
    require(max(sum(not (a & b) for b in triangles) for a in triangles) >= 1,
            f"no disjoint triangles at k={k}")
    disjoint_pairs = [(a, b) for a, b in combinations(triangles, 2) if not a & b]
    require(len(disjoint_pairs) == 4 * (k - 5), f"wrong disjoint-triangle count at k={k}")
    require(not any(not (a & b or a & c or b & c) for a, b, c in combinations(triangles, 3)),
            f"three disjoint triangles found at k={k}")
    for t1, t2 in disjoint_pairs:
        residual = set(verts) - t1 - t2
        isolated = [x for x in residual if not any(edge(x, y) in h for y in residual - {x})]
        twin_obstruction = [
            (x, y) for x, y in combinations(residual, 2) if edge(x, y) not in h
            and len({z for z in residual - {x, y} if edge(x, z) in h or edge(y, z) in h}) < 2
        ]
        require(bool(isolated or twin_obstruction), f"missing residual matching obstruction at k={k}")

    aset = {"p", "q"} | {f"a{i}" for i in range(2, k)}
    require({x for x in aset if edge("w", x) in g} == {"a2", "a3"},
            f"wrong internal G-neighbours of w at k={k}")
    for start, other in (("a2", "a3"), ("a3", "a2")):
        allowed = aset - {"a2", "a3"}
        require({x for x in allowed if edge(start, x) in g} == {"p", "a5"},
                f"wrong second-step cut at k={k}, start={start}")
        require(all(edge(start, target) in h for target in ("b2", "b3")),
                f"a center path terminates too soon at k={k}")
    remaining_internal = aset - {"a2", "a3", "p", "a5"}
    require(all(edge("b4", x) in h for x in remaining_internal) and edge("b4", "b5") in h,
            f"external-demand cut failed at k={k}")

    branches = {"v", "p", "a2", "b2", "b4", "b5"} | {f"b{i}" for i in range(6, k)}
    shifted_paths = (("v", "b3", "p"), ("v", "w", "a2"),
                     ("a2", "a5", "b2"), ("b4", "a3", "b5"))
    missing = {edge(x, y) for x, y in combinations(sorted(branches), 2) if edge(x, y) in h}
    require(missing == {edge(path[0], path[-1]) for path in shifted_paths},
            f"wrong shifted branch nonedges at k={k}")
    interiors = [set(path[1:-1]) for path in shifted_paths]
    require(all(all(edge(x, y) in g for x, y in zip(path, path[1:])) for path in shifted_paths),
            f"shifted path missing at k={k}")
    require(not set().union(*interiors) & branches and sum(map(len, interiors)) == len(set().union(*interiors)),
            f"shifted path interiors fail at k={k}")

    if exhaustive:
        require(clique_cover_number(verts, h) == k, f"exact theta failed at k={k}")
        require(all(clique_cover_number(verts, h, x) == k - 1 for x in verts),
                f"exact deletion theta failed at k={k}")

    return {
        "k": k,
        "vertices": len(verts),
        "edges_h": len(h),
        "edges_g": len(g),
        "triangles": len(triangles),
        "disjoint_triangle_pairs": len(disjoint_pairs),
        "low_vertices": sorted(x for x, d in degrees_h.items() if d == k),
        "canonical_branch_linkage": False,
        "shifted_tk": True,
        "exhaustive_theta": exhaustive,
    }


def main() -> None:
    summaries = [verify(k, k <= 8) for k in (6, 7, 8, 29)]
    payload = json.dumps(summaries, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest()
    for item in summaries:
        mode = "exact-dp" if item["exhaustive_theta"] else "structural-certificate"
        print(f"k={item['k']} n={item['vertices']} eH={item['edges_h']} eG={item['edges_g']} "
              f"canonical=no shifted_TK=yes theta_check={mode}")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
