#!/usr/bin/env python3
"""Exact arithmetic for defect-compatible high pairs; see PROOF.md."""
from itertools import product
from math import comb
from pathlib import Path
import argparse,hashlib,json

def lower(k,same):
    if not 0<=k<=21:raise ValueError("table domain is 0..21")
    odd_coordinates=k if k%2==0 else 41-k
    free_norm=max(odd_coordinates,4*k-odd_coordinates) if same else odd_coordinates
    numerator=41*k*k-81*k+free_norm
    return -((-numerator)//8)

def high(k,same):
    return max(0,-((-(lower(k,same)-9*comb(k,2)))//4))

def cells(color,c,a):
    # Colors are always original red=1, blue=0.
    quota=5 if color else 4
    e=[a,quota-a,quota-a,9-2*quota+a]
    zcell=3 if color else 0
    sizes=[c,20-c,20-c,c+1]
    central=[sizes[j]-e[j]-int(j==zcell) for j in range(4)]
    return e,central,zcell

def roots():
    out=[]
    # Case 0/1: second defect is z; case 2/3: it is a central vertex w.
    # Even cases give y blue excess; odd cases give y red excess.
    for case,color,c,eta,a in product(range(4),range(2),range(10,14),range(2),range(10)):
        e,central,_=cells(color,c,a)
        ycell=0 if eta==color else 3
        if min(e+central)<0 or e[ycell]<1:continue
        for wcell in (range(4) if case>=2 else [-1]):
            if wcell>=0 and central[wcell]<1:continue
            out.append([case,color,c,eta,a,wcell])
    return out

def certificate():
    bounds=[[k,int(same),lower(k,same),high(k,same)]
            for k,same in product(range(22),(False,True))]
    multiplicities=[]
    for n in (19,20,21):
        vals=[high(a,True)+high(n-a,False) for a in range(n+1)]
        multiplicities.append([n,min(vals),(n-15)//2])
    return {"schema":1,"bounds":bounds,"multiplicities":multiplicities,"roots":roots()}

def encoded():
    return (json.dumps(certificate(),sort_keys=True,separators=(',',':'))+'\n').encode()

def report():
    data=certificate()
    return {"threshold_nine_pair_sum":lower(9,False),"threshold_nine_all_at_most_nine":9*comb(9,2),
            "same_blue_star_sharp_eight_pair_sum":lower(8,True),
            "compatible_high_pairs_by_exact_blue_set":[row[1]for row in data["multiplicities"]],
            "disjoint_pairs_by_exact_blue_set":[row[2]for row in data["multiplicities"]],
            "marked_cell_keys":len(data["roots"]),"retained_raw_single_anchor_B_keys":12,
            "certificate_sha256":hashlib.sha256(encoded()).hexdigest()}

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--write",type=Path);args=parser.parse_args()
    if args.write:args.write.write_bytes(encoded())
    print(json.dumps(report(),sort_keys=True,indent=2))
