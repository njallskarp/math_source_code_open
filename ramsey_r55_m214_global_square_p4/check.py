#!/usr/bin/env python3
"""Exact complete Q+G point and a universal cut-square separator."""
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
    def __init__(self,path):
        raw=json.loads(path.read_text());require(set(raw)=={'format','denominator','cells','active_selectors','four_tables'} and raw['format']=='class-state-orbits-v1','certificate schema');self.D=raw['denominator'];require(type(self.D)==int and self.D>0,'integer scale')
        self.cells=raw['cells'];require(self.cells and all(isinstance(vs,list) and vs and all(type(v)==int for v in vs) for vs in self.cells),'cell schema');flat=sum(self.cells,[]);require(sorted(flat)==list(range(N)) and len(flat)==N,'complete vertex partition')
        self.classes={v:t for t,vs in enumerate(self.cells) for v in vs}
        require(all(all((v in E)==(vs[0] in E) for v in vs) for vs in self.cells),'degree homogeneous cell')
        self.exceptional_types={t for t,vs in enumerate(self.cells) if vs[0] in E};sizes=list(map(len,self.cells))
        base={}
        for row in raw['four_tables']:
            require(set(row)=={'types','orbits'},'table fields');types=tuple(row['types']);require(len(types)==4 and all(type(t)==int and 0<=t<len(sizes) for t in types) and tuple(sorted(types))==types and types not in base,'four types')
            dist=[0]*64
            perms=[perm for perm in it.permutations(range(4)) if tuple(types[j] for j in perm)==types];seen=set()
            for key,value in row['orbits'].items():
                state=int(key);require(str(state)==key and 0<=state<64 and type(value)==int and 0<value<=self.D,'orbit mass')
                orbit={sum((state>>PAIRS4.index(tuple(sorted((perm[a],perm[b]))))&1)<<j for j,(a,b) in enumerate(PAIRS4)) for perm in perms}
                require(state==min(orbit) and not(seen&orbit),'canonical orbit');seen.update(orbit)
                for mask in orbit:dist[mask]=value
            require(sum(dist)==self.D,'normalization');base[types]=tuple(dist)
        expected={ts for ts in it.combinations_with_replacement(range(len(sizes)),4) if all(ts.count(t)<=sizes[t] for t in ts)}
        require(set(base)==expected,'complete type support')
        self.four={}
        for canonical,dist in base.items():
            for types in set(it.permutations(canonical)):
                order=tuple(sorted(range(4),key=lambda j:types[j]));out=[]
                for mask in range(64):
                    state=0
                    for j,(a,b) in enumerate(PAIRS4):
                        physical=PAIRS4.index(tuple(sorted((order[a],order[b]))));state|=(mask>>physical&1)<<j
                    out.append(dist[state])
                self.four[types]=tuple(out)
        self.triples={}
        for ts in it.product(range(len(sizes)),repeat=3):
            if any(ts.count(t)>sizes[t] for t in ts):continue
            extra=next(t for t in range(len(sizes)) if ts.count(t)<sizes[t])
            self.triples[ts]=self.project(self.four[ts+(extra,)],(0,1,2))
        self.edges={}
        for ts in it.product(range(len(sizes)),repeat=2):
            if any(ts.count(t)>sizes[t] for t in ts):continue
            extra=next(t for t in range(len(sizes)) if ts.count(t)<sizes[t])
            self.edges[ts]=sum(m for s,m in enumerate(self.triples[ts+(extra,)]) if s&1)
        self.edge,self.triangle,self.roots,self.missed,self.q=geometry();self.V=[0]*98759;defined=set()
        def set_value(index,value):
            require(index not in defined and 0<=value<=self.D,'coordinate box/uniqueness');defined.add(index);self.V[index]=value
        for pair,index in self.edge.items():set_value(index,self.edges[self.types(pair)])
        for vs,index in self.triangle.items():set_value(index,self.triples[self.types(vs)][7])
        active=raw['active_selectors'];require(active==sorted(set(active)) and active and all(type(r)==int and 0<=r<389 for r in active),'selector support')
        require(self.D%len(active)==0,'selector scale')
        for r in range(389):set_value(13245+r,self.D//len(active) if r in active else 0)
        for key,index in self.missed.items():set_value(index,self.wedge(*key))
        for key,index in self.q.items():
            dist=self.four[self.types(key)];set_value(index,dist[32]+dist[33])
        require(defined==set(range(1,98759)),'complete coordinate decoder')
        self.all_wedges={(a,b,h):self.wedge(a,b,h) for a,b in it.combinations(range(N),2) for h in range(N) if h not in (a,b)}
        require(len(self.all_wedges)==37023 and all(0<=v<=self.D for v in self.all_wedges.values()),'all wedge boxes')

    def types(self,vs):return tuple(self.classes[v] for v in vs)

    @staticmethod
    def project(dist,positions):
        bits=[PAIRS4.index(pair) for pair in it.combinations(positions,2)];result=[0]*8
        for state,mass in enumerate(dist):result[sum((state>>bit&1)<<j for j,bit in enumerate(bits))]+=mass
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


def base_point(opb,point):
    D=point.D;wanted=physical_root_rows(point);wanted.update(forbidden_source_rows(point));seen=set();digest=hashlib.sha256();size=0;equalities=0;minimum=None
    for h in range(N):
        wanted[1974561+h]=({point.edge[tuple(sorted((h,w)))]:1 for w in range(N) if w!=h},b'=',20 if h in E else 21)
        wanted[1974604+h]=({point.triangle[tuple(sorted((h,u,v)))]:1 for u,v in it.combinations([v for v in range(N) if v!=h],2)},b'=',93 if h in E else 100)
    with opb.open('rb') as handle:
        header=next(handle,b'');require(header==HEADER,'base header');digest.update(header);size+=len(header)
        for number,raw in enumerate(handle,1):
            digest.update(raw);size+=len(raw);fields=raw.split();require(len(fields)>=5 and len(fields)%2==1 and fields[-1]==b';','OPB syntax')
            relation=fields[-3];rhs=int(fields[-2]);require(relation in (b'=',b'>='),'relation');constant=-rhs*D;terms={}
            for j in range(0,len(fields)-3,2):
                coefficient=int(fields[j]);token=fields[j+1];require(token.startswith(b'x'),'variable');index=int(token[1:]);require(1<=index<=98758 and index not in terms,'variable identity');terms[index]=coefficient;constant+=coefficient*point.V[index]
            if number in wanted:require((terms,relation,rhs)==wanted[number],'root unit '+str(number));seen.add(number)
            if relation==b'=':equalities+=1;require(constant==0,'base equality '+str(number))
            else:require(constant>=0,'base inequality '+str(number));minimum=constant if minimum is None else min(minimum,constant)
    require((number,equalities,size)==(2983003,87,511537255),'entire base coverage');require(digest.hexdigest()==FORMULA_SHA,'formula identity');require(seen==set(wanted),'all anchor units')
    return {'base_rows':number,'base_equalities':equalities,'base_bytes':size,'base_sha256':digest.hexdigest(),'physical_root_unit_rows':32287,'physical_five_clause_rows':11970,'physical_degree_source_rows':43,'physical_triangle_source_rows':43,'total_semantic_source_rows':len(seen),'minimum_base_slack':str(F(minimum,D))}


def suffix_rows(point):
    D=point.D;V=point.V;red=[];coupled=facets=0;min_coupled=None;min_hull=None
    for (a,b),index in point.edge.items():
        total=sum(V[point.triangle[tuple(sorted((a,b,h)))]] for h in range(N) if h not in (a,b))
        red.append(13*V[index]-total)
    require(min(red)>=0,'every red codegree row')
    for r,(_,core,outside,_) in enumerate(point.roots):
        U=V[13245+r]
        c=len(core);p=math.comb(len(outside),2)
        for i,j in it.combinations(core,2):
            degrees=(20 if i in E else 21)+(20 if j in E else 21);K=64-c-degrees;x=V[point.edge[i,j]]
            Q=sum(V[point.q[a,b,i,j]] for a,b in it.combinations(outside,2))
            A=sum(V[point.edge[tuple(sorted((h,w)))]] for h in (i,j) for w in core if h!=w)
            T=sum(V[point.triangle[tuple(sorted((i,j,w)))]] for w in outside)
            constant=45-c-degrees;S=constant*D+A+T;B=math.comb(K,2)
            gap=B*x+(p-B)*(D-U)-Q;require(gap>=0,'physical coupled column');coupled+=1
            min_coupled=gap if min_coupled is None else min(min_coupled,gap)
            for tangent in range(K):
                guard=tangent*constant-math.comb(tangent+1,2)+tangent*(c+39)
                require(guard>=0,'lower hull guard')
                intercept=Q-tangent*S+math.comb(tangent+1,2)*D+guard*(2*D-x)
                gap=intercept-guard*U;require(gap>=0,'physical lower rational hull facet');facets+=1
                min_hull=gap if min_hull is None else min(min_hull,gap)
            guard=-(K-1)*constant+2*p;require(guard>0,'upper hull guard')
            intercept=(K-1)*S-2*Q+guard*(2*D-x);require(intercept-guard*U>=0,'physical upper rational hull chord');facets+=1
            min_hull=min(min_hull,intercept-guard*U)
    require((coupled,facets)==(21762,264560),'complete suffix coverage')
    return {'red_codegree_rows':903,'red_codegree_minimum_slack':str(F(min(red),D)),
            'coupled_column_rows':coupled,'moment_hull_rows':facets,
            'minimum_coupled_slack':str(F(min_coupled,D)),'minimum_hull_slack':str(F(min_hull,D))}


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
    require(all(local[h]<=(107 if h in E else 100)*D for h in range(N)),'all blue hard caps')
    require(sum((114 if h in E else 107)*D-local[h] for h in range(N))==303*D,'blue deficiency sum')
    require((atom_rows,stars)==(98728,1806),'complete global-moment coverage')
    # The local totals are reported properties, not newly imposed LP rows.
    return {'triangle_atom_rows':atom_rows,'global_star_equalities':stars,'blue_codegree_rows':903,
            'blue_codegree_minimum_slack':str(F(min(blue_slacks),D)),
            'blue_totals':list(map(lambda v:str(F(v,D)),local)),'red_deficiency_sum':301,'blue_deficiency_sum':303}


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
    census=[sum(n for types,n in patterns.items() if sum(t in point.exceptional_types for t in types)==q) for q in range(5)]
    require(census==[math.comb(13,q)*math.comb(30,4-q) for q in range(5)],'all physical class-count placements')
    return {'four_sets':sets,'four_nonnegative_rows':64*sets,'four_normalizations':sets,
            'triangle_marginal_equalities':equalities,'footprint_equalities':footprints,
            'physical_four_set_census':census,'four_state_minimum_mass':str(F(min(min(d) for d in point.four.values()),D))}


def check_links(point,path):
    D=point.D;V=point.V;require(sum(V[13245:13634])==D,'selector sum');require(all(V[13245+r]==0 for r in REMOVED),'nine cuts')
    lines=path.read_text().splitlines();anchor_edges=sorted(point.roots[0][3]);require(len(lines)==83,'all anchor links')
    for pair,line in zip(anchor_edges,lines):
        fields=line.split();require(fields[-3:]==['=','0',';'] and len(fields)%2==1,'link syntax');terms={}
        for j in range(0,len(fields)-3,2):
            index=int(fields[j+1][1:]);require(fields[j+1].startswith('x') and index not in terms,'link variable');terms[index]=int(fields[j])
        expected={point.edge[pair]:1};expected.update({13245+r:-1 for r,(_,_,_,bits) in enumerate(point.roots) if bits[pair]});require(terms==expected,'link physical coefficients')
        require(sum(a*V[i] for i,a in terms.items())==0,'anchor linkage '+str(pair))
    return {'anchor_link_equations':83,'anchor_link_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'nonzero_selectors':[r for r in range(389) if V[13245+r]],'selector_values':[str(F(V[13245+r],D)) for r in range(389) if V[13245+r]]}


def rank_subset(vs,n):
    require(tuple(sorted(set(vs)))==vs and all(0<=v<n for v in vs),'ranked physical subset')
    rank=0;previous=-1;k=len(vs)
    for i,v in enumerate(vs):
        rank+=sum(math.comb(n-j-1,k-i-1) for j in range(previous+1,v));previous=v
    return rank


def forbidden_family(point):
    units=point.roots[0][3];common={pair:bit for pair,bit in units.items() if 0 in pair}
    require(len(common)==42 and all(all(bits[pair]==bit for pair,bit in common.items()) for _,_,_,bits in point.roots),'all roots share anchor-zero star')
    rows=[]
    for color in (0,1):
        neighbors=[v for v in range(1,N) if common[0,v]==color];require(len(neighbors)==21,'both anchor neighborhoods')
        for vs in it.combinations(neighbors,4):
            state=63 if color else 0
            variable=125170+64*rank_subset(vs,N)+state
            source=2*rank_subset((0,)+vs,N)+(2 if color else 1)
            rows.append((color,vs,state,variable,source))
    require(len(rows)==11970 and len({row[3] for row in rows})==11970,'complete forbidden-state family')
    return rows


def forbidden_source_rows(point):
    wanted={}
    for color,vs,state,variable,source in forbidden_family(point):
        terms={point.edge[pair]:-1 if color else 1 for pair in it.combinations((0,)+vs,2)}
        wanted[source]=(terms,b'>=',-9 if color else 1)
    require(len(wanted)==11970,'all source five clauses distinct')
    return wanted


def check_forbidden_file(path,point):
    family=forbidden_family(point);lines=path.read_text().splitlines();require(len(lines)==len(family),'complete forbidden file')
    violations=Counter();target=None
    for (color,vs,state,variable,source),line in zip(family,lines):
        require(line==f'-1 x{variable} >= 0 ;','literal forbidden-state row')
        mass=point.four[point.types(vs)][state]
        if mass:violations[color]+=1
        if color==0 and vs==(39,40,41,42):target=F(mass,point.D)
    require(target == 0,'old separating mass is now zero')
    require((violations[0],violations[1])==(0,0),'complete forbidden-state satisfaction')
    return {'forbidden_state_rows':11970,'forbidden_state_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'violated_blue_forbidden_states':violations[0],'violated_red_forbidden_states':violations[1],
            'old_separating_anchor':0,'old_separating_four':[39,40,41,42],'old_separating_blue_mass':str(target),
            'anchor_zero_subsystem_compressed_rows':15417041,'forbidden_sum':'0'}


def star_slacks(point,h,vs):
    require(h not in vs and len(set(vs))==4,'physical star support')
    dist=point.four[point.types(vs)]
    red_sum=sum(point.V[point.edge[tuple(sorted((h,v)))]] for v in vs)
    return red_sum-dist[0],4*point.D-red_sum-dist[63]


def global_star_rows(point):
    # Literal physical enumeration, independent of discovery class quotienting.
    # For each A and h outside A: p[A,blue] <= sum x[h,v], and
    # p[A,red] + sum x[h,v] <= 4. All variables already belong to P4.
    count=0;minimum=None;tight=[0,0];by_anchor=[0]*N
    for vs in it.combinations(range(N),4):
        for h in range(N):
            if h in vs:continue
            gaps=star_slacks(point,h,vs)
            require(min(gaps)>=0,'global star-event row '+str((h,vs)))
            if minimum is None or min(gaps)<minimum:minimum=min(gaps)
            for color,gap in enumerate(gaps):tight[color]+=int(gap==0)
            by_anchor[h]+=2;count+=2
    require(count==2*N*math.comb(N-1,4)==9625980,'all global star rows')
    require(by_anchor==[223860]*N,'complete per-anchor star coverage')
    return {'global_star_rows':count,'global_star_rows_per_anchor':by_anchor,
            'global_star_minimum_slack':str(F(minimum,point.D)),
            'global_star_tight_blue_rows':tight[0],'global_star_tight_red_rows':tight[1],
            'total_rows_without_redundant_anchor_zero_rows':25365693}


def conditioned_degrees(point,path):
    # Precompute exact four-event probabilities; then sum over every physical
    # outside vertex, without quotienting any physical identity.
    events={}
    for types,dist in point.four.items():
        for pos,bit in enumerate((2,4,5)):
            out=[0]*8
            for state,mass in enumerate(dist):
                if state>>bit&1:
                    triple=(state&1)+2*(state>>1&1)+4*(state>>3&1)
                    out[triple]+=mass
            events[types,pos]=tuple(out)
    total=violated=0;witness=None
    pair3=tuple(it.combinations(range(3),2))
    for A in it.combinations(range(N),3):
        types=point.types(A);tri=point.triples[types];outside=[v for v in range(N) if v not in A]
        for pos,h in enumerate(A):
            lhs=[0]*8
            for w in outside:
                event=events[types+(point.classes[w],),pos]
                for state in range(8):lhs[state]+=event[state]
            for state in range(8):
                local=sum(state>>j&1 for j,e in enumerate(pair3) if pos in e)
                gap=lhs[state]-((20 if h in E else 21)-local)*tri[state]
                total+=1;violated+=int(gap!=0)
                if (A,h,state)==((14,27,29),27,0):witness=(lhs[state],tri[state],gap)
    require((total,violated)==(296184,0),'complete conditioned-degree census')
    require(witness is not None and witness[2]==0,'all global degree identities satisfied')
    # Reconstruct the one emitted row by polynomial coefficient accumulation
    # on each sorted physical four-set, using binomial coordinate ranks.
    A=(14,27,29);h=27;state=0;b=0;expected=Counter();values={}
    for w in range(N):
        if w in A:continue
        Q=tuple(sorted(A+(w,)));pairs=tuple(it.combinations(Q,2));base=125170+64*rank_subset(Q,N)
        for s in range(64):
            bits={pair:s>>j&1 for j,pair in enumerate(pairs)}
            event=int(all(bits[e]==0 for e in it.combinations(A,2)))
            coefficient=event*(bits[tuple(sorted((h,w)))]-21*int(w==b))
            expected[base+s]+=coefficient;values[base+s]=point.four[point.types(Q)][s]
    expected={i:c for i,c in expected.items() if c}
    fields=path.read_text().split();require(fields[-3:]==['=','0',';'] and len(fields)%2==1,'conditioned-degree row syntax')
    actual={}
    for j in range(0,len(fields)-3,2):
        token=fields[j+1];require(token.startswith('x'),'conditioned-degree variable');i=int(token[1:]);require(i not in actual,'duplicate conditioned-degree term');actual[i]=int(fields[j])
    require(actual==expected,'literal conditioned-degree separator coefficients')
    require(sum(c*values[i] for i,c in actual.items())==witness[2],'literal separator value')
    return {'conditioned_degree_family_rows':total,'violated_conditioned_degree_rows':violated,
            'former_separator_triple':list(A),'former_separator_center':h,'former_separator_state':state,
            'former_separator_triple_mass':str(F(witness[1],point.D)),'former_separator_lhs':str(F(witness[0],point.D)),
            'former_separator_rhs':str(F(21*witness[1],point.D)),'former_separator_gap':str(F(witness[2],point.D)),
            'conditioned_degree_maximum_absolute_gap':'0','former_separator_terms':len(actual),
            'former_separator_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'conditioned_degree_system_status':'EXACT_FEASIBLE'}


def triangle_rows(point):
    # Every physical triangle and outside vertex, both colors.  No quotient
    # of physical row coverage is used by this checker.
    caps=0;minimum=None
    for A in it.combinations(range(N),3):
        types=point.types(A)
        for color in (0,1):
            lhs=sum(point.four[types+(point.classes[w],)][63 if color else 0]
                    for w in range(N) if w not in A)
            slack=4*point.triples[types][7 if color else 0]-lhs
            require(slack>=0,'triangle common-neighbor cap '+str((A,color)))
            minimum=slack if minimum is None else min(minimum,slack);caps+=1
    # In the order (h,a,u,v), bits 0,1,2,5 are ha,hu,hv,uv.
    joint={types:sum(m for s,m in enumerate(dist) if s&39==39)
           for types,dist in point.four.items()}
    identities=0
    for h in range(N):
        others=[v for v in range(N) if v!=h]
        for a in others:
            lhs=0
            for u,v in it.combinations(others,2):
                if a in (u,v):lhs+=point.triples[point.types((h,u,v))][7]
                else:lhs+=joint[point.types((h,a,u,v))]
            rhs=(93 if h in E else 100)*point.V[point.edge[tuple(sorted((h,a)))]]
            require(lhs==rhs,'edge-conditioned red triangle total '+str((h,a)));identities+=1
    require((caps,identities)==(24682,1806),'complete triangle-family coverage')
    return {'triangle_common_neighbor_rows':caps,'triangle_common_neighbor_minimum_slack':str(F(minimum,point.D)),
            'edge_conditioned_triangle_rows':identities,'edge_conditioned_triangle_maximum_gap':'0'}


def deficiency_bound(point,path):
    # The complete existing P3 blue-wedge numbering: retain inherited names,
    # append exactly the missing triples in lexicographic endpoint order.
    names=dict(point.missed);next_name=98759
    for key in sorted(point.all_wedges):
        if key not in names:names[key]=next_name;next_name+=1
    require(next_name==125170,'global P3 variable support')
    coefficients=Counter();constant=0;sum_a=sum_a2=0
    for h in range(N):
        neighbors=sorted(E-{h});mean=sum(point.V[point.edge[tuple(sorted((h,u)))]] for u in neighbors)
        square=mean
        for u in neighbors:coefficients[point.edge[tuple(sorted((h,u)))]]+=1
        for u,v in it.combinations(neighbors,2):
            wedge=point.all_wedges[u,v,h]
            square+=2*(wedge+point.V[point.edge[tuple(sorted((h,u)))]]+point.V[point.edge[tuple(sorted((h,v)))]]-point.D)
            coefficients[names[u,v,h]]+=2
            coefficients[point.edge[tuple(sorted((h,u)))]]+=2
            coefficients[point.edge[tuple(sorted((h,v)))]]+=2
            constant-=2
        sum_a+=mean;sum_a2+=square
    require(sum_a==260*point.D,'global first moment')
    # Independent Boolean upper bound: a=6+epsilon, epsilon>=0 integral,
    # sum epsilon=2 implies sum a^2<=1576. Linear form uses existing m,x.
    expected={i:-c for i,c in coefficients.items() if c};rhs=constant-1576
    fields=path.read_text().split();require(fields[-3:]==['>=',str(rhs),';'],'global separator relation/RHS')
    require(len(fields)%2==1,'global separator syntax');actual={}
    for j in range(0,len(fields)-3,2):
        token=fields[j+1];require(token.startswith('x'),'global separator variable');i=int(token[1:]);require(i not in actual,'duplicate global separator variable');actual[i]=int(fields[j])
    require(actual==expected,'complete global separator coefficients')
    values=dict(enumerate(point.V));values.update({i:point.all_wedges[k] for k,i in names.items()})
    gap=sum_a2-1576*point.D
    require(sum(c*values[i] for i,c in actual.items())-rhs*point.D==-gap,'literal global separator value')
    require(gap<=0,'global deficiency upper bound')
    return {'deficiency_first_moment':'260','deficiency_second_moment':str(F(sum_a2,point.D)),
            'deficiency_second_moment_upper_bound':1576,'deficiency_upper_slack':str(F(-gap,point.D)),
            'deficiency_separator_terms':len(actual),'deficiency_separator_rhs':rhs,
            'deficiency_separator_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def cut_square(point,path):
    # Expand the square from every unordered pair of physical cut edges.
    # This is independent of the emitter's closed-form cut coefficients.
    A=tuple(range(2,15));B=tuple(range(15,27));cut=tuple((u,v) for u in A for v in B);t=72
    names=dict(point.missed);next_name=98759
    for key in sorted(point.all_wedges):
        if key not in names:names[key]=next_name;next_name+=1
    expected=Counter({point.edge[e]:1-2*t for e in cut})
    values=dict(enumerate(point.V));values.update({i:point.all_wedges[key] for key,i in names.items()})
    mean=sum(point.V[point.edge[e]] for e in cut);second=mean;constant=t*t;shared=disjoint=0
    for e,f in it.combinations(cut,2):
        common=set(e)&set(f)
        if common:
            h=next(iter(common));u,v=sorted((set(e)|set(f))-{h})
            expected[names[u,v,h]]+=2;expected[point.edge[e]]+=2;expected[point.edge[f]]+=2;constant-=2
            mass=point.all_wedges[u,v,h]+point.V[point.edge[e]]+point.V[point.edge[f]]-point.D
            shared+=1
        else:
            vs=tuple(sorted(e+f));pairs=tuple(it.combinations(vs,2));mask=(1<<pairs.index(e))|(1<<pairs.index(f));base=125170+64*rank_subset(vs,N)
            dist=point.four[point.types(vs)];mass=0
            for state,m in enumerate(dist):
                if state&mask==mask:expected[base+state]+=2;values[base+state]=m;mass+=m
            disjoint+=1
        second+=2*mass
    value=second-2*t*mean+t*t*point.D;expected={i:c for i,c in expected.items() if c}
    require((len(cut),shared,disjoint,len(expected),constant)==(156,1794,10296,146094,1596),'complete cut-square support')
    require(mean==72*point.D,'cut mean of this point')
    fields=path.read_text().split();require(fields[-3:]==['>=','-1596',';'] and len(fields)%2==1,'cut-square syntax');actual={}
    for j in range(0,len(fields)-3,2):
        token=fields[j+1];require(token.startswith('x'),'cut-square variable');i=int(token[1:]);require(i not in actual,'cut-square duplicate term');actual[i]=int(fields[j])
    require(actual==expected,'all physical cut-square coefficients')
    require(sum(c*values[i] for i,c in actual.items())+constant*point.D==value,'literal cut-square evaluation')
    require(value < -353*point.D,'strict negative square below -353')
    return {'cut_square_edges':156,'cut_square_terms':len(actual),'cut_square_shared_edge_pairs':shared,
            'cut_square_disjoint_edge_pairs':disjoint,'cut_square_constant':constant,
            'cut_mean':'72','cut_second_moment':str(F(second,point.D)),
            'cut_square_value':str(F(value,point.D)),'cut_square_strict_upper_bound':-353,
            'cut_square_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--certificate',type=Path,required=True);parser.add_argument('--opb',type=Path,required=True);parser.add_argument('--links',type=Path,required=True);parser.add_argument('--forbidden',type=Path,required=True);parser.add_argument('--degree-separator',type=Path,required=True);parser.add_argument('--deficiency-separator',type=Path,required=True);parser.add_argument('--square',type=Path,required=True);args=parser.parse_args();point=Point(args.certificate)
    result={'status':'EXACT_COMPLETE_GLOBAL_SQUARE_P4_SURVIVOR',
            'common_denominator':str(point.D),'certificate_sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
            'total_variables':8023409,'total_rows':25377663,'total_equalities':4447009,
            **check_links(point,args.links),**global_moments(point),**full_four_hull(point),**suffix_rows(point),
            **base_point(args.opb,point),**check_forbidden_file(args.forbidden,point),**global_star_rows(point),
            **conditioned_degrees(point,args.degree_separator),**triangle_rows(point),**deficiency_bound(point,args.deficiency_separator),**cut_square(point,args.square)}
    require(result['nonzero_selectors']==[278] and result['selector_values']==['1'],'integral selector root278')
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
