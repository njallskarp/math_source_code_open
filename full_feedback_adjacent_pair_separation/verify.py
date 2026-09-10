#!/usr/bin/env python3
"""Exact Tutte 12-cage certificate verification; standard library only."""
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

LCF = (17, 27, -13, -59, -35, 35, -11, 13, -53,
       53, -27, 21, 57, 11, -21, -57, 59, -17)
ORDER = 126
ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph():
    edges = {tuple(sorted((v, (v + 1) % ORDER))) for v in range(ORDER)}
    edges.update(tuple(sorted((v, (v + LCF[v % len(LCF)]) % ORDER)))
                 for v in range(ORDER))
    adjacency = [set() for _ in range(ORDER)]
    for u, v in edges:
        require(u != v, 'loop')
        adjacency[u].add(v)
        adjacency[v].add(u)
    require(len(edges) == 189, 'wrong size')
    require(all(len(a) == 3 for a in adjacency), 'not cubic')
    return adjacency, sorted(edges)


def distances(adjacency, source, omitted_edge=None):
    row = {source: 0}
    queue = deque([source])
    while queue:
        v = queue.popleft()
        for w in adjacency[v]:
            if omitted_edge is not None and tuple(sorted((v, w))) == omitted_edge:
                continue
            if w not in row:
                row[w] = row[v] + 1
                queue.append(w)
    return row


def response_table(adjacency, distance):
    return [[frozenset([p]) if p == x else
             frozenset(w for w in adjacency[p]
                       if distance[w][x] + 1 == distance[p][x])
             for x in range(ORDER)] for p in range(ORDER)]


def check_evasion(adjacency, edges, distance, responses):
    """Every territory and every edge action, with no symmetry reduction."""
    pairs = [(a, b) for a, b in combinations(range(ORDER), 2)
             if 2 <= distance[a][b] <= 4]
    pair_counts = Counter(distance[a][b] for a, b in pairs)
    require(dict(pair_counts) == {2: 378, 3: 756, 4: 1512}, 'wrong core census')
    obligations = 0
    digest = sha256()
    for a, b in pairs:
        territory = {a, b} | adjacency[a] | adjacency[b]
        candidates = [(x, y) for x, y in combinations(sorted(territory), 2)
                      if 2 <= distance[x][y] <= 4]
        for p, q in edges:
            witness = next(((x, y) for x, y in candidates
                            if responses[p][x] == responses[p][y]
                            and responses[q][x] == responses[q][y]), None)
            require(witness is not None,
                    f'evasion fails for core {(a, b)} and probes {(p, q)}')
            x, y = witness
            # These two actual targets have one joint response. After a legal
            # edge-or-stay move their closed neighborhood is a new lower core.
            digest.update(f'{a},{b},{p},{q},{x},{y}\n'.encode('ascii'))
            obligations += 1
    require(obligations == 500094, 'incomplete evasion coverage')
    return {'core_pairs': len(pairs),
            'core_pairs_by_distance': dict(sorted(pair_counts.items())),
            'edge_actions_per_core': len(edges),
            'checked_obligations': obligations,
            'witness_sha256': digest.hexdigest()}


def check_policy(data, adjacency, responses):
    require(set(data) == {'depth', 'nodes'}, 'unexpected policy fields')
    require(data['depth'] == 3, 'wrong root rank')
    policy = {}
    for row in data['nodes']:
        require(isinstance(row, list) and len(row) == 4, 'bad policy row')
        mask, rank, p, q = row
        require(all(type(v) is int for v in row), 'noninteger policy entry')
        require(0 < mask < (1 << ORDER) and 1 <= rank <= 3, 'bad territory/rank')
        require(0 <= p < ORDER and 0 <= q < ORDER and p != q, 'bad probe pair')
        require((mask, rank) not in policy, 'duplicate policy node')
        policy[(mask, rank)] = (p, q)
    root = ((1 << ORDER) - 1, data['depth'])
    pending = [root]
    seen = set()
    unresolved = 0
    singletons = 0
    while pending:
        key = pending.pop()
        if key in seen:
            continue
        seen.add(key)
        require(key in policy, 'missing reachable policy node')
        mask, rank = key
        p, q = policy[key]
        classes = defaultdict(set)
        for x in range(ORDER):
            if (mask >> x) & 1:
                classes[(responses[p][x], responses[q][x])].add(x)
        for posterior in classes.values():
            if len(posterior) == 1:
                singletons += 1
                continue
            require(rank > 1, 'unresolved terminal response')
            territory = set(posterior)
            for x in posterior:
                territory.update(adjacency[x])
            child = sum(1 << x for x in territory)
            require((child, rank - 1) in policy, 'missing legal response child')
            pending.append((child, rank - 1))
            unresolved += 1
    require(seen == set(policy), 'unused policy nodes')
    return {'round_bound': data['depth'], 'policy_nodes': len(seen),
            'unresolved_response_branches': unresolved,
            'singleton_response_branches': singletons,
            'initial_probes': list(policy[root])}


def reject_mutations(data, adjacency, responses):
    # Checks target meaningful obligations, not the certificate's byte hash.
    mutations = []
    missing = json.loads(json.dumps(data))
    missing['nodes'].pop(0)
    mutations.append(missing)
    repeated_probe = json.loads(json.dumps(data))
    repeated_probe['nodes'][0][3] = repeated_probe['nodes'][0][2]
    mutations.append(repeated_probe)
    wrong_first_action = json.loads(json.dumps(data))
    for row in wrong_first_action['nodes']:
        if row[1] == 3:
            row[2:] = [0, 1]  # An edge, which cannot be a winning root action.
    mutations.append(wrong_first_action)
    for mutation in mutations:
        try:
            check_policy(mutation, adjacency, responses)
        except ValueError:
            pass
        else:
            raise ValueError('corrupted policy accepted')
    return len(mutations)


def main():
    adjacency, edges = graph()
    distance = [distances(adjacency, v) for v in range(ORDER)]
    require(all(len(row) == ORDER for row in distance), 'disconnected graph')
    require(all(Counter(row.values()) ==
                Counter({0: 1, 1: 3, 2: 6, 3: 12, 4: 24, 5: 48, 6: 32})
                for row in distance), 'unexpected distance layers')
    require(all((distance[0][u] - distance[0][v]) % 2 for u, v in edges),
            'not bipartite')
    girth = min(distances(adjacency, u, (u, v))[v] + 1 for u, v in edges)
    require(girth == 12, 'wrong girth')
    responses = response_table(adjacency, distance)
    policy_bytes = (ROOT / 'policy.json').read_bytes()
    data = json.loads(policy_bytes)
    result = {'graph': {'order': ORDER, 'size': len(edges), 'degree': 3,
                        'diameter': 6, 'girth': girth, 'bipartite': True},
              'evasion': check_evasion(adjacency, edges, distance, responses),
              'winning_policy': check_policy(data, adjacency, responses),
              'rejected_policy_mutations': reject_mutations(data, adjacency, responses),
              'policy_sha256': sha256(policy_bytes).hexdigest()}
    canonical = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
    print(json.dumps(result, indent=2, sort_keys=True))
    print('result_sha256=' + sha256(canonical).hexdigest())
    print('VERIFIED: unrestricted two probes win; every adjacent-pair strategy loses')


if __name__ == '__main__':
    main()
