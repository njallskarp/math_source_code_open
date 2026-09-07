#!/usr/bin/env python3
"""Emit the nonnegative square (e_R(A,B)-t)^2 using existing moments."""
import argparse
from itertools import combinations
from pathlib import Path


def wedge_names():
    inherited=set()
    for c in range(9,14):
        for k in range(7):
            sizes=(k,6-k,6-k,1+k,c-k,14-c+k,14-c+k,c-k)
            cells=[];first=2
            for size in sizes:cells.append(list(range(first,first+size)));first+=size
            core=set(cells[0]+cells[4]);outside=sorted(set(range(2,43))-core)
            inherited.update((u,v,h) for u,v in combinations(outside,2) for h in core)
    if len(inherited)!=10612:raise ValueError('inherited support')
    names={k:13634+i for i,k in enumerate(sorted(inherited))}
    missing=[(u,v,h) for u,v in combinations(range(43),2) for h in range(43) if h not in (u,v) and (u,v,h) not in inherited]
    names.update({k:98759+i for i,k in enumerate(missing)})
    return names


def coefficients(n,A,B,t,wedges,first_p):
    A=tuple(sorted(A));B=tuple(sorted(B))
    if set(A)&set(B) or not A or not B:raise ValueError('disjoint nonempty cut')
    edges={e:i for i,e in enumerate(combinations(range(n),2),1)}
    four={v:first_p+64*j for j,v in enumerate(combinations(range(n),4))}
    result={edges[tuple(sorted((u,v)))]:1-2*t+2*(len(A)+len(B)-2) for u in A for v in B}
    shared=0
    for left,right in ((A,B),(B,A)):
        for h in right:
            for u,v in combinations(left,2):result[wedges[u,v,h]]=2;shared+=1
    for a,b in combinations(A,2):
        for c,d in combinations(B,2):
            vertices=tuple(sorted((a,b,c,d)));pairs=list(combinations(vertices,2))
            masks=[sum(1<<pairs.index(tuple(sorted(e))) for e in matching)
                   for matching in (((a,c),(b,d)),((a,d),(b,c)))]
            for state in range(64):
                value=2*sum(state&mask==mask for mask in masks)
                if value:result[four[vertices]+state]=value
    return {i:c for i,c in sorted(result.items()) if c},2*shared-t*t


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    terms,rhs=coefficients(43,range(2,15),range(15,27),72,wedge_names(),125170)
    if len(terms)!=146094 or rhs!=-1596:raise ValueError('complete cut square')
    a.output.write_text(' '.join(f'{c:+d} x{i}' for i,c in terms.items())+f' >= {rhs} ;\n')

if __name__=='__main__':main()
