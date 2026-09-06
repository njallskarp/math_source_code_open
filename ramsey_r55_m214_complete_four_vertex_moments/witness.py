#!/usr/bin/env python3
"""Expand the compact certificate into physical six-edge distributions."""
import argparse
import hashlib
import importlib.util
import itertools as it
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
PRIOR_SHA='f4632a73ce93c6f5caffdfacbb3fecafe34ede8fe53749f107cb4d264da26eff'
PAIRS=tuple(it.combinations(range(4),2))


def require(ok,message):
    if not ok: raise ValueError(message)


def previous():
    path=REPO/'ramsey_r55_m214_global_star_moments/witness.py'
    require(hashlib.sha256(path.read_bytes()).hexdigest()==PRIOR_SHA,'previous producer identity')
    spec=importlib.util.spec_from_file_location('star_producer',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def read_certificate(path):
    data=json.loads(path.read_text());require(set(data)=={'denominator','templates'},'certificate fields')
    D=int(data['denominator']);require(D>0,'positive denominator')
    result={}
    for row in data['templates']:
        require(set(row)=={'types','edges','atoms'},'template fields')
        key=(tuple(row['types']),tuple(map(F,row['edges'])))
        require(len(key[0])==4 and len(key[1])==6 and key not in result,'template key')
        atoms={int(k):int(v) for k,v in row['atoms'].items()}
        require(len(atoms)==len(row['atoms']) and atoms and all(0<=k<64 and v>0 for k,v in atoms.items()),'sparse atoms')
        require(sum(atoms.values())==D,'atom normalization')
        result[key]=atoms
    require(len(result)==463,'template count')
    return D,result


def canonical(vertices,classes,edges):
    blocks=defaultdict(list)
    for v in vertices:blocks[classes.TYPE_INDEX[classes.VERTEX_TYPE[v]]].append(v)
    types=tuple(sorted(classes.TYPE_INDEX[classes.VERTEX_TYPE[v]] for v in vertices))
    orders=(sum(p,()) for p in it.product(*(it.permutations(blocks[k]) for k in sorted(blocks))))
    order=min(orders,key=lambda p:tuple(edges[a,b] for a,b in it.combinations(p,2)))
    return (types,tuple(edges[a,b] for a,b in it.combinations(order,2))),order


def transport(atoms,order,vertices):
    positions=[PAIRS.index(tuple(sorted((vertices.index(order[a]),vertices.index(order[b]))))) for a,b in PAIRS]
    return {sum(((mask>>k)&1)<<j for k,j in enumerate(positions)):mass for mask,mass in atoms.items()}


def marginal(atoms,bits):
    result=[0]*8
    for mask,mass in atoms.items():result[sum(((mask>>b)&1)<<j for j,b in enumerate(bits))]+=mass
    return tuple(result)


def generate(vector_path,moments_path,four_path):
    old=previous();_,classes=old.base();decoder=old.load('ramsey_r55_m214_reanchored_moment_hull/check.py','physical_decoder')
    edges,_,missed,footprints=decoder.decoder()
    base=old.values()[1];D,templates=read_certificate(HERE/'certificate.json')
    values=[0]*98759
    for k in list(edges.values())+list(range(13245,13634)):values[k]=int(base[k][1]*D)
    # Only fixed edge/selector coordinates are inherited. Every triangle, wedge,
    # and footprint is overwritten from physical four-vertex distributions.
    require(all((base[k][1]*D).denominator==1 for k in list(edges.values())+list(range(13245,13634))),'fixed coordinate scale')
    edge_values={(a,b):classes.edge_value(a,b) for a in range(43) for b in range(43) if a!=b}
    by_four=defaultdict(list)
    for key,index in footprints.items():by_four[tuple(sorted(key))].append((key,index))
    triangles={t:k for k,t in enumerate(it.combinations(range(43),3),904)}
    moments={};seen_triangles={};seen_q=set();used=set()
    with four_path.open('w',encoding='ascii') as handle:
        handle.write(f'four-vertex-atoms\t43\t{D}\n')
        for vertices in it.combinations(range(43),4):
            key,order=canonical(vertices,classes,edge_values);used.add(key)
            atoms=transport(templates[key],order,vertices)
            pairs=tuple(it.combinations(vertices,2))
            handle.write('\t'.join(map(str,vertices))+'\t'+'\t'.join(f'{k}:{v}' for k,v in sorted(atoms.items()))+'\n')
            for tri in it.combinations(vertices,3):
                bits=[pairs.index(p) for p in it.combinations(tri,2)];dist=marginal(atoms,bits)
                if tri in seen_triangles:require(seen_triangles[tri]==dist,'shared physical triangle')
                else:
                    seen_triangles[tri]=dist;values[triangles[tri]]=dist[7]
                    tp=tuple(it.combinations(tri,2))
                    for h in tri:
                        incident=[i for i,p in enumerate(tp) if h in p]
                        moments[tuple(v for v in tri if v!=h)+(h,)]=sum(p for mask,p in enumerate(dist) if all(not(mask>>i&1) for i in incident))
            for (a,b,i,j),index in by_four[vertices]:
                red=pairs.index((i,j));blue=[pairs.index(tuple(sorted((v,h)))) for v in (a,b) for h in (i,j)]
                values[index]=sum(mass for mask,mass in atoms.items() if mask>>red&1 and all(not(mask>>k&1) for k in blue));seen_q.add(index)
    require(used==set(templates) and len(seen_triangles)==12341 and len(seen_q)==74513,'physical support')
    for key,index in missed.items():values[index]=moments[key]
    with vector_path.open('w',encoding='ascii') as handle:
        handle.write('variable\tvalue\n')
        for k,v in enumerate(values[1:],1):handle.write(f'{k}\t{F(v,D)}\n')
    with moments_path.open('w',encoding='ascii') as handle:
        handle.write(old.MOMENT_HEADER)
        for tri in it.combinations(range(43),3):handle.write('\t'.join(map(str,tri))+ '\t'+'\t'.join(str(F(moments[tuple(v for v in tri if v!=h)+(h,)],D)) for h in tri)+'\n')
    print('PASS templates=463 physical_four_sets=123410 old_coordinates=98758 full_wedges=37023')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('vector','moments','four'):parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();generate(args.vector,args.moments,args.four)

if __name__=='__main__':main()
