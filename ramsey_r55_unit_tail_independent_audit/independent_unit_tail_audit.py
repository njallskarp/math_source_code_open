#!/usr/bin/env python3
"""Clean-room audit of the all-p potential-matched unit-tail construction.

This checker deliberately uses a different filler-selection rule from the
producer: at every filler step it takes the *last* available clauses in a
canonical order, rather than the first.  It constructs fresh histories for
all 3 <= p <= 33, carries explicit one-clause-deletion witnesses, checks each
reverse DP identity, and audits the arithmetic and first-fan normalization.
"""

from __future__ import annotations

import hashlib
import json


Clause = frozenset[int]
Formula = frozenset[Clause]
Assignment = dict[int, bool]


def clause_order(clause: Clause) -> tuple[int, tuple[int, ...]]:
    return len(clause), tuple(sorted(clause))


def lit_value(literal: int, assignment: Assignment) -> bool:
    value = assignment[abs(literal)]
    return value if literal > 0 else not value


def satisfies(clause: Clause, assignment: Assignment) -> bool:
    return any(lit_value(literal, assignment) for literal in clause)


def check_deletion_witnesses(
    formula: Formula, witnesses: dict[Clause, Assignment]
) -> None:
    assert set(witnesses) == set(formula)
    variables = {abs(literal) for clause in formula for literal in clause}
    for deleted, assignment in witnesses.items():
        assert variables <= set(assignment)
        assert all(
            clause == deleted or satisfies(clause, assignment)
            for clause in formula
        )


def terminal(p: int) -> tuple[Formula, dict[Clause, Assignment]]:
    cycle = {
        frozenset((-i, i + 1 if i < p else 1))
        for i in range(1, p + 1)
    }
    positive = frozenset(range(1, p + 1))
    negative = frozenset(-i for i in range(1, p + 1))
    formula = frozenset(cycle | {positive, negative})

    # The cycle implications force all variables true as soon as one is true.
    # Hence positive and negative long clauses make the formula unsatisfiable.
    assert all(
        frozenset((-i, i + 1 if i < p else 1)) in formula
        for i in range(1, p + 1)
    )

    witnesses: dict[Clause, Assignment] = {
        positive: {i: False for i in range(1, p + 1)},
        negative: {i: True for i in range(1, p + 1)},
    }
    for i in range(1, p + 1):
        deleted = frozenset((-i, i + 1 if i < p else 1))
        witnesses[deleted] = {j: j == i for j in range(1, p + 1)}
    check_deletion_witnesses(formula, witnesses)
    return formula, witnesses


def dp(formula: Formula, variable: int) -> Formula:
    positive = [clause for clause in formula if variable in clause]
    negative = [clause for clause in formula if -variable in clause]
    untouched = {
        clause
        for clause in formula
        if variable not in clause and -variable not in clause
    }
    resolvents: set[Clause] = set()
    for pos in positive:
        for neg in negative:
            resolvent = frozenset((pos - {variable}) | (neg - {-variable}))
            if not any(-literal in resolvent for literal in resolvent):
                resolvents.add(resolvent)
    return frozenset(untouched | resolvents)


def potential(formula: Formula) -> int:
    return sum(len(clause) - 2 for clause in formula)


def unit_lift(
    formula: Formula,
    witnesses: dict[Clause, Assignment],
    variable: int,
    selected: tuple[Clause, ...],
) -> tuple[Formula, dict[Clause, Assignment]]:
    selected_set = set(selected)
    assert selected and len(selected_set) == len(selected)
    assert selected_set <= set(formula)
    assert all(variable not in clause and -variable not in clause for clause in formula)

    unit = frozenset({variable})
    image = {
        old: frozenset(set(old) | {-variable}) if old in selected_set else old
        for old in formula
    }
    extended = frozenset({unit} | set(image.values()))
    assert len(extended) == len(formula) + 1

    new_witnesses: dict[Clause, Assignment] = {}
    # Deleting the unit: one selected-clause deletion witness satisfies every
    # untouched clause, while u=false satisfies every lifted clause.
    unit_witness = dict(witnesses[selected[-1]])
    unit_witness[variable] = False
    new_witnesses[unit] = unit_witness
    # Deleting any lifted or untouched image: u=true reduces the remaining
    # formula to a subformula of the corresponding old deletion.
    for old in formula:
        assignment = dict(witnesses[old])
        assignment[variable] = True
        new_witnesses[image[old]] = assignment
    check_deletion_witnesses(extended, new_witnesses)
    assert dp(extended, variable) == formula
    return extended, new_witnesses


def binary_split(
    formula: Formula,
    witnesses: dict[Clause, Assignment],
    variable: int,
    resolvent: Clause,
    main_tail: Clause,
    side_tail: Clause,
) -> tuple[Formula, dict[Clause, Assignment], Clause, Clause]:
    assert resolvent in formula
    assert main_tail | side_tail == resolvent
    assert not (main_tail & side_tail)
    assert all(variable not in clause and -variable not in clause for clause in formula)

    main = frozenset(set(main_tail) | {variable})
    side = frozenset(set(side_tail) | {-variable})
    extended = frozenset((set(formula) - {resolvent}) | {main, side})
    assert len(extended) == len(formula) + 1

    base = witnesses[resolvent]
    new_witnesses: dict[Clause, Assignment] = {}
    deleting_main = dict(base)
    deleting_main[variable] = False
    new_witnesses[main] = deleting_main
    deleting_side = dict(base)
    deleting_side[variable] = True
    new_witnesses[side] = deleting_side
    for old in formula:
        if old == resolvent:
            continue
        assignment = dict(witnesses[old])
        if satisfies(main_tail, assignment):
            assignment[variable] = False
        else:
            assert satisfies(side_tail, assignment)
            assignment[variable] = True
        new_witnesses[old] = assignment
    check_deletion_witnesses(extended, new_witnesses)
    assert dp(extended, variable) == formula
    return extended, new_witnesses, main, side


