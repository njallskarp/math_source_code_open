"""Definition-level controls for the weaker kernel and complete physical scope."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import tempfile
import audit
import consumer


def forbidden(colors, active):
    for q in combinations(range(active), 5):
        values = {colors[e] for e in combinations(q, 2)}
        if len(values) == 1:
            return True
    return False


def cohort(upstream):
    inputs, _ = audit.load_inputs(upstream)
    certificate = json.loads(Path(__file__).with_name('certificate.json').read_text())
    rows = list(consumer.cases(inputs, certificate))
    expected = [(6, 62, j, k) for j in range(1697) for k in range(2)]
    audit.require([x[0] for x in rows] == expected, 'complete ordered cohort')
    pairs = list(combinations(range(43), 2))
    location = {e: i for i, e in enumerate(pairs)}
    moved = [(5*v+7) % 43 for v in range(43)]
    seen, digest, checks = set(), sha256(), 0
    for key, edges, mark, columns in rows:
        raw = audit.matrix(inputs, certificate, key)
        fixed = consumer.specification(edges, mark, columns)
        produced = bytes(48+int(fixed[e]) if e in fixed else 50 for e in pairs)
        audit.require(raw == produced and raw not in seen, 'distinct physical template')
        seen.add(raw)
        digest.update((' '.join(map(str, key))+'\n').encode())
        digest.update(bytes(c-48 for c in raw))
        values = [c-48 if c != 50 else (i+key[2]+key[3]) % 2 for i, c in enumerate(raw)]
        image = [None]*903
        for e, c in zip(pairs, values):
            image[location[tuple(sorted((moved[e[0]], moved[e[1]])))]] = c
        for e, c in zip(pairs, values):
            audit.require(image[location[tuple(sorted((moved[e[0]], moved[e[1]])))]] == c,
                          'physical transport')
            checks += 1
    return {'cohort_templates': len(seen), 'physical_edge_transports': checks,
            'marked_template_sha256': digest.hexdigest()}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--upstream', type=Path, required=True)
    p.add_argument('--audit-cnf', required=True)
    args = p.parse_args()
    result = cohort(args.upstream)
    rng = random.Random(61043)
    assignments = accepted = formulas = rejected = 0
    with tempfile.TemporaryDirectory(prefix='r55-kernel-controls-') as directory:
        scratch = Path(directory)
        for n in (5, 6, 7, 8):
            pairs = list(combinations(range(n), 2))
            for trial in range(8):
                active = 5+trial % (n-4)
                free = set(rng.sample(pairs, min(10, len(pairs))))
                fixed = {e: rng.randrange(2) for e in pairs if e not in free}
                data, variables, clauses = consumer.encode(fixed, n, active)
                raw = bytes(48+fixed[e] if e in fixed else 50 for e in pairs)
                (scratch/'matrix').write_bytes(raw)
                subprocess.run([args.audit_cnf, str(n), str(active), str(scratch/'matrix'),
                                str(scratch/'formula')], check=True, capture_output=True)
                audit.require((scratch/'formula').read_bytes() == data, 'small literal CNF')
                formulas += 1
                for mask in range(1 << len(variables)):
                    colors = {**fixed, **{e: mask >> (v-1) & 1 for e, v in variables.items()}}
                    satisfies = all(any((mask >> (abs(x)-1) & 1) == (x > 0) for x in c)
                                    for c in clauses)
                    audit.require(satisfies == (not forbidden(colors, active)),
                                  'truth table differs from physical definition')
                    assignments += 1
                    accepted += satisfies
        # A forbidden five-set involving an omitted vertex is intentionally irrelevant.
        colors = {e: int(4 not in e) for e in combinations(range(6), 2)}
        data, variables, clauses = consumer.encode(colors, 6, 5)
        audit.require(not forbidden(colors, 5) and forbidden(colors, 6)
                      and not variables and not clauses, 'proper weaker-system control')
        for raw, n, active in [(b'2'*9, 5, 5), (b'2'*11, 5, 5), (b'3'*10, 5, 5),
                               (b'2'*10, 5, 4), (b'2'*10, 5, 6), (b'', 44, 40),
                               (b'2'*10, '5x', 5)]:
            (scratch/'matrix').write_bytes(raw)
            run = subprocess.run([args.audit_cnf, str(n), str(active), str(scratch/'matrix'),
                                  str(scratch/'bad')], capture_output=True)
            audit.require(run.returncode != 0, 'malformed matrix accepted')
            rejected += 1
        inputs, _ = audit.load_inputs(args.upstream)
        cert = json.loads(Path(__file__).with_name('certificate.json').read_text())
        for key in [(1,62,0,0), (6,126,0,0), (6,62,1697,0), (6,62,0,2), (6,62,-1,0), (6,62,False,0), (6.0,62,0,0)]:
            try:
                audit.matrix(inputs, cert, key)
            except ValueError:
                rejected += 1
            else:
                raise ValueError('invalid cohort key accepted')
        for name in audit.PINS:
            changed = scratch/'upstream'
            changed.mkdir(exist_ok=True)
            for file in audit.PINS:
                data = (args.upstream/file).read_bytes()
                (changed/file).write_bytes(data+b' ' if file == name else data)
            try:
                audit.load_inputs(changed)
            except ValueError:
                rejected += 1
            else:
                raise ValueError('changed upstream accepted')
        raw = audit.matrix(inputs, cert, (6,62,0,0))
        fixed = consumer.specification(*list(consumer.cases(inputs, cert))[0][1:])
        _, variables, clauses = consumer.encode(fixed)
        outside = next(v for e, v in variables.items() if e[1] >= 40)
        for bad_variables, bad_clauses in [(dict(list(variables.items())[1:]), clauses),
                                           (variables, clauses | {(outside,)})]:
            try:
                audit.check_support(raw, bad_variables, bad_clauses)
            except ValueError:
                rejected += 1
            else:
                raise ValueError('changed physical scope accepted')
    result.update(status='VERIFIED_KERNEL_CONTROLS_AND_COMPLETE_COHORT',
                  small_formulas=formulas, full_assignments=assignments,
                  satisfying_assignments=accepted, corruptions_rejected=rejected,
                  omitted_vertex_relaxation_checked=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
