"""Fresh complete cohort replay. Native proofs and formulas remain in external scratch."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    p = argparse.ArgumentParser()
    p.add_argument('scratch', type=Path)
    p.add_argument('--cxx', default='c++')
    p.add_argument('--kissat', required=True)
    p.add_argument('--drat-trim', required=True)
    p.add_argument('--seconds', type=int, default=30)
    args = p.parse_args()
    source = Path(__file__).resolve().parent
    upstream = source.parent/'ramsey_r55_dense_degree23_hub_classification'
    scratch = args.scratch.resolve()
    if scratch.exists() or source == scratch or source in scratch.parents:
        raise ValueError('new external scratch required')
    scratch.mkdir(parents=True)
    runs = []

    def run(command, name, expected=None):
        start = time.monotonic()
        r = subprocess.run(command, capture_output=True, check=True)
        (scratch/name).write_bytes(r.stdout)
        if r.stderr:
            (scratch/(name+'.stderr')).write_bytes(r.stderr)
        if expected and r.stdout != (source/expected).read_bytes():
            raise ValueError('expected output mismatch: '+name)
        runs.append({'stage': name, 'seconds': time.monotonic()-start})
        print(name, 'PASS', flush=True)

    for stem in ['audit_cnf', 'audit_local']:
        run([args.cxx, '-std=c++20', '-O3', '-Wall', '-Wextra', '-Wpedantic',
             str(source/(stem+'.cpp')), '-o', str(scratch/stem)], 'compile-'+stem+'.txt')
    run([sys.executable, '-B', str(source/'test_checks.py'), '--upstream', str(upstream),
         '--audit-cnf', str(scratch/'audit_cnf'), '--audit-local', str(scratch/'audit_local')], 'controls.json', 'EXPECTED_TEST.json')
    run([sys.executable, '-B', str(source/'consumer.py'), str(scratch/'cohort'),
         '--upstream', str(upstream), '--kissat', args.kissat, '--drat-trim', args.drat_trim,
         '--audit-cnf', str(scratch/'audit_cnf'), '--seconds', str(args.seconds)], 'cohort.log')
    if (scratch/'cohort/result.json').read_bytes() != (source/'EXPECTED.json').read_bytes():
        raise ValueError('complete cohort result mismatch')
    (scratch/'timings.json').write_text(json.dumps(runs, indent=2)+'\n')
    print('VERIFIED_COMPLETE_TWENTY_FOUR_EDGE_FAMILY_AND_TWO_COHORT_EXCLUSION', flush=True)


if __name__ == '__main__':
    main()
