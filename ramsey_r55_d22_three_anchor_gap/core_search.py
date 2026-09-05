"""Discovery-only extraction of a small exact third-anchor contradiction."""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations
import argparse
import json

from pysat.solvers import Solver

from search import build_formula


def local_clauses_with_origins(root):
    fixed, variables, _clauses, _top, _target, _counts = build_formula(
        root, use_local=False, use_degrees=False, use_edge_count=False
    )
    origins = defaultdict(list)

    def prohibit(conditions, origin):
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
        origins[tuple(sorted(clause))].append(origin)

    for neighborhood_color in (True, False):
        possible = [
            vertex
            for vertex in range(43)
            if vertex != root
            and fixed.get(tuple(sorted((root, vertex))), neighborhood_color) == neighborhood_color
        ]
        for size, target_color in ((4, neighborhood_color), (5, not neighborhood_color)):
            for subset in combinations(possible, size):
                prohibit(
                    [(a, b, target_color) for a, b in combinations(subset, 2)]
                    + [(root, vertex, neighborhood_color) for vertex in subset],
                    {
                        "anchor_color": "R" if neighborhood_color else "B",
                        "forbidden_color": "R" if target_color else "B",
                        "subset": list(subset),
                    },
                )
    return fixed, variables, origins


def subset_minimal_core(clauses, variable_top):
    selector = {clause: variable_top + index + 1 for index, clause in enumerate(clauses)}
    with Solver(name="glucose42") as solver:
        for clause in clauses:
            solver.add_clause(list(clause) + [selector[clause]])
        assumptions = [-selector[clause] for clause in clauses]
        assert not solver.solve(assumptions=assumptions)
        core_set = set(solver.get_core())
        active = [clause for clause in clauses if -selector[clause] in core_set]
        index = 0
        while index < len(active):
            trial = active[:index] + active[index + 1:]
            trial_assumptions = [-selector[clause] for clause in trial]
            if not solver.solve(assumptions=trial_assumptions):
                active = trial
            else:
                index += 1
    return active


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=int, default=1)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    roots = [root for root in range(43) if root not in (0, 3)] if args.all else [args.root]
    records = []
    for root in roots:
        _fixed, variables, origins = local_clauses_with_origins(root)
        clauses = sorted(origins, key=lambda clause: (len(clause), clause))
        core = subset_minimal_core(clauses, max(variables.values()))
        inverse = {literal: edge for edge, literal in variables.items()}
        used = sorted({abs(literal) for clause in core for literal in clause})
        records.append({
            "clauses": [list(clause) for clause in core],
            "core_variables": [[literal, list(inverse[literal])] for literal in used],
            "root": root,
            "unique_local_clauses": len(clauses),
        })
    output = {
        "format": "r55-d22-three-anchor-local-cores-v1",
        "records": records,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
