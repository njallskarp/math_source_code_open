"""Complete alternate final matcher; direct Gaussian checks on all real matches."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import time
from audit_fibers import cases,caps32

W=Path(__file__).resolve().parent


def decode(code,n):
    b=32//n;base=2*b+1;row=[]
    for _ in range(n):row.append(code%base-b);code//=base
    assert not code
    return tuple(reversed(row))


@lru_cache(None)
def all_paf(row):
    n=len(row)
    return tuple(sum(x*row[(j+k)%n] for j,x in enumerate(row)) for k in range(n))


def gaussian_check(p,r,s):
    # The original compressed A is 2p; original B has coordinates s+r,s-r.
    real=[a+b for a,b in zip(s,r)];imag=[a-b for a,b in zip(s,r)]
    n=len(p)
    for k in range(n):
        a=4*all_paf(p)[k]+sum(real[j]*real[(j+k)%n]+imag[j]*imag[(j+k)%n] for j in range(n))
        b=sum(imag[j]*real[(j+k)%n]-real[j]*imag[(j+k)%n] for j in range(n))
        assert a==(126 if k==0 else -4)
        if b:return k,b
    return None


def main():
    verified=json.loads((W/'fiber-audit.json').read_text());assert verified['all_complete_sets_equal']
    cs,_=cases();fibers={}
    with (W/'fiber-output.txt').open() as stream:
        for n,k,cap,p in cs:
            codes=list(map(int,stream.readline().split()));assert codes[0]==len(codes)-1
            if n==32:fibers[(k,cap,p)]=tuple(decode(w,n) for w in codes[1:])
        assert not stream.read().strip()
    real_matches=[];failures={};survivors=[];pairs=stored=0;t=time.monotonic()
    parents=json.loads((W/'quotient16.json').read_text())
    for q in parents:
        caps=caps32(q)
        if caps is None:continue
        ps,rs,ss=(fibers[(min(k,1),cap,tuple(r))] for k,(r,cap) in enumerate(zip(q,caps)))
        rsmall=len(rs)<=len(ss);small,large=(rs,ss) if rsmall else (ss,rs)
        table={}
        for row in large:table.setdefault(all_paf(row)[:17],[]).append(row)
        stored+=len(large)
        sc=[all_paf(row) for row in small]
        for p in ps:
            target=tuple((63 if k==0 else -2)-2*c for k,c in enumerate(all_paf(p)[:17]))
            for j,row in enumerate(small):
                pairs+=1;key=tuple(a-b for a,b in zip(target,sc[j]))
                for other in table.get(key,()):
                    r,s=(row,other) if rsmall else (other,row)
                    triple=(p,r,s);real_matches.append(triple)
                    fail=gaussian_check(p,r,s)
                    if fail is None:survivors.append(triple)
                    else:failures[str(fail[0])]=failures.get(str(fail[0]),0)+1
    assert len(real_matches)==len(set(real_matches))
    data=json.dumps(sorted(real_matches),separators=(',',':'))+'\n'
    (W/'real-matches32.json').write_text(data)
    result=dict(parents=len(parents),pair_operations=pairs,stored_rows=stored,
                real_matches=len(real_matches),real_match_sha256=hashlib.sha256(data.encode()).hexdigest(),
                rejected_by_first_imaginary_lag=failures,survivors=len(survivors),seconds=time.monotonic()-t)
    assert not survivors
    (W/'replay32.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
    return result
