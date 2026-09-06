#!/usr/bin/env python3
"""Independent degree-moment reconstruction and literal sharpness checks.

Imports no producer, solver, parent package, or external data.
"""
from collections import Counter
from itertools import combinations,product
from math import comb
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)

def binomial_min(total,length):
    a,b=divmod(total,length)
    return (length-b)*comb(a,2)+b*comb(a+1,2)

def independent_bound(k,red_stars):
    if k==0:return 0
    options=[]
    for internal_edges in range(comb(k,2)+1):
        crossing=(21-red_stars)*k-2*internal_edges
        if not 0<=crossing<=k*(41-k):continue
        options.append(binomial_min(2*internal_edges,k)+binomial_min(crossing,41-k)
                       +(red_stars-1)*comb(k,2)+internal_edges)
    return min(options)

def bound_rows():
    out=[]
    for k in range(22):
        for same in (0,1):
            v=independent_bound(k,0 if same else 1)
            if same:need(v==independent_bound(k,2),"global color reversal")
            high=max(0,(v-9*comb(k,2)+3)//4)
            out.append([k,same,v,high])
    return out

def direct_roots():
    answer=[]
    # Enumerate all weak compositions of nine exceptional vertices,
    # independently of the producer's common-cell parameterization.
    compositions=[(a,b,c,9-a-b-c) for a in range(10)
                  for b in range(10-a)for c in range(10-a-b)]
    for case in range(4):
        for color in range(2):
            for size in range(10,14):
                sizes=[size,20-size,20-size,size+1]
                for eta in range(2):
                    for e in compositions:
                        red_to_first=e[0]+e[1] if color else e[2]+e[3]
                        red_to_second=e[0]+e[2] if color else e[1]+e[3]
                        if (red_to_first,red_to_second)!=(5,5):continue
                        zcell=0 if color==0 else 3
                        ycell=0 if eta==color else 3
                        if e[ycell]==0:continue
                        central=[sizes[j]-e[j]-(j==zcell)for j in range(4)]
                        if min(central)<0:continue
                        for wcell in range(-1,4):
                            if (case<2)!=(wcell==-1):continue
                            if wcell>=0 and central[wcell]<1:continue
                            answer.append([case,color,size,eta,e[0],wcell])
    return sorted(answer)

def expected():
    bounds=bound_rows()
    h={(k,s):high for k,s,_,high in bounds}
    mult=[[n,min(h[k,1]+h[n-k,0]for k in range(n+1)),(n-15)//2]for n in (19,20,21)]
    return {"schema":1,"bounds":bounds,"multiplicities":mult,"roots":direct_roots()}

def validate(data):
    need(data==expected(),"certificate mismatch")

def sharp_graph():
    data=json.loads((HERE/"sharpness.json").read_text())
    a=[set()for _ in range(43)]
    for u in range(8):
        for d in (1,2,6,7):a[u].add((u+d)%8)
    nxt=10
    for mask,count in data["external_signatures"]:
        need(0<=mask<256 and count>0,"signature input")
        for _ in range(count):
            for u in range(8):
                if mask>>u&1:a[u].add(nxt);a[nxt].add(u)
            nxt+=1
    need(nxt==43,"graph order")
    need(all(len(a[u])==21 for u in range(8)),"balanced degrees")
    need(all(8 not in a[u] and 9 not in a[u]for u in range(8)),"two shared blue stars")
    degrees=[]
    for u,v in combinations(range(8),2):
        color=v in a[u]
        q=sum(w!=u and w!=v and (w in a[u])==color and (w in a[v])==color for w in range(43))
        degrees.append(q)
    need(max(degrees)==9 and sum(degrees)==250,"sharpness codegrees")
    need(sum(degrees)==independent_bound(8,0),"sharpness equality")
    # The outside 35 vertices are all independent. This is a degree-only
    # sharpness graph, not a Ramsey/profile-B witness.
    need(all(v not in a[u]for u,v in combinations(range(8,13),2)),"scope control")
    return dict(sorted(Counter(degrees).items()))

def scalar_separator():
    # Ten scalar same-edge-color codegrees: 9 except q_01=10.
    # G has diagonal42 and offdiagonal 4q-39; H=G-J pins one blue star.
    n=10
    q={(u,v):10 if (u,v)==(0,1)else 9 for u,v in combinations(range(n),2)}
    G=[[42 if u==v else 4*q[tuple(sorted((u,v)))]-39 for v in range(n)]for u in range(n)]
    H=[[entry-1 for entry in row]for row in G]
    margins=[H[u][u]-sum(abs(H[u][v])for v in range(n)if u!=v)for u in range(n)]
    need(min(margins)==5,"strict diagonal dominance certificate")
    # Symmetric strict diagonal dominance with positive diagonal implies
    # H positive definite; hence G is positive definite as well.
    value=sum(q.values())
    need(value==406 and value>=400,"old one-star scalar lower bound")
    negative=sum(sum(row)for row in H)-n*n
    need(negative==-42,"second common-star Gram obstruction")
    need(independent_bound(10,1)==413 and independent_bound(10,0)==415,"new exact bounds")
    return {"pair_sum":value,"one_star_psd_margin":min(margins),
            "two_star_residual_quadratic_value":negative,
            "opposite_star_bound":413,"same_star_bound":415}

if __name__=="__main__":
    data=json.loads((HERE/"certificate.json").read_text());validate(data)
    rejected=0
    for kind in range(3):
        x=json.loads(json.dumps(data))
        if kind==0:x["roots"].pop()
        elif kind==1:x["bounds"][21][2]-=1
        else:x["roots"][0][3]=1-x["roots"][0][3]
        try:validate(x)
        except ValueError:rejected+=1
    need(rejected==3,"damaged certificate accepted")
    print(json.dumps({"bound_rows_matched":len(data["bounds"]),"roots_matched":len(data["roots"]),
                      "sharpness_codegree_histogram":sharp_graph(),"scalar_separator":scalar_separator(),
                      "mutations_rejected":rejected,
                      "certificate_sha256":hashlib.sha256((HERE/"certificate.json").read_bytes()).hexdigest()},
                     sort_keys=True,indent=2))
