#!/usr/bin/env python3
"""Independent h4291 audit. Python 3.10+ standard library; no author imports.

All-pairs Floyd--Warshall distances and shortest-path prefix unions replace
the author's BFS distance/neighbor-distance implementation. Evasion is a
dual covering calculation over response-equivalent pairs, rather than a
search for one witness per core. Only the untrusted policy JSON is imported.
"""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

N = 126
SHIFTS = (17, 27, -13, -59, -35, 35, -11, 13, -53,
          53, -27, 21, 57, 11, -21, -57, 59, -17)
HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'full_feedback_adjacent_pair_separation' / 'policy.json'
POLICY_SHA = '8753aa21c22b1726e5a676b37b5c93c2f796c5a9cc49b2ec70ca1a8bb5846ed8'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def bits(mask):
    while mask:
        one = mask & -mask
        yield one.bit_length() - 1
        mask ^= one


def build():
    adj = [[False] * N for _ in range(N)]
    for u in range(N):
        for v in ((u - 1) % N, (u + 1) % N,
                  (u + SHIFTS[u % 18]) % N):
            adj[u][v] = adj[v][u] = True
    edges = [(u, v) for u in range(N) for v in range(u + 1, N) if adj[u][v]]
    neighbors = [tuple(v for v in range(N) if adj[u][v]) for u in range(N)]
    need(all(not adj[u][u] and len(neighbors[u]) == 3 for u in range(N)), 'cubic graph')
    need(len(edges) == 189, 'edge census')
    dist = [[0 if u == v else 1 if adj[u][v] else N
             for v in range(N)] for u in range(N)]
    for k in range(N):
        for u in range(N):
            for v in range(N):
                via = dist[u][k] + dist[k][v]
                if via < dist[u][v]:
                    dist[u][v] = via
    layers = [1, 3, 6, 12, 24, 48, 32]
    need(all([row.count(d) for d in range(7)] == layers for row in dist), 'distance layers')
    need(all((dist[0][u] + dist[0][v]) % 2 == 1 for u, v in edges), 'bipartite graph')
    # In a cubic graph, these full binary tree layers through radius five
    # exclude cycles through length ten. Bipartiteness excludes odd cycles.
    # Explicitly find a twelve-cycle to close the girth check.
    cycle = []
    def extend(path):
        if len(path) == 12:
            if adj[path[-1]][path[0]]:
                cycle.extend(path)
                return True
            return False
        return any(extend(path + [v]) for v in neighbors[path[-1]] if v not in path)
    need(extend([0]), 'twelve-cycle')
    responses = [[0] * N for _ in range(N)]
    for p in range(N):
        responses[p][p] = 1 << p
        for x in neighbors[p]:
            responses[p][x] = 1 << x
        for depth in range(2, 7):
            for x in range(N):
                if dist[p][x] == depth:
                    for v in neighbors[x]:
                        if dist[p][v] == depth - 1:
                            responses[p][x] |= responses[p][v]
        need(all(responses[p]), 'empty direction response')
    closed = [frozenset((u,) + neighbors[u]) for u in range(N)]
    return edges, neighbors, dist, responses, closed, cycle


def evasion(edges, dist, response, closed):
    cores = [(a, b) for a, b in combinations(range(N), 2) if 2 <= dist[a][b] <= 4]
    count = Counter(dist[a][b] for a, b in cores)
    need(dict(count) == {2: 378, 3: 756, 4: 1512}, 'core census')
    containing = [0] * N
    by_distance = {d: 0 for d in (2, 3, 4)}
    for i, (a, b) in enumerate(cores):
        by_distance[dist[a][b]] |= 1 << i
        for x in closed[a] | closed[b]:
            containing[x] |= 1 << i
    all_cores = (1 << len(cores)) - 1
    failures = Counter()
    support_histogram = Counter()
    incidence_total = 0
    witness_pair_total = 0
    # Reverse the quantifiers computationally: a response-equivalent pair
    # covers exactly the cores containing both targets. No graph symmetry.
    for p, q in edges:
        classes = defaultdict(list)
        for x in range(N):
            classes[(response[p][x], response[q][x])].append(x)
        covered = {d: 0 for d in (2, 3, 4)}
        for targets in classes.values():
            for x, y in combinations(targets, 2):
                d = dist[x][y]
                if d in covered:
                    support = containing[x] & containing[y]
                    covered[d] |= support
                    witness_pair_total += 1
                    incidence_total += support.bit_count()
                    support_histogram[support.bit_count()] += 1
        need(covered[2] | covered[3] | covered[4] == all_cores,
             f'uncovered core for edge {(p, q)}')
        # Test all nonempty distance-subfamilies, to check whether the
        # published invariant can be simplified in this particular way.
        for subset in range(1, 8):
            required = actual = 0
            for j, d in enumerate((2, 3, 4)):
                if subset & (1 << j):
                    required |= by_distance[d]
                    actual |= covered[d]
            failures[subset] += (required & ~actual).bit_count()
    return {'core_pairs_by_distance': dict(sorted(count.items())),
            'edge_actions': len(edges), 'obligations': len(cores) * len(edges),
            'equivalent_witness_pairs_across_edges': witness_pair_total,
            'witness_core_incidences': incidence_total,
            'support_size_histogram': dict(sorted(support_histogram.items())),
            'distance_subfamily_failed_obligations': {
                ','.join(str(d) for j, d in enumerate((2, 3, 4)) if subset & (1 << j)): failures[subset]
                for subset in range(1, 8)}}


