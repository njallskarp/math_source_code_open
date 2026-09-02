#!/usr/bin/env python3
"""Definition-level verification of the 216 exact order-three quotient lifts."""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PI3 = ROOT / "qlp42_q5_q37_pi3_witnesses"
sys.path.insert(0, str(PI3))

from verify_pi3_witnesses import (  # noqa: E402
    CASES,
    N,
    STATES,
    add,
    conjugate,
    multiply,
    read_supports,
)


def paf(word: list[tuple[int, int]]) -> list[tuple[int, int]]:
    answer: list[tuple[int, int]] = []
    for shift in range(len(word)):
        value = (0, 0)
        for position, left in enumerate(word):
            value = add(
                value,
                multiply(left, conjugate(word[(position + shift) % len(word)])),
            )
        answer.append(value)
    return answer


def compress_mod_three(word: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [
        sum((word[position][coordinate] for position in range(residue, N, 3)), 0)
        for residue in range(3)
        for coordinate in range(2)
    ]


def as_gaussians(flat: list[int]) -> list[tuple[int, int]]:
    assert len(flat) == 6
    return [(flat[2 * index], flat[2 * index + 1]) for index in range(3)]


def verify_row(
    row: dict[str, str], supports: dict[int, list[tuple[int, int]]]
) -> None:
    q_value = int(row["q"])
    orbit = int(row["orbit"])
    case_id = int(row["case"])
    support = supports[q_value][orbit]
    assert support == (
        int(row["a_mask_hex"], 16),
        int(row["b_mask_hex"], 16),
    )
    words = (
        [int(character, 16) for character in row["states_a"]],
        [int(character, 16) for character in row["states_b"]],
    )
    assert all(len(word) == N for word in words)

    equal_count = 0
    opposite_count = 0
    components: list[dict[str, list[tuple[int, int]]]] = []
    for family, (word, mask) in enumerate(zip(words, support)):
        current = {"s": [], "h": []}
        for position, state_index in enumerate(word):
            state = STATES[state_index]
            assert (state["kind"] == "quarter") == bool((mask >> position) & 1)
            equal_count += state["kind"] == "equal"
            opposite_count += state["kind"] == "opposite"
            current["s"].append(state["s"])  # type: ignore[arg-type]
            current["h"].append(state["h"])  # type: ignore[arg-type]
        components.append(current)

    assert equal_count == (41 - q_value) // 2
    assert opposite_count == (43 - q_value) // 2

    p, q, x, y = CASES[case_id]
    sum_targets = (((p + q, q - p), (0, 0)), ((x + y - 1, y - x), (1, 0)))
    for family in range(2):
        for component_id, component in enumerate(("s", "h")):
            total = (0, 0)
            for value in components[family][component]:
                total = add(total, value)
            assert total == sum_targets[family][component_id]

    compressed = [
        {
            component: as_gaussians(compress_mod_three(components[family][component]))
            for component in ("s", "h")
        }
        for family in range(2)
    ]
    expected = {
        "s": [(43, 0), (0, 0), (0, 0)],
        "h": [(29, 0), (-14, 0), (-14, 0)],
    }
    for component in ("s", "h"):
        combined = []
        pa = paf(compressed[0][component])
        pb = paf(compressed[1][component])
        for left, right in zip(pa, pb):
            combined.append(add(left, right))
        assert combined == expected[component]


def main() -> None:
    path = Path(__file__).with_name("order3_lifts.tsv")
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    keys = [(int(row["q"]), int(row["orbit"]), int(row["case"])) for row in rows]
    expected = {
        (q_value, orbit, case_id)
        for q_value in (5, 37)
        for orbit in range(18)
        for case_id in range(6)
    }
    assert len(rows) == 216 and set(keys) == expected and len(keys) == len(set(keys))
    supports = read_supports()
    for row in rows:
        verify_row(row, supports)
    counts = Counter(int(row["q"]) for row in rows)
    assert counts == Counter({5: 108, 37: 108})
    print("rows=216;q5_cells=108;q37_cells=108")
    print("exact_factor7_order3_coupled_quotient_lifts=verified")


if __name__ == "__main__":
    main()
