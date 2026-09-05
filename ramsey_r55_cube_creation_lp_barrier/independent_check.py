#!/usr/bin/env python3
"""Separate exact checker: rooted clauses, seed clique recursion, cell products.

Does not import verify.py, use a solver, or enumerate all vertex five-sets.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    seed_bytes = (ROOT/'SEED.json').read_bytes()
    seed_hash = sha256(seed_bytes).hexdigest()
    check(seed_hash == '9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916', 'seed hash')
    raw = json.loads(seed_bytes)['red_adjacency_hex']
    adj = [{v for v,bit in enumerate(bin(int(row,16))[2:][::-1]) if bit == '1'} for row in raw]
    check(len(adj) == 43, 'order')
    check(all(u not in adj[u] and adj[u] <= set(range(43)) for u in range(43)), 'loops/range')
    check(all((v in adj[u]) == (u in adj[v]) for u,v in combinations(range(43),2)), 'symmetry')
    p = json.loads((ROOT/'primal.json').read_text())
    check(p['seed_sha256'] == seed_hash, 'point seed')
    check(p['format'] == 'r55-cube-creation-rational-primal-v1', 'format')
    check(p['edge_order'] == 'lexicographic central pairs 3..42', 'order convention')
    D, nums = p['denominator'], p['numerators']
    check(type(D) is int and D > 0 and len(nums) == 780, 'point dimensions')
    check(all(type(n) is int and 0 <= n <= D for n in nums), 'boxes')
    x = {frozenset((u,v)):n for (u,v),n in zip(combinations(range(3,43),2),nums)}
    E, C = set(range(3)), set(range(3,43))
    for u in range(43):
        check(len(adj[u]) == (20 if u in E else 21), 'seed degrees')
        change = sum((1-2*int(v in adj[u]))*x.get(frozenset((u,v)),0) for v in range(43) if v != u)
        check(change == 0, 'degree conservation')
    for u in E:
        for color in (0,1):
            side = adj[u] if color else set(range(43)) - adj[u] - {u}
            count = sum(int(v in adj[w]) == color for v,w in combinations(side,2))
            check(count == (92 if color else 107), 'seed profile')
            change = sum((1-2*int((v in adj[w]) == color))*x.get(frozenset((v,w)),0) for v,w in combinations(side,2))
            check(change == 0, 'profile conservation')

    def opposite(q, color):
        """D times the expected number of edges opposite to color."""
        value = 0
        for u,v in combinations(q,2):
            old_same = int((v in adj[u]) == color)
            n = x.get(frozenset((u,v)),0)
            value += (1-old_same)*D + (2*old_same-1)*n
        return value

    rooted = 0
    for a in (1,2,3):
        for anchors in combinations(sorted(E),a):
            for central in combinations(sorted(C),5-a):
                q = anchors+central
                fixed = [(u,v) for u,v in combinations(q,2) if u in E or v in E]
                for color in (0,1):
                    if all(int(v in adj[u]) == color for u,v in fixed):
                        check(opposite(q,color) >= D, 'rooted row')
                        rooted += 1
    check(rooted == 31153, 'rooted coverage')

    def cliques(prefix, candidates, neighborhoods):
        if len(prefix) == 5:
            yield prefix
            return
        remaining = set(candidates)
        while remaining:
            v = min(remaining)
            remaining.remove(v)
            yield from cliques(prefix+(v,),remaining & neighborhoods[v],neighborhoods)

    old_counts = []
    for color in (0,1):
        neighborhoods = {v:(adj[v] & C if color else C-adj[v]-{v}) for v in C}
        count = 0
        for q in cliques((),C,neighborhoods):
            check(opposite(q,color) >= D, 'old destruction')
            count += 1
        old_counts.append(count)
    check(old_counts == [177,176], 'old clique counts')

    sig = {v:sum(1 << a for a in E if a in adj[v]) for v in C}
    cells = {s:sorted(v for v in C if sig[v] == s) for s in range(8)}
    check([len(cells[s]) for s in range(8)] == [0,8,8,6,10,4,4,0], 'cell sizes')
    # With only six proper signatures, a complement-free mixed support must
    # pick one from each antipodal pair; the two qualifying triples are these.
    supports = {s for s in combinations(range(1,7),3)
                if all(a^b != 7 for a,b in combinations(s,2))
                and all({a >> i & 1 for a in s} == {0,1} for i in range(3))}
    check(supports == {(1,2,4),(3,5,6)}, 'proper mixed supports')
    table = {}
    holes = Counter()
    for support in sorted(supports):
        for sizes in product(range(1,4),repeat=3):
            if sum(sizes) != 5:
                continue
            groups = [list(combinations(cells[s],k)) for s,k in zip(support,sizes)]
            for selected in product(*groups):
                q = tuple(sorted(v for group in selected for v in group))
                check(q not in table, 'cube duplicate')
                blue_total = opposite(q,1)
                red_total = opposite(q,0)
                check(blue_total >= D and red_total >= D, 'cube two-sided clauses')
                check(blue_total+red_total == 10*D, 'color complement')
                table[q] = red_total
                original = sum(v in adj[u] for u,v in combinations(q,2))
                holes[original] += 1
                holes[10-original] += 1
    check(len(table) == 46088 and holes[1] == 730, 'cube coverage')
    digest = sha256()
    for q,total in sorted(table.items()):
        digest.update((','.join(map(str,q))+':'+str(total)+'\n').encode())

    visible = {e for e in x if (sig[min(e)] ^ sig[max(e)]) != 7}
    check(len(visible) == 656, 'visible edges')
    V = sum(x[e] for e in visible)
    check(38*D < V < 39*D, 'strict visible budget')
    q = (3,10,25,28,36)
    check(p['missing_local_clause'] == {'color':1,'five':list(q),'blue_anchor':1,'hole':[25,28]}, 'witness metadata')
    pairs = list(combinations(q,2))
    absent = [e for e in pairs if e[1] not in adj[e[0]]]
    check(absent == [(25,28)], 'unique blue hole')
    check(all(v not in adj[1] for v in q), 'blue neighborhood')
    check(all(frozenset(e) in visible for e in pairs) and q not in table, 'visible but not mixed')
    delta = x[frozenset(absent[0])] - sum(x[frozenset(e)] for e in pairs if e != absent[0])
    check(delta > 0 and opposite(q,1) == D-delta, 'violated local row')
    for bits in product((0,1),repeat=10):
        final = [int(v in adj[u]) ^ bit for (u,v),bit in zip(pairs,bits)]
        lhs = bits[pairs.index(absent[0])] - sum(bit for e,bit in zip(pairs,bits) if e != absent[0])
        check((lhs <= 0) == (not all(final)), 'one-hole Boolean equivalence')
    return {
        'status':'SEPARATE EXACT ENUMERATION VERIFIED',
        'old_blue_red_cliques':old_counts,'root_colored_rows':rooted,
        'cube_five_sets':len(table),'cube_evaluation_sha256':digest.hexdigest(),
        'visible_edges':len(visible),'visible_edit_value':str(Fraction(V,D)),
        'missing_local_clause_violation':str(Fraction(delta,D)),
        'one_hole_truth_table_cases':1024,
    }


if __name__ == '__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
