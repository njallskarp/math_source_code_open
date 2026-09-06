"""Independent budget recursion and degree-sequence DP; imports no producer."""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent

def require(ok, detail):
    if not ok: raise ValueError(detail)

def budget_profiles():
    result=[]
    weights=(21,12,3,0,3,12,21)
    def walk(i, left, budget, prefix):
        if i==7:
            if left==0:
                total=sum((18+j)*x for j,x in enumerate(prefix))
                if total%2==0 and total<=902: result.append(tuple(prefix))
            return
        for x in range(left+1):
            if x*weights[i]<=budget: walk(i+1,left-x,budget-x*weights[i],prefix+[x])
    walk(0,43,39,[])
    return sorted(result)

@lru_cache(None)
def square_dp(order):
    states={0:0}
    for _ in range(order):
        following={}
        for total,cost in states.items():
            for degree in range(order):
                key=total+degree
                value=cost+degree*degree
                following[key]=min(following.get(key,10**9),value)
        states=following
    return states

@lru_cache(None)
def ceiling(order, cap):
    costs=square_dp(order)
    return max(s//2 for s,cost in costs.items() if s%2==0 and cost-order*(s//2)<=cap)

def check(doc):
    caps=[78,85,93,100,107,115,125]
    require(doc['format']=='r55-hard-cap-cut-bridge-v1','format')
    require(doc['caps_18_to_24']==caps,'caps')
    ns=budget_profiles()
    require(doc['profiles']==[list(n) for n in ns],'complete profiles')
    count=Counter(); tables={m:[[1000]*21 for _ in range(2)] for m in range(214,221)}
    records=[]
    for n in ns:
        total=sum((18+i)*x for i,x in enumerate(n));m=total//2-231
        require(214<=m<=220,'slice');count[m]+=1
        weight=sum(x*w for x,w in zip(n,[21,12,3,0,3,12,21]))
        mixed=sum(x*(18+i)*(24-i) for i,x in enumerate(n))
        triangle_incidence=3*12341-3*mixed//2
        cap_total=sum(x*(caps[i]+caps[6-i]) for i,x in enumerate(n))
        require(2*(cap_total-triangle_incidence)==43-weight,'defect identity')
        # Add degree classes one at a time, retaining every partial marking.
        states=[(0,0,0,())]
        for i,multiplicity in enumerate(n):
            states=[(a+k,d+k*(18+i),c+k*caps[i],v+(k,))
                    for a,d,c,v in states for k in range(multiplicity+1) if a+k<=21]
        for a,d,c,side in sorted(states,key=lambda v:v[3]):
            if a==0: continue
            records.append(','.join(map(str,n))+';'+','.join(map(str,side))+'\n')
            blue_d=42*a-d
            blue_c=sum(x*caps[6-i] for i,x in enumerate(side))
            for color,ds,cs in ((0,d,c),(1,blue_d,blue_c)):
                lower=ds-2*ceiling(a,cs)
                tables[m][color][a-1]=min(tables[m][color][a-1],lower)
    require({str(k):v for k,v in sorted(count.items())}==doc['profile_counts_by_M'],'profile counts')
    require({str(k):v for k,v in tables.items()}==doc['lower_bounds_by_M'],'all cut tables')
    require(len(records)==doc['side_placements'],'placements')
    require(hashlib.sha256(''.join(records).encode()).hexdigest()==doc['placement_sha256'],'placement stream')
    universal=[min(tables[m][color][a] for m in tables for color in (0,1)) for a in range(21)]
    require(universal==doc['universal_lower_bounds'],'universal table')
    require(doc['uniform_two_side_bound']==min(universal[1:])==35,'two-side gap')
    require(doc['uniform_three_side_bound']==min(universal[2:])==51,'three-side gap')
    old=[18*a-2*(3*a*a//8) for a in range(1,22)]
    require(old==doc['old_full_q_bound'],'old cut schema')
    require(doc['sizes_where_this_bound_does_not_dominate_old_q']==[
        a for a in range(1,22) if universal[a-1]<old[a-1]],'full-q limitation')
    return len(ns),len(records)

def controls():
    graphs=cuts=0
    for n in range(1,7):
        pairs=list(combinations(range(n),2))
        for word in range(1<<len(pairs)):
            adj=[set() for _ in range(n)]
            for bit,(u,v) in enumerate(pairs):
                if word>>bit&1:adj[u].add(v);adj[v].add(u)
            degrees=list(map(len,adj));edges=sum(degrees)//2
            triangles=sum(v in adj[u] and w in adj[u] and w in adj[v]
                          for u,v,w in combinations(range(n),3))
            require(3*triangles>=sum(d*d for d in degrees)-n*edges,'codegree inequality')
            require(square_dp(n)[2*edges]<=sum(d*d for d in degrees),'square lower bound')
            if n<=5:
                local=[sum(v in adj[u] for u,v in combinations(sorted(adj[w]),2)) for w in range(n)]
                for mask in range(1,1<<n):
                    side={v for v in range(n) if mask>>v&1};a=len(side)
                    e=sum(v in adj[u] for u,v in combinations(sorted(side),2))
                    boundary=sum(len(adj[u]-side) for u in side)
                    cap=sum(local[u] for u in side)
                    require(e<=ceiling(a,cap),'physical induced-edge ceiling')
                    require(boundary==sum(degrees[u] for u in side)-2*e,'physical cut identity')
                    cuts+=1
            graphs+=1
    large=[]
    for a in (19,20,21):
        e=(21*a-63+1)//2
        gap=4*e*e-a*a*e-125*a*a
        require(gap>0 and 8*e>a*a,'large-side hand proof')
        large.append([a,e,gap])
    return {'labeled_graphs':graphs,'literal_cut_controls':cuts,'large_side_hand_gaps':large}

def main():
    raw=(HERE/'certificate.json').read_bytes();doc=json.loads(raw)
    profiles,placements=check(doc)
    bad=[]
    d=deepcopy(doc);d['profiles'].pop();bad.append(d)
    d=deepcopy(doc);d['lower_bounds_by_M']['216'][0][15]+=1;bad.append(d)
    d=deepcopy(doc);d['caps_18_to_24'][0]+=1;bad.append(d)
    d=deepcopy(doc);d['placement_sha256']='0'*64;bad.append(d)
    d=deepcopy(doc);d['uniform_three_side_bound']=52;bad.append(d)
    d=deepcopy(doc);d['sizes_where_this_bound_does_not_dominate_old_q']=[];bad.append(d)
    for changed in bad:
        try:check(changed)
        except ValueError:pass
        else:raise ValueError('accepted mutation')
    report={'status':'VERIFIED_HARD_CAP_35_51_CUT_BRIDGE','profiles':profiles,
            'side_placements':placements,'mutations_rejected':len(bad),
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),**controls()}
    print(json.dumps(report,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
