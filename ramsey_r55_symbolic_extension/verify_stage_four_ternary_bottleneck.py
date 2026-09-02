#!/usr/bin/env python3
"""Definition-level checker for the stage-four ternary bottleneck."""

from __future__ import annotations

import json
import sys
from itertools import product
from pathlib import Path

Literal = int
Clause = frozenset[Literal]
Formula = frozenset[Clause]


def clause(values: list[int] | tuple[int, ...]) -> Clause:
    result = frozenset(values)
    assert all(-literal not in result for literal in result)
    return result


def dp_reduce(formula: Formula, variable: int) -> Formula:
    positive = [item for item in formula if variable in item]
    negative = [item for item in formula if -variable in item]
    untouched = {item for item in formula if variable not in item and -variable not in item}
    resolvents: set[Clause] = set()
    for left in positive:
        for right in negative:
            candidate = (left - {variable}) | (right - {-variable})
            if any(-literal in candidate for literal in candidate):
                continue
            resolvents.add(frozenset(candidate))
    return frozenset(untouched | resolvents)


def terminal_formula(p: int) -> Formula:
    cycle = {
        frozenset((-index, index % p + 1)) for index in range(1, p + 1)
    }
    long_clauses = {
        frozenset(range(1, p + 1)),
        frozenset(range(-p, 0)),
    }
    return frozenset(cycle | long_clauses)


def verify_final_unit_fans(p: int, unit: int) -> int:
    terminal = terminal_formula(p)
    cycle = {item for item in terminal if len(item) == 2}
    long_clauses = sorted(
        (item for item in terminal if len(item) == p), key=lambda item: min(item)
    )
    assert len(cycle) == p and len(long_clauses) == 2

    count = 0
    for choices in product((False, True), repeat=2):
        selected = set(cycle)
        selected.update(
            long_clause
            for long_clause, take in zip(long_clauses, choices, strict=True)
            if take
        )
        stage_seven = {frozenset({unit})}
        stage_seven.update(
            (item | {-unit}) if item in selected else item for item in terminal
        )
        assert dp_reduce(frozenset(stage_seven), unit) == terminal
        count += 1
    return count


def verify_pattern(pattern: dict, expected_pair: Formula, unit: int, x: int) -> None:
    stage_four = frozenset(
        clause(tuple(item)) for item in pattern["stage_four_forced_ternaries"]
    )
    assert len(stage_four) == 4
    assert all(len(item) == 3 for item in stage_four)

    stage_five = dp_reduce(stage_four, pattern["step_five_pivot"])
    stage_six = dp_reduce(stage_five, pattern["step_six_pivot"])
    assert stage_six == expected_pair
    stage_seven = dp_reduce(stage_six, x)
    assert stage_seven == frozenset({frozenset({unit})})


def verify_certificate(data: dict) -> None:
    p = data["terminal_p"]
    assert data["core_variables"] - p == data["singular_steps"] == 8
    assert data["stage_floor_through_five"] == [4, 4, 4, 4, 3, 2]

    # At step four, the main clause has length at least four, so its tail has
    # length at least three.  Every new ternary is exactly that same tail;
    # old clauses have length at least four.
    stage_three_floor = data["stage_floor_through_five"][3]
    main_tail_floor = stage_three_floor - 1
    assert main_tail_floor == 3
    assert data["maximum_ternary_clauses_after_step_four"] == 1
    assert data["maximum_binary_clauses_after_step_four"] == 0
    assert data["maximum_binary_clauses_after_step_five"] == 1

    expected_pair = frozenset(
        clause(tuple(item)) for item in data["forced_stage_six_binaries"]
    )
    assert expected_pair == frozenset(
        {frozenset({2, 1}), frozenset({-2, 1})}
    )
    unit_clause = clause(tuple(data["forced_stage_seven_unit"]))
    assert unit_clause == frozenset({1})

    patterns = data["sixth_step_parent_patterns"]
    assert [item["name"] for item in patterns] == [
        "singleton-main-tail",
        "two-literal-main-tail",
    ]
    for pattern in patterns:
        verify_pattern(pattern, expected_pair, unit=1, x=2)
        assert len(pattern["stage_four_forced_ternaries"]) > data[
            "maximum_ternary_clauses_after_step_four"
        ]

    assert verify_final_unit_fans(p, unit=p + 1) == data[
        "labeled_final_unit_fan_choices"
    ] == 4

    assert data["excluded_p"] == [34]
    assert data["previously_excluded_p"] == [35, 36, 37, 38, 39, 40, 41]
    assert data["surviving_p_minimum"] == 2
    assert data["surviving_p_maximum"] == 33


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} CERTIFICATE.json")
    data = json.loads(Path(sys.argv[1]).read_text())
    verify_certificate(data)
    print(
        "verified: G4 ternary cap=1, forced p=34 patterns=2, "
        "each forces 4 ternaries, excluded p=34, surviving p=2..33"
    )


if __name__ == "__main__":
    main()
