#!/usr/bin/env python3
"""Independent edge-set decoding of the global squared-neighbor separator only."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations,permutations
import json
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate',type=Path);a=p.parse_args()
    raw=json.loads(a.certificate.read_text());D=raw['denominator'];cells=raw['cells']
    require(type(D)==int and D>0,'positive integer denominator')
    require(sorted(sum(cells,[]))==list(range(43)),'vertex partition')
    cls={v:t for t,cell in enumerate(cells) for v in cell};pairs=list(combinations(range(4),2));tables={}
    for record in raw['four_tables']:
        types=tuple(record['types']);require(types not in tables,'unique table');distribution={}
        for text,mass in record['orbits'].items():
            require(type(mass)==int and 0<mass<=D,'positive mass')
            edges=frozenset(e for j,e in enumerate(pairs) if int(text)&(1<<j))
            orbit=set()
            for permutation in permutations(range(4)):
                if any(types[j]!=types[permutation[j]] for j in range(4)):continue
                orbit.add(frozenset(tuple(sorted((permutation[u],permutation[v]))) for u,v in edges))
            require(not(set(distribution)&orbit),'disjoint orbits')
            distribution.update({e:mass for e in orbit})
        require(sum(distribution.values())==D,'normalized edge-set distribution');tables[types]=distribution
    cache={}
    def red_event(vertices,edges):
        vertices=set(vertices)
        for v in range(43):
            if len(vertices)==4:break
            vertices.add(v)
        ordered=sorted(vertices,key=lambda v:(cls[v],v));types=tuple(cls[v] for v in ordered)
        required=frozenset(tuple(sorted((ordered.index(u),ordered.index(v)))) for u,v in edges)
        key=(types,required)
        if key not in cache:cache[key]=sum(m for e,m in tables[types].items() if required<=e)
        return cache[key]
    E=set(range(2,15));means=[];squares=[]
    for h in range(43):
        targets=sorted(E-{h})
        mean=sum(red_event((h,u),((h,u),)) for u in targets)
        square=mean+2*sum(red_event((h,u,v),((h,u),(h,v))) for u,v in combinations(targets,2))
        means.append(mean);squares.append(square)
    require(sum(means)==260*D,'first moment')
    # This decoder checks the separated scalar, not the full LP or marginal
    # compatibility; the complete checker is a separate reproduction step.
    gap=sum(squares)-1576*D;require(gap>71*D,'strict gap greater than 71')
    print(json.dumps({'status':'INDEPENDENT_GLOBAL_SQUARE_SEPARATOR_PASS',
          'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),
          'sum_a':'260','sum_a2':str(Fraction(sum(squares),D)),
          'upper_bound':1576,'gap':str(Fraction(gap,D)),'strict_gap_lower_bound':71},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
