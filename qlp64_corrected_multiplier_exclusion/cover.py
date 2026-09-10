"""Build and audit the corrected necessary-condition cover, without final claims."""
from itertools import product
import hashlib
import json
from pathlib import Path
import subprocess
import reference as ref

def read(path):
    lines=path.read_text().splitlines()
    d,n=map(int,lines[0].split())
    vals=[list(map(int,line.split())) for line in lines[1:]]
    assert len(vals)==n and all(len(v)==4*d for v in vals)
    return [tuple(tuple(v[i*d:(i+1)*d]) for i in range(4)) for v in vals]

def write(path,qs):
    d=len(qs[0][0])
    path.write_text(f'{d} {len(qs)}\n'+'\n'.join(
        ' '.join(str(v) for r in q for v in r) for q in qs)+'\n')

def native(work,qs,stem,units=False):
    source,output=work/(stem+'-input.txt'),work/(stem+'-output.txt')
    write(source,qs)
    args=[str(work/'match'),str(source),str(output)]
    if units: args.append('--units')
    result=json.loads(subprocess.check_output(args,text=True))
    assert result['begin']==0 and result['end']==result['total_input']==len(qs)
    result.pop('seconds')
    return read(output),result

def box_audit(d,parents):
    """Complete symmetric box; no production doubling formulas are used."""
    n,b=2*d,64//(4*d)
    fibers={(r,int(i==3)):set() for q in parents for i,r in enumerate(q)}
    box=children=0
    for free in product(range(-b,b+1),repeat=d+1):
        box+=1
        row=free+free[-2:0:-1]
        s=sum(row)
        if s not in (0,1) or (row[0]-b-s)%2 or (row[d]-b)%2:
            continue
        if sum(v*v for v in row)>65-64//n:
            continue
        parent=tuple(row[j]+row[j+d] for j in range(d))
        if (parent,s) in fibers:
            fibers[parent,s].add(row);children+=1
    for (parent,s),expected in fibers.items():
        assert set(ref.lifts(parent,s))==expected
    return {'child_length':n,'symmetric_box_size':box,'parent_fibers':len(fibers),
            'children':children,'empty_fibers':sum(not x for x in fibers.values()),
            'complete_sets_equal':True}

def build(work):
    if not __debug__: raise RuntimeError('run Python without -O')
    zero,special=ref.root_rows(0),ref.root_rows(1)
    raw=list(ref.match((zero,zero,zero,special),ref.target(4)))
    qs=sorted({ref.canonical(q) for q in raw})
    result={'root_rows':[len(zero),len(special)],'labelled_roots':len(raw),
            'canonical4':len(qs),'layers':[],'box_audits':[]}
    for d in (4,8):
        result['box_audits'].append(box_audit(d,qs))
        actual,stats=native(work,qs,f'length{2*d}')
        qs=ref.extend(qs)
        assert actual==qs
        result['layers'].append(dict(stats,sha256=ref.digest(qs),python_entries_equal=True))
    qs=sorted({ref.unit_canonical(q) for q in qs})
    result['unit16']=len(qs)
    write(work/'unit16.txt',qs)
    result['box32']=json.loads(subprocess.check_output(
        [str(work/'box_audit'),str(work/'unit16.txt')],text=True))
    qs,stats=native(work,qs,'length32',units=True)
    result['layers'].append(dict(stats,sha256=ref.digest(qs)))
    # Check every emitted row, full compressed equation and chosen unit representative.
    for q in qs:
        assert all(sum(r)==s for r,s in zip(q,(0,0,0,1)))
        assert tuple(sum(v) for v in zip(*(ref.paf(r) for r in q)))==ref.target(32)
        assert ref.unit_canonical(q)==q
    text=str(len(qs))+'\n'+'\n'.join(' '.join(str(v) for r in q for v in r) for q in qs)+'\n'
    (work/'compressed.txt').write_text(text)
    result['input_sha256']=hashlib.sha256(text.encode()).hexdigest()
    result['parents']=len(qs)
    return result
