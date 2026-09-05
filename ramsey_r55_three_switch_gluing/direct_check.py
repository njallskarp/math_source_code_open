#!/usr/bin/env python3
"""Separate literal-graph audit over all 4096 assignments of the 12 holes.

Imports no producer/primary checker and does not compile K5 clauses.
"""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def check(ok,message):
    if not ok: raise ValueError(message)


def digest(value):
    return sha256((json.dumps(value,separators=(',',':'))+'\n').encode()).hexdigest()


def cliques(rows,color):
    neighbors=rows if color else [((1<<15)-1)^r^(1<<u) for u,r in enumerate(rows)]
    result=[]
    def visit(chosen,candidates):
        if len(chosen)==5:
            result.append(chosen);return
        while candidates:
            bit=candidates&-candidates;candidates-=bit;v=bit.bit_length()-1
            visit(chosen+(v,),candidates&neighbors[v])
    visit((),(1<<15)-1)
    return result


def main():
    d=json.loads((ROOT/'fixture.json').read_text());p=d['partial'];blocks=d['blocks']
    check(d['n']==15 and len(p)==15,'domain')
    check(all(len(row)==15 and row[u]=='-' for u,row in enumerate(p)),'dimensions')
    check(all(p[u][v]==p[v][u] and p[u][v] in '01.' for u,v in combinations(range(15),2)),'matrix')
    holes=[e for e in combinations(range(15),2) if p[e[0]][e[1]]=='.']
    check(len(holes)==12,'holes')
    base=[sum(1<<v for v,c in enumerate(row) if c=='1') for row in p]
    block_of={tuple(sorted((u,v))):i for i,(left,right) in enumerate(blocks) for u in left for v in right}
    check(set(block_of)==set(holes),'complete complementary blocks')
    check([base[a].bit_count() for a in range(3)]==d['red_degrees'][:3],'root degrees')
    for i,(left,right) in enumerate(blocks):
        check(all(base[u]&7==1<<i for u in left),'singleton signature')
        check(all(base[v]&7==7^(1<<i) for v in right),'pair signature')
        check(all(d['red_degrees'][v]-base[v].bit_count()==1 for v in left+right),'residual margins')
    events=defaultdict(set);states_seen=set();ramsey_masks=[];degree_masks=[];census=[]
    for mask in range(4096):
        rows=base[:]
        for bit,(u,v) in enumerate(holes):
            if mask>>bit&1: rows[u]|=1<<v;rows[v]|=1<<u
        red=cliques(rows,1);blue=cliques(rows,0)
        if not red and not blue: ramsey_masks.append(mask)
        degrees=[r.bit_count() for r in rows]
        if degrees!=d['red_degrees']: continue
        degree_masks.append(mask)
        state=tuple(1-int(bool(rows[left[0]]>>right[0]&1)) for left,right in blocks)
        check(state not in states_seen,'unique margin realization per state');states_seen.add(state)
        census.append([list(state),len(red),len(blue)])
        check(bool(red or blue),'no Ramsey degree completion')
        for color,qs in [(0,blue),(1,red)]:
            for q in qs: events[color,q].add(state)
    check(len(degree_masks)==8 and len(states_seen)==8,'full degree fiber')
    check(ramsey_masks and 4095 in ramsey_masks,'degree hypotheses are substantive')
    records=[]
    for (color,q),states in sorted(events.items()):
        support=sorted({block_of[e] for e in combinations(q,2) if e in block_of})
        check(len(support)==2 and len(states)==2,'two-block event support')
        assignments=[[i,next(iter({s[i] for s in states}))] for i in support]
        check(all(len({s[i] for s in states})==1 for i in support),'fixed event state')
        records.append([color,list(q),assignments])
    relations={pair:set(product((0,1),repeat=2)) for pair in combinations(range(3),2)}
    for color,q,assignment in records:
        pair=tuple(i for i,s in assignment);value=tuple(s for i,s in assignment)
        relations[pair].discard(value)
    check(all(r=={(0,1),(1,0)} for r in relations.values()),'literal pair relations')
    check(len(records)==10 and all(r[0]==0 for r in records),'all ten events blue')
    for r in d['selected_clauses']:
        check([r['color'],r['five'],[[i,r['equal_state']] for i in r['blocks']]] in records,'selected literal event')
    # Different route to the abstract table: compose 2x2 relation matrices.
    matrices={}
    for bits in range(16):
        m=[[bits>>(a+2*b)&1 for b in range(2)] for a in range(2)]
        if all(any(row) for row in m) and all(any(m[a][b] for a in range(2)) for b in range(2)): matrices[bits]=m
    table=[]
    for a,b,c in product(sorted(matrices),repeat=3):
        product_matrix=[[sum(matrices[a][u][v]*matrices[b][v][w] for v in range(2)) for w in range(2)] for u in range(2)]
        count=sum(product_matrix[u][w]*matrices[c][u][w] for u in range(2) for w in range(2))
        table.append([a,b,c,count])
    return {'status':'LITERAL THREE-SWITCH GRAPH AUDIT VERIFIED','all_hole_assignments':4096,
            'degree_realizations':len(degree_masks),'ramsey_without_degree_count':len(ramsey_masks),
            'all_red_holes_is_ramsey':4095 in ramsey_masks,'degree_completion_census':sorted(census),
            'active_records':records,'active_records_sha256':digest(records),
            'abstract_table_sha256':digest(table),'zero_join_relation_triples':[r[:3] for r in table if not r[3]]}


if __name__=='__main__': print(json.dumps(main(),sort_keys=True,indent=2))
