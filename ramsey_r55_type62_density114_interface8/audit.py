"""Independent physical reconstruction and exact input/support audit; no producer import."""
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

PINS = {'inputs.json': '8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2',
        'certificate.json': 'f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_inputs(directory):
    result = []
    for name, digest in PINS.items():
        raw = (Path(directory)/name).read_bytes()
        require(sha256(raw).hexdigest() == digest, 'upstream identity: '+name)
        result.append(json.loads(raw))
    return tuple(result)


def load_classification(directory):
    raw = (Path(directory)/'certificate.json').read_bytes()
    require(sha256(raw).hexdigest() == '39491fe6f15eb2ff887c0985cbbe50cced364a27047b7ead39427125f5b86cf8',
            'density-114 classification identity')
    return json.loads(raw)


def graph6(record):
    require(type(record) is str and record and all(63 <= ord(c) <= 126 for c in record),
            'graph6 characters')
    n = ord(record[0])-63
    bits = n*(n-1)//2
    require(n < 63 and len(record) == 1+(bits+5)//6, 'graph6 length')
    value = 0
    for c in record[1:]:
        value = (value << 6) | (ord(c)-63)
    padding = 6*(len(record)-1)-bits
    require(not value & ((1 << padding)-1), 'graph6 padding')
    value >>= padding
    edges = set()
    position = bits-1
    for v in range(n):
        for u in range(v):
            if value >> position & 1:
                edges.add((u, v))
            position -= 1
    return n, edges


def matrix(inputs, certificate, key):
    require(type(key) is tuple and len(key) == 4 and all(type(x) is int for x in key) and key[:2] == (8, 62)
            and type(key[2]) is int and 0 <= key[2] < len(certificate['family']['representatives'])
            and type(key[3]) is int and 0 <= key[3] < 2, 'cohort key')
    n, edges = graph6(inputs['interfaces'][8])
    require(n == 22 and len(edges) == 109, 'interface order/size')
    neighbors = [v for v in range(n) if (min(v, 21), max(v, 21)) in edges]
    marks = [q for q in permutations(neighbors)
             if all(((min(q[i], q[j]), max(q[i], q[j])) in edges)
                    == ((i,j) in {(0,2),(0,3),(0,4),(1,2),(1,3)}) for i, j in combinations(range(5), 2))]
    require(len(neighbors) == 5 and len(marks) == 2, 'all type62 markings')
    families = [certificate['family']]
    require(len(families) == 1 and families[0]['type'] == 62 and len(families[0]['representatives']) == 1697,
            'complete density-114 representatives')
    row = families[0]['representatives'][key[2]]['columns']
    require(len(row) == 5 and all(type(x) is int and 0 <= x < (1 << 17) for x in row)
            and sum(x.bit_count() for x in row) == 36, 'actual density-114 columns')
    a = [[2]*43 for _ in range(43)]

    def put(u, v, c):
        require(u != v and a[u][v] in (2, int(c)), 'conflicting physical pin')
        a[u][v] = a[v][u] = int(c)

    for u, v in combinations(range(22), 2):
        put(u, v, (u, v) in edges)
    for v in range(43):
        if v != 22:
            put(22, v, v < 22)
    for v in range(23, 43):
        put(21, v, v <= 39)
    residues = {v*v % 17 for v in range(1, 17)}
    for u, v in combinations(range(17), 2):
        put(u+23, v+23, (u-v) % 17 in residues)
    for s, vertex in enumerate(marks[key[3]]):
        for t in range(17):
            put(vertex, t+23, row[s] >> t & 1)
    raw = bytes(48+a[u][v] for u, v in combinations(range(43), 2))
    require(raw.count(b'2') == 389, 'full remaining interface')
    j_vertices = [22]+neighbors+list(range(23, 40))
    require(sum(a[u][v] for u, v in combinations(j_vertices, 2)) == 114,
            'physical hub density')
    return raw


def check_support(raw, variables, clauses):
    pairs = list(combinations(range(43), 2))
    expected = {e: i+1 for i, e in enumerate(e for e, c in zip(pairs, raw) if c == 50)}
    require(variables == expected and len(variables) == 389, 'all physical variables')
    active = {i for e, i in variables.items() if e[1] < 40}
    outside = set(variables.values())-active
    require(len(active) == 272 and len(outside) == 117, 'active/outside split')
    used = {abs(x) for row in clauses for x in row}
    require(used == active and not used & outside, 'kernel uses only and all A-to-T edges')
    require(all(e[0] in range(16) and 23 <= e[1] < 40
                for e, i in variables.items() if i in active), 'physical kernel support')
