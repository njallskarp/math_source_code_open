#!/usr/bin/env python3
"""Boundary, definition-level, physical-rule, and damaged-certificate controls."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import audit
import verify

BASE = Path(__file__).resolve().parent

def encode(n, code):
    bits = ''.join(str((code >> k) & 1) for k in range(n*(n-1)//2))
    bits += '0' * (-len(bits) % 6)
    return chr(n+63)+''.join(chr(int(bits[i:i+6], 2)+63) for i in range(0, len(bits), 6))

def must_reject(fn):
    try:
        fn()
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise RuntimeError('bad input was accepted')

def main():
    comparisons = 0
    for n in range(6):
        for code in range(1 << (n*(n-1)//2)):
            record = encode(n, code)
            matrix = audit.read_graph(record)
            adj = verify.decode(record)
            verify.require(adj == [sum((1 << j) for j in range(n) if matrix[i][j])
                                   for i in range(n)], 'decoder disagreement')
            for color in (True, False):
                rows = adj if color else verify.complement(adj)
                for size in range(n+2):
                    literal = any(all(matrix[i][j] == color for i, j in combinations(vs, 2))
                                  for vs in combinations(range(n), size))
                    verify.require(verify.clique(rows, (1 << n)-1, size) == literal,
                                   'clique definition mismatch')
                    comparisons += 1
    bad_records = ['', '!', '~~', '?@', 'A?', 'A@', 'B', 'A_', 'D~~~~']
    # A? is valid (two isolated vertices), so replace it with wrong length.
    bad_records[4] = 'A??'
    # A_ is a valid edge; nonzero padding makes A` invalid.
    bad_records[7] = 'A`'
    for record in bad_records:
        must_reject(lambda: verify.decode(record))
        must_reject(lambda: audit.read_graph(record))
    data = verify.load_certificate(BASE/'certificate.json')
    cases = verify.small_cases()
    all_solutions = [{code: set() for code in cases} for _ in range(2)]
    for rep in data['representatives']:
        c, code = rep['core'], rep['type']
        a = verify.decode(data['catalogue_records'][c])
        orbit = {verify.transform(rep['columns'], p, q)
                 for p in verify.automorphisms(a) for q in verify.automorphisms(cases[code])}
        all_solutions[c][code] |= orbit
    verify.check_certificate(data, all_solutions, cases)
    damaged = []
    d = deepcopy(data); d['representatives'].pop(); damaged.append(d)
    d = deepcopy(data); d['representatives'][0]['columns'][0] ^= 1; damaged.append(d)
    d = deepcopy(data); d['representatives'][0]['orbit'] += 1; damaged.append(d)
    d = deepcopy(data); d['representatives'][1] = deepcopy(d['representatives'][0]); damaged.append(d)
    d = deepcopy(data); d['cases'].pop(); damaged.append(d)
    d = deepcopy(data); d['cases'][0]['solutions'] += 1; damaged.append(d)
    d = deepcopy(data); d['cases'][0]['s_edges'].pop(); damaged.append(d)
    d = deepcopy(data); d['representatives'][0]['graph6'] += '?'; damaged.append(d)
    for d in damaged:
        must_reject(lambda: verify.check_certificate(d, all_solutions, cases))
    physical = 0
    for case in data['cases']:
        c, code = case['core'], case['type']
        adj = verify.decode(data['catalogue_records'][c])
        core = audit.read_graph(data['catalogue_records'][c])
        rules, _ = audit.physical_rules(core, case['s_edges'])
        points = [[0]*5, [65535]*5, [255]*5, [43690, 21845, 3855, 61680, 26214]]
        points += [r['columns'] for r in data['representatives'] if (r['core'], r['type']) == (c, code)]
        for columns in points:
            graph = verify.assemble(adj, cases[code], columns)
            matrix = [[bool(row & (1 << j)) for j in range(22)] for row in graph]
            residual_good = True
            for (red, which), supports in rules.items():
                common = 65535
                for j in which:
                    common &= columns[j] if red else 65535 ^ columns[j]
                if any(common & support == support for support in supports):
                    residual_good = False
                    break
            verify.require(residual_good == audit.good(matrix), 'physical-rule mismatch')
            physical += 1
    print(json.dumps({'clique_comparisons': comparisons, 'decoder_rejections': 2*len(bad_records),
                      'certificate_rejections': len(damaged), 'physical_assignments': physical},
                     sort_keys=True, separators=(',', ':')))

if __name__ == '__main__':
    main()
