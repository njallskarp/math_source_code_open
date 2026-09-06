#!/usr/bin/env python3
"""Clean-room audit of the Paley(41) switching obstruction.

The input is only the researcher's compact DIMACS obstruction.  This checker
does not read the researcher's DRAT trace or import any of their Python code.
It checks every clause against the physical switched Paley graph, then proves
the resulting CNF unsatisfiable with a deterministic exhaustive DPLL search.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


EXPECTED_INPUT_SHA256 = "67eb55fbd11e5973a23e5a0f58cb37ceda4d763fc17d4984e45bbf2bc34c5005"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse_dimacs(path: Path) -> tuple[tuple[tuple[int, ...], ...], str]:
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    require(digest == EXPECTED_INPUT_SHA256, "unexpected obstruction SHA-256")
    clauses: list[tuple[int, ...]] = []
    variables = expected = None
    for number, raw_line in enumerate(raw.decode("ascii").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            require(variables is None and not clauses, f"misplaced header at line {number}")
            words = line.split()
            require(len(words) == 4 and words[:2] == ["p", "cnf"], "bad DIMACS header")
            variables, expected = map(int, words[2:])
            continue
        require(variables is not None, "clause before header")
        values = list(map(int, line.split()))
        require(values and values[-1] == 0 and 0 not in values[:-1],
                f"bad clause terminator at line {number}")
        clause = tuple(values[:-1])
        require(all(1 <= abs(lit) <= variables for lit in clause),
                f"out-of-range literal at line {number}")
        require(len({abs(lit) for lit in clause}) == len(clause),
                f"repeated variable at line {number}")
        require(not any(-lit in clause for lit in clause), f"tautology at line {number}")
        clauses.append(clause)
    require(variables == 123, "expected the declared full-family variable range")
    require(expected == len(clauses), "DIMACS clause-count mismatch")
    require(len(set(clauses)) == len(clauses), "duplicate input clause")
    require(all(abs(lit) <= 40 for clause in clauses for lit in clause),
            "compact obstruction unexpectedly uses a non-core variable")
    return tuple(clauses), digest


def paley_edge(u: int, v: int) -> int:
    """Quadratic-character edge test, independently using Euler's criterion."""
    require(u != v, "loops are not graph edges")
    return int(pow((u - v) % 41, 20, 41) == 1)


def physical_audit(clauses: tuple[tuple[int, ...], ...]) -> dict[str, object]:
    widths: Counter[int] = Counter()
    colors: Counter[int] = Counter()
    vertices_used: set[int] = set()
    witnesses = []
    for index, clause in enumerate(clauses):
        require(len(clause) in (4, 5), f"clause {index} has nonphysical width")
        switch = {abs(lit): int(lit < 0) for lit in clause}
        if len(clause) == 4:
            switch[0] = 0
        require(len(switch) == 5, f"clause {index} does not name a five-set")
        vertices = tuple(sorted(switch))
        edge_colors = {
            paley_edge(u, v) ^ switch[u] ^ switch[v]
            for u, v in combinations(vertices, 2)
        }
        require(len(edge_colors) == 1, f"clause {index} is not a monochromatic K5 event")
        color = edge_colors.pop()
        widths[len(clause)] += 1
        colors[color] += 1
        vertices_used.update(vertices)
        if len(witnesses) < 2:
            witnesses.append({"vertices": list(vertices), "color": color})

    # These graph facts are not required by DPLL, but catch convention errors.
    degrees = [sum(paley_edge(u, v) for v in range(41) if v != u) for u in range(41)]
    require(set(degrees) == {20}, "the independently decoded graph is not Paley(41)")
    require(vertices_used == set(range(41)), "some physical core vertex is never audited")
    return {
        "clauses": len(clauses),
        "widths": {str(k): widths[k] for k in sorted(widths)},
        "colors": {"blue": colors[0], "red": colors[1]},
        "paley_degrees": {"minimum": min(degrees), "maximum": max(degrees)},
        "sample_clause_witnesses": witnesses,
    }


def canonical(clauses: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(set(clauses), key=lambda row: (len(row), row)))


def set_literal(
    clauses: tuple[tuple[int, ...], ...], literal: int
) -> tuple[tuple[tuple[int, ...], ...] | None, bool]:
    """Set one literal true; return (simplified clauses, contradiction)."""
    reduced: list[tuple[int, ...]] = []
    opposite = -literal
    for clause in clauses:
        if literal in clause:
            continue
        if opposite not in clause:
            reduced.append(clause)
            continue
        shorter = tuple(x for x in clause if x != opposite)
        if not shorter:
            return None, True
        reduced.append(shorter)
    return canonical(reduced), False


