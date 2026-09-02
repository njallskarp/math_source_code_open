#!/usr/bin/env python3
"""Dependency-free exact verifier for the QLP-42 pi^3 witness manifest."""

from __future__ import annotations

from collections import Counter
from csv import DictReader
from itertools import product
from pathlib import Path

G = tuple[int, int]
N = 21
FULL = (1 << N) - 1
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: G, right: G) -> G:
    return left[0] - right[0], left[1] - right[1]


def multiply(left: G, right: G) -> G:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: G) -> G:
    return value[0], -value[1]


def div_pi(value: G) -> G:
    real, imag = value
    assert (real + imag) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def divisible_pi3(value: G) -> bool:
    current = value
    for _ in range(3):
        if (current[0] + current[1]) % 2:
            return False
        current = div_pi(current)
    return True


def local_states() -> tuple[dict[str, G | str], ...]:
    states = []
    for x, y in product(ROOTS, repeat=2):
        s = div_pi(subtract(x, y))
        h = div_pi(add(x, y))
        dot = x[0] * y[0] + x[1] * y[1]
        kind = "equal" if dot == 1 else "opposite" if dot == -1 else "quarter"
        states.append({"s": s, "h": h, "kind": kind})
    assert len(states) == len({(state["s"], state["h"]) for state in states}) == 16
    return tuple(states)


STATES = local_states()


def rotate(mask: int, shift: int) -> int:
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def canonical(mask: int) -> int:
    return min(rotate(mask, shift) for shift in range(N))


def read_supports() -> dict[int, list[tuple[int, int]]]:
    path = Path(__file__).parent.parent / "qlp42_q5_q37_binary_frontier" / "frontier_orbits.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(DictReader(handle, delimiter="\t"))
    q5 = sorted(
        (int(row["a_mask_hex"], 16), int(row["b_mask_hex"], 16))
        for row in rows
        if int(row["q_a"]) % 2 == 0
    )
    q37 = sorted(
        {
            (
                canonical(FULL ^ int(row["a_mask_hex"], 16)),
                canonical(FULL ^ int(row["b_mask_hex"], 16)),
            )
            for row in rows
            if int(row["q_a"]) % 2 == 1
        }
    )
    assert len(q5) == len(q37) == 18
    return {5: q5, 37: q37}


def target(component: str, shift: int) -> G:
    if component == "h":
        return -2, 0
    if shift == 4:
        return -2, 0
    if shift == 10:
        return 2, 0
    return 0, 0


def verify_row(row: dict[str, str], supports: dict[int, list[tuple[int, int]]]) -> None:
    q_value = int(row["q"])
    orbit = int(row["orbit"])
    case_id = int(row["case"])
    support = supports[q_value][orbit]
    assert support == (int(row["a_mask_hex"], 16), int(row["b_mask_hex"], 16))
    words = [
        [int(character, 16) for character in row["states_a"]],
        [int(character, 16) for character in row["states_b"]],
    ]
    assert all(len(word) == N for word in words)

    opposite_count = 0
    for family, support_mask in enumerate(support):
        for position, state_index in enumerate(words[family]):
            kind = STATES[state_index]["kind"]
            assert (kind == "quarter") == bool((support_mask >> position) & 1)
            opposite_count += kind == "opposite"
    assert opposite_count == (19 if q_value == 5 else 3)

    p, q, x, y = CASES[case_id]
    sum_targets = (((p + q, q - p), (0, 0)), ((x + y - 1, y - x), (1, 0)))
    for family in range(2):
        for component_id, component in enumerate(("s", "h")):
            total = (0, 0)
            for state_index in words[family]:
                total = add(total, STATES[state_index][component])  # type: ignore[arg-type]
            assert total == sum_targets[family][component_id]

    for component in ("s", "h"):
        for shift in range(1, 11):
            correlation = (0, 0)
            for family in range(2):
                for position in range(N):
                    left = STATES[words[family][position]][component]
                    right = STATES[words[family][(position + shift) % N]][component]
                    correlation = add(  # type: ignore[arg-type]
                        correlation,
                        multiply(left, conjugate(right)),  # type: ignore[arg-type]
                    )
            assert divisible_pi3(subtract(correlation, target(component, shift)))


def main() -> None:
    supports = read_supports()
    path = Path(__file__).parent / "witnesses.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(DictReader(handle, delimiter="\t"))
    assert len(rows) == 83
    keys = [(int(row["q"]), int(row["orbit"]), int(row["case"])) for row in rows]
    assert len(set(keys)) == len(keys)
    for row in rows:
        verify_row(row, supports)

    branch_rows = Counter(int(row["q"]) for row in rows)
    branch_orbits = {
        q_value: {int(row["orbit"]) for row in rows if int(row["q"]) == q_value}
        for q_value in (5, 37)
    }
    case_rows = {
        q_value: Counter(
            int(row["case"]) for row in rows if int(row["q"]) == q_value
        )
        for q_value in (5, 37)
    }
    assert branch_rows == Counter({5: 31, 37: 52})
    assert all(branch_orbits[q_value] == set(range(18)) for q_value in (5, 37))
    assert case_rows[5] == Counter({0: 3, 1: 6, 2: 5, 3: 3, 4: 8, 5: 6})
    assert case_rows[37] == Counter({0: 6, 1: 10, 2: 8, 3: 11, 4: 11, 5: 6})
    print("rows=83;q5_rows=31;q37_rows=52;q5_orbits=18;q37_orbits=18")
    print("independent_certificate=verified")


if __name__ == "__main__":
    main()
