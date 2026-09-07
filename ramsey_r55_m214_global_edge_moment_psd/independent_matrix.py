#!/usr/bin/env python3
"""Independent edge-set decoding and integer Bareiss checks of all incident Gram matrices."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations,permutations
import json
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def bareiss_rank(matrix):
    a=[row[:] for row in matrix];n=len(a);previous=1;rank=0
    require(all(len(row)==n for row in a),'square input')
    require(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)),'symmetric input')
    for k in range(n):
        pivot=a[k][k];require(pivot>=0,'negative Bareiss pivot')
        if pivot==0:
            require(all(a[k][j]==0 for j in range(k+1,n)),'nonzero Bareiss zero-pivot row')
            continue
        rank+=1
        for i in range(k+1,n):
            for j in range(i,n):
                numerator=pivot*a[i][j]-a[i][k]*a[k][j]
                quotient,remainder=divmod(numerator,previous)
                require(remainder==0,'exact Bareiss division')
                a[i][j]=a[j][i]=quotient
        for i in range(k+1,n):a[i][k]=a[k][i]=0
        previous=pivot
    return rank


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
    adj={h:[tuple(sorted((h,u))) for u in range(2,15) if h!=u] for h in range(43)}
    mean=[sum(red_event(e,(e,)) for e in adj[h]) for h in range(43)]
    factor=[1]+[7 if h in (29,30) else 6 for h in range(43)]
    require(mean==[D*v for v in factor[1:]],'all physical means')
    matrix=[[D]+mean]+[[mean[h]]+[sum(red_event(e+f,(e,f)) for e in adj[h] for f in adj[k]) for k in range(43)] for h in range(43)]
    for i in range(44):
        for j in range(44):require(matrix[i][j]==D*factor[i]*factor[j],'full physical Gram entry')
    neighbors=tuple(range(3,15))+(29,);star=[(2,u) for u in neighbors]
    bmean=sum(red_event(e,(e,)) for e in star)
    bsecond=bmean+2*sum(red_event(e+f,(e,f)) for e,f in combinations(star,2))
    square=bsecond-12*bmean+36*D
    require(square>=0,'former star square nonnegative')
    # Decode all physical matrices from edge sets. Cache only byte-for-byte
    # equal full matrices, without importing the contrast decomposition.
    ranks=[];cache_matrices={};physical_entries=0
    for h in range(43):
        edges=[tuple(sorted((h,u))) for u in range(43) if u!=h]
        first=[red_event(e,(e,)) for e in edges]
        gram=[[D]+first]+[[first[i]]+[red_event(e+f,(e,f)) for f in edges] for i,e in enumerate(edges)]
        key=tuple(map(tuple,gram))
        if key not in cache_matrices:cache_matrices[key]=bareiss_rank(gram)
        ranks.append(cache_matrices[key]);physical_entries+=43**2
    weighted=[(tuple(sorted((29,u))),2) for u in range(2,15)]+[((2,8),1)]
    mixed_mean=sum(c*red_event(e,(e,)) for e,c in weighted)
    mixed_second=sum(c*d*red_event(e+f,(e,f)) for e,c in weighted for f,d in weighted)
    mixed=mixed_second-28*mixed_mean+196*D
    require(mixed>=0,'former mixed square repaired')
    print(json.dumps({'status':'INDEPENDENT_INCIDENT_PSD_BAREISS_PASS',
          'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),
          'mixed_square':str(Fraction(mixed,D)),'incident_physical_entries':physical_entries,'incident_ranks':ranks,'distinct_full_matrices':len(cache_matrices),'order':44,'physical_entries':1936,'factor':factor,'rank':1,
          'star_count_mean':str(Fraction(bmean,D)),'star_count_second_moment':str(Fraction(bsecond,D)),'star_square':str(Fraction(square,D)),'trace_without_constant':1574,'covariance_maximum_absolute_entry':'0'},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
