#!/usr/bin/env python3
"""Exact checker for the p=34 terminal unit-fan classification."""

from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import product
from pathlib import Path

Literal = int
Clause = frozenset[Literal]
Formula = frozenset[Clause]


def terminal_parts(p: int) -> tuple[Formula, Clause, Clause]:
    cycle = frozenset(
        frozenset((-index, index % p + 1)) for index in range(1, p + 1)
    )
    positive = frozenset(range(1, p + 1))
    negative = frozenset(range(-p, 0))
    return cycle, positive, negative


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


def satisfies(formula: Formula, true_variables: frozenset[int]) -> bool:
    def literal_true(literal: int) -> bool:
        value = abs(literal) in true_variables
        return value if literal > 0 else not value

    return all(any(literal_true(literal) for literal in item) for item in formula)


def terminal_deletion_witness(p: int, removed: Clause, positive: Clause, negative: Clause) -> frozenset[int]:
    if removed == positive:
        return frozenset()
    if removed == negative:
        return frozenset(range(1, p + 1))
    negative_literals = [literal for literal in removed if literal < 0]
    assert len(removed) == 2 and len(negative_literals) == 1
    return frozenset({-negative_literals[0]})


def unit_extension(terminal: Formula, selected: Formula, unit: int) -> Formula:
    assert selected <= terminal and selected
    return frozenset(
        {frozenset({unit})}
        | {item | {-unit} for item in selected}
        | set(terminal - selected)
    )


def split_unit(extension: Formula, unit: int, pivot: int) -> Formula:
    return frozenset(
        set(extension - {frozenset({unit})})
        | {frozenset({pivot, unit}), frozenset({-pivot, unit})}
    )


def check_minimality_witnesses(
    p: int,
    terminal: Formula,
    selected: Formula,
    extension: Formula,
    stage_six: Formula,
    positive: Clause,
    negative: Clause,
    unit: int,
    pivot: int,
) -> None:
    # Remove the unit: u=false satisfies all lifted clauses, while a witness
    # for F\{C0} satisfies the untouched subset F\S.
    selected_clause = next(iter(selected))
    base = terminal_deletion_witness(p, selected_clause, positive, negative)
    assert satisfies(extension - {frozenset({unit})}, base)

    for item in extension - {frozenset({unit})}:
        tail = item - {-unit} if -unit in item else item
        base = terminal_deletion_witness(p, frozenset(tail), positive, negative)
        assignment = frozenset(set(base) | {unit})
        assert satisfies(extension - {item}, assignment)

    pair_positive = frozenset({pivot, unit})
    pair_negative = frozenset({-pivot, unit})
    base = terminal_deletion_witness(p, selected_clause, positive, negative)
    assert satisfies(stage_six - {pair_positive}, base)
    assert satisfies(stage_six - {pair_negative}, frozenset(set(base) | {pivot}))

    for item in stage_six - {pair_positive, pair_negative}:
        tail = item - {-unit} if -unit in item else item
        base = terminal_deletion_witness(p, frozenset(tail), positive, negative)
        assignment = frozenset(set(base) | {unit})
        assert satisfies(stage_six - {item}, assignment)


def complement_reverse_literal(literal: int, p: int, fixed: set[int]) -> int:
    if abs(literal) in fixed:
        return literal
    index = abs(literal) - 1
    target = (-index) % p + 1
    return -target if literal > 0 else target


def transform(formula: Formula, p: int, fixed: set[int]) -> Formula:
    return frozenset(
        frozenset(complement_reverse_literal(literal, p, fixed) for literal in item)
        for item in formula
    )


def length_profile(formula: Formula) -> dict[str, int]:
    return {str(length): count for length, count in sorted(Counter(map(len, formula)).items())}


def verify_certificate(data: dict) -> None:
    p = data["terminal_p"]
    cycle, positive, negative = terminal_parts(p)
    terminal = frozenset(set(cycle) | {positive, negative})
    assert len(cycle) == data["terminal_cycle_clause_count"] == p
    assert len(terminal) == data["terminal_clause_count"] == p + 2
    assert data["unrestricted_nonempty_labeled_unit_extensions"] == 2 ** len(terminal) - 1

    # Verify the elementary MU witnesses for F_p.
    for removed in terminal:
        witness = terminal_deletion_witness(p, removed, positive, negative)
        assert satisfies(terminal - {removed}, witness)

    unit = p + 1
    pivot = p + 2
    pair = {frozenset({pivot, unit}), frozenset({-pivot, unit})}
    assert pair == {
        frozenset(item) for item in data["stage_six_binary_pair"]
    }
    assert frozenset({unit}) == frozenset(data["stage_seven_unit"])

    # From B(G6)=pair, every terminal binary must be selected.  The only
    # remaining decisions are the two long clauses, hence 2^(36-34)=4.
    assert all(len(item) == 2 for item in cycle)
    free_terminal_clauses = terminal - cycle
    assert free_terminal_clauses == frozenset({positive, negative})
    derived_count = 2 ** len(free_terminal_clauses)
    assert derived_count == 2 ** (len(terminal) - len(cycle))
    assert derived_count == data["compatible_labeled_fans"] == 4

    fans: dict[tuple[bool, bool], Formula] = {}
    profiles: dict[int, dict[str, int]] = {}
    long_order = (positive, negative)
    for choices in product((False, True), repeat=2):
        selected = frozenset(
            set(cycle)
            | {item for item, take in zip(long_order, choices, strict=True) if take}
        )
        extension = unit_extension(terminal, selected, unit)
        stage_six = split_unit(extension, unit, pivot)
        assert dp_reduce(stage_six, pivot) == extension
        assert dp_reduce(extension, unit) == terminal

        binaries = {item for item in stage_six if len(item) == 2}
        assert binaries == pair
        # Omitting any cycle member would leave exactly that extra binary.
        for omitted in cycle:
            bad_selected = selected - {omitted}
            bad_binaries = {
                item for item in split_unit(unit_extension(terminal, bad_selected, unit), unit, pivot)
                if len(item) == 2
            }
            assert bad_binaries == pair | {omitted}

        check_minimality_witnesses(
            p, terminal, selected, extension, stage_six,
            positive, negative, unit, pivot
        )
        fans[choices] = stage_six
        profiles[sum(choices)] = length_profile(stage_six)

    expected_profiles = {
        int(size): profile
        for size, profile in data["length_profiles_by_long_selection_size"].items()
    }
    assert profiles == expected_profiles
    assert len(set(tuple(sorted(profile.items())) for profile in profiles.values())) == 3
    assert data["canonical_long_selection_sizes"] == [0, 1, 2]
    assert data["symmetry_classes"] == 3

    fixed = {unit, pivot}
    assert transform(terminal, p, fixed) == terminal
    assert transform(fans[(True, False)], p, fixed) == fans[(False, True)]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} CERTIFICATE.json")
    data = json.loads(Path(sys.argv[1]).read_text())
    verify_certificate(data)
    print(
        "verified: unrestricted=2^36-1, compatible labeled fans=4, "
        "symmetry classes=3, long-selection sizes=[0, 1, 2]"
    )


if __name__ == "__main__":
    main()
