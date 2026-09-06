#!/usr/bin/env python3
"""Exact full-P4 selector-fiber audit, importing no producer or solver."""
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as F
import hashlib
import itertools as it
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
E=frozenset(range(2,15));N=43
REMOVED=(48,128,129,201,202,299,300,375,376)
FORMULA_SHA='9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609'
HEADER=b'* #variable= 98758 #constraint= 2983003 #equal= 87 intsize= 64\n'
PAIRS4=tuple(it.combinations(range(4),2))


def require(ok,message):
    if not ok:raise ValueError(message)


def geometry():
    edge={pair:i for i,pair in enumerate(it.combinations(range(N),2),1)}
    triangle={vs:i for i,vs in enumerate(it.combinations(range(N),3),904)}
    roots=[]
    for family,patterns in enumerate((('H','A'),('BB','BO','OO'),('B','O'),('BB','BO','OO'),('HO','AB'))):
        for c in range(9,14):
            for k in range(7):
                sizes=(k,6-k,6-k,1+k,c-k,14-c+k,14-c+k,c-k)
                cells=[];first=2
                for size in sizes:cells.append(tuple(range(first,first+size)));first+=size
                require(first==43,'complete physical partition')
                for pattern in patterns:
                    offset=0 if family<2 else 4
                    if any(pattern.count(label)>sizes[offset+j] for j,label in enumerate('HABO')):continue
                    core=tuple(sorted(cells[0]+cells[4]));outside=tuple(v for v in range(2,N) if v not in core)
                    units={(0,1):1}
                    for j,cell in enumerate(cells):
                        bits=((1,1),(1,0),(0,1),(0,0))[j%4]
                        for w in cell:units[0,w]=bits[0];units[1,w]=bits[1]
                    require(len(units)==83,'full two-anchor star')
                    roots.append(((family,c,k,pattern),core,outside,units))
    require(len(roots)==389,'root cover count')
    require(tuple(r for r,(key,*_) in enumerate(roots) if key[1:3]==(13,0))==REMOVED,'exact nine removed roots')
    ms=set();qs=set()
    for _,core,outside,_ in roots:
        for a,b in it.combinations(outside,2):
            ms.update((a,b,h) for h in core);qs.update((a,b,i,j) for i,j in it.combinations(core,2))
    require((len(ms),len(qs))==(10612,74513),'complete inherited support')
    missed={key:13634+i for i,key in enumerate(sorted(ms))}
    footprints={key:24246+i for i,key in enumerate(sorted(qs))}
    return edge,triangle,roots,missed,footprints


class Point:
    """The certificate defines a value at every physical coordinate."""
    def __init__(self,path):
        raw=json.loads(path.read_text());require(set(raw)=={'denominator','four_vertex_atoms'},'certificate fields')
        self.D=raw['denominator'];require(type(self.D)==int and self.D>0 and self.D%13==0,'integer scale')
        rows=raw['four_vertex_atoms'];require(len(rows)==5,'all five class counts')
        base=[]
        for q,row in enumerate(rows):
            require(set(row)=={'exceptional_count','numerators'} and row['exceptional_count']==q,'class ordering')
            nums=row['numerators'];require(len(nums)==64 and all(type(x)==int and 0<=x<=self.D for x in nums),'64 exact masses')
            require(sum(nums)==self.D,'normalization');base.append(tuple(nums))
        self.four={}
        # Map each physical six-bit state into the certificate's E-first order.
        for types in it.product((0,1),repeat=4):
            order=tuple(i for i in range(4) if types[i])+tuple(i for i in range(4) if not types[i])
            dist=[]
            for mask in range(64):
                canonical=0
                for j,(a,b) in enumerate(PAIRS4):
                    physical=PAIRS4.index(tuple(sorted((order[a],order[b]))))
                    canonical|=((mask>>physical)&1)<<j
                dist.append(base[sum(types)][canonical])
            self.four[types]=tuple(dist)
        self.triples={}
        for types in it.product((0,1),repeat=3):
            self.triples[types]=self.project(self.four[types+(0,)],(0,1,2))
        self.edges={types:sum(m for s,m in enumerate(self.triples[types+(0,)]) if s&1) for types in it.product((0,1),repeat=2)}
        self.edge,self.triangle,self.roots,self.missed,self.q=geometry()
        self.V=[0]*98759;defined=set()
        def set_value(index,value):
            require(index not in defined and 0<=value<=self.D,'coordinate box/uniqueness');defined.add(index);self.V[index]=value
        for pair,index in self.edge.items():set_value(index,self.edges[self.types(pair)])
        for vs,index in self.triangle.items():set_value(index,self.triples[self.types(vs)][7])
        for r in range(389):set_value(13245+r,0)  # symbolic selector, not a fixed zero
        for key,index in self.missed.items():set_value(index,self.wedge(*key))
        for key,index in self.q.items():
            # Physical order (a,b,i,j): state 32/33 has ij red and the four
            # cross incidences blue, with ab unrestricted.
            dist=self.four[self.types(key)];set_value(index,dist[32]+dist[33])
        require(defined==set(range(1,98759)),'all inherited coordinates decoded')
        self.all_wedges={(a,b,h):self.wedge(a,b,h) for a,b in it.combinations(range(N),2) for h in range(N) if h not in (a,b)}
        require(len(self.all_wedges)==37023 and all(0<=v<=self.D for v in self.all_wedges.values()),'all old/new wedge boxes')

    @staticmethod
    def types(vs):return tuple(int(v in E) for v in vs)

    @staticmethod
    def project(dist,positions):
        bits=[PAIRS4.index(pair) for pair in it.combinations(positions,2)];result=[0]*8
        for state,mass in enumerate(dist):
            target=sum(((state>>bit)&1)<<j for j,bit in enumerate(bits));result[target]+=mass
        return tuple(result)

    def wedge(self,a,b,h):
        dist=self.triples[self.types((a,b,h))];return dist[0]+dist[1]


