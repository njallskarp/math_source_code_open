#!/usr/bin/env python3
"""Exact checker for unit-fan universality over the terminal formula F_p."""

from __future__ import annotations

import json
import sys
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
    positive = [clause for clause in formula if variable in clause]
    negative = [clause for clause in formula if -variable in clause]
    untouched = {
        clause
        for clause in formula
        if variable not in clause and -variable not in clause
    }
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

    return all(any(literal_true(literal) for literal in clause) for clause in formula)


def terminal_deletion_witness(
    p: int, removed: Clause, positive: Clause, negative: Clause
) -> frozenset[int]:
    if removed == positive:
        return frozenset()
    if removed == negative:
        return frozenset(range(1, p + 1))
    negative_literals = [literal for literal in removed if literal < 0]
    assert len(removed) == 2 and len(negative_literals) == 1
    return frozenset({-negative_literals[0]})


def canonical_selection(
    cycle: Formula, positive: Clause, retained_binary_cycle: Formula
) -> Formula:
    selected_cycle = cycle - retained_binary_cycle
    if selected_cycle:
        return selected_cycle
    # An inverse unit extension must have at least one side clause.  Selecting
    # L+ leaves the entire binary cycle untouched.
    return frozenset({positive})


def construct(p: int, retained_binary_cycle: Formula) -> tuple[Formula, Formula, Formula]:
    cycle, positive, negative = terminal_parts(p)
    terminal = frozenset(set(cycle) | {positive, negative})
    selected = canonical_selection(cycle, positive, retained_binary_cycle)
    unit = p + 1
    pivot = p + 2
    extension = frozenset(
        {frozenset({unit})}
        | {clause | {-unit} for clause in selected}
        | set(terminal - selected)
    )
    split = frozenset(
        set(extension - {frozenset({unit})})
        | {frozenset({pivot, unit}), frozenset({-pivot, unit})}
    )
    return terminal, extension, split


def check_deletion_witnesses(
    p: int,
    retained_binary_cycle: Formula,
    terminal: Formula,
    extension: Formula,
    split: Formula,
) -> None:
    cycle, positive, negative = terminal_parts(p)
    selected = canonical_selection(cycle, positive, retained_binary_cycle)
    unit = p + 1
    pivot = p + 2

    for removed in terminal:
        witness = terminal_deletion_witness(p, removed, positive, negative)
        assert satisfies(terminal - {removed}, witness)

    selected_clause = next(iter(selected))
    base = terminal_deletion_witness(p, selected_clause, positive, negative)
    assert satisfies(extension - {frozenset({unit})}, base)

    for clause in extension - {frozenset({unit})}:
        tail = clause - {-unit} if -unit in clause else clause
        witness = terminal_deletion_witness(p, frozenset(tail), positive, negative)
        assert satisfies(extension - {clause}, frozenset(set(witness) | {unit}))

    pair_positive = frozenset({pivot, unit})
    pair_negative = frozenset({-pivot, unit})
    assert satisfies(split - {pair_positive}, base)
    assert satisfies(split - {pair_negative}, frozenset(set(base) | {pivot}))
    for clause in split - {pair_positive, pair_negative}:
        tail = clause - {-unit} if -unit in clause else clause
        witness = terminal_deletion_witness(p, frozenset(tail), positive, negative)
        assert satisfies(split - {clause}, frozenset(set(witness) | {unit}))


def rotate_mask(mask: int, p: int, shift: int) -> int:
    return sum(((mask >> index) & 1) << ((index + shift) % p) for index in range(p))


def reflect_mask(mask: int, p: int, shift: int) -> int:
    return sum(((mask >> index) & 1) << ((shift - index) % p) for index in range(p))


def canonical_mask(mask: int, p: int) -> int:
    images = []
    for shift in range(p):
        images.append(rotate_mask(mask, p, shift))
        images.append(reflect_mask(mask, p, shift))
    return min(images)


def verify_p(p: int) -> int:
    cycle, _, _ = terminal_parts(p)
    ordered_cycle = sorted(cycle, key=lambda clause: next(-x for x in clause if x < 0))
    binary_counts: set[int] = set()
    orbit_representatives: set[int] = set()

    for mask in range(1 << p):
        retained = frozenset(
            clause for index, clause in enumerate(ordered_cycle) if (mask >> index) & 1
        )
        terminal, extension, split = construct(p, retained)
        unit = p + 1
        pivot = p + 2
        assert dp_reduce(split, pivot) == extension
        assert dp_reduce(extension, unit) == terminal

        expected_binary = retained | {
            frozenset({pivot, unit}),
            frozenset({-pivot, unit}),
        }
        actual_binary = frozenset(clause for clause in split if len(clause) == 2)
        assert actual_binary == expected_binary
        binary_counts.add(len(actual_binary))
        orbit_representatives.add(canonical_mask(mask, p))
        check_deletion_witnesses(p, retained, terminal, extension, split)

    assert binary_counts == set(range(2, p + 3))
    assert len(orbit_representatives) * 2 * p >= 2**p
    return len(orbit_representatives)


def verify_certificate(data: dict) -> None:
    minimum = data["exhaustive_check_range"]["minimum_p"]
    maximum = data["exhaustive_check_range"]["maximum_p"]
    expected = {
        int(p): count
        for p, count in data["binary_subset_orbits_under_terminal_symmetry"].items()
    }
    assert set(expected) == set(range(minimum, maximum + 1))
    for p in range(minimum, maximum + 1):
        assert verify_p(p) == expected[p]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} CERTIFICATE.json")
    data = json.loads(Path(sys.argv[1]).read_text())
    verify_certificate(data)
    print(
        "verified: every binary-cycle subset for p=3..12; "
        "binary counts 2..p+2; terminal-symmetry orbit counts match certificate"
    )


if __name__ == "__main__":
    main()
