"""Complete two-interface consensus consumer; 40-vertex necessary kernel."""
import argparse
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess
import time
import audit

PAIRS = list(combinations(range(43), 2))


def cases(inputs, certificate):
    record = inputs['interfaces'][1]
    bits = ''.join(f'{ord(c)-63:06b}' for c in record[1:])
    edges = set()
    offset = 0
    for v in range(22):
        for u in range(v):
            if bits[offset] == '1':
                edges.add((u, v))
            offset += 1
    s = [u for u in range(21) if (u, 21) in edges]
    template = {(i, j) for i in (0, 1) for j in (2, 3, 4)}
    marks = [q for q in permutations(s)
             if {tuple(sorted((q[i], q[j]))) for i, j in template}
             == {e for e in edges if e[0] in s and e[1] in s}]
    family = next(f for f in certificate['families'] if f['type'] == 126)
    for j, rep in enumerate(family['representatives']):
        for k, mark in enumerate(marks):
            yield (j, k), edges, mark, rep['columns']


def specification(edges, mark, columns, consensus=None):
    lookup = {v: i for i, v in enumerate(mark)}
    fixed = {}
    for u, v in PAIRS:
        if v < 22:
            fixed[u, v] = (u, v) in edges
        elif u == 22 or v == 22:
            fixed[u, v] = (u if v == 22 else v) < 22
        elif u == 21:
            fixed[u, v] = v < 40
        elif 23 <= u < v < 40:
            fixed[u, v] = (v-u) % 17 in {1, 2, 4, 8, 9, 13, 15, 16}
        elif u in lookup and 23 <= v < 40:
            fixed[u, v] = bool(columns[lookup[u]] >> (v-23) & 1)
    if consensus is not None:
        for edge in consensus['free_common_edges']:
            del fixed[tuple(edge)]
    return fixed


def encode(fixed, order=43, active=40):
    """Only active vertices contribute constraints; all unfixed pairs are variables."""
    if not 5 <= active <= order <= 43:
        raise ValueError('orders must satisfy 5 <= active <= order <= 43')
    pairs = list(combinations(range(order), 2))
    if any(e not in pairs or type(c) not in (int, bool) or c not in (0, 1)
           for e, c in fixed.items()):
        raise ValueError('invalid fixed physical edge')
    variables = {e: i+1 for i, e in enumerate(e for e in pairs if e not in fixed)}
    clauses = set()
    for color in (False, True):
        allowed = [sum(1 << v for v in range(u+1, active)
                       if fixed.get((u, v), color) == color) for u in range(active)]

        def visit(chosen, candidates):
            if len(chosen) == 5:
                clauses.add(tuple((-1 if color else 1)*variables[e]
                                  for e in combinations(chosen, 2) if e in variables))
                return
            while candidates.bit_count() >= 5-len(chosen):
                bit = candidates & -candidates
                candidates ^= bit
                v = bit.bit_length()-1
                visit(chosen+[v], candidates & allowed[v])

        visit([], (1 << active)-1)
    data = (f'p cnf {len(variables)} {len(clauses)}\n'
            + ''.join(' '.join(map(str, c))+' 0\n' for c in sorted(clauses))).encode()
    return data, variables, clauses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('scratch', type=Path)
    parser.add_argument('--upstream', type=Path, required=True)
    parser.add_argument('--kissat', required=True)
    parser.add_argument('--drat-trim', required=True)
    parser.add_argument('--audit-cnf', required=True)
    parser.add_argument('--seconds', type=int, default=30)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    scratch = args.scratch.resolve()
    if scratch.exists() or source == scratch or source in scratch.parents:
        raise ValueError('new external scratch required')
    scratch.mkdir(parents=True)
    inputs, certificate = audit.load_inputs(args.upstream)
    consensus = json.loads((source/'CONSENSUS.json').read_text())
    audit.validate_consensus(inputs, consensus)
    rows = list(cases(inputs, certificate))
    expected_keys = {(j, k) for j in range(29) for k in range(12)}
    audit.require(len(rows) == 348 and {r[0] for r in rows} == expected_keys,
                  'complete cohort keys')
    manifest, runs = [], []
    for key, edges, mark, columns in rows:
        stem = '-'.join(map(str, key))
        fixed = specification(edges, mark, columns, consensus)
        raw = bytes(48+int(fixed[e]) if e in fixed else 50 for e in PAIRS)
        independently_fixed = audit.matrix(inputs, certificate, consensus, key)
        audit.require(raw == independently_fixed, 'physical specifications differ')
        data, variables, clauses = encode(fixed)
        audit.check_support(raw, variables, clauses, consensus)
        matrix = scratch/(stem+'.matrix')
        matrix.write_bytes(independently_fixed)
        cnf = scratch/(stem+'.cnf')
        cnf.write_bytes(data)
        other = scratch/(stem+'.independent.cnf')
        subprocess.run([args.audit_cnf, '43', '40', str(matrix), str(other)], check=True)
        audit.require(other.read_bytes() == data, 'literal five-set formula mismatch')
        proof = scratch/(stem+'.drat')
        start = time.monotonic()
        with (scratch/(stem+'.solver.log')).open('w') as log:
            solved = subprocess.run([args.kissat, '--time='+str(args.seconds),
                                     str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=args.seconds+15)
        solver_seconds = time.monotonic()-start
        audit.require(solved.returncode == 20, 'UNSAT not established: cohort incomplete')
        start = time.monotonic()
        checked = subprocess.run([args.drat_trim, str(cnf), str(proof)],
                                 text=True, capture_output=True, timeout=120)
        (scratch/(stem+'.check.log')).write_text(checked.stdout+checked.stderr)
        audit.require(checked.returncode == 0 and 's VERIFIED' in checked.stdout,
                      'refutation not verified')
        row = {'key': list(key), 'variables': len(variables), 'clauses': len(clauses),
               'cnf_sha256': sha256(data).hexdigest(), 'matrix_sha256': sha256(raw).hexdigest()}
        manifest.append(row)
        runs.append({**row, 'solver_seconds': solver_seconds,
                     'checker_seconds': time.monotonic()-start,
                     'proof_bytes': proof.stat().st_size,
                     'proof_sha256': sha256(proof.read_bytes()).hexdigest()})
        (scratch/'runs.json').write_text(json.dumps(runs, indent=2)+'\n')
        if len(runs) % 12 == 0:
            print(len(runs), 'of 348 cases VERIFIED', flush=True)
    raw = (json.dumps(manifest, indent=2, sort_keys=True)+'\n').encode()
    (scratch/'manifest.json').write_bytes(raw)
    if (source/'MANIFEST.json').exists():
        audit.require((source/'MANIFEST.json').read_bytes() == raw, 'manifest changed')
    result = {'status': 'VERIFIED_COMPLETE_TWENTY_EDGE_TYPE126_DENSITY116_EXCLUSION',
              'complete_cases': 348, 'covered_original_cases': 696, 'valid_local_fillings': 434, 'interfaces': [1, 2], 'kernel_vertices': 40,
              'physical_free_edges': 409, 'kernel_edge_variables': 292,
              'unconstrained_outside_edges': 117,
              'new_global_hub_deficiency_lower_bound': 7,
              'manifest_sha256': sha256(raw).hexdigest()}
    (scratch/'result.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
