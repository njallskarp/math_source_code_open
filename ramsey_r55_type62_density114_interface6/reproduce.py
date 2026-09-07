"""Full classification and complete intrinsic consumer; all large output is external."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    p=argparse.ArgumentParser()
    p.add_argument('scratch',type=Path)
    p.add_argument('--cxx',default='c++')
    p.add_argument('--kissat',required=True)
    p.add_argument('--drat-trim',required=True)
    p.add_argument('--seconds',type=int,default=30)
    p.add_argument('--keep-native',action='store_true')
    args=p.parse_args()
    source=Path(__file__).resolve().parent
    upstream=source.parent/'ramsey_r55_dense_degree23_hub_classification'
    scratch=args.scratch.resolve()
    if scratch.exists() or source==scratch or source in scratch.parents:
        raise ValueError('new external scratch required')
    scratch.mkdir(parents=True)
    timings=[]

    def run(command,name,expected=None):
        start=time.monotonic()
        r=subprocess.run(command,capture_output=True,check=True)
        (scratch/name).write_bytes(r.stdout)
        if r.stderr:(scratch/(name+'.stderr')).write_bytes(r.stderr)
        if expected and json.loads(r.stdout)!=json.loads((source/expected).read_bytes()):
            raise ValueError('expected result differs: '+name)
        timings.append({'stage':name,'seconds':time.monotonic()-start})
        (scratch/'timings.json').write_text(json.dumps(timings,indent=2)+'\n')
        print(name,'PASS',flush=True)

    for name in ['audit_dense','audit_cnf']:
        run([args.cxx,'-std=c++20','-O3','-Wall','-Wextra','-Wpedantic',
             str(source/(name+'.cpp')),'-o',str(scratch/name)],name+'-compile.txt')
    run([sys.executable,'-B',str(source/'derive.py'),str(scratch/'certificate.json')],
        'derive.json','EXPECTED_DERIVE.json')
    if (scratch/'certificate.json').read_bytes()!=(source/'certificate.json').read_bytes():
        raise ValueError('regenerated compact classification differs')
    run([str(scratch/'audit_dense'),'62',str(scratch/'complete-tuples.txt')],
        'enumeration.json','EXPECTED_ENUMERATION.json')
    run([sys.executable,'-B',str(source/'audit_classification.py'),
         str(scratch/'certificate.json'),str(scratch/'complete-tuples.txt')],
        'classification.json','EXPECTED_CLASSIFICATION.json')
    run([sys.executable,'-B',str(source/'test_classification.py')],
        'classification-controls.json','EXPECTED_CLASSIFICATION_CONTROLS.json')
    run([sys.executable,'-B',str(source/'test_checks.py'),'--upstream',str(upstream),
         '--audit-cnf',str(scratch/'audit_cnf')],
        'kernel-controls.json','EXPECTED_KERNEL_CONTROLS.json')
    run([sys.executable,'-B',str(source/'consumer.py'),str(scratch/'cohort'),
         '--upstream',str(upstream),'--kissat',args.kissat,'--drat-trim',args.drat_trim,
         '--audit-cnf',str(scratch/'audit_cnf'),'--seconds',str(args.seconds)]
        +(['--keep-native'] if args.keep_native else []),'cohort.log')
    if (scratch/'cohort/result.json').read_bytes()!=(source/'EXPECTED.json').read_bytes():
        raise ValueError('complete consumer result or manifest hash differs')
    print('VERIFIED_TYPE62_DENSITY114_CLASSIFICATION_AND_INTERFACE6_EXCLUSION',flush=True)


if __name__=='__main__':main()
