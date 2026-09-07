"""Exact proof-identity audits and physical controls; not a graph census."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys

from extract import extract, graph
from verify import verify

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rows(matrix):
    return [''.join(str(x) for x in row) for row in matrix]


def fixture(edge, fill, hub=23, anchor=22):
    # Labels 0=u, 1=r, 2=s; all three stars are explicitly fixed.
    matrix = [[0] * 43 for _ in range(43)]
    def put(i, j, c):
        matrix[i][j] = matrix[j][i] = c
    for i in range(3, 43):
        for j in range(3, i):
            put(i, j, ((i * 41 + j * 67 + i * j * 13) % 101) < 50)
    matrix = [[int(x) for x in row] for row in matrix]
    for v in range(1, hub + 1):
        put(0, v, 1)
    put(1, 2, edge)
    for v in range(3, 8 - edge):
        put(1, v, 1)
    for v in range(8, 13 - edge):
        put(2, v, 1)
    for v in range(hub + 1, hub + 1 + anchor - 6):
        put(1, v, 1)
    for v in range(43 - (anchor - 6), 43):
        put(2, v, 1)
    # Force each of the four small-Ramsey extraction routes.
    if edge:
        domain = [i for i in range(3, 43) if not matrix[0][i] and matrix[1][i] and matrix[2][i]][:9]
    else:
        domain = [i for i in range(3, 43) if matrix[0][i] and not matrix[1][i] and not matrix[2][i]][:9]
    for i, j in itertools.combinations(domain, 2):
        put(i, j, fill)
    return {'rows': rows(matrix), 'fork': [0, 1, 2], 'color': 1}


def transport(data, shift, color):
    permutation = [(v + shift) % 43 for v in range(43)]
    mat = [['0'] * 43 for _ in range(43)]
    for i in range(43):
        for j in range(i):
            bit = int(data['rows'][i][j]) ^ (1 - color)
            mat[permutation[i]][permutation[j]] = str(bit)
            mat[permutation[j]][permutation[i]] = str(bit)
    return {'rows': [''.join(r) for r in mat],
            'fork': [permutation[v] for v in data['fork']], 'color': color}


def small_ramsey():
    pairs = list(itertools.combinations(range(6), 2))
    triple_masks = [sum(1 << pairs.index(p) for p in itertools.combinations(t, 2))
                    for t in itertools.combinations(range(6), 3)]
    def bit_triangle(adj):
        for i in range(6):
            domain = adj[i] & ~((1 << (i + 1)) - 1)
            for j in range(i + 1, 6):
                if domain >> j & 1 and domain & adj[j]:
                    return True
        return False
    for mask in range(1 << 15):
        literal = any(mask & t in (0, t) for t in triple_masks)
        adj = [0] * 6
        for index, (i, j) in enumerate(pairs):
            if mask >> index & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
        opposite = [((1 << 6) - 1) ^ (1 << i) ^ a for i, a in enumerate(adj)]
        independent = bit_triangle(adj) or bit_triangle(opposite)
        require(literal and literal == independent, 'R(3,3) check failed')
    allowed34 = [d for d in range(9) if d <= 3 and 8 - d <= 5]
    require(allowed34 == [3] and (9 * allowed34[0]) % 2 == 1, 'R(3,4) parity failed')
    return {'k6_graphs_two_algorithms': 1 << 15, 'r34_forced_degrees': allowed34,
            'r34_degree_sum': 27}


def identities():
    # Independent dense-set reconstruction of all 8192 three-star words on
    # seven labeled vertices. Edges among the other four do not enter either identity.
    count = 0
    for e in (0, 1):
        for signatures in itertools.product(range(8), repeat=4):
            neighbors = [set() for _ in range(7)]
            def put(i, j):
                neighbors[i].add(j)
                neighbors[j].add(i)
            put(0, 1)
            put(0, 2)
            if e:
                put(1, 2)
            for v, signature in enumerate(signatures, 3):
                for anchor in range(3):
                    if signature >> anchor & 1:
                        put(v, anchor)
            d, a, b = [len(neighbors[i]) for i in range(3)]
            p = len(neighbors[0] & neighbors[1])
            q = len(neighbors[0] & neighbors[2])
            t = len(neighbors[0] & neighbors[1] & neighbors[2])
            n000 = len(set(range(3, 7)) - neighbors[0] - neighbors[1] - neighbors[2])
            red = len(neighbors[1] & neighbors[2])
            require(red == a + b + d - 7 - p - q + t + n000, 'Red identity failed')
            if e:
                outside = len((neighbors[1] & neighbors[2]) - neighbors[0] - {0})
                require(outside == a + b + d - 8 - p - q + n000, 'Outside identity failed')
            if not e:
                blue = len(neighbors[0] - neighbors[1] - neighbors[2] - {1, 2})
                require(blue == d - 2 - p - q + t, 'Blue identity failed')
            count += 1
    # Coefficient certificate: the per-external-vertex expressions agree on
    # every Boolean signature, so summing proves the identities at all orders.
    signature_rows = []
    for x, y, z in itertools.product((0, 1), repeat=3):
        blue = x * (1 - y) * (1 - z)
        red = x + y + z - x*y - x*z + x*y*z + (1-x)*(1-y)*(1-z) - 1
        require(blue == x - x*y - x*z + x*y*z and red == y*z, 'Coefficient failed')
        signature_rows.append([x, y, z, blue, red])
    return count, signature_rows


def rejection(call):
    try:
        call()
    except ValueError:
        return 1
    raise ValueError('A deliberately bad input was accepted')


def run():
    result = small_ramsey()
    count, signature_rows = identities()
    result.update({'star_identity_controls': count, 'signature_certificate': signature_rows})
    specs = [(d, a, e, f) for d in (21, 22, 23) for a in (21, 22) for e in (0, 1) for f in (0, 1)]
    specs += [(d, 22, 1, f) for d in (19, 20) for f in (0, 1)]
    bases = [fixture(e, f, d, a) for d, a, e, f in specs]
    routes = set()
    stream = hashlib.sha256()
    controls = 0
    for base, (hub, anchor, edge, fill) in zip(bases, specs):
        adj, (u, r, s), color = graph(base)
        require([adj[v].bit_count() for v in (u, r, s)] == [hub, anchor, anchor], 'Fixture degree')
        require([(adj[u] & adj[v]).bit_count() for v in (r, s)] == [5, 5], 'Fixture codegree')
        for shift in range(43):
            for color in (0, 1):
                data = transport(base, shift, color)
                cert = extract(data)
                verify(data, cert)
                routes.add((bool(adj[r] >> s & 1), cert['color'] == color))
                stream.update(json.dumps([data, cert], sort_keys=True, separators=(',', ':')).encode())
                controls += 1
        # Every one of the 780 edges outside the three anchor stars can
        # change independently without changing any family-defining count.
        for i, j in itertools.combinations(range(3, 43), 2):
            data = copy.deepcopy(base)
            matrix = [list(r) for r in data['rows']]
            matrix[i][j] = matrix[j][i] = str(1 - int(matrix[i][j]))
            data['rows'] = [''.join(row) for row in matrix]
            cert = extract(data)
            verify(data, cert)
            stream.update(json.dumps([data, cert], sort_keys=True, separators=(',', ':')).encode())
            controls += 1
    require(len(routes) == 4, 'Missing extraction route')
    bad = []
    base = fixture(0, 0)
    for key, value in [('rows', []), ('fork', [0, 0, 2]), ('fork', [0, 1, 43]),
                       ('fork', [0, True, 2]), ('color', True), ('color', 3)]:
        data = copy.deepcopy(base); data[key] = value; bad.append(data)
    data = copy.deepcopy(base); data['unexpected'] = 1; bad.append(data)
    for i, j, val, both in [(0, 0, '1', False), (4, 5, 'x', True), (4, 5, str(1-int(base['rows'][4][5])), False), (0, 1, '0', True)]:
        data = copy.deepcopy(base); matrix = [list(r) for r in data['rows']]
        matrix[i][j] = val
        if both: matrix[j][i] = val
        data['rows'] = [''.join(r) for r in matrix]; bad.append(data)
    # Weaken both anchors to degree 18: the red threshold is then 7,
    # so codegree sum 10 is outside the strict admission criterion.
    data = fixture(1, 0); matrix = [list(r) for r in data['rows']]
    for v in range(24, 28):
        matrix[1][v] = matrix[v][1] = '0'
    for v in range(27, 31):
        matrix[2][v] = matrix[v][2] = '0'
    data['rows'] = [''.join(r) for r in matrix]; bad.append(data)
    bad.extend([fixture(0, 0, 20, 22), fixture(1, 0, 18, 22)])
    rejected = sum(rejection(lambda data=data: extract(data)) for data in bad)
    cert = extract(base)
    corrupt = [dict(cert, color=1-cert['color']), dict(cert, color=True),
               dict(cert, vertices=[0]*5), dict(cert, vertices=[0, 1, 2, 3, 43]),
               dict(cert, vertices=cert['vertices'][:4]), dict(cert, unexpected=1)]
    bad_certs = sum(rejection(lambda c=c: verify(base, c)) for c in corrupt)
    result.update({'physical_controls': controls, 'relabel_color_controls': len(bases) * 86,
                   'free_pair_toggle_controls': len(bases) * 780, 'extraction_routes': len(routes),
                   'rejected_graphs': rejected, 'rejected_certificates': bad_certs,
                   'physical_stream_sha256': stream.hexdigest(),
                   'status': 'VERIFIED_SHARED_HUB_INJECTION_PACKAGE',
                   'ramsey_graph_found': False, 'bound_improved': False})
    return result, base, extract(base)


if __name__ == '__main__':
    result, fixture_data, cert = run()
    # Evidence generation is explicit; ordinary replay must match all fields.
    if sys.argv[1:] == ['--write-expected']:
        for name, data in [('expected.json', result), ('fixture.json', fixture_data), ('fixture_certificate.json', cert)]:
            (ROOT / name).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    elif sys.argv[1:]:
        raise SystemExit('usage: python3 -B reproduce.py')
    else:
        for name, data in [('expected.json', result), ('fixture.json', fixture_data), ('fixture_certificate.json', cert)]:
            require(json.loads((ROOT / name).read_text()) == data, 'Evidence mismatch: ' + name)
    print(json.dumps(result, indent=2, sort_keys=True))
