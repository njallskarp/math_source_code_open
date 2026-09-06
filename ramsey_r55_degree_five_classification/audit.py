#!/usr/bin/env python3
"""Independent physical forbidden-set audit with first-column orbit fibers.
No imports from verify.py. The certificate is data, never executable code.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALL = 65535

def check(ok, message):
    if not ok:
        raise ValueError(message)

def hash_rows(rows):
    return sha256((json.dumps(rows, separators=(',', ':'))+'\n').encode()).hexdigest()

def read_graph(record):
    check(type(record) is str and len(record) > 0, 'graph6 text')
    values = [ord(c)-63 for c in record]
    check(all(0 <= x < 64 for x in values) and values[0] < 63, 'graph6 range')
    n = values[0]
    used = n*(n-1)//2
    check(len(values)-1 == (used+5)//6, 'graph6 size')
    packed = 0
    for x in values[1:]:
        packed = packed*64+x
    padding = 6*(len(values)-1)-used
    check(packed % (1 << padding) == 0, 'graph6 padding')
    packed >>= padding
    graph = [[False]*n for _ in range(n)]
    edges = list((i, j) for j in range(n) for i in range(j))
    for i, j in reversed(edges):
        graph[i][j] = graph[j][i] = bool(packed % 2)
        packed //= 2
    return graph

def good(graph, red_size=4, blue_size=5):
    for value, size in ((True, red_size), (False, blue_size)):
        for vertices in combinations(range(len(graph)), size):
            if all(graph[i][j] == value for i, j in combinations(vertices, 2)):
                return False
    return True

def all_maps(graph):
    """All matrix automorphisms, assigning vertices in descending degree order."""
    n = len(graph)
    degree = [sum(row) for row in graph]
    order = sorted(range(n), key=lambda i: (-degree[i], i))
    maps = []
    mapping = {}
    def extend(left):
        if not left:
            maps.append(tuple(mapping[i] for i in range(n)))
            return
        v = order[len(mapping)]
        for w in sorted(left):
            if degree[v] == degree[w] and all(graph[v][u] == graph[w][t]
                                               for u, t in mapping.items()):
                mapping[v] = w
                extend(left-{w})
                del mapping[v]
    extend(set(range(n)))
    return maps

def move(column, permutation):
    return sum(1 << permutation[v] for v in range(16) if column & (1 << v))

def s_inventory():
    """Independent isomorphism grouping of all 1024 literal five-vertex graphs."""
    pairs = list(combinations(range(5), 2))
    representatives = {}
    covered = set()
    for code in range(1024):
        if code in covered or code.bit_count() < 4:
            continue
        edges = [pair for k, pair in enumerate(pairs) if code & (1 << k)]
        if any(all(tuple(sorted(e)) in edges for e in combinations(t, 2))
               for t in combinations(range(5), 3)):
            continue
        orbit = {sum(1 << pairs.index(tuple(sorted((p[i], p[j])))) for i, j in edges)
                 for p in permutations(range(5))}
        representatives[min(orbit)] = orbit
        covered |= orbit
    return representatives

def physical_rules(core, s_edges):
    """Substitute every fixed pair in all physical K4 and independent K5 events."""
    fixed = {}
    for i, j in combinations(range(22), 2):
        if j < 16:
            fixed[i, j] = core[i][j]
        elif j == 21:
            fixed[i, j] = i >= 16
        elif i >= 16:
            fixed[i, j] = [i-16, j-16] in s_edges
    rules = defaultdict(set)
    residuals = []
    for red, size in ((True, 4), (False, 5)):
        for vertices in combinations(range(22), size):
            pairs = list(combinations(vertices, 2))
            if any(edge in fixed and fixed[edge] != red for edge in pairs):
                continue
            free = [edge for edge in pairs if edge not in fixed]
            check(bool(free), 'already forbidden fixed vertex set')
            columns = tuple(sorted({j-16 for i, j in free}))
            support = sum(1 << i for i in sorted({i for i, j in free}))
            # Verify that the residual is precisely the full rectangle.
            rectangle = {(i, 16+j) for i in range(16) if support & (1 << i)
                         for j in columns}
            check(set(free) == rectangle, 'nonrectangular physical residual')
            rules[red, columns].add(support)
            residuals.append([int(red), list(vertices), [list(e) for e in free]])
    return rules, hash_rows(residuals)

@lru_cache(None)
def upwards(supports):
    bad = bytearray(65536)
    for support in supports:
        bad[support] = 1
    for bit in range(16):
        step = 1 << bit
        for start in range(0, 65536, step*2):
            for low in range(step):
                if bad[start+low]:
                    bad[start+low+step] = 1
    return bad

def independent_census(core, s_edges, maps):
    rules, clause_hash = physical_rules(core, s_edges)
    single = [upwards(tuple(sorted(rules[True, (i,)]))) for i in range(5)]
    check(all(x == single[0] for x in single), 'single-column symmetry')
    check(not any((not red and len(cols) == 1) for red, cols in rules),
          'unexpected blue single-column residual')
    buckets = {d: [x for x in range(65536) if x.bit_count() == 8-d and not single[0][x]]
               for d in range(3)}
    ends = [[] for _ in range(5)]
    for (red, cols), supports in rules.items():
        if len(cols) >= 2:
            ends[max(cols)].append((red, cols[:-1], upwards(tuple(sorted(supports)))))
    slack = len(s_edges)-4
    roots = {x for d in range(slack+1) for x in buckets[d]
             if x == min(move(x, p) for p in maps)}
    # A first-column orbit normalization, then literal depth-first fibers.
    # No forward candidate-domain propagation is used.
    fibers = set()
    def fill(xs, remaining):
        i = len(xs)
        if i == 5:
            fibers.add(tuple(xs))
            return
        for d in range(remaining+1):
            for x in buckets[d]:
                if i == 0 and x not in roots:
                    continue
                valid = True
                for red, earlier, bad in ends[i]:
                    common = x if red else ALL ^ x
                    for j in earlier:
                        common &= xs[j] if red else ALL ^ xs[j]
                    if bad[common]:
                        valid = False
                        break
                if valid:
                    fill(xs+[x], remaining-d)
    fill([], slack)
    all_tuples = {tuple(move(x, p) for x in xs) for xs in fibers for p in maps}
    return all_tuples, len(fibers), len(roots), clause_hash

def verify_representatives(data, solutions, cores):
    result = []
    all_cases = {(x['core'], x['type']): x for x in data['cases']}
    for key, tuples in solutions.items():
        c, code = key
        case = all_cases[key]
        core = cores[c]
        a_maps = all_maps(core)
        s = [[False]*5 for _ in range(5)]
        for i, j in case['s_edges']:
            s[i][j] = s[j][i] = True
        s_maps = all_maps(s)
        union = set()
        orbit_sizes = []
        for rep in data['representatives']:
            if (rep['core'], rep['type']) != key:
                continue
            matrix = read_graph(rep['graph6'])
            check(len(matrix) == 22 and good(matrix), 'literal representative Ramsey test')
            check(sum(map(sum, matrix)) == 218, 'representative edge count')
            check([sum(row) for row in matrix].count(5) == 1, 'unique degree-five vertex')
            for i, j in combinations(range(22), 2):
                if j < 16:
                    expected = core[i][j]
                elif j == 21:
                    expected = i >= 16
                elif i >= 16:
                    expected = s[i-16][j-16]
                else:
                    expected = bool(rep['columns'][j-16] & (1 << i))
                check(matrix[i][j] == expected, 'matrix/incidence mismatch')
            orbit = set()
            for p in a_maps:
                for q in s_maps:
                    columns = [0]*5
                    for i in range(5):
                        columns[q[i]] = move(rep['columns'][i], p)
                    orbit.add(tuple(columns))
            check(len(orbit) == rep['orbit'] and not (union & orbit), 'orbit identity')
            check(tuple(rep['columns']) == min(orbit), 'noncanonical representative')
            union |= orbit
            orbit_sizes.append(len(orbit))
        check(union == tuples, 'complete physical census/orbit equality')
        check(len(tuples) == case['solutions'], 'declared census count')
        result.append({'core': c, 'type': code, 'count': len(tuples),
                       'tuple_sha256': hash_rows(sorted(tuples)), 'orbits': sorted(orbit_sizes)})
    return sorted(result, key=lambda r: (r['core'], r['type']))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text())
    raw = ''.join(line+'\n' for line in data['catalogue_records']).encode()
    check(sha256(raw).hexdigest() ==
          'b9a7c89cf999d64c976c877891d06f828ce2e846f5ddfa72bb402f2ddd57b927',
          'primary input identity')
    cores = list(map(read_graph, data['catalogue_records']))
    check(len(cores) == 2 and all(len(g) == 16 and good(g, 4, 4) for g in cores),
          'literal catalogue properties')
    check(all(sum(map(sum, g)) == 120 for g in cores), 'catalogue edge counts')
    low_triangles = [sum(all(g[i][j] for i, j in combinations(t, 2))
                         for t in combinations([v for v, row in enumerate(g)
                                                if sum(row) == 7], 3))
                     for g in cores]
    check(low_triangles == [0, 4], 'nonisomorphic cores: degree-seven triangles')
    inventory = s_inventory()
    keys = [(c['core'], c['type']) for c in data['cases']]
    check(len(keys) == len(set(keys)) == 14 and
          set(keys) == {(i, code) for i in range(2) for code in inventory}, 'case cover')
    solutions = {}
    fibers = []
    maps = [all_maps(core) for core in cores]
    check(list(map(len, maps)) == [8, 8], 'automorphism reconstruction')
    for case in sorted(data['cases'], key=lambda c: (c['core'], c['type'])):
        i, code = case['core'], case['type']
        edges = case['s_edges']
        pairs = list(combinations(range(5), 2))
        check(len(edges) == len({tuple(e) for e in edges}) and
              all(tuple(e) in pairs for e in edges), 'five-vertex edges')
        encoded = sum(1 << pairs.index(tuple(e)) for e in edges)
        check(encoded in inventory[code], 'wrong five-vertex graph class')
        result, nf, nr, residual_hash = independent_census(cores[i], edges, maps[i])
        solutions[i, code] = result
        fibers.append({'core': i, 'type': code, 'first_column_orbits': nr,
                       'fiber_tuples': nf, 'residual_sha256': residual_hash})
    rows = verify_representatives(data, solutions, cores)
    check(len(data['representatives']) == 13, 'representative count')
    print(json.dumps({'cases': rows, 'fibers': fibers, 'graphs': 13,
                      'labeled_tuples': sum(len(v) for v in solutions.values())},
                     sort_keys=True, separators=(',', ':')))

if __name__ == '__main__':
    main()
