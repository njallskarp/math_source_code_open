"""Replay the pinned complete classification and every interface-8 refutation."""
import argparse
import errno
import shutil
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time


def wait_for_storage(directory):
    while shutil.disk_usage(directory).free < 256*1024*1024:
        print('Waiting for 256 MiB of free scratch space', flush=True)
        time.sleep(5)


def save_output(path, data):
    while True:
        wait_for_storage(path.parent)
        try:
            path.write_bytes(data)
            return
        except OSError as error:
            if error.errno != errno.ENOSPC:
                raise
            print('Output storage exhausted; retaining result and retrying', flush=True)
            time.sleep(5)


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
    imports=json.loads((source/'IMPORTED_CLASSIFICATION.json').read_bytes())
    classification=source.parent/imports['package']
    for name, expected in imports['files'].items():
        if sha256((classification/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('pinned classification source changed: '+name)
    scratch=args.scratch.resolve()
    if scratch.exists() or source==scratch or source in scratch.parents:
        raise ValueError('new external scratch required')
    wait_for_storage(scratch.parent)
    scratch.mkdir(parents=True)
    timings=[]

    def run(command,name,expected=None):
        wait_for_storage(scratch)
        start=time.monotonic()
        r=subprocess.run(command,capture_output=True)
        if r.returncode and r.stderr:
            sys.stderr.buffer.write(r.stderr)
            sys.stderr.buffer.flush()
        save_output(scratch/name,r.stdout)
        if r.stderr:save_output(scratch/(name+'.stderr'),r.stderr)
        r.check_returncode()
        if expected and json.loads(r.stdout)!=json.loads(expected.read_bytes()):
            raise ValueError('expected result differs: '+name)
        timings.append({'stage':name,'seconds':time.monotonic()-start})
        save_output(scratch/'timings.json',(json.dumps(timings,indent=2)+'\n').encode())
        print(name,'PASS',flush=True)

    for name, location in [('audit_dense',classification),('audit_cnf',source)]:
        run([args.cxx,'-std=c++20','-O3','-Wall','-Wextra','-Wpedantic',
             str(location/(name+'.cpp')),'-o',str(scratch/name)],name+'-compile.txt')
    run([sys.executable,'-B',str(classification/'derive.py'),str(scratch/'certificate.json')],
        'derive.json',classification/'EXPECTED_DERIVE.json')
    if (scratch/'certificate.json').read_bytes()!=(classification/'certificate.json').read_bytes():
        raise ValueError('regenerated compact classification differs')
    run([str(scratch/'audit_dense'),'62',str(scratch/'complete-tuples.txt')],
        'enumeration.json',classification/'EXPECTED_ENUMERATION.json')
    run([sys.executable,'-B',str(classification/'audit_classification.py'),
         str(scratch/'certificate.json'),str(scratch/'complete-tuples.txt')],
        'classification.json',classification/'EXPECTED_CLASSIFICATION.json')
    run([sys.executable,'-B',str(classification/'test_classification.py')],
        'classification-controls.json',classification/'EXPECTED_CLASSIFICATION_CONTROLS.json')
    run([sys.executable,'-B',str(source/'test_checks.py'),'--upstream',str(upstream),
         '--classification',str(classification),'--audit-cnf',str(scratch/'audit_cnf')],
        'kernel-controls.json',source/'EXPECTED_KERNEL_CONTROLS.json')
    run([sys.executable,'-B',str(source/'consumer.py'),str(scratch/'cohort'),
         '--upstream',str(upstream),'--classification',str(classification),'--kissat',args.kissat,'--drat-trim',args.drat_trim,
         '--audit-cnf',str(scratch/'audit_cnf'),'--seconds',str(args.seconds)]
        +(['--keep-native'] if args.keep_native else []),'cohort.log')
    if (scratch/'cohort/result.json').read_bytes()!=(source/'EXPECTED.json').read_bytes():
        raise ValueError('complete consumer result or manifest hash differs')
    print('VERIFIED_COMPLETE_INTERFACE8_TYPE62_DENSITY114_EXCLUSION',flush=True)


if __name__=='__main__':main()
