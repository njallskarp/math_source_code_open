#!/usr/bin/env python3
"""Emit every monochromatic-four mass forbidden in anchor zero's neighborhoods."""
import argparse
import itertools as it
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    # Literal canonical anchor-zero star. The checker reconstructs it from all
    # 389 roots and audits every associated five-set clause in the source OPB.
    red={1,*range(2,8),*range(15,29)};blue=set(range(1,43))-red
    index={vs:125170+64*j for j,vs in enumerate(it.combinations(range(43),4))}
    with args.output.open('w') as f:
        for color,neighbors in ((0,blue),(1,red)):
            for vs in it.combinations(sorted(neighbors),4):f.write(f'-1 x{index[vs]+(63 if color else 0)} >= 0 ;\n')

if __name__=='__main__':main()
