"""Definition-level audit of the new quota-free base; no PySAT or producer.

Uses exact clique-recursion and threshold-grid primitives; no profile
loader, old block selector, prior theorem, or earlier proof is imported. This is author
cross-validation and is not independent mathematical review.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys

SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE))
from primitives import clique_rows, sequential


def expect():
    matrix = json.loads((SOURCE / 'PARTIAL.json').read_text())['rows']
    if len(matrix) != 43 or any(len(r) != 43 for r in matrix):
        raise ValueError('order')
    for u in range(43):
        if matrix[u][u] != '-':
            raise ValueError('diagonal')
        for v in range(u + 1, 43):
            if matrix[u][v] not in '01.' or matrix[u][v] != matrix[v][u]:
                raise ValueError('matrix')
            is_free = u in set(range(1, 23)) - {3, 9} and v >= 23
            if (matrix[u][v] == '.') != is_free:
                raise ValueError('free scope')
    free = {}
    for u in range(43):
        for v in range(u + 1, 43):
            if matrix[u][v] == '.':
                free[u, v] = len(free) + 1
    global_rows = clique_rows(matrix, free)
    expected = Counter(global_rows)
    top = len(free)
    count = 0
    counter_clauses = 0
    for v in range(43):
        fixed_red = matrix[v].count('1')
        incident = [free[e] for e in free if v in e]
        interval = (22, 22) if v == 0 else ((21, 22) if v < 23 else (20, 21))
        lower, upper = (b - fixed_red for b in interval)
        if upper < 0 or lower > len(incident):
            raise ValueError('fixed degree')
        bounds = []
        if upper < len(incident):
            bounds.append((incident, upper))
        if lower > 0:
            bounds.append(([-x for x in incident], len(incident) - lower))
        for signed, threshold in bounds:
            rows, top, _ = sequential(signed, threshold, top)
            expected.update(tuple(sorted(c)) for c in rows)
            count += 1
            counter_clauses += len(rows)
    return expected, {'variables': top, 'clauses': sum(expected.values()),
                      'global_clauses': len(global_rows), 'degree_blocks': count,
                      'counter_clauses': counter_clauses, 'primary_variables': len(free)}


def check(text, expected, info):
    lines = text.splitlines()
    if not lines or lines[0] != f'p cnf {info["variables"]} {info["clauses"]}':
        raise ValueError('header')
    observed = Counter()
    for line in lines[1:]:
        vals = list(map(int, line.split()))
        if not vals or vals[-1] != 0 or 0 in vals[:-1]:
            raise ValueError('clause syntax')
        c = vals[:-1]
        if len(c) != len(set(c)) or any(-x in c for x in c):
            raise ValueError('duplicate literal or tautology')
        if any(abs(x) > info['variables'] for x in c):
            raise ValueError('variable range')
        observed[tuple(sorted(c))] += 1
    if observed != expected:
        raise ValueError('exact clause multiset differs')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('base', type=Path)
    args = parser.parse_args()
    expected, info = expect()
    text = args.base.read_text()
    check(text, expected, info)
    lines = text.splitlines()
    counter_index = next(i for i, line in enumerate(lines[1:], 1)
                         if any(abs(int(x)) > 400 for x in line.split()))
    variants = [text + '1 0\n', '\n'.join(lines[:1] + lines[2:]) + '\n',
                '\n'.join(lines[:counter_index] + lines[counter_index + 1:]) + '\n',
                text.replace(lines[0], 'p cnf 8321 67384', 1)]
    for mutation in variants:
        try:
            check(mutation, expected, info)
        except ValueError:
            pass
        else:
            raise ValueError('corruption accepted')
    info.update({'all_checks': True, 'rejected_corruptions': len(variants),
                 'base_sha256': sha256(args.base.read_bytes()).hexdigest()})
    print(json.dumps(info, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
