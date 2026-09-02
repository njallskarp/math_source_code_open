#!/usr/bin/env python3
"""Independent exact audit of the rho=21 bichromatic matching-cover witnesses.

The producer's JSON certificates are treated as untrusted input.  This checker
reconstructs clause supports from the incidence multigraph, verifies the four
matching covers, and searches the selected-support graphs definitionally for
forced monochromatic K5s.  It does not import producer code.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys


PIVOT = 41
ORDINARY = range(41)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def endpoint_mask(edge: tuple[int, int]) -> int:
    a, b = edge
    assert 0 <= a < 23 and 0 <= b < 23 and a != b
    return (1 << a) | (1 << b)


def clique5(clauses: list[frozenset[int]]) -> tuple[int, ...] | None:
    adjacency = [0] * 42
    for clause in clauses:
        assert len(clause) == 4
        for a, b in combinations(clause, 2):
            adjacency[a] |= 1 << b
            adjacency[b] |= 1 << a
    for vertices in combinations(range(42), 5):
        if all(adjacency[a] & (1 << b) for a, b in combinations(vertices, 2)):
            return vertices
    return None


def canonical_hash(red: list[frozenset[int]], blue: list[frozenset[int]]) -> str:
    payload = {
        "red": sorted(sorted(c) for c in red),
        "blue": sorted(sorted(c) for c in blue),
    }
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def all_four_matching_count(edge_masks: list[int]) -> int:
    total = 0
    for indices in combinations(range(41), 4):
        used = 0
        for i in indices:
            if used & edge_masks[i]:
                break
            used |= edge_masks[i]
        else:
            total += 1
    return total


def check_kernel(rep: dict, side: set[int]) -> tuple[list[tuple[int, int]], list[int], list[frozenset[int]]]:
    edges = [tuple(x) for x in rep["edges"]]
    assert len(edges) == 41
    masks = [endpoint_mask(e) for e in edges]

    ordinary_degrees = Counter(v for e in edges for v in e)
    assert all(ordinary_degrees[v] == (3 if v in side else 4) for v in range(23))
    multiplicities = Counter(tuple(sorted(e)) for e in edges)
    assert max(multiplicities.values()) <= 3
    assert max((m for e, m in multiplicities.items() if set(e) <= side), default=0) <= 2

    blue: list[frozenset[int]] = []
    for node in range(23):
        support = {i for i, e in enumerate(edges) if node in e}
        if node in side:
            support.add(PIVOT)
        blue.append(frozenset(support))
    assert all(len(c) == 4 for c in blue)
    assert len(set(blue)) == 23
    return edges, masks, blue


def expected_demands(case: str, a: set[int], exceptional: int) -> list[int]:
    demand = [2] * 41
    for x in a:
        demand[x] -= 1
    if case == "exceptional_vertex_in_A":
        assert exceptional in a
        demand[exceptional] += 1
    elif case == "exceptional_vertex_outside_A":
        assert exceptional not in a
        demand[exceptional] += 1
    else:
        raise AssertionError(case)
    assert sum(demand) == 80
    return demand


def audit_survivor(
    survivor: dict,
    rep: dict,
    side: set[int],
    a: set[int],
    cases: dict,
) -> dict:
    edges, masks, blue = check_kernel(rep, side)
    case = survivor["demand_case"]
    exceptional = cases[case]["exceptional_edge_index"]
    target = expected_demands(case, a, exceptional)

    columns = [tuple(sorted(column)) for column in survivor["matchings"]]
    assert len(columns) == 20 and len(set(columns)) == 20
    observed = [0] * 41
    for column in columns:
        assert len(column) == 4 and len(set(column)) == 4
        assert all(x in ORDINARY for x in column)
        assert all(not (masks[x] & masks[y]) for x, y in combinations(column, 2))
        for x in column:
            observed[x] += 1
    assert observed == target

    red = [frozenset({PIVOT, *a})]
    red.extend(frozenset(column) for column in columns)
    assert all(len(c) == 4 for c in red)
    assert len(set(red)) == 21
    max_cross = max(len(r & b) for r in red for b in blue)
    assert max_cross == 1

    red_degrees = Counter(x for c in red for x in c)
    blue_degrees = Counter(x for c in blue for x in c)
    assert red_degrees[PIVOT] == 1 and blue_degrees[PIVOT] == 10
    assert all(red_degrees[x] == (3 if x == exceptional else 2) for x in ORDINARY)
    assert all(blue_degrees[x] == 2 for x in ORDINARY)
    assert clique5(red) is None and clique5(blue) is None

    return {
        "kernel": rep["name"],
        "case": case,
        "matching_count": all_four_matching_count(masks),
        "max_cross_intersection": max_cross,
        "system_sha256": canonical_hash(red, blue),
    }


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify_independent.py BASE_KERNEL_JSON MATCHING_COVER_JSON")
    base = load(Path(sys.argv[1]))
    cover = load(Path(sys.argv[2]))
    side = set(base["side_nodes"])
    assert len(side) == 10
    a = set(cover["distinguished_triangle_edge_indices"])
    assert len(a) == 3

    representatives = {rep["name"]: rep for rep in base["representatives"]}
    assert set(representatives) == {"q=0 two-link representative", "q=1 two-link representative"}
    side_mask = 0
    for s in side:
        side_mask |= 1 << s
    for rep in representatives.values():
        _, masks, _ = check_kernel(rep, side)
        used = 0
        for x in sorted(a):
            assert not (masks[x] & side_mask)
            assert not (used & masks[x])
            used |= masks[x]

    seen: set[tuple[str, str]] = set()
    reports = []
    for survivor in cover["survivors"]:
        key = (survivor["kernel_representative"], survivor["demand_case"])
        assert key not in seen
        seen.add(key)
        reports.append(
            audit_survivor(
                survivor,
                representatives[key[0]],
                side,
                a,
                cover["demand_cases"],
            )
        )
    expected = {
        (rep, case)
        for rep in representatives
        for case in {"exceptional_vertex_in_A", "exceptional_vertex_outside_A"}
    }
    assert seen == expected

    # Two deterministic rejection tests guard the distinct-column and
    # matching predicates against accidental weakening.
    template = json.loads(json.dumps(cover["survivors"][0]))
    template["matchings"][1] = list(template["matchings"][0])
    try:
        audit_survivor(
            template,
            representatives[template["kernel_representative"]],
            side,
            a,
            cover["demand_cases"],
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("duplicate-column mutation was accepted")

    template = json.loads(json.dumps(cover["survivors"][0]))
    rep = representatives[template["kernel_representative"]]
    _, masks, _ = check_kernel(rep, side)
    column = template["matchings"][0]
    replacement = next(
        y for y in ORDINARY if y not in column and masks[column[0]] & masks[y]
    )
    column[1] = replacement
    try:
        audit_survivor(template, rep, side, a, cover["demand_cases"])
    except AssertionError:
        pass
    else:
        raise AssertionError("nonmatching-column mutation was accepted")

    print("independent rho=21 matching-cover audit: PASS")
    for report in reports:
        print(json.dumps(report, sort_keys=True))
    print("negative_self_tests=2")


if __name__ == "__main__":
    main()
