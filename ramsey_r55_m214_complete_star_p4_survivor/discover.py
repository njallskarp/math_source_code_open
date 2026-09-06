#!/usr/bin/env python3
"""Optional exact candidate search with the complete star-event row family."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,importlib.util,itertools as it

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'ramsey_r55_m214_anchor_linked_p4_survivor/discover.py'
# Pinned discovery code is not imported by the certificate checker.
PIN='5faf67481ea3ae3f0971c2f97d1f16349fa56310ae60b06d0984c36f9fb80529'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=PIN:raise ValueError('changed candidate generator')
spec=importlib.util.spec_from_file_location('parent_discover',SOURCE)
parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)

def strengthened_model(base):
    m=parent.Model();m.initial();m.base(base)
    before=len(m.rows)
    # Retain every anchor-zero forbidden state explicitly.
    for color in (0,1):
        ns={v for v in range(1,43) if m.units[0,v]==color}
        for ts,vs in m.reps.items():
            if len(vs)==4 and set(vs)<=ns:
                m.add(m.event(vs,**{'red' if color else 'blue':list(it.combinations(vs,2))}),'=',0)
    anchor_rows=len(m.rows)-before;before=len(m.rows)
    # Every anchor and every disjoint four-set, modulo candidate symmetry.
    # No infeasibility conclusion about the unrestricted LP uses this quotient.
    for hc,cell in enumerate(m.cells):
        h=cell[0]
        for ts in it.combinations_with_replacement(range(len(m.cells)),4):
            counts=Counter(ts)
            if any(n>len(m.cells[t])-(t==hc) for t,n in counts.items()):continue
            vs=tuple(v for t,n in counts.items() for v in [v for v in m.cells[t] if v!=h][:n])
            star=[m.coords[m.edge[tuple(sorted((h,v)))]] for v in vs]
            for color in (0,1):
                event=m.event(vs,**{'red' if color else 'blue':list(it.combinations(vs,2))})
                m.addparts([(-1,event)]+[(-1 if color else 1,e) for e in star],'>=',-4 if color else 0)
    print('new anchor-zero and global-star discovery rows',anchor_rows,len(m.rows)-before,flush=True)
    return m

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--lp',type=Path);p.add_argument('--solution',type=Path);p.add_argument('--certificate',type=Path);a=p.parse_args()
    parent.require(a.lp is not None or (a.solution is not None and a.certificate is not None),'request LP or exact solution conversion')
    m=strengthened_model(a.base)
    if a.lp:m.write(a.lp)
    if a.solution:m.certificate(m.read(a.solution),a.certificate)

if __name__=='__main__':main()
