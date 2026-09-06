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


def validate_consensus(inputs, consensus):
    require(consensus['interfaces'] == [1, 2], 'covered interfaces')
    p = consensus['second_to_first']
    require(len(p) == 22 and all(type(x) is int for x in p)
            and sorted(p) == list(range(22)), 'relabeling bijection')
    require(set(p[:16]) == set(range(16)) and set(p[16:21]) == set(range(16, 21))
            and p[21] == 21, 'relabeling preserves distinguished cells')
    n, first = graph6(inputs['interfaces'][1])
    m, second = graph6(inputs['interfaces'][2])
    require(n == m == 22 and len(first) == len(second) == 109, 'original interfaces')
    moved = {tuple(sorted((p[u], p[v]))) for u, v in second}
    difference = sorted(first ^ moved)
    require(difference == [tuple(e) for e in consensus['free_common_edges']]
            and len(difference) == 20, 'exact twenty disagreements')
    require(all(u < 16 and 16 <= v < 21 for u, v in difference),
            'only common-neighborhood attachments may disagree')
    return first, moved


def markings(edges):
    s = [v for v in range(21) if (v, 21) in edges]
    require(s == list(range(16, 21)), 'common-neighborhood identity')
    result = [q for q in permutations(s)
              if all((tuple(sorted((q[i], q[j]))) in edges) == (i < 2 <= j)
                     for i, j in combinations(range(5), 2))]
    require(len(result) == 12, 'all twelve literal markings')
    return result


def build_matrix(edges, certificate, key, other=None):
    require(type(key) is tuple and len(key) == 2 and all(type(x) is int for x in key)
            and 0 <= key[0] < 29 and 0 <= key[1] < 12, 'complete cohort key')
    family = [f for f in certificate['families'] if f['type'] == 126]
    require(len(family) == 1 and len(family[0]['representatives']) == 29, 'complete local catalogue')
    row = family[0]['representatives'][key[0]]['columns']
    require(len(row) == 5 and all(type(x) is int and 0 <= x < (1 << 17) for x in row)
            and sum(x.bit_count() for x in row) == 37, 'actual equality columns')
    mark = markings(edges)[key[1]]
    a = [[2]*43 for _ in range(43)]

    def put(u, v, c):
        require(u != v and a[u][v] in (2, int(c)), 'conflicting physical pin')
        a[u][v] = a[v][u] = int(c)

    for u, v in combinations(range(22), 2):
        if other is None or ((u, v) in edges) == ((u, v) in other):
            put(u, v, (u, v) in edges)
    for v in range(43):
        if v != 22:
            put(22, v, v < 22)
    for v in range(23, 43):
        put(21, v, v < 40)
    squares = {x*x % 17 for x in range(1, 17)}
    for u, v in combinations(range(17), 2):
        put(u+23, v+23, (u-v) % 17 in squares)
    for s, vertex in enumerate(mark):
        for t in range(17):
            put(vertex, t+23, row[s] >> t & 1)
    raw = bytes(48+a[u][v] for u, v in combinations(range(43), 2))
    require(raw.count(b'2') == (389 if other is None else 409), 'physical free-edge count')
    require(sum(a[u][v] for u, v in combinations([22]+list(range(16, 21))
                                               +list(range(23, 40)), 2)) == 116,
            'physical neighborhood equality density')
    return raw


def matrix(inputs, certificate, consensus, key):
    first, second = validate_consensus(inputs, consensus)
    return build_matrix(first, certificate, key, second)


def check_support(raw, variables, clauses, consensus):
    pairs = list(combinations(range(43), 2))
    expected = {e: i+1 for i, e in enumerate(e for e, c in zip(pairs, raw) if c == 50)}
    require(variables == expected and len(variables) == 409, 'all physical variables')
    active = {i for e, i in variables.items() if e[1] < 40}
    outside = set(variables.values())-active
    expected_pairs = {(u, v) for u in range(16) for v in range(23, 40)}
    expected_pairs |= {tuple(e) for e in consensus['free_common_edges']}
    require({e for e, i in variables.items() if i in active} == expected_pairs,
            'all twenty attachment bits and 272 private-core bits')
    require(len(active) == 292 and len(outside) == 117, 'active/outside split')
    used = {abs(x) for c in clauses for x in c}
    require(used == active and not used & outside, 'exact necessary-kernel support')


def coverage(inputs, certificate, consensus):
    first, _ = validate_consensus(inputs, consensus)
    target_marks = markings(first)
    pairs = list(combinations(range(43), 2))
    index = {e: i for i, e in enumerate(pairs)}
    targets = {(j, k): matrix(inputs, certificate, consensus, (j, k))
               for j in range(29) for k in range(12)}
    require(len(set(targets.values())) == 348, 'distinct consensus templates')
    multiplicity = {key: 0 for key in targets}
    checks = 0
    digest = sha256()
    for key, raw in targets.items():
        digest.update((' '.join(map(str, key))+'\n').encode())
        digest.update(bytes(c-48 for c in raw))
    for h in (1, 2):
        _, edges = graph6(inputs['interfaces'][h])
        p = list(range(43)) if h == 1 else consensus['second_to_first']+list(range(22, 43))
        edge_map = [index[tuple(sorted((p[u], p[v])))] for u, v in pairs]
        seen_marks = set()
        for k, mark in enumerate(markings(edges)):
            target_k = target_marks.index(tuple(p[v] for v in mark))
            seen_marks.add(target_k)
            for j in range(29):
                original = build_matrix(edges, certificate, (j, k))
                target = targets[j, target_k]
                for i, to in enumerate(edge_map):
                    require(target[to] == 50 or target[to] == original[i],
                            'target fixed color is not implied by transported original')
                    if original[i] == 50:
                        require(target[to] == 50, 'a formerly free edge was pinned')
                    checks += 1
                multiplicity[j, target_k] += 1
        require(seen_marks == set(range(12)), 'complete marking permutation')
    require(set(multiplicity.values()) == {2}, 'two complete original cohorts covered')
    return {'covered_original_keys': 696, 'consensus_keys': 348,
            'original_keys_per_consensus_key': 2, 'physical_edge_transports': checks,
            'marked_template_sha256': digest.hexdigest()}
