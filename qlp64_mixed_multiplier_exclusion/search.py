"""Exact complete proper-compression cover for the mixed 31/63 QLP(64) family.

The default run retains all states: no sign, permutation, or unit quotient.
All inputs are generated from the equations in PROOF.md.
"""
from functools import lru_cache
import hashlib
from itertools import product
import json

N = 64


def reverse(p):
    return (p[0],) + p[:0:-1]



@lru_cache(None)
def paf(p):
    d = len(p)
    return tuple(sum(p[j]*p[(j+k) % d] for j in range(d))
                 for k in range(d//2+1))


def axes(p):
    """P(x)^2 = P(x^-1)^2 in Q[x]/(x^d-1), using integer convolution."""
    d = len(p)
    return all(sum(p[j]*p[(k-j) % d] for j in range(d))
               == sum(p[j]*p[(-k-j) % d] for j in range(d))
               for k in range(1, d//2))


def target(d):
    return (N+1-N//d,) + (-N//d,)*(d//2)


@lru_cache(None)
def mixed_lifts(parent, bound, norm_cap):
    """Every child with the axes property above an axes-property parent.

At a primitive root of order 2d the new component is either real or imaginary.
See the two-branch lifting lemma in PROOF.md.
    """
    d = len(parent)
    out = set()
    for real in (True, False):
        free_endpoint = 0 if real else d//2
        fixed_endpoint = d//2 if real else 0
        if parent[fixed_endpoint] % 2:
            continue
        if abs(parent[fixed_endpoint]//2) > bound:
            continue
        for free in product(range(-bound, bound+1), repeat=d//2):
            first = [0]*d
            first[fixed_endpoint] = parent[fixed_endpoint]//2
            first[free_endpoint] = free[0]
            for j in range(1, d//2):
                first[j] = free[j]
                difference = 2*first[j]-parent[j]
                twice = parent[d-j] + (-difference if real else difference)
                if twice % 2:
                    break
                first[d-j] = twice//2
            else:
                row = tuple(first+[parent[j]-first[j] for j in range(d)])
                if max(map(abs, row)) <= bound and sum(v*v for v in row) <= norm_cap:
                    assert sum(row) == sum(parent)
                    assert axes(row)
                    out.add(row)
    return tuple(sorted(out))


@lru_cache(None)
def symmetric_lifts(parent, s, bound, norm_cap):
    """Every symmetric child with the two required endpoint parities."""
    d = len(parent)
    mid = parent[d//2]
    if mid % 2 or abs(mid//2) > bound:
        return ()
    out = []
    for free in product(range(-bound, bound+1), repeat=d//2):
        if (free[0]-bound-s) % 2:
            continue
        row = [0]*(2*d)
        row[0], row[d] = free[0], parent[0]-free[0]
        row[d//2] = row[3*d//2] = mid//2
        for j in range(1, d//2):
            row[j] = row[2*d-j] = free[j]
            row[d-j] = row[d+j] = parent[j]-free[j]
        row = tuple(row)
        if (max(map(abs, row)) <= bound and (row[d]-bound) % 2 == 0
                and paf(row)[0] <= norm_cap):
            assert sum(row) == s
            out.append(row)
    return tuple(out)


def match(ps, rs, ss, wanted):
    table = {}
    for p in ps:
        key = tuple(t-2*c for t, c in zip(wanted, paf(p)))
        table.setdefault(key, []).append(p)
    for r, s in product(rs, ss):
        key = tuple(a+b for a, b in zip(paf(r), paf(s)))
        for p in table.get(key, ()):
            yield p, r, s


def root_rows():
    bound = N//8
    wanted = target(4)
    ps, rs, ss = [], [], []
    for a, b, c in product(range(-bound, bound+1), repeat=3):
        p = (a, b, c, -a-b-c)
        if max(map(abs, p)) <= bound and 2*paf(p)[0] <= wanted[0] and axes(p):
            ps.append(p)
        row = (a, b, c, b)
        for s, out in ((0, rs), (1, ss)):
            if (sum(row) == s and (a-bound-s) % 2 == 0
                    and (c-bound) % 2 == 0 and paf(row)[0] <= wanted[0]):
                out.append(row)
    return tuple(ps), tuple(rs), tuple(ss)


def extend(parents):
    d = 2*len(parents[0][0])
    bound = N//(2*d)
    wanted = target(d)
    out = set()
    viable = cost = 0
    for p, r, s in parents:
        ps = mixed_lifts(p, bound, wanted[0]//2)
        rs = symmetric_lifts(r, 0, bound, wanted[0])
        ss = symmetric_lifts(s, 1, bound, wanted[0])
        if not ps or not rs or not ss:
            continue
        viable += 1
        cost += len(ps)+len(rs)*len(ss)
        for q in match(ps, rs, ss, wanted):
            out.add(q)
    return sorted(out), {'viable_parents': viable,
                         'row_keys_plus_binary_pairs': cost}


def digest(qs):
    return hashlib.sha256((json.dumps(qs, separators=(',', ':'))+'\n').encode()).hexdigest()
