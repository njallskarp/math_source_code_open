#!/usr/bin/env python3
"""Emit the universal squared star-count inequality in existing P3 coordinates."""
import argparse,itertools as it
from pathlib import Path


def coefficients(n,center,neighbors,offset):
    neighbors=tuple(sorted(neighbors))
    if len(set(neighbors))!=len(neighbors) or center in neighbors or any(v<0 or v>=n for v in (center,)+neighbors):raise ValueError('physical star')
    # Every red-red wedge is m_blue + x + x - 1.
    b=len(neighbors)
    edge_coefficient=2*b-1-2*offset
    edges={tuple(sorted((center,u))):edge_coefficient for u in neighbors}
    wedges={(u,v,center):2 for u,v in it.combinations(neighbors,2)}
    return edges,wedges,b*(b-1)-offset*offset


def row():
    from check import geometry
    edge,_,_,names,_=geometry();names=dict(names);next_name=98759
    for key in sorted((u,v,h) for u,v in it.combinations(range(43),2) for h in range(43) if h not in(u,v)):
        if key not in names:names[key]=next_name;next_name+=1
    if next_name!=125170:raise ValueError('complete P3 names')
    edges,wedges,rhs=coefficients(43,2,tuple(range(3,15))+(29,),6)
    terms={edge[k]:v for k,v in edges.items()};terms.update({names[k]:v for k,v in wedges.items()})
    if len(terms)!=91 or rhs!=120:raise ValueError('star-square support')
    return ' '.join(f'{v:+d} x{k}' for k,v in sorted(terms.items()))+f' >= {rhs} ;\n'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(row())

if __name__=='__main__':main()
