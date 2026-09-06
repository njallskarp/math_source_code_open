"""Independent graph6/bitset witness audit; imports no construction/checker code."""
import base64
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def need(test, message):
    if not test:
        raise ValueError(message)


def decode(text):
    raw = base64.b64decode(text, validate=True)
    need(len(raw) == 40 and raw[0] == 85, 'graph6 order/length')
    packed = 0
    for b in raw[1:]:
        need(63 <= b <= 126, 'graph6 alphabet')
        packed = (packed << 6) | (b - 63)
    need(packed & 7 == 0, 'graph6 padding')
    rows, shift = [0] * 22, 233
    for j in range(1, 22):
        for i in range(j):
            if packed >> shift & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
            shift -= 1
    need(shift == 2, 'graph6 bit count')
    return rows


def cliques(rows, k):
    def visit(mask, left):
        if mask.bit_count() == k:
            yield mask
        elif mask.bit_count() + left.bit_count() >= k:
            while left:
                bit = left & -left
                left ^= bit
                yield from visit(mask | bit, left & rows[bit.bit_length() - 1])
    return list(visit(0, (1 << len(rows)) - 1))


def component_masks(rows, deleted):
    left = ((1 << len(rows)) - 1) & ~deleted
    result = []
    while left:
        reached = left & -left
        while True:
            enlarged, todo = reached, reached
            while todo:
                bit = todo & -todo
                todo ^= bit
                enlarged |= rows[bit.bit_length() - 1] & left
            if enlarged == reached:
                break
            reached = enlarged
        left &= ~reached
        result.append(reached)
    return result


def controls():
    comparisons = 0
    for n in range(6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            E = {p for i, p in enumerate(pairs) if mask >> i & 1}
            rows = [sum(1 << v for v in range(n) if tuple(sorted((u, v))) in E) for u in range(n)]
            for k in (3, 4, 5):
                want = {sum(1 << v for v in S) for S in combinations(range(n), k)
                        if all(p in E for p in combinations(S, 2))}
                need(set(cliques(rows, k)) == want, 'small graph clique control')
                comparisons += 1
    return comparisons


if __name__ == '__main__':
    data = json.loads((Path(__file__).parent / 'WITNESS.json').read_text())
    rows = decode(data['graph6_base64'])
    blue = [((1 << 22) - 1) ^ (1 << i) ^ r for i, r in enumerate(rows)]
    need(not cliques(rows, 4) and not cliques(blue, 5), 'Ramsey property')
    edges = [(i, j) for i in range(22) for j in range(i + 1, 22) if rows[i] >> j & 1]
    digest = sha256((json.dumps(edges, separators=(',', ':')) + '\n').encode('ascii')).hexdigest()
    need(digest == data['edge_sha256'] and len(edges) == 108, 'edge identity')
    checked = 0
    for k in range(4):
        for S in combinations(range(22), k):
            need(len(component_masks(rows, sum(1 << x for x in S))) == 1, 'small vertex cut')
            checked += 1
    parts = sorted(x.bit_count() for x in component_masks(rows, sum(1 << x for x in data['separator'])))
    need(parts == [1, 17], 'four-cut')
    cycle = data['hamilton_cycle']
    need(sorted(cycle) == list(range(22)) and all(rows[u] >> v & 1
         for u, v in zip(cycle, cycle[1:] + cycle[:1])), 'Hamilton cycle')
    print(json.dumps({'audit': 'PASS', 'edges': len(edges), 'edge_sha256': digest,
                      'small_cuts_checked': checked, 'four_cut_parts': parts,
                      'small_graph_clique_controls': controls()}, sort_keys=True))
