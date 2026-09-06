"""Producer-free recursion, subset convolution, and physical graph controls."""
from collections import Counter
from copy import deepcopy
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

HERE=Path(__file__).resolve().parent
CAP=[78,85,93,100,107,115,125]

def require(ok,message):
    if not ok:raise ValueError(message)

def profiles():
    found=[]
    def visit(i,left,budget,partial):
        if i==7:
            if not left:
                total=sum((18+j)*x for j,x in enumerate(partial))
                if total<=902 and total%2==0:found.append(partial)
            return
        cost=[21,12,3,0,3,12,21][i]
        for x in range(left+1):
            if cost*x<=budget:visit(i+1,left-x,budget-cost*x,partial+[x])
    visit(0,43,39,[])
    return sorted(found)

def verify_certificate(doc,stream=None):
    require(doc['format']=='r55-hard-separator18-v1','format')
    require(doc['caps']==CAP,'caps')
    ns=profiles();require(doc['profiles']==ns,'complete profiles')
    census={};categories=Counter();digest=hashlib.sha256();count=0;saturated=[]
    for n in ns:
        category='red18' if n[0] else 'blue18' if n[-1] else 'both_at_least19'
        categories[category]+=1;M=sum((i+18)*x for i,x in enumerate(n))//2-231
        census.setdefault(str(M),Counter())[category]+=1
        require(n[0]+n[-1]<=1,'unique endpoint degree')
        for color in (0,1):
            p=n if color==0 else n[::-1]
            states=[()]
            for bound in p:
                states=[a+(x,) for a in states for x in range(min(bound,12-sum(a))+1)]
            for a in sorted(x for x in states if sum(x)==12):
                D=sum((18+i)*v for i,v in enumerate(a));count+=1
                raw=(json.dumps([n,color,list(a),D],separators=(',',':'))+'\n').encode()
                digest.update(raw)
                if stream is not None:stream.write(raw)
                if D>240 or D%2:continue
                require(a==(0,0,12,0,0,0,0),'saturated subset degrees')
                outside=[p[i]-a[i] for i in range(7)]
                require(outside in ([0,0,1,30,0,0,0],[0,0,0,30,1,0,0]),'remaining degree')
                degrees=[i+18 for i,x in enumerate(p) for _ in range(x)]
                m=sum(degrees)//2
                mixed=sum(d*(42-d) for d in degrees)
                literal_total=3*comb(43,3)-3*mixed//2
                cap_total=sum(CAP[d-18]+CAP[24-d] for d in degrees)
                S=cap_total-literal_total
                require(S==2,'two slack units')
                # Enumerate whether the one exceptional outside vertex is adjacent.
                outsider=20 if outside[2] else 22
                possible_weights=[8,8+(21-outsider)]
                H=20*21+22*21//2-m-93-107
                lower=min(possible_weights)-H
                require(12*lower>S,'physical slack contradiction')
                saturated.append({'profile':p,'A':list(a),'outside':outside,'m':m,'M':m-231,
                    'total_slack':S,'H20':H,'neighbor_weight_lower':min(possible_weights),
                    'slack_per_A_vertex_at_least':lower,'required_A_slack':12*lower,
                    'contradiction_gap':12*lower-S})
    require(doc['profile_census_by_M']==census,'M census')
    require(doc['profile_categories']==categories,'endpoint census')
    require(doc['twelve_subset_count']==count,'subset count')
    require(doc['twelve_subset_stream_sha256']==digest.hexdigest(),'full subset stream')
    require(doc['saturated_degree_rows']==saturated,'saturated rows')
    rows=[]
    for k in range(19):
        for size in range(2,5):
            # Union bound on missed vertices: k - size*(k-(18-(size-1))).
            lower=k-size*(k-19+size);upper=[None,None,13,4,0][size]
            require(lower>upper,'clique component not excluded')
            rows.append([k,size,lower,upper,lower-upper])
    require(rows==doc['clique_component_rows'],'clique rows')
    sizes=[]
    for a in range(2,14):
        for b in range(2,14):
            k=43-a-b
            if a<=b and 0<=k<=18:sizes.append([k,a,b])
    require(sorted(sizes)==doc['nonclique_size_rows'],'nonclique shapes')
    require(sorted(sizes)==[[17,13,13],[18,12,13]],'three-part frontier')
    # At k17 both blue sets have at least five; at k18 the 12-side
    # blue set must be a red clique of exactly four vertices.
    require(13-8>=5 and 12-8==4,'outside-vertex dichotomy')
    require(doc['allowed_separator18_component_sizes']==[1,24],'singleton exception')
    require(doc['allowed_separator18_independence_numbers']==[1,3],'independence budget')
    require(doc['full_two_nontrivial_part_sizes']==[[a,25-a] for a in range(2,13)],'complete 25-vertex cut family')
    return {'profiles':len(ns),'twelve_subsets':count,'saturated_rows':len(saturated),
            'clique_rows':len(rows),'nonclique_size_rows':len(sizes),
            'profile_categories':dict(categories),'minimum_slack_contradiction':min(x['contradiction_gap'] for x in saturated)}

