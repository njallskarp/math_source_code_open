#!/usr/bin/env python3
"""Eight complete equality cases, conditional on the complete R(3,5;13) catalog."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

CASES = (
    ((0,0,0),()), ((0,0,1),(0,)),
    ((0,0,2),(0,2)), ((0,0,2),(0,4)),
    ((0,1,1),(0,1)), ((0,1,2),(0,1,2)),
    ((0,1,2),(0,1,5)), ((0,2,2),(0,1,5,6)),
)


def formula(pattern, omitted):
    H=tuple(range(13));v=13;x=14;tail=tuple(range(15,21))
    groups=(tail[:2],tail[2:4],tail[4:])
    edges={e:i+1 for i,e in enumerate(it.combinations(range(21),2))}
    fixed={edges[tuple(sorted((v,w)))]:w in H for w in range(21) if w!=v}
    fixed.update({edges[a,b]:(a-b)%13 in (1,5,8,12) for a,b in it.combinations(H,2)})
    fixed.update({edges[a,b]:all(not (a in g and b in g) for g in groups) for a,b in it.combinations(tail,2)})
    redS={w for g,k in zip(groups,pattern) for w in g[:k]}
    fixed.update({edges[x,w]:w in redS for w in tail})
    fixed.update({edges[h,x]:h not in omitted for h in H})
    clauses=[]
    for size,red in ((4,True),(5,False)):
        for q in it.combinations(range(21),size):
            row=[]
            for pair in it.combinations(q,2):
                e=edges[pair]
                if e in fixed:
                    if fixed[e]!=red:break
                else:row.append(-e if red else e)
            else:clauses.append(row)
    for e,r in fixed.items():clauses.append([e if r else -e])
    return (f'p cnf 210 {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    result=[]
    for i,(pattern,omitted) in enumerate(CASES):
        raw=formula(pattern,omitted);(args.output/f'case-{i}.cnf').write_bytes(raw)
        result.append({'case':i,'pattern':pattern,'omitted_core':omitted,'variables':210,
                       'fixed_edges':132,'free_edges':78,'clauses':int(raw.splitlines()[0].split()[3]),
                       'cnf_sha256':hashlib.sha256(raw).hexdigest()})
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
