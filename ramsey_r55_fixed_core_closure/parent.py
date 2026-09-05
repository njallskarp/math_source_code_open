"""Bounded discovery of a complete fully-visible three-anchor interface.

SAT models are discovery output; UNSAT/UNKNOWN are not standalone theorems.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
from threading import Timer
from time import monotonic

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

BASE = Path(__file__).parent
sys.path.insert(0,str(BASE))
from seed import construct


def validate_candidate(found,original,fixed,quotas,mixed):
    if any((p in found) != c for p,c in fixed.items()):
        raise ValueError("fixed edge decoding")
    adjacency=[set() for _ in range(43)]
    for u,v in found:
        adjacency[u].add(v)
        adjacency[v].add(u)
    if len(found)!=452 or Counter(map(len,adjacency))!=Counter({20:8,21:26,22:9}):
        raise ValueError("global profile")
    neighborhoods=[]
    for r in (0,3,9):
        for c in (True,False):
            vertices=adjacency[r] if c else set(range(43))-adjacency[r]-{r}
            ordered=sorted(vertices)
            neighborhoods.append(vertices)
            original_count=sum((u,v) in original for u,v in combinations(ordered,2))
            if sum(v in adjacency[u] for u,v in combinations(ordered,2))!=original_count:
                raise ValueError("local edge profile")
            for size,target in ((4,c),(5,not c)):
                if any(all((v in adjacency[u])==target for u,v in combinations(subset,2)) for subset in combinations(ordered,size)):
                    raise ValueError("local Ramsey condition")
    if quotas:
        cells=[[v for v in range(43) if v not in (0,3,9) and
                sum(int(v in adjacency[r]) << (2-i) for i,r in enumerate((0,3,9)))==s] for s in range(8)]
        for s in range(8):
            for t in range(s,8):
                pairs=list(combinations(cells[s],2)) if s==t else [tuple(sorted((u,v))) for u in cells[s] for v in cells[t]]
                if sum(p in found for p in pairs)!=sum(p in original for p in pairs):
                    raise ValueError("cell edge count")
    if mixed:
        visible={pair for pair in combinations(range(43),2) if set(pair)&{0,3,9} or any(set(pair)<=n for n in neighborhoods)}
        for subset in combinations(range(43),5):
            pairs=list(combinations(subset,2))
            if all(p in visible for p in pairs) and len({p in found for p in pairs})==1:
                raise ValueError("fully visible monochromatic five-set")


def build(free_cores=False, quotas=True, mixed=True):
    data=json.loads((BASE/"SEED.json").read_text())
    red=construct(data)
    roots=(0,3,9)
    pairs=list(combinations(range(43),2))
    edge=lambda u,v:tuple(sorted((u,v)))
    color=lambda u,v:edge(u,v) in red
    sig={v:tuple(int(color(r,v)) for r in roots) for v in range(43) if v not in roots}
    fixed={p:p in red for p in pairs if set(p)&set(roots) or (not free_cores and ((p[1]<=22) or (p[0]>=23)))}
    pool=IDPool()
    variables={p:pool.id(p) for p in pairs if p not in fixed}
    clauses=[]
    origins=Counter()

    def prohibit(vertices,target,origin):
        clause=[]
        for pair in combinations(vertices,2):
            p=edge(*pair)
            if p in fixed:
                if fixed[p] != target: return
            else:
                clause.append(-variables[p] if target else variables[p])
        clauses.append(clause)
        origins[origin]+=1

    def bound(subpairs,low,high,origin):
        known=sum(fixed[p] for p in subpairs if p in fixed)
        literals=[variables[p] for p in subpairs if p in variables]
        lo,hi=low-known,high-known
        if hi<0 or lo>len(literals):
            clauses.append([])
        else:
            if hi<len(literals):
                clauses.extend(CardEnc.atmost(literals,bound=hi,vpool=pool,encoding=EncType.totalizer if len(literals)>60 else EncType.seqcounter).clauses)
            if lo>0:
                clauses.extend(CardEnc.atleast(literals,bound=lo,vpool=pool,encoding=EncType.totalizer if len(literals)>60 else EncType.seqcounter).clauses)
        origins[origin]+=1

    for root in roots:
        for c in (True,False):
            vertices=[v for v in range(43) if v!=root and color(root,v)==c]
            for size,target in ((4,c),(5,not c)):
                for subset in combinations(vertices,size):
                    prohibit(subset,target,"local")
            subpairs=list(combinations(vertices,2))
            target=sum(p in red for p in subpairs)
            if not quotas:
                bound(subpairs,target,target,"local_edges")
    outside=sorted(sig)
    if mixed:
        for subset in combinations(outside,5):
            support={sig[v] for v in subset}
            if not all({s[i] for s in support}=={0,1} for i in range(3)):continue
            if any(tuple(1-bit for bit in s) in support for s in support):continue
            for c in (True,False):prohibit(subset,c,"mixed")
    for v in range(43):
        incident=[p for p in pairs if v in p]
        low,high=(22,22) if v==0 else ((21,22) if v<=22 else (20,21))
        bound(incident,low,high,"degrees")
    if not quotas:
        bound(pairs,452,452,"edges")
    if quotas:
        cells=[[v for v in outside if sig[v]==tuple((s>>(2-i))&1 for i in range(3))] for s in range(8)]
        for s in range(8):
            for t in range(s,8):
                subpairs=list(combinations(cells[s],2)) if s==t else [edge(u,v) for u in cells[s] for v in cells[t]]
                target=sum(p in red for p in subpairs)
                bound(subpairs,target,target,"cell_counts")
    return data,red,fixed,variables,clauses,origins
