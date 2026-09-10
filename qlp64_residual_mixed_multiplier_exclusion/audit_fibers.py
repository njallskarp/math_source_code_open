"""Product-box row oracle and independent per-coordinate energy minima."""
from itertools import product
import hashlib
import json
from pathlib import Path
import subprocess
import time

W=Path(__file__).resolve().parent


def choices(parent,kind):
    n=2*len(parent);b=32//n
    return [tuple((x,v-x) for x in range(-b,b+1)
                  if abs(v-x)<=b and (kind==0 or j%2==0 or
                      (x-b)%2==0 and (v-x-b)%2==0))
            for j,v in enumerate(parent)]


def row_minimum(parent,kind):
    return sum(min(x*x+y*y for x,y in options) for options in choices(parent,kind))


def caps32(q):
    minima=[row_minimum(r,kind) for kind,r in enumerate(q)]
    # Independently challenge the closed-form bounds on every input parent.
    formula=[sum(map(abs,q[0]))]+[16+sum(abs(v) for v in r[::2]) for r in q[1:]]
    assert minima==formula
    if 2*minima[0]+sum(minima[1:])>63:return None
    a,b,c=minima
    return ((63-b-c)//2,63-2*a-c,63-2*a-b)


def reference(parent,kind,cap):
    n=2*len(parent);b=32//n;out=[];box=0
    for assignment in product(*choices(parent,kind)):
        box+=1
        if sum(x*x+y*y for x,y in assignment)>cap:continue
        row=tuple(x for x,y in assignment)+tuple(y for x,y in assignment)
        code=0
        for v in row:code=code*(2*b+1)+v+b
        assert code<2**64
        out.append(code)
    return sorted(out),box


def cases():
    out=set();budgets=[]
    for d,file in ((4,'cover4.json'),(8,'quotient8.json'),(16,'quotient16.json')):
        qs=json.loads((W/file).read_text());retained=0
        for q in qs:
            caps=caps32(q) if d==16 else ((65-32//d)//2,65-32//d,65-32//d)
            if caps is None:continue
            retained+=1
            for kind,(parent,cap) in enumerate(zip(q,caps)):
                out.add((2*d,min(kind,1),cap,tuple(parent)))
        budgets.append(dict(parent_length=d,parents=len(qs),retained=retained))
    return sorted(out),budgets


def main():
    cs,budgets=cases();input_path=W/'fiber-input.txt'
    input_path.write_text(str(len(cs))+'\n'+'\n'.join(' '.join(map(str,(n,k,cap,*p))) for n,k,cap,p in cs)+'\n')
    subprocess.run([str(W/'fiber_export'),str(input_path),str(W/'fiber-output.txt')],check=True)
    totals={};started=time.monotonic()
    with (W/'fiber-output.txt').open() as stream:
        for index,(n,kind,cap,parent) in enumerate(cs):
            words=list(map(int,stream.readline().split()));assert words and words[0]==len(words)-1
            reference_words,box=reference(parent,kind,cap)
            assert reference_words==words[1:],(n,kind,cap,parent)
            t=totals.setdefault(n,dict(fibers=0,empty=0,box=0,children=0))
            t['fibers']+=1;t['empty']+=not reference_words;t['box']+=box;t['children']+=len(reference_words)
            if (index+1)%16==0:print('fiber',index+1,'of',len(cs),flush=True)
        assert not stream.read().strip()
    result=dict(budgets=budgets,stages=totals,all_complete_sets_equal=True,seconds=time.monotonic()-started)
    (W/'fiber-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
    return result
