#!/usr/bin/env python3
"""Independent physical provenance and compact complete-root proof audit.

Imports no producer, inherited graph decoder, SAT solver or native verdict.
The small RUP interpreter is separate from proof production.
"""
import argparse
import hashlib
import itertools as it
import json
import math
from pathlib import Path
from check_rup import require,rup,verify

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
OPB_SHA='469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f'
ROOT_SHA='fd3eb74fe43816bf5a6e270ad6ff69e302e085db07bef51eed23432db268301a'
TABLE_SHA='f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e'
Y=13620
H=tuple(range(15,28))
U,V,P,Q=0,1,15,30
VERTICES=(0,1)+H+(30,)


def edge(a,b):
    a,b=sorted((a,b));require(0<=a<b<43,'physical edge')
    return sum(42-v for v in range(a))+b-a


def rank_five(vertices):
    rank=0;last=-1
    for j,value in enumerate(vertices):
        rank+=sum(math.comb(42-x,4-j) for x in range(last+1,value));last=value
    return rank


def root_check(path):
    raw=path.read_bytes();require(hashlib.sha256(raw).hexdigest()==ROOT_SHA,'root descriptor identity')
    r=json.loads(raw);require(r['key']==['C77partition',13,0,'HO'],'complete root key')
    require(r['anchors']==[U,V] and r['E']==list(range(2,15)) and r['anomalies']==[P,Q],'physical marks')
    expected=[[],list(range(2,8)),list(range(8,14)),[14],list(H),[28],[29],list(range(30,43))]
    require(r['cells']==expected and r['E_cells']==[0,6,6,1] and r['C_cells']==[13,1,1,13],'full cell partition')
    units=[(0,1,1)]
    for i,cell in enumerate(expected):
        bits=((1,1),(1,0),(0,1),(0,0))[i%4]
        for w in cell:units.extend([(0,w,bits[0]),(1,w,bits[1])])
    require(r['edge_units']==[list(row) for row in sorted(units)],'all 83 anchor units')
    require(r['a_equalities']==[[w,7 if w in (P,Q) else 6] for w in range(43)],'all a targets')
    central=[w for w in range(43) if w not in r['E'] and w not in (P,Q)]
    require(r['partition']=={'blue_pair':[P,Q],'one_red_to_pair':central},'universal partition')
    buckets=[]
    for cell in expected:
        for status in (0,1):
            bucket=[w for w in cell if int(w in (P,Q))==status]
            if bucket:buckets.append(bucket)
    require(r['ordering_buckets']==buckets,'residual buckets')
    table=REPO/'ramsey_r55_m214_pair_normalization/roots.tsv';raw=table.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==TABLE_SHA,'parent root table')
    rows=raw.decode().splitlines()[1:];require(len(rows)==389,'parent root count')
    row=rows[375].split('\t');require(row[:4]==['C77partition','13','0','HO'] and row[-1]==ROOT_SHA,'parent membership')
    start=1974689+2+sum(169+(57 if line.startswith('C77partition\t') else 0) for line in rows[:375])
    require(start==2041258,'selected-root first OPB row')
    return r,start


def expected_kernel(root,start):
    clauses=[];positions=[]
    for five in it.combinations(VERTICES,5):
        values=tuple(edge(a,b) for a,b in it.combinations(five,2));rank=rank_five(five)
        clauses.extend([values,tuple(-x for x in values)]);positions.extend([2*rank+1,2*rank+2])
    for offset,(a,b,value) in enumerate(root['edge_units']):
        if a in VERTICES and b in VERTICES:clauses.append((edge(a,b)*(1 if value else -1),));positions.append(start+offset)
    clauses.append((-edge(P,Q),));positions.append(start+169)
    for offset,w in enumerate(root['partition']['one_red_to_pair']):
        if w in VERTICES:
            a,b=edge(w,P),edge(w,Q);clauses.extend([(a,b),(-a,-b)]);positions.extend([start+170+2*offset,start+171+2*offset])
    require(len(clauses)==len(set(positions))==8794,'physical kernel input coverage')
    return clauses,dict(zip(positions,clauses))


def check_kernel(path,clauses):
    with path.open(encoding='ascii') as handle:
        require(next(handle,'')=='p cnf 903 8794\n','kernel header')
        for clause in clauses:
            row=next(handle,'').split();require(row and row[-1]=='0' and tuple(map(int,row[:-1]))==clause,'kernel physical clause')
        require(handle.read()=='','extra kernel clauses')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_provenance(path,positions):
    digest=hashlib.sha256();seen=set();size=0;count=0
    with path.open('rb') as handle:
        header=handle.readline();require(header==b'* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n','complete OPB header')
        digest.update(header);size+=len(header)
        for number,raw in enumerate(handle,1):
            digest.update(raw);size+=len(raw);count=number
            if number not in positions:continue
            row=raw.split();require(row[-3]==b'>=' and row[-1]==b';','kernel source relation')
            terms={int(row[k+1][1:]):int(row[k]) for k in range(0,len(row)-3,2)}
            rhs=int(row[-2])-terms.pop(Y,0)
            clause=positions[number];wanted={abs(x):1 if x>0 else -1 for x in clause}
            require(terms==wanted and rhs==1-sum(x<0 for x in clause),'source OPB does not imply physical clause under y=1')
            seen.add(number)
    require((count,size)==(2044421,172788992) and digest.hexdigest()==OPB_SHA,'complete parent identity')
    require(seen==set(positions),'source row coverage')
    return len(seen)


