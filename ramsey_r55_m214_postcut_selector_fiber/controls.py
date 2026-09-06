#!/usr/bin/env python3
"""Complete small transport controls and rejection of damaged certificates."""
import argparse
from fractions import Fraction as F
import itertools as it
import json
from pathlib import Path
import tempfile
import check


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--links',type=Path,required=True);args=parser.parse_args()
    point=check.Point(check.HERE/'certificate.json');transports=0
    for types,dist in point.four.items():
        for perm in it.permutations(range(4)):
            newtypes=tuple(types[i] for i in perm)
            bits=[check.PAIRS4.index(tuple(sorted((perm[a],perm[b])))) for a,b in check.PAIRS4]
            for state,mass in enumerate(dist):
                target=sum(((state>>bit)&1)<<j for j,bit in enumerate(bits))
                check.require(point.four[newtypes][target]==mass,'physical vertex/state transport');transports+=1
    check.require(transports==24576,'all four-vertex label transports')
    rejected=0
    def reject(call):
        nonlocal rejected
        try:call()
        except ValueError:rejected+=1
        else:raise ValueError('damaged evidence accepted')
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'mutated'
        baseline=json.loads((check.HERE/'certificate.json').read_text())
        for mode in ('scale','missing_class','missing_mass','negative','normalization','order'):
            data=json.loads(json.dumps(baseline))
            if mode=='scale':data['denominator']=-1
            elif mode=='missing_class':data['four_vertex_atoms'].pop()
            elif mode=='missing_mass':data['four_vertex_atoms'][0]['numerators'].pop()
            elif mode=='negative':data['four_vertex_atoms'][0]['numerators'][0]=-1
            elif mode=='normalization':data['four_vertex_atoms'][0]['numerators'][0]+=1
            else:data['four_vertex_atoms'][0]['exceptional_count']=1
            path.write_text(json.dumps(data));reject(lambda:check.Point(path))
        for index in (min(point.edge.values()),min(point.triangle.values())):
            point.V[index]+=1;reject(lambda:check.global_moments(point));point.V[index]-=1
        key=min(point.all_wedges);point.all_wedges[key]+=1;reject(lambda:check.global_moments(point));point.all_wedges[key]-=1
        index=min(point.q.values());point.V[index]+=1;reject(lambda:check.full_four_hull(point));point.V[index]-=1
        original=args.links.read_text().splitlines()
        damaged=original.copy();damaged[0]=damaged[0].replace('+1 x1','+2 x1',1)
        path.write_text('\n'.join(damaged)+'\n');reject(lambda:check.check_link_file(path,point))
        path.write_text('\n'.join(original[:-1])+'\n');reject(lambda:check.check_link_file(path,point))
        # The cap 6/13 is sharp at the actual root unit x02-y_r>=0.
        path.write_bytes(check.HEADER+b'+1 x2 -1 x13245 >= 0 ;\n')
        reject(lambda:check.base_fiber(path,point,F(1,2)))
        path.write_bytes(check.HEADER+b'+1 x0 >= 0 ;\n');reject(lambda:check.base_fiber(path,point))
        path.write_bytes(check.HEADER+b'+1 x1 >= 0 ;\n');reject(lambda:check.base_fiber(path,point))
        cg=json.loads((check.HERE/'anchor_cg.json').read_text())
        for field,value in (('each_guard_multiplier','-1/389'),('selector_equality_multiplier','0'),('rounded_rhs',2)):
            damaged=dict(cg);damaged[field]=value;path.write_text(json.dumps(damaged));reject(lambda:check.check_cg(point,path))
    check.require(rejected==18,'all corruption controls')
    print(json.dumps({'status':'PASS','physical_four_state_transports':transports,'corruptions_rejected':rejected},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
