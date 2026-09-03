#!/usr/bin/env python3
"""Standalone standard-library checker for the even-b, c=1 formulas."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

SUPPORT = (1, 2, 11)
EXPECTED_SEEDS = ((1, 20, 1), (2, 18, 1))
EXPECTED_CHANGED = {
    "A": ((2, 0), (1, 3)),
    "B": ((2, 0), (3, 1)),
}


def cyclic_length(u: int, v: int, order: int) -> int:
    difference = abs(u - v)
    return min(difference, order - difference)


def family_a(q: int) -> list[int]:
    assert q >= 0
    return (
        list(range(8 + 2 * q, -1, -2))
        + list(range(21 + 2 * q, 12 + 2 * q, -2))
        + list(range(1, 12 + 2 * q, 2))
        + list(range(10 + 2 * q, 23 + 2 * q, 2))
    )


def family_b(q: int) -> list[int]:
    assert q >= 0
    return (
        list(range(8 + 2 * q, -1, -2))
        + list(range(20 + 2 * q, 11 + 2 * q, -2))
        + list(range(11 + 2 * q, 22 + 2 * q, 2))
        + [10 + 2 * q]
        + list(range(9 + 2 * q, 0, -2))
    )


def changed_edges(path: list[int]) -> list[tuple[int, int]]:
    order = len(path)
    changed = []
    for u, v in zip(path, path[1:]):
        old = cyclic_length(u, v, order)
        uu = u if u <= 1 else u + 2
        vv = v if v <= 1 else v + 2
        if cyclic_length(uu, vv, order + 2) > old:
            changed.append((u, v))
    return changed


def insert_gap(path: list[int]) -> list[int]:
    """Apply 2-growth at cut 1 from its definition."""
    critical = {0, 1}
    changed = set(changed_edges(path))
    embedded = {vertex: vertex if vertex <= 1 else vertex + 2 for vertex in path}
    out = [embedded[path[0]]]
    for u, v in zip(path, path[1:]):
        if (u, v) in changed:
            inside = [vertex for vertex in (u, v) if vertex in critical]
            assert len(inside) == 1
            out.append(inside[0] + 2)
        out.append(embedded[v])
    return out


def check(certificate: Path, grid: int) -> dict[str, object]:
    assert grid >= 1
    raw = certificate.read_bytes()
    data = json.loads(raw)
    assert data["schema"] == "bhr-even-b-c1-completion-v1"
    assert tuple(data["support"]) == SUPPORT
    records = data["families"]
    assert [record["name"] for record in records] == ["A", "B"]
    formulas = (family_a, family_b)
    digest = hashlib.sha256()
    paths_checked = 0
    transitions_checked = 0

    for record, formula, seed_counts in zip(records, formulas, EXPECTED_SEEDS):
        name = record["name"]
        assert tuple(record["counts_at_q_zero"]) == seed_counts
        assert record["selected_growth_cut"] == {"mode": 2, "cut": 1}
        assert record["path_at_q_zero"] == formula(0)
        for q in range(grid + 2):
            path = formula(q)
            counts = (seed_counts[0], seed_counts[1] + 2 * q, 1)
            order = sum(counts) + 1
            assert sorted(path) == list(range(order))
            lengths = Counter(
                cyclic_length(u, v, order) for u, v in zip(path, path[1:])
            )
            assert lengths == Counter(dict(zip(SUPPORT, counts)))
            changed = changed_edges(path)
            assert tuple(changed) == EXPECTED_CHANGED[name]
            incidence = Counter(
                vertex
                for edge in changed
                for vertex in edge
                if vertex in {0, 1}
            )
            assert incidence == Counter({0: 1, 1: 1})
            digest.update(json.dumps([name, q, path], separators=(",", ":")).encode())
            digest.update(b"\n")
            paths_checked += 1
            if q <= grid:
                assert insert_gap(path) == formula(q + 1)
                transitions_checked += 1

    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "grid": grid,
        "family_paths_checked": paths_checked,
        "transitions_checked": transitions_checked,
        "record_sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=64)
    args = parser.parse_args()
    for key, value in check(args.certificate, args.grid).items():
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
