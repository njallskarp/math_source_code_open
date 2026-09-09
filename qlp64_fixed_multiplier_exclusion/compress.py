"""Complete integer compression cover for fixed multipliers 31 and 63 at N=64.

No full-length existence decision is made here. See README.md for the coverage
proof and lift64.cpp for the final exact Gray compatibility check.
"""
import argparse
from functools import lru_cache
import hashlib
from itertools import product
import json
from pathlib import Path

N = 64


def canonical(q):
    """Sign/permutation quotient of the THREE zero-sum rows only."""
    return tuple(sorted(min(r, tuple(-v for v in r)) for r in q[:3])) + (q[3],)


def unit_canonical(q):
    d = len(q[0])
    return min(canonical(tuple(tuple(r[u*j % d] for j in range(d)) for r in q))
               for u in range(1, d, 2))


@lru_cache(None)
def paf(r):
    d = len(r)
    return tuple(sum(r[j]*r[(j+k) % d] for j in range(d))
                 for k in range(d//2+1))


def target(d):
    return (N+1-N//d,) + (-N//d,)*(d//2)


def root_rows(s):
    """All eligible length-four rows; no spectral filter is needed."""
    bound = N//8
    out = []
    for a, b, c in product(range(-bound, bound+1), repeat=3):
        r = (a, b, c, b)
        if (sum(r) == s and (a-bound-s) % 2 == 0
                and (c-bound) % 2 == 0 and paf(r)[0] <= target(4)[0]):
            out.append(r)
    return tuple(out)


@lru_cache(None)
def lifts(parent, s):
    """ALL symmetric half-compressed children with the stated endpoint parity."""
    d = len(parent)
    bound = N//(4*d)
    mid = parent[d//2]
    if mid % 2 or abs(mid//2) > bound or (mid//2-bound) % 2:
        return ()
    out = []
    for free in product(range(-bound, bound+1), repeat=d//2):
        if (free[0]-bound-s) % 2:
            continue
        r = [0]*(2*d)
        r[0], r[d] = free[0], parent[0]-free[0]
        r[d//2] = r[3*d//2] = mid//2
        for j in range(1, d//2):
            r[j] = r[2*d-j] = free[j]
            r[d-j] = r[d+j] = parent[j]-free[j]
        if max(map(abs, r)) > bound or (r[d]-bound) % 2:
            continue
        r = tuple(r)
        assert sum(r) == s
        assert all(r[j] == r[-j % (2*d)] for j in range(2*d))
        assert tuple(r[j]+r[j+d] for j in range(d)) == parent
        if sum(v*v for v in r) <= target(2*d)[0]:
            out.append(r)
    return tuple(out)


def match(rows, wanted):
    """Exact equality of full integer keys; preserve EVERY matching row tuple."""
    if any(not r for r in rows):
        return
    inds = sorted(range(4), key=lambda i: len(rows[i]))
    groups = [(inds[0], inds[3]), (inds[1], inds[2])]
    groups.sort(key=lambda ij: len(rows[ij[0]])*len(rows[ij[1]]))
    (i, j), (k, ell) = groups
    table = {}
    for x, y in product(rows[i], rows[j]):
        key = tuple(a+b for a, b in zip(paf(x), paf(y)))
        table.setdefault(key, []).append((x, y))
    for x, y in product(rows[k], rows[ell]):
        key = tuple(t-a-b for t, a, b in zip(wanted, paf(x), paf(y)))
        for z, w in table.get(key, ()):
            q = [None]*4
            q[i], q[j], q[k], q[ell] = z, w, x, y
            yield tuple(q)


def extend(parents, reduce=True):
    out = set() if reduce else []
    for q in parents:
        rows = [lifts(r, s) for r, s in zip(q, (0, 0, 0, 1))]
        for child in match(rows, target(2*len(q[0]))):
            if reduce:
                out.add(canonical(child))
            else:
                out.append(child)
    return sorted(out)


def digest(qs):
    data = (json.dumps(qs, separators=(',', ':'))+'\n').encode()
    return hashlib.sha256(data).hexdigest()


def build(output):
    zero, special = root_rows(0), root_rows(1)
    raw = list(match((zero, zero, zero, special), target(4)))
    qs = sorted({canonical(q) for q in raw})
    print(json.dumps({'root_rows': [len(zero), len(special)],
                      'labelled_roots': len(raw)}), flush=True)
    for d in (4, 8, 16, 32):
        if d > 4:
            qs = extend(qs)
        print(json.dumps({'length': d, 'canonical_quadruples': len(qs),
                          'sha256': digest(qs)}), flush=True)
    qs = sorted({unit_canonical(q) for q in qs})
    data = str(len(qs))+'\n'+'\n'.join(
        ' '.join(str(v) for r in q for v in r) for q in qs)+'\n'
    output.write_text(data)
    print(json.dumps({'unit_representatives': len(qs),
                      'input_sha256': hashlib.sha256(data.encode()).hexdigest()}),
          flush=True)


def reduction_audit():
    """Compare exact entries, not just counts, with unreduced enumerations."""
    zero, special = root_rows(0), root_rows(1)
    raw = list(match((zero, zero, zero, special), target(4)))
    reduced = sorted({canonical(q) for q in raw})
    for d in (8, 16):
        raw = extend(raw, reduce=False)
        reduced = extend(reduced)
        assert sorted({canonical(q) for q in raw}) == reduced
        print(json.dumps({'audit_length': d, 'labelled': len(raw),
                          'canonical': len(reduced), 'entrywise_equal': True}),
              flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--audit-reduction', action='store_true')
    args = parser.parse_args()
    if args.audit_reduction:
        reduction_audit()
    elif args.output:
        build(args.output)
    else:
        parser.error('supply --output PATH or --audit-reduction')