def r34_base():
    pairs=tuple(it.combinations(range(9),2));rank={p:i+1 for i,p in enumerate(pairs)}
    clauses=[tuple(-rank[p] for p in it.combinations(t,2)) for t in it.combinations(range(9),3)]
    clauses += [tuple(rank[p] for p in it.combinations(t,2)) for t in it.combinations(range(9),4)]
    return pairs,rank,clauses


def r34_check(proof):
    pairs,rank,base=r34_base();normalized=base+[(-rank[0,w],) for w in range(4,9)]
    proof_rows=verify(normalized,proof,36)
    require(proof_rows==288,'compact RUP certificate size')
    cap_count=0
    for neighbors in it.combinations(range(1,9),4):
        cap=tuple(-rank[0,w] for w in neighbors)
        require(rup(base,cap),'R34 star-degree cap');cap_count+=1
    # Every degree<=3 star is transported into the normalized five-blue-star case.
    original={frozenset(row) for row in base};covers=transports=0
    for size in range(4):
        for neighbors in it.combinations(range(1,9),size):
            remaining=sorted(set(range(1,9))-set(neighbors));order=(0,)+neighbors+tuple(remaining)
            mapping={i+1:rank[tuple(sorted((order[a],order[b])))] for i,(a,b) in enumerate(pairs)}
            moved={frozenset(mapping[abs(x)]*(1 if x>0 else -1) for x in row) for row in base}
            require(moved==original,'R34 full-clause permutation')
            require(all(order[w] not in neighbors for w in range(4,9)),'normalization coverage')
            covers+=1;transports+=len(mapping)
    require((cap_count,covers,transports)==(70,93,3348),'complete R34 normalization')
    return {'r34_rup_rows':proof_rows,'r34_degree_caps':cap_count,'r34_normalized_star_patterns':covers,'r34_edge_transports':transports}


def root_proof(clauses):
    database={frozenset(c):c for c in clauses};triangles={};units=[]
    def input_clause(row):
        key=frozenset(row);require(key in database,'missing physical axiom');return database[key]
    for a,b in it.combinations(VERTICES,2):
        for sign in (1,-1):
            row=(sign*edge(a,b),)
            if frozenset(row) in database:units.append(row)
    # Red triangles in H are forbidden by their red K5 with the two anchors.
    for t in it.combinations(H,3):
        row=tuple(-edge(a,b) for a,b in it.combinations(t,2));five=(U,V)+t
        red_five=input_clause(tuple(-edge(a,b) for a,b in it.combinations(five,2)))
        require(rup([red_five]+units,row),'physical core triangle derivation');triangles[t]=row
    others=tuple(w for w in H if w!=P);caps=[]
    for four in it.combinations(others,4):
        blue_five=input_clause(tuple(edge(a,b) for a,b in it.combinations(tuple(sorted(four+(Q,))),2)))
        premises=[blue_five]
        for a,b in it.combinations(four,2):premises.append(triangles[tuple(sorted((P,a,b)))])
        for w in four:premises.append(input_clause((-edge(P,w),-edge(Q,w))))
        cap=tuple(-edge(P,w) for w in four);require(rup(premises,cap),'partition forces degree<=3');caps.append(cap)
    # If any nine are blue to p, their induced graph is an R(3,4) graph.
    # Verify every physical injection and every required clause weakening.
    embeddings=implications=0
    for nine in it.combinations(others,9):
        guard={edge(P,w) for w in nine}
        for three in it.combinations(nine,3):require(three in triangles,'R34 red triangle embedding');implications+=1
        for four in it.combinations(nine,4):
            row=tuple(edge(a,b) for a,b in it.combinations(tuple(sorted((P,)+four)),2))
            premise=input_clause(row)
            target={edge(a,b) for a,b in it.combinations(four,2)}|guard
            require(set(premise)<=target,'R34 independent-four guarded weakening');implications+=1
        embeddings+=1
    require((len(triangles),len(caps),embeddings,implications)==(286,495,220,46200),'complete root proof coverage')
    # Exact exhaustive cover of the remaining twelve incident Boolean bits.
    assignments=0
    for mask in range(1<<12):
        neighbors={others[k] for k in range(12) if mask>>k&1}
        if len(neighbors)>=4:
            first=tuple(sorted(neighbors))[:4];require(tuple(-edge(P,w) for w in first) in caps,'uncovered high-degree assignment')
        else:
            nonneighbors=sorted(set(others)-neighbors);require(len(nonneighbors)>=9,'uncovered low-degree assignment')
            require(tuple(nonneighbors[:9]) in set(it.combinations(others,9)),'missing R34 embedding')
        assignments+=1
    return {'core_triangle_rup_rows':len(triangles),'partition_degree_cap_rup_rows':len(caps),'r34_physical_embeddings':embeddings,'embedding_clause_checks':implications,'incident_star_assignments_covered':assignments}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel',type=Path,required=True);parser.add_argument('--opb',type=Path,required=True)
    args=parser.parse_args();root,start=root_check(HERE/'root.json');clauses,positions=expected_kernel(root,start)
    kernel_sha=check_kernel(args.kernel,clauses);source_rows=check_provenance(args.opb,positions)
    result={'status':'EXACT_COMPLETE_M214_ROOT375_EXCLUSION','root_index':375,'root_key':['C77partition',13,0,'HO'],'selector':Y,'root_core_variables_fixed':0,'nonanchor_physical_edges_retained':820,'kernel_vertices':list(VERTICES),'kernel_clauses':len(clauses),'kernel_sha256':kernel_sha,'parent_opb_sha256':OPB_SHA,'source_rows_verified':source_rows,'remaining_root_descriptors':388,'remaining_family_counts':[60,85,70,104,69],**r34_check(HERE/'r34.rup'),**root_proof(clauses)}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
