#!/usr/bin/env python3
"""Audit fresh P83 replay records and independently decide terminal domains."""
import argparse
import csv
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import tempfile

PIN = 'd198c6081c400f4096b53bb7737ca014442fd160'
HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):
            h.update(block)
    return h.hexdigest()

def sidon(a):
    seen=set()
    for i,x in enumerate(a):
        for y in a[i:]:
            if x+y in seen:
                return False
            seen.add(x+y)
    return True

def rows(p):
    return [list(map(int,s.split())) for s in Path(p).read_text().splitlines()]

def bitmask(a):
    return sum(1<<x for x in a)

def table(p):
    with Path(p).open() as f:
        return [{k:int(v) for k,v in r.items()} for r in csv.DictReader(f)]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True,help='Pinned math_results repository root')
    ap.add_argument('--profiles',type=Path,required=True,help='Completed fresh profile work directory')
    ap.add_argument('--exclusion',type=Path,required=True,help='Completed fresh exclusion work directory')
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(); source=a.source.resolve(); base=source/'sidon_ramsey_8'
    require(subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==PIN,'source commit')
    require(not subprocess.check_output(['git','-C',str(source),'diff','--name-only','HEAD','--','sidon_ramsey_8'],text=True).strip(),'modified upstream source')
    for part in ['p83_profiles','p83_exclusion']:
        for line in (base/part/'SHA256SUMS').read_text().splitlines():
            digest,name=line.split(maxsplit=1)
            require(sha(base/part/name)==digest,f'upstream manifest {part}/{name}')
    w=rows(base/'p83_profiles/weights.txt')[0]
    require(len(w)==83 and w==w[::-1] and sum(w)==31134774 and max(w)==444444,'weights')
    W=sum(w); M=4000000
    require(9*max(w)<=M and 7*max(w)<W-7*M,'small-class bound')
    require(min((W-(8-k)*M+k-1)//k for k in range(2,6))==3567387,'heavy threshold')
    # Recover all possible profiles from deficits, rather than importing a list.
    profiles=sorted({tuple(sorted((11-d for d in ds),reverse=True))
                     for ds in itertools.product(range(6),repeat=8) if sum(ds)==5})
    require(len(profiles)==7 and all(p.count(11)>=3 for p in profiles),'profile completeness')
    raw=rows(a.profiles/'raw11.txt')
    require(len(raw)==15958 and len(set(map(tuple,raw)))==15958,'eleven uniqueness')
    require(all(len(r)==11 and r==sorted(set(r)) and 0<=r[0]<=r[-1]<=82 and sidon(r) for r in raw),'eleven validity')
    pool={bitmask(r):tuple(r) for r in raw}; orbits=[]
    for m,r in pool.items():
        reflected=tuple(sorted(82-x for x in r)); rm=bitmask(reflected)
        require(rm in pool and rm!=m,'reflection closure')
        if m<rm:
            orbits.append((sum(w[x] for x in r),m,r,reflected))
    orbits.sort(key=lambda x:(-x[0],x[1])); canonical=[list(r) for o in orbits for r in o[2:]]
    require(canonical==rows(a.profiles/'orbit11.txt')==rows(a.exclusion/'orbit11.txt'),'catalog interface')
    require(max(sum(w[x] for x in r) for r in raw)==3999979,'eleven cap')
    require(sha(a.profiles/'heavy_0.bin')==sha(a.exclusion/'catalog_heavy_0.bin')=='b74d251f459a209951e87ae1519976e7dc42d4263f7dffc967d9ceaf3650bd49','heavy catalog interface')
    for path,expect in [(a.profiles/'cases_three.csv','d9858a448b47d98b3a3879e7a0f14e0f773dc50519fb25c8af635830569af236'),
                        (a.profiles/'cases_four.csv','6a171fbe3afe6d79ff46db48d45e46a876cc1acae428f242a912a5fd4ad63f9c'),
                        (a.exclusion/'cases.csv','b32d9a00e42e5349dbf6677988fb7c9da107fd325b5507cd308392006a57b250')]:
        require(sha(path)==expect,'case ledger hash')
    three=table(a.profiles/'cases_three.csv'); exc=table(a.exclusion/'cases.csv')
    require([r['orbit'] for r in exc]==list(range(5364)),'all anchors')
    require(all(r['orbit']==s['orbit'] and r['packings']==s['packings'] for r,s in zip(three,exc)),'profile to exclusion cover')
    require(sum(r['packings'] for r in exc)==65073232 and sum(r['packings']>0 for r in exc)==5157,'cover totals')
    terminals={}
    for label,work,ne,nt,nlast in [('four',a.profiles,4,3,9),('three',a.exclusion,3,4,10)]:
        data=json.loads((work/'all_terminals.json').read_text());terminals[label]=data
        require(len(data)==(380 if label=='four' else 1771),'terminal count')
        for r in data:
            elevens=[canonical[i] for i in r['eleven_ids']]; tens=r['chosen_tens']; last=r['residual']
            require(len(elevens)==ne and len(tens)==nt and len(last)==nlast,'terminal sizes')
            require(all(len(t)==10 and t==sorted(set(t)) and sidon(t) for t in tens),'selected tens')
            require(sorted(x for c in [*elevens,*tens,last] for x in c)==list(range(83)),'full partition incidence')
            require(not sidon(last),'terminal obstruction')
            weights=[sum(w[x] for x in t) for t in tens]
            require(weights==sorted(weights,reverse=True) and weights[0]<=M,'weight order including ties')
            remaining=sum(w[x] for c in [*tens,last] for x in c)
            for j,u in enumerate(weights):
                k=nt-j
                lower=(remaining-M+k-1)//k if label=='four' else (remaining+k)//(k+1)
                require(u>=lower,'heaviest-class inequality')
                remaining-=u
            if label=='four': require(remaining<=M,'nine-class cap')
            else: require(remaining<=weights[-1],'last-ten ordering')
    seed=rows(base/'p80_extension_barrier/partition80.txt')
    require(len(seed)==8 and all(len(r)==10 and sidon(r) for r in seed) and sorted(x for r in seed for x in r)==list(range(1,81)),'P80 witness')
    report={'source_commit':PIN,'initial_profiles':profiles,'terminal_occurrences':{k:len(v) for k,v in terminals.items()},'P80_witness':True}
    with tempfile.TemporaryDirectory(prefix='p83-independent-') as tmp:
        tmp=Path(tmp); exe=tmp/'terminal_audit'
        compiler=os.environ.get('CXX','g++')
        subprocess.run([compiler,'-std=c++20','-O3','-Wall','-Wextra','-Werror',str(HERE/'terminal_audit.cpp'),'-o',str(exe)],check=True)
        def execute(k,domains):
            fp=tmp/'domains.txt';fp.write_text(''.join(' '.join(map(str,d))+'\n' for d in domains))
            result=subprocess.check_output([str(exe),str(k),str(fp)],text=True)
            out=[list(map(int,l.split())) for l in result.splitlines()]
            require([r[0] for r in out]==list(range(len(domains))),'independent output coverage')
            return [r[1:] for r in out]
        domains=[tuple(x+shift for x in range(9) if m>>x&1) for shift in [0,74] for m in range(1,512)]
        for k in range(2,7):
            out=execute(k,domains)
            for d,got in zip(domains,out):
                expected=sorted(sum(1<<i for i in ids) for ids in itertools.combinations(range(len(d)),k) if sidon([d[i] for i in ids]))
                require(got==expected,'brute-force enumerator control')
        report['independent_enumerator_controls']=len(domains)*5
        positive28=json.loads((base/'p83_profiles/positive28.json').read_text())
        for row,out in zip(positive28,execute(0,[r['points'] for r in positive28])):
            shapes=[[10,10,8],[10,9,9],[11,10,7],[11,11,6],[11,9,8]]
            require(out[3+shapes.index(row['sizes'])]>0,'28-point positive control')
        domains28=rows(a.profiles/'five_domains.txt');out28=execute(0,domains28)
        require(len(domains28)==2142 and len(set(map(tuple,domains28)))==2142,'28-point domain coverage')
        require(all(not any(r[3:]) for r in out28),'unrestricted 28-point profile completion')
        report['independent_28']={'domains':2142,'ten_occurrences':sum(r[0] for r in out28),'eleven_occurrences':sum(r[1] for r in out28),'nine_occurrences':sum(r[2] for r in out28),'all_five_profiles_impossible':True}
        domains20=sorted({tuple(sorted(r['chosen_tens'][-1]+r['residual'])) for r in terminals['three']})
        require(len(domains20)==1754,'20-point domain coverage')
        out20=execute(10,domains20)
        for options in out20:
            catalog=set(options)
            require(not any(((1<<20)-1)^m in catalog for m in catalog),'unrestricted two-ten completion')
        positive20=[sorted(x-1+shift for r in seed[:2] for x in r) for shift in [0,3]]
        for options in execute(10,positive20):
            catalog=set(options);require(any(((1<<20)-1)^m in catalog for m in catalog),'two-ten positive control')
        report['independent_20']={'domains':1754,'ten_occurrences':sum(map(len,out20)),'two_ten_completions':0}
        report['compiler']=subprocess.check_output([compiler,'--version'],text=True).splitlines()[0]
    report['verified']=True
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__': main()
