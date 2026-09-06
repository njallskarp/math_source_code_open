"""Producer-free budget recursion and DP verification of every physical case."""
import argparse
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
CAP=[78,85,93,100,107,115,125]

def require(ok,detail):
    if not ok:raise ValueError(detail)

def enumerate_profiles():
    answer=[];costs=[21,12,3,0,3,12,21]
    def visit(i,left,budget,n):
        if i==7:
            if left==0:
                d=sum((18+j)*x for j,x in enumerate(n))
                if d%2==0 and d<=902:answer.append(n)
            return
        for x in range(left+1):
            if x*costs[i]<=budget:visit(i+1,left-x,budget-x*costs[i],n+[x])
    visit(0,43,39,[])
    return sorted(answer)

@lru_cache(None)
def minimum_cost(length,upper,limit,kind):
    states={0:0}
    for _ in range(length):
        after={}
        for total,cost in states.items():
            for d in range(min(upper,limit-total)+1):
                key=total+d;value=cost+(d*d if kind=='square' else d*(d-1)//2)
                after[key]=min(after.get(key,10**9),value)
        states=after
    return states

@lru_cache(None)
def missing_weight(side,h):
    # Bounded knapsack from degree-class pair multiplicities, not sorted edges.
    bins=Counter()
    for i in range(7):
        for j in range(i,7):
            multiplicity=side[i]*side[j] if i!=j else side[i]*(side[i]-1)//2
            bins[6-i-j]+=multiplicity
    states={0:0}
    for weight,multiplicity in sorted(bins.items()):
        after={}
        for used,value in states.items():
            for k in range(min(multiplicity,h-used)+1):
                after[used+k]=max(after.get(used+k,-10**9),value+k*weight)
        states=after
    return states[h]

def reconstruct(stream=None):
    ns=enumerate_profiles();counts=Counter();census=Counter();slice_counts={}
    placements=candidates=0;minimum={};examples={};digest=hashlib.sha256()
    for index,original in enumerate(ns):
        M=sum((18+i)*k for i,k in enumerate(original))//2-231
        require(214<=M<=220,'slice');census[M]+=1
        weight=sum(k*w for k,w in zip(original,[21,12,3,0,3,12,21]))
        require(weight%6==3,'parity')
        all_caps=sum(k*(CAP[i]+CAP[6-i]) for i,k in enumerate(original))
        mixed=sum(k*(18+i)*(24-i) for i,k in enumerate(original))
        S=all_caps-(3*comb(43,3)-3*mixed//2)
        require(2*S==43-weight,'total cap deficit')
        for color in (0,1):
            n=original if color==0 else original[::-1]
            m=sum((18+i)*k for i,k in enumerate(n))//2
            sides=[()]
            for multiplicity in n:
                sides=[s+(k,) for s in sides for k in range(multiplicity+1) if sum(s)+k<=21]
            for side in sorted(sides):
                a=sum(side)
                if a==0:continue
                placements+=1;b=43-a;D=sum((18+i)*x for i,x in enumerate(side))
                C=sum(CAP[i]*x for i,x in enumerate(side));old=18*a-2*(3*a*a//8)
                # Descending edge counts give the producer's ascending cut order.
                for e in range(min(comb(a,2),D//2),-1,-1):
                    q=D-2*e
                    if q>=old:break
                    candidates+=1;h=comb(a,2)-e
                    gap=minimum_cost(a,a-1,a*(a-1),'square')[2*e]-a*e-C
                    route='internal'
                    if gap<=0:
                        wedges=minimum_cost(b,a,108,'pairs')[q]
                        lost_triangles=h*(a-2)
                        gap=3*(comb(a,3)-lost_triangles)+2*(wedges-b*h)-C
                        route='cross'
                    if gap<=0:
                        internal_weight=(a-1)*sum((3-i)*x for i,x in enumerate(side))
                        outside_lower=sum(a*(3-i)*(n[i]-side[i]) for i in range(4,7))
                        local_upper=S+sum(x*(21*(18+i)+(24-i)*(23-i)//2-m-CAP[i]-CAP[6-i]) for i,x in enumerate(side))
                        gap=internal_weight+outside_lower-local_upper-missing_weight(side,h)
                        route='weighted'
                    require(gap>0,('surviving cut',original,color,side,q))
                    counts[route]+=1;slice_counts.setdefault(M,Counter())[route]+=1
                    minimum[route]=min(minimum.get(route,gap),gap)
                    key=[index,color,*side,q,route,gap]
                    raw=(json.dumps(key,separators=(',',':'))+'\n').encode()
                    digest.update(raw)
                    if stream is not None:stream.write(raw)
                    if original==[0,2,5,36,0,0,0] and color==0 and route not in examples:
                        examples[route]={'side':list(side),'q':q,'missing':h,'gap':gap}
    return {'format':'r55-complete-hard-cut-composition-v1','caps':CAP,'profiles':ns,
            'profile_counts_by_M':{str(k):v for k,v in sorted(census.items())},
            'oriented_side_placements':placements,'candidate_violations':candidates,
            'closed_by':dict(counts),'closed_by_M':{str(m):dict(v) for m,v in sorted(slice_counts.items())},
            'minimum_positive_gaps':minimum,'candidate_stream_sha256':digest.hexdigest(),
            'q_by_size':[18*a-2*(3*a*a//8) for a in range(1,22)],
            'M216_examples':examples,'unexcluded_candidates':0}

def physical_controls():
    graphs=cuts=0
    for n in range(1,7):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            adj=[set() for _ in range(n)]
            for bit,(u,v) in enumerate(pairs):
                if mask>>bit&1:adj[u].add(v);adj[v].add(u)
            d=list(map(len,adj));m=sum(d)//2
            tr=[sum(v in adj[u] for u,v in combinations(adj[w],2)) for w in range(n)]
            tb=[sum(v not in adj[u] for u,v in combinations(set(range(n))-{w}-adj[w],2)) for w in range(n)]
            require(sum(tr)+sum(tb)==3*comb(n,3)-3*sum(x*(n-1-x) for x in d)//2,'mixed identity')
            gamma=n//2;weights=[gamma-x for x in d]
            # Synthetic literal cap slack permits a non-vacuous universal control.
            slack=[(v+mask)%3 for v in range(n)];S=sum(slack)
            H=[gamma*d[v]+comb(n-1-d[v],2)-m-tr[v]-tb[v]-slack[v] for v in range(n)]
            for v in range(n):
                require(sum(weights[u] for u in adj[v])==H[v]+slack[v],'local identity')
            if n<=5:
                for sm in range(1,(1<<n)-1):
                    A={v for v in range(n) if sm>>v&1};B=set(range(n))-A;a=len(A);b=len(B)
                    e=sum(v in adj[u] for u,v in combinations(A,2));q=sum(len(adj[u]&B) for u in A);h=comb(a,2)-e
                    C=sum(tr[v] for v in A)
                    F=minimum_cost(b,a,a*b,'pairs')[q]
                    require(3*(comb(a,3)-h*(a-2))+2*(F-b*h)<=C,'cross-wedge bound')
                    actual_missing=sum(weights[u]+weights[v] for u,v in combinations(A,2) if v not in adj[u])
                    required=(a-1)*sum(weights[v] for v in A)+a*sum(min(0,weights[v]) for v in B)-sum(H[v] for v in A)-S
                    require(required<=actual_missing,'weighted missing-edge bound')
                    cuts+=1
            graphs+=1
    # Independent knapsack controls include negative pair weights.
    knapsack_cases=0
    for side in [(2,0,0,0,0,0,0),(1,1,0,1,0,0,0),(0,0,2,0,1,0,0),(1,0,0,0,0,0,2)]:
        ws=[3-i for i,x in enumerate(side) for _ in range(x)]
        values=[x+y for x,y in combinations(ws,2)]
        for h in range(len(values)+1):
            brute=max(sum(values[i] for i in selected) for selected in combinations(range(len(values)),h))
            require(brute==missing_weight(tuple(side),h),'knapsack control');knapsack_cases+=1
    return {'labeled_graph_controls':graphs,'physical_cut_controls':cuts,'knapsack_controls':knapsack_cases}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stream',type=Path);args=parser.parse_args()
    raw=(HERE/'certificate.json').read_bytes();doc=json.loads(raw)
    if args.stream:
        with args.stream.open('wb') as f:computed=reconstruct(f)
    else:computed=reconstruct()
    require(doc==computed,'certificate differs from independent reconstruction')
    mutations=[]
    d=deepcopy(doc);d['profiles'].pop();mutations.append(d)
    d=deepcopy(doc);d['candidate_violations']-=1;mutations.append(d)
    d=deepcopy(doc);d['caps'][0]+=1;mutations.append(d)
    d=deepcopy(doc);d['closed_by']['weighted']=0;mutations.append(d)
    d=deepcopy(doc);d['q_by_size'][14]+=1;mutations.append(d)
    d=deepcopy(doc);d['candidate_stream_sha256']='0'*64;mutations.append(d)
    for d in mutations:require(d!=computed,'accepted certificate mutation')
    report={'status':'VERIFIED_COMPLETE_HARD_CAP_CUT_REDUNDANCY',
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'candidate_stream_sha256':computed['candidate_stream_sha256'],
            'profiles':len(computed['profiles']),'oriented_side_placements':computed['oriented_side_placements'],
            'candidate_violations':computed['candidate_violations'],'closed_by':computed['closed_by'],
            'mutations_rejected':len(mutations),**physical_controls()}
    print(json.dumps(report,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
