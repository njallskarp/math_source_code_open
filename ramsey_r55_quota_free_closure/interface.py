"""Literal audit of conservative gates and the twenty local proof interfaces.

Imports no solver or producer. A local proof may use only audited base/gate
clauses and the single negated root it promises to derive.
"""
from collections import Counter
from itertools import groupby, product
from pathlib import Path
import json

from audit import expect, check


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def read(path):
    lines = path.read_text().splitlines()
    require(bool(lines), 'empty CNF')
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ['p', 'cnf'], 'header')
    top, count = map(int, header[2:])
    clauses = []
    for line in lines[1:]:
        c = list(map(int, line.split()))
        require(bool(c) and c[-1] == 0 and 0 not in c[:-1], 'terminator')
        c = c[:-1]
        require(len(c) == len(set(c)) and not any(-v in c for v in c), 'duplicate/tautology')
        require(all(abs(v) <= top for v in c), 'range')
        clauses.append(c)
    require(len(clauses) == count, 'count')
    return top, clauses


def split(tail):
    groups, current = [], []
    for clause in tail:
        if len(clause) == 1:
            require(bool(current) and clause[0] > 0, 'positive root after gates')
            groups.append((clause[0], current))
            current = []
        else:
            current.append(clause)
    require(not current and len(groups) == 20, 'twenty column groups')
    return groups


def gate(z, clauses, last):
    require(z == last + 1, 'fresh consecutive gate')
    require(all(len(c) in (2, 3) and abs(c[0]) == z for c in clauses), 'gate syntax')
    choices = {abs(c[1]) for c in clauses}
    require(len(choices) == 1 and 1 <= next(iter(choices)) <= 400, 'primary test')
    x = next(iter(choices))
    for sign in (x, -x):
        negative = [c for c in clauses if c[:2] == [-z, sign]]
        positive = [c for c in clauses if c[:2] == [z, sign]]
        require(len(negative) <= 1 and len(positive) <= 1, 'unique cofactor clauses')
        if not positive:
            require(negative == [[-z, sign]], 'false cofactor')
        elif not negative:
            require(positive == [[z, sign]], 'true cofactor')
        else:
            a, b = negative[0], positive[0]
            require(len(a) == len(b) == 3 and 0 < a[2] < z and b[2] == -a[2],
                    'earlier-variable cofactor')
    require(sum(1 for c in clauses if abs(c[1]) == x) == len(clauses), 'extra clause')
    return z


def local_premises(local_top, local, root, top, permitted):
    require(bool(local) and local_top <= top and local[-1] == [-root],
            'single promised negated root')
    require(all(tuple(c) in permitted for c in local[:-1]), 'unauthorized local premise')


def audit(work):
    expected, info = expect()
    check((work / 'base.cnf').read_text(), expected, info)
    base_top, base = read(work / 'base.cnf')
    top, formula = read(work / 'formula.cnf')
    require(formula[:len(base)] == base, 'base prefix')
    groups = split(formula[len(base):])
    last = base_top
    permitted = {tuple(c) for c in base}
    for root, definitions in groups:
        for z, iterator in groupby(definitions, key=lambda c: abs(c[0])):
            last = gate(z, list(iterator), last)
        require(root == last, 'root is final defined variable')
        permitted.update(tuple(c) for c in definitions)
    require(last == top, 'top matches gate allocation')
    local_counts = []
    for b, (root, _) in enumerate(groups, 23):
        local_top, local = read(work / 'local' / f'{b}.cnf')
        local_premises(local_top, local, root, top, permitted)
        local_counts.append(len(local))
    return {'all_checks': True, 'base_variables': base_top, 'base_clauses': len(base),
            'gate_variables': top - base_top, 'gate_clauses': len(formula)-len(base)-20,
            'roots': [r for r, _ in groups], 'local_clauses': local_counts,
            'formula_variables': top, 'formula_clauses': len(formula)}


if __name__ == '__main__':
    import sys
    print(json.dumps(audit(Path(sys.argv[1])), indent=2, sort_keys=True))
