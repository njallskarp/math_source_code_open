"""Solver-free audit of the final CNF; imports no producer or PySAT code."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

BASE = Path(__file__).parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load():
    rows = json.loads((BASE / 'PARTIAL.json').read_text())['rows']
    profile = json.loads((BASE / 'PROFILE.json').read_text())
    require(profile['anchors'] == [0, 3, 9], 'anchor order')
    require([len(r) for r in profile['cell_red_upper_triangle']] == list(range(8, 0, -1)), 'quota shape')
    require(len(rows) == 43, 'order')
    for u, row in enumerate(rows):
        require(len(row) == 43 and row[u] == '-', 'row or diagonal')
        for v, c in enumerate(row):
            if u != v:
                require(c in '01.' and c == rows[v][u], 'partial matrix symmetry')
                expected_free = (1 <= min(u, v) <= 22 and max(u, v) >= 23 and
                                 min(u, v) not in (3, 9))
                require((c == '.') == expected_free, 'fixed-core scope')
    free = {p: i + 1 for i, p in enumerate(p for p in combinations(range(43), 2)
                                         if rows[p[0]][p[1]] == '.')}
    cells = [[] for _ in range(8)]
    for v in range(43):
        if v not in (0, 3, 9):
            signature = int(''.join(rows[r][v] for r in (0, 3, 9)), 2)
            cells[signature].append(v)
    require(list(map(len, cells)) == profile['cell_sizes'], 'cell sizes')
    return rows, profile, free, cells


def clique_rows(rows, free):
    """Generate possible monochromatic cliques by adjacency intersections."""
    result = set()
    for color in '01':
        adj = [sum(1 << v for v in range(43) if v != u and rows[u][v] in (color, '.'))
               for u in range(43)]

        def visit(chosen, candidates):
            if len(chosen) == 5:
                ids = [free[tuple(sorted(p))] for p in combinations(chosen, 2)
                       if tuple(sorted(p)) in free]
                sign = -1 if color == '1' else 1
                result.add(tuple(sorted(sign * v for v in ids)))
                return
            while candidates:
                bit = candidates & -candidates
                candidates ^= bit
                v = bit.bit_length() - 1
                visit(chosen + [v], candidates & adj[v])

        visit([], (1 << 43) - 1)
    return result


def sequential(lits, threshold, top):
    """Independent explicit threshold-grid reconstruction of the counter."""
    n = len(lits)
    if threshold >= n:
        return [], top, {}
    if threshold == n - 1:
        return [[-x for x in lits]], top, {}
    if threshold == 0:
        return [[-x] for x in lits], top, {}
    require(0 < threshold < n - 1, 'counter threshold')
    nodes = {}
    clauses = []

    def node(k, j):
        nonlocal top
        if (k, j) not in nodes:
            top += 1
            nodes[k, j] = top
        return nodes[k, j]

    for j in range(n - threshold):
        clauses.append([-lits[j], node(0, j)])
        for k in range(threshold):
            a = node(k, j)
            if j + 1 < n - threshold:
                clauses.append([-a, node(k, j + 1)])
            if k + 1 < threshold:
                clauses.append([-lits[j + k + 1], -a, node(k + 1, j)])
            else:
                clauses.append([-lits[j + threshold], -a])
    return clauses, top, nodes


def cardinal_rows(rows, profile, free, cells):
    blocks = []
    pairs = list(combinations(range(43), 2))
    for v in range(43):
        low, high = (22, 22) if v == 0 else ((21, 22) if v <= 22 else (20, 21))
        blocks.append(([p for p in pairs if v in p], low, high))
    for s in range(8):
        for t in range(s, 8):
            pairs = list(combinations(cells[s], 2)) if s == t else [tuple(sorted((a, b))) for a in cells[s] for b in cells[t]]
            target = profile['cell_red_upper_triangle'][s][t-s]
            blocks.append((pairs, target, target))
    top, output, count = 400, [], 0
    for pairs, low, high in blocks:
        known = sum(rows[a][b] == '1' for a, b in pairs if (a, b) not in free)
        lits = [free[p] for p in pairs if p in free]
        low, high = low - known, high - known
        require(high >= 0 and low <= len(lits), 'fixed quota infeasible')
        specs = []
        if high < len(lits):
            specs.append((lits, high))
        if low > 0:
            specs.append(([-v for v in lits], len(lits) - low))
        for signed, threshold in specs:
            added, top, _ = sequential(signed, threshold, top)
            output.extend(tuple(sorted(c)) for c in added)
            count += 1
    return output, top, count


def audit(path):
    rows, profile, free, cells = load()
    globals_ = clique_rows(rows, free)
    counters, top, count = cardinal_rows(rows, profile, free, cells)
    lines = path.read_text().splitlines()
    require(lines[0] == f'p cnf {top} 88433', 'header')
    clauses = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        require(bool(values) and values[-1] == 0 and 0 not in values[:-1], 'clause terminator')
        require(len(values[:-1]) == len(set(values[:-1])), 'duplicate literal')
        require(not any(-v in values[:-1] for v in values[:-1]), 'tautology')
        require(all(abs(v) <= top for v in values[:-1]), 'variable range')
        clauses.append(tuple(sorted(values[:-1])))
    require(len(clauses) == 88433, 'clause count')
    rest = Counter(clauses)
    for clause in counters:
        require(rest[clause] > 0, 'missing counter clause')
        rest[clause] -= 1
    present = {c for c, multiplicity in rest.items() if multiplicity > 0}
    require(present == globals_, 'Ramsey coverage or unauthorized constraint')
    return {'all_checks': True, 'primary_variables': len(free), 'variables': top,
            'clauses': len(clauses), 'distinct_global_clauses': len(globals_),
            'counter_blocks': count, 'counter_clauses': len(counters),
            'formula_sha256': sha256(path.read_bytes()).hexdigest()}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('formula', type=Path)
    args = p.parse_args()
    print(json.dumps(audit(args.formula), indent=2, sort_keys=True))