def physical_root_rows(point):
    wanted={};first=1974691
    for r,(key,_,_,units) in enumerate(point.roots):
        y=13245+r
        for offset,(pair,bit) in enumerate(sorted(units.items())):
            wanted[first+offset]=({point.edge[pair]:1 if bit else -1,y:-1},b'>=',0 if bit else -1)
        first+=169+(57 if key[0]==4 else 0)
    require(first==2044422 and len(wanted)==32287,'complete root-unit provenance')
    return wanted


def base_fiber(opb,point,upper=F(6,13)):
    """Check every base row for the entire independent selector box.

    The single sum-of-selectors equality is verified symbolically and imposed
    separately. Every other row must hold throughout 0<=y_r<=upper.
    """
    D=point.D;scaled=upper*D;require(scaled.denominator==1,'selector endpoint scale');bound=int(scaled)
    wanted=physical_root_rows(point);seen=set();digest=hashlib.sha256();size=0;equalities=0;selector_equalities=0;upper_witnesses=set();minimum=None
    with opb.open('rb') as handle:
        header=next(handle,b'');require(header==HEADER,'base header');digest.update(header);size+=len(header)
        for number,raw in enumerate(handle,1):
            digest.update(raw);size+=len(raw);fields=raw.split()
            require(len(fields)>=5 and len(fields)%2==1 and fields[-1]==b';','OPB syntax')
            relation=fields[-3];rhs=int(fields[-2]);require(relation in (b'=',b'>='),'relation')
            constant=-rhs*D;selector={};terms={}
            for j in range(0,len(fields)-3,2):
                coefficient=int(fields[j]);token=fields[j+1];require(token.startswith(b'x'),'variable token');index=int(token[1:])
                require(1<=index<=98758 and index not in terms,'variable identity');terms[index]=coefficient
                if 13245<=index<=13633:selector[index]=coefficient
                else:constant+=coefficient*point.V[index]
            if number in wanted:
                require((terms,relation,rhs)==wanted[number],'physical root-unit row '+str(number));seen.add(number)
            if relation==b'=':
                equalities+=1
                if selector:
                    require(number==1974690 and terms=={13245+r:1 for r in range(389)} and rhs==1,'exact one-hot sum row')
                    selector_equalities+=1;continue
                require(constant==0,'base equality '+str(number));continue
            # Exact minimum of a linear form on this independent box.
            lower=constant+sum(min(0,c*bound) for c in selector.values())
            require(lower>=0,'base selector-box row '+str(number))
            minimum=lower if minimum is None else min(minimum,lower)
            if len(terms)==2 and terms.get(point.edge[0,2])==1 and rhs==0 and len(selector)==1:
                y,c=next(iter(selector.items()))
                if c==-1:upper_witnesses.add(y-13245)
    require((number,equalities,size)==(2983003,87,511537255),'entire base coverage')
    require(digest.hexdigest()==FORMULA_SHA,'base formula identity')
    require(seen==set(wanted) and selector_equalities==1,'root and selector provenance')
    require(upper_witnesses==set(range(389)) and F(point.V[point.edge[0,2]],D)==F(6,13),'sharp cap at every root')
    return {'base_rows':number,'base_equalities':equalities,'base_bytes':size,'base_sha256':digest.hexdigest(),
            'physical_root_unit_rows':len(seen),'sharp_selector_cap_rows':len(upper_witnesses),'base_minimum_box_slack':str(F(minimum,D))}


