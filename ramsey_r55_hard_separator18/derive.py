"""Exact arithmetic accompanying the written separator classification."""
from collections import Counter
from itertools import product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

CAP=(78,85,93,100,107,115,125)
COST=(21,12,3,0,3,12,21)

def profiles():
    result=[]
    for a,b,c,e,f,g in product(range(2),range(4),range(14),range(14),range(4),range(2)):
        n=(a,b,c,43-a-b-c-e-f-g,e,f,g)
        degree=sum((18+i)*v for i,v in enumerate(n))
        if min(n)>=0 and sum(x*y for x,y in zip(n,COST))<=39 and degree%2==0 and degree<=902:
            result.append(n)
    return sorted(result)

def produce(stream=None):
    ns=profiles();census={};trace=hashlib.sha256();subset_count=0;survivors=[]
    for n in ns:
        M=sum((18+i)*v for i,v in enumerate(n))//2-231
        category='red18' if n[0] else 'blue18' if n[6] else 'both_at_least19'
        census.setdefault(M,Counter())[category]+=1
        for color in (0,1):
            p=n if color==0 else n[::-1]
            m=sum((18+i)*v for i,v in enumerate(p))//2
            for a in product(*(range(v+1) for v in p)):
                if sum(a)!=12:continue
                degree=sum((18+i)*v for i,v in enumerate(a));subset_count+=1
                raw=(json.dumps([list(n),color,list(a),degree],separators=(',',':'))+'\n').encode()
                trace.update(raw)
                if stream is not None:stream.write(raw)
                if degree>240 or degree%2:continue
                outside=[p[i]-a[i] for i in range(7)]
                internal_weight=8  # proved in README: A is 8-regular, all degree20
                outside_min=sum(min(0,21-(18+i))*v for i,v in enumerate(outside))
                H=21*20+comb(22,2)-m-CAP[2]-CAP[4]
                slack=(43-sum(x*y for x,y in zip(p,COST)))//2
                per_vertex=internal_weight+outside_min-H
                survivors.append({'profile':p,'A':a,'outside':outside,'m':m,'M':m-231,
                    'total_slack':slack,'H20':H,'neighbor_weight_lower':8+outside_min,
                    'slack_per_A_vertex_at_least':per_vertex,
                    'required_A_slack':12*per_vertex,'contradiction_gap':12*per_vertex-slack})
    clique=[]
    for k in range(19):
        for a in (2,3,4):
            lower=a*(19-a)-(a-1)*k;upper={2:13,3:4,4:0}[a]
            clique.append([k,a,lower,upper,lower-upper])
    nonclique=[[k,a,b] for k in range(19) for a in range(2,14) for b in range(a,14) if a+b==43-k]
    return {'format':'r55-hard-separator18-v1','caps':CAP,'profiles':ns,
        'profile_census_by_M':{str(k):dict(v) for k,v in sorted(census.items())},
        'profile_categories':dict(Counter('red18' if n[0] else 'blue18' if n[6] else 'both_at_least19' for n in ns)),
        'clique_component_rows':clique,'nonclique_size_rows':nonclique,
        'twelve_subset_count':subset_count,'twelve_subset_stream_sha256':trace.hexdigest(),
        'saturated_degree_rows':survivors,
        'allowed_separator18_component_sizes':[1,24],
        'allowed_separator18_independence_numbers':[1,3],
        'full_two_nontrivial_part_sizes':[[a,25-a] for a in range(2,13)]}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stream',type=Path);args=parser.parse_args()
    if args.stream:
        with args.stream.open('wb') as out:doc=produce(out)
    else:doc=produce()
    print(json.dumps(doc,sort_keys=True,separators=(',',':')))
