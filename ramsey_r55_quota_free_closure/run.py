"""Regenerate the complete twenty-local-plus-global RUP proof package."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from time import monotonic

BASE = Path(__file__).resolve().parent


def command(argv, timeout):
    result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stdout)
    return result.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--drat-trim', required=True, type=Path)
    parser.add_argument('--seconds', default=240, type=int)
    args = parser.parse_args()
    work = args.work.resolve()
    if work == BASE or BASE in work.parents:
        raise ValueError('work must be outside source')
    if work.exists():
        raise ValueError('work must not already exist')
    start = monotonic()
    output = command([sys.executable,'-B',str(BASE/'trial.py'),'--work',str(work),
                      '--columns','--seconds',str(args.seconds)], args.seconds+120)
    print(output,end='',flush=True)
    summary = json.loads((work/'summary.json').read_text())
    if summary.get('status') != 'UNSAT':
        raise RuntimeError('bounded global trial unresolved; no exclusion')
    base_audit = json.loads(command([sys.executable,'-B',str(BASE/'audit.py'),str(work/'base.cnf')],60))
    local = command([sys.executable,'-B',str(BASE/'derive.py'),str(work),
                     '--drat-trim',str(args.drat_trim.resolve())],600)
    print(local,end='',flush=True)
    checked_interface = json.loads(command([sys.executable,'-B',str(BASE/'interface.py'),str(work)],60))
    controls = json.loads(command([sys.executable,'-B',str(BASE/'controls.py'),str(work)],60))
    replay = command([str(args.drat_trim.resolve()),str(work/'formula.cnf'),
                      str(work/'proof.drat'),'-U','-t','120'],150)
    if 's VERIFIED' not in replay:
        raise RuntimeError(replay)
    print(replay,end='',flush=True)
    (work/'global.replay.txt').write_text(replay)
    paths = [work/'base.cnf',work/'formula.cnf',work/'proof.drat']
    paths += sorted((work/'local').glob('*.cnf')) + sorted((work/'local').glob('*.drat'))
    result = {'status':'VERIFIED','rup_replays':21,'base':base_audit,
              'interface':checked_interface,'controls':controls,
              'files':{str(p.relative_to(work)):{'bytes':p.stat().st_size,
                        'sha256':sha256(p.read_bytes()).hexdigest()} for p in paths}}
    (work/'verification.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'VERIFIED','rup_replays':21,
                      'elapsed_seconds':monotonic()-start,
                      'verification_sha256':sha256((work/'verification.json').read_bytes()).hexdigest()}),flush=True)


if __name__ == '__main__':
    main()
