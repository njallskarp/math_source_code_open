#!/usr/bin/env python3
"""Exact physical-source and Farkas audit for complete M214 root376."""
import argparse
from collections import Counter
import hashlib
import itertools as it
import json
import math
from pathlib import Path
from check_rup import require, rup, verify

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
N=43; U,V=0,1; P,Q=28,29; Z=14; Y=13621
H=tuple(range(15,28));E=tuple(range(2,15))
A=tuple(range(2,8))+(P,);B=tuple(range(8,14))+(Q,)
ROOT_SHA='407b3d0c56f117e6eab6f9943728faa30bb16f77ec2ca6499e88ebb4d528bc46'
TABLE_SHA='f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e'
OPB_SHA='469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f'


def edge(a,b):
    a,b=sorted((a,b));require(0<=a<b<N,'physical edge')
    return a*(85-a)//2+b-a


def subset_rank(vertices,n):
    rank=0;last=-1;k=len(vertices)
    for j,v in enumerate(vertices):
        rank+=sum(math.comb(n-1-x,k-1-j) for x in range(last+1,v));last=v
    return rank


def triangle_id(t):return 904+subset_rank(t,43)


def root_check(path):
    raw=path.read_bytes();require(hashlib.sha256(raw).hexdigest()==ROOT_SHA,'complete descriptor hash');r=json.loads(raw)
    require(r['key']==['C77partition',13,0,'AB'] and r['anchors']==[U,V] and r['anomalies']==[P,Q],'root marks')
    cells=[[],list(range(2,8)),list(range(8,14)),[Z],list(H),[P],[Q],list(range(30,43))]
    require(r['cells']==cells and r['E']==list(E),'all physical cells')
    require(r['E_cells']==[0,6,6,1] and r['C_cells']==[13,1,1,13],'cell dimensions')
    units=[(0,1,1)]
    for i,cell in enumerate(cells):
        bits=((1,1),(1,0),(0,1),(0,0))[i%4]
        for w in cell:units.extend([(0,w,bits[0]),(1,w,bits[1])])
    require(r['edge_units']==[list(x) for x in sorted(units)],'83 anchor units')
    require(r['a_equalities']==[[w,7 if w in (P,Q) else 6] for w in range(N)],'43 E-incidence equations')
    central=[w for w in range(N) if w not in E and w not in (P,Q)]
    require(r['partition']=={'blue_pair':[P,Q],'one_red_to_pair':central},'universal partition')
    buckets=[]
    for cell in cells:
        for status in (0,1):
            bucket=[w for w in cell if int(w in (P,Q))==status]
            if bucket:buckets.append(bucket)
    require(r['ordering_buckets']==buckets,'residual buckets')
    raw=(REPO/'ramsey_r55_m214_pair_normalization/roots.tsv').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==TABLE_SHA,'root table identity')
    rows=raw.decode().splitlines()[1:];require(len(rows)==389,'full root census')
    require(rows[376].split('\t')[:4]==['C77partition','13','0','AB'] and rows[376].split('\t')[-1]==ROOT_SHA,'exact root membership')
    selected=[(i,row.split('\t')[3]) for i,row in enumerate(rows) if row.split('\t')[:3]==['C77partition','13','0']]
    require(selected==[(375,'HO'),(376,'AB')],'complete two-pattern parameter slice')
    counts=Counter(row.split('\t')[0] for i,row in enumerate(rows) if i not in (375,376))
    require([counts[f] for f in ('E8','E77','C8','C77','C77partition')]==[60,85,70,104,68] and sum(counts.values())==387,'remaining census after both cuts')
    first=1974691+sum(169+(57 if row.startswith('C77partition\t') else 0) for row in rows[:376])
    require(first==2041484,'root first physical row')
    return r,first


