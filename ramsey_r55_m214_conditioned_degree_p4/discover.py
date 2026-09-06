#!/usr/bin/env python3
"""Regenerate the exact Q witness locally; no solver output is a proof verdict."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools as it
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ramsey_r55_m214_complete_star_p4_survivor/discover.py'
PIN='8f0d7d255251f6f81b9d14669ff495bd021cf052e9ee59d96700cc17df0aca6a'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=PIN:raise ValueError('changed star generator')
spec=importlib.util.spec_from_file_location('star_discover',SOURCE)
parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)


def conditioned_model(base):
    m=parent.strengthened_model(base)
    for types,A in m.reps.items():
        if len(A)!=3:continue
        pairs=list(it.combinations(A,2));counts=Counter(m.types[v] for v in A)
        for h in A:
            degree=20 if h in range(2,15) else 21
            for state in range(8):
                red=[e for j,e in enumerate(pairs) if state>>j&1]
                blue=[e for j,e in enumerate(pairs) if not(state>>j&1)]
                local=sum(h in e for e in red)
                parts=[(-(degree-local),m.event(A,red=red,blue=blue))]
                for t,cell in enumerate(m.cells):
                    weight=len(cell)-counts[t]
                    if not weight:continue
                    w=next(v for v in cell if v not in A)
                    parts.append((weight,m.event(A+(w,),red=red+[(h,w)],blue=blue)))
                m.addparts(parts,'=',0)
    if (m.n,len(m.rows))!=(8558,19388):raise ValueError('complete D3 discovery coverage')
    return m


def extra_model():
    m=parent.parent.Model();m.rows=[];m.rowset=set()
    for types,A in m.reps.items():
        if len(A)!=3:continue
        for color in (0,1):
            key='red' if color else 'blue'
            parts=[(4,m.event(A,**{key:list(it.combinations(A,2))}))]
            for w in range(43):
                if w not in A:
                    parts.append((-1,m.event(A+(w,),**{key:list(it.combinations(A+(w,),2))})))
            m.addparts(parts,'>=',0)
    if len(m.rows)!=181:raise ValueError('complete triangle caps')
    for cell in m.cells:
        h=cell[0];others=[v for v in range(43) if v!=h]
        for acell in m.cells:
            eligible=[v for v in acell if v!=h]
            if not eligible:continue
            a=eligible[0]
            parts=[(-(93 if h in range(2,15) else 100),m.event((h,a),red=[(h,a)]))]
            for u,v in it.combinations(others,2):
                A=tuple(sorted({h,a,u,v}))
                parts.append((1,m.event(A,red=[(h,u),(h,v),(u,v),(h,a)])))
            m.addparts(parts,'=',0)
    if len(m.rows)!=243:raise ValueError('complete conditioned triangle totals')
    return m


def generate(base,work,soplex):
    m=conditioned_model(base);extra=extra_model()
    lp=work/'candidate.lp';m.write(lp)
    head,tail=lp.read_text().split('Bounds\n')
    rows=''.join(' extra'+str(j)+': '+' '.join(f'{c:+d} p{i}' for i,c in row)+f' {rel} {rhs}\n'
                 for j,(row,rel,rhs) in enumerate(extra.rows))
    lp.write_text(head+rows+'Bounds\n'+tail)
    # Preserve the discovery model's exact row ordering, including redundant
    # rows across the two stages; necessary for deterministic regeneration.
    m.rows.extend(extra.rows)
    sol=work/'candidate.sol'
    command=[soplex,'--readmode=1','--solvemode=2','--int:checkmode=2',
             '--int:ratfac_minstalls=0','--bool:ratfacjump=true',
             '--real:feastol=0','--real:opttol=0','-s1','-g2','-v3','-t180',
             '-X='+str(sol),str(lp)]
    with (work/'solver.log').open('w') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
    # m.read checks every exact compressed row and box, including all extra
    # rows. The independent physical checker remains the evidence boundary.
    m.certificate(m.read(sol),work/'certificate.json')
    return work/'certificate.json'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--soplex',default='soplex');a=p.parse_args()
    a.work.mkdir(parents=True,exist_ok=True)
    if a.work.resolve()==HERE.parent or HERE.parent in a.work.resolve().parents:raise ValueError('work must be outside source checkout')
    generate(a.base,a.work,a.soplex)

if __name__=='__main__':main()
