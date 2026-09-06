#!/usr/bin/env python3
"""Independent finite-cover, physical-row and exact arithmetic audit."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools as it
import json
import math
from pathlib import Path
from check_rup import require, rup, verify
HERE=Path(__file__).resolve().parent
REPO=HERE.parent
N=43;U,V=0,1;H=tuple(range(15,28));E=tuple(range(2,15));Z=14
A=tuple(range(2,8))+(28,);B=tuple(range(8,14))+(29,)
TABLE_SHA='f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e'
OPB_SHA='469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f'
ROOTS=(48,128,129,201,202,299,300,376)


def edge(a,b):
    a,b=sorted((a,b));require(0<=a<b<N,'physical edge')
    return a*(85-a)//2+b-a

def subset_rank(vertices,n):
    rank=0;last=-1;k=len(vertices)
    for j,v in enumerate(vertices):
        rank+=sum(math.comb(n-1-x,k-1-j) for x in range(last+1,v));last=v
    return rank

def triangle_id(t):return 904+subset_rank(t,43)

def check_stream(path,wanted):
    digest=hashlib.sha256();seen=set();count=size=0
    with path.open('rb') as f:
        header=f.readline();require(header==b'* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n','parent header')
        digest.update(header);size+=len(header)
        for count,raw in enumerate(f,1):
            digest.update(raw);size+=len(raw)
            if count not in wanted:continue
            fields=raw.decode('ascii').split();require(fields[-1]==';' and len(fields)%2==1,'OPB syntax')
            terms={int(fields[i+1][1:]):int(fields[i]) for i in range(0,len(fields)-3,2)}
            require(len(terms)==(len(fields)-3)//2,'repeated source variable')
            require((terms,fields[-3],int(fields[-2]))==wanted[count],'physical OPB row '+str(count));seen.add(count)
    require((count,size)==(2044421,172788992) and digest.hexdigest()==OPB_SHA,'entire parent identity')
    require(seen==set(wanted),'all used rows found')
    return len(seen)

def small_r34():
    pairs=tuple(it.combinations(range(9),2));rank={p:i+1 for i,p in enumerate(pairs)}
    base=[tuple(-rank[p] for p in it.combinations(t,2)) for t in it.combinations(range(9),3)]
    base += [tuple(rank[p] for p in it.combinations(t,2)) for t in it.combinations(range(9),4)]
    steps=verify(base+[(-rank[0,w],) for w in range(4,9)],HERE/'r34.rup',36)
    caps=normalizations=0;original={frozenset(c) for c in base}
    for neighbors in it.combinations(range(1,9),4):require(rup(base,tuple(-rank[0,w] for w in neighbors)),'R34 degree cap');caps+=1
    for size in range(4):
        for neighbors in it.combinations(range(1,9),size):
            order=(0,)+neighbors+tuple(sorted(set(range(1,9))-set(neighbors)))
            mapping={i+1:rank[tuple(sorted((order[a],order[b])))] for i,(a,b) in enumerate(pairs)}
            require({frozenset(mapping[abs(x)]*(1 if x>0 else -1) for x in c) for c in base}==original,'R34 permutation')
            require(all(order[w] not in neighbors for w in range(4,9)),'R34 star normalization');normalizations+=1
    require((steps,caps,normalizations)==(288,70,93),'complete R34 audit')
    return steps


def equality_cover():
    # Every graph on six vertices is examined; the extremizers are exactly
    # the complements of the 15 perfect matchings. No extremizer is sampled.
    pairs=tuple(it.combinations(range(6),2))
    k4=[sum(1<<pairs.index(e) for e in it.combinations(q,2)) for q in it.combinations(range(6),4)]
    equality=[]
    for bits in range(1<<15):
        if any(bits&m==m for m in k4):continue
        require(bits.bit_count()<=12,'Turan6 bound')
        if bits.bit_count()==12:
            missing=[e for j,e in enumerate(pairs) if not(bits>>j&1)]
            require(sorted(sum((list(e) for e in missing),[]))==list(range(6)),'Turan6 equality matching')
            equality.append(bits)
    require(len(equality)==15,'all Turan6 equality cases')
    blocks=((0,1),(2,3),(4,5));canonical={e for e in pairs if e[0]//2!=e[1]//2}
    transports=[]
    for order in it.permutations(range(3)):
        for flips in it.product((0,1),repeat=3):
            perm=tuple(blocks[order[i]][j^flips[i]] for i in range(3) for j in range(2))
            require({tuple(sorted((perm[a],perm[b]))) for a,b in canonical}==canonical,'Turan automorphism')
            transports.append(perm)
    allowed={};rejected=0
    for mask in range(64):
        chosen={w for w in range(6) if mask>>w&1}
        sizes=tuple(sorted(len(chosen&set(g)) for g in blocks))
        if sizes[0]>0:rejected+=1;continue  # a red triangle plus x
        target={2*i+j for i,k in enumerate(sizes) for j in range(k)}
        require(any({perm[w] for w in chosen}==target for perm in transports),'complete x-star normalization')
        allowed.setdefault(sizes,0);allowed[sizes]+=1
    require(set(allowed)=={(0,0,0),(0,0,1),(0,0,2),(0,1,1),(0,1,2),(0,2,2)},'six equality patterns')
    require(sum(allowed.values())+rejected==64,'full x-star domain')
    # Catalog contents and a literal isomorphism are checked. The fact that
    # this one record is COMPLETE is an explicit external premise.
    data=(HERE/'r35_13.g6').read_bytes()
    require(hashlib.sha256(data).hexdigest()=='eb4d3f787f07ed14c0a82a83bee170ed096c24b6a7e971fded185ca1a760798f','catalog fixture')
    lines=data.splitlines();require(len(lines)==1 and lines[0][0]-63==13,'one order13 record')
    bits=''.join(f'{b-63:06b}' for b in lines[0][1:])
    catalog={e for e,b in zip(((i,j) for j in range(1,13) for i in range(j)),bits) if b=='1'}
    mapping=(0,1,5,12,8,2,3,10,11,9,6,7,4)
    red=lambda a,b:(a-b)%13 in (1,5,8,12)
    require(set(mapping)==set(range(13)),'catalog transport bijection')
    require(all(((a,b) in catalog)==red(mapping[a],mapping[b]) for a,b in it.combinations(range(13),2)),'catalog transport adjacency')
    require(all(sum(red(a,b) for b in range(13) if b!=a)==4 for a in range(13)),'core regularity fixture')
    require(all(not all(red(a,b) for a,b in it.combinations(q,2)) for q in it.combinations(range(13),3)),'catalog no red triangle')
    require(all(any(red(a,b) for a,b in it.combinations(q,2)) for q in it.combinations(range(13),5)),'catalog no blue five')
    affine=[tuple((a*w+b)%13 for w in range(13)) for a in (1,5,8,12) for b in range(13)]
    require(len(set(affine))==52 and all(all(red(i,j)==red(p[i],p[j]) for i,j in it.combinations(range(13),2)) for p in affine),'52 verified automorphisms')
    cases=[];census=[]
    for pat in sorted(allowed):
        d=sum(pat);target=pat[1]*pat[2];subsets=set()
        for J in it.combinations(range(13),d):
            if sum(red(a,b) for a,b in it.combinations(J,2))==target:subsets.add(J)
        reps={min(tuple(sorted(p[w] for w in J)) for p in affine) for J in subsets}
        expanded={tuple(sorted(p[w] for w in J)) for J in reps for p in affine}
        require(expanded==subsets,'full omitted-core orbit coverage')
        cases.extend((pat,J) for J in sorted(reps));census.append({'pattern':list(pat),'subsets':len(subsets),'orbits':len(reps)})
    require(len(cases)==8,'complete eight-case cover')
    return cases,{'six_vertex_graphs':32768,'turan_extremizers':15,'x_star_assignments':64,
                  'admissible_x_stars':sum(allowed.values()),'catalog_completeness':'IMPORTED_PRIMARY_SOURCE',
                  'catalog_transport':list(mapping),'verified_affine_automorphisms':52,'orbit_census':census}


def audit_cnf(path,pattern,omitted):
    # Independent encoder: form full clauses as sets, then remove satisfied
    # clauses and false fixed literals. The producer is not imported.
    pairs=list(it.combinations(range(21),2));ids={e:j+1 for j,e in enumerate(pairs)}
    assigned={}
    for j,(a,b) in enumerate(pairs,1):
        if a==13 or b==13:assigned[j]=int((b if a==13 else a)<13)
        elif b<13:assigned[j]=int((a-b)%13 in (1,5,8,12))
        elif a>=15:assigned[j]=int((a-15)//2!=(b-15)//2)
        elif a==14:assigned[j]=int((b-15)%2<pattern[(b-15)//2])
        elif b==14:assigned[j]=int(a not in omitted)
    require(len(assigned)==132,'normalized fixed-edge count')
    expected=[]
    for size,sign in ((4,-1),(5,1)):
        for vs in it.combinations(range(21),size):
            full={sign*ids[p] for p in it.combinations(vs,2)}
            if any(abs(z) in assigned and assigned[abs(z)]==int(z>0) for z in full):continue
            expected.append(tuple(sorted(z for z in full if abs(z) not in assigned)))
    expected += [(j if b else -j,) for j,b in assigned.items()]
    lines=path.read_text().splitlines();header=lines.pop(0).split()
    require(header[:3]==['p','cnf','210'] and int(header[3])==len(lines),'CNF header')
    parsed=[]
    for line in lines:
        z=list(map(int,line.split()));require(z[-1]==0 and all(1<=abs(v)<=210 for v in z[:-1]),'CNF syntax')
        require(len(set(z[:-1]))==len(z)-1,'CNF repeated literal');parsed.append(tuple(sorted(z[:-1])))
    require(Counter(parsed)==Counter(expected),'all and only reduced physical clique clauses plus fixed units')
    return {'clauses':len(parsed),'cnf_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def physical_audit(opb):
    raw=(REPO/'ramsey_r55_m214_pair_normalization/roots.tsv').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==TABLE_SHA,'parent root table')
    rows=[row.split('\t') for row in raw.decode().splitlines()[1:]]
    selected=[i for i,r in enumerate(rows) if r[1:3]==['13','0']]
    require(selected==[48,128,129,201,202,299,300,375,376],'complete c13 k0 domain')
    require(tuple(i for i in selected if rows[i][:4]!=['C77partition','13','0','HO'])==ROOTS,'all zero-core-anomaly roots')
    wanted={}
    def put(number,terms,relation,rhs):
        value=(dict(terms),relation,rhs)
        require(number not in wanted or wanted[number]==value,'physical row conflict');wanted[number]=value
    def five(vs,red):
        vs=tuple(sorted(vs));sign=-1 if red else 1
        put(2*subset_rank(vs,N)+(2 if red else 1),[(edge(a,b),sign) for a,b in it.combinations(vs,2)],'>=',-9 if red else 1)
    for anchor,partner,cell in ((U,V,A),(V,U,B)):
        hood=tuple(sorted((partner,)+H+cell));require(len(hood)==21,'full anchor neighborhood')
        for four in it.combinations(hood,4):five((anchor,)+four,True)
        for five_set in it.combinations(hood,5):five(five_set,False)
    for four in it.combinations(H,4):five((Z,)+four,False)
    five_rows=len(wanted)
    for t in it.combinations(range(N),3):
        if U not in t and V not in t:continue
        z=triangle_id(t);es=[edge(a,b) for a,b in it.combinations(t,2)];first=2*math.comb(N,5)+4*(z-904)+1
        for j,e in enumerate(es):put(first+j,[(z,-1),(e,1)],'>=',0)
        put(first+3,[(z,1)]+[(e,-1) for e in es],'>=',-2)
    for anchor in (U,V):
        stars=[triangle_id(tuple(sorted((anchor,a,b)))) for a,b in it.combinations([w for w in range(N) if w!=anchor],2)]
        put(2*math.comb(N,5)+4*math.comb(N,3)+43+anchor+1,[(z,1) for z in stars],'=',100)
    put(1974690,[(y,1) for y in range(13245,13634)],'=',1)
    units=[(0,1,1)]
    cells=[[],list(range(2,8)),list(range(8,14)),[Z],list(H),[28],[29],list(range(30,43))]
    for j,cell in enumerate(cells):
        bits=((1,1),(1,0),(0,1),(0,0))[j%4]
        for w in cell:units.extend(((U,w,bits[0]),(V,w,bits[1])))
    units.sort();require(len(units)==83,'all anchor units')
    for r in ROOTS:
        first=1974691+sum(169+(57 if row[0]=='C77partition' else 0) for row in rows[:r]);selector=13245+r
        require(all(int(v) not in H for v in rows[r][6].split(',') if v),'no anomalous core vertex')
        for j,(a,b,value) in enumerate(units):put(first+j,[(edge(a,b),1 if value else -1),(selector,-1)],'>=',0 if value else -1)
        for h in H:
            es=[edge(h,z) for z in E]
            put(first+83+2*h,[(e,1) for e in es]+[(selector,-6)],'>=',0)
            put(first+84+2*h,[(e,-1) for e in es]+[(selector,-7)],'>=',-13)
    checked=check_stream(opb,wanted)
    fixed={edge(a,b):value for a,b,value in units};lhs=Counter();constant=0
    for anchor in (U,V):
        for a,b in it.combinations([w for w in range(N) if w!=anchor],2):
            if fixed[edge(anchor,a)] and fixed[edge(anchor,b)]:
                e=edge(a,b)
                if e in fixed:constant+=fixed[e]
                else:lhs[e]+=1
    for h in H:
        for z in E:lhs[edge(h,z)]-=1
    rhs=Counter({edge(a,b):2 for a,b in it.combinations(H,2)})
    for cell,x in ((A,28),(B,29)):
        rhs.update(edge(a,b) for a,b in it.combinations(cell,2));rhs.update(edge(x,h) for h in H)
    for h in H:rhs[edge(h,Z)]-=1
    require({e:c for e,c in lhs.items() if c}==dict(rhs),'global identity in every physical coordinate')
    require(constant==26 and 200-constant-13*6==96,'global identity constant')
    for a,b,c,z in it.product((0,1),repeat=4):require(all((z<=a,z<=b,z<=c,z>=a+b+c-2))==(z==a*b*c),'triangle product semantics')
    residual=Counter(row[0] for j,row in enumerate(rows) if j not in set(ROOTS)|{375})
    counts=[residual[f] for f in ('E8','E77','C8','C77','C77partition')]
    require(counts==[59,83,68,102,68] and sum(counts)==380,'cumulative candidate descriptor census')
    return {'physical_source_rows':checked,'physical_five_set_rows':five_rows,'identity_coordinates':len(rhs),
            'current_excluded_roots':list(ROOTS),'new_roots':[r for r in ROOTS if r!=376],
            'prior_excluded_roots':[375,376],'cumulative_excluded_roots':selected,'residual_counts':counts,
            'residual_descriptors':380,'identity_rhs':96,'anchor_triangle_upper_bound':199,'required_anchor_triangle_sum':200}


def farkas(path=None):
    c=json.loads((path or HERE/'certificate.json').read_text())
    require(c['variables']==['weighted_A','weighted_B','twice_eH','footprint_z'],'certificate coordinates')
    require([(r['coefficients'],r['rhs']) for r in c['inequalities']]==[([1,0,0,0],24),([0,1,0,0],24),([0,0,1,0],52),([0,0,0,-1],-5)],'derived bounds')
    require(c['equality']=={'coefficients':[1,1,1,-1],'rhs':96},'global equality')
    mu=c['inequality_multipliers'];nu=c['equality_multiplier']
    require(len(mu)==4 and all(type(m)==int and m>=0 for m in mu) and type(nu)==int,'exact multipliers')
    coeff=[sum(mu[j]*c['inequalities'][j]['coefficients'][i] for j in range(4))+nu*c['equality']['coefficients'][i] for i in range(4)]
    rhs=sum(mu[j]*c['inequalities'][j]['rhs'] for j in range(4))+nu*96
    require(coeff==[0]*4 and rhs==-1 and c['result']=={'coefficients':coeff,'rhs':rhs},'strict exact contradiction')
    # The HO root has RHS 95 and is NOT excluded by this certificate.
    require(24+24+52-5==95,'nonnegative HO boundary control')
    return rhs


def moment_separator():
    # The accepted P4 point inherits precisely these edge coordinates. Its
    # whole-system feasibility is a cited reviewed dependency, not re-proved.
    path=REPO/'ramsey_r55_m214_pair_column_hull/derive_fractional_certificate.py'
    require(hashlib.sha256(path.read_bytes()).hexdigest()=='e4508d3d79b5af10b5b195c76f84cfb96f8a2ed4fffc5a774db5bbf5268c145e','accepted edge producer')
    spec=importlib.util.spec_from_file_location('accepted_edges',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    answer=[]
    for cell,x in ((A,28),(B,29)):
        e=sum((m.edge_value(a,b) for a,b in it.combinations(cell,2)),F(0));t=sum((m.edge_value(x,h) for h in H),F(0))
        require((e,t,e+t)==(F(86,5),F(39,5),F(25)),'exact accepted point separator')
        answer.append({'cell':list(cell),'vertex':x,'cell_edges':str(e),'core_footprint':str(t),'sum':str(e+t),'slack':str(24-e-t)})
    return answer


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--cnfs',type=Path,required=True);parser.add_argument('--opb',type=Path,required=True)
    args=parser.parse_args();cases,coverage=equality_cover();cnfs=[]
    for i,(pat,J) in enumerate(cases):cnfs.append({'case':i,**audit_cnf(args.cnfs/f'case-{i}.cnf',pat,J)})
    result={'status':'EXACT_FINITE_COVER_AND_GLOBAL_CONSUMER_AUDITED_NATIVE_PROOFS_REQUIRED',
            'r34_rup_steps':small_r34(),'cover':coverage,'cnfs':cnfs,'global':physical_audit(args.opb),
            'farkas_rhs':farkas(),'moment_separator':moment_separator()}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
