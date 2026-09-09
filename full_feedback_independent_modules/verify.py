#!/usr/bin/env python3
"""Exact audits for THEOREM.md, Python >=3.10, standard library only."""
from collections import Counter, deque
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json


def require(test, message):
    if not test:
        raise AssertionError(message)


def graphs(n):
    edges = list(combinations(range(n), 2))
    for mask in range(1 << len(edges)):
        g = [set() for _ in range(n)]
        for i, (u, v) in enumerate(edges):
            if mask >> i & 1:
                g[u].add(v)
                g[v].add(u)
        yield g


def distances(g, p):
    d = {p: 0}
    q = deque([p])
    while q:
        u = q.popleft()
        for v in sorted(g[u]):
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d


def responses(g):
    n = len(g)
    ds = [distances(g, p) for p in range(n)]
    require(all(len(d) == n for d in ds), 'disconnected graph')
    return [[frozenset([p]) if p == x else
             frozenset(y for y in g[p] if ds[y][x] + 1 == ds[p][x])
             for x in range(n)] for p in range(n)]


def blowup(base, sizes):
    g = []; modules = []; labels = []
    for u, size in enumerate(sizes):
        module = list(range(len(g), len(g) + size))
        modules.append(module)
        g.extend(set() for _ in module)
        labels.extend([u] * size)
    for u in range(len(base)):
        for v in base[u]:
            for x in modules[u]:
                g[x].update(modules[v])
    return g, modules, labels


def closed(g, s):
    return frozenset(s).union(*(g[x] for x in s))


def partitions(response, p, s):
    parts = {}
    for x in sorted(s):
        parts.setdefault(response[p][x], set()).add(x)
    return [frozenset(part) for part in parts.values()]


def policy_duration(base, sizes, p):
    """Explore every response branch of the written constructive strategy."""
    g, modules, labels = blowup(base, sizes)
    response = responses(g)
    nodes = 0

    @lru_cache(None)
    def finish(posterior):
        nonlocal nodes
        if len(posterior) == 1:
            return 0
        nodes += 1
        v = labels[next(iter(posterior))]
        require(all(labels[x] == v for x in posterior), 'module not known')
        outside = g[modules[v][0]]
        probe = min(outside) if len(outside) == 1 else min(posterior)
        branches = []
        for part in partitions(response, probe, closed(g, posterior)):
            if len(part) == 1:
                branches.append(0)
            else:
                require(part < posterior, ('finisher did not decrease', posterior, part))
                branches.append(finish(part))
        return 1 + max(branches)

    @lru_cache(None)
    def scan(territory, i):
        nonlocal nodes
        nodes += 1
        require(i < sizes[p], 'scan exceeded its module')
        probe = modules[p][i]
        branches = []
        for part in partitions(response, probe, territory):
            if len(part) == 1:
                branches.append(0)
            elif len({labels[x] for x in part}) == 1:
                branches.append(finish(part))
            else:
                require(i + 1 < sizes[p], 'multimodule posterior after full scan')
                branches.append(scan(closed(g, part), i + 1))
        return 1 + max(branches)

    full = frozenset(range(len(g)))
    if len(base) == 2:
        small = min(range(2), key=lambda v: sizes[v])
        probe = modules[small][0]
        value = 1 + max(finish(part) for part in partitions(response, probe, full))
    else:
        value = scan(full, 0)
    require(value <= sizes[p] + max(sizes) - 1, ('round bound', base, sizes, p, value))
    return value, nodes


def audit_general_policy():
    c = Counter(); duration_histogram = Counter()
    for n in range(2, 5):
        for base in graphs(n):
            if len(distances(base, 0)) != n:
                continue
            response = responses(base)
            resolvers = [p for p in range(n) if len(set(response[p])) == n]
            if not resolvers:
                continue
            c['quotient_graphs'] += 1
            c['quotient_resolvers'] += len(resolvers)
            for sizes in product(range(1, 4), repeat=n):
                for p in resolvers:
                    value, nodes = policy_duration(base, sizes, p)
                    c['policy_instances'] += 1
                    c['policy_nonterminal_nodes'] += nodes
                    duration_histogram[value] += 1
    return {'counts': dict(sorted(c.items())),
            'duration_histogram': dict(sorted(duration_histogram.items()))}


