#!/usr/bin/env python3
"""Small standalone checker for the (4,7,23) BHR seed and growth cuts."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

SUPPORT = (1, 2, 11)
EXPECTED_COUNTS = (4, 7, 23)
EXPECTED_CUTS = {1: 22, 2: 23, 11: 10}
EXPECTED_CHANGED = {
    1: [(22, 33)],
    2: [(23, 34), (22, 33)],
    11: [
        (10, 12),
        (12, 1),
        (3, 14),
        (13, 2),
        (0, 11),
        (9, 20),
        (19, 8),
        (7, 18),
        (16, 5),
        (4, 15),
        (17, 6),
    ],
}


def cyclic_length(u: int, v: int, order: int) -> int:
    difference = abs(u - v)
    return min(difference, order - difference)


def changed_by_embedding(
    u: int, v: int, mode: int, cut: int, order: int
) -> bool:
    uu = u if u <= cut else u + mode
    vv = v if v <= cut else v + mode
    return cyclic_length(uu, vv, order + mode) > cyclic_length(u, v, order)


def changed_edges(path: list[int], mode: int, cut: int) -> list[tuple[int, int]]:
    order = len(path)
    return [
        (u, v)
        for u, v in zip(path, path[1:])
        if changed_by_embedding(u, v, mode, cut, order)
    ]


def check(certificate: Path) -> dict[str, object]:
    raw = certificate.read_bytes()
    data = json.loads(raw)
    assert data["schema"] == "bhr-target-orthant-v1"
    assert tuple(data["support"]) == SUPPORT
    seed = data["seed"]
    counts = tuple(seed["counts"])
    cuts = {int(mode): cut for mode, cut in seed["selected_growth_cuts"].items()}
    path = seed["path"]
    order = sum(counts) + 1
    assert counts == EXPECTED_COUNTS
    assert cuts == EXPECTED_CUTS
    assert sorted(path) == list(range(order))
    actual = Counter(
        cyclic_length(u, v, order) for u, v in zip(path, path[1:])
    )
    assert actual == Counter(dict(zip(SUPPORT, counts)))

    observed_changed = {}
    for mode, cut in cuts.items():
        assert mode - 1 <= cut <= order - 1 - mode
        critical = set(range(cut - mode + 1, cut + 1))
        edges = changed_edges(path, mode, cut)
        assert edges == EXPECTED_CHANGED[mode]
        incidence: Counter[int] = Counter()
        for u, v in edges:
            assert u in critical or v in critical
            if u in critical:
                incidence[u] += 1
            if v in critical:
                incidence[v] += 1
        assert all(incidence[vertex] == 1 for vertex in critical)
        observed_changed[str(mode)] = [list(edge) for edge in edges]

    maximum = max(actual)
    maximum_pair_sum = max(sum(pair) for pair in ((1, 2), (1, 11), (2, 11)))
    assert maximum == 11
    assert 2 * maximum + maximum_pair_sum == order == 35
    path_bytes = json.dumps(path, separators=(",", ":")).encode()
    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "path_sha256": hashlib.sha256(path_bytes).hexdigest(),
        "order": order,
        "length_counts": dict(sorted(actual.items())),
        "growth_cuts": cuts,
        "changed_edges": observed_changed,
        "safe_margin": f"{2 * maximum + maximum_pair_sum}<={order}",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    for key, value in check(args.certificate).items():
        if isinstance(value, dict):
            value = json.dumps(value, separators=(",", ":"), sort_keys=True)
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
