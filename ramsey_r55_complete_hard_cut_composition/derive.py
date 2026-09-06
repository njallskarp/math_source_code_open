"""Exact complete cut-violation census; see README for the physical reduction."""
import argparse
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json

CAP=(78,85,93,100,107,115,125)

def profiles():
    out=[]
    for a,b,c,e,f,g in product(range(2),range(4),range(14),range(14),range(4),range(2)):
        n=(a,b,c,43-a-b-c-e-f-g,e,f,g)
        w=21*(a+g)+12*(b+f)+3*(c+e)
        d=sum((18+i)*k for i,k in enumerate(n))
        if min(n)>=0 and w<=39 and d%2==0 and d<=902:out.append(n)
    return sorted(out)

def payload(stream=None):
    ns=profiles();digest=hashlib.sha256();count=Counter();by_slice={}
    placements=candidates=0;minimum={};examples={}
    for index,original in enumerate(ns):
        M=sum((18+i)*k for i,k in enumerate(original))//2-231
        for color in (0,1):
            n=original if color==0 else original[::-1]
            m=sum((18+i)*k for i,k in enumerate(n))//2
            S=(43-sum(k*w for k,w in zip(n,(21,12,3,0,3,12,21))))//2
            for side in product(*(range(k+1) for k in n)):
                a=sum(side)
                if not 1<=a<=21:continue
                placements+=1;b=43-a;old=18*a-2*(3*a*a//8)
                D=sum((18+i)*k for i,k in enumerate(side));C=sum(CAP[i]*k for i,k in enumerate(side))
                weighted=None
                for q in range(max(0,D-a*(a-1)),old):
                    if (D-q)%2:continue
                    candidates+=1;e=(D-q)//2;h=comb(a,2)-e;k,r=divmod(2*e,a)
                    gap=(a-r)*k*k+r*(k+1)**2-a*e-C;route='internal'
                    if gap<=0:
                        k,r=divmod(q,b)
                        gap=3*comb(a,3)+2*(b*comb(k,2)+r*k)-(a+80)*h-C
                        route='cross'
                    if gap<=0:
                        if weighted is None:
                            weights=[3-i for i,k in enumerate(side) for _ in range(k)]
                            values=sorted((x+y for x,y in combinations(weights,2)),reverse=True)
                            top=[0]
                            for value in values:top.append(top[-1]+value)
                            negative=sum(min(0,3-i)*(n[i]-side[i]) for i in range(7))
                            H=sum(k*(21*(18+i)+comb(24-i,2)-m-CAP[i]-CAP[6-i]) for i,k in enumerate(side))
                            weighted=((a-1)*sum(weights)+a*negative-H-S,top)
                        gap=weighted[0]-weighted[1][h];route='weighted'
                    if gap<=0:raise ValueError(('unexcluded candidate',original,color,side,q))
                    count[route]+=1;by_slice.setdefault(M,Counter())[route]+=1
                    minimum[route]=min(minimum.get(route,gap),gap)
                    key=[index,color,*side,q,route,gap]
                    raw=(json.dumps(key,separators=(',',':'))+'\n').encode()
                    digest.update(raw)
                    if stream is not None:stream.write(raw)
                    if original==(0,2,5,36,0,0,0) and color==0 and route not in examples:
                        examples[route]={'side':side,'q':q,'missing':h,'gap':gap}
    return {'format':'r55-complete-hard-cut-composition-v1','caps':CAP,
            'profiles':ns,'profile_counts_by_M':dict(sorted(Counter(sum((18+i)*k for i,k in enumerate(n))//2-231 for n in ns).items())),
            'oriented_side_placements':placements,'candidate_violations':candidates,
            'closed_by':dict(count),'closed_by_M':{m:dict(v) for m,v in sorted(by_slice.items())},
            'minimum_positive_gaps':minimum,'candidate_stream_sha256':digest.hexdigest(),
            'q_by_size':[18*a-2*(3*a*a//8) for a in range(1,22)],
            'M216_examples':examples,'unexcluded_candidates':0}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stream',type=Path);args=parser.parse_args()
    if args.stream:
        with args.stream.open('wb') as f:out=payload(f)
    else:out=payload()
    print(json.dumps(out,sort_keys=True,separators=(',',':')))
