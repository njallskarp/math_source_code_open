#!/usr/bin/env python3
"""Independent direct-line-graph replay for two leaves on c=3 bases."""

from __future__ import annotations

from collections import Counter
import hashlib
import json

from verify_c3_core import characteristic_polynomial, inertia_from_charpoly


def build_base(
    central_lengths: tuple[int, int], connector_lengths: tuple[int, int]
) -> tuple[list[str], list[tuple[int, int]]]:
    names = ["x", "y", "u", "v"]
    edges: list[tuple[int, int]] = []

    def append_path(label: str, start: int, finish: int, length: int) -> None:
        walk = [start]
        for position in range(1, length):
            walk.append(len(names))
            names.append(f"{label}:{position}")
        walk.append(finish)
        edges.extend((walk[index], walk[index + 1]) for index in range(length))

    append_path("A", 2, 2, 5)
    append_path("B", 3, 3, 5)
    append_path("P", 0, 1, central_lengths[0])
    append_path("Q", 0, 1, central_lengths[1])
    append_path("R", 0, 3, connector_lengths[0])
    append_path("S", 1, 2, connector_lengths[1])
    normalized = [tuple(sorted(edge)) for edge in edges]
    assert len(normalized) == len(set(normalized))
    return names, normalized


def line_graph_adjacency(edges: list[tuple[int, int]]) -> list[list[int]]:
    size = len(edges)
    adjacency = [[0] * size for _ in range(size)]
    for first in range(size):
        for second in range(first + 1, size):
            if set(edges[first]) & set(edges[second]):
                adjacency[first][second] = adjacency[second][first] = 1
    return adjacency


def direct_signature(edges: list[tuple[int, int]]) -> tuple[int, int]:
    polynomial = characteristic_polynomial(line_graph_adjacency(edges))
    positive, zero, negative = inertia_from_charpoly(polynomial)
    return positive - negative, zero


def main() -> None:
    pair_cases = 0
    line_signatures: Counter[int] = Counter()
    nullities: Counter[int] = Counter()
    records: list[str] = []

    for central in ((1, 3), (3, 1)):
        for connectors in ((1, 1), (1, 3), (3, 1), (3, 3)):
            names, base_edges = build_base(central, connectors)
            base_signature, base_nullity = direct_signature(base_edges)
            assert (base_signature, base_nullity) == (2, 0)

            for first in range(len(names)):
                for second in range(first, len(names)):
                    leaf_one = len(names)
                    leaf_two = leaf_one + 1
                    augmented_edges = base_edges + [(first, leaf_one), (second, leaf_two)]
                    line_signature, nullity = direct_signature(augmented_edges)
                    assert line_signature <= 2
                    line_signatures[line_signature] += 1
                    nullities[nullity] += 1
                    pair_cases += 1
                    records.append(
                        ":".join(
                            (
                                str(central[0]),
                                str(central[1]),
                                str(connectors[0]),
                                str(connectors[1]),
                                names[first],
                                names[second],
                                str(line_signature),
                            )
                        )
                    )

    assert pair_cases == 1096
    assert line_signatures == Counter({0: 1088, 2: 8})
    record_digest = hashlib.sha256("\n".join(sorted(records)).encode()).hexdigest()

    result = {
        "algorithm": "direct line graphs and exact characteristic-polynomial inertia",
        "base_assignments": 8,
        "line_signature_counts": {
            str(key): value for key, value in sorted(line_signatures.items())
        },
        "nullity_counts": {str(key): value for key, value in sorted(nullities.items())},
        "pair_cases": pair_cases,
        "record_sha256": record_digest,
        "status": "VERIFIED",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
