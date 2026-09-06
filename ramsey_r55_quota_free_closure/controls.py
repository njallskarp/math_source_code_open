"""Small exact extension truth tables and adversarial interface controls."""
from itertools import product
import json
from pathlib import Path
import sys

from audit import expect, check
from interface import audit, gate, local_premises
from primitives import sequential


def main():
    work = Path(sys.argv[1])
    audit(work)
    tested = 0
    for n in range(9):
        lits = [(i+1) * (-1 if i % 2 else 1) for i in range(n)]
        for bound in range(n+1):
            clauses, _, nodes = sequential(lits, bound, n)
            for values in product((False, True), repeat=n):
                if sum(values) > bound:
                    continue
                assignment = {abs(x): v if x > 0 else not v for x, v in zip(lits, values)}
                assignment.update({var: sum(values[:j+k+1]) >= k+1 for (k,j),var in nodes.items()})
                if not all(any(assignment[abs(x)] == (x > 0) for x in c) for c in clauses):
                    raise ValueError('counter extension')
                tested += 1
    gates = 0
    for lo, hi in product((False, True, 2), (False, True, 3)):
        def literal(child, sign=True):
            return child == sign if type(child) is bool else child * (1 if sign else -1)
        defs = []
        for clause in ([-5,-1,literal(hi)],[-5,1,literal(lo)],
                       [5,-1,literal(hi,False)],[5,1,literal(lo,False)]):
            if not any(x is True for x in clause):
                defs.append([x for x in clause if x is not False])
        gate(5, defs, 4)
        for values in product((False,True), repeat=4):
            assignment = dict(zip((1,2,3,5), values))
            child = hi if assignment[1] else lo
            selected = child if type(child) is bool else assignment[child]
            actual = all(any(assignment[abs(x)] == (x > 0) for x in c) for c in defs)
            if actual != (assignment[5] == selected):
                raise ValueError('gate truth table')
            gates += 1
    bad_gates = [([],4), ([[-5,-1,5],[5,-1,-5],[-5,1],[5,1]],4),
                 ([[-5,-1,2],[5,-1,2],[-5,1]],4),
                 ([[-5,-401],[5,-401],[-5,401],[5,401]],4)]
    rejected = 0
    for clauses, previous in bad_gates:
        try:
            gate(5, clauses, previous)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('corrupt gate accepted')
    expected, info = expect()
    original = (work/'base.cnf').read_text()
    mutations = [original+'1 0\n', '\n'.join(original.splitlines()[:-1])+'\n',
                 original.replace('p cnf 8320 67384','p cnf 8321 67384',1)]
    for mutation in mutations:
        try:
            check(mutation,expected,info)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('corrupt base accepted')
    permitted = {(1,2),(-3,4)}
    local_premises(6, [[1,2],[-6]],6,6,permitted)
    for top, clauses in ((7,[[1,2],[-6]]),(6,[[1,2],[-5]]),
                         (6,[[5],[-6]]),(6,[[-6],[-6]]),(6,[])):
        try:
            local_premises(top,clauses,6,6,permitted)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('unauthorized local premise accepted')
    print(json.dumps({'counter_extensions':tested,'gate_truth_rows':gates,
                      'rejected_corruptions':rejected},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
