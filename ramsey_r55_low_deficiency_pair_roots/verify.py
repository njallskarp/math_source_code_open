#!/usr/bin/env python3
"""Exact checker for the deficiency-at-most-six pair-root reduction."""

from __future__ import annotations

import argparse
import base64
from collections.abc import Iterable
from hashlib import sha256
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
R35_COUNTS = {9: 290, 10: 313, 11: 105, 12: 12, 13: 1}
R35_SHA256 = {
    9: "3246c40dc444a248ae9199625abe16a984f630cf3d5f1ff1528e4409ff0c80cb",
    10: "194d2f95511f562e44a4137b1b91633f182e2adb14e7ea6880fa1b052bcbb3bb",
    11: "d5c52b2209e25080868adeef2dd52fa32835e5143208aceef129332c9184f16e",
    12: "322e7a54e67f4201bd37998ab420afb3eee41b1dcd6b277b7f055bda152da95e",
    13: "eb4d3f787f07ed14c0a82a83bee170ed096c24b6a7e971fded185ca1a760798f",
}
EXPECTED_Q0 = {18: 9, 19: 10, 20: 10, 21: 10, 22: 10, 23: 11, 24: 11}
EXPECTED_MULTIPLICITY = {18: 3, 19: 1, 20: 2, 21: 4, 22: 5, 23: 1, 24: 4}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


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


def has_clique(n: int, edges: set[tuple[int, int]], order: int, complement: bool) -> bool:
    for vertices in itertools.combinations(range(n), order):
        present = all((left, right) in edges for left, right in itertools.combinations(vertices, 2))
        if (not complement and present) or (
            complement
            and all((left, right) not in edges for left, right in itertools.combinations(vertices, 2))
        ):
            return True
    return False


def degree_sequence(n: int, edges: Iterable[tuple[int, int]]) -> list[int]:
    degrees = [0] * n
    for left, right in edges:
        require(0 <= left < right < n, "canonical simple edge")
        degrees[left] += 1
        degrees[right] += 1
    return degrees


def ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def audit_thresholds() -> tuple[list[str], int, int, str]:
    lines = ["d\tt\tq0\tpartners\tpartner_degree\tq\tcommon\tu_only\tv_only\tneither\toverlap_types"]
    scalar_cells = 0
    templates = 0
    for d in range(18, 25):
        threshold = U[d] - 6
        q0 = ceil_div(2 * threshold, d)
        require(q0 == EXPECTED_Q0[d], f"q0 d={d}")
        multiplicity = ceil_div(2 * threshold - d * (q0 - 1), 14 - q0)
        require(multiplicity == EXPECTED_MULTIPLICITY[d], f"multiplicity d={d}")
        for partner_degree in range(18, 25):
            for q in range(q0, 14):
                cells = (q, d - 1 - q, partner_degree - 1 - q, 43 - d - partner_degree + q)
                require(min(cells) >= 0 and sum(cells) == 41, "pair-cell partition")
                lines.append(
                    "\t".join(
                        map(
                            str,
                            (
                                d,
                                threshold,
                                q0,
                                multiplicity,
                                partner_degree,
                                q,
                                *cells,
                                R35_COUNTS[q],
                            ),
                        )
                    )
                )
                scalar_cells += 1
                templates += R35_COUNTS[q]
    payload = ("\n".join(lines) + "\n").encode("ascii")
    require(scalar_cells == 189, "scalar-cell count")
    require(templates == 18_767, "coarse-template count")
    return lines, scalar_cells, templates, sha256(payload).hexdigest()


def audit_witnesses() -> list[tuple[int, int, int, int]]:
    data = json.loads((HERE / "SHARP_WITNESSES.json").read_text(encoding="utf-8"))
    require(len(data["witnesses"]) == 7, "seven sharp witnesses")
    summaries = []
    for item in data["witnesses"]:
        d = item["d"]
        n, edges = decode_graph6(base64.b64decode(item["parent_graph6_base64"], validate=True))
        require(n == d, f"witness order d={d}")
        require(len(edges) == item["parent_edges"], f"parent edge count d={d}")
        for raw_edge in item["delete_edges"]:
            edge = tuple(raw_edge)
            require(edge in edges, f"deleted edge exists d={d}")
            edges.remove(edge)
        degrees = degree_sequence(n, edges)
        require(not has_clique(n, edges, 4, False), f"K4-free d={d}")
        require(not has_clique(n, edges, 5, True), f"alpha<5 d={d}")
        deficiency = U[d] - len(edges)
        require(0 <= deficiency <= 6, f"deficiency range d={d}")
        require(max(degrees) == EXPECTED_Q0[d], f"sharp maximum degree d={d}")
        summaries.append((d, len(edges), deficiency, max(degrees)))
    return summaries


def audit_catalogs(catalog_dir: Path) -> int:
    total = 0
    for q, expected_count in R35_COUNTS.items():
        path = catalog_dir / f"r35_{q}.g6"
        raw = path.read_bytes()
        require(sha256(raw).hexdigest() == R35_SHA256[q], f"catalog hash q={q}")
        records = [record for record in raw.splitlines() if record]
        require(len(records) == expected_count, f"catalog count q={q}")
        for index, record in enumerate(records):
            n, edges = decode_graph6(record)
            require(n == q, f"catalog order q={q} index={index}")
            require(not has_clique(n, edges, 3, False), f"triangle-free q={q} index={index}")
            require(not has_clique(n, edges, 5, True), f"alpha<5 q={q} index={index}")
        total += len(records)
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog-dir", type=Path)
    args = parser.parse_args()
    _, scalar_cells, templates, table_hash = audit_thresholds()
    summaries = audit_witnesses()
    print("PASS thresholds q0=9,10,10,10,10,11,11 partners=3,1,2,4,5,1,4")
    print(f"PASS pair-root cover scalar_cells={scalar_cells} coarse_templates={templates}")
    print(f"PAIR_ROOT_TABLE_SHA256 {table_hash}")
    print(
        "PASS sharp witnesses "
        + " ".join(f"d={d}:e={edges}:delta={delta}:Delta={maximum}" for d, edges, delta, maximum in summaries)
    )
    if args.catalog_dir is None:
        print("CATALOG_AUDIT skipped; pass --catalog-dir for 721 pinned R(3,5) records")
    else:
        print(f"PASS pinned R(3,5) catalog records={audit_catalogs(args.catalog_dir)}")
    print("SCOPE complete low-deficiency pair-root reduction; no R(5,5;43) existence verdict")


if __name__ == "__main__":
    main()
