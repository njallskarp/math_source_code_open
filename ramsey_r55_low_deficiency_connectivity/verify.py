"""Definition-level construction and finite arithmetic checks; standard library."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def need(test, message):
    if not test:
        raise ValueError(message)


def construct(data):
    need(data['order'] == 22 and data['paley_order'] == 17, 'orders')
    need(data['separator'] == [17, 18, 19, 20], 'separator labels')
    need(data['isolated_after_cut'] == 21, 'isolated label')
    squares = {x * x % 17 for x in range(1, 17)}
    edges = {p for p in combinations(range(17), 2) if (p[1] - p[0]) % 17 in squares}
    need(len(data['red_signatures']) == 4, 'signature count')
    for v, signature in enumerate(data['red_signatures'], 17):
        need(len(signature) == 8 and signature == sorted(set(signature))
             and all(type(x) is int and 0 <= x < 17 for x in signature), 'signature schema')
        edges.update((x, v) for x in signature)
    edges.update([(17, 18), (18, 19), (19, 20), (17, 20)])
    edges.update((x, 21) for x in range(17, 21))
    return edges


def monochromatic(n, edges, k, red):
    return [S for S in combinations(range(n), k)
            if all((p in edges) == red for p in combinations(S, 2))]


def components(n, edges, removed):
    remaining = set(range(n)) - set(removed)
    answer = []
    while remaining:
        seen, todo = set(), [min(remaining)]
        while todo:
            u = todo.pop()
            if u in seen:
                continue
            seen.add(u)
            todo.extend(v for v in remaining - seen if tuple(sorted((u, v))) in edges)
        remaining -= seen
        answer.append(sorted(seen))
    return sorted(answer, key=lambda C: (len(C), C))


def edge_hash(edges):
    raw = (json.dumps(sorted(edges), separators=(',', ':')) + '\n').encode('ascii')
    return sha256(raw).hexdigest()


def check(data):
    edges = construct(data)
    need(len(edges) == 108, 'edge count')
    need(edge_hash(edges) == data['edge_sha256'], 'edge identity')
    need(not monochromatic(22, edges, 4, True), 'red K4')
    need(not monochromatic(22, edges, 5, False), 'independent five-set')
    cuts_checked = 0
    for k in range(4):
        for S in combinations(range(22), k):
            need(len(components(22, edges, S)) == 1, 'cut smaller than four')
            cuts_checked += 1
    cut = components(22, edges, data['separator'])
    need(cut == [[21], list(range(17))], 'displayed cut components')
    degrees = Counter(sum(v in e for e in edges) for v in range(22))
    need(min(degrees) == 4, 'minimum degree')
    cycle = data['hamilton_cycle']
    need(len(cycle) == 22 and set(cycle) == set(range(22)), 'Hamilton cycle vertices')
    need(all(tuple(sorted((cycle[i], cycle[(i + 1) % 22]))) in edges for i in range(22)), 'Hamilton cycle edges')
    # Adding a universal red root is a 23-vertex local cone, never a K43 claim.
    cone = edges | {(v, 22) for v in range(22)}
    need(not monochromatic(23, cone, 5, True)
         and not monochromatic(23, cone, 5, False), 'local cone')
    return {'order': 22, 'edges': 108, 'deficiency_using_U22_114': 6,
            'red_k4': 0, 'blue_k5': 0, 'connectivity': 4,
            'checked_cuts_size_at_most_three': cuts_checked,
            'displayed_cut_component_sizes': list(map(len, cut)),
            'degree_multiplicities': dict(sorted(degrees.items())),
            'local_cone_order': 23, 'local_cone_monochromatic_k5': 0,
            'hamilton_cycle_checked': True,
            'edge_sha256': edge_hash(edges)}


def partitions(n, lower=1):
    if n == 0:
        yield ()
    for first in range(lower, n + 1):
        for rest in partitions(n - first, first):
            yield (first,) + rest


def separator_arithmetic():
    # If independence numbers add to at most four, component capacities are
    # 3,8,17 at alpha=1,2,3, using R(4,2), R(4,3), R(4,4).
    capacities = {1: 3, 2: 8, 3: 17}
    budget_cases = [P for total in range(2, 5) for P in partitions(total) if len(P) >= 2]
    large = [P for P in budget_cases if sum(capacities[a] for a in P) >= 19]
    need(large == [(1, 3)], 'large disconnected profile')
    rows = []
    for s in range(4):
        for b in range(1, 4):
            a = 22 - s - b
            if 1 <= a <= 17:
                bound = 4 * a + 8 * s + (s + b) ** 2 // 3
                rows.append([s, a, b, bound])
    need(rows == [[2, 17, 3, 92], [3, 17, 2, 100], [3, 16, 3, 100]], 'separator bound rows')
    return {'independence_partitions': len(budget_cases), 'separator_rows': rows,
            'maximum_edges_with_cut_at_most_three': max(r[3] for r in rows),
            'four_connectivity_sufficient_edges': 101}


if __name__ == '__main__':
    data = json.loads((Path(__file__).parent / 'WITNESS.json').read_text())
    print(json.dumps({'arithmetic': separator_arithmetic(), 'witness': check(data)}, sort_keys=True))
