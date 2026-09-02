#!/usr/bin/env python3
"""Verify the potential-matched unit-tail ancestry counterfamily.

The accompanying note proves the universal statement.  This dependency-free
checker reconstructs the canonical formulas for every 3 <= p <= 33, checks
every inverse step and reverse DP identity, verifies explicit
minimal-unsatisfiability deletion witnesses, and hashes the complete family.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from collections.abc import Iterable


Clause = frozenset[int]
Formula = frozenset[Clause]
Assignment = dict[int, bool]


def clause_key(clause: Clause) -> tuple[int, tuple[int, ...]]:
    return (len(clause), tuple(sorted(clause)))


def canonical_formula(formula: Formula) -> list[list[int]]:
    return [list(sorted(clause)) for clause in sorted(formula, key=clause_key)]


def formula_digest(formula: Formula) -> str:
    payload = json.dumps(canonical_formula(formula), separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def terminal_formula(p: int) -> Formula:
    cycle = {
        frozenset((-i, i + 1 if i < p else 1))
        for i in range(1, p + 1)
    }
    return frozenset(
        cycle
        | {
            frozenset(range(1, p + 1)),
            frozenset(-i for i in range(1, p + 1)),
        }
    )


def terminal_deletion_witnesses(p: int) -> dict[Clause, Assignment]:
    formula = terminal_formula(p)
    positive = frozenset(range(1, p + 1))
    negative = frozenset(-i for i in range(1, p + 1))
    all_false = {i: False for i in range(1, p + 1)}
    all_true = {i: True for i in range(1, p + 1)}
    witnesses: dict[Clause, Assignment] = {
        positive: all_false,
        negative: all_true,
    }
    for i in range(1, p + 1):
        cycle_clause = frozenset((-i, i + 1 if i < p else 1))
        witnesses[cycle_clause] = {
            j: (j == i) for j in range(1, p + 1)
        }
    if set(witnesses) != set(formula):
        raise AssertionError("terminal witness family is incomplete")
    return witnesses


def literal_value(literal: int, assignment: Assignment) -> bool:
    value = assignment[abs(literal)]
    return value if literal > 0 else not value


def satisfies_clause(clause: Clause, assignment: Assignment) -> bool:
    return any(literal_value(literal, assignment) for literal in clause)


def verify_deletion_witnesses(
    formula: Formula, witnesses: dict[Clause, Assignment]
) -> None:
    if set(witnesses) != set(formula):
        raise AssertionError("wrong deletion-witness domain")
    for deleted, assignment in witnesses.items():
        for clause in formula:
            if clause != deleted and not satisfies_clause(clause, assignment):
                raise AssertionError("invalid deletion witness")


def inverse_unit_extension(
    formula: Formula,
    witnesses: dict[Clause, Assignment],
    variable: int,
    selected: tuple[Clause, ...],
) -> tuple[Formula, dict[Clause, Assignment], tuple[Clause, ...]]:
    arity = len(selected)
    if not 1 <= arity <= len(formula) or len(set(selected)) != arity:
        raise AssertionError("infeasible unit-fan arity")
    if not set(selected) <= set(formula):
        raise AssertionError("selected clause is absent")
    selected_set = set(selected)
    unit = frozenset((variable,))
    lifted = {frozenset(set(clause) | {-variable}) for clause in selected}
    untouched = set(formula) - selected_set
    extended = frozenset({unit} | lifted | untouched)
    if len(extended) != len(formula) + 1:
        raise AssertionError("clause collision in inverse unit extension")

    # Explicit minimality witnesses implement the proof in the note.
    new_witnesses: dict[Clause, Assignment] = {}
    base_for_unit = dict(witnesses[selected[0]])
    base_for_unit[variable] = False
    new_witnesses[unit] = base_for_unit
    for old_clause in formula:
        new_clause = (
            frozenset(set(old_clause) | {-variable})
            if old_clause in selected_set
            else old_clause
        )
        assignment = dict(witnesses[old_clause])
        assignment[variable] = True
        new_witnesses[new_clause] = assignment
    verify_deletion_witnesses(extended, new_witnesses)
    return extended, new_witnesses, selected


def inverse_binary_split(
    formula: Formula,
    witnesses: dict[Clause, Assignment],
    variable: int,
    resolvent: Clause,
    main_tail: Clause,
    side_tail: Clause,
) -> tuple[Formula, dict[Clause, Assignment]]:
    """Replace A union B by xA and -xB, preserving minimality."""
    if resolvent not in formula or main_tail | side_tail != resolvent:
        raise AssertionError("invalid split resolvent")
    if main_tail & side_tail:
        raise AssertionError("split tails are not disjoint")
    main = frozenset(set(main_tail) | {variable})
    side = frozenset(set(side_tail) | {-variable})
    extended = frozenset((set(formula) - {resolvent}) | {main, side})
    if len(extended) != len(formula) + 1:
        raise AssertionError("clause collision in binary split")

    base = witnesses[resolvent]
    new_witnesses: dict[Clause, Assignment] = {}
    delete_main = dict(base)
    delete_main[variable] = False
    new_witnesses[main] = delete_main
    delete_side = dict(base)
    delete_side[variable] = True
    new_witnesses[side] = delete_side
    for old_clause in formula:
        if old_clause == resolvent:
            continue
        assignment = dict(witnesses[old_clause])
        if any(literal_value(lit, assignment) for lit in main_tail):
            assignment[variable] = False
        else:
            if not any(literal_value(lit, assignment) for lit in side_tail):
                raise AssertionError("deletion witness does not satisfy split resolvent")
            assignment[variable] = True
        new_witnesses[old_clause] = assignment
    verify_deletion_witnesses(extended, new_witnesses)
    return extended, new_witnesses


def dp_reduce(formula: Formula, variable: int) -> Formula:
    positive = [clause for clause in formula if variable in clause]
    negative = [clause for clause in formula if -variable in clause]
    unaffected = {
        clause for clause in formula if variable not in clause and -variable not in clause
    }
    resolvents: set[Clause] = set()
    for pos in positive:
        for neg in negative:
            resolvent = frozenset((set(pos) - {variable}) | (set(neg) - {-variable}))
            if any(-literal in resolvent for literal in resolvent):
                continue
            resolvents.add(resolvent)
    return frozenset(unaffected | resolvents)


def potential(formula: Formula) -> int:
    return sum(len(clause) - 2 for clause in formula)


def schedule(p: int) -> list[int]:
    """Return filler unit-fan arities whose charges sum to 92-2p."""
    steps = 42 - p
    filler_steps = steps - 5
    if filler_steps < 1:
        raise AssertionError("the theorem uses the current range p <= 33")
    total_charge = 92 - 2 * p
    quotient, remainder = divmod(total_charge, filler_steps)
    charges = [quotient + 1] * remainder + [quotient] * (filler_steps - remainder)
    return [charge + 1 for charge in charges]


def verify_parameter(p: int) -> dict[str, object]:
    formula = terminal_formula(p)
    witnesses = terminal_deletion_witnesses(p)
    verify_deletion_witnesses(formula, witnesses)
    stages = [formula]
    charges: list[int] = []
    selections: list[str] = []
    distinguished = frozenset((-1, 2))
    if distinguished not in formula:
        raise AssertionError("distinguished terminal binary is absent")

    # Filler unit steps carry the complete positive charge budget while never
    # touching the distinguished binary clause.
    for offset, arity in enumerate(schedule(p), start=1):
        variable = p + offset
        before = formula
        candidates = [
            clause for clause in sorted(formula, key=clause_key)
            if clause != distinguished
        ]
        selected_input = tuple(candidates[:arity])
        formula, witnesses, selected = inverse_unit_extension(
            before, witnesses, variable, selected_input
        )
        if dp_reduce(formula, variable) != before:
            raise AssertionError("reverse DP identity failed")
        charge = potential(formula) - potential(before)
        if charge != arity - 1:
            raise AssertionError("unit-main charge identity failed")
        charges.append(charge)
        selected_payload = json.dumps(
            [list(sorted(clause)) for clause in selected], separators=(",", ":")
        )
        selections.append(hashlib.sha256(selected_payload.encode()).hexdigest())
        stages.append(formula)

    # One zero-charge unit lift turns the protected binary into a ternary B.
    variable = p + len(schedule(p)) + 1
    before = formula
    formula, witnesses, selected = inverse_unit_extension(
        before, witnesses, variable, (distinguished,)
    )
    if dp_reduce(formula, variable) != before:
        raise AssertionError("ternary-preparation DP identity failed")
    distinguished = frozenset(set(distinguished) | {-variable})
    side_tail = distinguished
    charges.append(0)
    selections.append(hashlib.sha256(
        json.dumps([list(sorted(selected[0]))], separators=(",", ":")).encode()
    ).hexdigest())
    stages.append(formula)

    # Three further zero-charge unit lifts add a fresh common three-tail A.
    main_tail_literals: list[int] = []
    for _ in range(3):
        variable += 1
        before = formula
        formula, witnesses, selected = inverse_unit_extension(
            before, witnesses, variable, (distinguished,)
        )
        if dp_reduce(formula, variable) != before:
            raise AssertionError("common-tail preparation DP identity failed")
        distinguished = frozenset(set(distinguished) | {-variable})
        main_tail_literals.append(-variable)
        charges.append(0)
        selections.append(hashlib.sha256(
            json.dumps([list(sorted(selected[0]))], separators=(",", ":")).encode()
        ).hexdigest())
        stages.append(formula)

    # The last inverse step is a disjoint 3+3 split.  It is the first forward
    # pivot and has a=4, m=1, c=0, hence charge zero.
    variable += 1
    if variable != 42:
        raise AssertionError("wrong final pivot label")
    before = formula
    main_tail = frozenset(main_tail_literals)
    formula, witnesses = inverse_binary_split(
        before, witnesses, variable, distinguished, main_tail, side_tail
    )
    if dp_reduce(formula, variable) != before:
        raise AssertionError("final disjoint 3+3 DP identity failed")
    if len(main_tail) != 3 or len(side_tail) != 3 or main_tail & side_tail:
        raise AssertionError("final fan is not disjoint 3+3")
    charges.append(0)
    selections.append(formula_digest(frozenset((distinguished,))))
    stages.append(formula)

    # Re-run the complete forward chain in the mathematically correct reverse
    # construction order.
    reduced = formula
    for variable, expected in zip(range(42, p, -1), reversed(stages[:-1])):
        reduced = dp_reduce(reduced, variable)
        if reduced != expected:
            raise AssertionError("complete singular-DP ancestry failed")

    if reduced != terminal_formula(p):
        raise AssertionError("wrong terminal formula")
    if len(formula) != 44 or len({abs(lit) for c in formula for lit in c}) != 42:
        raise AssertionError("wrong 42-variable, 44-clause endpoint")
    if len(formula) - 42 != 2:
        raise AssertionError("wrong deficiency")
    if len(charges) != 42 - p or sum(charges) != 92 - 2 * p:
        raise AssertionError("wrong total charge")
    if potential(formula) != 88:
        raise AssertionError("wrong endpoint potential")

    return {
        "p": p,
        "steps": 42 - p,
        "arities": schedule(p),
        "charges": charges,
        "terminal_potential": potential(terminal_formula(p)),
        "initial_potential": potential(formula),
        "formula_sha256": formula_digest(formula),
        "first_forward_fan": {"arity": 1, "main_length": 4, "side_lengths": [4], "overlap": 0},
        "selection_sha256": selections,
    }


def aggregate_digest(records: Iterable[dict[str, object]]) -> str:
    payload = json.dumps(list(records), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def main() -> None:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
        "ramsey_r55_symbolic_extension/potential-matched-unit-ancestry-certificate.json"
    )
    raw = path.read_bytes()
    certificate = json.loads(raw)
    p_min = certificate["terminal_parameter"]["minimum"]
    p_max = certificate["terminal_parameter"]["maximum"]
    records = [verify_parameter(p) for p in range(p_min, p_max + 1)]
    digest = aggregate_digest(records)

    expected = certificate["expected"]
    if len(records) != expected["parameter_count"]:
        raise AssertionError("wrong parameter count")
    if sum(record["steps"] for record in records) != expected["total_dp_steps"]:
        raise AssertionError("wrong total DP-step count")
    if max(max(record["arities"]) for record in records) != expected["maximum_arity"]:
        raise AssertionError("wrong maximum arity")
    if digest != expected["aggregate_sha256"]:
        raise AssertionError(
            f"aggregate digest mismatch: observed {digest}, expected {expected['aggregate_sha256']}"
        )

    print(
        "verified: potential-matched unit-tail ancestries for p=3..33; "
        f"formulas={len(records)}; dp_steps={expected['total_dp_steps']}; "
        "variables=42; clauses=44; deficiency=2; potential=88; "
        f"maximum_arity={expected['maximum_arity']}; "
        f"aggregate_sha256={digest}; certificate_sha256={hashlib.sha256(raw).hexdigest()}"
    )


if __name__ == "__main__":
    main()