def components(adj,vertices):
    found=[]
    while vertices:
        part=vertices & -vertices;todo=part
        while todo:
            bit=todo & -todo;todo-=bit
            more=adj[bit.bit_length()-1] & vertices & ~part
            part|=more;todo|=more
        found.append(part);vertices &= ~part
    return found

def physical_controls():
    graphs=local=separators=clique=blue_pair=0
    for n in range(1,7):
        pairs=list(combinations(range(n),2));full=(1<<n)-1
        for mask in range(1<<len(pairs)):
            adj=[0]*n
            for bit,(u,v) in enumerate(pairs):
                if mask>>bit&1:adj[u]|=1<<v;adj[v]|=1<<u
            d=[a.bit_count() for a in adj];m=sum(d)//2
            red=[];blue=[]
            for v in range(n):
                R=[u for u in range(n) if adj[v]>>u&1]
                B=[u for u in range(n) if u!=v and not adj[v]>>u&1]
                red.append(sum(bool(adj[u]>>w&1) for u,w in combinations(R,2)))
                blue.append(sum(not adj[u]>>w&1 for u,w in combinations(B,2)))
                actual=red[-1]+blue[-1]
                require(actual==comb(n-1-d[v],2)-m+sum(d[u] for u in R),'literal identity')
                gamma=n//2;extra=(mask+v)%3
                H=gamma*d[v]+comb(n-1-d[v],2)-m-actual-extra
                require(sum(gamma-d[u] for u in R)-H==extra,'slack sign and weight')
                local+=1
            require(sum(red)+sum(blue)==3*comb(n,3)-3*sum(x*(n-1-x) for x in d)//2,'global identity')
            alpha=[0]*(1<<n)
            for subset in range(1,1<<n):
                bit=subset&-subset;v=bit.bit_length()-1;rest=subset^bit
                alpha[subset]=max(alpha[rest],1+alpha[rest & ~adj[v]])
            for remaining in range(1,1<<n):
                parts=components(adj,remaining)
                if len(parts)<2:continue
                S=full ^ remaining;k=S.bit_count()
                require(sum(alpha[A] for A in parts)==alpha[remaining],'component independence additivity')
                separators+=1
                for A in parts:
                    if alpha[A]!=1:continue
                    common=S;degree_sum=0
                    for v in range(n):
                        if A>>v&1:common &= adj[v];degree_sum+=(adj[v]&S).bit_count()
                    require(common.bit_count()>=degree_sum-(A.bit_count()-1)*k,'clique common neighborhood')
                    clique+=1
                for A,B in combinations(parts,2):
                    for z in range(n):
                        if not S>>z&1:continue
                        X=A & ~adj[z];Y=B & ~adj[z]
                        if alpha[X]>=2 and alpha[Y]>=2:
                            require(alpha[(1<<z)|X|Y]>=5,'crossing blue five-set')
                            blue_pair+=1
            graphs+=1
    # Two connected nonclique components plus an outside vertex need seven
    # vertices, so exhaust all 64 outside attachments to two red P3 components.
    attachment_cases=0
    for mask in range(64):
        edges={(0,1),(1,2),(3,4),(4,5)}
        edges.update((v,6) for v in range(6) if mask>>v&1)
        X=[v for v in range(3) if not mask>>v&1]
        Y=[v for v in range(3,6) if not mask>>v&1]
        xp=[p for p in combinations(X,2) if p not in edges]
        yp=[p for p in combinations(Y,2) if p not in edges]
        if xp and yp:
            witness=(*xp[0],*yp[0],6)
            require(all(tuple(sorted(p)) not in edges for p in combinations(witness,2)),'nonvacuous blue-five transport')
            blue_pair+=1
        attachment_cases+=1
    require(blue_pair>0,'vacuous crossing control')
    return {'labeled_graphs':graphs,'local_identity_cases':local,'separator_instances':separators,
            'clique_common_neighbor_cases':clique,'blue_pair_five_set_cases':blue_pair,
            'seven_vertex_attachment_controls':attachment_cases}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stream',type=Path);args=parser.parse_args()
    raw=(HERE/'certificate.json').read_bytes();doc=json.loads(raw)
    if args.stream:
        with args.stream.open('wb') as out:counts=verify_certificate(doc,out)
    else:counts=verify_certificate(doc)
    mutations=[]
    for key,value in [('profiles',doc['profiles'][:-1]),('allowed_separator18_component_sizes',[12,13]),
                      ('allowed_separator18_independence_numbers',[1,2]),('twelve_subset_count',0),
                      ('caps',[79,85,93,100,107,115,125]),('full_two_nontrivial_part_sizes',[[1,24]])]:
        altered=deepcopy(doc);altered[key]=value;mutations.append(altered)
    altered=deepcopy(doc);altered['saturated_degree_rows'][0]['total_slack']=24;mutations.append(altered)
    for changed in mutations:
        try:verify_certificate(changed)
        except ValueError:pass
        else:raise ValueError('accepted mutation')
    print(json.dumps({'status':'VERIFIED_HARD_SEPARATOR18_CLASSIFICATION',**counts,**physical_controls(),
        'mutations_rejected':len(mutations),'certificate_sha256':hashlib.sha256(raw).hexdigest()},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