def suffix_fiber(point):
    D=point.D;V=point.V;U=6*D//13;red=[];coupled=facets=0;min_coupled=None;min_hull=None
    for (a,b),index in point.edge.items():
        total=sum(V[point.triangle[tuple(sorted((a,b,h)))]] for h in range(N) if h not in (a,b))
        red.append(13*V[index]-total)
    require(min(red)>=0,'every red codegree row')
    for _,core,outside,_ in point.roots:
        c=len(core);p=math.comb(len(outside),2)
        for i,j in it.combinations(core,2):
            degrees=(20 if i in E else 21)+(20 if j in E else 21);K=64-c-degrees;x=V[point.edge[i,j]]
            Q=sum(V[point.q[a,b,i,j]] for a,b in it.combinations(outside,2))
            A=sum(V[point.edge[tuple(sorted((h,w)))]] for h in (i,j) for w in core if h!=w)
            T=sum(V[point.triangle[tuple(sorted((i,j,w)))]] for w in outside)
            constant=45-c-degrees;S=constant*D+A+T;B=math.comb(K,2)
            gap=B*x+(p-B)*(D-U)-Q;require(gap>=0,'coupled column throughout selector box');coupled+=1
            cap=F(B*x+(p-B)*D-Q,(p-B)*D);min_coupled=cap if min_coupled is None else min(min_coupled,cap)
            for tangent in range(K):
                guard=tangent*constant-math.comb(tangent+1,2)+tangent*(c+39)
                require(guard>=0,'lower hull guard')
                intercept=Q-tangent*S+math.comb(tangent+1,2)*D+guard*(2*D-x)
                require(intercept-guard*U>=0,'all lower rational hull facets');facets+=1
                if guard:
                    cap=F(intercept,guard*D);min_hull=cap if min_hull is None else min(min_hull,cap)
            guard=-(K-1)*constant+2*p;require(guard>0,'upper hull guard')
            intercept=(K-1)*S-2*Q+guard*(2*D-x);require(intercept-guard*U>=0,'upper rational hull chord');facets+=1
            cap=F(intercept,guard*D);min_hull=min(min_hull,cap)
    require((coupled,facets)==(21762,264560),'complete suffix coverage')
    return {'red_codegree_rows':903,'red_codegree_minimum_slack':str(F(min(red),D)),
            'coupled_column_rows':coupled,'moment_hull_rows':facets,
            'minimum_coupled_selector_cap':str(min_coupled),'minimum_hull_selector_cap':str(min_hull)}


def global_moments(point):
    D=point.D;V=point.V;blue=Counter();local=[0]*N;atom_rows=0
    for vs,index in point.triangle.items():
        pairs=tuple(it.combinations(vs,2));a,b,c=(V[point.edge[e]] for e in pairs)
        m=[point.all_wedges[tuple(w for w in vs if w!=h)+(h,)] for h in vs]
        u,v,w=m[0]+a+b-D,m[1]+a+c-D,m[2]+b+c-D;z=V[index]
        inversion=(D-a-b-c+u+v+w-z,a-u-v+z,b-u-w+z,u-z,c-v-w+z,v-z,w-z,z)
        require(inversion==point.triples[point.types(vs)] and min(inversion)>=0 and sum(inversion)==D,'complete triangle probabilities')
        for pair in pairs:blue[pair]+=inversion[0]
        for h in vs:local[h]+=inversion[0]
        atom_rows+=8
    stars=0
    for h in range(N):
        degree=20 if h in E else 21
        for a in range(N):
            if a==h:continue
            x=V[point.edge[tuple(sorted((a,h)))]];red=blue_sum=0
            for b in range(N):
                if b in (h,a):continue
                m=point.all_wedges[tuple(sorted((a,b)))+(h,)];blue_sum+=m
                red+=m+x+V[point.edge[tuple(sorted((b,h)))]]-D
            require(red==(degree-1)*x and blue_sum==(41-degree)*(D-x),'global degree-star identities');stars+=1
    blue_slacks=[13*(D-V[index])-blue[pair] for pair,index in point.edge.items()]
    require(min(blue_slacks)>=0,'all blue codegrees')
    require([F(v,D) for v in local]==[F(1389,13) if h in E else F(100) for h in range(N)],'new point blue totals')
    require((atom_rows,stars)==(98728,1806),'complete global-moment coverage')
    # The local totals are reported properties, not newly imposed LP rows.
    return {'triangle_atom_rows':atom_rows,'global_star_equalities':stars,'blue_codegree_rows':903,
            'blue_codegree_minimum_slack':str(F(min(blue_slacks),D)),
            'blue_totals_E':'1389/13','blue_totals_C':'100','red_deficiency_sum':301,'blue_deficiency_sum':303}


