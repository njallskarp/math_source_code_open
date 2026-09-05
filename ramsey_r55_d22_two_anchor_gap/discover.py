"""Discovery-only CEGAR search for a two-anchor unit-conflict-free witness.

The SAT model enforces the two complete anchor-neighborhood constraints and
the tight degree/edge profile.  A refinement clause is added for every pair of
opposite monochromatic K5-minus-one-edge configurations whose missing edge is
unseen by both anchors.  Any emitted model still requires definition-level
verification independent of this file and of the SAT solver.
"""
from __future__ import annotations

import argparse
import base64
from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path
import threading
import time

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
WITNESS = HERE / "WITNESS.json"


def decode_graph6(encoded):
    data = base64.b64decode(encoded)
    n = data[0] - 63
    bits = [(value - 63) >> bit & 1 for value in data[1:] for bit in range(5, -1, -1)]
    edges = {edge for edge, flag in zip(((i, j) for j in range(1, n) for i in range(j)), bits) if flag}
    return n, edges


def build_base(data):
    _, red_core = decode_graph6(data["red_core_parent_graph6_base64"])
    red_core -= set(map(tuple, data["red_core_delete_edges"]))
    _, blue_core = decode_graph6(data["blue_core_graph6_base64"])
    partner = 3
    if sum(partner - 1 in edge for edge in red_core) < 10:
        raise ValueError("partner is not eligible")

    pool = IDPool()
    fixed = {}
    variables = {}
    for a, b in combinations(range(43), 2):
        edge = (a, b)
        if a == 0:
            fixed[edge] = b <= 22
        elif b <= 22:
            fixed[edge] = (a - 1, b - 1) in red_core
        elif a <= 22:
            variables[edge] = pool.id(edge)
        else:
            fixed[edge] = (a - 23, b - 23) not in blue_core

    clauses = []

    def prohibit(conditions):
        clause = set()
        for a, b, color in conditions:
            edge = tuple(sorted((a, b)))
            if edge in fixed:
                if fixed[edge] != color:
                    return
            else:
                literal = -variables[edge] if color else variables[edge]
                if -literal in clause:
                    return
                clause.add(literal)
        clauses.append(sorted(clause))

    for root in (0, partner):
        for color in (True, False):
            possible = [
                vertex for vertex in range(43)
                if vertex != root
                and fixed.get(tuple(sorted((root, vertex))), color) == color
            ]
            for size, target_color in ((4, color), (5, not color)):
                for subset in combinations(possible, size):
                    prohibit(
                        [(a, b, target_color) for a, b in combinations(subset, 2)]
                        + [(root, vertex, color) for vertex in subset]
                    )

    for vertex in range(43):
        fixed_red = sum(color for edge, color in fixed.items() if vertex in edge)
        literals = [var for edge, var in variables.items() if vertex in edge]
        low, high = (22, 22) if vertex == 0 else ((21, 22) if vertex <= 22 else (20, 21))
        for bound, negate in ((high - fixed_red, False), (len(literals) - (low - fixed_red), True)):
            if 0 <= bound < len(literals):
                encoded = CardEnc.atmost(
                    [-literal for literal in literals] if negate else literals,
                    bound=bound,
                    vpool=pool,
                    encoding=EncType.seqcounter,
                )
                clauses.extend(encoded.clauses)
            elif bound < 0:
                clauses.append([])

    cross = [var for (a, b), var in variables.items() if a <= 22 < b]
    clauses.extend(CardEnc.equals(cross, bound=232, vpool=pool, encoding=EncType.totalizer).clauses)
    return partner, fixed, variables, pool, clauses


def red_edges(model, fixed, variables):
    positive = set(model)
    return {edge for edge, color in fixed.items() if color} | {
        edge for edge, var in variables.items() if var in positive
    }


