#!/usr/bin/env python3
"""Emit all prescribed-degree identities conditioned on three-vertex states."""
import argparse,itertools as it
from collections import Counter
from pathlib import Path

def family(n=43,exceptional=frozenset(range(2,15)),first_p=125170,witness=False,degrees=None):
    indices={vs:first_p+64*j for j,vs in enumerate(it.combinations(range(n),4))}
    triples=[(14,27,29)] if witness else it.combinations(range(n),3)
    for A in triples:
        outside=[v for v in range(n) if v not in A];b=outside[0]
        pairA=list(it.combinations(A,2))
        for h in ([27] if witness else A):
            degree=degrees[h] if degrees is not None else (20 if h in exceptional else 21)
            for state in ([0] if witness else range(8)):
                local=sum(state>>j&1 for j,e in enumerate(pairA) if h in e)
                row=Counter()
                for w in outside:
                    Q=tuple(sorted(A+(w,)));pairs=list(it.combinations(Q,2))
                    bits=[pairs.index(pair) for pair in pairA];incident=pairs.index(tuple(sorted((h,w))))
                    for s in range(64):
                        if sum((s>>bit&1)<<j for j,bit in enumerate(bits))!=state:continue
                        if s>>incident&1:row[indices[Q]+s]+=1
                        if w==b:row[indices[Q]+s]-=degree-local
                yield A,h,state,dict(sorted((i,c) for i,c in row.items() if c))

def text_row(row):return ' '.join(f'{c:+d} x{i}' for i,c in row.items())+' = 0 ;\n'

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--witness-only',action='store_true');a=p.parse_args()
    with a.output.open('w') as f:
        for A,h,state,row in family(witness=a.witness_only):f.write(text_row(row))

if __name__=='__main__':main()
