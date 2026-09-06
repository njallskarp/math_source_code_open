"""Complete local family: independent sets of an 18-edge conflict graph."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import audit
import consumer


def has_clique(adj, k):
    def search(candidates, left):
        if left == 0:
            return True
        while candidates:
            if candidates.bit_count() < left:
                return False
            bit = candidates & -candidates
            candidates ^= bit
            v = bit.bit_length()-1
            if search(candidates & adj[v], left-1):
                return True
        return False
    return search((1 << len(adj))-1, k)


def classify(inputs, consensus, local, executable, scratch):
    first, second = audit.validate_consensus(inputs, consensus)
    pairs = list(combinations(range(23), 2))
    fixed = {e: int(e in first) for e in combinations(range(22), 2)
             if (e in first) == (e in second)}
    fixed.update({(v, 22): 1 for v in range(22)})
    raw = bytes(48+fixed[e] if e in fixed else 50 for e in pairs)
    data, variables, clauses = consumer.encode(fixed, 23, 23)
    matrix = scratch/'local.matrix'
    matrix.write_bytes(raw)
    subprocess.run([executable, '23', '23', str(matrix), str(scratch/'local.independent.cnf')],
                   capture_output=True, check=True)
    audit.require((scratch/'local.independent.cnf').read_bytes() == data, 'literal local CNF')
    (scratch/'local.cnf').write_bytes(data)
    audit.require(len(variables) == 12 and list(variables) == [tuple(e) for e in local['free_common_edges']],
                  'ordered local variables')
    minimal = {c for c in clauses if not any(set(d) < set(c) for d in clauses)}
    conflict = local['conflict_edges']
    audit.require(len(conflict) == 18 and conflict == sorted(map(sorted, conflict))
                  and len(set(map(tuple, conflict))) == 18
                  and all(1 <= u < v <= 12 for u, v in conflict), 'conflict graph')
    expected = {tuple(sorted(local['required_meeting_set']))}
    expected |= {tuple(-x for x in sorted(e)) for e in conflict}
    audit.require(minimal == expected and local['required_meeting_set'] == [3, 4],
                  'exact independent-set characterization')
    by_conflict, by_cnf, by_graph, densities = [], [], [], []
    for mask in range(1 << 12):
        if any(mask >> (i-1) & 1 for i in (3, 4)) and all(
                not (mask >> (u-1) & 1 and mask >> (v-1) & 1) for u, v in conflict):
            by_conflict.append(mask)
        if all(any((mask >> (abs(x)-1) & 1) == (x > 0) for x in c) for c in clauses):
            by_cnf.append(mask)
        adj = [0]*22
        for u, v in combinations(range(22), 2):
            color = mask >> (variables[u, v]-1) & 1 if (u, v) in variables else fixed[u, v]
            if color:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
        blue = [((1 << 22)-1) ^ row ^ (1 << v) for v, row in enumerate(adj)]
        if not has_clique(adj, 4) and not has_clique(blue, 5):
            by_graph.append(mask)
            densities.append(sum(row.bit_count() for row in adj)//2)
            audit.require([v for v, row in enumerate(adj) if row.bit_count() == 5] == [21],
                          'unique distinguished hub in every local filling')
    audit.require(by_conflict == by_cnf == by_graph == local['models'], 'all local models agree')
    histogram = dict(sorted(Counter(map(str, densities)).items()))
    audit.require(len(by_graph) == local['model_count'] == 110
                  and histogram == local['density_histogram'], 'complete local density counts')
    raw_models = ''.join(str(m)+'\n' for m in by_graph).encode()
    audit.require(sha256(raw_models).hexdigest() == local['model_sha256'], 'local model stream')
    dense = [m for m, e in zip(by_graph, densities) if e == 109]
    inherited = sorted(sum(1 << (v-1) for e, v in variables.items() if e in edges)
                       for edges in (first, second))
    audit.require(dense == local['dense_models'] == inherited, 'both original dense endpoints')
    audit.require(sum(fixed[e] for e in fixed if e[1] < 22) == 103, 'density polynomial base')
    return {'complete_assignments': 4096, 'literal_local_clauses': len(clauses),
            'minimal_clauses': len(minimal), 'conflict_edges': len(conflict),
            'valid_local_fillings': len(by_graph), 'density_histogram': histogram,
            'dense_models': dense, 'all_unique_hub': True,
            'model_sha256': sha256(raw_models).hexdigest()}
