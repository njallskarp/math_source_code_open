#!/usr/bin/env python3
"""Exact rational primal verification; no solver or external module."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED_SHA = '9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(seed_bytes, point):
    require(sha256(seed_bytes).hexdigest() == SEED_SHA, 'seed identity')
    seed = json.loads(seed_bytes)
    r = [int(s,16) for s in seed['red_adjacency_hex']]
    require(len(r) == 43 and all(0 <= row < 1 << 43 for row in r), 'seed range')
    require(all(not (r[u] >> u & 1) for u in range(43)), 'seed diagonal')
    require(all((r[u] >> v & 1) == (r[v] >> u & 1) for u,v in combinations(range(43),2)), 'seed symmetry')
    edges = list(combinations(range(3,43),2))
    fields = {'seed_sha256','format','edge_order','denominator','numerators','missing_local_clause'}
    require(type(point) is dict and set(point) == fields, 'point fields')
    require(point['format'] == 'r55-cube-creation-rational-primal-v1', 'point format')
    require(point['seed_sha256'] == SEED_SHA, 'point seed')
    require(point['edge_order'] == 'lexicographic central pairs 3..42', 'edge order')
    D = point['denominator']
    nums = point['numerators']
    require(type(D) is int and D > 0, 'denominator')
    require(type(nums) is list and len(nums) == 780 and all(type(n) is int and 0 <= n <= D for n in nums), 'point boxes')
    z = dict(zip(edges,nums))
    old = {(u,v):r[u] >> v & 1 for u,v in combinations(range(43),2)}
    final = {e:D*c+(1-2*c)*z.get(e,0) for e,c in old.items()}
    degree_rows = 0
    profile_rows = 0
    for u in range(43):
        expected = 20 if u < 3 else 21
        require(r[u].bit_count() == expected, 'seed degree')
        require(sum(final[min(u,v),max(u,v)] for v in range(43) if v != u) == D*expected, 'degree equality')
        degree_rows += int(u >= 3)
    for u in range(3):
        for color in (0,1):
            side = [v for v in range(43) if v != u and (r[u] >> v & 1) == color]
            expected = 92 if color else 107
            original_same = sum(old[e] == color for e in combinations(side,2))
            require(original_same == expected, 'seed profile')
            final_same = sum(final[e] if color else D-final[e] for e in combinations(side,2))
            require(final_same == D*expected, 'profile equality')
            profile_rows += 1

    signatures = [row & 7 for row in r]
    require([signatures[3:].count(s) for s in range(8)] == [0,8,8,6,10,4,4,0], 'signature sizes')
    mixed_patterns = set()
    for pat in combinations_with_replacement(range(8),5):
        if (all(len({s >> i & 1 for s in pat}) == 2 for i in range(3))
                and all(a ^ b != 7 for a,b in combinations(pat,2))):
            mixed_patterns.add(pat)
    require(len(mixed_patterns) == 88, 'full cube patterns')
    counts = Counter()
    root_rows = set()
    cube_hole_counts = Counter()
    full_violations = Counter()
    audit_hash = sha256()
    for five in combinations(range(43),5):
        pairs = list(combinations(five,2))
        original = sum(old[e] for e in pairs)
        total = sum(final[e] for e in pairs)
        if five[0] < 3:
            counts['root_five_sets'] += 1
            require(0 < original < 10, 'seed root K5')
            require(D <= total <= 9*D, 'root clause')
            for color in (0,1):
                if all(old[e] == color for e in pairs if e[0] < 3):
                    root_rows.add((color,five))
            continue
        if original in (0,10):
            counts['old_cliques'] += 1
            require((total >= D) if original == 0 else (total <= 9*D), 'old destruction clause')
        pat = tuple(sorted(signatures[v] for v in five))
        if pat in mixed_patterns:
            counts['cube_five_sets'] += 1
            require(D <= total <= 9*D, 'complete mixed cube clause')
            for color in (0,1):
                holes = 10-original if color else original
                cube_hole_counts[holes] += 1
            audit_hash.update((','.join(map(str,five))+':'+str(total)+'\n').encode())
        if total < D or total > 9*D:
            color = int(total > 9*D)
            holes = 10-original if color else original
            visible = all(signatures[u] ^ signatures[v] != 7 for u,v in pairs)
            full_violations['local-visible' if visible else 'uses-invisible'] += 1
            require(holes >= 1, 'zero-hole violation contradicts old coverage')

    require(counts == {'root_five_sets':304590,'old_cliques':353,'cube_five_sets':46088}, 'complete counts')
    require(len(root_rows) == 31153 and cube_hole_counts[1] == 730, 'root/one-hole coverage')
    V = sum(z[e] for e in edges if signatures[e[0]] ^ signatures[e[1]] != 7)
    require(38*D < V < 39*D, 'visible budget interval')

    witness = point['missing_local_clause']
    require(witness == {'color':1,'five':[3,10,25,28,36],'blue_anchor':1,'hole':[25,28]}, 'local witness metadata')
    five = witness['five']
    pairs = list(combinations(five,2))
    hole = tuple(witness['hole'])
    require([e for e in pairs if not old[e]] == [hole], 'one-hole origin')
    require(all(not (r[1] >> v & 1) for v in five), 'opposite-color neighborhood')
    require(all(signatures[u] ^ signatures[v] != 7 for u,v in pairs), 'witness visible')
    require(tuple(sorted(signatures[v] for v in five)) not in mixed_patterns, 'witness omitted from cube')
    violation = z[hole] - sum(z[e] for e in pairs if e != hole)
    require(violation > 0, 'missing clause violation')
    return {
        'status':'EXACT CUBE-CREATION LP BARRIER VERIFIED',
        'degree_equations':degree_rows,'profile_equations':profile_rows,
        **dict(counts),'root_colored_rows':len(root_rows),
        'cube_one_sided_rows':2*counts['cube_five_sets'],'cube_one_hole_rows':cube_hole_counts[1],
        'visible_edit_value':str(Fraction(V,D)),
        'missing_local_clause_violation':str(Fraction(violation,D)),
        'minimum_omitted_violated_hole_count':1,
        'remaining_global_linear_violations':dict(full_violations),
        'cube_evaluation_sha256':audit_hash.hexdigest(),
        'fractional_variables':sum(0<n<D for n in nums),
    }


if __name__ == '__main__':
    result = verify((ROOT/'SEED.json').read_bytes(),json.loads((ROOT/'primal.json').read_text()))
    print(json.dumps(result,sort_keys=True,indent=2))
