#!/usr/bin/env python3
"""Regenerate a rational Q+G candidate; the full checker is separate."""
import argparse,hashlib,importlib.util,itertools as it,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ramsey_r55_m214_conditioned_degree_p4/discover.py'
PIN='c71f605a97c22b262f8daebb068aa2edc7af9e6657fbd724f19fde857c486177'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=PIN:raise ValueError('changed Q producer')
spec=importlib.util.spec_from_file_location('q_producer',SOURCE)
parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)


def generate(base,work,soplex):
    m=parent.conditioned_model(base);extra=parent.extra_model();lp=work/'candidate.lp';m.write(lp)
    head,tail=lp.read_text().split('Bounds\n')
    rows=''.join(' extra'+str(j)+': '+' '.join(f'{c:+d} p{i}' for i,c in row)+f' {rel} {rhs}\n'
                 for j,(row,rel,rhs) in enumerate(extra.rows))
    m.rows.extend(extra.rows)
    parts=[]
    for h in range(43):
        neighbors=[v for v in range(2,15) if v!=h]
        parts.extend((-1,m.event((h,u),red=[(h,u)])) for u in neighbors)
        parts.extend((-2,m.event((h,u,v),red=[(h,u),(h,v)])) for u,v in it.combinations(neighbors,2))
    before=len(m.rows);m.addparts(parts,'>=',-1576)
    if len(m.rows)!=before+1 or len(m.rows)!=19632:raise ValueError('global row coverage')
    row,rel,rhs=m.rows[-1]
    rows+=' globalG: '+' '.join(f'{c:+d} p{i}' for i,c in row)+f' {rel} {rhs}\n'
    lp.write_text(head+rows+'Bounds\n'+tail)
    sol=work/'candidate.sol'
    command=[soplex,'--readmode=1','--solvemode=2','--int:checkmode=2',
             '--int:ratfac_minstalls=0','--bool:ratfacjump=true',
             '--real:feastol=0','--real:opttol=0','-s1','-g2','-v3','-t180',
             '-X='+str(sol),str(lp)]
    with (work/'solver.log').open('w') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
    m.certificate(m.read(sol),work/'certificate.json')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--soplex',default='soplex');a=p.parse_args()
    work=a.work.resolve()
    if work==HERE.parent or HERE.parent in work.parents:raise ValueError('work must be outside source checkout')
    work.mkdir(parents=True,exist_ok=True);generate(a.base,work,a.soplex)

if __name__=='__main__':main()
