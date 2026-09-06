"""Exhaustive mask-domain proof and literal interface consumer (stdlib)."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


def need(ok,message):
    if not ok:raise ValueError(message)


def graph6(record):
    need(type(record) is str and record and all(63<=ord(c)<=126 for c in record),'graph6 characters')
    n=ord(record[0])-63
    need(n<63 and len(record)==1+(n*(n-1)//2+5)//6,'graph6 length')
    bits=''.join(f'{ord(c)-63:06b}' for c in record[1:])
    need(not any(c=='1' for c in bits[n*(n-1)//2:]),'graph6 padding')
    red=set();k=0
    for v in range(n):
        for u in range(v):
            if bits[k]=='1':red.add((u,v))
            k+=1
    return n,red


def forbidden(red,n,k,color):
    return any(all((e in red)==color for e in combinations(q,2)) for q in combinations(range(n),k))


def domains(rows):
    n=len(rows);U=(1<<n)-1
    triangles=[sum(1<<v for v in q) for q in combinations(range(n),3)
               if all(rows[u]>>v&1 for u,v in combinations(q,2))]
    tf={m for m in range(U+1) if not any(m&t==t for t in triangles)}
    maximal=sorted(m for m in tf if all(m>>v&1 or m|1<<v not in tf for v in range(n)))
    return len(tf),maximal


def pair_graph(rows,columns):
    n=len(rows);U=(1<<n)-1
    blue=[U ^ (1<<v) ^ rows[v] for v in range(n)]
    triples=[sum(1<<v for v in q) for q in combinations(range(n),3)
             if all(blue[u]>>v&1 for u,v in combinations(q,2))]
    blue_tf={m for m in range(U+1) if not any(m&t==t for t in triples)}
    omissions=[U^x for x in columns]
    loops=[i for i,m in enumerate(omissions) if m in blue_tf]
    edges=[(i,j) for i in range(len(columns)) for j in range(i+1,len(columns))
           if omissions[i]&omissions[j] in blue_tf]
    return loops,edges


def graph_counts(size,edges):
    adj=[0]*size
    for i,j in edges:adj[i]|=1<<j;adj[j]|=1<<i
    tri=quad=0
    for i,j in edges:
        candidates=adj[i]&adj[j]&~((1<<(j+1))-1)
        while candidates:
            bit=candidates & -candidates;candidates^=bit;k=bit.bit_length()-1
            tri+=1
            quad+=(adj[i]&adj[j]&adj[k]&~((1<<(k+1))-1)).bit_count()
    return [1,size,len(edges),tri,quad]


def consumer(inputs):
    interfaces=inputs['interfaces'];need(len(interfaces)==13 and len(set(interfaces))==13,'thirteen distinct records')
    labels=[]
    for record in interfaces:
        n,red=graph6(record)
        need(n==22 and len(red)==109,'dense interface size')
        need(not forbidden(red,n,4,True) and not forbidden(red,n,5,False),'interface Ramsey property')
        deg=[sum(v in e for e in red) for v in range(n)]
        hubs=[v for v in range(n) if deg[v]==5];need(len(hubs)==1,'unique degree-five hub')
        z=hubs[0];S=[v for v in range(n) if tuple(sorted((v,z))) in red]
        profile=sorted(sum(tuple(sorted((u,v))) in red for v in S if v!=u) for u in S)
        kinds={(1,1,1,1,4):15,(1,2,2,2,3):62,(2,2,2,3,3):126}
        need(tuple(profile) in kinds,'unexpected hub type');labels.append(kinds[tuple(profile)])
    cat=inputs['r44_17'];n,red=graph6(cat['record']);perm=cat['catalogue_to_paley']
    need(n==17 and sorted(perm)==list(range(17)),'catalogue identification')
    need(sha256((cat['record']+'\n').encode()).hexdigest()==cat['raw_sha256'],'primary raw identity')
    residues={1,2,4,8,9,13,15,16}
    need(all(((u,v) in red)==((perm[v]-perm[u])%17 in residues) for u,v in combinations(range(17),2)),'Paley transport')
    types={62:[(0,2),(0,3),(0,4),(1,2),(1,3)],126:[(0,2),(0,3),(0,4),(1,2),(1,3),(1,4)]}
    survivors=[]
    need(sorted(row['type'] for row in inputs['local_survivors'])==[62,126],'two surviving local types')
    for row in inputs['local_survivors']:
        columns=row['columns'];need(len(columns)==5,'five survivor columns')
        for col in columns:need(col==sorted(set(col)) and all(type(v) is int and 0<=v<17 for v in col),'survivor column')
        red={e for e in combinations(range(17),2) if (e[1]-e[0])%17 in residues}
        red.update((u+17,v+17) for u,v in types[row['type']]);red.update((v,22) for v in range(17,22))
        red.update((a,17+i) for i,col in enumerate(columns) for a in col)
        need(len(red)==row['red_edges'],'survivor edges')
        need(not forbidden(red,23,4,True) and not forbidden(red,23,5,False),'survivor Ramsey property')
        survivors.append({'type':row['type'],'red_edges':len(red)})
    return {'interface_types':labels,'excluded_degree23_indices':[i for i,t in enumerate(labels) if t==15],
            'retained_degree23_indices':[i for i,t in enumerate(labels) if t!=15],
            'global_hub_upper_bounds':[22 if t==15 else 23 for t in labels],
            'local_degree23_survivors':survivors}


def calculate(inputs):
    rows=[sum(1<<v for v in range(17) if (v-u)%17 in {1,2,4,8,9,13,15,16}) for u in range(17)]
    red={(u,v) for u,v in combinations(range(17),2) if rows[u]>>v&1}
    need(not forbidden(red,17,4,True) and not forbidden(red,17,4,False),'Paley Ramsey property')
    count,columns=domains(rows);loops,edges=pair_graph(rows,columns)
    counts=graph_counts(len(columns),edges)
    need(not loops and counts[4]==0,'independent-four obstruction failed')
    encoded=''.join(f'{i} {j}\n' for i,j in edges).encode()
    certificate={'maximal_columns':columns,'compatibility_clique_counts':counts,
                 'compatible_self_pairs':loops,'pair_graph_sha256':sha256(encoded).hexdigest()}
    certbytes=(json.dumps(certificate,indent=2,sort_keys=True)+'\n').encode()
    result={'status':'VERIFIED_PALEY17_INDEPENDENT_FOUR_OBSTRUCTION',
        'trianglefree_subsets':count,'maximal_columns':len(columns),
        'column_size_histogram':dict(sorted(Counter(x.bit_count() for x in columns).items())),
        'compatibility_clique_counts':counts,'compatible_self_pairs':len(loops),
        'pair_graph_sha256':sha256(encoded).hexdigest(),'certificate_sha256':sha256(certbytes).hexdigest(),
        'consumer':consumer(inputs)}
    return result,certificate,edges


if __name__=='__main__':
    directory=Path(__file__).parent
    result,cert,_=calculate(json.loads((directory/'inputs.json').read_text()))
    if len(sys.argv)>1:
        need(len(sys.argv)==3 and sys.argv[1]=='--write-certificate','arguments')
        Path(sys.argv[2]).write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
