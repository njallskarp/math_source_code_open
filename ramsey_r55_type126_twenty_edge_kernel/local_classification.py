"""Conflict-independent-set generator versus complete literal C++ enumeration."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
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


def independent_transversals(conflict, meeting):
    adj = [0]*20
    for u, v in conflict:
        adj[u-1] |= 1 << (v-1)
        adj[v-1] |= 1 << (u-1)
    hits = [sum(1 << (v-1) for v in row) for row in meeting]
    models = []

    def visit(chosen, available):
        if any(not h & (chosen | available) for h in hits):
            return
        if not available:
            models.append(chosen)
            return
        bit = available & -available
        rest = available ^ bit
        visit(chosen, rest)
        visit(chosen | bit, rest & ~adj[bit.bit_length()-1])

    visit(0, (1 << 20)-1)
    return sorted(models)


def classify(inputs, consensus, local, executable, local_executable, scratch):
    first, second = audit.validate_consensus(inputs, consensus)
    fixed = {e: int(e in first) for e in combinations(range(22), 2)
             if (e in first) == (e in second)}
    raw22 = bytes(48+fixed[e] if e in fixed else 50
                  for e in combinations(range(22), 2))
    fixed.update({(v, 22): 1 for v in range(22)})
    raw23 = bytes(48+fixed[e] if e in fixed else 50
                  for e in combinations(range(23), 2))
    data, variables, clauses = consumer.encode(fixed, 23, 23)
    (scratch/'local23.matrix').write_bytes(raw23)
    subprocess.run([executable, '23', '23', str(scratch/'local23.matrix'),
                    str(scratch/'local.independent.cnf')], check=True, capture_output=True)
    audit.require((scratch/'local.independent.cnf').read_bytes() == data, 'literal local CNF')
    (scratch/'local.cnf').write_bytes(data)
    audit.require(len(variables) == 20 and list(variables) == list(map(tuple, local['free_common_edges'])),
                  'ordered local variables')
    minimal = {c for c in clauses if not any(set(d) < set(c) for d in clauses)}
    conflict, meeting = local['conflict_edges'], local['required_meeting_sets']
    audit.require(conflict == sorted(map(sorted, conflict))
                  and len(set(map(tuple, conflict))) == len(conflict) == 29
                  and all(1 <= u < v <= 20 for u, v in conflict), 'conflict graph')
    audit.require(len(meeting) == 8 and meeting == sorted(meeting)
                  and all(row == sorted(set(row)) and all(1 <= v <= 20 for v in row)
                          for row in meeting), 'required intersections')
    expected = {tuple(-v for v in e) for e in conflict} | set(map(tuple, meeting))
    audit.require(minimal == expected, 'exact independent-set transversal characterization')
    models = independent_transversals(conflict, meeting)
    audit.require(models == local['models'] and len(models) == local['model_count'] == 434,
                  'complete conflict-graph enumeration')
    stream = ''.join(str(m)+'\n' for m in models).encode()
    (scratch/'local22.matrix').write_bytes(raw22)
    result = subprocess.run([local_executable, str(scratch/'local22.matrix'),
                             str(scratch/'independent.models')], check=True, capture_output=True)
    native = json.loads(result.stdout)
    audit.require((scratch/'independent.models').read_bytes() == stream,
                  'independent all-assignment literal graph enumeration')
    densities = []
    for mask in models:
        adj = [0]*22
        for u, v in combinations(range(22), 2):
            color = mask >> (variables[u, v]-1) & 1 if (u, v) in variables else fixed[u, v]
            if color:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
        blue = [((1 << 22)-1) ^ row ^ (1 << v) for v, row in enumerate(adj)]
        audit.require(not has_clique(adj, 4) and not has_clique(blue, 5), 'physical local graph')
        audit.require([v for v,row in enumerate(adj) if row.bit_count() == 5] == [21], 'unique hub')
        densities.append(sum(row.bit_count() for row in adj)//2)
    histogram = dict(sorted(Counter(map(str, densities)).items()))
    audit.require(native == {'complete_assignments': 1048576, 'valid_local_fillings': 434,
                             'all_unique_hub': True, 'density_histogram': histogram}, 'native local summary')
    audit.require(histogram == local['density_histogram'] and sha256(stream).hexdigest() == local['model_sha256'],
                  'local census identity')
    dense = [m for m, e in zip(models, densities) if e == 109]
    inherited = sorted(sum(1 << (v-1) for e,v in variables.items() if e in edges)
                       for edges in (first, second))
    audit.require(dense == local['dense_models'] == inherited, 'complete dense endpoints')
    audit.require(sum(c for e,c in fixed.items() if e[1]<22) == local['fixed_red_base'] == 99,
                  'density polynomial base')
    return {**native, 'literal_local_clauses': len(clauses), 'minimal_clauses': len(minimal),
            'conflict_edges': len(conflict), 'required_meeting_sets': len(meeting),
            'dense_models': dense, 'model_sha256': sha256(stream).hexdigest()}
