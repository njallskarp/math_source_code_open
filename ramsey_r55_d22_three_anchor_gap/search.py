"""Discovery-only search for a degree-compatible three-anchor survivor.

The four neighborhoods of anchors 0 and 3 are fixed by the preceding exact
witness.  Only their 210 antipodal (hence doubly unseen) edges may change.  We
promote vertex 1 to a third full anchor, enforce its two exact local Ramsey
conditions, and iteratively eliminate monochromatic K5s whose ten edges are
all seen by at least one of the six anchor neighborhoods.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
import argparse
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
def prior_red_edges():
    from verify import construct

    data = json.loads((HERE / "BASE_WITNESS.json").read_text())
    return construct(data)


def build_formula(root, use_local=True, use_degrees=True, use_edge_count=True):
    old_red = prior_red_edges()
    outside = [vertex for vertex in range(43) if vertex not in (0, 3)]
    old_bit = {
        vertex: (
            int(tuple(sorted((0, vertex))) in old_red),
            int(tuple(sorted((3, vertex))) in old_red),
        )
        for vertex in outside
    }
    diagonal = {
        edge
        for edge in combinations(outside, 2)
        if all(old_bit[edge[0]][i] != old_bit[edge[1]][i] for i in range(2))
    }
    assert len(diagonal) == 210

    pool = IDPool()
    variables = {edge: pool.id(edge) for edge in sorted(diagonal)}
    fixed = {
        edge: edge in old_red
        for edge in combinations(range(43), 2)
        if edge not in diagonal
    }
    local_clauses = []

    def prohibit(conditions):
        """Forbid a conjunction of requested edge colors."""
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
        local_clauses.append(sorted(clause))

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
                    [(a, b, target_color) for a, b in combinations(subset, 2)]
                    + [(root, vertex, color) for vertex in subset]
                )

    degree_clauses = []
    for vertex in range(43):
        fixed_red = sum(color for edge, color in fixed.items() if vertex in edge)
        literals = [literal for edge, literal in variables.items() if vertex in edge]
        low, high = (22, 22) if vertex == 0 else ((21, 22) if vertex <= 22 else (20, 21))
        for bound, negate in ((high - fixed_red, False), (len(literals) - (low - fixed_red), True)):
            if 0 <= bound < len(literals):
                degree_clauses.extend(
                    CardEnc.atmost(
                        [-literal for literal in literals] if negate else literals,
                        bound=bound,
                        vpool=pool,
                        encoding=EncType.seqcounter,
                    ).clauses
                )
            elif bound < 0:
                degree_clauses.append([])

    required_diagonal_red = 452 - sum(fixed.values())
    edge_count_clauses = (
        CardEnc.equals(
            list(variables.values()),
            bound=required_diagonal_red,
            vpool=pool,
            encoding=EncType.totalizer,
        ).clauses
    )
    clauses = (
        (local_clauses if use_local else [])
        + (degree_clauses if use_degrees else [])
        + (edge_count_clauses if use_edge_count else [])
    )
    counts = {
        "local": len(local_clauses),
        "degree": len(degree_clauses),
        "edge_count": len(edge_count_clauses),
    }
    return fixed, variables, clauses, pool.top, required_diagonal_red, counts


def red_from_model(model, fixed, variables):
    positive = set(model)
    return {edge for edge, color in fixed.items() if color} | {
        edge for edge, literal in variables.items() if literal in positive
    }


def fully_exposed_defects(red, root):
    adjacency = [[False] * 43 for _ in range(43)]
    for left, right in red:
        adjacency[left][right] = adjacency[right][left] = True
    roots = (0, 3, root)
    outside = [vertex for vertex in range(43) if vertex not in roots]
    signature = {
        vertex: tuple(int(adjacency[anchor][vertex]) for anchor in roots)
        for vertex in outside
    }
    omitted = {
        edge
        for edge in combinations(outside, 2)
        if all(signature[edge[0]][i] != signature[edge[1]][i] for i in range(3))
    }
    defects = []
    profile = Counter()
    for subset in combinations(outside, 5):
        pairs = tuple(combinations(subset, 2))
        colors = {adjacency[a][b] for a, b in pairs}
        if len(colors) == 1:
            color = colors.pop()
            width = sum(edge in omitted for edge in pairs)
            profile[("R" if color else "B", width)] += 1
            if width == 0:
                defects.append((color, subset))
    return signature, omitted, profile, defects


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=int, default=1)
    parser.add_argument("--relax-degrees", action="store_true")
    parser.add_argument("--relax-edge-count", action="store_true")
    parser.add_argument("--relax-local", action="store_true")
    args = parser.parse_args()
    if args.root in (0, 3) or not 0 <= args.root < 43:
        parser.error("root must be a vertex other than 0 or 3")
    fixed, variables, clauses, top, target, counts = build_formula(
        args.root,
        use_local=not args.relax_local,
        use_degrees=not args.relax_degrees,
        use_edge_count=not args.relax_edge_count,
    )
    print(json.dumps({
        "base_clauses": len(clauses),
        "clause_groups": counts,
        "diagonal_red_target": target,
        "primary_variables": len(variables),
        "root": args.root,
        "total_variables": top,
    }, sort_keys=True))
    learned = set()
    with Solver(name="glucose42", bootstrap_with=clauses) as solver:
        for iteration in range(1, 1001):
            if not solver.solve():
                print(json.dumps({"iteration": iteration, "status": "UNSAT"}, sort_keys=True))
                return
            red = red_from_model(solver.get_model(), fixed, variables)
            signature, omitted, profile, defects = fully_exposed_defects(red, args.root)
            print(json.dumps({
                "defect_profile": [[c, w, n] for (c, w), n in sorted(profile.items())],
                "fully_exposed_defects": len(defects),
                "iteration": iteration,
                "omitted_edges": len(omitted),
            }, sort_keys=True))
            if not defects:
                rows = [
                    "".join("1" if (a, b) in red else "0" for b in range(23, 43))
                    for a in range(1, 23)
                ]
                cells = Counter(signature.values())
                print(json.dumps({
                    "cell_sizes": [["".join(map(str, bits)), cells[bits]] for bits in sorted(cells)],
                    "cross_rows": rows,
                    "status": "SAT_THREE_ANCHOR_SURVIVOR",
                }, indent=2, sort_keys=True))
                return
            added = 0
            for color, subset in defects:
                clause = tuple(sorted(
                    (-variables[edge] if color else variables[edge])
                    for edge in combinations(subset, 2)
                    if edge in variables
                ))
                assert clause
                if clause not in learned:
                    solver.add_clause(clause)
                    learned.add(clause)
                    added += 1
            print(json.dumps({"added_global_k5_clauses": added, "learned_total": len(learned)}, sort_keys=True))
    raise RuntimeError("iteration limit")


if __name__ == "__main__":
    main()
