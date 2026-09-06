#!/usr/bin/env python3
"""Complete degree-five classification by exact column-domain propagation."""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
from urllib.request import urlopen

BASE = Path(__file__).resolve().parent
FULL = (1 << 16) - 1
PAIRS = list(combinations(range(5), 2))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(obj):
    return sha256((json.dumps(obj, separators=(',', ':')) + '\n').encode()).hexdigest()

def decode(record):
    require(isinstance(record, str) and bool(record), 'empty graph6')
    require(all(63 <= ord(c) <= 126 for c in record), 'graph6 character')
    n = ord(record[0]) - 63
    require(n < 63, 'only short graph6 is supported')
    length = n * (n - 1) // 2
    require(len(record) == 1 + (length + 5) // 6, 'graph6 length')
    bits = ''.join(f'{ord(c)-63:06b}' for c in record[1:])
    require('1' not in bits[length:], 'nonzero graph6 padding')
    adj = [0] * n
    k = 0
    for j in range(n):
        for i in range(j):
            if bits[k] == '1':
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            k += 1
    return adj

def clique(adj, vertices, size):
    if size == 0:
        return True
    while vertices:
        if vertices.bit_count() < size:
            return False
        bit = vertices & -vertices
        vertices -= bit
        i = bit.bit_length() - 1
        if clique(adj, vertices & adj[i], size - 1):
            return True
    return False

def complement(adj):
    full = (1 << len(adj)) - 1
    return [full ^ row ^ (1 << i) for i, row in enumerate(adj)]

def mask(vertices):
    return sum(1 << v for v in vertices)

def automorphisms(adj):
    """All adjacency-preserving bijections, with degree filtering only."""
    n = len(adj)
    domains = [[j for j in range(n) if adj[j].bit_count() == adj[i].bit_count()]
               for i in range(n)]
    result = []
    def walk(p, used):
        i = len(p)
        if i == n:
            result.append(tuple(p))
            return
        for j in domains[i]:
            if used >> j & 1:
                continue
            if all(((adj[i] >> k) & 1) == ((adj[j] >> p[k]) & 1)
                   for k in range(i)):
                walk(p + [j], used | (1 << j))
    walk([], 0)
    return result

def small_cases():
    """Generate every triangle-free five-vertex graph with >=4 edges."""
    result = {}
    for code in range(1 << 10):
        edges = [e for bit, e in enumerate(PAIRS) if code >> bit & 1]
        if len(edges) < 4:
            continue
        adj = [0] * 5
        for i, j in edges:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
        if clique(adj, 31, 3):
            continue
        canonical = min(sum(1 << PAIRS.index(tuple(sorted((p[i], p[j]))))
                            for i, j in edges) for p in permutations(range(5)))
        if canonical not in result:
            order = sorted(range(5), key=lambda i: -adj[i].bit_count())
            result[canonical] = [sum(1 << j for j in range(5)
                                     if adj[order[i]] >> order[j] & 1)
                                 for i in range(5)]
    return result

def load_certificate(path, fetch=False):
    data = json.loads(Path(path).read_text())
    raw = ('\n'.join(data['catalogue_records']) + '\n').encode()
    require(sha256(raw).hexdigest() == data['catalogue_sha256'], 'catalogue hash')
    require(data['catalogue_sha256'] ==
            'b9a7c89cf999d64c976c877891d06f828ce2e846f5ddfa72bb402f2ddd57b927',
            'unpinned catalogue')
    if fetch:
        with urlopen(data['catalogue_url'], timeout=30) as response:
            require(response.read() == raw, 'primary catalogue differs')
    require(len(data['catalogue_records']) == 2, 'catalogue record count')
    for text in data['catalogue_records']:
        a = decode(text)
        require(len(a) == 16 and sum(map(int.bit_count, a)) == 120, 'core order/edges')
        require(not clique(a, FULL, 4) and not clique(complement(a), FULL, 4),
                'core Ramsey property')
    low_triangles = []
    for record in data['catalogue_records']:
        a = decode(record)
        low = [i for i, row in enumerate(a) if row.bit_count() == 7]
        low_triangles.append(sum(clique(a, mask(t), 3) for t in combinations(low, 3)))
    require(low_triangles == [0, 4], 'nonisomorphic cores')
    return data

def census(adj, small):
    blue = complement(adj)
    independent = bytearray(not clique(adj, m, 2) for m in range(1 << 16))
    no_blue3 = bytearray(not clique(blue, m, 3) for m in range(1 << 16))
    no_blue2 = bytearray(not clique(blue, m, 2) for m in range(1 << 16))
    columns = [mask(c) for k in (8, 7, 6) for c in combinations(range(16), k)
               if not clique(adj, mask(c), 3)]
    deficit = [8 - x.bit_count() for x in columns]
    size_domains = [sum(1 << j for j, d in enumerate(deficit) if d <= k)
                    for k in range(3)]
    @lru_cache(None)
    def compatible(j, red):
        x = columns[j]
        return sum(1 << i for i, y in enumerate(columns)
                   if (independent[x & y] if red else no_blue3[FULL ^ (x | y)]))
    results = {}
    for code, s in sorted(small.items()):
        slack = sum(map(int.bit_count, s)) // 2 - 4
        triple_tests = [[js for js in combinations(range(i), 2)
                         if all(not (s[u] >> v & 1)
                                for u, v in combinations((*js, i), 2))]
                        for i in range(5)]
        quad_tests = [[js for js in combinations(range(i), 3)
                       if all(not (s[u] >> v & 1)
                              for u, v in combinations((*js, i), 2))]
                      for i in range(5)]
        solutions = set()
        def visit(chosen, domains, used):
            i = len(chosen)
            if i == 5:
                solutions.add(tuple(columns[j] for j in chosen))
                return
            candidates = domains[0] & size_domains[slack - used]
            while candidates:
                bit = candidates & -candidates
                candidates -= bit
                j = bit.bit_length() - 1
                x = columns[j]
                if any(not no_blue2[FULL ^ (x | columns[chosen[u]] | columns[chosen[v]])]
                       for u, v in triple_tests[i]):
                    continue
                if any((x | columns[chosen[u]] | columns[chosen[v]] | columns[chosen[w]]) != FULL
                       for u, v, w in quad_tests[i]):
                    continue
                future = [d & compatible(j, bool(s[i] >> k & 1))
                          for k, d in enumerate(domains[1:], i + 1)]
                if all(future):
                    visit(chosen + [j], future, used + deficit[j])
        visit([], [size_domains[slack]] * 5, 0)
        results[code] = solutions
    return results, dict(sorted(Counter(map(int.bit_count, columns)).items()))

def assemble(adj, s, columns):
    graph = adj + [0] * 6
    for i in range(5):
        for j in range(5):
            if s[i] >> j & 1:
                graph[16+i] |= 1 << (16+j)
        graph[16+i] |= columns[i] | (1 << 21)
        graph[21] |= 1 << (16+i)
        for j in range(16):
            if columns[i] >> j & 1:
                graph[j] |= 1 << (16+i)
    return graph

def transform(xs, p, q):
    out = [0] * 5
    for i, x in enumerate(xs):
        out[q[i]] = sum(1 << p[j] for j in range(16) if x >> j & 1)
    return tuple(out)

def check_certificate(data, all_solutions, small):
    expected_cases = {(c['core'], c['type']): c for c in data['cases']}
    require(len(expected_cases) == len(data['cases']) == 14, 'case inventory')
    representatives = data['representatives']
    require(len(representatives) == 13, 'representative inventory')
    report = []
    for core in range(2):
        adj = decode(data['catalogue_records'][core])
        perms = automorphisms(adj)
        require(len(perms) == 8, 'core automorphism count')
        for code, s in sorted(small.items()):
            case = expected_cases[(core, code)]
            edges = [[i, j] for i, j in PAIRS if s[i] >> j & 1]
            require(case['s_edges'] == edges, 'neighbor graph mismatch')
            solutions = all_solutions[core][code]
            require(len(solutions) == case['solutions'], 'solution count')
            orbit_union = set()
            orbit_sizes = []
            for entry in representatives:
                if (entry['core'], entry['type']) != (core, code):
                    continue
                xs = entry['columns']
                require(len(xs) == 5 and all(type(x) is int and 0 <= x <= FULL for x in xs),
                        'column syntax')
                graph = assemble(adj, s, xs)
                require(graph == decode(entry['graph6']), 'independent graph serialization')
                require(sum(map(int.bit_count, graph)) == 218, 'representative density')
                degrees = list(map(int.bit_count, graph))
                require(degrees.count(5) == 1 and min(degrees) == 5, 'unique degree-five root')
                require(not clique(graph, (1 << 22)-1, 4) and
                        not clique(complement(graph), (1 << 22)-1, 5), 'representative Ramsey')
                orbit = {transform(xs, p, q) for p in perms for q in automorphisms(s)}
                require(len(orbit) == entry['orbit'], 'orbit size')
                require(tuple(xs) == min(orbit), 'representative canonicality')
                require(not orbit_union.intersection(orbit), 'duplicate isomorphism class')
                orbit_union.update(orbit)
                orbit_sizes.append(len(orbit))
            require(orbit_union == solutions, 'orbit coverage set equality')
            report.append({'core': core, 'type': code, 'count': len(solutions),
                           'tuple_sha256': digest(sorted(solutions)), 'orbits': sorted(orbit_sizes)})
    require(all((r['core'], r['type']) in expected_cases for r in representatives),
            'unrecognized representative')
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=BASE/'certificate.json')
    parser.add_argument('--fetch-catalogue', action='store_true')
    args = parser.parse_args()
    data = load_certificate(args.certificate, args.fetch_catalogue)
    small = small_cases()
    require(sorted(small) == [15, 29, 54, 58, 62, 126, 220], 'five-vertex classification')
    solutions = []
    column_counts = []
    for record in data['catalogue_records']:
        result, counts = census(decode(record), small)
        solutions.append(result)
        column_counts.append(counts)
    rows = check_certificate(data, solutions, small)
    print(json.dumps({'cases': rows, 'column_counts': column_counts,
                      'graphs': 13, 'labeled_tuples': sum(r['count'] for r in rows),
                      'edge_counts': [109], 'catalogue_sha256': data['catalogue_sha256']},
                     sort_keys=True, separators=(',', ':')))

if __name__ == '__main__':
    main()
