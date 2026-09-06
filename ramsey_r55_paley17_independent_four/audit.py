"""Independent growing-subset, Boolean-matrix and common-edge audit.

Imports no producer code. Rebuilds all 459 columns and all 13,617 pairs,
compares the complete column certificate, and checks every compatibility
edge's common neighborhood for edges (each K4 would be counted six times).
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations,permutations
import json
from pathlib import Path


def decode(record):
    if type(record) is not str or not record or any(not 63<=ord(c)<=126 for c in record):
        raise ValueError('graph6 alphabet')
    n=ord(record[0])-63;payload=record[1:]
    if n>=63 or len(payload)!=(n*(n-1)//2+5)//6:raise ValueError('graph6 size')
    value=0
    for c in payload:value=64*value+ord(c)-63
    width=6*len(payload);padding=width-n*(n-1)//2
    if value & ((1<<padding)-1):raise ValueError('graph6 unused bits')
    matrix=[[False]*n for _ in range(n)];k=0
    for v in range(n):
        for u in range(v):
            matrix[u][v]=matrix[v][u]=bool(value>>(width-1-k)&1);k+=1
    return matrix


def has_clique(matrix,vertices,size,color=True):
    if size==0:return True
    for i,v in enumerate(vertices):
        tail=vertices[i+1:]
        if len(tail)<size-1:break
        if has_clique(matrix,[u for u in tail if matrix[v][u]==color],size-1,color):return True
    return False


def domains(matrix):
    n=len(matrix);subsets=[]
    def grow(chosen,start):
        subsets.append(tuple(chosen))
        for v in range(start,n):
            neighbors=[u for u in chosen if matrix[v][u]]
            if not any(matrix[u][w] for u,w in combinations(neighbors,2)):
                grow(chosen+[v],v+1)
    grow([],0)
    maximal=[]
    for chosen in subsets:
        for v in range(n):
            if v in chosen:continue
            neighbors=[u for u in chosen if matrix[v][u]]
            if not any(matrix[u][w] for u,w in combinations(neighbors,2)):break
        else:maximal.append(sum(1<<v for v in chosen))
    return len(subsets),sorted(maximal)


def pair_graph(matrix,columns):
    n=len(matrix);missing=[frozenset(v for v in range(n) if not mask>>v&1) for mask in columns]
    def compatible(i,j):
        common=sorted(missing[i]&missing[j])
        for a,b,c in combinations(common,3):
            if not (matrix[a][b] or matrix[a][c] or matrix[b][c]):return False
        return True
    loops=[i for i in range(len(columns)) if compatible(i,i)]
    edges=[(i,j) for i in range(len(columns)) for j in range(i+1,len(columns)) if compatible(i,j)]
    return loops,edges


def graph_counts(size,edges):
    neighbors=[set() for _ in range(size)]
    for u,v in edges:neighbors[u].add(v);neighbors[v].add(u)
    triple_incidence=quad_incidence=0
    for u,v in edges:
        common=neighbors[u]&neighbors[v];triple_incidence+=len(common)
        quad_incidence+=sum(b in neighbors[a] for a,b in combinations(sorted(common),2))
    if triple_incidence%3 or quad_incidence%6:raise ValueError('clique incidence divisibility')
    return [1,size,len(edges),triple_incidence//3,quad_incidence//6]


def consumer(inputs):
    refs=inputs['interfaces']
    if len(refs)!=13 or len(set(refs))!=13:raise ValueError('interface records')
    patterns={15:{(0,1),(0,2),(0,3),(0,4)},62:{(0,2),(0,3),(0,4),(1,2),(1,3)},
              126:{(0,2),(0,3),(0,4),(1,2),(1,3),(1,4)}}
    labels=[]
    for record in refs:
        matrix=decode(record);n=len(matrix)
        if n!=22 or sum(sum(row) for row in matrix)!=218:raise ValueError('interface size')
        if has_clique(matrix,list(range(n)),4) or has_clique(matrix,list(range(n)),5,False):raise ValueError('interface forbidden clique')
        hubs=[v for v,row in enumerate(matrix) if sum(row)==5]
        if len(hubs)!=1:raise ValueError('hub uniqueness')
        S=[v for v in range(n) if matrix[hubs[0]][v]]
        types=[]
        for kind,pattern in patterns.items():
            if any(all(matrix[S[p[u]]][S[p[v]]]==((u,v) in pattern)
                       for u,v in combinations(range(5),2)) for p in permutations(range(5))):types.append(kind)
        if len(types)!=1:raise ValueError('hub induced isomorphism type')
        labels.append(types[0])
    cat=inputs['r44_17'];matrix=decode(cat['record']);p=cat['catalogue_to_paley']
    if len(matrix)!=17 or sorted(p)!=list(range(17)):raise ValueError('primary record map')
    if sha256((cat['record']+'\n').encode()).hexdigest()!=cat['raw_sha256']:raise ValueError('primary record identity')
    squares={k*k%17 for k in range(1,17)}
    if any(matrix[u][v]!=((p[u]-p[v])%17 in squares) for u in range(17) for v in range(17)):
        raise ValueError('primary Paley map')
    survivors=[]
    if sorted(row['type'] for row in inputs['local_survivors'])!=[62,126]:raise ValueError('surviving cases')
    for row in inputs['local_survivors']:
        cols=row['columns']
        if len(cols)!=5:raise ValueError('survivor column count')
        for col in cols:
            if col!=sorted(set(col)) or any(type(a) is not int or not 0<=a<17 for a in col):raise ValueError('survivor column encoding')
        m=[[False]*23 for _ in range(23)]
        for u in range(17):
            for v in range(17):m[u][v]=(u-v)%17 in squares
        for u,v in patterns[row['type']]:m[u+17][v+17]=m[v+17][u+17]=True
        for i,col in enumerate(cols):
            m[17+i][22]=m[22][17+i]=True
            for a in col:m[a][17+i]=m[17+i][a]=True
        if has_clique(m,list(range(23)),4) or has_clique(m,list(range(23)),5,False):raise ValueError('invalid local survivor')
        edgecount=sum(sum(r) for r in m)//2
        if edgecount!=row['red_edges']:raise ValueError('local survivor count')
        survivors.append({'type':row['type'],'red_edges':edgecount})
    return {'interface_types':labels,'excluded_degree23_indices':[i for i,t in enumerate(labels) if t==15],
            'retained_degree23_indices':[i for i,t in enumerate(labels) if t!=15],
            'global_hub_upper_bounds':[22 if t==15 else 23 for t in labels],
            'local_degree23_survivors':survivors}


def calculate(inputs,certificate):
    squares={x*x%17 for x in range(1,17)}
    matrix=[[(u-v)%17 in squares for v in range(17)] for u in range(17)]
    if has_clique(matrix,list(range(17)),4) or has_clique(matrix,list(range(17)),4,False):raise ValueError('Paley core')
    count,columns=domains(matrix);loops,edges=pair_graph(matrix,columns);counts=graph_counts(len(columns),edges)
    if loops or counts[4]:raise ValueError('local obstruction failed')
    encoded=''.join(f'{i} {j}\n' for i,j in edges).encode()
    rebuilt={'maximal_columns':columns,'compatibility_clique_counts':counts,
             'compatible_self_pairs':loops,'pair_graph_sha256':sha256(encoded).hexdigest()}
    if certificate!=rebuilt:raise ValueError('complete certificate mismatch')
    if any(type(x) is not int for x in certificate['maximal_columns']):raise ValueError('column mask type')
    certbytes=(json.dumps(rebuilt,indent=2,sort_keys=True)+'\n').encode()
    result={'status':'VERIFIED_PALEY17_INDEPENDENT_FOUR_OBSTRUCTION',
        'trianglefree_subsets':count,'maximal_columns':len(columns),
        'column_size_histogram':dict(sorted(Counter(x.bit_count() for x in columns).items())),
        'compatibility_clique_counts':counts,'compatible_self_pairs':len(loops),
        'pair_graph_sha256':sha256(encoded).hexdigest(),'certificate_sha256':sha256(certbytes).hexdigest(),
        'consumer':consumer(inputs)}
    return result,rebuilt,edges


if __name__=='__main__':
    directory=Path(__file__).parent
    result,_,_=calculate(json.loads((directory/'inputs.json').read_text()),json.loads((directory/'certificate.json').read_text()))
    print(json.dumps(result,indent=2,sort_keys=True))
