#!/usr/bin/env python3
"""Clean-room check of the complete McKay Ramsey(4,4;15) catalog.

The catalog's completeness is an external literature/data trust boundary.  This
program independently checks the bytes actually supplied: graph6 decoding,
the Ramsey property of every record, edge counts, and absence of an
eight-regular graph.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


EXPECTED_INPUT_SHA256 = (
    "53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1"
)
EXPECTED_HISTOGRAM = {50: 13, 51: 96, 52: 211, 53: 211, 54: 96, 55: 13}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def decode_graph6(line: bytes) -> tuple[int, ...]:
    """Decode a short-form graph6 record into adjacency bitsets."""
    require(line and line[0] != ord(">"), "headers and long graph6 forms are not accepted")
    n = line[0] - 63
    require(n == 15, "expected an order-15 graph6 record")
    values = [byte - 63 for byte in line[1:]]
    require(len(values) == 18 and all(0 <= value < 64 for value in values), "payload")
    bits = [(value >> shift) & 1 for value in values for shift in range(5, -1, -1)]
    require(not any(bits[n * (n - 1) // 2 :]), "nonzero graph6 padding")

    adjacency = [0] * n
    for bit, (i, j) in zip(bits, ((i, j) for j in range(1, n) for i in range(j))):
        if bit:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    require(all(not (adjacency[i] >> i) & 1 for i in range(n)), "loop")
    require(
        all(((adjacency[i] >> j) & 1) == ((adjacency[j] >> i) & 1)
            for i in range(n) for j in range(n)),
        "asymmetric adjacency",
    )
    return tuple(adjacency)


def audit(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    require(digest == EXPECTED_INPUT_SHA256, "unexpected catalog SHA-256")
    lines = raw.splitlines()
    require(len(lines) == 640 and len(raw) == 12_800, "catalog size/count")

    edge_histogram: Counter[int] = Counter()
    invalid_four_sets = 0
    regular_records: list[tuple[int, int]] = []
    degree_eight_records: list[int] = []
    checked_four_sets = 0

    for index, line in enumerate(lines):
        adjacency = decode_graph6(line)
        degrees = [row.bit_count() for row in adjacency]
        edges = sum(degrees) // 2
        edge_histogram[edges] += 1
        if len(set(degrees)) == 1:
            regular_records.append((index, degrees[0]))
        if degrees == [8] * 15:
            degree_eight_records.append(index)
        for vertices in combinations(range(15), 4):
            red_edges = sum(
                (adjacency[i] >> j) & 1 for i, j in combinations(vertices, 2)
            )
            checked_four_sets += 1
            invalid_four_sets += int(red_edges in (0, 6))

    require(invalid_four_sets == 0, "catalog contains a non-Ramsey record")
    require(dict(sorted(edge_histogram.items())) == EXPECTED_HISTOGRAM, "edge histogram")
    require(not regular_records and not degree_eight_records, "regular catalog record")
    require(max(edge_histogram) == 55, "maximum edge count")

    summary = {
        "catalog_bytes": len(raw),
        "catalog_records": len(lines),
        "catalog_sha256": digest,
        "checked_four_sets": checked_four_sets,
        "invalid_four_sets": invalid_four_sets,
        "edge_histogram": [[key, edge_histogram[key]] for key in sorted(edge_histogram)],
        "maximum_edges": max(edge_histogram),
        "regular_records": regular_records,
        "degree_eight_records": degree_eight_records,
        "conclusion": "no eight-regular Ramsey(4,4;15) graph occurs in the catalog",
    }
    encoded = json.dumps(summary, sort_keys=True, separators=(",", ":")).encode()
    summary["certificate_sha256"] = sha256(encoded).hexdigest()
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    summary = audit(args.catalog)
    print(f"catalog_sha256={summary['catalog_sha256']}")
    print(f"records={summary['catalog_records']} checked_four_sets={summary['checked_four_sets']}")
    print("edge_histogram=" + ",".join(f"{e}:{n}" for e, n in summary["edge_histogram"]))
    print(f"maximum_edges={summary['maximum_edges']} regular_records=0 degree_eight_records=0")
    print("VERIFIED no eight-regular Ramsey(4,4;15) graph in the complete supplied catalog")
    print(f"certificate_sha256={summary['certificate_sha256']}")


if __name__ == "__main__":
    main()