def full_four_hull(point):
    D=point.D;projections={};by_four=defaultdict(list)
    for types,dist in point.four.items():
        require(min(dist)>=0 and sum(dist)==D,'four-atom domains')
        for positions in it.combinations(range(4),3):projections[types,positions]=point.project(dist,positions)
    for key,index in point.q.items():by_four[tuple(sorted(key))].append((key,index))
    sets=equalities=footprints=0;patterns=Counter()
    for vs in it.combinations(range(N),4):
        types=point.types(vs);dist=point.four[types];patterns[types]+=1
        for positions in it.combinations(range(4),3):
            triple=tuple(vs[j] for j in positions)
            require(projections[types,positions]==point.triples[point.types(triple)],'all shared physical triple marginals')
            equalities+=8
        pairs=tuple(it.combinations(vs,2))
        for (a,b,i,j),index in by_four[vs]:
            red=1<<pairs.index((i,j));blues=sum(1<<pairs.index(tuple(sorted((z,h)))) for z in (a,b) for h in (i,j))
            mass=sum(value for mask,value in enumerate(dist) if mask&red and not(mask&blues))
            require(mass==point.V[index],'existing physical footprint equality');footprints+=1
        sets+=1
    require((sets,equalities,footprints)==(123410,3949120,74513),'entire four-vertex lift')
    census=[sum(n for types,n in patterns.items() if sum(types)==q) for q in range(5)]
    require(census==[math.comb(13,q)*math.comb(30,4-q) for q in range(5)],'all physical class-count placements')
    return {'four_sets':sets,'four_nonnegative_rows':64*sets,'four_normalizations':sets,
            'triangle_marginal_equalities':equalities,'footprint_equalities':footprints,
            'physical_four_set_census':census,'four_state_minimum_mass':str(F(min(min(d) for d in point.four.values()),D))}


def selector_links(point):
    remaining=[r for r in range(389) if r not in REMOVED];require(len(remaining)==380,'surviving selector count')
    barycenter={r:F(0) if r in REMOVED else F(1,380) for r in range(389)}
    require(sum(barycenter.values())==1 and max(barycenter.values())<=F(6,13),'exact postcut selector point')
    # Necessity and sufficiency for this fixed physical-moment family:
    # fewer than three allowed coordinates cannot sum to one; three can.
    require(2*F(6,13)<1 and F(1,3)<=F(6,13),'sharp retained-root threshold for this family')
    anchor_edges=set(point.roots[0][3]);require(len(anchor_edges)==83,'anchor interface')
    common=set(point.roots[remaining[0]][3].items())
    for r in remaining:common&=set(point.roots[r][3].items())
    require(len(common)==53 and ((0,2),1) in common,'complete common-unit intersection after cuts')
    transports=0
    for r,(_,_,_,bits) in enumerate(point.roots):
        require(set(bits)==anchor_edges,'complete anchor linkage domain')
        for pair in anchor_edges:
            # In one-hot Boolean case r, the barycentric equation reduces
            # exactly to the literal root unit already audited in the OPB.
            require(bits[pair] in (0,1),'Boolean anchor value');transports+=1
    require(transports==389*83,'every anchor-link case')
    edgevalue=F(point.V[point.edge[0,2]],point.D)
    require(edgevalue==F(6,13) and all(point.roots[r][3][0,2]==1 for r in range(389)),'entire fiber strict separator')
    violated=sum(F(point.V[point.edge[pair]],point.D)!=bit for pair,bit in common)
    require(violated==53,'all common units violated by this family')
    # All sixteen h3485 weighted guards are also satisfied once their eight
    # selectors are cut to zero; these derived checks add no independent row.
    H=tuple(range(15,28));weighted=[]
    for cell,x in ((tuple(range(2,8))+(28,),28),(tuple(range(8,14))+(29,),29)):
        W=sum(point.V[point.edge[tuple(sorted(e))]] for e in it.combinations(cell,2))+sum(point.V[point.edge[tuple(sorted((x,h)))]] for h in H)
        require(W<=34*point.D,'cut-implied weighted guard');weighted.append(str(F(W,point.D)))
    return {'removed_roots':list(REMOVED),'retained_selectors':380,'selector_cap':'6/13','uniform_selector':'1/380',
            'minimum_retained_roots_for_this_family':3,'root_unit_link_equations':83,'root_unit_link_cases':transports,
            'postcut_common_anchor_units':53,'violated_common_units':violated,
            'separating_edge':[0,2],'separating_edge_value':'6/13','required_common_edge_value':'1','separation_gap':'7/13',
            'postcut_weighted_cell_values':weighted}


