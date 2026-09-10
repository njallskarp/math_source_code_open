#!/usr/bin/env python3
"""Compile the referee verifier, regenerate its finite objects, and check every residual."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

SOURCE = Path(__file__).resolve().parent
HASHES = {
    'weights.txt': 'fd37c58558d7af2066661eccb4f97d271b771c6f0277b06398c7343357cbc703',
    'ordered_sets.txt': '29f50fe15a092b6b1a8270dcbe7c6f4714b6e21cd3d9ea3fe71831af8d96f907',
    'packings.txt': '3ac309d39a65e7853042b50a8d11d4203821ed19ba13a952a107befc369d7122',
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_run(command):
    result = subprocess.run(list(map(str, command)), check=True, capture_output=True, text=True)
    return [json.loads(line) for line in result.stdout.splitlines()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--cxx', default=os.environ.get('CXX', 'g++'))
    parser.add_argument('--jobs', type=int, default=6)
    args = parser.parse_args()
    work = args.work.resolve()
    require(1 <= args.jobs <= 64, 'jobs must be in 1..64')
    require(SOURCE != work and SOURCE not in work.parents, 'work must be outside the source directory')
    require(not work.exists(), 'use a fresh, nonexistent work directory')
    require(digest(SOURCE / 'weights.txt') == HASHES['weights.txt'], 'weight hash mismatch')
    work.mkdir(parents=True)
    started = time.monotonic()
    exe = work / 'verify'
    subprocess.run([args.cxx, '-std=c++20', '-O3', '-Wall', '-Wextra', '-Werror',
                    str(SOURCE / 'verify.cpp'), '-o', str(exe)], check=True)
    generated = checked_run([exe, 'generate', SOURCE / 'weights.txt', work])
    (work / 'generation.json').write_text(json.dumps(generated, indent=2) + '\n')
    for name in ('ordered_sets.txt', 'packings.txt'):
        require(digest(work / name) == HASHES[name], f'{name}: hash mismatch')
    print(json.dumps({'generation': generated}), flush=True)

    def run_part(i):
        rows = checked_run([exe, 'residual', work, i, args.jobs])
        require(len(rows) == 1, 'unexpected residual output')
        result = rows[0]
        require(result['part'] == i and result['parts'] == args.jobs, 'wrong batch')
        require(result['tested'] == len(range(i, 130780, args.jobs)), 'wrong batch length')
        require(result['completable'] == 0, 'a residual partition exists')
        (work / f'residual_{i}.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result), flush=True)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        batches = list(pool.map(run_part, range(args.jobs)))
    totals = {key: sum(row[key] for row in batches)
              for key in ('tested', 'ten_sets', 'eleven_sets', 'completable')}
    require(totals == {'tested': 130780, 'ten_sets': 1487970, 'eleven_sets': 26, 'completable': 0},
            'residual totals mismatch')
    weights = list(map(int, (SOURCE / 'weights.txt').read_text().split()))
    rows = [list(map(int, line.split())) for line in (work / 'ordered_sets.txt').read_text().splitlines()]
    set_weights = [sum(weights[x] for x in row) for row in rows]
    tuple_weights = [sum(set_weights[int(i)] for i in line.split())
                     for line in (work / 'packings.txt').read_text().splitlines()]
    refinement = {
        'eight_element_profile_weight_shortfall': sum(weights) - (7 * 999995 + 8 * max(weights)),
        'tuples_below_4899979': sum(w < 4899979 for w in tuple_weights),
        'tuples_below_4899981': sum(w < 4899981 for w in tuple_weights),
    }
    require(refinement == {'eight_element_profile_weight_shortfall': 11116,
                           'tuples_below_4899979': 130, 'tuples_below_4899981': 142}, 'refinement mismatch')
    report = {'verified': True, 'bound': 'SR(8) <= 85', 'generation': generated,
              'residual_totals': totals, 'refinement': refinement,
              'hashes': HASHES, 'seconds': time.monotonic() - started}
    (work / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