def decode_policy(data):
    need(set(data) == {'depth', 'nodes'} and data['depth'] == 3, 'policy header')
    policy = {}
    for row in data['nodes']:
        need(isinstance(row, list) and len(row) == 4 and
             all(type(x) is int for x in row), 'integer row')
        mask, rank, p, q = row
        need(0 < mask < 1 << N and 1 <= rank <= 3 and
             0 <= p < N and 0 <= q < N and p != q, 'row domain')
        state = frozenset(bits(mask))
        need(state not in policy, 'duplicate territory')
        policy[state] = (rank, p, q)
    return policy


def refined_invariant(edges, dist, neighbors, closed):
    """Direct check of the newly observed even-distance subfamily.

    Deliberately uses the local neighbor-distance response formula instead
    of the prefix-union response table, and core-first witness enumeration
    instead of the dual covering calculation.
    """
    direction = [[frozenset([p]) if p == x else
                  frozenset(w for w in neighbors[p] if dist[w][x] == dist[p][x] - 1)
                  for x in range(N)] for p in range(N)]
    checked = 0
    digest = sha256()
    for a, b in combinations(range(N), 2):
        if dist[a][b] not in (2, 4):
            continue
        pairs = [(x, y) for x, y in combinations(sorted(closed[a] | closed[b]), 2)
                 if dist[x][y] in (2, 4)]
        for p, q in edges:
            witness = next(((x, y) for x, y in pairs if
                            direction[p][x] == direction[p][y] and
                            direction[q][x] == direction[q][y]), None)
            need(witness is not None, 'even-distance invariant fails')
            x, y = witness
            digest.update(f'{a},{b},{p},{q},{x},{y}\n'.encode())
            checked += 1
    need(checked == 357210, 'even-distance cover incomplete')
    return {'core_pairs': 1890, 'checked_obligations': checked,
            'witness_sha256': digest.hexdigest()}


def verify_policy(data, response, closed):
    policy = decode_policy(data)
    root = frozenset(range(N))
    need(root in policy and policy[root][0] == 3, 'root')
    visited = set()
    singles = unresolved = 0
    ranks = Counter()
    def visit(state):
        nonlocal singles, unresolved
        need(state in policy, 'missing next territory')
        if state in visited:
            return
        visited.add(state)
        rank, p, q = policy[state]
        ranks[rank] += 1
        posteriors = defaultdict(set)
        for x in state:
            posteriors[(response[p][x], response[q][x])].add(x)
        for posterior in posteriors.values():
            if len(posterior) == 1:
                singles += 1
            else:
                unresolved += 1
                child = frozenset().union(*(closed[x] for x in posterior))
                need(rank > 1 and child in policy and policy[child][0] == rank - 1,
                     'rank transition')
                visit(child)
    visit(root)
    need(visited == set(policy), 'unreachable policy rows')
    # Independent physical-history replay: enumerate every legal length-two
    # robber walk. Reconstruct belief states from observed responses; no
    # certificate transition is taken on faith, even for merged states.
    caught = Counter()
    for x0 in range(N):
        for x1 in sorted(closed[x0]):
            for x2 in sorted(closed[x1]):
                territory = root
                for round_number, true_target in enumerate((x0, x1, x2), 1):
                    need(true_target in territory, 'legal target lost')
                    need(territory in policy, 'walk reaches missing policy state')
                    _, p, q = policy[territory]
                    posterior = {x for x in territory if
                                 response[p][x] == response[p][true_target] and
                                 response[q][x] == response[q][true_target]}
                    if len(posterior) == 1:
                        caught[round_number] += 1
                        break
                    territory = frozenset().union(*(closed[x] for x in posterior))
                else:
                    raise ValueError('legal robber walk survives three rounds')
    need(sum(caught.values()) == 2016, 'walk coverage')
    return {'rows': len(visited), 'rows_by_rank': dict(sorted(ranks.items())),
            'singleton_branches': singles, 'unresolved_branches': unresolved,
            'root_probes': list(policy[root][1:]),
            'length_two_legal_walks': sum(caught.values()),
            'walks_by_capture_round': dict(sorted(caught.items()))}


def mutation_checks(data, response, closed):
    rejected = 0
    # Every row is essential to this exact certificate.
    for i in range(len(data['nodes'])):
        mutated = {'depth': 3, 'nodes': data['nodes'][:i] + data['nodes'][i + 1:]}
        try:
            verify_policy(mutated, response, closed)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('missing row accepted')
    wrong_root = json.loads(json.dumps(data))
    for row in wrong_root['nodes']:
        if row[0] == (1 << N) - 1:
            row[2:] = [0, 1]
    try:
        verify_policy(wrong_root, response, closed)
    except ValueError:
        rejected += 1
    else:
        raise ValueError('adjacent root accepted')
    return rejected


def main():
    edges, neighbors, dist, response, closed, cycle = build()
    policy_bytes = INPUT.read_bytes()
    need(sha256(policy_bytes).hexdigest() == POLICY_SHA, 'policy bytes changed')
    data = json.loads(policy_bytes)
    result = {'graph': {'order': N, 'size': len(edges), 'degree': 3,
                        'diameter': 6, 'girth': 12, 'bipartite': True,
                        'twelve_cycle': cycle},
              'response_sha256': sha256(json.dumps(response, separators=(',', ':')).encode()).hexdigest(),
              'evasion': evasion(edges, dist, response, closed),
              'refined_even_distance_invariant': refined_invariant(edges, dist, neighbors, closed),
              'policy': verify_policy(data, response, closed),
              'rejected_policy_mutations': mutation_checks(data, response, closed),
              'policy_sha256': POLICY_SHA}
    output = json.dumps(result, sort_keys=True, indent=2)
    print(output)
    print('result_sha256=' + sha256(output.encode()).hexdigest())
    print('PASS: complete Tutte 12-cage adjacent-pair separation audit')


if __name__ == '__main__':
    main()
