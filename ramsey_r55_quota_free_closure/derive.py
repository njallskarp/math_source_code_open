"""Produce and immediately replay twenty local root refutations."""
import argparse
import json
from pathlib import Path
import subprocess
from threading import Timer
from time import monotonic

from pysat.solvers import Solver

from interface import read, split


def main():
    p = argparse.ArgumentParser()
    p.add_argument('work', type=Path)
    p.add_argument('--drat-trim', required=True, type=Path)
    p.add_argument('--seconds', type=int, default=20)
    args = p.parse_args()
    work = args.work
    start = monotonic()
    _, base = read(work / 'base.cnf')
    _, full = read(work / 'formula.cnf')
    if full[:len(base)] != base:
        raise ValueError('base prefix')
    groups = split(full[len(base):])
    summary = json.loads((work / 'summary.json').read_text())
    offset = summary['global_clauses']
    by_vertex = {v: [] for v in range(43)}
    for item in json.loads((work / 'degree_blocks.json').read_text()):
        size = item['clauses']
        by_vertex[item['vertex']].extend(base[offset:offset+size])
        offset += size
    if offset != len(base):
        raise ValueError('degree suffix')
    directory = work / 'local'
    directory.mkdir(exist_ok=False)
    results = []
    for j, (root, gates) in enumerate(groups):
        b = 23 + j
        ids = {j + 1 + 20*r for r in range(20)}
        unary = [c for c in base[:summary['global_clauses']] if all(abs(v) in ids for v in c)]
        local = unary + by_vertex[b] + gates + [[-root]]
        cnf, proof = directory / f'{b}.cnf', directory / f'{b}.drat'
        with cnf.open('x') as out:
            top = max(abs(v) for c in local for v in c)
            out.write(f'p cnf {top} {len(local)}\n')
            for c in local:
                out.write(' '.join(map(str, c)) + ' 0\n')
        with Solver(name='glucose42', bootstrap_with=local, with_proof=True) as solver:
            timer = Timer(args.seconds, solver.interrupt)
            timer.start()
            try:
                status = solver.solve_limited(expect_interrupt=True)
            finally:
                timer.cancel()
            if status is not False:
                raise RuntimeError(f'column {b} unresolved: {status}')
            proof.write_text('\n'.join(solver.get_proof()) + '\n')
        checked = subprocess.run([str(args.drat_trim.resolve()), str(cnf), str(proof), '-U', '-t', '30'],
                                 capture_output=True, text=True, timeout=45)
        output = checked.stdout + checked.stderr
        if checked.returncode or 's VERIFIED' not in output:
            raise RuntimeError(output)
        (directory / f'{b}.replay.txt').write_text(output)
        results.append({'column': b, 'root': root, 'clauses': len(local), 'rup_verified': True})
        print(json.dumps(results[-1]), flush=True)
    (work / 'local_results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({'local_rup_replays': len(results), 'elapsed_seconds': monotonic()-start}), flush=True)


if __name__ == '__main__':
    main()
