#!/usr/bin/env python3
"""Optional exact discovery model; the checked public witness needs no solver.

The triangle_system function is adapted verbatim, apart from its name,
from the height-3401 discovery source. See README.md for provenance.
"""
import argparse
import itertools as it
import json
import math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from witness import previous, canonical as four_canonical, require

old=previous()
E,H,X,base,canonical=old.E,old.H,old.X,old.base,old.canonical

def triangle_system():
    _, classes = base()
    triples = tuple(it.combinations(range(43), 3))
    groups = sorted({canonical(t, classes)[0] for t in triples})
    ids = {key: i for i, key in enumerate(groups)}
    representatives, decode = {}, {}
    for triple in triples:
        key, order = canonical(triple, classes)
        gid = ids[key]
        representatives.setdefault(gid, order)
        decode[triple] = gid, order

    def form(triple, red=(), blue=()):
        gid, order = decode[tuple(sorted(triple))]
        pairs = [frozenset(p) for p in it.combinations(order, 2)]
        rr = [pairs.index(frozenset(pair)) for pair in red]
        bb = [pairs.index(frozenset(pair)) for pair in blue]
        return Counter({8*gid+mask: 1 for mask in range(8)
                        if all(mask >> i & 1 for i in rr)
                        and all(not (mask >> i & 1) for i in bb)})

    def plus(parts):
        row = Counter()
        for part in parts:
            row.update(part)
        return row

    rows = []
    for order in representatives.values():
        rows.append((form(order), "=", F(1)))
        for pair in it.combinations(order, 2):
            rows.append((form(order, red=[pair]), "=", classes.edge_value(*pair)))
        active = [h for h in order if h in H and set(order)-{h} <= X]
        if active:
            h = active[0]
            a, b = sorted(set(order)-{h})
            m = (F(1, 7), F(14, 65), F(7, 26))[(a in E)+(b in E)]
            rows.append((form(order, blue=[(a, h), (b, h)]), "=", m))
    for h in range(43):
        others = [v for v in range(43) if v != h]
        row = plus(form((a, b, h), red=tuple(it.combinations((a, b, h), 2)))
                   for a, b in it.combinations(others, 2))
        rows.append((row, "=", F(93 if h in E else 100)))
        for a in others:
            row = plus(form((a, b, h), red=[(h, a), (h, b)]) for b in others if b != a)
            rows.append((row, "=", (19 if h in E else 20)*classes.edge_value(a, h)))
    for a, b in it.combinations(range(43), 2):
        others = [h for h in range(43) if h not in (a, b)]
        row = plus(form((a, b, h), red=tuple(it.combinations((a, b, h), 2))) for h in others)
        rows.append((row, "<=", 13*classes.edge_value(a, b)))
        row = plus(form((a, b, h), blue=tuple(it.combinations((a, b, h), 2))) for h in others)
        rows.append((row, "<=", 13*(1-classes.edge_value(a, b))))
        if a in H and b in H and classes.edge_value(a, b) == 1:
            row = plus(form((a, b, h), red=tuple(it.combinations((a, b, h), 2))) for h in X)
            rows.append((row, "=", F(7)))
    require(len(groups) == 171 and len(rows) == 4389, "discovery scope")
    return groups, rows


