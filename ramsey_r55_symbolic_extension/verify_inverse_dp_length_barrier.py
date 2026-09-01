#!/usr/bin/env python3
"""Exact checker for the inverse singular-DP length-barrier certificate.

The universal classification is proved in the accompanying Markdown note.
This checker validates its integer certificate and exhaustively audits the
common-core inverse constructor on F_p for the small values listed in the
certificate. It uses only Python's standard library and exact finite sets.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

Literal = int
Clause = frozenset[Literal]
Formula = frozenset[Clause]


def powerset(items: tuple[Literal, ...]):
    for mask in range(1 << len(items)):
        yield frozenset(items[i] for i in range(len(items)) if mask >> i & 1)


def f_p(p: int) -> Formula:
    clauses: set[Clause] = set()
    for i in range(1, p + 1):
        successor = i % p + 1
        clauses.add(frozenset((-i, successor)))
    clauses.add(frozenset(range(1, p + 1)))
    clauses.add(frozenset(range(-p, 0)))
    assert len(clauses) == p + 2
    return frozenset(clauses)


def satisfies_clause(assignment: int, clause: Clause) -> bool:
    for literal in clause:
        value = bool(assignment >> (abs(literal) - 1) & 1)
        if value == (literal > 0):
            return True
    return False


def is_satisfiable(formula: Formula, variables: int) -> bool:
    return any(
        all(satisfies_clause(assignment, clause) for clause in formula)
        for assignment in range(1 << variables)
    )


def is_minimally_unsatisfiable(formula: Formula, variables: int) -> bool:
    if is_satisfiable(formula, variables):
        return False
    return all(is_satisfiable(formula - {clause}, variables) for clause in formula)


def inverse_extension(
    formula: Formula,
    selected: tuple[Clause, ...],
    common: Clause,
    overlaps: tuple[Clause, ...],
    fresh: int,
) -> Formula:
    sides = []
    for clause, overlap in zip(selected, overlaps, strict=True):
        tail = (clause - common) | overlap
        sides.append(frozenset({-fresh}) | tail)
    main = frozenset({fresh}) | common
    return frozenset((formula - set(selected)) | {main, *sides})


def dp(formula: Formula, variable: int) -> Formula:
    positive = [clause for clause in formula if variable in clause]
    negative = [clause for clause in formula if -variable in clause]
    untouched = {
        clause for clause in formula if variable not in clause and -variable not in clause
    }
    resolvents = set()
    for pos in positive:
        for neg in negative:
            candidate = (pos - {variable}) | (neg - {-variable})
            if not any(-literal in candidate for literal in candidate):
                resolvents.add(frozenset(candidate))
    return frozenset(untouched | resolvents)


def audit_inverse_constructor(p: int) -> int:
    formula = f_p(p)
    assert is_minimally_unsatisfiable(formula, p)
    clauses = tuple(sorted(formula, key=lambda c: (len(c), tuple(sorted(c)))))
    checked = 0
    for family_mask in range(1, 1 << len(clauses)):
        selected = tuple(
            clauses[i] for i in range(len(clauses)) if family_mask >> i & 1
        )
        intersection = set(selected[0])
        for clause in selected[1:]:
            intersection &= clause
        for common in powerset(tuple(sorted(intersection))):
            overlap_options = [tuple(powerset(tuple(sorted(common))))] * len(selected)
            for overlaps in itertools.product(*overlap_options):
                lifted = inverse_extension(formula, selected, common, overlaps, p + 1)
                assert dp(lifted, p + 1) == formula
                assert len(lifted) == len(formula) + 1
                assert is_minimally_unsatisfiable(lifted, p + 1)
                checked += 1
    return checked


def verify_certificate(data: dict) -> None:
    n = data["core_variables"]
    clauses = data["obstruction_clauses"]
    leaf = data["leaf_clause_length"]
    intersection = data["leaf_tail_intersection"]
    first = 2 * (leaf - 1) - intersection
    assert first == data["first_derived_clause_length"] == 6

    loss = data["maximum_loss_per_descendant_resolution"]
    binary = data["terminal_binary_clause_length"]
    descendants = (first - binary + loss - 1) // loss
    minimum_steps = 1 + descendants
    assert minimum_steps == data["minimum_reductions_for_binary_clause"] == 5

    maximum_p = n - minimum_steps
    assert maximum_p == data["maximum_terminal_p"] == 37
    assert data["excluded_p"] == list(range(maximum_p + 1, n))

    coverage = (n + leaf - 1) // leaf
    assert coverage == data["coverage_clauses_per_sign"] == 11
    witnesses = data["one_flip_avoiding_witnesses"]
    maximum_arity = clauses - coverage - witnesses
    assert maximum_arity == data["maximum_final_fan_arity"] == 30


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} CERTIFICATE.json")
    certificate = json.loads(Path(sys.argv[1]).read_text())
    verify_certificate(certificate)
    counts = {
        p: audit_inverse_constructor(p) for p in certificate["small_inverse_audit_p"]
    }
    print("small inverse audits:", ", ".join(f"F_{p}={count}" for p, count in counts.items()))
    print(
        "verified: inverse-step classification samples, "
        f"m<={certificate['maximum_final_fan_arity']}, "
        f"p<={certificate['maximum_terminal_p']}, "
        f"excluded={certificate['excluded_p']}"
    )


if __name__ == "__main__":
    main()
