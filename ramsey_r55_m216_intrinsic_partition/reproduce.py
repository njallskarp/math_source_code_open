"""Rebuild the independent census in external scratch and verify the package."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('scratch', type=Path)
    parser.add_argument('--cxx', default=os.environ.get('CXX') or shutil.which('g++-16') or 'c++')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    if args.scratch.resolve() == here or here in args.scratch.resolve().parents:
        raise ValueError('use external scratch')
    args.scratch.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    exe = args.scratch/'census'
    subprocess.run([args.cxx,'-std=c++20','-O2','-Wall','-Wextra','-Wpedantic',
                    str(here/'census.cpp'),'-o',str(exe)],check=True)
    literal = args.scratch/'literal-cores.txt'
    with literal.open('w') as f:
        subprocess.run([str(exe)],stdout=f,check=True)
    outputs = []
    for flags in (['-B'],['-B','-O']):
        r = subprocess.run([sys.executable,*flags,str(here/'check.py'),str(literal)],
                           capture_output=True,text=True,check=True)
        outputs.append(r.stdout)
    if outputs[0] != outputs[1] or outputs[0] != (here/'EXPECTED.json').read_text():
        raise ValueError('normal/optimized/expected mismatch')
    for line in (here/'SHA256SUMS').read_text().splitlines():
        expected,name = line.split('  ',1)
        if hashlib.sha256((here/name).read_bytes()).hexdigest() != expected:
            raise ValueError('manifest '+name)
    print(outputs[0],end='')
    print('REPRODUCED',round(time.monotonic()-start,3),'seconds')

if __name__ == '__main__':
    main()
