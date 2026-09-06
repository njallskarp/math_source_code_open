#!/usr/bin/env python3
"""Emit the exact convex hull of the selector/anchor-unit interface."""
import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    source=HERE.parent/'ramsey_r55_m214_pair_normalization/pair_roots.py'
    if hashlib.sha256(source.read_bytes()).hexdigest()!='8fdccc44cab88d462cc122c055a9c54cffbefc957a73b6eeff84aa57a9e2256e':raise ValueError('parent root source changed')
    spec=importlib.util.spec_from_file_location('root_source',source);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    roots=[module.root(*key) for key in module.definitions()]
    units=[{(a,b):bit for a,b,bit in root['edge_units']} for root in roots]
    if len(units)!=389 or any(set(bits)!=set(units[0]) for bits in units):raise ValueError('complete anchor-unit domain')
    with args.output.open('w') as handle:
        for a,b in sorted(units[0]):
            index=a*(85-a)//2+b-a
            terms=[f'+1 x{index}']+[f'-1 x{13245+r}' for r,bits in enumerate(units) if bits[a,b]]
            handle.write(' '.join(terms)+' = 0 ;\n')

if __name__=='__main__':main()
