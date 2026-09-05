#!/usr/bin/env python3
"""Exact clause compiler and binary-fiber gluing audit; no solver."""
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def require(ok,message):
    if not ok: raise ValueError(message)


def digest(value):
    return sha256((json.dumps(value,separators=(',',':'))+'\n').encode()).hexdigest()


def verify(doc):
    require(type(doc) is dict and set(doc)=={'format','n','anchors','blocks','partial','red_degrees','selected_clauses'},'fields')
    require(doc['format']=='r55-three-switch-gluing-v1' and doc['n']==15 and doc['anchors']==[0,1,2],'domain')
    blocks=doc['blocks'];p=doc['partial'];targets=doc['red_degrees']
    require(blocks==[[[3,4],[5,6]],[[7,8],[9,10]],[[11,12],[13,14]]],'block labels')
    require(type(p) is list and len(p)==15 and all(type(row) is str and len(row)==15 for row in p),'matrix shape')
    require(all(p[u][u]=='-' for u in range(15)),'diagonal')
    require(all(p[u][v] in '01.' and p[u][v]==p[v][u] for u,v in combinations(range(15),2)),'edge encoding')
    require(type(targets) is list and len(targets)==15 and all(type(d) is int and 0<=d<15 for d in targets),'degree schema')
    free={};fibers=[]
    for k,(left,right) in enumerate(blocks):
        es=[(u,v) for u in left for v in right]
        for j,e in enumerate(es): free[e]=(k,j)
        valid=[]
        for mask in range(16):
            if all(sum(mask>>j&1 for j,e in enumerate(es) if u in e)==1 for u in left+right): valid.append(mask)
        require(valid==[6,9],'complete margin fiber')
        fibers.append([9,6])  # state 0 diagonal, state 1 off-diagonal
    require({e for e in combinations(range(15),2) if p[e[0]][e[1]]=='.'}==set(free),'exact free pairs')
    for u in range(15):
        require(targets[u]==p[u].count('1')+int(u>=3),'residual degree one')
    require(all(p[u][v]=='1' for u,v in combinations(range(3),2)),'red anchor triangle')
    sig={u:sum(1<<a for a in range(3) if p[a][u]=='1') for u in range(3,15)}
    for k,(left,right) in enumerate(blocks):
        require(all(sig[u]==1<<k for u in left) and all(sig[u]==7^(1<<k) for u in right),'proper signatures')
    require(all((e in free)==(sig[e[0]]^sig[e[1]]==7) for e in combinations(range(3,15),2)),'visibility')

    def fixed_cliques(side,size,color):
        return [q for q in combinations(sorted(side),size) if all(p[u][v]==str(color) for u,v in combinations(q,2))]

    for a in range(3):
        for color in (0,1):
            side=[v for v in range(15) if p[a][v]==str(color)]
            require(all(p[u][v]!='.' for u,v in combinations(side,2)),'neighborhood fixed')
            require(not fixed_cliques(side,4,color) and not fixed_cliques(side,5,1-color),'full neighborhood test')
    singles=[u for u,s in sig.items() if s.bit_count()==1]
    pairs=[u for u,s in sig.items() if s.bit_count()==2]
    require(not fixed_cliques(singles,5,1) and not fixed_cliques(pairs,5,0),'two mixed strata')

    records=[];raw=0
    for q in combinations(range(15),5):
        es=list(combinations(q,2));unknown=[e for e in es if e in free]
        support=sorted({free[e][0] for e in unknown})
        require(len(support)<=2,'at most two complementary blocks')
        for color in (0,1):
            if any(p[u][v]!=str(color) for u,v in es if (u,v) not in free): continue
            raw+=1
            for states in product((0,1),repeat=len(support)):
                assignment=dict(zip(support,states))
                if all(fibers[free[e][0]][assignment[free[e][0]]]>>free[e][1]&1==color for e in unknown):
                    require(len(support)==2,'zero/single-block obstruction')
                    records.append([color,list(q),[[k,assignment[k]] for k in support]])
    records.sort()
    require(len(records)==10 and all(r[0]==0 for r in records),'active colored five-sets')
    relations={pair:{(a,b) for a,b in product((0,1),repeat=2)} for pair in combinations(range(3),2)}
    for color,q,assignment in records:
        pair=tuple(k for k,s in assignment);state=tuple(s for k,s in assignment)
        relations[pair].discard(state)
    require(all(r=={(0,1),(1,0)} for r in relations.values()),'exact pairwise disequalities')
    good=[s for s in product((0,1),repeat=3) if all((s[a],s[b]) in r for (a,b),r in relations.items())]
    require(not good,'empty three-way join')
    for (a,b),r in relations.items():
        require({x for x,y in r}=={0,1} and {y for x,y in r}=={0,1},'arc consistency')

    selected=doc['selected_clauses']
    require(type(selected) is list and len(selected)==6,'selected rows')
    origins=[]
    for row in selected:
        require(set(row)=={'blocks','equal_state','color','five'},'selected schema')
        pair=row['blocks'];s=row['equal_state']
        require(pair in ([0,1],[0,2],[1,2]) and type(s) is int and s in (0,1) and row['color']==0,'selected state')
        rec=[0,row['five'],[[b,s] for b in pair]]
        require(rec in records,'literal selected origin')
        origins.append((tuple(pair),s))
    require(len(set(origins))==6,'distinct six state prohibitions')
    deletions=[]
    for omitted in range(6):
        models=[list(s) for s in product((0,1),repeat=3)
                if all(not(s[a]==s[b]==v) for j,((a,b),v) in enumerate(origins) if j!=omitted)]
        require(len(models)==1,'selected-row deletion model')
        deletions.append(models[0])

    arc=[]
    for mask in range(16):
        r={(a,b) for a,b in product((0,1),repeat=2) if mask>>(a+2*b)&1}
        if {a for a,b in r}=={0,1} and {b for a,b in r}=={0,1}: arc.append(mask)
    require(len(arc)==7,'binary arc-consistent relations')
    table=[];bad=[]
    for r01,r12,r02 in product(arc,repeat=3):
        count=sum(bool(r01>>(a+2*b)&1 and r12>>(b+2*c)&1 and r02>>(a+2*c)&1) for a,b,c in product((0,1),repeat=3))
        parity_obstruction=all(r in (6,9) for r in (r01,r12,r02)) and sum(r==6 for r in (r01,r12,r02))%2==1
        require((count==0)==parity_obstruction,'complete binary gluing classification')
        table.append([r01,r12,r02,count])
        if not count: bad.append([r01,r12,r02])
    require(len(bad)==4,'four parity obstructions')
    return {'status':'EXACT THREE-SWITCH GLUING SEPARATION VERIFIED','vertices':15,'free_edges':12,
            'block_domain_sizes':[2,2,2],'root_neighborhood_tests':6,'mixed_stratum_tests':2,
            'undischarged_raw_colored_fives':raw,'active_colored_fives':len(records),
            'active_records':records,'active_records_sha256':digest(records),
            'pair_relation_masks':[6,6,6],'joint_completions':0,'selected_rows':6,'deletion_models':deletions,
            'abstract_arc_consistent_networks':len(table),'inconsistent_networks':bad,'abstract_table_sha256':digest(table)}


if __name__=='__main__':
    print(json.dumps(verify(json.loads((ROOT/'fixture.json').read_text())),sort_keys=True,indent=2))
