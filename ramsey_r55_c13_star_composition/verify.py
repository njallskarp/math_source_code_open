#!/usr/bin/env python3
"""Exact all-unit Farkas certificate and Boolean row-minimality check."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SELECTION_SHA256 = "ebe63f742ec0fe25ace4aa14eecfada571592440001cb682e41389c834acedcc"


def require(test: bool, message: str) -> None:
    if not test:
        raise ValueError(message)


def edge(i: int, j: int) -> bool:
    return i != j and (i - j) % 13 in (1, 5, 8, 12)


def indices(value: object, size: int, bound: int) -> tuple[int, ...]:
    require(isinstance(value, list) and len(value) == size, "index list size")
    require(all(type(x) is int and 0 <= x < bound for x in value), "index range")
    require(value == sorted(set(value)), "index order/distinctness")
    return tuple(value)


def verify(data: dict, selection_bytes: bytes) -> dict:
    require(sha256(selection_bytes).hexdigest() == SELECTION_SHA256, "selection hash")
    selection = json.loads(selection_bytes)
    masks = [int(x, 16) for x in selection["footprints"]]
    fields = {"cell", "target_edges", "five", "anchors", "forced_pair",
              "blue_pair_witnesses", "red_pair_witnesses"}
    require(type(data) is dict and set(data) == fields, "certificate fields")
    cell = indices(data["cell"], 7, 28)
    require(cell == tuple(range(7, 14)), "B cell")
    five = indices(data["five"], 5, 28)
    anchors = indices(data["anchors"], 3, 13)
    pivot = indices(data["forced_pair"], 2, 28)
    require(set(pivot) <= set(cell) & set(five), "pivot incidence")
    require(type(data["target_edges"]) is int and data["target_edges"] == 13,
            "selected quota")
    require(sum(masks[x].bit_count() for x in cell) == 48, "B incidence")

    # These rows have form a*x <= b; all certificate multipliers are one.
    rows: list[tuple[str, dict[tuple[int, int], int], int]] = []
    red_units, blue_units, used = set(), set(), set()
    for x, y, triple_raw in data["blue_pair_witnesses"]:
        pair = indices([x, y], 2, 28)
        triple = indices(triple_raw, 3, 13)
        require(all(not edge(i, j) for i, j in combinations(triple, 2)),
                "blue core triple")
        require(all(not (masks[z] >> i & 1) for z in pair for i in triple),
                "blue incidences")
        require(pair not in red_units, "duplicate red unit")
        red_units.add(pair)
        used.update(pair)
        rows.append((f"blue-{x}-{y}", {pair: -1}, -1))
    for x, y, core_pair_raw in data["red_pair_witnesses"]:
        pair = indices([x, y], 2, 28)
        core_pair = indices(core_pair_raw, 2, 13)
        require(set(pair) <= set(cell) and edge(*core_pair), "red core pair")
        require(all(masks[z] >> i & 1 for z in pair for i in core_pair),
                "red incidences")
        require(pair not in blue_units, "duplicate blue unit")
        blue_units.add(pair)
        used.update(pair)
        rows.append((f"red-{x}-{y}", {pair: 1}, 0))

    star_edges = set(combinations(five, 2))
    cell_edges = set(combinations(cell, 2))
    require(red_units == star_edges - {pivot}, "nine-edge star coverage")
    require(len(blue_units) == 8 and not (blue_units & star_edges), "eight blue units")
    require(star_edges & cell_edges == {pivot}, "unique B edge in star")
    signatures = [sum((masks[x] >> h & 1) << k for k, h in enumerate(anchors))
                  for x in five]
    require(sorted(signatures) == [0, 0, 1, 2, 4], "star_center translation")
    require(all(len({s >> k & 1 for s in signatures}) == 2 for k in range(3)),
            "coordinate mixedness")
    require(all(a ^ b != 7 for a, b in combinations(signatures, 2)),
            "edge visibility")

    rows.append(("star", {e: 1 for e in star_edges}, 9))
    rows.append(("quota", {e: -1 for e in cell_edges}, -data["target_edges"]))
    box_edges = cell_edges - blue_units - {pivot}
    require(len(box_edges) == 12, "remaining B capacities")
    all_rows = rows + [(f"box-{x}-{y}", {(x, y): 1}, 1) for x, y in sorted(box_edges)]
    coefficients = Counter()
    for _, a, _ in all_rows:
        for variable, coefficient in a.items():
            coefficients[variable] += coefficient
    rhs = sum(b for _, _, b in all_rows)
    require(len(coefficients) == 30 and not any(coefficients.values()), "Farkas coefficients")
    require(rhs == -1, "Farkas right side")

    # Explicit satisfying assignment after deleting each of the 19 non-box rows.
    variables = sorted(cell_edges | star_edges)
    baseline = {e: int(e not in blue_units) for e in variables}
    deletion_masks = {}
    for deleted, _, _ in rows:
        assignment = baseline.copy()
        if deleted == "quota":
            assignment[pivot] = 0
        elif deleted.startswith("blue-"):
            _, x, y = deleted.split("-")
            assignment[int(x), int(y)] = 0
        elif deleted.startswith("red-"):
            _, x, y = deleted.split("-")
            assignment[int(x), int(y)] = 1
            assignment[pivot] = 0
        violations = [name for name, a, b in all_rows
                      if sum(c * assignment[e] for e, c in a.items()) > b]
        require(violations == [deleted], "deletion witness")
        # Also check the full equality whenever the quota is retained.
        if deleted != "quota":
            require(sum(assignment[e] for e in cell_edges) == 13, "exact deletion quota")
        deletion_masks[deleted] = sum(assignment[e] << k for k, e in enumerate(variables))

    require(used == {0, 7, 8, 9, 10, 11, 13, 14, 15}, "nine-footprint support")
    retained_b_incidence = sum(masks[x].bit_count() for x in cell if x != 12)
    require(retained_b_incidence == 43 and masks[12].bit_count() == 5, "free-row threshold")
    canonical = json.dumps(deletion_masks, sort_keys=True, separators=(",", ":")).encode()
    return {
        "status": "VERIFIED C13 STAR COMPOSITION OBSTRUCTION",
        "selection_sha256": SELECTION_SHA256,
        "footprint_support": sorted(used),
        "signatures": signatures,
        "mixed_orbit": "star_center",
        "K5_rows": 18,
        "Farkas_terms": len(all_rows),
        "Farkas_variables": len(coefficients),
        "Farkas_rhs": rhs,
        "B_edge_upper_bound": 12,
        "selected_B_edge_target": 13,
        "necessary_free_B_row_size": 6,
        "selected_free_B_row_size": 5,
        "deletion_witnesses": len(deletion_masks),
        "deletion_masks_sha256": sha256(canonical).hexdigest(),
    }


if __name__ == "__main__":
    result = verify(json.loads((ROOT / "certificate.json").read_text()),
                    (ROOT / "selection.json").read_bytes())
    print(json.dumps(result, sort_keys=True, indent=2))
