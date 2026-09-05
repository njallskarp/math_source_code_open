#!/usr/bin/env python3
"""Definition-level checker for the aggregate footprint counterexample."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


CORE_ORDER = 13
FULL = (1 << CORE_ORDER) - 1
DIFFERENCES = frozenset((1, 5, 8, 12))
CELLS = ("A", "B", "O")
CELL_SIZES = {"A": 7, "B": 7, "O": 14}
ANCHOR_RED = {"A": 1, "B": 1, "O": 0}


def core_edge(i: int, j: int) -> bool:
    return i != j and ((i - j) % CORE_ORDER) in DIFFERENCES


def parse(path: Path) -> tuple[dict[str, object], str]:
    raw = path.read_bytes()
    data = json.loads(raw)
    if not isinstance(data, dict) or set(data) != {
        "core_e", "core_pivot", "edge_counts", "k", "outside_pivot", "rows"
    }:
        raise ValueError("certificate fields")
    return data, hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    data, certificate_hash = parse(args.certificate)

    fours = tuple(
        sum(1 << vertex for vertex in subset)
        for subset in itertools.combinations(range(CORE_ORDER), 4)
        if all(not core_edge(i, j) for i, j in itertools.combinations(subset, 2))
    )
    transversals = frozenset(
        mask for mask in range(1 << CORE_ORDER) if all(mask & four for four in fours)
    )
    if len(fours) != 39 or len(transversals) != 3459:
        raise AssertionError("core census")

    k = data["k"]
    core_e = frozenset(data["core_e"])
    core_pivot = data["core_pivot"]
    outside_pivot = data["outside_pivot"]
    if not isinstance(k, int) or not 0 <= k <= 6 or k != len(core_e):
        raise AssertionError("core mark count")
    if any(not isinstance(vertex, int) or not 0 <= vertex < CORE_ORDER for vertex in core_e):
        raise AssertionError("core mark")
    if core_pivot is not None and core_pivot not in core_e:
        raise AssertionError("core pivot")
    if (core_pivot is not None) + (outside_pivot is True) != 1:
        raise AssertionError("pivot location")
    if outside_pivot and k > 5:
        raise AssertionError("no marked A vertex for outside pivot")

    rows: list[tuple[str, int, int]] = []
    previous = None
    for record in data["rows"]:
        if not isinstance(record, dict) or set(record) != {"cell", "count", "marked", "mask"}:
            raise ValueError("row fields")
        cell = record["cell"]
        count = record["count"]
        marked = record["marked"]
        mask_text = record["mask"]
        if cell not in CELLS or marked not in (0, 1) or not isinstance(count, int) or count <= 0:
            raise ValueError("row value")
        if not isinstance(mask_text, str) or len(mask_text) != 4 or mask_text.lower() != mask_text:
            raise ValueError("mask encoding")
        mask = int(mask_text, 16)
        key = (CELLS.index(cell), marked, mask)
        if previous is not None and key <= previous:
            raise ValueError("rows not canonical")
        previous = key
        if mask not in transversals:
            raise AssertionError(("nontransversal", cell, marked, mask_text))
        rows.extend((cell, marked, mask) for _ in range(count))
    if len(rows) != 28:
        raise AssertionError(("row count", len(rows)))

    expected_marked = {"A": 6 - k, "B": 6 - k, "O": 1 + k}
    for cell in CELLS:
        cell_rows = [row for row in rows if row[0] == cell]
        if len(cell_rows) != CELL_SIZES[cell]:
            raise AssertionError(("cell size", cell, len(cell_rows)))
        if sum(marked for _, marked, _ in cell_rows) != expected_marked[cell]:
            raise AssertionError(("cell marks", cell))

    pivot_bits = tuple(int(core_pivot == index) for index in range(CORE_ORDER))
    for index in range(CORE_ORDER):
        total_column = sum(mask >> index & 1 for _, _, mask in rows)
        if total_column != 15 - int(index in core_e):
            raise AssertionError(("column total", index, total_column))
        marked_column = sum(marked * (mask >> index & 1) for _, marked, mask in rows)
        marked_core_neighbors = sum(core_edge(index, other) for other in core_e)
        if marked_column + marked_core_neighbors != 6 + 2 * pivot_bits[index]:
            raise AssertionError(("marked column", index, marked_column, marked_core_neighbors))

    edges = data["edge_counts"]
    expected_edge_fields = {
        "i_A", "i_B", "d_A", "d_B", "d_O",
        "m_A", "m_B", "m_O", "m_AB", "m_AO", "m_BO",
    }
    if not isinstance(edges, dict) or set(edges) != expected_edge_fields:
        raise ValueError("edge-count fields")
    if any(not isinstance(value, int) for value in edges.values()):
        raise ValueError("nonintegral edge count")

    for cell in ("A", "B"):
        incidence = sum(mask.bit_count() for c, _, mask in rows if c == cell)
        if edges[f"i_{cell}"] != incidence or edges[f"m_{cell}"] + incidence != 61:
            raise AssertionError(("anchor red equation", cell))
    if edges["m_B"] + edges["m_O"] + edges["m_BO"] != 110:
        raise AssertionError("anchor u blue equation")
    if edges["m_A"] + edges["m_O"] + edges["m_AO"] != 110:
        raise AssertionError("anchor v blue equation")

    for cell in CELLS:
        required_sum = sum(
            21 - marked - ANCHOR_RED[cell] - mask.bit_count()
            for c, marked, mask in rows
            if c == cell
        )
        if edges[f"d_{cell}"] != required_sum:
            raise AssertionError(("degree sum", cell, required_sum))
    if edges["d_A"] != 2 * edges["m_A"] + edges["m_AB"] + edges["m_AO"]:
        raise AssertionError("A edge accounting")
    if edges["d_B"] != 2 * edges["m_B"] + edges["m_AB"] + edges["m_BO"]:
        raise AssertionError("B edge accounting")
    if edges["d_O"] != 2 * edges["m_O"] + edges["m_AO"] + edges["m_BO"]:
        raise AssertionError("O edge accounting")

    bounds = {
        "m_A": (3, 16), "m_B": (3, 16), "m_O": (18, 73),
        "m_AB": (0, 49), "m_AO": (0, 98), "m_BO": (0, 98),
    }
    for variable, (lower, upper) in bounds.items():
        if not lower <= edges[variable] <= upper:
            raise AssertionError(("edge bound", variable))
    ab_edges = edges["m_A"] + edges["m_B"] + edges["m_AB"]
    all_d_edges = sum(edges[variable] for variable in ("m_A", "m_B", "m_O", "m_AB", "m_AO", "m_BO"))
    if not 18 <= ab_edges <= 73 or not 84 <= all_d_edges <= 294:
        raise AssertionError("Turan union bound")

    # Pinpoint the first missing constraint.  In A the full-core row intersects
    # every other row in that other row.  Every transversal has at least five
    # vertices, while H has independence number four, so the intersection has
    # a red core edge.  A red edge joining the two A rows would then form a red
    # K5 with u and the endpoints of that core edge.  Hence every full row is
    # isolated in G[A].
    a_masks = [mask for cell, _, mask in rows if cell == "A"]
    full_rows = a_masks.count(FULL)
    if full_rows != 1:
        raise AssertionError(("expected one full A row", full_rows))
    for mask in a_masks:
        if mask == FULL:
            continue
        if not any(
            mask >> left & 1 and mask >> right & 1 and core_edge(left, right)
            for left, right in itertools.combinations(range(CORE_ORDER), 2)
        ):
            raise AssertionError(("full-row partner has no core edge", mask))
    pairwise_cap = (CELL_SIZES["A"] - full_rows) * (CELL_SIZES["A"] - full_rows - 1) // 2
    if edges["m_A"] <= pairwise_cap:
        raise AssertionError("certificate does not expose the claimed missing coupling")

    result = {
        "A_pairwise_compatible_edge_cap": pairwise_cap,
        "A_required_edges": edges["m_A"],
        "certificate_sha256": certificate_hash,
        "core_independent_fours": len(fours),
        "footprint_rows": len(rows),
        "k": k,
        "nonzero_row_types": len(data["rows"]),
        "status": "VERIFIED AGGREGATE COUNTEREXAMPLE",
        "transversal_masks": len(transversals),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
