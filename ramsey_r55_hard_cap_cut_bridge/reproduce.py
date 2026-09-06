"""Replay only compact exact arithmetic; no network or generated large data."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent

def main():
    start=time.monotonic()
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if '/' in name or name in ('.','..'):
            raise ValueError('manifest path')
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('manifest mismatch: '+name)
    for flags in (['-B'],['-O','-B']):
        for script,output in [('derive.py','certificate.json'),('check.py','EXPECTED.json')]:
            result=subprocess.run([sys.executable,*flags,str(HERE/script)],
                                  capture_output=True,check=True,timeout=90)
            if result.stdout!=(HERE/output).read_bytes():
                raise ValueError('replay mismatch: '+script)
    report=json.loads((HERE/'EXPECTED.json').read_text())
    report['replay_seconds']=round(time.monotonic()-start,3)
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()
