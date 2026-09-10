"""Necessary proper-compression rows for the residual mixed multiplier 33."""
from functools import lru_cache
from itertools import product


@lru_cache(None)
def paf(p):
    n=len(p)
    return tuple(sum(p[j]*p[(j+k)%n] for j in range(n)) for k in range(n//2+1))


def amicable(r,s):
    n=len(r)
    return all(sum(r[j]*s[(j+k)%n]-s[j]*r[(j+k)%n] for j in range(n))==0
               for k in range(1,n//2))


def rows(n,s,parity):
    b=32//n;cap=(65-64//n)//(2 if parity is None else 1)
    out=[]
    for first in product(*[range(-b,b+1,2) if parity is not None and j%2 else range(-b,b+1) for j in range(n-1)]):
        last=s-sum(first)
        if abs(last)>b or parity is not None and (last-b)%2:continue
        row=first+(last,)
        if sum(v*v for v in row)<=cap:out.append(row)
    return out


def match(ps,rs,ss,n):
    wanted=(65-64//n,)+(-64//n,)*(n//2)
    table={}
    for p in ps:
        key=tuple(a-2*b for a,b in zip(wanted,paf(p)))
        table.setdefault(key,[]).append(p)
    out=[]
    for r,s in product(rs,ss):
        key=tuple(a+b for a,b in zip(paf(r),paf(s)))
        if key not in table or not amicable(r,s):continue
        out.extend((p,r,s) for p in table[key])
    return sorted(out)


@lru_cache(None)
def lifts(parent,kind):
    d=len(parent);n=2*d;b=32//n
    cap=(65-64//n)//(2 if kind==0 else 1)
    choices=[]
    for j,v in enumerate(parent):
        choices.append(tuple(a for a in range(-b,b+1)
                             if -b<=v-a<=b and
                             (kind==0 or j%2==0 or (a-b)%2==0 and (v-a-b)%2==0)))
    out=[]
    for first in product(*choices):
        row=first+tuple(v-a for v,a in zip(parent,first))
        if sum(v*v for v in row)<=cap:out.append(row)
    return tuple(out)
