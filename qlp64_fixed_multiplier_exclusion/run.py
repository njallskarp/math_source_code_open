"""Regenerate, compile, independently audit, and exhaust both multiplier families."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def execute(args):
    result = subprocess.run(args, check=True, text=True, stdout=subprocess.PIPE)
    return result.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workdir', type=Path, required=True)
    parser.add_argument('--cxx', default='c++')
    parser.add_argument('--cxxflags', default='')
    args = parser.parse_args()
    work = args.workdir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    input_path, executable = work/'compressed.txt', work/'lift64'
    compression = execute([sys.executable, str(ROOT/'compress.py'),
                           '--output', str(input_path)])
    compression = [json.loads(line) for line in compression.splitlines()]
    flags = ['-std=c++20', '-O3', '-Wall', '-Wextra', '-Wpedantic', '-Wshadow']
    if platform.system() == 'Darwin':
        sdk = execute(['xcrun', '--show-sdk-path']).strip()
        flags += ['-isysroot', sdk, '-isystem', str(Path(sdk)/'usr/include/c++/v1')]
    flags += shlex.split(args.cxxflags)
    execute([args.cxx, *flags, str(ROOT/'lift64.cpp'), '-o', str(executable)])
    audit = json.loads(execute([sys.executable, str(ROOT/'audit.py'),
                               str(executable), str(input_path)]))
    searches = {}
    for h in (31, 63):
        output = execute([str(executable), str(input_path), str(h)])
        final = output.splitlines()[-1]
        match = re.fullmatch(r'COMPLETE multiplier (\d+) parents (\d+) total_input (\d+) '
                             r'pairs (\d+) unique_table_keys (\d+) witnesses 0', final)
        if not match:
            raise AssertionError(output)
        mh, parents, total, pairs, unique = map(int, match.groups())
        assert mh == h and parents == total == 1472
        searches[str(h)] = {'parents': parents, 'pairs': pairs,
                            'unique_table_keys': unique, 'witnesses': 0}
    result = {'compression': compression, 'audit': audit, 'searches': searches}
    expected = json.loads((ROOT/'expected.json').read_text())
    assert result == expected, json.dumps(result, indent=2)
    digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    print(json.dumps({'verified': True, 'input_sha256': digest,
                      'parents': 1472, 'multipliers': [31, 63],
                      'witnesses': [0, 0]}, sort_keys=True))


if __name__ == '__main__':
    raise SystemExit('WITHDRAWN: invalid quarter-entry parity filter omitted valid compressed lifts. See README.md and ../qlp64_lift_parity_correction.')
