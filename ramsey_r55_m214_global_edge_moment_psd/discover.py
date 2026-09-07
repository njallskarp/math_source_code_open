#!/usr/bin/env python3
"""Exact reconstruction of the complete global edge PSD survivor.

The numerical seed is untrusted discovery input. The complete physical
linear-row replay and exact global PSD check determine the claim.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,itertools as it,subprocess,time,json
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
SOURCE=BASE/'ramsey_r55_m214_incident_moment_psd/discover.py'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!='91cdfd4343caf03fee32b8af05dc2c900ca7a63a04678a18f252f69d065292df':raise ValueError('changed V producer')
spec=importlib.util.spec_from_file_location('v',SOURCE);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);q=v.q


def generate(base,work,soplex):
    t0=time.time()
    m=q.conditioned_model(base);m.rows.extend(q.extra_model().rows)
    E=set(range(2,15));edge=lambda a,b:tuple(sorted((a,b)))
    all_edges=list(it.combinations(range(43),2));mu=[7 if h in (29,30) else 6 for h in range(43)]
    adj={h:[edge(h,u) for u in sorted(E-{h})] for h in range(43)}
    stars={h:[edge(h,u) for u in range(43) if u!=h] for h in range(43)}
    parts=[]
    for h in range(43):
     parts.extend((-1,m.event(e,red=[e])) for e in adj[h])
     parts.extend((-2,m.event(tuple(sorted(set(e+f))),red=[e,f])) for e,f in it.combinations(adj[h],2))
    m.addparts(parts,'>=',-1576)
    for h in range(43):m.addparts([(1,m.event(e,red=[e])) for e in adj[h]],'=',mu[h])
    for h in range(43):
     for k in range(h,43):m.addparts([(1,m.event(tuple(sorted(set(e+f))),red=sorted(set((e,f))))) for e in adj[h] for f in adj[k]],'=',mu[h]*mu[k])
    if len(m.rows)!=19692:raise ValueError('rank-one U')
    for cell in m.cells:
     h=cell[0]
     for e in all_edges:
      for es,total in ((adj[h],mu[h]),(stars[h],20 if h in E else 21)):
       m.addparts([(-total,m.event(e,red=[e]))]+[(1,m.event(tuple(sorted(set(e+f))),red=sorted(set((e,f))))) for f in es],'=',0)
    if (m.n,len(m.rows))!=(8558,20334):raise ValueError('complete discovery row count')
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
    command=[soplex,'--readmode=1','--solvemode=2','--int:checkmode=2','--int:ratfac_minstalls=0','--bool:ratfacjump=true','--real:feastol=0','--real:opttol=0','-s1','-g2','-v3','-t240','-X='+str(sol),str(work/'near.lp')]
    with (work/'solver.log').open('w') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
    m.certificate(m.read(sol),work/'certificate.json')
    print('EXACT_RESTRICTED_GLOBAL_CANDIDATE',time.time()-t0,flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--soplex',default='soplex');a=p.parse_args();work=a.work.resolve()
    if work==BASE or BASE in work.parents:raise ValueError('scratch must be outside source checkout')
    work.mkdir(parents=True,exist_ok=True);generate(a.base,work,a.soplex)

if __name__=='__main__':main()