def propagate(
    clauses: tuple[tuple[int, ...], ...]
) -> tuple[tuple[tuple[int, ...], ...] | None, tuple[int, ...], bool]:
    assigned: dict[int, int] = {}
    units: list[int] = []
    current = clauses
    while True:
        new_units = sorted(
            (row[0] for row in current if len(row) == 1),
            key=lambda lit: (abs(lit), lit < 0),
        )
        if not new_units:
            return current, tuple(units), False
        for literal in new_units:
            variable, value = abs(literal), int(literal > 0)
            if variable in assigned:
                if assigned[variable] != value:
                    return None, tuple(units), True
                continue
            assigned[variable] = value
            units.append(literal)
            simplified, contradiction = set_literal(current, literal)
            if contradiction:
                return None, tuple(units), True
            assert simplified is not None
            current = simplified


def choose_variable(clauses: tuple[tuple[int, ...], ...]) -> int:
    """Deterministic Jeroslow-Wang-style score, represented by exact integers."""
    max_width = max(map(len, clauses))
    score: Counter[int] = Counter()
    for clause in clauses:
        weight = 1 << (max_width - len(clause))
        for literal in clause:
            score[abs(literal)] += weight
    return min(score, key=lambda variable: (-score[variable], variable))


@dataclass
class SearchStats:
    recursive_states: int = 0
    decisions: int = 0
    contradiction_leaves: int = 0
    satisfying_leaves: int = 0
    memo_hits: int = 0
    propagated_literals: int = 0
    maximum_depth: int = 0


def exhaustive_dpll(clauses: tuple[tuple[int, ...], ...]) -> tuple[bool, dict[str, int], str]:
    """Return satisfiability, exact search statistics, and a deterministic tree hash."""
    memo: dict[tuple[tuple[int, ...], ...], tuple[bool, bytes]] = {}
    stats = SearchStats()

    def visit(state: tuple[tuple[int, ...], ...], depth: int) -> tuple[bool, bytes]:
        stats.recursive_states += 1
        stats.maximum_depth = max(stats.maximum_depth, depth)
        reduced, units, contradiction = propagate(state)
        stats.propagated_literals += len(units)
        unit_bytes = (",".join(map(str, units))).encode("ascii")
        if contradiction:
            stats.contradiction_leaves += 1
            return False, sha256(b"C|" + unit_bytes).digest()
        assert reduced is not None
        if not reduced:
            stats.satisfying_leaves += 1
            return True, sha256(b"S|" + unit_bytes).digest()
        if reduced in memo:
            stats.memo_hits += 1
            satisfiable, child_hash = memo[reduced]
            return satisfiable, sha256(b"M|" + unit_bytes + b"|" + child_hash).digest()

        variable = choose_variable(reduced)
        stats.decisions += 1
        children = []
        for literal in (-variable, variable):
            child, child_contradiction = set_literal(reduced, literal)
            if child_contradiction:
                stats.contradiction_leaves += 1
                children.append((False, sha256(f"C|{literal}".encode("ascii")).digest()))
            else:
                assert child is not None
                children.append(visit(child, depth + 1))
            if children[-1][0]:
                # A satisfying witness is enough to refute the claimed obstruction.
                digest = sha256(b"W|" + unit_bytes + b"|" + children[-1][1]).digest()
                memo[reduced] = (True, digest)
                return True, digest
        digest = sha256(
            b"U|" + unit_bytes + f"|{variable}|".encode("ascii")
            + children[0][1] + children[1][1]
        ).digest()
        memo[reduced] = (False, digest)
        return False, digest

    satisfiable, root_hash = visit(canonical(list(clauses)), 0)
    return satisfiable, vars(stats), root_hash.hex()


def algorithm_controls() -> dict[str, int]:
    """Compare DPLL with literal brute force on 512 small CNFs."""
    pool = (
        (1,), (-1,), (2,), (-2,), (3,), (-3,),
        (1, 2), (-1, -2), (1, -2, 3),
    )
    checked = satisfiable = unsatisfiable = 0
    for selector in range(1 << len(pool)):
        formula = tuple(pool[i] for i in range(len(pool)) if selector >> i & 1)
        brute = any(
            all(
                any(bool(mask >> (abs(lit) - 1) & 1) == (lit > 0) for lit in clause)
                for clause in formula
            )
            for mask in range(1 << 3)
        )
        obtained, _, _ = exhaustive_dpll(formula)
        require(obtained == brute, f"DPLL control mismatch for selector {selector}")
        checked += 1
        satisfiable += int(brute)
        unsatisfiable += int(not brute)
    return {
        "small_formulas_checked": checked,
        "satisfiable": satisfiable,
        "unsatisfiable": unsatisfiable,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("obstruction", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    clauses, digest = parse_dimacs(args.obstruction)
    physical = physical_audit(clauses)
    satisfiable, search, tree_hash = exhaustive_dpll(clauses)
    require(not satisfiable, "counterexample switch found: obstruction is satisfiable")
    report = {
        "status": "INDEPENDENTLY_VERIFIED_PALEY41_SWITCH_OBSTRUCTION",
        "input_sha256": digest,
        "physical_audit": physical,
        "search": search,
        "search_tree_sha256": tree_hash,
        "algorithm_controls": algorithm_controls(),
        "method": "physical Euler-criterion audit plus exhaustive deterministic DPLL",
        "certificate_imported": False,
        "target_code_imported": False,
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
