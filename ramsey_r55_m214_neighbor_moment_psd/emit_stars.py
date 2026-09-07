#!/usr/bin/env python3
"""Emit the complete star-event family in the existing P4 coordinates."""
import argparse,itertools as it
from pathlib import Path

def rows(n=43,first_p=125170):
    edge={pair:i for i,pair in enumerate(it.combinations(range(n),2),1)}
    for j,vs in enumerate(it.combinations(range(n),4)):
        for h in range(n):
            if h in vs:continue
            variables=[edge[tuple(sorted((h,v)))] for v in vs]
            for color in (0,1):
                p=first_p+64*j+(63 if color else 0)
                sign='-1' if color else '+1'
                yield ' '.join(f'{sign} x{v}' for v in variables)+f' -1 x{p} >= '+('-4' if color else '0')+' ;\n'

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    with a.output.open('w') as f:f.writelines(rows())

if __name__=='__main__':main()
