"""Uniform exact allocations; these are not 43-vertex Ramsey graphs."""
from functools import lru_cache
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
P = json.loads((ROOT / 'parameters.json').read_text())
U = dict(zip(range(18, 25), P['U']))


def degree_word(word):
    n = ord(word[0]) - 63
    bits = ''.join(format(ord(c) - 63, '06b') for c in word[1:])
    ds = [0] * n
    at = 0
    for j in range(1, n):
        for i in range(j):
            if bits[at] == '1':
                ds[i] += 1; ds[j] += 1
            at += 1
    return sorted(ds)


def realize(values):
    """Construct a graph by Havel-Hakimi, then check its literal degrees."""
    remaining = list(values)
    edges = set()
    while max(remaining, default=0):
        v = max(range(len(values)), key=lambda i: (remaining[i], -i))
        demand = remaining[v]
        candidates = sorted((i for i in range(len(values)) if i != v and remaining[i]),
                            key=lambda i: (-remaining[i], i))
        if demand > len(candidates):
            raise ValueError('Non-graphical allocation')
        remaining[v] = 0
        for w in candidates[:demand]:
            remaining[w] -= 1
            edge = tuple(sorted((v, w)))
            if remaining[w] < 0 or edge in edges:
                raise ValueError('Realization failed')
            edges.add(edge)
    actual = [0] * len(values)
    for i, j in edges:
        actual[i] += 1; actual[j] += 1
    if actual != values:
        raise ValueError('Degree certificate failed')
    return len(edges)


def balanced(n, total, pin=None):
    count = n if pin is None else n - 1
    base, extra = divmod(total - (0 if pin is None else pin), count)
    result = ([] if pin is None else [pin]) + [base + 1] * extra + [base] * (count - extra)
    realize(result)
    return result


@lru_cache(maxsize=None)
def neighbor_rows(degrees, red, blue):
    """Certify each row separately by exact cardinality subset-sum.

    These selections are not required to be reciprocal and are not a graph.
    """
    rows = []
    m = sum(degrees) // 2
    for v, d in enumerate(degrees):
        required = [1-v] if v < 2 else [v+20] if 3 <= v < 23 else [v-20] if v >= 23 else []
        need = d - len(required)
        target = m + U[d]-red[v] + U[42-d]-blue[v] - math.comb(42-d,2) - sum(degrees[w] for w in required)
        candidates = [w for w in range(43) if w != v and w not in required]
        states = [[1] + [0]*need]
        for w in candidates:
            old = states[-1]
            states.append([1] + [old[k] | (old[k-1] << degrees[w]) for k in range(1,need+1)])
        if target < 0 or not ((states[-1][need] >> target) & 1):
            raise ValueError('No pointwise neighbor-degree selection')
        selected = required[:]
        for at in range(len(candidates)-1,-1,-1):
            if not ((states[at][need] >> target) & 1):
                w = candidates[at]
                selected.append(w); need -= 1; target -= degrees[w]
        if need or target:
            raise ValueError('Subset-sum reconstruction failed')
        rows.append(tuple(sorted(selected)))
    return tuple(rows)


def cells():
    for d in range(18, 25):
        for p in range(18, 25):
            for q in range(P['q0'][d - 18], 14):
                yield d, p, q


def construct(d, p, q):
    if (d, p, q) not in set(cells()):
        raise ValueError('Not a low-deficiency scalar cell')
    degrees = [d, p, 20 if (d + p) % 2 == 0 else 21] + [22] * 20 + [23] * 20
    realize(degrees)
    omega = sum(21 if x in (18, 24) else 12 if x in (19, 23) else 3 if x in (20, 22) else 0 for x in degrees)
    if (1247 - omega) % 2:
        raise ValueError('Deficiency parity')
    total = (1247 - omega) // 2
    red = [6, 6, 6] + [5] * 20 + [9] * 20
    red[2] += (sum(U[x] for x in degrees) - sum(red)) % 3
    blue_budget = total - sum(red)
    blue = [3] * 43
    priority = [v for v in (0,1) if degrees[v] == 18]
    order = priority + list(range(3, 43)) + [v for v in (0,1,2) if v not in priority]
    for i in range(blue_budget - 129):
        blue[order[i % 43]] += 1
    local = {'red': [], 'blue': []}
    anchor_word = degree_word(P['interfaces'][8])
    for v, degree in enumerate(degrees):
        for color in ('red', 'blue'):
            n = degree if color == 'red' else 42 - degree
            deficiency = (red if color == 'red' else blue)[v]
            if color == 'red' and 3 <= v < 23:
                word = anchor_word[:]
                realize(word)
            else:
                pin = q if color == 'red' and v < 2 else 5 if color == 'red' and v >= 23 else None
                word = balanced(n, 2 * (U[n] - deficiency), pin)
            local[color].append(word)
    return {'cell': [d, p, q], 'cell_sizes': [q, d - 1 - q, p - 1 - q, 43 - d - p + q],
            'degrees': degrees, 'neighbor_selections': [list(row) for row in neighbor_rows(tuple(degrees),tuple(red),tuple(blue))], 'deficiencies': {'red': red, 'blue': blue}, 'local_degrees': local,
            'anchors': {'red': [{'vertex': v, 'hub': v + 20, 'interface': 8} for v in range(3, 23)], 'blue': []}}


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('usage: python3 -B construct.py d p q')
    print(json.dumps(construct(*(int(x) for x in sys.argv[1:])), separators=(',', ':'), sort_keys=True))
