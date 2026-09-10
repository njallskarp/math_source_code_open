"""Equivalences of the necessary compressed system, not all full mixed pairs."""
from functools import lru_cache


@lru_cache(None)
def p_canonical(p):
    n=len(p)
    return min(tuple(sign*p[(h*j+b)%n] for j in range(n))
               for h in (1,-1) for sign in (1,-1) for b in range(n))


@lru_cache(None)
def b_canonical(r,s):
    n=len(r)
    return min((tuple(sign*r[(h*j+b)%n] for j in range(n)),
                tuple(s[(h*j+b)%n] for j in range(n)))
               for h in (1,-1) for sign in (1,-1) for b in range(0,n,2))


def canonical(q):
    n=len(q[0]);out=[]
    for h in range(1,n,2):
        p,r,s=(tuple(row[h*j%n] for j in range(n)) for row in q)
        a=p_canonical(p);b,c=b_canonical(r,s);out.append((a,b,c))
    return min(out)