def filler_arities(p: int) -> list[int]:
    steps = 42 - p
    filler_steps = steps - 5
    charge = 92 - 2 * p
    quotient, remainder = divmod(charge, filler_steps)
    charges = [quotient + 1] * remainder + [quotient] * (filler_steps - remainder)
    return [value + 1 for value in charges]


def digest_formula(formula: Formula) -> str:
    payload = [list(sorted(clause)) for clause in sorted(formula, key=clause_order)]
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode()
    ).hexdigest()


def check_parameter(p: int) -> dict[str, object]:
    formula, witnesses = terminal(p)
    stages = [formula]
    charges: list[int] = []
    overlaps: list[int] = []
    protected = frozenset({-1, 2})

    arities = filler_arities(p)
    assert len(arities) == 37 - p
    assert max(arities) <= 8
    assert max(arities) <= p + 1
    assert sum(arity - 1 for arity in arities) == 92 - 2 * p

    # Independent selection policy: choose the last clauses, rather than the
    # producer's lexicographically first clauses, while protecting one binary.
    next_variable = p + 1
    for arity in arities:
        candidates = sorted(formula - {protected}, key=clause_order)
        assert len(candidates) >= arity
        selected = tuple(candidates[-arity:])
        before = formula
        formula, witnesses = unit_lift(
            formula, witnesses, next_variable, selected
        )
        charges.append(potential(formula) - potential(before))
        overlaps.extend([0] * arity)
        assert charges[-1] == arity - 1
        stages.append(formula)
        next_variable += 1

    # Four arity-one unit lifts turn the protected binary into A union B with
    # disjoint three-literal tails B (old binary plus first fresh literal) and
    # A (the next three fresh literals).
    before = formula
    formula, witnesses = unit_lift(
        formula, witnesses, next_variable, (protected,)
    )
    protected = frozenset(set(protected) | {-next_variable})
    side_tail = protected
    charges.append(potential(formula) - potential(before))
    overlaps.append(0)
    stages.append(formula)
    next_variable += 1

    main_literals: list[int] = []
    for _ in range(3):
        before = formula
        formula, witnesses = unit_lift(
            formula, witnesses, next_variable, (protected,)
        )
        protected = frozenset(set(protected) | {-next_variable})
        main_literals.append(-next_variable)
        charges.append(potential(formula) - potential(before))
        overlaps.append(0)
        stages.append(formula)
        next_variable += 1

    assert next_variable == 42
    main_tail = frozenset(main_literals)
    before = formula
    formula, witnesses, main, side = binary_split(
        formula,
        witnesses,
        next_variable,
        protected,
        main_tail,
        side_tail,
    )
    charges.append(potential(formula) - potential(before))
    overlaps.append(len(main_tail & side_tail))
    stages.append(formula)

    assert len(main) == len(side) == 4
    assert main_tail.isdisjoint(side_tail)
    assert charges[-5:] == [0, 0, 0, 0, 0]
    assert all(overlap == 0 for overlap in overlaps)

    # Exhibit a global variable-complementation map making the first forward
    # main clause all positive and its side clause all negative.
    flips = {abs(literal) for literal in main if literal < 0}
    flips |= {abs(literal) for literal in side if literal > 0}
    assert (
        {abs(literal) for literal in main}
        & {abs(literal) for literal in side}
    ) == {next_variable}
    normalized_main = {
        -literal if abs(literal) in flips else literal for literal in main
    }
    normalized_side = {
        -literal if abs(literal) in flips else literal for literal in side
    }
    assert all(literal > 0 for literal in normalized_main)
    assert all(literal < 0 for literal in normalized_side)

    # Eliminate in reverse construction order and compare every full formula.
    reduced = formula
    for variable, expected in zip(range(42, p, -1), reversed(stages[:-1])):
        reduced = dp(reduced, variable)
        assert reduced == expected
    assert reduced == terminal(p)[0]

    variables = {abs(literal) for clause in formula for literal in clause}
    assert len(variables) == 42
    assert len(formula) == 44
    assert len(formula) - len(variables) == 2
    assert len(charges) == 42 - p
    assert sum(charges) == 92 - 2 * p
    assert potential(formula) == 88
    assert potential(stages[0]) == 2 * p - 4
    check_deletion_witnesses(formula, witnesses)

    return {
        "p": p,
        "steps": len(charges),
        "filler_arities": arities,
        "total_charge": sum(charges),
        "formula_sha256": digest_formula(formula),
    }


def main() -> None:
    records = [check_parameter(p) for p in range(3, 34)]
    assert len(records) == 31
    assert sum(record["steps"] for record in records) == 744
    assert max(max(record["filler_arities"]) for record in records) == 8
    aggregate = hashlib.sha256(
        json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("parameters=31")
    print("reverse_dp_steps=744")
    print("maximum_filler_arity=8")
    print(f"independent_family_sha256={aggregate}")
    print("independent_unit_tail_audit=PASS")


if __name__ == "__main__":
    main()
