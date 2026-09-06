#!/usr/bin/env python3
"""Exact finite marked-density proof. Standard library; no solver."""
import base64
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(obj):
    return sha256((json.dumps(obj, separators=(',', ':')) + '\n').encode()).hexdigest()


def mask(vertices):
    return sum(1 << v for v in vertices)


def avoids(s, forbidden):
    return not any(s & q == q for q in forbidden)


def edges_doc(doc, n):
    require(type(doc) is dict and set(doc) == {'n', 'red_edges'}, 'graph schema')
    require(type(doc['n']) is int and doc['n'] == n, 'graph order')
    require(type(doc['red_edges']) is list, 'edge list')
    edges = set()
    for pair in doc['red_edges']:
        require(type(pair) is list and len(pair) == 2
                and all(type(v) is int for v in pair), 'edge type')
        u, v = pair
        require(0 <= u < v < n and (u, v) not in edges, 'simple ordered edge')
        edges.add((u, v))
    return edges


def source_edges(doc):
    require(type(doc['n']) is int and doc['n'] == 22, 'source order')
    raw = base64.b64decode(doc['red_parent_graph6_base64'], validate=True)
    require(len(raw) == 40 and raw[0] == 85
            and all(63 <= c <= 126 for c in raw), 'graph6 shape')
    bits = ''.join(format(c - 63, '06b') for c in raw[1:])
    require(bits[231:] == '000', 'graph6 padding')
    edges = {e for e, b in zip(((u, v) for v in range(1, 22) for u in range(v)), bits)
             if b == '1'}
    require(len(edges) == 114, 'parent edge count')
    require(len(doc['red_deletions']) == 6, 'six deletions')
    for pair in doc['red_deletions']:
        require(type(pair) is list and len(pair) == 2
                and all(type(v) is int for v in pair), 'deletion type')
        e = tuple(pair)
        require(e in edges, 'missing/repeated deletion')
        edges.remove(e)
    require(len(edges) == 108, 'source edge count')
    return edges


def cliques(edges, vertices, k, color=True):
    return [list(q) for q in combinations(vertices, k)
            if all((e in edges) == color for e in combinations(q, 2))]


def compute(source, hdoc):
    h = edges_doc(hdoc, 20)
    require(len(h) == 92 and not cliques(h, range(20), 4)
            and not cliques(h, range(20), 5, False), 'H20 local Ramsey graph')
    neighbors = lambda v: {u for u in range(20) if tuple(sorted((u, v))) in h}
    require(neighbors(0) == {1, 10, 11, 12, 13, 14, 15}
            and neighbors(1) == {0, 16, 17, 18, 19}, 'marked neighborhoods')
    side = sorted(neighbors(1))
    require(cliques(h, side, 2) == [[16, 17], [16, 19], [17, 18], [18, 19]],
            'isolated marked vertex and C4')
    original = source_edges(source)
    require(not cliques(original, range(22), 4)
            and not cliques(original, range(22), 5, False), 'R2 literal core')
    base = set(combinations(range(22), 2)) - original
    forbidden4 = [mask(q) for q in cliques(base, range(22), 4)]
    domains = [list(q) for q in combinations(range(22), 14)
               if avoids(mask(q), forbidden4)]
    require(len(domains) == 6, 'complete base fourteen-domains')
    records = []
    for vertices in domains:
        tri = [mask(q) for q in cliques(base, vertices, 3)]
        require(all(not avoids(mask(q), tri) for q in combinations(vertices, 9)),
                'triangle-free capacity at most eight')
        states8 = [list(q) for q in combinations(vertices, 8) if avoids(mask(q), tri)]
        require(states8, 'capacity-eight witness')
        obstruction = cliques(base, sorted(set(range(22)) - set(vertices)), 4)
        records.append({'vertices': vertices, 'red_edges': len(cliques(base, vertices, 2)),
                        'maximum_triangle_free_size': 8, 'capacity_witness': states8[0],
                        'complement_red_K4': obstruction[0] if obstruction else None})
    require([i for i, r in enumerate(records) if r['complement_red_K4']] == [3],
            'unique complement obstruction')
    require(records[3]['complement_red_K4'] == [8, 11, 16, 18]
            and records[3]['red_edges'] == 47, 'high-density obstruction')
    require(max(r['red_edges'] for r in records if not r['complement_red_K4']) == 45,
            'remaining base density bound')
    family = []
    failed = []
    for e in sorted(original):
        child = base | {e}
        bad5 = cliques(child, range(22), 5)
        if bad5:
            failed.append([list(e), bad5[0]])
            continue
        cases = []
        for i, vertices in enumerate(domains):
            if cliques(child, vertices, 4) or records[i]['complement_red_K4']:
                continue
            ec = len(cliques(child, vertices, 2))
            bound = 5 + 4 + 4 + ec + 4 * 8
            require(ec <= 46 and bound <= 91, 'strict marked-density cut')
            cases.append([i, ec, bound])
        require(cases, 'nonempty relaxed domain')
        family.append({'added_red_edge': list(e), 'cases': cases,
                       'marked_density_upper_bound': max(c[-1] for c in cases)})
    require(len(family) == 16 and len(failed) == 92, 'complete existing deletion family')
    return {'status': 'ALL SIXTEEN O22 MARKED GLUINGS EXCLUDED',
            'H20_red_edges': len(h), 'base_O22_red_edges': len(base),
            'base_fourteen_domains': records, 'candidate_family': family,
            'invalid_deletions': len(failed),
            'invalid_deletion_witnesses_sha256': digest(failed),
            'density_identity_constant': 13, 'four_attachment_capacity': 32,
            'universal_marked_density_upper_bound': 91, 'required_marked_density': 92}


def verify(certificate, source=None, hdoc=None):
    if source is None:
        source = json.loads((ROOT / 'SOURCE.json').read_text())
    if hdoc is None:
        hdoc = json.loads((ROOT / 'H20.json').read_text())
    actual = compute(source, hdoc)
    require(json.dumps(certificate, sort_keys=True, separators=(',', ':'))
            == json.dumps(actual, sort_keys=True, separators=(',', ':')), 'certificate mismatch')
    return actual


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--derive']:
        result = compute(json.loads((ROOT / 'SOURCE.json').read_text()),
                         json.loads((ROOT / 'H20.json').read_text()))
        print(json.dumps(result, sort_keys=True, indent=2))
    else:
        require(not sys.argv[1:], 'usage: verify.py [--derive]')
        result = verify(json.loads((ROOT / 'CERTIFICATE.json').read_text()))
        print('VERIFIED: 16 fixed O22 choices excluded; marked density <= 91 < 92')
        print('certificate_sha256=' + sha256((ROOT / 'CERTIFICATE.json').read_bytes()).hexdigest())
