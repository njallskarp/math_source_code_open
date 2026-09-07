"""Independent complete local classification and orbit audit; no producer import."""
from itertools import combinations,permutations
from hashlib import sha256
import json
from pathlib import Path
import sys

def require(ok,message):
    if not ok:raise ValueError(message)

def paley():
    squares={x*x%17 for x in range(1,17)}
    return [[(u-v)%17 in squares for v in range(17)] for u in range(17)]

def s_edges(kind):
    E={(0,2),(0,3),(0,4),(1,2),(1,3)}
    require(kind in (62,126),'unknown S type')
    if kind==126:E.add((1,4))
    return E

def automorphisms(P):
    N=[v for v in range(17) if P[0][v]]
    B=[v for v in range(1,17) if v not in N]
    signatures={frozenset(v for v in N if P[b][v]):b for b in B}
    require(len(signatures)==8,'outside signatures distinct')
    local=0;lifts=[]
    for q in permutations(range(8)):
        if not all(P[N[i]][N[j]]==P[N[q[i]]][N[q[j]]] for i,j in combinations(range(8),2)):continue
        local+=1;g=[0]*17
        for i,v in enumerate(N):g[v]=N[q[i]]
        for b in B:
            signature=frozenset(g[v] for v in N if P[b][v])
            if signature not in signatures:break
            g[b]=signatures[signature]
        else:
            if sorted(g)==list(range(17)) and all(P[u][v]==P[g[u]][g[v]] for u,v in combinations(range(17),2)):
                lifts.append(tuple(g))
    squares={x*x%17 for x in range(1,17)}
    require(set(lifts)=={tuple(a*v%17 for v in range(17)) for a in squares},'complete stabilizer')
    actions=sorted({tuple((v+b)%17 for v in g) for g in lifts for b in range(17)})
    require(local==16 and len(lifts)==8 and len(actions)==136,'Paley automorphism proof')
    return actions

def has_clique(matrix,k):
    def visit(candidates,left):
        if left==0:return True
        for i,v in enumerate(candidates):
            if len(candidates)-i<left:break
            if visit([w for w in candidates[i+1:] if matrix[v][w]],left-1):return True
        return False
    return visit(list(range(len(matrix))),k)

def physical_graph(kind,row,P):
    require(len(row)==5 and all(type(m) is int and 0<=m<1<<17 for m in row),'column encoding')
    A=[[False]*23 for _ in range(23)]
    for u,v in combinations(range(17),2):A[u][v]=A[v][u]=P[u][v]
    for u,v in s_edges(kind):A[u+17][v+17]=A[v+17][u+17]=True
    for s,m in enumerate(row):
        A[s+17][22]=A[22][s+17]=True
        for v in range(17):A[v][s+17]=A[s+17][v]=bool(m>>v&1)
    return A

def graph6(record):
    require(type(record) is str and record and all(63<=ord(c)<=126 for c in record),'graph6 characters')
    n=ord(record[0])-63;bits=n*(n-1)//2
    require(n<63 and len(record)==1+(bits+5)//6,'graph6 length')
    value=0
    for c in record[1:]:value=(value<<6)|(ord(c)-63)
    padding=6*(len(record)-1)-bits
    require(not value&((1<<padding)-1),'graph6 padding')
    value>>=padding;E=set();position=bits-1
    for v in range(n):
        for u in range(v):
            if value>>position&1:E.add((u,v))
            position-=1
    return n,E

def orbit(row,actions,sp):
    maps={m:[sum(1<<g[v] for v in range(17) if m>>v&1) for g in actions] for m in row}
    return {tuple(maps[row[p[s]]][i] for s in range(5)) for p in sp for i in range(len(actions))}

def check_certificate(certificate,tuple_path):
    require(certificate['type']==62 and certificate['cross_edges']==36,'density/type')
    require(certificate['paley_order']==17 and certificate['column_domain']==7225
            and certificate['minimum_column_size']==4 and certificate['maximum_column_size']==8,'domain metadata')
    require(len(certificate['family']['representatives'])==1697,'complete class count')
    P=paley();actions=automorphisms(P);E=s_edges(62)
    sp=[p for p in permutations(range(5)) if all(((u,v) in E)==(tuple(sorted((p[u],p[v]))) in E) for u,v in combinations(range(5),2))]
    require(len(sp)==2,'complete type62 action')
    f=certificate['family'];require(f['type']==62 and f['edges']==114,'family metadata')
    expanded=set();previous=None;sizes={};profiles={}
    for entry in f['representatives']:
        row=tuple(entry['columns']);require(len(row)==5 and all(type(m) is int and 0<=m<(1<<17) for m in row),'column shape')
        require(sum(m.bit_count() for m in row)==36,'exact sum')
        require(previous is None or previous<row,'ordered canonical representatives');previous=row
        A=physical_graph(62,row,P);degrees=list(map(sum,A))
        require([v for v,d in enumerate(degrees) if d==5]==[22],'unique hub')
        require(sum(degrees)==228,'physical density114')
        require(not has_clique(A,4),'red four in representative')
        require(not has_clique([[u!=v and not A[u][v] for v in range(23)] for u in range(23)],5),'blue five in representative')
        copies=orbit(row,actions,sp)
        require(min(copies)==row and len(copies)==entry['orbit_size'],'canonical orbit and stabilizer')
        require(not expanded&copies,'orbit overlap');expanded|=copies
        sizes[len(copies)]=sizes.get(len(copies),0)+1
        profile=','.join(map(str,sorted(m.bit_count() for m in row)))
        profiles[profile]=profiles.get(profile,0)+1
    raw=''.join(' '.join(map(str,row))+'\n' for row in sorted(expanded)).encode()
    require(len(expanded)==f['labeled_count'] and sha256(raw).hexdigest()==f['full_tuple_sha256'],'complete orbit identity')
    require(Path(tuple_path).read_bytes()==raw,'full independent labeled enumeration differs')
    return {'status':'VERIFIED_COMPLETE_TYPE62_DENSITY114_CLASSIFICATION',
            'classes':len(f['representatives']),'labeled_tuples':len(expanded),
            'orbit_sizes':sizes,'column_size_profiles':profiles,
            'all_unique_hub':True,'all_rigid':set(sizes)=={272},
            'paley_automorphisms':len(actions),'s_automorphisms':len(sp),
            'full_tuple_sha256':sha256(raw).hexdigest()}

if __name__=='__main__':
    require(len(sys.argv)==3,'certificate and independent complete tuple file required')
    print(json.dumps(check_certificate(json.loads(Path(sys.argv[1]).read_text()),sys.argv[2]),indent=2,sort_keys=True))
