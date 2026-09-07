"""Extract a physical K5 from a violating fork; no solver or catalogue."""
import itertools
import json
import sys


def graph(data):
    if not isinstance(data, dict) or set(data) != {'rows', 'fork', 'color'}:
        raise ValueError('Expected exactly rows, fork, color')
    rows = data['rows']
    if not isinstance(rows, list) or len(rows) != 43:
        raise ValueError('Expected 43 binary row strings')
    if any(not isinstance(r, str) or len(r) != 43 or set(r) - {'0', '1'} for r in rows):
        raise ValueError('Bad row')
    for i in range(43):
        if rows[i][i] != '0':
            raise ValueError('Nonzero diagonal')
        for j in range(i):
            if rows[i][j] != rows[j][i]:
                raise ValueError('Asymmetric graph')
    f = data['fork']
    if not isinstance(f, list) or len(f) != 3 or any(type(v) is not int or not 0 <= v < 43 for v in f) or len(set(f)) != 3:
        raise ValueError('Bad fork')
    color = data['color']
    if type(color) is not int or color not in (0, 1):
        raise ValueError('Bad color')
    adj = [sum(1 << j for j in range(43) if i != j and int(rows[i][j]) == color) for i in range(43)]
    u, r, s = f
    if not (adj[u] >> r & 1 and adj[u] >> s & 1):
        raise ValueError('Fork edges have wrong color')
    d, a, b = (adj[v].bit_count() for v in f)
    p = (adj[u] & adj[r]).bit_count()
    q = (adj[u] & adj[s]).bit_count()
    bound = a + b + d - 52 if adj[r] >> s & 1 else d - 10
    if p + q >= bound:
        raise ValueError('Outside the proved violating-fork family')
    return adj, (u, r, s), color


def vertices(mask):
    return [i for i in range(43) if mask >> i & 1]


def clique(adj, domain, size, present):
    for choice in itertools.combinations(domain, size):
        if all(bool(adj[a] >> b & 1) == present for a, b in itertools.combinations(choice, 2)):
            return list(choice)
    return None


def extract(data):
    adj, (u, r, s), color = graph(data)
    if not (adj[r] >> s & 1):
        domain = vertices(adj[u] & ~adj[r] & ~adj[s] & ~(1 << r) & ~(1 << s))
        if len(domain) < 9:
            raise RuntimeError('Counting identity failed')
        domain = domain[:9]
        small = clique(adj, domain, 4, True)
        if small is not None:
            return {'color': color, 'vertices': [u] + small}
        small = clique(adj, domain, 3, False)
        if small is not None:
            return {'color': 1 - color, 'vertices': [r, s] + small}
    else:
        domain = vertices(adj[r] & adj[s] & ~adj[u] & ~(1 << u))
        if len(domain) < 9:
            raise RuntimeError('Counting identity failed')
        domain = domain[:9]
        small = clique(adj, domain, 3, True)
        if small is not None:
            return {'color': color, 'vertices': [r, s] + small}
        small = clique(adj, domain, 4, False)
        if small is not None:
            return {'color': 1 - color, 'vertices': [u] + small}
    raise RuntimeError('Small Ramsey bound failed')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python3 -B extract.py graph.json')
    try:
        with open(sys.argv[1], encoding='utf-8') as stream:
            print(json.dumps(extract(json.load(stream)), sort_keys=True))
    except (ValueError, RuntimeError) as error:
        raise SystemExit(str(error))
