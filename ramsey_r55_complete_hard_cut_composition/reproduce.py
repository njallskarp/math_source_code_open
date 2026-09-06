"""Compare complete independent streams in temporary space, then remove them."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent

def run(script,flags,stream=None):
    args=[sys.executable,*flags,str(HERE/script)]
    if stream is not None:args+=['--stream',str(stream)]
    return subprocess.run(args,capture_output=True,check=True,timeout=90).stdout

def main():
    start=time.monotonic()
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if '/' in name or name in ('.','..'):raise ValueError('manifest path')
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('manifest mismatch: '+name)
    with tempfile.TemporaryDirectory(prefix='r55-complete-cut-') as scratch:
        scratch=Path(scratch);left=scratch/'producer';right=scratch/'checker'
        if run('derive.py',['-B'],left)!=(HERE/'certificate.json').read_bytes():
            raise ValueError('producer mismatch')
        if run('check.py',['-B'],right)!=(HERE/'EXPECTED.json').read_bytes():
            raise ValueError('checker mismatch')
        lines=0
        with left.open('rb') as f,right.open('rb') as g:
            while True:
                a,b=f.readline(),g.readline()
                if a!=b:raise ValueError(('stream disagreement',lines))
                if not a:break
                lines+=1
        if lines!=187929:raise ValueError('incomplete stream')
    for script,target in [('derive.py','certificate.json'),('check.py','EXPECTED.json')]:
        if run(script,['-O','-B'])!=(HERE/target).read_bytes():
            raise ValueError('assertion-disabled mismatch')
    report=json.loads((HERE/'EXPECTED.json').read_text())
    report.update({'complete_records_byte_compared':lines,'seconds':round(time.monotonic()-start,3)})
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()
