#!/usr/bin/env python3
"""Exact primal discovery restriction; full checking and PSD proof are separate."""
from pathlib import Path
import argparse,hashlib,importlib.util,itertools as it,subprocess,time,json
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
SOURCE=BASE/'ramsey_r55_m214_conditioned_degree_p4/discover.py'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!='c71f605a97c22b262f8daebb068aa2edc7af9e6657fbd724f19fde857c486177':raise ValueError('changed Q producer')
spec=importlib.util.spec_from_file_location('q',BASE/'ramsey_r55_m214_conditioned_degree_p4/discover.py');q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)

def generate(base,work,soplex):
    t0=time.time();m=q.conditioned_model(base);extra=q.extra_model();m.rows.extend(extra.rows)
    parts=[]
    for h in range(43):
     ns=[u for u in range(2,15) if u!=h]
     parts.extend((-1,m.event((h,u),red=[(h,u)])) for u in ns)
     parts.extend((-2,m.event((h,u,v),red=[(h,u),(h,v)])) for u,v in it.combinations(ns,2))
    m.addparts(parts,'>=',-1576)
    if len(m.rows)!=19632:raise ValueError('T discovery coverage')
    mean=[7 if h in (29,30) else 6 for h in range(43)]
    adj={h:[tuple(sorted((h,u))) for u in range(2,15) if u!=h] for h in range(43)}
    before=len(m.rows)
    for h in range(43):m.addparts([(1,m.event(e,red=[e])) for e in adj[h]],'=',mean[h])
    for h in range(43):
     for k in range(h,43):
      parts=[(1,m.event(tuple(sorted(set(e+f))),red=sorted(set((e,f))))) for e in adj[h] for f in adj[k]]
      m.addparts(parts,'=',mean[h]*mean[k])
    if len(m.rows)-before!=60 or len(m.rows)!=19692:raise ValueError('rank-one discovery coverage')
    m.write(work/'candidate.lp');sol=work/'candidate.sol'
    command=[soplex,'--readmode=1','--solvemode=2','--int:checkmode=2','--int:ratfac_minstalls=0','--bool:ratfacjump=true','--real:feastol=0','--real:opttol=0','-s1','-g2','-v3','-t180','-X='+str(sol),str(work/'candidate.lp')]
    with (work/'solver.log').open('w') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
    m.certificate(m.read(sol),work/'certificate.json')
    print('EXACT_RESTRICTED_CANDIDATE',time.time()-t0,flush=True)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--soplex',default='soplex');a=p.parse_args();work=a.work.resolve()
    if work==BASE or BASE in work.parents:raise ValueError('scratch must be outside source checkout')
    work.mkdir(parents=True,exist_ok=True);generate(a.base,work,a.soplex)

if __name__=='__main__':main()