def cube_substitution(m):
    base = [{v ^ (1 << bit) for bit in range(3)} for v in range(8)]
    return blowup(base, [m] * 8)[0]


def bit_partitions(g):
    response = responses(g)
    result = []
    for p in range(len(g)):
        parts = {}
        for x in range(len(g)):
            r = response[p][x]
            parts[r] = parts.get(r, 0) | (1 << x)
        result.append(tuple(parts.values()))
    return result


def bit_spreader(g):
    adj = [sum(1 << v for v in g[u]) for u in range(len(g))]

    @lru_cache(None)
    def spread(s):
        out = s
        rest = s
        while rest:
            bit = rest & -rest
            rest ^= bit
            out |= adj[bit.bit_length() - 1]
        return out
    return spread


def all_cores(m):
    """All nonempty subsets supported on one antipodal module pair."""
    cores = set()
    for u in range(4):  # u < (u xor 7), so each pair is used exactly once.
        vs = [u * m + i for i in range(m)] + [(u ^ 7) * m + i for i in range(m)]
        for mask in range(1, 1 << (2 * m)):
            cores.add(sum(1 << vs[i] for i in range(2 * m) if mask >> i & 1))
    return cores


def audit_core_invariant(m):
    g = cube_substitution(m)
    parts = bit_partitions(g)
    spread = bit_spreader(g)
    cores = all_cores(m)
    checks = 0
    for core in sorted(cores):
        size = core.bit_count()
        if size < 3:
            continue
        territory = spread(core)
        for probe_parts in parts:
            # This existential audit scans actual response classes; it does
            # not encode the proof's distance cases or its chosen responses.
            require(any((b := territory & block) in cores and
                        b.bit_count() >= max(2, size - 1) for block in probe_parts),
                    ('core invariant failed', m, core))
            checks += 1
    return {'m': m, 'nonempty_cores': len(cores), 'core_probe_checks': checks}


def exact_duration(m):
    """Complete reachable belief game, then least finite-horizon fixed point."""
    g = cube_substitution(m)
    parts = bit_partitions(g)
    spread = bit_spreader(g)
    full = (1 << len(g)) - 1
    states = [full]; seen = {full}; transitions = {}
    for s in states:
        actions = []
        for probe_parts in parts:
            children = frozenset(spread(b) for block in probe_parts
                                 if (b := s & block).bit_count() > 1)
            actions.append(children)
            for child in sorted(children):
                if child not in seen:
                    seen.add(child)
                    states.append(child)
                    require(len(states) <= 50000, 'finite game size limit exceeded')
        transitions[s] = actions
    rank = {}; level = 0
    while True:
        level += 1
        new = [s for s in states if s not in rank and
               any(all(child in rank for child in action) for action in transitions[s])]
        if not new:
            break
        for s in new:
            rank[s] = level
    require(full in rank, ('no winning strategy', m))
    require(rank[full] == 2 * m - 1, ('duration mismatch', m, rank[full]))
    return {'m': m, 'vertices': len(g), 'reachable_beliefs': len(states),
            'winning_beliefs': len(rank), 'optimal_rounds': rank[full]}


def main():
    result = {
        'general_policy': audit_general_policy(),
        'core_invariant': [audit_core_invariant(m) for m in range(1, 6)],
        'complete_belief_games': [exact_duration(m) for m in range(1, 5)],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
    print(json.dumps(result, sort_keys=True, indent=2))
    print('result_sha256=' + sha256(canonical).hexdigest())
    print('VERIFIED')


if __name__ == '__main__':
    main()
