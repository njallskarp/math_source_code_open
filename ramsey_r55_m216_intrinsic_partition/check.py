"""Check complete sets, intrinsic transports, and definition-level controls."""
from itertools import combinations, permutations, product
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys
import derive

HERE = Path(__file__).resolve().parent

def require(ok, why):
    if not ok:
        raise ValueError(why)

def check_document(d, literal):
    require(d == derive.produce(), 'certificate differs from regeneration')
    pairs = tuple(combinations(range(7), 2))
    def image(mask, p):
        edges = {tuple(sorted((p[u], p[v]))) for i, (u, v) in enumerate(pairs) if mask >> i & 1}
        return sum(1 << i for i, uv in enumerate(pairs) if uv in edges)
    group = [list(z)+list(e) for z in permutations(range(2)) for e in permutations(range(2, 7))]
    expanded = set(); per_core = {}
    transported = 0
    for c in d['cores']:
        orbit = {image(c['mask'], p) for p in group}
        require(min(orbit) == c['mask'], 'canonical representative')
        require(len(orbit) == c['orbit_size'] and not expanded&orbit, 'orbit cardinality or overlap')
        expanded |= orbit
        per_core[c['mask']] = orbit
        for p in group:
            source = derive.decode(c['mask'])
            target = derive.decode(image(c['mask'], p))
            for u, v in pairs:
                require((v in source[u]) == (p[v] in target[p[u]]), 'core bit transport')
                transported += 1
    require(sorted(expanded) == literal, 'independent complete labeled streams differ')
    require(expanded == derive.structured_census(), 'structured census differs')
    blue = {mask for mask in expanded if not mask & 1}
    require(blue == per_core[4094] and len(blue) == 10, 'closed blue-pair branch')
    parent_transport = min((image(901619,p),p) for p in group)
    require(parent_transport[0] == 380277, 'h2731 core transport')
    branch_hist = Counter()
    full_bits = placements = 0
    for root in d['roots']:
        core = next(c for c in d['cores'] if c['mask'] == root['core_mask'])
        defects = dict(root['central_red_excess'])
        require(sum(defects.values()) == core['central_red_excess'], 'central defect total')
        s = core['exceptional_red_excess']+[defects.get(v, 0) for v in range(7, 43)]
        r = [85,85]+[93]*5+[100]*36
        b = [115,115]+[107]*5+[100]*36
        require(sum(s) == 2 and (sum(r)-sum(s)) % 3 == sum(b) % 3 == 0, 'triangle divisibility')
        branch_hist[core['central_red_excess']] += 1
        # Arbitrary outside bits test the physical bijection, not feasibility.
        full = {(u,v): bool(((u+3)*(v+5)+root['index']) % 7 < 3)
                for u,v in combinations(range(43), 2)}
        for bit, uv in enumerate(pairs):
            full[uv] = bool(core['mask'] >> bit & 1)
        for support in combinations(range(7,43), len(defects)):
            source_defects = dict(zip(support, defects.values()))
            order = list(support)+[v for v in range(7,43) if v not in source_defects]
            p = list(range(43))
            for target, source in enumerate(order, 7):
                p[source] = target
            require(sorted(p) == list(range(43)), 'nonbijective physical relabeling')
            require({p[v]: value for v,value in source_defects.items()} == defects, 'defect transport')
            moved = {tuple(sorted((p[u],p[v]))): color for (u,v),color in full.items()}
            for uv,color in full.items():
                require(moved[tuple(sorted((p[uv[0]],p[uv[1]])))] == color, 'full edge transport')
                full_bits += 1
            placements += 1
    return {'necessary_labeled_cores': len(expanded), 'necessary_core_orbits': len(d['cores']),
            'closed_labeled_blue_pair_cores': len(blue), 'remaining_core_orbits': len(d['cores'])-1,
            'complete_marked_roots': len(d['roots']), 'roots_by_central_excess': dict(sorted(branch_hist.items())),
            'core_transport_pairs': transported, 'full_transport_pairs': full_bits,
            'all_labeled_central_defect_placements': placements,
            'h2731_canonical_core': parent_transport[0], 'h2731_transport': parent_transport[1],
            'labeled_stream_sha256': hashlib.sha256(''.join(f'{m}\n' for m in literal).encode()).hexdigest()}

def controls():
    # R(3,3)<=6 by complete literal six-vertex coloring enumeration.
    e6 = tuple(combinations(range(6), 2))
    triples = [tuple(e6.index(uv) for uv in combinations(vs,2)) for vs in combinations(range(6),3)]
    for mask in range(1 << 15):
        require(any(len({mask>>i&1 for i in t}) == 1 for t in triples), 'R33 control')
    # The order-five triangle-free extremum and its exact equality family.
    e5 = tuple(combinations(range(5), 2))
    equality = []
    for mask in range(1 << 10):
        edges = {uv for bit,uv in enumerate(e5) if mask>>bit&1}
        if any(all(uv in edges for uv in combinations(vs,2)) for vs in combinations(range(5),3)):
            continue
        require(len(edges) <= 6, 'triangle-free five cap')
        if len(edges) == 6:
            require(any(edges == {uv for uv in e5 if (uv[0] in side) != (uv[1] in side)}
                        for side in combinations(range(5),2)), 'K23 equality')
            equality.append(mask)
    require(len(equality) == 10, 'K23 labeled count')
    # Triangle-edge common-neighbor counts cannot alternate between 2 and 3.
    for a,b,c in product((2,3),repeat=3):
        require(not (a!=b and b!=c and c!=a), 'local K23 triangle contradiction')
    return {'six_vertex_colorings': 32768, 'five_vertex_colorings': 1024,
            'K23_equality_graphs': 10, 'triangle_codegree_patterns': 8}

def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: check.py /external/scratch/literal-cores.txt')
    raw = Path(sys.argv[1]).read_text()
    literal = [int(x) for x in raw.splitlines()]
    require(literal == sorted(set(literal)), 'incomplete or duplicate native stream')
    d = json.loads((HERE/'certificate.json').read_text())
    out = check_document(d,literal)
    out['controls'] = controls()
    mutations = []
    for change in ('drop_core','wrong_orbit','drop_root','wrong_defect'):
        altered = json.loads(json.dumps(d))
        if change == 'drop_core':
            altered['cores'].pop()
        elif change == 'wrong_orbit':
            altered['cores'][0]['orbit_size'] += 1
        elif change == 'drop_root':
            altered['roots'].pop()
        else:
            altered['roots'][0]['central_red_excess'] = []
        try:
            check_document(altered,literal)
        except ValueError:
            mutations.append(change)
        else:
            raise ValueError('mutation accepted')
    out['rejected_mutations'] = mutations
    out['status'] = 'VERIFIED_M216_INTRINSIC_PARTITION_AND_BLUE_PAIR_EXCLUSION'
    print(json.dumps(out,sort_keys=True))

if __name__ == '__main__':
    main()
