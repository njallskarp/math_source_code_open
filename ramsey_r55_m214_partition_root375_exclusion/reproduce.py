#!/usr/bin/env python3
"""Regenerate full parent and physical kernel, then replay compact root proof."""
import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
PARENT_SHA='e6b26db8a05ee7c246b431b185bee2543697c2a7a720154bea70dfa2e10c8a08'


def run(script,*args):
    return subprocess.check_output([sys.executable,'-B',str(script),*map(str,args)],text=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('work',type=Path)
    parser.add_argument('--cadical',type=Path);parser.add_argument('--drat-trim',type=Path);parser.add_argument('--lrat-check',type=Path)
    args=parser.parse_args();work=args.work.resolve()
    if work==REPO or REPO in work.parents:raise ValueError('generated state must be outside the source checkout')
    if any((args.cadical,args.drat_trim,args.lrat_check)) and not all((args.cadical,args.drat_trim,args.lrat_check)):raise ValueError('native replay needs all three executable paths')
    parent=REPO/'ramsey_r55_m214_integrated_pair_roots/generate_opb.py'
    if hashlib.sha256(parent.read_bytes()).hexdigest()!=PARENT_SHA:raise ValueError('changed full parent generator')
    work.mkdir(parents=True,exist_ok=False)
    run(parent,'--output',work/'parent.opb')
    run(HERE/'build.py','--kernel',work/'kernel.cnf','--cut',work/'cut.opbpart')
    controls=run(HERE/'controls.py')
    if controls!=(HERE/'EXPECTED_CONTROLS.json').read_text():raise ValueError('controls differ')
    result=run(HERE/'audit.py','--kernel',work/'kernel.cnf','--opb',work/'parent.opb')
    if result!=(HERE/'EXPECTED_RESULT.json').read_text():raise ValueError('compact proof differs: '+result)
    if args.cadical:
        with (work/'solver.log').open('w') as log:
            code=subprocess.run([str(args.cadical.resolve()),'--plain','--no-binary',str(work/'kernel.cnf'),str(work/'kernel.drat')],stdout=log,stderr=subprocess.STDOUT).returncode
        if code!=20:raise ValueError('native solver did not return UNSAT; no native claim')
        with (work/'drat.log').open('w') as log:
            subprocess.run([str(args.drat_trim.resolve()),str(work/'kernel.cnf'),str(work/'kernel.drat'),'-U','-L',str(work/'kernel.lrat')],stdout=log,stderr=subprocess.STDOUT,check=True)
        with (work/'lrat.log').open('w') as log:
            subprocess.run([str(args.lrat_check.resolve()),str(work/'kernel.cnf'),str(work/'kernel.lrat')],stdout=log,stderr=subprocess.STDOUT,check=True)
        if 's VERIFIED' not in (work/'drat.log').read_text() or 'c VERIFIED' not in (work/'lrat.log').read_text():raise ValueError('native proof checker verdict')
    print(result,end='')

if __name__=='__main__':main()
