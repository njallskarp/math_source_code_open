#!/usr/bin/env python3
"""Physical transport, elementary Boolean implication and corruption controls."""
import argparse
from pathlib import Path
import itertools as it
import json
import tempfile
import check


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--links',type=Path,required=True);parser.add_argument('--forbidden',type=Path,required=True);args=parser.parse_args()
    point=check.Point(check.HERE/'certificate.json');transports=0
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
    rejected=0
    def reject(call):
        nonlocal rejected
        try:call()
        except ValueError:rejected+=1
        else:raise ValueError('damaged evidence accepted')
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'bad';base=json.loads((check.HERE/'certificate.json').read_text())
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
    check.require(rejected==21,'all corruption controls')
    print(json.dumps({'status':'PASS','physical_transports':transports,'boolean_implication_cases':implication,'corruptions_rejected':rejected},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
