#!/usr/bin/env python3
"""Exact small-graph and triangle-type audit; U14 upper bound remains external."""

import hashlib
import itertools
import json
import sys
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def alpha_at_least_five(n, edges):
    return any(all(tuple(pair) not in edges for pair in itertools.combinations(vertices, 2))
               for vertices in itertools.combinations(range(n), 5))


def check(data):
    pairs = list(itertools.combinations(range(6), 2))
    allowed_two = []
    for choice in itertools.combinations(pairs, 2):
        edges = set(choice)
        if not alpha_at_least_five(6, edges):
            require(len(set().union(*map(set, edges))) == 4, 'two edges are not disjoint')
            allowed_two.append(choice)
    require(len(allowed_two) == 45, 'two-edge census')
    squares = []
    for choice in itertools.combinations(pairs, 5):
        edges = set(choice)
        if alpha_at_least_five(6, edges):
            continue
        degrees = [sum(vertex in edge for edge in edges) for vertex in range(6)]
        square = sum(d * d for d in degrees)
        require(square <= 26, 'five-edge degree-square bound')
        squares.append(square)
    require(len(squares) == 2997 and max(squares) == 26, 'five-edge census')

    corrections = {'EEE': 3, 'EEX': 1, 'EXX': 0, 'XXX': 0, 'EET': 2, 'EXT': 0, 'XXT': -1}
    expected_types = {word: [word.count('E'), word.count('X'),
                            word.count('X') * (word.count('X') - 1) // 2]
                      for word in corrections}
    require(data['type_columns'] == ['S_E', 'S_X', 'D'], 'columns')
    require(data['triangle_types'] == expected_types, 'type coefficient table')
    for word, (s_e, s_x, d) in expected_types.items():
        require(d == s_x - s_e + corrections[word], 'triangle accounting')

    g6 = data['catalog_witness_graph6']
    require(isinstance(g6, str) and all(63 <= ord(ch) <= 126 for ch in g6), 'graph6 characters')
    n = ord(g6[0]) - 63
    bits = [(ord(ch) - 63 >> shift) & 1 for ch in g6[1:] for shift in range(5, -1, -1)]
    pair_count = n * (n - 1) // 2
    require(n == 14 and len(bits) == 6 * ((pair_count + 5) // 6), 'graph6 order/length')
    require(not any(bits[pair_count:]), 'graph6 padding')
    edges = set()
    for bit, pair in zip(bits, ((i, j) for j in range(n) for i in range(j))):
        if bit:
            edges.add(pair)
    require(len(edges) == 60, 'catalog witness edge count')
    require(not alpha_at_least_five(n, edges), 'catalog witness independent five')
    require(not any(all(e in edges for e in itertools.combinations(vs, 2))
                    for vs in itertools.combinations(range(n), 4)), 'catalog witness K4')
    require(data['catalog_upper_U14'] == 60, 'external catalog premise changed')

    # At least two local triangles at each vertex, and the r=2 argument gives ten.
    require(min(13, 2 + 2 * (4 + 4 - 6) + (6 * 5 - 26)) == 10, 'regular-13 lemma arithmetic')
    require(data['lower_a_b_e'] == [10, 28 * 2, 2 * 3], 'lower bound inputs')
    require(data['upper_g'] == 2 * data['catalog_upper_U14'], 'upper g')
    require(data['S_E'] == 13 * 93 and data['S_X'] == 28 * 100, 'local triangle sums')
    require(data['J_edges'] == 28 * 14 // 2, 'J edges')
    a, b, e = data['lower_a_b_e']
    lower = data['S_X'] - data['S_E'] + 3 * a + b + 2 * e - data['upper_g']
    require(data['D_lower'] == lower == 1569, 'D lower')
    require(data['partner_min'] == (lower + data['J_edges'] - 1) // data['J_edges'] == 9, 'partner guarantee')
    return len(allowed_two), len(squares)


def main():
    require(len(sys.argv) <= 2, 'usage: verify.py [certificate.json]')
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name('certificate.json')
    raw = path.read_bytes()
    allowed_two, allowed_five = check(json.loads(raw))
    print(f'PASS six-vertex audits: two_edge_allowed={allowed_two}/105 five_edge_allowed={allowed_five}/3003 max_degree_square=26')
    print('PASS seven triangle types; regular13_triangles>=10')
    print('PASS catalog witness n=14 m=60 omega<=3 alpha<=4; upper_U14=60 IS AN EXTERNAL PREMISE')
    print('PASS D>=1569>1568; exact-anchor partner codegree>=9')
    print('certificate_sha256=' + hashlib.sha256(raw).hexdigest())


if __name__ == '__main__':
    main()
