#!/usr/bin/env python3
"""Exact finite audits for THEOREM.md; Python >=3.10, standard library only."""
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def graphs(n):
    """All labelled simple graphs on range(n), in edge-mask order."""
    edges = list(combinations(range(n), 2))
    for mask in range(1 << len(edges)):
        g = [set() for _ in range(n)]
        for i, (u, v) in enumerate(edges):
            if mask >> i & 1:
                g[u].add(v)
                g[v].add(u)
        yield g


def distances(g, source):
    d = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in sorted(g[u]):
            if v not in d:
                d[v] = d[u] + 1
                queue.append(v)
    return d


def responses(g):
    """Direct shortest-path definition, without quotient formulas."""
    n = len(g)
    ds = [distances(g, u) for u in range(n)]
    require(all(len(d) == n for d in ds), "disconnected graph")
    return [[frozenset([p]) if p == x else
             frozenset(w for w in g[p] if ds[w][x] + 1 == ds[p][x])
             for x in range(n)] for p in range(n)]


def substitute(base, internals):
    modules = []
    labels = []
    g = []
    for u, h in enumerate(internals):
        offset = len(g)
        module = list(range(offset, offset + len(h)))
        modules.append(module)
        labels.extend([u] * len(h))
        g.extend({offset + y for y in row} for row in h)
    for u in range(len(base)):
        for v in sorted(base[u]):
            for x in modules[u]:
                g[x].update(modules[v])
    return g, modules, labels


def audit_substitution():
    counts = Counter()
    # For two quotient vertices, allow every labelled internal graph through
    # order four; for three, through order three; for four, through order two.
    for n, internal_max in [(2, 4), (3, 3), (4, 2)]:
        options = [h for size in range(1, internal_max + 1) for h in graphs(size)]
        for base in graphs(n):
            if len(distances(base, 0)) != n:
                continue
            base_responses = responses(base)
            for internals in product(options, repeat=n):
                g, modules, labels = substitute(base, internals)
                response = responses(g)
                counts['substitution_graphs'] += 1
                for u in range(n):
                    for a in modules[u]:
                        for x in range(len(g)):
                            if labels[x] != u:
                                projected = frozenset(labels[y] for y in response[a][x])
                                require(projected == base_responses[u][labels[x]],
                                        ('projection', base, internals, a, x))
                                counts['projected_responses'] += 1
                    local = set(modules[u])
                    for v in base[u]:
                        local.update(modules[v])
                    for v in sorted(base[u]):
                        for a, b in product(modules[u], modules[v]):
                            signatures = [(response[a][x], response[b][x])
                                          for x in range(len(g))]
                            multiplicities = Counter(signatures)
                            for x in modules[u]:
                                require(multiplicities[signatures[x]] == 1,
                                        ('guard', base, internals, a, b, x))
                                counts['guarded_targets'] += 1
                            require(len({signatures[x] for x in local}) == len(local),
                                    ('finishing', base, internals, a, b))
                            counts['finishing_pairs'] += 1
    return dict(sorted(counts.items()))


def cube(d):
    return [{x ^ (1 << bit) for bit in range(d)} for x in range(1 << d)]


def neighborhood(g, vertices):
    result = set(vertices)
    for v in vertices:
        result.update(g[v])
    return result


def cube_lower_bounds(max_d):
    bounds = [[0, 1]]
    for d in range(1, max_d + 1):
        prev = bounds[-1]
        half = 1 << (d - 1)
        row = []
        for m in range(2 * half + 1):
            row.append(min(max(prev[a], m - a) + max(prev[m - a], a)
                           for a in range(max(0, m - half), min(half, m) + 1)))
        bounds.append(row)
    return bounds


def audit_cube():
    bounds = cube_lower_bounds(6)
    require(bounds[5][:14] == [0, 6, 10, 13, 15, 16, 16, 19, 21, 22, 22, 24, 25, 25],
            'incorrect dimension-five prefix')
    cases = [max(bounds[5][a], 13 - a) + max(bounds[5][13 - a], a)
             for a in range(14)]
    require(cases == [38, 37, 35, 35, 37, 37, 35, 35, 37, 37, 35, 35, 37, 38],
            'incorrect dimension-six split cases')
    require(bounds[6][13] == 35, 'required lower bound fails')
    subset_checks = 0
    for d in range(5):
        g = cube(d)
        closed = [sum(1 << y for y in neighborhood(g, [x])) for x in range(len(g))]
        union = [0] * (1 << len(g))
        for mask in range(len(union)):
            if mask:
                bit = mask & -mask
                union[mask] = union[mask ^ bit] | closed[bit.bit_length() - 1]
            require(union[mask].bit_count() >= bounds[d][mask.bit_count()],
                    ('cube lower bound', d, mask))
            subset_checks += 1
    q = cube(6)
    extremizer = {0} | {1 << j for j in range(6)}
    extremizer |= {1 | (1 << j) for j in range(1, 6)} | {2 | 4}
    require(len(extremizer) == 13 and len(neighborhood(q, extremizer)) == 35,
            'explicit neighborhood extremizer fails')
    q_responses = responses(q)
    require(all(len(set(row)) == 64 for row in q_responses), 'cube one-probe decoding')
    base = [{1}, {0}]
    join, modules, _ = substitute(base, [q, q])
    response = responses(join)
    far_cells = 0
    for side in range(2):
        other = frozenset(modules[1 - side])
        for p in modules[side]:
            cell = {x for x in range(128) if response[p][x] == other}
            intended = {x for x in modules[side] if ((p % 64) ^ (x % 64)).bit_count() >= 3}
            require(cell == intended and len(cell) == 42, ('far cell', p))
            far_cells += 1
    require(len({(response[0][x], response[64][x]) for x in range(128)}) == 128,
            'join two-probe injectivity')
    require(35 - (1 + 6 + 15) == 13 and bounds[6][13] >= 35,
            'robber invariant arithmetic')
    return {
        'cube_subsets_checked': subset_checks,
        'cube_lower_bound_6_13': bounds[6][13],
        'cube_extremizer': sorted(extremizer),
        'cube_extremizer_neighborhood': 35,
        'cube_split_cases': cases,
        'cube_bounds_sha256': sha256(json.dumps(bounds, separators=(',', ':')).encode()).hexdigest(),
        'join_vertices': len(join),
        'join_edges': sum(map(len, join)) // 2,
        'join_far_response_cells': far_cells,
        'join_far_cell_size': 42,
        'join_two_probe_distinct_responses': 128,
        'robber_invariant_module_size': 35,
        'robber_minimum_response_class': 13,
    }


def main():
    result = {'substitution': audit_substitution(), 'cube_join': audit_cube()}
    canonical = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
    print(json.dumps(result, sort_keys=True, indent=2))
    print('result_sha256=' + sha256(canonical).hexdigest())
    print('VERIFIED')


if __name__ == '__main__':
    main()
