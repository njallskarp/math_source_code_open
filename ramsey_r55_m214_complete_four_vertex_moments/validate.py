#!/usr/bin/env python3
"""Verify physical data without importing the new producer or its templates."""
import argparse
import hashlib
import importlib.util
import itertools as it
import json
import math
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
PRIOR_SHA='b126d42d57a403cb66c307962ba7a55c3ecd9a73176d66ef54750abe6b935de2'
OLD_VECTOR_SHA='c4bb5b1ccf67291ebf430a0cc5ea1e2a0dcf5d95998c4fc4b993418f484b78e4'
OLD_MOMENTS_SHA='99f9385f47f98d46093d973e3b6ccc2b84fac37b6f1d7738f9c10dac65a68210'


def require(ok,message):
    if not ok:raise ValueError(message)


def predecessor():
    path=REPO/'ramsey_r55_m214_global_star_moments/validate.py'
    require(hashlib.sha256(path.read_bytes()).hexdigest()==PRIOR_SHA,'prior checker identity')
    spec=importlib.util.spec_from_file_location('star_check',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def read_vector(path,D):
    out=[0]
    with path.open(encoding='ascii') as handle:
        require(next(handle,'')=='variable\tvalue\n','vector header')
        for k in range(1,98759):
            fields=next(handle,'').split();require(len(fields)==2 and fields[0]==str(k),'coordinate order')
            x=F(fields[1]);require(0<=x<=1 and (x*D).denominator==1,'coordinate box/scale');out.append(int(x*D))
        require(handle.read()=='','extra coordinates')
    return out


def check_old_lifts(prior,V,D,edges,roots,q):
    _,_,missed,_=prior.decoder()
    require([V[13245+r] for r in range(389)]==[D if r==48 else 0 for r in range(389)],'selected root 48')
    tri={t:k for k,t in enumerate(it.combinations(range(43),3),904)}
    for pair,index in edges.items():
        require(sum(V[tri[tuple(sorted(pair+(h,)))]] for h in range(43) if h not in pair)<=13*V[index],'red codegree')
    old_rows=moment_rows=0;S_active=set();Q_active=set()
    for r,(_,core,exterior) in enumerate(roots):
        c=len(core);p=math.comb(len(exterior),2);y=V[13245+r]
        for i,j in it.combinations(core,2):
            ds=(20 if 2<=i<=14 else 21)+(20 if 2<=j<=14 else 21);K=64-c-ds;x=V[edges[i,j]]
            Q=sum(V[q[a,b,i,j]] for a,b in it.combinations(exterior,2))
            A=sum(V[edges[tuple(sorted((h,v)))]] for h in (i,j) for v in core if h!=v)
            T=sum(V[tri[tuple(sorted((i,j,v)))]] for v in exterior);S=(45-c-ds)*D+A+T
            require(math.comb(K,2)*x+(p-math.comb(K,2))*(D-y)-Q>=0,'coupled column')
            # Reuse only the pinned algebraic facet routine, without old witness conventions.
            require(min(prior.hull_slacks(c,ds,p,S,Q,y,x,D))>=0,'reanchored moment hull')
            old_rows+=1;moment_rows+=K+1
            if y==D and x==D:
                S_active.add(F(S,D));Q_active.add(F(Q,D))
                for a,b in it.combinations(exterior,2):
                    require(V[missed[a,b,i]]==V[missed[a,b,j]] and 14*V[q[a,b,i,j]]==3*V[missed[a,b,i]],'active rho=3/14')
    require((old_rows,moment_rows,len(edges))==(21762,264560,903),'old suffix coverage')
    require(S_active=={F(5)} and Q_active=={F(117,7)},'selected-core aggregate')
    return {'coupled_column_rows':old_rows,'reanchored_hull_rows':moment_rows,'red_codegree_rows':len(edges),'active_S':'5','active_Q':'117/7'}


def parse_four_line(line,vertices,D):
    fields=line.split();require(len(fields)>=5 and tuple(map(int,fields[:4]))==vertices,'four-set order')
    atoms={};last=-1
    for field in fields[4:]:
        pair=field.split(':');require(len(pair)==2,'atom field')
        mask,mass=map(int,pair);require(last<mask<64 and mass>0,'atom state/order/positivity');last=mask;atoms[mask]=mass
    require(sum(atoms.values())==D,'four-set normalization')
    return atoms


def physical_projections(vertices,atoms):
    pairs=tuple(it.combinations(vertices,2));out={}
    for triangle in it.combinations(vertices,3):
        selected=[pairs.index(pair) for pair in it.combinations(triangle,2)];dist=[0]*8
        for mask,mass in atoms.items():
            state=0
            for bit,index in enumerate(selected):
                if mask&(1<<index):state|=1<<bit
            dist[state]+=mass
        out[triangle]=tuple(dist)
    return pairs,out


def footprint_mass(pairs,atoms,key):
    a,b,i,j=key;red=1<<pairs.index((i,j));blue=sum(1<<pairs.index(tuple(sorted((v,h)))) for v in (a,b) for h in (i,j))
    return sum(mass for mask,mass in atoms.items() if mask&red and mask&blue==0)


def check_four(handle,V,D,moments,edges,q,atom_values):
    tri_atoms={}
    for index,t in enumerate(it.combinations(range(43),3),904):
        pairs=tuple(it.combinations(t,2));m=[int(moments[tuple(v for v in t if v!=h)+(h,)]*D) for h in t]
        tri_atoms[t]=atom_values(tuple(V[edges[p]] for p in pairs),m,V[index],D)
    by_four=defaultdict(list)
    for key,index in q.items():by_four[tuple(sorted(key))].append((key,index))
    sets=equations=footprint_equations=nonzeros=0
    for vertices in it.combinations(range(43),4):
        atoms=parse_four_line(next(handle,''),vertices,D);pairs,marginals=physical_projections(vertices,atoms)
        for tri,dist in marginals.items():require(dist==tri_atoms[tri],'physical triangle marginal '+str((vertices,tri)));equations+=8
        for key,index in by_four[vertices]:require(footprint_mass(pairs,atoms,key)==V[index],'physical footprint '+str(key));footprint_equations+=1
        sets+=1;nonzeros+=len(atoms)
    require(handle.read()=='','extra four sets')
    require((sets,equations,footprint_equations)==(123410,3949120,74513),'complete four-set coverage')
    return {'four_sets':sets,'four_nonnegative_rows':64*sets,'normalization_equalities':sets,'triangle_marginal_equalities':equations,'footprint_equalities':footprint_equations,'physical_nonzero_atoms':nonzeros}


def separator(vector_path,moment_path,star,prior,edges,q):
    require(hashlib.sha256(vector_path.read_bytes()).hexdigest()==OLD_VECTOR_SHA,'old vector identity')
    require(hashlib.sha256(moment_path.read_bytes()).hexdigest()==OLD_MOMENTS_SHA,'old moment identity')
    D,V=prior.read_vector(vector_path);mom=star.read_moments(moment_path);single={}
    for index,t in enumerate(it.combinations(range(43),3),904):
        pp=tuple(it.combinations(t,2));atoms=star.atom_values(tuple(F(V[edges[p]][1],D) for p in pp),tuple(mom[tuple(v for v in t if v!=h)+(h,)] for h in t),F(V[index][1],D))
        for bit,pair in enumerate(pp):single[(next(v for v in t if v not in pair),)+pair]=atoms[1<<bit]
    counts=[0,0]
    for (a,b,i,j),index in q.items():
        bound=min(single[a,i,j],single[b,i,j])
        for col in (1,2):counts[col-1]+=F(V[index][col],D)>bound
    key=(2,30,15,16);index=q[key];upper=single[30,15,16]
    gaps=[upper-F(V[index][col],D) for col in (1,2)]
    require(counts==[32437,32437] and gaps==[-F(493,141960),-F(137,10920)],'strict old-family separator')
    return {'old_upper_violating_footprints_by_endpoint':counts,'old_family_excluded':['3/14','10/39'],'separator_key':list(key),'separator_upper':str(upper),'separator_endpoint_slacks':list(map(str,gaps))}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('vector','moments','four','opb','old-vector','old-moments'):parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();star=predecessor();prior=star.predecessor();edges,roots,missed,q=prior.decoder()
    with args.four.open(encoding='ascii') as handle:
        fields=next(handle,'').split();require(len(fields)==3 and fields[:2]==['four-vertex-atoms','43'],'four header');D=int(fields[2]);require(D>0,'scale')
        V=read_vector(args.vector,D);tripled=[(x,x,x) for x in V];moments=star.read_moments(args.moments)
        require(all((m*D).denominator==1 for m in moments.values()),'moment scale')
        rows,eq=prior.check_opb(args.opb,tripled,D)
        old_stats=check_old_lifts(prior,V,D,edges,roots,q)
        star_stats=star.check_joint(tripled,D,moments,edges,missed)
        four_stats=check_four(handle,V,D,moments,edges,q,star.atom_values)
    sep=separator(args.old_vector,args.old_moments,star,prior,edges,q)
    result={'status':'EXACT_COMPLETE_FOUR_VERTEX_LP_SURVIVOR','base_opb_rows':rows,'base_opb_equalities':eq,'prior_full_rows':3371665,'total_rows':15416948,'total_equalities':4148936,'total_variables':8023409,'point_rho':'3/14','common_denominator':str(D),'formula_sha256':prior.FORMULA_SHA,'red_deficiency_sum':star_stats['red_deficiency_sum'],'blue_deficiency_sum':star_stats['blue_deficiency_sum'],**old_stats,**four_stats,**sep}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
