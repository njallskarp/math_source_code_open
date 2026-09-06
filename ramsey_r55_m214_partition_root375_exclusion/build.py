#!/usr/bin/env python3
"""Generate the weaker physical UNSAT kernel and a selector-cut suffix."""
import argparse
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
ROOT_SOURCE_SHA='8fdccc44cab88d462cc122c055a9c54cffbefc957a73b6eeff84aa57a9e2256e'
KEY=('C77partition',13,0,'HO')


def require(ok,message):
    if not ok:raise ValueError(message)


def root():
    path=REPO/'ramsey_r55_m214_pair_normalization/pair_roots.py'
    require(hashlib.sha256(path.read_bytes()).hexdigest()==ROOT_SOURCE_SHA,'root source identity')
    spec=importlib.util.spec_from_file_location('original_roots',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    require(list(mod.definitions()).index(KEY)==375,'root index')
    record=mod.root(*KEY)
    require(mod.canonical_bytes(record)==(HERE/'root.json').read_bytes(),'full root descriptor')
    return record


def kernel():
    record=root();p,q=record['anomalies'];vertices=sorted(record['anchors']+record['cells'][4]+[q])
    edge={pair:i+1 for i,pair in enumerate(it.combinations(range(43),2))};clauses=[]
    for five in it.combinations(vertices,5):
        row=[edge[pair] for pair in it.combinations(five,2)];clauses.extend([row,[-x for x in row]])
    for a,b,value in record['edge_units']:
        if a in vertices and b in vertices:clauses.append([edge[a,b]*(1 if value else -1)])
    clauses.append([-edge[p,q]])
    for w in vertices:
        if w in record['partition']['one_red_to_pair']:
            a=edge[tuple(sorted((w,p)))];b=edge[tuple(sorted((w,q)))];clauses.extend([[a,b],[-a,-b]])
    require(len(vertices)==16 and len(clauses)==8794,'kernel dimensions')
    return 'p cnf 903 8794\n'+''.join(' '.join(map(str,row))+' 0\n' for row in clauses)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel',type=Path,required=True);parser.add_argument('--cut',type=Path);parser.add_argument('--r34',type=Path)
    args=parser.parse_args();data=kernel();args.kernel.write_text(data,encoding='ascii')
    if args.cut is not None:args.cut.write_text('-1 x13620 >= 0 ;\n',encoding='ascii')
    if args.r34 is not None:
        pairs={p:i+1 for i,p in enumerate(it.combinations(range(9),2))}
        rows=[[-pairs[p] for p in it.combinations(t,2)] for t in it.combinations(range(9),3)]
        rows += [[pairs[p] for p in it.combinations(t,2)] for t in it.combinations(range(9),4)]
        rows += [[-pairs[0,w]] for w in range(4,9)]
        args.r34.write_text('p cnf 36 215\n'+''.join(' '.join(map(str,row))+' 0\n' for row in rows),encoding='ascii')
    print(json.dumps({'status':'GENERATED_COMPLETE_ROOT375_KERNEL','root_index':375,'selector':13620,'variables':903,'clauses':8794,'sha256':hashlib.sha256(data.encode()).hexdigest()},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