def opposite_near_pairs(red, partner):
    def is_red(a, b):
        return tuple(sorted((a, b))) in red

    vertices = [vertex for vertex in range(43) if vertex not in (0, partner)]
    signature = {vertex: (is_red(0, vertex), is_red(partner, vertex)) for vertex in vertices}
    diagonal = {
        edge for edge in combinations(vertices, 2)
        if signature[edge[0]][0] != signature[edge[1]][0]
        and signature[edge[0]][1] != signature[edge[1]][1]
    }
    near = {True: defaultdict(list), False: defaultdict(list)}
    for subset in combinations(vertices, 5):
        pairs = list(combinations(subset, 2))
        holes = [edge for edge in pairs if edge in diagonal]
        if len(holes) != 1:
            continue
        hole = holes[0]
        support = [edge for edge in pairs if edge != hole]
        if all(edge in red for edge in support):
            near[True][hole].append(subset)
        if all(edge not in red for edge in support):
            near[False][hole].append(subset)
    conflicts = []
    for hole in sorted(diagonal):
        for red_set in near[True][hole]:
            for blue_set in near[False][hole]:
                conflicts.append((hole, red_set, blue_set, signature))
    return len(diagonal), conflicts


def refinement_clause(conflict, fixed, variables, partner):
    hole, red_set, blue_set, signature = conflict
    conditions = []
    conditions.extend((a, b, True) for a, b in combinations(red_set, 2) if (a, b) != hole)
    conditions.extend((a, b, False) for a, b in combinations(blue_set, 2) if (a, b) != hole)
    for vertex in set(red_set) | set(blue_set):
        conditions.append((partner, vertex, signature[vertex][1]))

    clause = set()
    for a, b, color in conditions:
        edge = tuple(sorted((a, b)))
        if edge in fixed:
            if fixed[edge] != color:
                raise ValueError("inconsistent fixed refinement condition")
            continue
        literal = -variables[edge] if color else variables[edge]
        if -literal in clause:
            raise ValueError("inconsistent variable refinement condition")
        clause.add(literal)
    if not clause:
        raise ValueError("empty refinement clause")
    return tuple(sorted(clause))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--max-rounds", type=int, default=1000)
    args = parser.parse_args()
    started = time.monotonic()
    data = json.loads(WITNESS.read_text())
    partner, fixed, variables, pool, clauses = build_base(data)
    base_clause_count = len(clauses)
    seen_refinements = set()
    result = {
        "status": "TIMEOUT",
        "base_variables": len(variables),
        "base_clauses": base_clause_count,
        "rounds": 0,
        "refinement_clauses": 0,
    }

    with Solver(name="glucose42", bootstrap_with=clauses) as solver:
        for round_number in range(1, args.max_rounds + 1):
            remaining = args.seconds - (time.monotonic() - started)
            if remaining <= 0:
                break
            timer = threading.Timer(remaining, solver.interrupt)
            timer.start()
            answer = solver.solve_limited(expect_interrupt=True)
            timer.cancel()
            solver.clear_interrupt()
            result["rounds"] = round_number
            if answer is None:
                break
            if answer is False:
                result["status"] = "UNSAT_REFINEMENT_ENCODING"
                break
            red = red_edges(solver.get_model(), fixed, variables)
            diagonal_count, conflicts = opposite_near_pairs(red, partner)
            if not conflicts:
                rows = [
                    "".join("1" if (1 + i, 23 + j) in red else "0" for j in range(20))
                    for i in range(22)
                ]
                result.update(
                    status="SAT_UNIT_CONFLICT_FREE",
                    partner=partner,
                    diagonal_edges=diagonal_count,
                    cross_rows=rows,
                )
                break
            added = 0
            for conflict in conflicts:
                clause = refinement_clause(conflict, fixed, variables, partner)
                if clause in seen_refinements:
                    continue
                seen_refinements.add(clause)
                solver.add_clause(list(clause))
                added += 1
            if not added:
                raise RuntimeError("conflicting model survived all existing refinements")
            result["refinement_clauses"] = len(seen_refinements)
            print(
                json.dumps(
                    {
                        "round": round_number,
                        "conflict_pairs": len(conflicts),
                        "new_refinements": added,
                        "total_refinements": len(seen_refinements),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    result["refinement_clauses"] = len(seen_refinements)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
