"""Bounded independent-definition trial of the degree-only fixed-core family.

No cell quota, total-edge count, local edge count, or prior exclusion is used.
Solver output is exploratory until a model is directly checked or a proof is
replayed against the independently audited base. Generated files stay in a
fresh external directory. No historical theorem is imported as a premise.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import platform
import sys
from threading import Timer
from time import monotonic

from pysat import __version__ as pysat_version
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE))
from columns import complete_domains, decision_diagram


def load():
    rows = json.loads((SOURCE / 'PARTIAL.json').read_text())['rows']
    if len(rows) != 43:
        raise ValueError('order')
    pairs = list(combinations(range(43), 2))
    for u, row in enumerate(rows):
        if len(row) != 43 or row[u] != '-':
            raise ValueError('row/diagonal')
        for v in range(u + 1, 43):
            if row[v] not in '01.' or row[v] != rows[v][u]:
                raise ValueError('symmetry/alphabet')
            free = 1 <= u <= 22 and u not in (3, 9) and v >= 23
            if (row[v] == '.') != free:
                raise ValueError('scope')
    fixed = {p: rows[p[0]][p[1]] == '1' for p in pairs if rows[p[0]][p[1]] != '.'}
    variables = {p: i + 1 for i, p in enumerate(p for p in pairs if p not in fixed)}
    if len(fixed) != 503 or len(variables) != 400:
        raise ValueError('fixed/free counts')
    return rows, pairs, fixed, variables


def degree_bounds(v):
    return (22, 22) if v == 0 else ((21, 22) if v <= 22 else (20, 21))


def build():
    rows, pairs, fixed, variables = load()
    prohibitions = set()
    for vertices in combinations(range(43), 5):
        edges = list(combinations(vertices, 2))
        colors = {fixed[p] for p in edges if p in fixed}
        if len(colors) == 2:
            continue
        for color in colors or (False, True):
            prohibitions.add(tuple(variables[p] * (-1 if color else 1)
                                   for p in edges if p in variables))
    clauses = [list(c) for c in sorted(prohibitions)]
    pool = IDPool(start_from=401)
    blocks = []
    for v in range(43):
        incident = [p for p in pairs if v in p]
        known = sum(fixed[p] for p in incident if p in fixed)
        lits = [variables[p] for p in incident if p in variables]
        low, high = degree_bounds(v)
        low, high = low - known, high - known
        if high < 0 or low > len(lits):
            raise ValueError('fixed degrees infeasible')
        specs = []
        if high < len(lits):
            specs.append((lits, high))
        if low > 0:
            specs.append(([-x for x in lits], len(lits) - low))
        for signed, threshold in specs:
            added = CardEnc.atmost(signed, threshold, vpool=pool,
                                  encoding=EncType.seqcounter).clauses
            clauses.extend(added)
            blocks.append({'vertex': v, 'literals': signed, 'atmost': threshold,
                           'clauses': len(added)})
    return rows, fixed, variables, clauses, pool.top, len(prohibitions), blocks


def add_columns(fixed, variables, clauses, top):
    # These are discovery accelerators only. A final exclusion must replay
    # without them, or supply an independently checked domain reduction.
    rows, domains = complete_domains(set(), fixed, variables, clauses)
    added = []
    diagrams = {}
    for b, masks in domains.items():
        key = tuple(masks)
        if key not in diagrams:
            diagrams[key] = decision_diagram(masks, len(rows))
        root, nodes = diagrams[key]
        ids = {node: top + i + 1 for i, node in enumerate(nodes)}
        top += len(ids)

        def lit(node, positive=True):
            return bool(node) == positive if node in (0, 1) else ids[node] * (1 if positive else -1)

        def append(c):
            if not any(x is True for x in c):
                added.append([x for x in c if x is not False])

        for node, (j, lo, hi) in nodes.items():
            z, x = ids[node], variables[rows[j], b]
            append([-z, -x, lit(hi)])
            append([-z, x, lit(lo)])
            append([z, -x, lit(hi, False)])
            append([z, x, lit(lo, False)])
        append([lit(root)])
    return clauses + added, top, {'column_choices': sum(map(len, domains.values())),
                                  'bdd_clauses': len(added)}


def check_model(red, rows):
    adjacency = [set() for _ in range(43)]
    for u, v in red:
        adjacency[u].add(v)
        adjacency[v].add(u)
    for u in range(43):
        low, high = degree_bounds(u)
        if not low <= len(adjacency[u]) <= high:
            raise ValueError('decoded degree')
        for v in range(u + 1, 43):
            if rows[u][v] != '.' and ((v in adjacency[u]) != (rows[u][v] == '1')):
                raise ValueError('decoded fixed color')
    # Direct graph-neighbor intersections, not the CNF generator's five-sets.
    for color in (0, 1):
        neighbors = adjacency if color else [set(range(43)) - a - {v}
                                             for v, a in enumerate(adjacency)]

        def visit(chosen, available):
            if len(chosen) == 5:
                raise ValueError(('monochromatic five-set', color, chosen))
            while available:
                v = min(available)
                available.remove(v)
                visit(chosen + [v], available & neighbors[v])

        visit([], set(range(43)))
    return {'red_edges': len(red), 'degrees': dict(sorted(Counter(map(len, adjacency)).items()))}


def dimacs(path, clauses, top):
    with path.open('w') as stream:
        stream.write(f'p cnf {top} {len(clauses)}\n')
        for c in clauses:
            stream.write(' '.join(map(str, c)) + ' 0\n')
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--seconds', type=int, default=240)
    parser.add_argument('--columns', action='store_true')
    parser.add_argument('--generate-only', action='store_true')
    args = parser.parse_args()
    work = args.work.resolve()
    if SOURCE.parent == work or SOURCE.parent in work.parents:
        raise ValueError('generated state must be outside research source')
    work.mkdir(parents=True, exist_ok=False)
    start = monotonic()
    rows, fixed, variables, clauses, top, globals_, blocks = build()
    summary = {'python': platform.python_version(), 'pysat': pysat_version,
               'fixed': len(fixed), 'free': len(variables), 'global_clauses': globals_,
               'base_variables': top, 'base_clauses': len(clauses),
               'degree_blocks': len(blocks), 'solve_limit_seconds': args.seconds,
               'base_sha256': dimacs(work / 'base.cnf', clauses, top)}
    (work / 'degree_blocks.json').write_text(json.dumps(blocks, indent=2) + '\n')
    print(json.dumps(summary), flush=True)
    if args.columns:
        clauses, top, info = add_columns(fixed, variables, clauses, top)
        summary.update(info)
    summary.update({'variables': top, 'clauses': len(clauses),
                    'formula_sha256': dimacs(work / 'formula.cnf', clauses, top),
                    'generation_seconds': monotonic() - start})
    print(json.dumps(summary), flush=True)
    status = None
    if not args.generate_only:
        with Solver(name='glucose42', bootstrap_with=clauses, with_proof=True) as solver:
            timer = Timer(args.seconds, solver.interrupt)
            timer.start()
            try:
                status = solver.solve_limited(expect_interrupt=True)
            finally:
                timer.cancel()
            summary['status'] = 'SAT' if status else 'UNSAT' if status is False else 'UNKNOWN'
            if status is False:
                (work / 'proof.drat').write_text('\n'.join(solver.get_proof()) + '\n')
            elif status:
                model = set(solver.get_model())
                red = {p for p, color in fixed.items() if color} | {p for p, v in variables.items() if v in model}
                summary['direct_check'] = check_model(red, rows)
                (work / 'red_edges.json').write_text(json.dumps(sorted(red)) + '\n')
    summary['elapsed_seconds'] = monotonic() - start
    (work / 'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
