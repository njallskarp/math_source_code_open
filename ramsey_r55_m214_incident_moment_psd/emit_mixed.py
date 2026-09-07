#!/usr/bin/env python3
"""Emit (2 a_h + x_rs - 14)^2 >= 0 in existing P3/P4 coordinates."""
import argparse,itertools as it,math
from pathlib import Path


def coefficients(center,neighbors,remote):
    neighbors=tuple(sorted(neighbors));r,s=sorted(remote);d=len(neighbors)
    if len(set(neighbors))!=d or center in neighbors or r==s or not {r,s}<=set(neighbors):raise ValueError('mixed star domain')
    edges={tuple(sorted((center,u))):8*d-60 for u in neighbors}
    for u in (r,s):edges[tuple(sorted((center,u)))]+=4
    edges[r,s]=-19
    wedges={(u,v,center):8 for u,v in it.combinations(neighbors,2)}
    wedges[tuple(sorted((s,center)))+(r,)]=4
    wedges[tuple(sorted((r,center)))+(s,)]=4
    products=[(tuple(sorted((center,u))),(r,s)) for u in neighbors if u not in (r,s)]
    return edges,wedges,products,4*d*(d-1)-188


def row():
    from check import geometry
    edge,_,_,names,_=geometry();names=dict(names);nxt=98759
    for key in sorted((u,v,h) for u,v in it.combinations(range(43),2) for h in range(43) if h not in(u,v)):
        if key not in names:names[key]=nxt;nxt+=1
    if nxt!=125170:raise ValueError('P3 support')
    ec,wc,products,rhs=coefficients(29,range(2,15),(2,8))
    terms={edge[e]:c for e,c in ec.items()};terms.update({names[w]:c for w,c in wc.items()})
    for e,f in products:
        vs=tuple(sorted(e+f));pairs=list(it.combinations(vs,2));rank=0;previous=-1
        for j,v in enumerate(vs):
            rank+=sum(math.comb(43-u-1,3-j) for u in range(previous+1,v));previous=v
        mask=(1<<pairs.index(e))|(1<<pairs.index(f))
        for state in range(64):
            if state&mask==mask:terms[125170+64*rank+state]=4
    if len(terms)!=270 or rhs!=436:raise ValueError('mixed square support')
    return ' '.join(f'{c:+d} x{i}' for i,c in sorted(terms.items()))+f' >= {rhs} ;\n'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(row())

if __name__=='__main__':main()
