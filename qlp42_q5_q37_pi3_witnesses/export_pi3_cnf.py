#!/usr/bin/env python3
"""Export the sparse QLP-42 pi^3 encoding as deterministic pure DIMACS CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import solve_pi3_mq


class Recorder:
    def __init__(self) -> None:
        self.clauses: list[list[int]] = []
        self.xors: list[tuple[list[int], bool]] = []

    def add_clause(self, literals: list[int]) -> None:
        self.clauses.append(list(literals))

    def add_xor_clause(self, variables: list[int], rhs: bool) -> None:
        self.xors.append((list(variables), rhs))


def xor_gate(left: int, right: int, output: int) -> list[list[int]]:
    """Return clauses equivalent to output = left XOR right."""
    return [
        [left, right, -output],
        [-left, -right, -output],
        [left, -right, output],
        [-left, right, output],
    ]


def check_xor_gate() -> None:
    for left in (False, True):
        for right in (False, True):
            for output in (False, True):
                assignment = {1: left, 2: right, 3: output}
                satisfied = all(
                    any(
                        assignment[abs(literal)] == (literal > 0)
                        for literal in clause
                    )
                    for clause in xor_gate(1, 2, 3)
                )
                assert satisfied == (output == (left ^ right))


def expand_xors(
    variables: int,
    clauses: list[list[int]],
    xors: list[tuple[list[int], bool]],
) -> tuple[int, list[list[int]]]:
    result = [list(clause) for clause in clauses]
    next_variable = variables
    for xor_variables, rhs in xors:
        if not xor_variables:
            if rhs:
                result.append([])
            continue
        accumulator = xor_variables[0]
        for right in xor_variables[1:]:
            next_variable += 1
            result.extend(xor_gate(accumulator, right, next_variable))
            accumulator = next_variable
        result.append([accumulator if rhs else -accumulator])
    return next_variable, result


def write_dimacs(path: Path, variables: int, clauses: list[list[int]]) -> str:
    digest = hashlib.sha256()
    with path.open("w", encoding="ascii", newline="\n") as handle:
        header = f"p cnf {variables} {len(clauses)}\n"
        handle.write(header)
        digest.update(header.encode("ascii"))
        for clause in clauses:
            line = " ".join(map(str, clause)) + " 0\n"
            handle.write(line)
            digest.update(line.encode("ascii"))
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("q", type=int, choices=(5, 37))
    parser.add_argument("orbit", type=int, choices=range(18))
    parser.add_argument("case", type=int, choices=range(6))
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    check_xor_gate()

    recorder = Recorder()
    original_solver = solve_pi3_mq.Solver
    solve_pi3_mq.Solver = lambda threads=1: recorder  # type: ignore[assignment]
    try:
        encoding, cells, support = solve_pi3_mq.encode_problem(
            args.q, args.orbit, args.case
        )
    finally:
        solve_pi3_mq.Solver = original_solver
    assert encoding.solver is recorder
    variables, clauses = expand_xors(
        encoding.variables, recorder.clauses, recorder.xors
    )
    cnf_sha256 = write_dimacs(args.cnf, variables, clauses)
    metadata = {
        "q": args.q,
        "orbit": args.orbit,
        "case": args.case,
        "support": [f"{support[0]:06x}", f"{support[1]:06x}"],
        "cell_variables": cells,
        "native_variables": encoding.variables,
        "native_clauses": len(recorder.clauses),
        "native_xors": len(recorder.xors),
        "cnf_variables": variables,
        "cnf_clauses": len(clauses),
        "cnf_sha256": cnf_sha256,
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"q={args.q};orbit={args.orbit};case={args.case};"
        f"native_variables={encoding.variables};"
        f"native_clauses={len(recorder.clauses)};"
        f"native_xors={len(recorder.xors)};"
        f"cnf_variables={variables};cnf_clauses={len(clauses)};"
        f"cnf_sha256={cnf_sha256}"
    )


if __name__ == "__main__":
    main()
