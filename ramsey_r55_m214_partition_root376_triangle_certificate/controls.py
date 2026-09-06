#!/usr/bin/env python3
"""Definition-level physical identity, guard, and corruption controls."""
import itertools as it
import argparse
import json
from pathlib import Path
import random
import tempfile
import audit
from check_rup import require,verify

HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--opb',type=Path,required=True);args=parser.parse_args()
    root,_=audit.root_check(HERE/'root.json');fixed={(a,b):v for a,b,v in root['edge_units']};rng=random.Random(376)
    pairs=list(it.combinations(range(43),2));count=0
    for _ in range(256):
        red={e:(fixed[e] if e in fixed else rng.randrange(2)) for e in pairs}
        edge=lambda a,b:red[tuple(sorted((a,b)))]
        # Direct graph definitions, not audit.py's symbolic coefficient map.
        triangles=0
        for anchor in (0,1):
            neighbors=[w for w in range(43) if w!=anchor and edge(w,anchor)]
            triangles+=sum(edge(a,b) for a,b in it.combinations(neighbors,2))
        incidences=sum(edge(h,e) for h in range(15,28) for e in range(2,15))
        partition=sum(edge(h,p) for h in range(15,28) for p in (28,29))
        core=2*sum(edge(a,b) for a,b in it.combinations(range(15,28),2))
        within=sum(edge(a,b) for cell in (list(range(2,8))+[28],list(range(8,14))+[29]) for a,b in it.combinations(cell,2))
        footprint=sum(edge(14,h) for h in range(15,28))
        require(triangles-incidences-partition==core+within-footprint+26,'literal physical identity');count+=1
    guards=0
    for value,x,y in it.product((0,1),repeat=3):
        condition=x-y>=0 if value else -x-y>=-1
        require(condition==(y==0 or x==value),'unit selector guard');guards+=1
    for total in range(14):
        for y in (0,1):
            require((total-6*y>=0 and -total-7*y>=-13)==(y==0 or total==6),'E-incidence guard');guards+=1
    for x,z,y in it.product((0,1),repeat=3):
        require((x+z-y>=0 and -x-z-y>=-2)==(y==0 or x+z==1),'partition guard');guards+=1
    base=json.loads((HERE/'certificate.json').read_text());rejected=0
    with tempfile.TemporaryDirectory() as directory:
        target=Path(directory)/'mutation.json'
        for mode in ('looser_turan','wrong_rhs','missing_row','negative_multiplier','no_cancellation'):
            c=json.loads(json.dumps(base))
            if mode=='looser_turan':c['inequalities'][0]['rhs']=17
            elif mode=='wrong_rhs':c['equality']['rhs']=82
            elif mode=='missing_row':c['inequalities'].pop()
            elif mode=='negative_multiplier':c['inequality_multipliers'][0]=-1
            else:c['equality_multiplier']=0
            target.write_text(json.dumps(c))
            try:audit.farkas_check(target)
            except ValueError:rejected+=1
            else:raise ValueError('accepted damaged Farkas certificate')
        for mode in ('HO','k1','missing_partition'):
            r=json.loads(json.dumps(root))
            if mode=='HO':r['key'][3]='HO'
            elif mode=='k1':r['key'][2]=1
            else:r['partition']['one_red_to_pair'].remove(15)
            target.write_text(json.dumps(r))
            try:audit.root_check(target)
            except ValueError:rejected+=1
            else:raise ValueError('accepted changed root scope')
        # An empty proof is never a contradiction certificate.
        target.write_text('')
        try:verify([],target,36)
        except ValueError:rejected+=1
        else:raise ValueError('accepted empty proof')
    require((count,guards,rejected)==(256,44,9),'control coverage')
    _,first=audit.root_check(HERE/'root.json');wanted,_,_=audit.physical_rows(root,first);row=min(wanted)
    with args.opb.open('rb') as source:prefix=[source.readline() for _ in range(row+1)]
    require(all(prefix),'parent prefix missing');source_rejections=0
    with tempfile.TemporaryDirectory() as directory:
        target=Path(directory)/'damaged.opb';parts=prefix[-1].split();parts[-2]=str(int(parts[-2])+1).encode()
        target.write_bytes(b''.join(prefix[:-1])+b' '.join(parts)+b'\n')
        try:audit.check_stream(target,wanted)
        except ValueError as error:
            require(str(error)=='physical OPB row '+str(row),'wrong altered-source rejection');source_rejections+=1
        else:raise ValueError('accepted altered physical source row')
        target.write_bytes(b''.join(prefix))
        try:audit.check_stream(target,wanted)
        except ValueError as error:
            require(str(error)=='entire parent identity','wrong incomplete-source rejection');source_rejections+=1
        else:raise ValueError('accepted incomplete parent stream')
    require(source_rejections==2,'source corruption controls')
    print(json.dumps({'status':'PASS','literal_physical_identity_assignments':count,'selector_guard_cases':guards,'certificate_and_scope_mutations_rejected':rejected,'physical_source_corruptions_rejected':source_rejections},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
