"""Exact counter-extension tests and malformed-formula rejection controls."""
from itertools import product
import json
from pathlib import Path
import sys
import tempfile

from audit import audit, sequential


def main():
    formula = Path(sys.argv[1])
    report = audit(formula)
    cases = 0
    for n in range(9):
        lits = [(j + 1) * (-1 if j % 2 else 1) for j in range(n)]
        for t in range(n + 1):
            clauses, _, nodes = sequential(lits, t, n)
            for values in product((False, True), repeat=n):
                if sum(values) > t:
                    continue
                assignment = {abs(lit): value if lit > 0 else not value for lit, value in zip(lits, values)}
                assignment.update({var: sum(values[:j+k+1]) >= k+1 for (k, j), var in nodes.items()})
                if not all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses):
                    raise ValueError('canonical counter extension')
                cases += 1
    original = formula.read_text().splitlines()
    mutations = []
    changed = original.copy(); changed[0] = 'p cnf 13601 88433'; mutations.append(changed)
    mutations.append(original[:-1])
    changed = original.copy(); changed[1] = '0'; mutations.append(changed)
    changed = original.copy(); changed[1] = '13601 0'; mutations.append(changed)
    changed = original.copy(); changed[1] = '1 -1 0'; mutations.append(changed)
    changed = original.copy(); changed[1] = '1 1 0'; mutations.append(changed)
    i = next(i for i, line in enumerate(original[1:], 1) if any(abs(int(x)) > 400 for x in line.split()))
    changed = original.copy(); parts = changed[i].split(); parts[0] = str(-int(parts[0])); changed[i] = ' '.join(parts); mutations.append(changed)
    rejected = 0
    with tempfile.TemporaryDirectory(prefix='r55-closure-controls-') as directory:
        for i, lines in enumerate(mutations):
            path = Path(directory) / f'bad-{i}.cnf'
            path.write_text('\n'.join(lines) + '\n')
            try:
                audit(path)
            except ValueError:
                rejected += 1
            else:
                raise ValueError(f'accepted mutation {i}')
    print(json.dumps({'canonical_counter_extensions': cases, 'rejected_corruptions': rejected,
                      'formula_sha256': report['formula_sha256']}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
