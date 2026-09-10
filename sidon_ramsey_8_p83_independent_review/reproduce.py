#!/usr/bin/env python3
"""Fresh end-to-end replay of the P83 profile and exclusion, then referee audit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
PIN='d198c6081c400f4096b53bb7737ca014442fd160'

def run(command, **kwargs):
    subprocess.run(list(map(str,command)),check=True,**kwargs)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work',required=True,type=Path)
    ap.add_argument('--jobs',type=int,default=4,help='Profile workers and anchor shards')
    ap.add_argument('--shards',type=int,default=6,help='Exclusion anchor shards')
    ap.add_argument('--workers',type=int,default=6,help='Exclusion workers')
    args=ap.parse_args()
    if not __debug__:
        raise SystemExit('Upstream verification requires Python assertions; do not use -O.')
    work=args.work.resolve()
    if work.exists() or HERE in work.parents or not(1<=args.jobs<=12 and 1<=args.shards<=12 and 1<=args.workers<=12):
        raise SystemExit('Use a new work directory outside this contribution; jobs/workers must be 1..12.')
    work.mkdir(parents=True)
    source=work/'upstream'
    run(['git','clone','--filter=blob:none','--no-checkout','https://github.com/helgithorskarp/math_results.git',source])
    run(['git','-C',source,'sparse-checkout','init','--cone'])
    run(['git','-C',source,'sparse-checkout','set','sidon_ramsey_8'])
    run(['git','-C',source,'checkout','--detach',PIN])
    manifest=json.loads((HERE/'upstream_files.json').read_text())
    for name,digest in manifest.items():
        if hashlib.sha256((source/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Source hash mismatch: '+name)
    compiler=shutil.which(os.environ.get('CXX','g++'))
    if not compiler:
        raise SystemExit('Set CXX to a GCC C++20 compiler with unsigned __int128 support.')
    toolchain=work/'toolchain';toolchain.mkdir();(toolchain/'g++').symlink_to(compiler)
    env=dict(os.environ,PATH=str(toolchain)+os.pathsep+os.environ.get('PATH',''),CXX=compiler)
    # Sequential drivers avoid oversubscribing the host. Each driver runs its
    # own disjoint shards concurrently. Both regenerate every mathematical input.
    for part,output,extra in [('p83_profiles','profiles',[]),('p83_exclusion','exclusion',['--workers',args.workers])]:
        run([sys.executable,'-B',source/'sidon_ramsey_8'/part/'reproduce.py','--work',work/output,'--jobs',args.jobs if part=='p83_profiles' else args.shards,'--sanitizers',*extra],env=env)
    run([sys.executable,'-B',HERE/'audit.py','--source',source,'--profiles',work/'profiles','--exclusion',work/'exclusion','--output',work/'audit.json'],env=env)
    print('VERIFIED: full P83 profile and exclusion replay plus independent terminal audit')

if __name__=='__main__':main()
