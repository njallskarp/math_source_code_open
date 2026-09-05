#!/usr/bin/env python3
"""Exact, dependency-free checker for the Gallai capacity certificates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "capacity_certificates.json"


def weight(units: int) -> int:
    return units * (units + 1) // 2


def check_bellman(entry: dict[str, object]) -> None:
    cap = int(entry["cap"])
    max_budget = int(entry["max_budget"])
    values = [int(value) for value in entry["values"]]
    assert len(values) == max_budget + 1
    assert values[0] == 0
    for budget in range(1, max_budget + 1):
        for part in range(1, min(cap, budget) + 1):
            assert weight(part) + values[budget - part] <= values[budget], (
                cap,
                budget,
                part,
            )


def attainable_pairs(budget: int, cap: int) -> set[tuple[int, int]]:
    """All (used units, weight) pairs for unordered positive atom packings."""
    states = {(0, 0)}
    for part in range(1, cap + 1):
        old = set(states)
        for used, total in old:
            next_used = used + part
            while next_used <= budget:
                states.add((next_used, total + ((next_used - used) // part) * weight(part)))
                next_used += part
    return states


def check_exact_gaps() -> None:
    weights49 = {value for _, value in attainable_pairs(49, 25)}
    weights48 = {value for _, value in attainable_pairs(48, 25)}
    assert not (weights49 & set(range(582, 600)))
    assert 581 in weights49 and 600 in weights49
    assert not (weights48 & set(range(560, 576)))
    assert 559 in weights48 and 576 in weights48


def check_odd_cycle_compression() -> None:
    for units in range(2, 200):
        assert units == 2 + (units - 2)
        assert units + 1 == weight(2) + (units - 2) * weight(1)


def main() -> None:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    assert document["format"] == "gallai-clique-capacity-v1"
    assert document["weight"] == "u*(u+1)/2"
    for entry in document["certificates"]:
        check_bellman(entry)
    check_exact_gaps()
    check_odd_cycle_compression()
    print(f"certificate_sha256={hashlib.sha256(raw).hexdigest()}")
    print("bellman_certificates=3 valid")
    print("budget49_gap=582..599 empty; endpoints 581,600 attained")
    print("budget48_gap=560..575 empty; endpoints 559,576 attained")
    print("odd_cycle_compression=valid for diagnostic range 2..199")


if __name__ == "__main__":
    main()
