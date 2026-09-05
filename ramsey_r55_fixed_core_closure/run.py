"""Regenerate a proof, remove discovery-only BDDs, audit and replay the result."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys

from parent import build
from audit import audit

BASE = Path(__file__).resolve().parent


def command(argv, timeout):
    completed = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout)
    return completed.stdout


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--seconds', type=int, default=240)
    args = p.parse_args()
    work = args.work.resolve()
    if work == BASE or BASE in work.parents:
        raise ValueError('generated state must be outside the source directory')
    work.mkdir(parents=True, exist_ok=False)
    _, red, fixed, variables, clauses, _ = build()
    extra = set()
    for vertices in combinations(range(43), 5):
        edges = list(combinations(vertices, 2))
        known = {fixed[e] for e in edges if e in fixed}
        if len(known) == 2:
            continue
        for color in known or (True, False):
            extra.add(tuple(variables[e] * (-1 if color else 1) for e in edges if e in variables))
    clauses.extend(sorted(extra))
    final = work / 'final.cnf'
    with final.open('w') as stream:
        stream.write(f'p cnf 13600 {len(clauses)}\n')
        for clause in clauses:
            stream.write(' '.join(map(str, clause)) + ' 0\n')
    report = audit(final)
    print(json.dumps(report), flush=True)
    discovery = work / 'discovery'
    output = command([sys.executable, '-B', str(BASE / 'discover.py'), '--full', '--seconds', str(args.seconds),
                      '--certificate-work', str(discovery)], args.seconds + 180)
    print(output, end='', flush=True)
    proof = discovery / 'proof.drat'
    if not proof.is_file():
        raise RuntimeError('no UNSAT trace; bounded outcome does not establish exclusion')
    trimmed = work / 'trimmed.drat'
    trim_output = command([str(args.drat_trim.resolve()), str(discovery / 'formula.cnf'), str(proof),
                           '-U', '-t', '120', '-l', str(trimmed)], 150)
    if 's VERIFIED' not in trim_output:
        raise RuntimeError(trim_output)
    print(trim_output, end='', flush=True)
    final_output = command([str(args.drat_trim.resolve()), str(final), str(trimmed), '-U', '-t', '120'], 150)
    if 's VERIFIED' not in final_output:
        raise RuntimeError(final_output)
    print(final_output, end='', flush=True)
    report['rup_replays'] = 2
    report['files'] = {str(path.relative_to(work)): {'bytes': path.stat().st_size,
                         'sha256': sha256(path.read_bytes()).hexdigest()}
                       for path in (final, discovery / 'formula.cnf', proof, trimmed)}
    (work / 'verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
