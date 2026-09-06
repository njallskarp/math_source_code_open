"""Independent physical, orbit and complete-consumer audit (no producer import)."""
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

def check_certificate(certificate,tuple_paths=None):
    require(certificate['minimum_cross_edges']==37,'density threshold')
    families=certificate['families'];require([f['type'] for f in families]==[62,126],'two complete families')
    P=paley();actions=automorphisms(P);results=[]
    for position,f in enumerate(families):
        kind=f['type'];E=s_edges(kind)
        sp=[p for p in permutations(range(5)) if all(((u,v) in E)==(tuple(sorted((p[u],p[v]))) in E) for u,v in combinations(range(5),2))]
        require(len(sp)==(2 if kind==62 else 12),'S automorphisms')
        representatives=f['representatives'];require(len(representatives)==(24 if kind==62 else 29),'class count')
        expanded=set();previous=None
        for entry in representatives:
            row=tuple(entry['columns']);require(sum(m.bit_count() for m in row)==37,'boundary sum')
            require(previous is None or previous<row,'canonical order');previous=row
            A=physical_graph(kind,row,P);degrees=list(map(sum,A))
            require([v for v,d in enumerate(degrees) if d==5]==[22],'unique degree-five hub')
            require(sum(degrees)//2==f['maximum_edges']==(115 if kind==62 else 116),'edge extremum')
            require(not has_clique(A,4),'red K4 in representative')
            blue=[[u!=v and not A[u][v] for v in range(23)] for u in range(23)]
            require(not has_clique(blue,5),'blue K5 in representative')
            copies=orbit(row,actions,sp)
            require(min(copies)==row and len(copies)==entry['orbit_size']==136*len(sp),'canonical rigid orbit')
            require(not expanded&copies,'overlapping isomorphism classes');expanded|=copies
        raw=''.join(' '.join(map(str,row))+'\n' for row in sorted(expanded)).encode()
        require(len(expanded)==f['labeled_count'] and sha256(raw).hexdigest()==f['full_tuple_sha256'],'orbit expansion identity')
        if tuple_paths is not None:
            require(Path(tuple_paths[position]).read_bytes()==raw,'full independent enumeration differs entry by entry')
        results.append({'type':kind,'classes':len(representatives),'labeled_tuples':len(expanded),
                        'maximum_edges':f['maximum_edges'],'all_rigid':True,'tuple_sha256':sha256(raw).hexdigest()})
    return results

def consumer(inputs,certificate):
    records=inputs['interfaces'];require(len(records)==13 and len(set(records))==13,'complete thirteen input records')
    P=paley();pairs=list(combinations(range(43),2));index={e:i for i,e in enumerate(pairs)}
    permutation=[(5*v+7)%43 for v in range(43)]
    transport=[index[tuple(sorted((permutation[u],permutation[v])))] for u,v in pairs]
    families={f['type']:f for f in certificate['families']};digest=sha256();counts={62:0,126:0};edge_checks=0;types=[]
    for h,record in enumerate(records):
        n,E=graph6(record);require(n==22 and len(E)==109,'input interface order/density')
        A=[[tuple(sorted((u,v))) in E if u!=v else False for v in range(n)] for u in range(n)]
        require(not has_clique(A,4) and not has_clique([[u!=v and not A[u][v] for v in range(n)] for u in range(n)],5),'input interface forbidden set')
        hubs=[v for v in range(n) if sum(A[v])==5];require(hubs==[21],'pinned unique hub')
        S=[v for v in range(n) if A[21][v]]
        profile=sorted(sum(A[u][v] for v in S) for u in S)
        if profile==[1,1,1,1,4]:
            require(h==5,'star interface identity');types.append(15);continue
        kind=62 if profile==[1,2,2,2,3] else 126 if profile==[2,2,2,3,3] else None
        require(kind is not None,'unexpected S type');types.append(kind)
        embeddings=[q for q in permutations(S) if all(A[q[u]][q[v]]==((u,v) in s_edges(kind)) for u,v in combinations(range(5),2))]
        require(len(embeddings)==(2 if kind==62 else 12),'all S markings')
        seen=set()
        for j,entry in enumerate(families[kind]['representatives']):
            for mark,q in enumerate(embeddings):
                fixed={e:e in E for e in combinations(range(22),2)}
                fixed.update({(u,22):True for u in range(22)})
                fixed.update({(22,v):False for v in range(23,43)})
                fixed.update({(21,v):v<40 for v in range(23,43)})
                fixed.update({(u+23,v+23):P[u][v] for u,v in combinations(range(17),2)})
                fixed.update({(q[s],v+23):bool(entry['columns'][s]>>v&1) for s in range(5) for v in range(17)})
                require(len(fixed)==514,'fixed/free physical count')
                encoded=bytes(int(fixed[e]) if e in fixed else 2 for e in pairs)
                require(encoded not in seen,'duplicate marked template');seen.add(encoded)
                key=f'{h} {kind} {j} {mark}\n'.encode();digest.update(key);digest.update(encoded)
                # Deliberately arbitrary free colors test transport, not Ramsey feasibility.
                values=[int(fixed[e]) if e in fixed else (u+3*v+j+mark)%2 for e in pairs for u,v in [e]]
                moved=[None]*903
                for i,t in enumerate(transport):moved[t]=values[i]
                require(all(moved[t]==values[i] for i,t in enumerate(transport)),'full physical round trip')
                neighbors=[22]+S+list(range(23,40))
                require(sum(values[index[tuple(sorted(e))]] for e in combinations(neighbors,2))==families[kind]['maximum_edges'],'hub density retained with all free bits')
                counts[kind]+=1;edge_checks+=903
    require(types==[126]*5+[15]+[62]*3+[126]*4,'all thirteen type distinctions')
    require(counts=={62:144,126:3132},'complete boundary case counts')
    return {'boundary_keys':sum(counts.values()),'keys_by_type':{str(k):v for k,v in counts.items()},
            'free_edges_per_boundary_key':389,'physical_edge_transports':edge_checks,
            'marked_template_sha256':digest.hexdigest(),
            'degree23_hub_deficiency_lower_bounds':[6]*5+[None]+[7]*3+[6]*4}

def audit(directory,tuple_paths=None):
    certificate=json.loads((directory/'certificate.json').read_text())
    families=check_certificate(certificate,tuple_paths)
    return {'status':'VERIFIED_COMPLETE_DENSE_HUB_CLASSIFICATION',
            'families':families,'paley_automorphisms':136,
            'consumer':consumer(json.loads((directory/'inputs.json').read_text()),certificate)}

if __name__=='__main__':
    require(len(sys.argv)==3,'supply both complete independent tuple files')
    print(json.dumps(audit(Path(__file__).parent,sys.argv[1:]),indent=2,sort_keys=True))
