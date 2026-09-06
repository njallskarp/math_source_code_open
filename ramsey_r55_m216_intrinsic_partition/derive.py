"""Complete necessary exceptional-core census and canonical marked partition."""
from itertools import combinations, permutations
from pathlib import Path
import json

PAIRS = tuple(combinations(range(7), 2))
INDEX = {uv: i for i, uv in enumerate(PAIRS)}
GROUP = tuple(z+e for z in permutations(range(2)) for e in permutations(range(2, 7)))

def decode(mask):
    if type(mask) is not int or not 0 <= mask < 1 << 21:
        raise ValueError('seven-vertex mask')
    a = [set() for _ in range(7)]
    for bit, (u, v) in enumerate(PAIRS):
        if mask >> bit & 1:
            a[u].add(v); a[v].add(u)
    return a

def transport(mask, p):
    return sum(1 << INDEX[tuple(sorted((p[u], p[v])))]
               for bit, (u, v) in enumerate(PAIRS) if mask >> bit & 1)

def deficits(mask):
    a = decode(mask)
    return [2*len(a[v] & {0, 1}) + len(a[v] & set(range(2, 7)))
            - (5 if v < 2 else 4) for v in range(7)]

def structured_census():
    found = set()
    epairs = tuple(combinations(range(2, 7), 2))
    # The four numerical possibilities follow from the proof, before
    # the impossible b=8,e=2 case is removed by individual inequalities.
    buckets = {(0, 10, 0), (0, 10, 1), (1, 6, 4), (1, 6, 5),
               (1, 7, 3), (1, 8, 2)}
    for eta in (0, 1):
        for ma in range(32):
            for mb in range(32):
                az, bz = ma.bit_count(), mb.bit_count()
                if min(az, bz) < 5-2*eta:
                    continue
                star = eta
                for i in range(5):
                    if ma >> i & 1:
                        star |= 1 << INDEX[(0, i+2)]
                    if mb >> i & 1:
                        star |= 1 << INDEX[(1, i+2)]
                for em in range(1024):
                    if (eta, az+bz, em.bit_count()) not in buckets:
                        continue
                    mask = star | sum(1 << INDEX[uv] for bit, uv in enumerate(epairs) if em >> bit & 1)
                    s = deficits(mask)
                    if min(s) < 0 or sum(s) > 2:
                        continue
                    a = decode(mask)
                    if any(len({v in a[u] for u, v in combinations(vs, 2)}) == 1
                           for vs in combinations(range(7), 5)):
                        continue
                    found.add(mask)
    return found

def produce():
    found = structured_census()
    remaining = found.copy()
    cores = []
    while remaining:
        representative = min(remaining)
        orbit = {transport(representative, p) for p in GROUP}
        if not orbit <= remaining:
            raise ValueError('orbit overlap or incomplete census')
        remaining -= orbit
        s = deficits(representative)
        cores.append({'mask': representative, 'orbit_size': len(orbit),
                      'exceptional_red_excess': s, 'central_red_excess': 2-sum(s),
                      'closed_blue_degree19_pair': not bool(representative & 1)})
    roots = []
    for core in cores:
        if core['closed_blue_degree19_pair']:
            continue
        excess = core['central_red_excess']
        partitions = [[]] if excess == 0 else [[[7, 1]]] if excess == 1 else [[[7, 2]], [[7, 1], [8, 1]]]
        for defect in partitions:
            roots.append({'index': len(roots), 'core_mask': core['mask'],
                          'central_red_excess': defect})
    return {'format': 'r55-m216-intrinsic-partition-v1',
            'degree_profile': [19, 19]+[20]*5+[21]*36,
            'labeled_necessary_cores': len(found), 'cores': cores, 'roots': roots}

if __name__ == '__main__':
    print(json.dumps(produce(), sort_keys=True, indent=2))