def physical_rows(root,first):
    wanted={};five_inputs={};units=[]
    def put(number,terms,relation,rhs):
        item=(dict(terms),relation,rhs)
        require(number not in wanted or wanted[number]==item,'conflicting source row');wanted[number]=item
    def five(vs,red):
        vs=tuple(sorted(vs));values=tuple(edge(a,b)*(-1 if red else 1) for a,b in it.combinations(vs,2))
        put(2*subset_rank(vs,N)+(2 if red else 1),[(abs(x),1 if x>0 else -1) for x in values],'>=',-9 if red else 1)
        five_inputs[frozenset(values)]=values
    for t in it.combinations(H,3):five((U,V)+t,True)
    for s in it.combinations(H,5):five(s,False)
    for s in it.combinations(H,4):five((Z,)+s,False)
    for anchor,cell in ((U,A),(V,B)):
        for s in it.combinations(cell,4):five((anchor,)+s,True)
    for offset,(a,b,value) in enumerate(root['edge_units']):
        e=edge(a,b);units.append((e if value else -e,))
        put(first+offset,[(e,1 if value else -1),(Y,-1)],'>=',0 if value else -1)
    for w in H:
        es=[edge(w,z) for z in E]
        put(first+83+2*w,[(e,1) for e in es]+[(Y,-6)],'>=',0)
        put(first+84+2*w,[(e,-1) for e in es]+[(Y,-7)],'>=',-13)
        offset=root['partition']['one_red_to_pair'].index(w)
        es=[edge(w,t) for t in (P,Q)]
        put(first+170+2*offset,[(e,1) for e in es]+[(Y,-1)],'>=',0)
        put(first+171+2*offset,[(e,-1) for e in es]+[(Y,-1)],'>=',-2)
    stars={};products=0
    for t in it.combinations(range(N),3):
        if U not in t and V not in t:continue
        z=triangle_id(t);es=[edge(a,b) for a,b in it.combinations(t,2)];row=2*math.comb(N,5)+4*(z-904)+1
        for i,e in enumerate(es):put(row+i,[(z,-1),(e,1)],'>=',0)
        put(row+3,[(z,1)]+[(e,-1) for e in es],'>=',-2);products+=1
    for anchor in (U,V):
        stars[anchor]=[triangle_id(tuple(sorted((anchor,a,b)))) for a,b in it.combinations([w for w in range(N) if w!=anchor],2)]
        put(2*math.comb(N,5)+4*math.comb(N,3)+43+anchor+1,[(z,1) for z in stars[anchor]],'=',100)
    put(1974690,[(y,1) for y in range(13245,13634)],'=',1)
    require((len(five_inputs),products,len(wanted))==(2358,1681,9220),'physical input coverage')
    return wanted,five_inputs,units


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


def combinatorial_bounds(inputs,units):
    def axiom(c):
        require(frozenset(c) in inputs,'missing physical five-set');return inputs[frozenset(c)]
    triangles={}
    for t in it.combinations(H,3):
        c=tuple(-edge(a,b) for a,b in it.combinations(t,2))
        five=axiom(tuple(-edge(a,b) for a,b in it.combinations((U,V)+t,2)))
        require(rup([five]+units,c),'core triangle RUP');triangles[t]=c
    caps=0
    for h in H:
        for five in it.combinations([w for w in H if w!=h],5):
            premises=[triangles[tuple(sorted((h,a,b)))] for a,b in it.combinations(five,2)]
            premises.append(axiom(tuple(edge(a,b) for a,b in it.combinations(five,2))))
            require(rup(premises,tuple(-edge(h,w) for w in five)),'core five-neighbor cap');caps+=1
    # These are every five-subset of every twelve-bit core star.
    require(caps==13*math.comb(12,5),'complete degree caps')
    star_count=0
    for mask in range(1<<12):
        if mask.bit_count()>4:require(len([j for j in range(12) if mask>>j&1][:5])==5,'degree cap coverage')
        star_count+=1
    k4_rows=0
    for anchor,cell in ((U,A),(V,B)):
        for four in it.combinations(cell,4):
            clause=tuple(-edge(a,b) for a,b in it.combinations(four,2))
            five=axiom(tuple(-edge(a,b) for a,b in it.combinations(tuple(sorted((anchor,)+four)),2)))
            require(rup([five]+units,clause),'off-diagonal K4 prohibition');k4_rows+=1
    # Complete violation domain for e(K4-free graph on seven vertices)<=16.
    pairs=tuple(it.combinations(range(7),2));quad_masks=[sum(1<<pairs.index(e) for e in it.combinations(s,2)) for s in it.combinations(range(7),4)]
    tested=0
    for k in range(5):
        for missing in it.combinations(range(21),k):
            blue=sum(1<<e for e in missing)
            require(any(blue&m==0 for m in quad_masks),'Turan7 counterexample');tested+=1
    require(tested==7547,'complete Turan violation enumeration')
    blocks=({0,1,2},{3,4},{5,6});sharp={e for e in pairs if not any(set(e)<=b for b in blocks)}
    require(len(sharp)==16 and all(not all(e in sharp for e in it.combinations(s,2)) for s in it.combinations(range(7),4)),'sharp Turan fixture')
    embeddings=checks=0
    for nine in it.combinations(H,9):
        guard={edge(Z,w) for w in nine}
        for t in it.combinations(nine,3):require(t in triangles,'R34 triangle embedding');checks+=1
        for four in it.combinations(nine,4):
            premise=axiom(tuple(edge(a,b) for a,b in it.combinations(tuple(sorted((Z,)+four)),2)))
            require(set(premise)<={edge(a,b) for a,b in it.combinations(four,2)}|guard,'R34 guarded four-set');checks+=1
        embeddings+=1
    footprint_assignments=0
    for mask in range(1<<13):
        if mask.bit_count()<=4:
            blue=[H[j] for j in range(13) if not(mask>>j&1)]
            require(len(blue)>=9 and tuple(blue[:9]) in set(it.combinations(H,9)),'footprint low-degree coverage')
        footprint_assignments+=1
    require((k4_rows,embeddings,checks,footprint_assignments)==(70,715,150150,8192),'local bound coverage')
    return {'core_triangle_rup_rows':len(triangles),'core_degree_cap_rup_rows':caps,'core_star_assignments':star_count,'off_diagonal_k4_rup_rows':k4_rows,'turan7_violating_graphs_exhausted':tested,'footprint_r34_embeddings':embeddings,'embedding_clause_checks':checks,'footprint_assignments':footprint_assignments}


