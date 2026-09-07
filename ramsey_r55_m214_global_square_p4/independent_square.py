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
    cut=[(u,v) for u in range(2,15) for v in range(15,27)]
    mean=sum(red_event(e,(e,)) for e in cut)
    second=mean+2*sum(red_event(e+f,(e,f)) for e,f in combinations(cut,2))
    value=second-144*mean+5184*D
    require(mean==72*D,'cut first moment')
    require(value < -353*D,'negative square below -353')
    print(json.dumps({'status':'INDEPENDENT_CUT_SQUARE_SEPARATOR_PASS',
          'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),
          'cut_mean':'72','cut_second_moment':str(Fraction(second,D)),
          'cut_square_value':str(Fraction(value,D)),'strict_upper_bound':-353},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
