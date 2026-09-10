"""Rebuild the audited cover and exhaust both fixed-multiplier families."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import shlex
import subprocess
import sys
import time
import cover

ROOT=Path(__file__).resolve().parent

def digest(data): return hashlib.sha256(data).hexdigest()

def compile_sources(work,cxx,flags):
    args=[cxx,'-std=c++20','-O3','-Wall','-Wextra','-Wpedantic','-Wshadow','-Werror']
    if platform.system()=='Darwin':
        sdk=subprocess.check_output(['xcrun','--show-sdk-path'],text=True).strip()
        args+=['-isysroot',sdk,'-isystem',str(Path(sdk)/'usr/include/c++/v1')]
    args+=shlex.split(flags)
    for name in ('match','box_audit','lift64','reversible_check'):
        subprocess.run([*args,str(ROOT/(name+'.cpp')),'-o',str(work/name)],check=True)

def search(work,summary,resume):
    lines=(work/'compressed.txt').read_text().splitlines()
    n=int(lines[0]);assert n==len(lines)-1==summary['parents']
    # Eight disjoint consecutive partitions of at most 4096 parents.
    # A complete receipt is bound to the exact input and current executable bytes.
    executable_hash=digest((work/'lift64').read_bytes())
    result={}
    for h in (31,63):
        totals=dict(parents=0,pairs=0,unique_table_keys=0,witnesses=0)
        for begin in range(0,n,4096):
            batch=lines[begin+1:min(begin+4096,n)+1]
            data=str(len(batch))+'\n'+'\n'.join(batch)+'\n'
            key=dict(input_sha256=digest(data.encode()),executable_sha256=executable_hash,
                     multiplier=h,begin=begin,end=begin+len(batch))
            stem=work/f'full-{h}-{begin}'
            receipt=stem.with_suffix('.json')
            if resume and receipt.exists():
                saved=json.loads(receipt.read_text())
                assert saved['key']==key
                counts=saved['counts']
            else:
                input_path=stem.with_suffix('.txt');input_path.write_text(data)
                t=time.monotonic()
                completed=subprocess.run([str(work/'lift64'),str(input_path),str(h)],
                    text=True,stdout=subprocess.PIPE,check=True)
                stem.with_suffix('.log').write_text(completed.stdout)
                final=completed.stdout.splitlines()[-1]
                match=re.fullmatch(r'COMPLETE multiplier (\d+) parents (\d+) total_input (\d+) '
                    r'pairs (\d+) unique_table_keys (\d+) witnesses 0',final)
                if not match: raise RuntimeError('Search did not complete negatively: '+final)
                mh,parents,total,pairs,unique=map(int,match.groups())
                assert mh==h and parents==total==len(batch)
                counts=dict(parents=parents,pairs=pairs,unique_table_keys=unique,witnesses=0)
                temp=receipt.with_suffix('.pending')
                temp.write_text(json.dumps(dict(key=key,counts=counts,seconds=time.monotonic()-t)))
                temp.replace(receipt)
            for k,v in counts.items():totals[k]+=v
            print(json.dumps(dict(multiplier=h,completed_through=begin+len(batch),total=n)),flush=True)
        result[str(h)]=totals
    return result

def main():
    if not __debug__: raise RuntimeError('run Python without -O')
    parser=argparse.ArgumentParser()
    parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--cover-only',action='store_true')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--cxx',default='c++')
    parser.add_argument('--cxxflags',default='')
    args=parser.parse_args();work=args.workdir.resolve();work.mkdir(parents=True,exist_ok=True)
    if work==ROOT or ROOT in work.parents:raise RuntimeError('choose a workdir outside the source package')
    compile_sources(work,args.cxx,args.cxxflags)
    summary=cover.build(work)
    (work/'cover-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    expected=json.loads((ROOT/'expected.json').read_text())
    assert summary==expected['cover']
    if args.cover_only:
        print(json.dumps(dict(cover_verified=True,parents=summary['parents'],
                             input_sha256=summary['input_sha256'],full_exclusion_checked=False)))
        return
    audit=json.loads(subprocess.check_output([sys.executable,str(ROOT/'audit_full.py'),
        str(work/'lift64'),str(work/'compressed.txt')],text=True))
    assert audit==expected['full_lift_audit']
    searches=search(work,summary,args.resume)
    assert searches==expected['searches']
    independent=json.loads(subprocess.check_output(
        [str(work/'reversible_check'),str(work/'compressed.txt')],text=True))
    assert independent==expected['independent63']
    print(json.dumps(dict(verified=True,parents=summary['parents'],multipliers=[31,63],
        witnesses=[0,0],input_sha256=summary['input_sha256']),sort_keys=True))

if __name__=='__main__':main()
