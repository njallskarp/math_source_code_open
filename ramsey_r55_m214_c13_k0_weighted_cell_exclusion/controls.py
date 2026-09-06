#!/usr/bin/env python3
"""Literal graph identities and rejection of altered proof inputs."""
import argparse
import itertools as it
import json
from pathlib import Path
import random
import subprocess
import tempfile
import audit
from check_rup import require,verify


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--cnfs',type=Path,required=True);parser.add_argument('--drat-trim',type=Path,required=True)
    args=parser.parse_args();cases,_=audit.equality_cover();rng=random.Random(214007)
    # These assignments need not obey the Ramsey constraints: the identity
    # must hold for every physical graph with the anchor incidence pattern.
    fixed={(0,1):1};H=set(range(15,28));A=set(range(2,8))|{28};B=set(range(8,14))|{29}
    for w in range(2,43):fixed[0,w]=int(w in H|A);fixed[1,w]=int(w in H|B)
    for _ in range(128):
        values={e:fixed[e] if e in fixed else rng.randrange(2) for e in it.combinations(range(43),2)}
        x=lambda a,b:values[tuple(sorted((a,b)))]
        triangles=sum(sum(x(a,b) for a,b in it.combinations([w for w in range(43) if w!=v and x(v,w)],2)) for v in (0,1))
        inc=sum(x(h,e) for h in H for e in range(2,15))
        weighted=sum(x(a,b) for S in (A,B) for a,b in it.combinations(sorted(S),2))+sum(x(c,h) for c in (28,29) for h in H)
        core=2*sum(x(a,b) for a,b in it.combinations(sorted(H),2));foot=sum(x(14,h) for h in H)
        require(triangles-inc==26+weighted+core-foot,'literal triangle identity')
    guards=0
    for value,x,y in it.product((0,1),repeat=3):
        require((x-y>=0 if value else -x-y>=-1)==(y==0 or x==value),'unit guard');guards+=1
    for total in range(14):
        for y in (0,1):require((total-6*y>=0 and -total-7*y>=-13)==(y==0 or total==6),'incidence guard');guards+=1
    rejected=0
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'mutated'
        for i,(pat,J) in enumerate(cases):
            lines=(args.cnfs/f'case-{i}.cnf').read_text().splitlines()
            fields=lines[-1].split();fields[0]=str(-int(fields[0]));lines[-1]=' '.join(fields)
            path.write_text('\n'.join(lines)+'\n')
            try:audit.audit_cnf(path,pat,J)
            except ValueError:rejected+=1
            else:raise ValueError('accepted flipped physical unit')
        base=json.loads((audit.HERE/'certificate.json').read_text())
        for mode in ('loosen','wrong_rhs','negative','missing','no_cancel'):
            c=json.loads(json.dumps(base))
            if mode=='loosen':c['inequalities'][0]['rhs']=25
            elif mode=='wrong_rhs':c['equality']['rhs']=95
            elif mode=='negative':c['inequality_multipliers'][0]=-1
            elif mode=='missing':c['inequalities'].pop()
            else:c['equality_multiplier']=0
            path.write_text(json.dumps(c))
            try:audit.farkas(path)
            except ValueError:rejected+=1
            else:raise ValueError('accepted invalid Farkas certificate')
        path.write_text('')
        try:verify([],path,36)
        except ValueError:rejected+=1
        else:raise ValueError('accepted absent small Ramsey proof')
        result=subprocess.run([str(args.drat_trim.resolve()),str((args.cnfs/'case-0.cnf').resolve()),str(path)],capture_output=True,text=True)
        require(result.returncode!=0 and '\ns VERIFIED\n' not in result.stdout,'native checker accepted absent proof');rejected+=1
    require(guards==36 and rejected==15,'complete control count')
    print(json.dumps({'status':'PASS','literal_identity_assignments':128,'guard_truth_cases':guards,'mutations_rejected':rejected},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
