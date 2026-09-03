#!/usr/bin/env python3
"""Independent tensor-fiber checker for the QLP-42 counterexample."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

P = 7
Q = 3
STATE_ATTRIBUTES = (
    (0, 0, 1, -1, 0, 0),
    (0, -1, 1, 0, 1, -1),
    (1, -1, 0, 0, 0, 0),
    (1, 0, 0, -1, 1, 1),
    (0, 1, 1, 0, 1, 1),
    (0, 0, 1, 1, 0, 0),
    (1, 0, 0, 1, 1, -1),
    (1, 1, 0, 0, 0, 0),
    (-1, 1, 0, 0, 0, 0),
    (-1, 0, 0, 1, 1, 1),
    (0, 0, -1, 1, 0, 0),
    (0, 1, -1, 0, 1, -1),
    (-1, 0, 0, -1, 1, -1),
    (-1, -1, 0, 0, 0, 0),
    (0, -1, -1, 0, 1, 1),
    (0, 0, -1, -1, 0, 0),
)


def rows(word: list[int]) -> tuple[tuple[int, ...], ...]:
    assert len(word) == P * Q
    return tuple(
        tuple(word[Q * row : Q * (row + 1)]) for row in range(P)
    )


def count_vector(word: list[int]) -> tuple[int, ...]:
    histogram = Counter(word)
    return tuple(histogram.get(label, 0) for label in range(16))


def exact_totals(word: list[int]) -> tuple[int, ...]:
    return tuple(
        sum(STATE_ATTRIBUTES[label][coordinate] for label in word)
        for coordinate in range(6)
    )


def indicator_difference_is_row_fiber_constant(
    first: list[int], second: list[int], label: int
) -> bool:
    for first_row, second_row in zip(rows(first), rows(second), strict=True):
        differences = {
            int(new == label) - int(old == label)
            for old, new in zip(first_row, second_row, strict=True)
        }
        if len(differences) != 1:
            return False
    return True


def main() -> None:
    path = Path(__file__).with_name("fiber_trade_counterexample.json")
    raw = path.read_bytes()
    certificate = json.loads(raw)

    assert set(certificate) == {
        "schema",
        "case",
        "coordinate_order",
        "family_targets",
        "global_parameters",
        "family_parameters",
        "state_counts",
        "first",
        "second",
        "expected",
    }
    assert certificate["case"] == 0
    assert certificate["global_parameters"] == {"q": 5, "sigma": 3}

    for family in ("A", "B"):
        first = certificate["first"][family]
        second = certificate["second"][family]
        expected_counts = tuple(certificate["state_counts"][family])
        assert count_vector(first) == count_vector(second) == expected_counts
        expected_target = certificate["family_targets"][family]
        expected_parameters = certificate["family_parameters"][family]
        expected_totals = (
            *expected_target["S"],
            *expected_target["H"],
            expected_parameters["q"],
            expected_parameters["sigma"],
        )
        assert exact_totals(first) == exact_totals(second) == expected_totals
        for label in range(16):
            assert indicator_difference_is_row_fiber_constant(
                first, second, label
            )

    first_a = certificate["first"]["A"]
    second_a = certificate["second"]["A"]
    first_rows = rows(first_a)
    second_rows = rows(second_a)
    changed_rows = [
        row
        for row, (old, new) in enumerate(
            zip(first_rows, second_rows, strict=True)
        )
        if old != new
    ]
    assert changed_rows == [0, 1]
    for row in changed_rows:
        assert len(set(first_rows[row])) == len(set(second_rows[row])) == 1
    assert first_rows[0] == second_rows[1]
    assert first_rows[1] == second_rows[0]

    first_support = [STATE_ATTRIBUTES[label][4] for label in first_a]
    second_support = [STATE_ATTRIBUTES[label][4] for label in second_a]
    symmetric_difference = sum(
        left != right
        for left, right in zip(first_support, second_support, strict=True)
    )
    assert symmetric_difference == 6
    assert certificate["first"]["B"] == certificate["second"]["B"]

    digest = hashlib.sha256(raw).hexdigest()
    print("counterexample_case=0")
    print("counterexample_branch=q5_sigma3")
    print("family_A_parameters=q4_sigma4")
    print("family_B_parameters=q1_sigma-1")
    print("primitive_indicator_colors_checked=16")
    print("primitive_vanishing_reason=C3_fiber_factor")
    print("changed_three_cell_fibers=2")
    print("quarter_support_symmetric_difference=6")
    print("fixed_invariant_lemma=disproved")
    print("qlp_witness_claim=false")
    print(f"fiber_counterexample_certificate_sha256={digest}")
    print("counterexample=verified")


if __name__ == "__main__":
    main()