def system():
    _,classes=base();groups,rows=triangle_system();ids={key:i for i,key in enumerate(groups)}
    edges={(a,b):classes.edge_value(a,b) for a in range(43) for b in range(43) if a!=b}
    representatives={}
    for vertices in it.combinations(range(43),4):
        key,order=four_canonical(vertices,classes,edges);representatives.setdefault(key,order)
    keys=sorted(representatives,key=lambda k:(k[0],tuple(map(str,k[1]))))
    require(len(keys)==463,'four-vertex templates')
    pairs=list(it.combinations(range(4),2))
    for gid,key in enumerate(keys):
        vs=representatives[key];offset=1368+64*gid
        rows.append((Counter({offset+mask:1 for mask in range(64)}),'=',F(1)))
        for tri in it.combinations(vs,3):
            key3,_=canonical(tri,classes);tid=ids[key3]
            # Include every tie; no automorphism invariance is assumed silently.
            for order in it.permutations(tri):
                observed=(tuple(classes.TYPE_INDEX[classes.VERTEX_TYPE[v]] for v in order),tuple(classes.edge_value(a,b) for a,b in it.combinations(order,2)))
                if observed!=key3:continue
                bits=[pairs.index(tuple(sorted((vs.index(a),vs.index(b))))) for a,b in it.combinations(order,2)]
                for state in range(8):
                    row=Counter({offset+mask:1 for mask in range(64) if sum(((mask>>b)&1)<<j for j,b in enumerate(bits))==state})
                    row[8*tid+state]-=1;rows.append((row,'=',F(0)))
        for i,j in it.combinations(vs,2):
            if not({i,j}<=H and classes.edge_value(i,j)==1):continue
            a,b=sorted(set(vs)-{i,j})
            if not {a,b}<=X:continue
            red=pairs.index(tuple(sorted((vs.index(i),vs.index(j)))))
            blue=[pairs.index(tuple(sorted((vs.index(s),vs.index(t))))) for s in (a,b) for t in (i,j)]
            m=(F(1,7),F(14,65),F(7,26))[(a in E)+(b in E)]
            row=Counter({offset+mask:1 for mask in range(64) if mask>>red&1 and all(not(mask>>k&1) for k in blue)})
            rows.append((row,'=',F(3,14)*m))
    unique={(tuple(sorted((k,v) for k,v in row.items() if v)),relation,rhs) for row,relation,rhs in rows}
    rows=[(dict(row),relation,rhs) for row,relation,rhs in sorted(unique)]
    require(len(rows)==19659,'discovery row count')
    return keys,rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lp',type=Path);parser.add_argument('--solution',type=Path);parser.add_argument('--output',type=Path)
    args=parser.parse_args();keys,rows=system();n=1368+64*len(keys)
    if args.lp is not None:
        lines=['Minimize',' obj: 0 p0','Subject To']
        for k,(row,relation,rhs) in enumerate(rows):lines.append(f' row{k}:'+''.join(f' + {v} p{j}' for j,v in sorted(row.items()) if v)+f' {relation} {rhs}')
        lines+=['Bounds']+[f' 0 <= p{j} <= 1' for j in range(n)]+['End'];args.lp.write_text('\n'.join(lines)+'\n',encoding='ascii')
    if args.solution is not None:
        require(args.output is not None,'solution needs output');values=[F(0)]*n;seen=set()
        for line in args.solution.read_text().splitlines():
            if line.startswith('p'):
                name,value=line.split();index=int(name[1:]);require(0<=index<n and index not in seen,'solution coordinate');seen.add(index);values[index]=F(value)
        require(seen and min(values)>=0 and max(values)<=1,'exact solution box')
        for k,(row,relation,rhs) in enumerate(rows):
            val=sum(c*values[j] for j,c in row.items());require(val==rhs if relation=='=' else val<=rhs,f'exact discovery row {k}')
        D=math.lcm(*(v.denominator for v in values[1368:]));table=[]
        for gid,key in enumerate(keys):table.append({'types':list(key[0]),'edges':list(map(str,key[1])),'atoms':{str(k):str(int(x*D)) for k,x in enumerate(values[1368+64*gid:1368+64*(gid+1)]) if x}})
        args.output.write_text(json.dumps({'denominator':str(D),'templates':table},separators=(',',':'))+'\n',encoding='ascii')
    require(args.lp is not None or args.solution is not None,'no requested output')
    print('PASS discovery_variables=31000 discovery_rows=19659 four_templates=463')

if __name__=='__main__':main()