def physical_identity(root):
    fixed={edge(a,b):value for a,b,value in root['edge_units']};lhs=Counter();constant=0;product_controls=0
    # The four Boolean product inequalities are truth-table checked once.
    for a,b,c,z in it.product((0,1),repeat=4):
        rows=(z<=a,z<=b,z<=c,z>=a+b+c-2)
        require(all(rows)==(z==a*b*c),'triangle conjunction semantics');product_controls+=1
    for anchor in (U,V):
        for a,b in it.combinations([w for w in range(N) if w!=anchor],2):
            if fixed[edge(anchor,a)] and fixed[edge(anchor,b)]:
                e=edge(a,b)
                if e in fixed:constant+=fixed[e]
                else:lhs[e]+=1
    # Subtract all 13 a(h)=6 and all 13 anomaly partition equations.
    for h in H:
        for z in E:lhs[edge(h,z)]-=1
        for z in (P,Q):lhs[edge(h,z)]-=1
    expected=Counter()
    for a,b in it.combinations(H,2):expected[edge(a,b)]+=2
    for cell in (A,B):
        for a,b in it.combinations(cell,2):expected[edge(a,b)]+=1
    for h in H:expected[edge(h,Z)]-=1
    require({e:c for e,c in lhs.items() if c}==dict(expected),'exact coefficient cancellation in physical coordinates')
    require(constant==26 and 200-13*6-13-constant==83,'exact right-hand side')
    # Summing thirteen degree caps is exactly twice the common-core edge sum.
    incidences=Counter(edge(h,w) for h in H for w in H if w!=h)
    require(incidences==Counter({edge(a,b):2 for a,b in it.combinations(H,2)}),'degree sum coefficients')
    return {'triangle_product_truth_cases':product_controls,'identity_physical_coordinates':len(expected),'identity_rhs':83,'anchor_triangle_upper_bound':196,'required_anchor_triangle_sum':200}


def farkas_check(path):
    c=json.loads(path.read_text());require(c['variables']==['eA','eB','twice_eH','footprint_z'],'certificate coordinates')
    expected=[([1,0,0,0],16),([0,1,0,0],16),([0,0,1,0],52),([0,0,0,-1],-5)]
    require([(r['coefficients'],r['rhs']) for r in c['inequalities']]==expected,'certified bound rows')
    require((c['equality']['coefficients'],c['equality']['rhs'])==([1,1,1,-1],83),'physical equality row')
    mus=c['inequality_multipliers'];nu=c['equality_multiplier']
    require(len(mus)==4 and all(type(m)==int and m>=0 for m in mus) and type(nu)==int,'exact Farkas multipliers')
    coeff=[sum(m*r['coefficients'][i] for m,r in zip(mus,c['inequalities']))+nu*c['equality']['coefficients'][i] for i in range(4)]
    rhs=sum(m*r['rhs'] for m,r in zip(mus,c['inequalities']))+nu*c['equality']['rhs']
    require(coeff==[0]*4 and rhs<0 and c['result']=={'coefficients':coeff,'rhs':rhs},'Farkas contradiction')
    return rhs


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--opb',type=Path,required=True);args=parser.parse_args()
    r,start=root_check(HERE/'root.json');wanted,inputs,units=physical_rows(r,start);source=check_stream(args.opb,wanted)
    result={'status':'EXACT_COMPLETE_M214_ROOT376_TRIANGLE_EXCLUSION','root_index':376,'root_key':r['key'],'selector':Y,'root_core_variables_fixed':0,'nonanchor_physical_edges_retained':820,'parent_opb_sha256':OPB_SHA,'source_rows_verified':source,'small_r34_rup_rows':small_r34(),**combinatorial_bounds(inputs,units),**physical_identity(r),'farkas_rhs':farkas_check(HERE/'certificate.json'),'remaining_root_descriptors_with_reviewed_root375_cut':387,'remaining_family_counts':[60,85,70,104,68]}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
