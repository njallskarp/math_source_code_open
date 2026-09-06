"""Exact family reduction and orbit check. CPython 3.12, standard library."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
SQUARES = {x*x % 17 for x in range(1, 17)}
P = {e for e in combinations(range(17), 2) if (e[1]-e[0]) % 17 in SQUARES}
SOURCES = {
    15: ('53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1', 640, 55),
    16: ('b9a7c89cf999d64c976c877891d06f828ce2e846f5ddfa72bb402f2ddd57b927', 2, 60),
    17: ('23f8802eed6281e1b40c7ec157f687d67624c6a327a513b003bce93e33e9214c', 1, 68),
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return sha256((json.dumps(value, separators=(',', ':'))+'\n').encode()).hexdigest()


def decode(line):
    need(bool(line) and all(63 <= x <= 126 for x in line), 'graph6 alphabet')
    n = line[0]-63
    need(n < 63, 'short graph6 only')
    bits = [int(b) for x in line[1:] for b in f'{x-63:06b}']
    size = n*(n-1)//2
    need(len(bits) == 6*((size+5)//6) and not any(bits[size:]), 'graph6 size/padding')
    order = [(i, j) for j in range(1, n) for i in range(j)]
    return n, {e for e, b in zip(order, bits) if b}


def cliques(vertices, edges, k, red=True):
    return [c for c in combinations(vertices, k)
            if all((e in edges) == red for e in combinations(c, 2))]


def isomorphism(n, source, target):
    """Return a checked source-to-target permutation, not a canonization claim."""
    mapping = []
    used = set()
    def visit():
        i = len(mapping)
        if i == n:
            return tuple(mapping)
        for v in range(n):
            if v not in used and all(((j, i) in source) ==
                    (tuple(sorted((mapping[j], v))) in target) for j in range(i)):
                mapping.append(v)
                used.add(v)
                answer = visit()
                if answer is not None:
                    return answer
                used.remove(v)
                mapping.pop()
        return None
    return visit()


def catalogues(directory=None):
    result = {}
    for n, (identity, count, maximum) in SOURCES.items():
        name = f'r44_{n}.g6'
        if directory is None:
            with urlopen('https://users.cecs.anu.edu.au/~bdm/data/'+name, timeout=30) as stream:
                raw = stream.read()
        else:
            raw = (Path(directory)/name).read_bytes()
        need(sha256(raw).hexdigest() == identity, 'catalogue identity '+name)
        records = [decode(line) for line in raw.splitlines()]
        need(len(records) == count, 'catalogue count')
        for order, edges in records:
            need(order == n, 'catalogue order')
            need(not cliques(range(n), edges, 4) and
                 not cliques(range(n), edges, 4, False), 'catalogue Ramsey property')
        histogram = Counter(len(edges) for _, edges in records)
        need(max(histogram) == maximum, 'catalogue maximum')
        result[str(n)] = {'count': count, 'edge_histogram': dict(sorted(histogram.items())),
                          'sha256': identity}
        if n == 17:
            permutation = isomorphism(17, records[0][1], P)
            need(permutation is not None, 'Paley identification')
            result[str(n)]['catalogue_to_paley'] = permutation
    return result


def validate_seed(data):
    need(set(data) == {'signatures', 'edge_sha256'}, 'certificate fields')
    signatures = data['signatures']
    need(type(signatures) is list and len(signatures) == 4, 'four signatures')
    for s in signatures:
        need(type(s) is list and len(s) == 8 and all(type(x) is int and 0 <= x < 17 for x in s)
             and s == sorted(set(s)), 'signature schema')
    edges = P | {(a, i+17) for i, s in enumerate(signatures) for a in s}
    edges |= {(17, 18), (18, 19), (19, 20), (17, 20)} | {(i, 21) for i in range(17, 21)}
    need(len(edges) == 108, 'seed density')
    need(not cliques(range(22), edges, 4), 'seed red K4')
    need(not cliques(range(22), edges, 5, False), 'seed blue K5')
    need(digest(sorted(edges)) == data['edge_sha256'], 'seed identity')
    return tuple(tuple(s) for s in signatures), edges


def signature_classification(seed):
    triangles = [set(t) for t in cliques(range(17), P, 3)]
    independent = [set(t) for t in cliques(range(17), P, 3, False)]
    signatures = [tuple(s) for s in combinations(range(17), 8)
                  if not any(t <= set(s) for t in triangles)]
    sets = list(map(set, signatures))
    red = [[not any(set(e) <= x & y for e in P) for y in sets] for x in sets]
    blue = [[not any(t.isdisjoint(x | y) for t in independent) for y in sets] for x in sets]
    tuples = set()
    for i, x in enumerate(signatures):
        for k, z in enumerate(signatures):
            if not blue[i][k]:
                continue
            middle = [j for j in range(len(signatures)) if red[i][j] and red[k][j]]
            for j in middle:
                for ell in middle:
                    if blue[j][ell]:
                        tuples.add((x, signatures[j], z, signatures[ell]))
    orbit = set()
    for a in sorted(SQUARES):
        for b in range(17):
            permutation = [(a*x+b) % 17 for x in range(17)]
            need({tuple(sorted((permutation[x], permutation[y]))) for x, y in P} == P,
                 'affine action preserves Paley graph')
            for shift in range(4):
                for direction in (-1, 1):
                    orbit.add(tuple(tuple(sorted(permutation[x] for x in seed[(shift+direction*i) % 4]))
                                    for i in range(4)))
    need(tuples == orbit, 'exact orbit exhaustion, not just count agreement')
    need(len(signatures) == 51 and len(tuples) == 1088, 'classification counts')
    return {'signatures': len(signatures), 'compatible_ordered_tuples': len(tuples),
            'affine_dihedral_orbit_size': len(orbit), 'exact_set_equality': True,
            'tuple_sha256': digest(sorted(tuples)),
            'red_relation_degree_histogram': dict(sorted(Counter(map(sum, red)).items())),
            'blue_relation_degree_histogram': dict(sorted(Counter(map(sum, blue)).items()))}


def separator_rows():
    def partitions(n, lower=1):
        if n == 0:
            yield ()
        for first in range(lower, n+1):
            for rest in partitions(n-first, first):
                yield (first,)+rest
    capacities = {1: 3, 2: 8, 3: 17}
    profiles = [p for total in range(2, 5) for p in partitions(total)
                if len(p) >= 2 and sum(capacities[a] for a in p) >= 18]
    need(profiles == [(1, 3)], 'component independence budgets')
    rows = [[b, 18-b, SOURCES[18-b][2]+32+((b+4)**2//3)] for b in range(1, 4)]
    need(rows == [[1, 17, 108], [2, 16, 104], [3, 15, 103]], 'density rows')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog-dir', type=Path, help='optional directory of original primary .g6 files')
    args = parser.parse_args()
    data = json.loads((ROOT/'certificate.json').read_text())
    seed, edges = validate_seed(data)
    result = {'catalogues': catalogues(args.catalog_dir), 'classification': signature_classification(seed),
              'component_rows_b_a_edge_bound': separator_rows(),
              'seed': {'order': 22, 'edges': len(edges), 'edge_sha256': digest(sorted(edges)),
                       'degree_histogram': dict(sorted(Counter(sum(v in e for e in edges)
                                                       for v in range(22)).items()))}}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
