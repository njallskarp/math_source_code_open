"""Exact density-114 type62 five-column classification; Python bitset producer."""
from itertools import combinations,permutations
from collections import Counter
from pathlib import Path
import json,sys
from hashlib import sha256

def setup(minimum):
    U=(1<<17)-1
    P=[sum(1<<v for v in range(17) if (v-u)%17 in {1,2,4,8,9,13,15,16}) for u in range(17)]
    Q=[U^(1<<v)^P[v] for v in range(17)]
    ind=bytearray(U+1);clique=bytearray(U+1);tf=bytearray(U+1);btf=bytearray(U+1)
    ind[0]=clique[0]=tf[0]=btf[0]=1
    for m in range(1,U+1):
        bit=m&-m;v=bit.bit_length()-1;r=m^bit
        ind[m]=ind[r] and not(P[v]&r);clique[m]=clique[r] and not(Q[v]&r)
        tf[m]=tf[r] and ind[P[v]&r];btf[m]=btf[r] and clique[Q[v]&r]
    cols=[m for m in range(U+1) if tf[m] and m.bit_count()>=minimum-32]
    sizes=[m.bit_count() for m in cols];N=len(cols);RR=[0]*N;BB=[0]*N
    for i,x in enumerate(cols):
        for j,y in enumerate(cols):
            if ind[x&y]:RR[i]|=1<<j
            if btf[U^(x|y)]:BB[i]|=1<<j
    return cols,sizes,RR,BB,clique

def enumerate_type(kind,minimum,data,affine=False):
    cols,sizes,RR,BB,clique=data;N=len(cols);full=(1<<N)-1
    bysize={k:sum(1<<i for i,s in enumerate(sizes) if s>=k) for k in range(9)}
    E={(0,2),(0,3),(0,4),(1,2),(1,3)}
    if kind==126:E.add((1,4))
    order=[0,2,1,3,4];chosen={};visits=Counter();solutions=[]
    first=full
    if affine:
        lookup={m:i for i,m in enumerate(cols)};left=set(cols);first=0
        while left:
            m=min(left);first|=1<<lookup[m]
            orbit={sum(1<<((a*v+b)%17) for v in range(17) if m>>v&1)
                   for a in (1,2,4,8,9,13,15,16) for b in range(17)}
            if not orbit<=set(cols):raise ValueError('invalid column action')
            left-=orbit
    def dfs(domains,total):
        d=len(chosen);visits[d]+=1
        if d==5:
            solutions.append([cols[chosen[s]] for s in range(5)]);return
        s=order[d];cand=domains[s]&bysize[max(0,minimum-total-8*(4-d))]
        if d==0:cand&=first
        while cand:
            bit=cand&-cand;cand^=bit;i=bit.bit_length()-1
            good=True
            for a,b in combinations(chosen,2):
                if all(tuple(sorted(e)) not in E for e in [(a,b),(a,s),(b,s)]):
                    missing=131071^(cols[i]|cols[chosen[a]]|cols[chosen[b]])
                    if not clique[missing]:good=False;break
            if not good:continue
            nextdomains=dict(domains)
            for t in order[d+1:]:
                nextdomains[t]&=(RR if tuple(sorted((s,t))) in E else BB)[i]
                if not nextdomains[t]:good=False;break
            if good:
                chosen[s]=i;dfs(nextdomains,total+sizes[i]);del chosen[s]
    dfs({s:full for s in range(5)},0)
    return {'type':kind,'minimum_cross_edges':minimum,'column_domain':N,'affine':affine,'first_columns':first.bit_count(),'solutions':solutions,'visits':dict(visits),'cross_histogram':dict(Counter(sum(m.bit_count() for m in row) for row in solutions))}

def canonical_family(kind,solutions):
    E={(0,2),(0,3),(0,4),(1,2),(1,3)}
    if kind==126:E.add((1,4))
    sa=[p for p in permutations(range(5)) if {tuple(sorted((p[u],p[v]))) for u,v in E}==E]
    masks={m for row in solutions for m in row}
    trans={m:[sum(1<<((a*v+b)%17) for v in range(17) if m>>v&1)
              for a in (1,2,4,8,9,13,15,16) for b in range(17)] for m in masks}
    reps=sorted({min(tuple(trans[row[p[s]]][i] for s in range(5))
                     for p in sa for i in range(136)) for row in solutions})
    full={tuple(trans[m][i] for m in row) for row in solutions for i in range(136)}
    representatives=[]
    for row in reps:
        orbit={tuple(trans[row[p[s]]][i] for s in range(5)) for p in sa for i in range(136)}
        if not orbit<=full:raise ValueError('incomplete orbit')
        representatives.append({'columns':list(row),'orbit_size':len(orbit)})
    raw=''.join(' '.join(map(str,row))+'\n' for row in sorted(full)).encode()
    return {'type':kind,'labeled_count':len(full),
            'full_tuple_sha256':sha256(raw).hexdigest(),'representatives':representatives}

def calculate():
    data=setup(36)
    if max(data[1])!=8: raise ValueError('column maximum')
    answer=enumerate_type(62,36,data,True)
    exact=[row for row in answer['solutions'] if sum(m.bit_count() for m in row)==36]
    family=canonical_family(62,exact)
    family['edges']=114
    return {'type':62,'cross_edges':36,'paley_order':17,'column_domain':len(data[0]),
            'minimum_column_size':min(data[1]),'maximum_column_size':max(data[1]),
            'first_column_orbits':answer['first_columns'],'normalized_tuples':len(exact),
            'family':family}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);args=p.parse_args()
    result=calculate()
    args.output.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'COMPLETE_TYPE62_DENSITY114_PRODUCED',
        'classes':len(result['family']['representatives']),
        'labeled_tuples':result['family']['labeled_count'],
        'column_domain':result['column_domain'],
        'orbit_sizes':dict(Counter(r['orbit_size'] for r in result['family']['representatives'])),
        'tuple_sha256':result['family']['full_tuple_sha256']},sort_keys=True),flush=True)
