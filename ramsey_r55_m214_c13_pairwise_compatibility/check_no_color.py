#!/usr/bin/env python3
"""Definition-level checker for the duplicate-footprint no-color obstruction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

N=13
DIFF=frozenset((1,5,8,12))
SOURCE_HASH="8b8454e0924238e08561cd2d456b5f15940b9e45bfc1af5a46e3c172657d734f"

def edge(i: int,j: int)->bool:
    return i!=j and ((i-j)%N) in DIFF

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument("certificate",type=Path);args=parser.parse_args()
    raw=args.certificate.read_bytes();data=json.loads(raw)
    fields={"blue_core_triple","cell","mask","multiplicity","red_anchor","red_core_edge","source_certificate_sha256"}
    if not isinstance(data,dict) or set(data)!=fields:raise ValueError("certificate fields")
    if data["source_certificate_sha256"]!=SOURCE_HASH:raise ValueError("source hash")
    if data["cell"]!="A" or data["red_anchor"]!="u":raise AssertionError("common red anchor")
    if data["multiplicity"]!=2:raise AssertionError("duplicate multiplicity")
    text=data["mask"]
    if not isinstance(text,str) or len(text)!=4 or text!=text.lower():raise ValueError("mask encoding")
    mask=int(text,16)
    if not 0<=mask<1<<N:raise ValueError("mask range")
    core_edges=tuple(pair for pair in itertools.combinations(range(N),2) if edge(*pair))
    triples=tuple(t for t in itertools.combinations(range(N),3)
                  if all(not edge(*pair) for pair in itertools.combinations(t,2)))
    fours=tuple(t for t in itertools.combinations(range(N),4)
                if all(not edge(*pair) for pair in itertools.combinations(t,2)))
    fives=tuple(t for t in itertools.combinations(range(N),5)
                if all(not edge(*pair) for pair in itertools.combinations(t,2)))
    transversals=frozenset(m for m in range(1<<N)
                          if all(m & sum(1<<i for i in four) for four in fours))
    if (len(core_edges),len(triples),len(fours),len(fives),len(transversals))!=(26,78,39,0,3459):
        raise AssertionError("core census")
    if mask not in transversals:raise AssertionError("mask not a legal footprint")
    red_edge=data["red_core_edge"]
    blue_triple=data["blue_core_triple"]
    if (not isinstance(red_edge,list) or len(red_edge)!=2 or red_edge!=sorted(set(red_edge))
            or any(not isinstance(i,int) or not 0<=i<N for i in red_edge)):
        raise ValueError("red edge")
    if not edge(*red_edge) or any(not(mask>>i&1) for i in red_edge):
        raise AssertionError("red edge is not in both identical footprints")
    if (not isinstance(blue_triple,list) or len(blue_triple)!=3 or blue_triple!=sorted(set(blue_triple))
            or any(not isinstance(i,int) or not 0<=i<N for i in blue_triple)):
        raise ValueError("blue triple")
    if any(edge(*pair) for pair in itertools.combinations(blue_triple,2)):
        raise AssertionError("blue triple is not core-independent")
    if any(mask>>i&1 for i in blue_triple):
        raise AssertionError("blue triple is not disjoint from the footprint union")
    result={"certificate_sha256":hashlib.sha256(raw).hexdigest(),"core_independent_fours":len(fours),
            "core_transversals":len(transversals),"duplicate_mask":text,"maximum_multiplicity":1,
            "red_edge_forbidden":True,"blue_edge_forbidden":True,"status":"VERIFIED NO-COLOR PAIR OBSTRUCTION"}
    print(json.dumps(result,sort_keys=True,separators=(",",":")))
if __name__=="__main__":main()
