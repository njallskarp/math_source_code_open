"""Independent adjacency, clique-recursion, distances and disjoint-path audit."""
from collections import deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def check(ok,message):
    if not ok: raise ValueError(message)


def mask_graph(rows):
    n=len(rows)
    for v,row in enumerate(rows):
        check(row==sorted(set(row)) and all(type(x) is int and 0<=x<n and x!=v for x in row),'adjacency domain')
        check(all(v in rows[x] for x in row),'symmetry')
    return [sum(1<<x for x in row) for row in rows]


def clique_count(adj,size,mask=None):
    if mask is None: mask=(1<<len(adj))-1
    if size==0:return 1
    if mask.bit_count()<size:return 0
    count=0
    while mask:
        b=mask&-mask;mask^=b
        count+=clique_count(adj,size-1,mask&adj[b.bit_length()-1])
    return count


def complement(adj):
    return [((1<<len(adj))-1)^mask^(1<<v) for v,mask in enumerate(adj)]


def certify_paths(rows,u,v,count=7):
    n=len(rows);m=2*n;s=2*u+1;t=2*v
    cap=[[0]*m for _ in range(m)]
    for x in range(n):
        cap[2*x][2*x+1]=n if x in (u,v) else 1
        for y in rows[x]:cap[2*x+1][2*y]=n
    residual=[r[:] for r in cap]
    def path_in(matrix):
        parents=[-1]*m;parents[s]=s;Q=deque([s])
        while Q and parents[t]<0:
            x=Q.popleft()
            for y,c in enumerate(matrix[x]):
                if c>0 and parents[y]<0:parents[y]=x;Q.append(y)
        check(parents[t]>=0,'seven-flow exists')
        p=[t]
        while p[-1]!=s:p.append(parents[p[-1]])
        return p[::-1]
    for _ in range(count):
        p=path_in(residual)
        for x,y in zip(p,p[1:]):residual[x][y]-=1;residual[y][x]+=1
    flow=[[max(0,cap[x][y]-residual[x][y]) for y in range(m)] for x in range(m)]
    # Decode and check the paths directly; no solver or flow theorem is trusted.
    used=set();paths=[]
    for _ in range(count):
        split=path_in(flow)
        for x,y in zip(split,split[1:]):flow[x][y]-=1
        p=[u]+[x//2 for x in split[1:] if x%2==0]
        check(p[-1]==v and len(p)==len(set(p)) and all(y in rows[x] for x,y in zip(p,p[1:])),'literal path')
        check(not used&set(p[1:-1]),'internally disjoint paths')
        used.update(p[1:-1]);paths.append(p)
    return paths


def main():
    w=json.loads((Path(__file__).resolve().parent/'WITNESS.json').read_text())
    rows=w['core_adjacency'];check(len(rows)==22,'core order');A=mask_graph(rows)
    E={(u,v) for u in range(22) for v in rows[u] if u<v}
    check(len(E)==108 and clique_count(A,4)==clique_count(complement(A),5)==0,'core Ramsey')
    distances=[[0 if u==v else 1 if v in rows[u] else 100 for v in range(22)] for u in range(22)]
    for k in range(22):
        for u in range(22):
            for v in range(22):distances[u][v]=min(distances[u][v],distances[u][k]+distances[k][v])
    check(max(map(max,distances))==3 and [(u,v) for u,v in combinations(range(22),2) if distances[u][v]>2]==[(4,5)],'all-pairs distances')
    path_total=0
    for u,v in combinations(range(22),2):
        if v not in rows[u]:path_total+=len(certify_paths(rows,u,v))
    check(path_total==861,'all 123 nonadjacent pairs')
    cut=set(w['seven_cut']);check(cut==set(rows[4]) and len(cut)==7 and 5 not in cut,'isolating seven-cut')
    plus=[r[:] for r in rows];plus[4]=sorted(plus[4]+[5]);plus[5]=sorted(plus[5]+[4])
    P=mask_graph(plus);check(clique_count(P,4)==clique_count(complement(P),5)==0,'locally safe addition')
    whole=[r[:] for r in rows]+[list(range(22)),[],[],[]]
    for v in range(22):whole[v].append(22)
    for x,signature in enumerate(w['outside_signatures'],23):
        check(signature==sorted(set(signature)) and all(type(v) is int and 0<=v<22 for v in signature),'outside domain')
        whole[x]=signature+[y for y in range(23,26) if y!=x]
        for v in signature:whole[v].append(x)
    B=mask_graph(whole)
    check(clique_count(B,5)==clique_count(complement(B),5)==0,'full Ramsey graph')
    BF=B[:];BF[4]|=1<<5;BF[5]|=1<<4
    check(clique_count(BF,5)==1 and clique_count(complement(BF),5)==0,'unique post-addition red K5')
    check(all(clique_count(BF,5,((1<<26)-1)^(1<<x))==0 for x in range(23,26)),'minimal outside obstruction')
    F={(u,v) for u in range(26) for v in whole[u] if u<v}
    def digest(edges):return sha256((json.dumps(sorted(edges),separators=(',',':'))+'\n').encode()).hexdigest()
    print(json.dumps({'core_edge_sha256':digest(E),'extension_edge_sha256':digest(F),'core_connectivity':7,'core_diameter':3,
                      'nonadjacent_pairs_certified':123,'internally_disjoint_paths_checked':path_total,'red_edges':len(F),
                      'post_addition_red_K5':1,'outside_deletion_controls':3},sort_keys=True))


if __name__=='__main__':main()
