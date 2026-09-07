#!/usr/bin/env python3
"""Physical transport, elementary Boolean implication and corruption controls."""
import argparse
from pathlib import Path
import itertools as it
import json
import tempfile
import check
import emit_stars
import emit_degree
import emit_square


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--links',type=Path,required=True);parser.add_argument('--forbidden',type=Path,required=True);parser.add_argument('--degree-separator',type=Path,required=True);parser.add_argument('--certificate',type=Path,required=True);parser.add_argument('--deficiency-separator',type=Path,required=True);parser.add_argument('--square',type=Path,required=True);args=parser.parse_args()
    point=check.Point(args.certificate);transports=0
    canonical=sorted(ts for ts in point.four if tuple(sorted(ts))==ts)
    for types in canonical:
        dist=point.four[types]
        for perm in it.permutations(range(4)):
            newtypes=tuple(types[i] for i in perm);bits=[check.PAIRS4.index(tuple(sorted((perm[a],perm[b])))) for a,b in check.PAIRS4]
            for state,mass in enumerate(dist):
                target=sum((state>>bit&1)<<j for j,bit in enumerate(bits))
                check.require(point.four[newtypes][target]==mass,'physical vertex/state transport');transports+=1
    check.require(transports==345*24*64,'complete transports')
    implication=0
    pairs=list(it.combinations(range(5),2));anchor=[i for i,pair in enumerate(pairs) if 0 in pair];inner=[i for i,pair in enumerate(pairs) if 0 not in pair]
    for color in (0,1):
        for state in range(1024):
            fixed=all((state>>j&1)==color for j in anchor)
            five_clause=state.bit_count()<=9 if color else state.bit_count()>=1
            four_event=all((state>>j&1)==color for j in inner)
            check.require(not(fixed and five_clause and four_event),'forbidden-state implication');implication+=1
    star_cases=star_violations=0
    for state in range(1024):
        for h in range(5):
            inner_pairs=[i for i,pair in enumerate(pairs) if h not in pair]
            star_pairs=[i for i,pair in enumerate(pairs) if h in pair]
            red_sum=sum(state>>i&1 for i in star_pairs)
            for color in (0,1):
                event=int(all((state>>i&1)==color for i in inner_pairs))
                slack=(4-red_sum if color else red_sum)-event
                check.require((slack<0)==(state==(1023 if color else 0)),'literal global star implication')
                star_cases+=1;star_violations+=int(slack<0)
    # Compare every emitted coefficient with a different lexicographic rank
    # formula and five-set/omitted-anchor enumeration on small complete domains.
    emitted_rows=0
    for n in (5,6,7):
        edges={pair:i for i,pair in enumerate(it.combinations(range(n),2),1)}
        expected=set();start=100
        for five in it.combinations(range(n),5):
            for h in five:
                vs=tuple(v for v in five if v!=h)
                for color in (0,1):
                    terms={edges[tuple(sorted((h,v)))]:-1 if color else 1 for v in vs}
                    terms[start+64*check.rank_subset(vs,n)+(63 if color else 0)]=-1
                    expected.add((tuple(sorted(terms.items())),-4 if color else 0))
        actual=[]
        for line in emit_stars.rows(n,start):
            fields=line.split();check.require(fields[-3]=='>=' and fields[-1]==';','emitter syntax')
            terms=tuple(sorted((int(fields[j+1][1:]),int(fields[j])) for j in range(0,len(fields)-3,2)))
            actual.append((terms,int(fields[-2])))
        check.require(len(actual)==len(set(actual)) and set(actual)==expected,'full small physical row emitter')
        emitted_rows+=len(actual)
    degree_cases=0
    for graph in range(1024):
        red={pair for j,pair in enumerate(pairs) if graph>>j&1}
        degree=[sum(v in e for e in red) for v in range(5)]
        for A in it.combinations(range(5),3):
            observed=sum(int(pair in red)<<j for j,pair in enumerate(it.combinations(A,2)))
            for h in A:
                external=sum(tuple(sorted((h,w))) in red for w in range(5) if w not in A)
                for state in range(8):
                    indicator=int(observed==state)
                    local=sum(state>>j&1 for j,e in enumerate(it.combinations(A,2)) if h in e)
                    check.require(indicator*external==(degree[h]-local)*indicator,'literal conditioned degree identity')
                    degree_cases+=1
    # Coefficient-level comparison over the complete order-five family, with
    # prescribed values spanning every possible degree 0 through 4.
    degree_rows=0;degrees=list(range(5))
    for A,h,state,actual in emit_degree.family(n=5,first_p=100,degrees=degrees):
        expected={};b=next(v for v in range(5) if v not in A)
        for w in range(5):
            if w in A:continue
            Q=tuple(sorted(A+(w,)));physical_pairs=tuple(it.combinations(Q,2))
            for mask in range(64):
                colors={pair:mask>>j&1 for j,pair in enumerate(physical_pairs)}
                observed=sum(colors[pair]<<j for j,pair in enumerate(it.combinations(A,2)))
                local=sum(state>>j&1 for j,e in enumerate(it.combinations(A,2)) if h in e)
                c=int(observed==state)*(colors[tuple(sorted((h,w)))]-(degrees[h]-local)*int(w==b))
                if c:expected[100+64*check.rank_subset(Q,5)+mask]=c
        check.require(actual==expected,'complete small degree-row coefficients');degree_rows+=1
    check.require((degree_cases,degree_rows)==(245760,240),'degree control coverage')
    triangle_cases=cap_cases=square_cases=0
    for graph in range(1024):
        red={pair for j,pair in enumerate(pairs) if graph>>j&1}
        for h in range(5):
            others=[v for v in range(5) if v!=h]
            total=sum(all(tuple(sorted(e)) in red for e in ((h,u),(h,v),(u,v))) for u,v in it.combinations(others,2))
            for a in others:
                actual=sum(all(tuple(sorted(e)) in red for e in ((h,u),(h,v),(u,v),(h,a))) for u,v in it.combinations(others,2))
                check.require(actual==total*int(tuple(sorted((h,a))) in red),'literal conditioned triangle identity');triangle_cases+=1
        for color in (0,1):
            # A monochromatic triangle plus five common same-color neighbors:
            # an inner same-color edge completes a K5; if none, the five
            # common neighbors themselves form an opposite-color K5.
            same=any((graph>>j&1)==color for j in range(10))
            opposite=all((graph>>j&1)!=color for j in range(10))
            check.require(same or opposite,'triangle cap Ramsey implication');cap_cases+=1
        E={1,2,3}
        for h in range(5):
            targets=sorted(E-{h});a=sum(tuple(sorted((h,u))) in red for u in targets)
            expansion=a
            for u,v in it.combinations(targets,2):
                x=int(tuple(sorted((h,u))) in red);y=int(tuple(sorted((h,v))) in red)
                expansion+=2*((1-x)*(1-y)+x+y-1)
            check.require(expansion==a*a,'literal blue-wedge square expansion');square_cases+=1
    anomaly_cases=0
    for count in (1,2):
        for support in it.combinations(range(43),count):
            values=[6+(2//count if h in support else 0) for h in range(43)]
            check.require(sum(values)==260 and sum(a*a for a in values)==(1576 if count==1 else 1574),'global deficiency partition');anomaly_cases+=1
    check.require((triangle_cases,cap_cases,square_cases,anomaly_cases)==(20480,2048,5120,946),'new control coverage')
    # Independent literal graph evaluation of every emitted small cut-square
    # coefficient, across every 2-by-3 cut and all 1024 physical graphs.
    small_edges=list(it.combinations(range(5),2));small_wedges={(u,v,h):11+j for j,(u,v,h) in enumerate((u,v,h) for u,v in small_edges for h in range(5) if h not in (u,v))}
    four=list(it.combinations(range(5),4));emitted=[]
    for A in it.combinations(range(5),2):
        B=tuple(v for v in range(5) if v not in A);row,rhs=emit_square.coefficients(5,A,B,3,small_wedges,100);emitted.append((A,B,row,rhs))
    square_emitter_cases=0
    for graph in range(1024):
        red={e for j,e in enumerate(small_edges) if graph>>j&1};values={i:int(e in red) for i,e in enumerate(small_edges,1)}
        values.update({i:int(tuple(sorted((u,h))) not in red and tuple(sorted((v,h))) not in red) for (u,v,h),i in small_wedges.items()})
        for j,vs in enumerate(four):
            observed=sum(int(e in red)<<b for b,e in enumerate(it.combinations(vs,2)))
            values.update({100+64*j+state:int(state==observed) for state in range(64)})
        for A,B,row,rhs in emitted:
            X=sum(tuple(sorted((u,v))) in red for u in A for v in B)
            actual=sum(c*values[i] for i,c in row.items())-rhs
            check.require(actual==(X-3)**2 and actual>=0,'literal emitted cut-square');square_emitter_cases+=1
    check.require(square_emitter_cases==10240,'complete cut-square emitter truth table')
    rejected=0
    def reject(call):
        nonlocal rejected
        try:call()
        except ValueError:rejected+=1
        else:raise ValueError('damaged evidence accepted')
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'bad';base=json.loads((args.certificate).read_text())
        for mode in ('schema','scale','partition','missing_table','negative','normalization','type_order','selector'):
            d=json.loads(json.dumps(base))
            if mode=='schema':d['format']='bad'
            elif mode=='scale':d['denominator']=-1
            elif mode=='partition':d['cells'][-1][-1]=0
            elif mode=='missing_table':d['four_tables'].pop()
            elif mode=='negative':
                row=d['four_tables'][0]['orbits'];row[next(iter(row))]=-1
            elif mode=='normalization':
                row=d['four_tables'][0]['orbits'];row[next(iter(row))]+=1
            elif mode=='type_order':d['four_tables'][0]['types'].reverse()
            else:d['active_selectors']=[389]
            path.write_text(json.dumps(d));reject(lambda:check.Point(path))
        for idx in [min(point.edge.values()),min(point.triangle.values())]:
            point.V[idx]+=1;reject(lambda:check.global_moments(point));point.V[idx]-=1
        key=min(point.all_wedges);point.all_wedges[key]+=1;reject(lambda:check.global_moments(point));point.all_wedges[key]-=1
        idx=min(point.q.values());point.V[idx]+=1;reject(lambda:check.full_four_hull(point));point.V[idx]-=1
        for original,fn in [(args.links.read_text().splitlines(),check.check_links),(args.forbidden.read_text().splitlines(),check.check_forbidden_file)]:
            path.write_text('\n'.join(original[:-1])+'\n');reject(lambda:fn(point,path) if fn==check.check_links else fn(path,point))
            bad=original.copy();bad[0]=bad[0].replace('+1 ','+2 ',1).replace('-1 ','-2 ',1);path.write_text('\n'.join(bad)+'\n');reject(lambda:fn(point,path) if fn==check.check_links else fn(path,point))
        point.V[13245+278]-=1;reject(lambda:check.check_links(point,args.links));point.V[13245+278]+=1
        point.V[13245+278]=0;point.V[13245+48]=point.D;reject(lambda:check.check_links(point,args.links));point.V[13245+48]=0;point.V[13245+278]=point.D
        for content in [check.HEADER+b'+1 x0 >= 0 ;\n',check.HEADER+b'+1 x1 >= 0 ;\n',check.HEADER+b'-1 x1 >= 0 ;\n']:
            path.write_bytes(content);reject(lambda:check.base_point(path,point))
        original=args.degree_separator.read_text()
        path.write_text(original.replace(' = 0 ;',' >= 0 ;'))
        reject(lambda:check.conditioned_degrees(point,path))
        path.write_text(original.replace('+1 ','+2 ',1))
        reject(lambda:check.conditioned_degrees(point,path))
        original=args.deficiency_separator.read_text()
        for damaged in (original.replace('>= -7972','>= -7971'),original.replace('-46 ','-45 ',1),' '.join(original.split()[2:])):
            path.write_text(damaged);reject(lambda:check.deficiency_bound(point,path))
        triple=next(key for key in point.triples if point.triples[key][7]>0)
        old=point.triples[triple];d=list(old);d[7]-=point.D;point.triples[triple]=tuple(d)
        reject(lambda:check.triangle_rows(point));point.triples[triple]=old
        original=args.square.read_text()
        for damaged in (original.replace('>= -1596','>= -1595'),original.replace('-97 ','-96 ',1),' '.join(original.split()[2:])):
            path.write_text(damaged);reject(lambda:check.cut_square(point,path))
    # Change a zero forbidden atom while retaining the old fixed star: both
    # the specialized and global evaluators must detect it. Restore afterward.
    vs=(8,9,10,11);types=point.types(vs);old=point.four[types]
    changed=list(old);changed[0]+=1;point.four[types]=tuple(changed)
    reject(lambda:check.check_forbidden_file(args.forbidden,point))
    reject(lambda:check.require(min(check.star_slacks(point,0,vs))>=0,'global star corruption'))
    point.four[types]=old
    check.require(rejected==32,'all corruption controls')
    print(json.dumps({'status':'PASS','physical_transports':transports,'boolean_implication_cases':implication,'corruptions_rejected':rejected,'global_star_boolean_cases':star_cases,'excluded_monochromatic_star_cases':star_violations,'small_complete_emitted_rows':emitted_rows,'conditioned_degree_boolean_cases':degree_cases,'small_complete_degree_rows':degree_rows,'conditioned_triangle_boolean_cases':triangle_cases,'triangle_cap_boolean_cases':cap_cases,'square_expansion_boolean_cases':square_cases,'all_deficiency_partitions':anomaly_cases,'cut_square_emitter_boolean_cases':square_emitter_cases},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
