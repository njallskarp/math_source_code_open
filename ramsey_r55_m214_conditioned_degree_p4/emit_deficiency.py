#!/usr/bin/env python3
"""Emit sum a(h)^2 <= 1576 in the inherited x/blue-wedge coordinates."""
import argparse
from itertools import combinations
from pathlib import Path


def row():
    edge={e:i for i,e in enumerate(combinations(range(43),2),1)}
    inherited=set()
    for c in range(9,14):
        for k in range(7):
            sizes=(k,6-k,6-k,1+k,c-k,14-c+k,14-c+k,c-k)
            cells=[];start=2
            for size in sizes:cells.append(list(range(start,start+size)));start+=size
            core=set(cells[0]+cells[4]);outside=set(range(2,43))-core
            inherited.update((u,v,h) for u,v in combinations(sorted(outside),2) for h in core)
    if len(inherited)!=10612:raise ValueError('inherited support')
    names={k:13634+i for i,k in enumerate(sorted(inherited))}
    missing=[(u,v,h) for u,v in combinations(range(43),2) for h in range(43)
             if h not in (u,v) and (u,v,h) not in inherited]
    names.update({k:98759+i for i,k in enumerate(missing)})
    if len(names)!=37023 or max(names.values())!=125169:raise ValueError('full support')
    E=set(range(2,15));terms={}
    for (u,v),i in edge.items():
        count=int(u in E)+int(v in E)
        if count:terms[i]=-46 if count==2 else -25
    for key,i in names.items():
        if key[0] in E and key[1] in E:terms[i]=-2
    if len(terms)!=3666:raise ValueError('full global row')
    return ' '.join(f'{c:+d} x{i}' for i,c in sorted(terms.items()))+' >= -7972 ;\n'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.write_text(row())

if __name__=='__main__':main()
