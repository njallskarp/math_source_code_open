#!/usr/bin/env python3
"""Literal uniform-star bounds and complete marked-cell edge transport."""
from itertools import combinations
from math import comb
import json
from build import roots

def need(ok,why):
    if not ok:raise ValueError(why)

def star_bound(a,A,z,y):
    n,k=len(a),len(A)
    if not A:return
    red_stars=int(z in a[A[0]])+int(y in a[A[0]])
    need(all(len(a[v])==(n-1)//2 for v in A),"unbalanced")
    need(all((z in a[v])==(z in a[A[0]]) and (y in a[v])==(y in a[A[0]])for v in A),"nonuniform")
    rows=[[0 if w==v else 1 if w in a[v]else -1 for w in range(n)]for v in A]
    sums=[sum(row[w]for row in rows)for w in range(n)]
    norm=sum(s*s for w,s in enumerate(sums)if w not in (z,y))
    p=k if k%2==0 else n-k-2
    need(norm>=p,"parity")
    if red_stars!=1:need(norm>=4*k-p,"balance correction")
    q=0
    for u,v in combinations(A,2):
        color=v in a[u]
        q+=sum(w not in (u,v) and (w in a[u])==color and (w in a[v])==color for w in range(n))
    need(8*q==(n-2)*k*k-(2*n-5)*k+norm,"signed identity")
    counts=[sum(v in a[w]for v in A)for w in range(n)]
    e=sum(v in a[u]for u,v in combinations(A,2))
    need(q==sum(comb(t,2)for t in counts)-comb(k,2)+e,"incidence identity")

def small_graphs():
    graphs=tests=0
    for n in (3,5):
        edges=list(combinations(range(n),2))
        for code in range(1<<len(edges)):
            a=[set()for _ in range(n)]
            for bit,(u,v)in enumerate(edges):
                if code>>bit&1:a[u].add(v);a[v].add(u)
            for z,y in combinations(range(n),2):
                groups={}
                for v in range(n):
                    if v not in (z,y)and len(a[v])==(n-1)//2:
                        groups.setdefault((z in a[v],y in a[v]),[]).append(v)
                for group in groups.values():
                    for mask in range(1,1<<len(group)):
                        A=[v for bit,v in enumerate(group)if mask>>bit&1]
                        star_bound(a,A,z,y);tests+=1
            graphs+=1
    return graphs,tests

def transport():
    cases=bad_inputs=0
    for case,color,c,eta,a,wcell in roots():
        sizes=[c,20-c,20-c,c+1]
        quota=5 if color else 4
        Ecounts=[a,quota-a,quota-a,9-2*quota+a]
        zcell=3 if color else 0;ycell=0 if eta==color else 3
        cells=[];nextlabel=2
        for size in sizes:
            cells.append(list(range(nextlabel,nextlabel+size)));nextlabel+=size
        E=set(v for j,cell in enumerate(cells)for v in cell[:Ecounts[j]])
        y=cells[ycell][0]
        z=cells[zcell][Ecounts[zcell]]
        need(y in E and z not in E,"distinguished marks")
        w=None
        if case>=2:
            w=next(v for v in cells[wcell]if v not in E and v!=z)
        adj=[set()for _ in range(43)]
        for u,v in combinations(range(43),2):
            if u<2:
                if v==1:red=bool(color)
                else:
                    j=next(j for j,cell in enumerate(cells)if v in cell)
                    in_color=j in ((0,1)if u==0 else (0,2))
                    red=bool(color)if in_color else not color
            else:
                red=((u*71+v*113+case*17+c*5+a)%11)<5
            if red:adj[u].add(v);adj[v].add(u)
        need(len(adj[0])==len(adj[1])==21,"anchor degrees")
        need(len(adj[0]&E)==len(adj[1]&E)==5,"exceptional incidence")
        need(z not in adj[0]and z not in adj[1],"z star")
        need((y in adj[0])==bool(eta)==(y in adj[1]),"y star agreement")
        if w is not None:need(w in cells[wcell]and w not in E|{z,0,1},"central defect transport")
        free=[(u,v)for u,v in combinations(range(43),2)if u>=2]
        need(len(free)==820,"omitted physical shared edge")
        perm=[(17*v+9)%43 for v in range(43)]
        transported=[set()for _ in range(43)]
        for u,v in combinations(range(43),2):
            if v in adj[u]:transported[perm[u]].add(perm[v]);transported[perm[v]].add(perm[u])
        need(all((v in adj[u])==(perm[v]in transported[perm[u]])for u,v in combinations(range(43),2)),"physical lift")
        need(len(transported[perm[0]]&{perm[v]for v in E})==5,"marked lift")
        altered=set(adj[0]);altered.symmetric_difference_update({y})
        need((y in altered)!=(y in adj[1]),"damaged y-star control");bad_inputs+=1
        cases+=1
    return cases,bad_inputs

if __name__=="__main__":
    graphs,tests=small_graphs()
    transports,damaged=transport()
    print(json.dumps({"small_graphs":graphs,"literal_uniform_star_subsets":tests,
                      "marked_root_transports":transports,"physical_pair_transports":903*transports,
                      "damaged_y_star_controls":damaged},sort_keys=True,indent=2))
