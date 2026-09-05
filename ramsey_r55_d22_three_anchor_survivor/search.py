"""Discovery search for three simultaneous valid anchors in the d=22 branch."""
from __future__ import annotations

from itertools import combinations
import argparse
import json
from pathlib import Path
import sys

from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "ramsey_r55_d22_three_anchor_gap"
sys.path.insert(0, str(HERE.parent / "ramsey_r55_d22_two_anchor_2sat_gap"))
from sat_base import build_base, red_edges


def add_anchor_clauses(root, fixed, variables):
    clauses = []

    def prohibit(conditions):
        clause = set()
        for left, right, color in conditions:
            edge = tuple(sorted((left, right)))
            if edge in fixed:
                if fixed[edge] != color:
                    return
            else:
                literal = -variables[edge] if color else variables[edge]
                if -literal in clause:
                    return
                clause.add(literal)
        clauses.append(sorted(clause))

    for color in (True, False):
        possible = [
            vertex
            for vertex in range(43)
            if vertex != root
            and fixed.get(tuple(sorted((root, vertex))), color) == color
        ]
        for size, target_color in ((4, color), (5, not color)):
            for subset in combinations(possible, size):
                prohibit(
                    [(left, right, target_color) for left, right in combinations(subset, 2)]
                    + [(root, vertex, color) for vertex in subset]
                )
    return clauses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--third", type=int, default=9)
    parser.add_argument("--solver", default="glucose42")
    args = parser.parse_args()
    if args.third in (0, 3) or not 1 <= args.third <= 22:
        parser.error("third anchor must lie in A and differ from 3")
    data = json.loads((BASE / "BASE_WITNESS.json").read_text())
    partner, fixed, variables, clauses = build_base(data)
    assert partner == 3 and len(variables) == 440
    third_clauses = add_anchor_clauses(args.third, fixed, variables)
    print(json.dumps({
        "base_clauses": len(clauses),
        "third": args.third,
        "third_clauses": len(third_clauses),
        "variables": len(variables),
    }, sort_keys=True))
    with Solver(name=args.solver, bootstrap_with=clauses + third_clauses) as solver:
        status = solver.solve()
        print(json.dumps({"status": "SAT" if status else "UNSAT"}, sort_keys=True))
        if not status:
            return
        red = red_edges(solver.get_model(), fixed, variables)
    rows = [
        "".join("1" if (left, right) in red else "0" for right in range(23, 43))
        for left in range(1, 23)
    ]
    print(json.dumps({"cross_rows": rows, "third": args.third}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
