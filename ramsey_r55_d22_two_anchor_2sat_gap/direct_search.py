"""Direct discovery encoding for a degree-compatible width-two survivor.

For a nonroot A--B edge, diagonal status is the XOR of the endpoints'
incidences to partner 3.  Enumerating the at most sixteen partner-bit patterns
on each mixed five-set therefore gives a direct conditional encoding of every
monochromatic K5 having one or two diagonal edges.
"""
from __future__ import annotations

import argparse
from itertools import combinations, product
import json
from pathlib import Path
import threading
import time

from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
from sat_base import build_base, red_edges


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--solver", default="glucose42")
    args = parser.parse_args()
    started = time.monotonic()
    data = json.loads((HERE / "WITNESS.json").read_text())
    partner, fixed, variables, clauses = build_base(data)

    conditional = set()

    def prohibit(conditions):
        clause = set()
        for a, b, color in conditions:
            edge = tuple(sorted((a, b)))
            if edge in fixed:
                if fixed[edge] != color:
                    return
                continue
            literal = -variables[edge] if color else variables[edge]
            if -literal in clause:
                return
            clause.add(literal)
        conditional.add(tuple(sorted(clause)))

    a_vertices = [vertex for vertex in range(1, 23) if vertex != partner]
    b_vertices = list(range(23, 43))
    partner_a = {vertex: fixed[tuple(sorted((partner, vertex)))] for vertex in a_vertices}
    candidate_fives = 0
    conditioned_patterns = 0
    for a_size in range(1, 5):
        b_size = 5 - a_size
        for left in combinations(a_vertices, a_size):
            left_pairs = list(combinations(left, 2))
            for right in combinations(b_vertices, b_size):
                right_pairs = list(combinations(right, 2))
                possible_colors = [
                    color for color in (True, False)
                    if all(fixed[edge] == color for edge in left_pairs + right_pairs)
                ]
                if not possible_colors:
                    continue
                candidate_fives += 1
                for bits in product((False, True), repeat=b_size):
                    diagonal_count = sum(
                        partner_a[a] != bit for a in left for bit in bits
                    )
                    if diagonal_count not in (1, 2):
                        continue
                    conditioned_patterns += 1
                    root_conditions = [(partner, b, bit) for b, bit in zip(right, bits)]
                    subset = left + right
                    for color in possible_colors:
                        prohibit(root_conditions + [(a, b, color) for a, b in combinations(subset, 2)])

    clauses.extend(map(list, conditional))
    print(json.dumps({
        "base_clauses": len(clauses) - len(conditional),
        "candidate_fives": candidate_fives,
        "conditioned_patterns": conditioned_patterns,
        "conditional_clauses": len(conditional),
        "variables": len(variables),
        "generation_seconds": round(time.monotonic() - started, 6),
    }, sort_keys=True), flush=True)

    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        remaining = max(0.001, args.seconds - (time.monotonic() - started))
        timer = threading.Timer(remaining, solver.interrupt)
        timer.start()
        answer = solver.solve_limited(expect_interrupt=True)
        timer.cancel()
        solver.clear_interrupt()
        output = {
            "status": "SAT" if answer is True else ("UNSAT_NO_PROOF" if answer is False else "TIMEOUT"),
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "stats": solver.accum_stats(),
        }
        if answer:
            red = red_edges(solver.get_model(), fixed, variables)
            output["cross_rows"] = [
                "".join("1" if (i + 1, j + 23) in red else "0" for j in range(20))
                for i in range(22)
            ]
        print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