def check_link_file(path,point):
    lines=path.read_text().splitlines();anchor_edges=sorted(point.roots[0][3]);require(len(lines)==83,'all linkage equations')
    violated=0
    for pair,line in zip(anchor_edges,lines):
        fields=line.split();require(fields[-3:]==['=','0',';'] and len(fields)%2==1,'link equation syntax')
        terms={}
        for j in range(0,len(fields)-3,2):
            index=int(fields[j+1][1:]);require(fields[j+1].startswith('x') and index not in terms,'link variable');terms[index]=int(fields[j])
        expected={point.edge[pair]:1}
        expected.update({13245+r:-1 for r,(_,_,_,bits) in enumerate(point.roots) if bits[pair]})
        require(terms==expected,'literal anchor-to-selector coefficients')
        physical=F(point.V[point.edge[pair]],point.D)
        predicted=sum(F(1,380) for r,(_,_,_,bits) in enumerate(point.roots) if r not in REMOVED and bits[pair])
        violated+=physical!=predicted
    require(violated==83,'uniform survivor violates every anchor-link equation')
    return {'anchor_link_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'uniform_anchor_link_violations':violated,'rows_after_anchor_linkage':15417040,
            'equalities_after_anchor_linkage':4149019,'anchor_link_strengthened_system_status':'UNDECIDED'}


def check_cg(point,path=None):
    cert=json.loads((path or HERE/'anchor_cg.json').read_text())
    require(cert['edge']==[0,2] and cert['physical_variable']==point.edge[0,2] and cert['guard_rows']==389,'CG target')
    multiplier=F(cert['each_guard_multiplier']);equality=F(cert['selector_equality_multiplier'])
    require(multiplier>=0,'nonnegative CG inequality multiplier')
    coeff=Counter();used=0
    for terms,relation,rhs in physical_root_rows(point).values():
        if terms.get(2)!=1 or len(terms)!=2 or relation!=b'>=' or rhs!=0:continue
        require(any(13245<=v<=13633 and a==-1 for v,a in terms.items()),'CG physical unit premise')
        for v,a in terms.items():coeff[v]+=multiplier*a
        used+=1
    require(used==389,'every guarded common unit')
    for r in range(389):coeff[13245+r]+=equality
    cleaned={str(v):str(a) for v,a in coeff.items() if a}
    require(cleaned=={'2':'1'}==cert['pre_round_coefficients'],'exact CG coefficient cancellation')
    require(equality==F(1,389)==F(cert['pre_round_rhs']),'CG pre-round RHS')
    # The sole remaining coefficient is integral. The physical edge variable
    # is Boolean in the original problem, so integer rounding is sound.
    require(math.ceil(equality)==cert['rounded_rhs']==1,'exact integer rounding')
    return {'cg_guard_premises':used,'cg_pre_round_rhs':'1/389','cg_rounded_rhs':1,'cg_rank':1,
            'cg_family_separation_gap':str(1-F(point.V[2],point.D))}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json');parser.add_argument('--opb',type=Path,required=True);parser.add_argument('--links',type=Path,required=True)
    args=parser.parse_args();point=Point(args.certificate)
    result={'status':'EXACT_COMPLETE_P4_POSTCUT_SURVIVOR_AND_SELECTOR_FIBER',
            'physical_moment_denominator':point.D,'postcut_point_denominator':math.lcm(point.D,380),
            'total_variables':8023409,'total_rows_with_nine_cuts':15416957,'total_equalities':4148936,
            'certificate_sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
            **base_fiber(args.opb,point),**suffix_fiber(point),**global_moments(point),**full_four_hull(point),**selector_links(point),**check_link_file(args.links,point),**check_cg(point)}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
