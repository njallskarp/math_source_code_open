#!/usr/bin/env python3
"""Boundary fixtures, proof corruption and definition-level RUP controls."""
import itertools as it
import json
import random
import tempfile
from pathlib import Path
from check_rup import require,rup,verify
import audit

HERE=Path(__file__).resolve().parent


def boundary(rows):
    require([r['name'] for r in rows]==['c12','one_exception'],'boundary case list')
    counts=[]
    for row in rows:
        vertices=row['vertices'];H=set(row['core']);p,q=row['p'],row['q'];u,v=row['anchors'];red={frozenset(e) for e in row['red_edges']}
        require(len(red)==len(row['red_edges']) and all(len(e)==2 and e<=set(vertices) for e in red),'simple fixture')
        require(set(vertices)==H|{q,u,v} and p in H and len(H)==(12 if row['name']=='c12' else 13),'fixture scope')
        edge=lambda a,b:frozenset((a,b)) in red
        require(edge(u,v) and all(edge(u,h) and edge(v,h) for h in H),'fixture common core')
        require(not edge(q,p) and not edge(q,u) and not edge(q,v),'fixture blue contacts')
        require(all(sum(edge(a,b) for a,b in it.combinations(t,2))<3 for t in it.combinations(H,3)),'triangle-free core')
        deviations=[h for h in sorted(H-{p}) if int(edge(p,h))+int(edge(q,h))!=1]
        require(deviations==([] if row['name']=='c12' else [1]),'partition boundary')
        require(sum(edge(p,h) for h in H-{p})==(3 if row['name']=='c12' else 4),'degree boundary')
        monochromatic=0
        for five in it.combinations(vertices,5):
            n=sum(edge(a,b) for a,b in it.combinations(five,2));monochromatic+=n in (0,10)
        require(monochromatic==row['monochromatic_fives']==0,'boundary is not a Ramsey witness at its stated small order')
        counts.append(math_comb(len(vertices),5))
    return counts


def math_comb(n,k):
    return len(list(it.combinations(range(n),k)))


def main():
    rows=json.loads((HERE/'boundary-fixtures.json').read_text());five_counts=boundary(rows)
    rng=random.Random(375);accepted=0
    def satisfies(clause,mask):return any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in clause)
    for _ in range(1000):
        formula=[]
        for _ in range(rng.randrange(1,13)):
            variables=rng.sample(range(1,5),rng.randrange(1,5));formula.append(tuple(v*rng.choice((-1,1)) for v in variables))
        variables=rng.sample(range(1,5),rng.randrange(5));candidate=tuple(v*rng.choice((-1,1)) for v in variables)
        if rup(formula,candidate):
            require(all(not all(satisfies(c,m) for c in formula) or satisfies(candidate,m) for m in range(16)),'RUP soundness');accepted+=1
    _,_,base=audit.r34_base();normalized=base+[(-w,) for w in range(4,9)]
    proof=(HERE/'r34.rup').read_text();mutations=['',proof.rsplit('\n',2)[0]+'\n',proof+'0\n','37 0\n'+proof,'0\n'+proof]
    rejected=0
    with tempfile.TemporaryDirectory() as directory:
        p=Path(directory)/'damaged.rup'
        for text in mutations:
            p.write_text(text)
            try:verify(normalized,p,36)
            except ValueError:rejected+=1
            else:raise ValueError('accepted proof mutation')
        original=json.loads((HERE/'root.json').read_text())
        for mutate in ('k','pattern','missing_partition','wrong_anomaly'):
            r=json.loads(json.dumps(original))
            if mutate=='k':r['key'][2]=1
            elif mutate=='pattern':r['key'][3]='AB'
            elif mutate=='missing_partition':r['partition']['one_red_to_pair'].remove(16)
            else:r['anomalies'][0]=16
            p.write_text(json.dumps(r))
            try:audit.root_check(p)
            except ValueError:rejected+=1
            else:raise ValueError('accepted changed complete-root scope')
    require(rejected==9,'mutation count')
    guard_checks=0
    for x,z,y in it.product((0,1),repeat=3):
        lower=x+z-y>=0;upper=-x-z-y>=-2
        require((lower and upper)==(y==0 or x+z==1),'selector partition semantics');guard_checks+=1
    print(json.dumps({'status':'PASS','boundary_orders':[15,16],'boundary_five_sets':five_counts,'boundary_monochromatic_fives':[0,0],'rup_truth_table_instances':1000,'rup_accepted_and_sound':accepted,'proof_and_scope_mutations_rejected':rejected,'selector_guard_checks':guard_checks},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
