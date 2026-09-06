"""Fresh complete replay; expanded tuples and binaries stay in external scratch."""
import argparse
from pathlib import Path
import subprocess
import sys
import json
import time

def main():
    parser=argparse.ArgumentParser();parser.add_argument('scratch',type=Path)
    parser.add_argument('--cxx',default='c++');parser.add_argument('--kissat');parser.add_argument('--drat-trim');args=parser.parse_args()
    if bool(args.kissat)!=bool(args.drat_trim):raise ValueError('supply both native proof tools or neither')
    source=Path(__file__).resolve().parent;scratch=args.scratch.resolve()
    if scratch.exists() or source==scratch or source in scratch.parents:raise ValueError('scratch must be new and outside source')
    scratch.mkdir(parents=True);runs=[]
    def run(command,name,expected=None):
        start=time.monotonic();r=subprocess.run(command,capture_output=True,check=True)
        (scratch/name).write_bytes(r.stdout)
        if r.stderr:(scratch/(name+'.stderr')).write_bytes(r.stderr)
        if expected and r.stdout!=(source/expected).read_bytes():raise ValueError('expected output mismatch: '+name)
        runs.append({'stage':name,'seconds':time.monotonic()-start});print(name,'PASS',flush=True)
    run([sys.executable,'-B',str(source/'derive.py')],'derive.json','EXPECTED_DERIVE.json')
    run([args.cxx,'-std=c++20','-O3','-Wall','-Wextra','-Wpedantic',str(source/'audit_dense.cpp'),'-o',str(scratch/'audit_dense')],'compile.txt')
    for kind in (62,126):run([str(scratch/'audit_dense'),str(kind),str(scratch/f'tuples-{kind}.txt')],f'audit-{kind}.json')
    run([sys.executable,'-B',str(source/'audit.py'),str(scratch/'tuples-62.txt'),str(scratch/'tuples-126.txt')],'audit.json','EXPECTED.json')
    run([sys.executable,'-B',str(source/'test_checks.py')],'controls.json','EXPECTED_TEST.json')
    if args.kissat:
        run([args.cxx,'-std=c++20','-O3','-Wall','-Wextra','-Wpedantic',str(source/'audit_cnf.cpp'),'-o',str(scratch/'audit_cnf')],'compile-cnf.txt')
        run([sys.executable,'-B',str(source/'glue.py'),str(scratch/'gluing'),'--kissat',args.kissat,
             '--drat-trim',args.drat_trim,'--audit-cnf',str(scratch/'audit_cnf')],'gluing.log')
        if (scratch/'gluing/result.json').read_bytes()!=(source/'EXPECTED_GLUING.json').read_bytes():raise ValueError('gluing result differs')
    (scratch/'timings.json').write_text(json.dumps(runs,indent=2)+'\n')
    print('VERIFIED_DENSE_HUB_CLASSIFICATION_AND_GLOBAL_EXCLUSION' if args.kissat else 'VERIFIED_COMPLETE_DENSE_HUB_CLASSIFICATION',flush=True)

if __name__=='__main__':main()
