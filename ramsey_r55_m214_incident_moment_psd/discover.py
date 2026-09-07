#!/usr/bin/env python3
"""Exact LP reconstruction near an untrusted, compact numerical discovery seed.

The independent physical checker, rather than this restriction or solver
status, establishes complete-family feasibility and positive semidefiniteness.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,itertools as it,subprocess,time,json
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
SOURCE=BASE/'ramsey_r55_m214_neighbor_moment_psd/discover.py'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!='933617f7aa29b7b185e634405aac7c4bc4f0c5324fc63417b5d42711245369a6':raise ValueError('changed U producer')
spec=importlib.util.spec_from_file_location('u',SOURCE);u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
q=u.q


def generate(base,work,soplex):
    t0=time.time();m=q.conditioned_model(base);m.rows.extend(q.extra_model().rows)
    parts=[]
    for h in range(43):
        ns=[v for v in range(2,15) if v!=h]
        parts.extend((-1,m.event((h,v),red=[(h,v)])) for v in ns)
        parts.extend((-2,m.event((h,v,w),red=[(h,v),(h,w)])) for v,w in it.combinations(ns,2))
    m.addparts(parts,'>=',-1576)
    mu=[7 if h in (29,30) else 6 for h in range(43)]
    E=set(range(2,15));edge=lambda a,b:tuple(sorted((a,b)))
    star={h:[edge(h,v) for v in range(43) if v!=h] for h in range(43)}
    adj={h:[edge(h,v) for v in sorted(E-{h})] for h in range(43)}
    for h in range(43):m.addparts([(1,m.event(e,red=[e])) for e in adj[h]],'=',mu[h])
    for h in range(43):
     for k in range(h,43):m.addparts([(1,m.event(tuple(sorted(set(e+f))),red=sorted(set((e,f))))) for e in adj[h] for f in adj[k]],'=',mu[h]*mu[k])
    if len(m.rows)!=19692:raise ValueError('rank-one U model')
    for h in range(43):
     for e in star[h]:
      for es,total in ((adj[h],mu[h]),(star[h],20 if h in E else 21)):
       m.addparts([(-total,m.event(e,red=[e]))]+[(1,m.event(tuple(sorted(set(e+f))),red=sorted(set((e,f))))) for f in es],'=',0)
    if (m.n,len(m.rows))!=(8558,19754):raise ValueError('complete discovery row count')
    seed=json.loads((HERE/'discovery-seed.json').read_text())
    if set(seed)!={'format','scale','radius','centers'} or seed['format']!='rational-box-centers-v1':raise ValueError('seed schema')
    scale=seed['scale'];radius=seed['radius'];centers=seed['centers']
    if (scale,radius,len(centers))!=(1000000,1000,m.n) or not all(type(n)==int for n in centers):raise ValueError('seed parameters')
    m.write(work/'near.lp');text=(work/'near.lp').read_text();head,tail=text.split('Bounds\n');tail=tail[tail.index('End\n'):]
    bounds=[]
    for i,n in enumerate(centers):
        lo=max(0,n-radius);hi=min(scale,n+radius)
        if lo>hi:raise ValueError('empty seed interval')
        bounds.append(f' {F(lo,scale)} <= p{i} <= {F(hi,scale)}\n')
    (work/'near.lp').write_text(head+'Bounds\n'+''.join(bounds)+tail)
    sol=work/'near.sol'
    command=[soplex,'--readmode=1','--solvemode=2','--int:checkmode=2','--int:ratfac_minstalls=0','--bool:ratfacjump=true','--real:feastol=0','--real:opttol=0','-s1','-g2','-v3','-t180','-X='+str(sol),str(work/'near.lp')]
    with (work/'solver.log').open('w') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
    m.certificate(m.read(sol),work/'certificate.json')
    print('EXACT_RESTRICTED_INCIDENT_CANDIDATE',time.time()-t0,flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--soplex',default='soplex');a=p.parse_args();work=a.work.resolve()
    if work==BASE or BASE in work.parents:raise ValueError('scratch must be outside source checkout')
    work.mkdir(parents=True,exist_ok=True);generate(a.base,work,a.soplex)

if __name__=='__main__':main()
