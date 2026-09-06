"""Definition-level controls for the weaker kernel and complete physical scope."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import tempfile
import audit
import consumer
import local_classification


def forbidden(colors, active):
    for q in combinations(range(active), 5):
        values = {colors[e] for e in combinations(q, 2)}
        if len(values) == 1:
            return True
    return False


def cohort(inputs, certificate, consensus):
    rows = list(consumer.cases(inputs, certificate))
    expected = [(j, k) for j in range(29) for k in range(12)]
    audit.require([x[0] for x in rows] == expected, 'complete ordered cohort')
    pairs = list(combinations(range(43), 2))
    for key, edges, mark, columns in rows:
        raw = audit.matrix(inputs, certificate, consensus, key)
        fixed = consumer.specification(edges, mark, columns, consensus)
        produced = bytes(48+int(fixed[e]) if e in fixed else 50 for e in pairs)
        audit.require(raw == produced, 'independent complete physical template')
    return audit.coverage(inputs, certificate, consensus)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--upstream', type=Path, required=True)
    p.add_argument('--audit-cnf', required=True)
    p.add_argument('--audit-local', required=True)
    args = p.parse_args()
    source = Path(__file__).resolve().parent
    inputs, cert = audit.load_inputs(args.upstream)
    consensus = json.loads((source/'CONSENSUS.json').read_text())
    local = json.loads((source/'LOCAL_CERTIFICATE.json').read_text())
    result = cohort(inputs, cert, consensus)
    rng = random.Random(61043)
    assignments = accepted = formulas = rejected = 0
    with tempfile.TemporaryDirectory(prefix='r55-kernel-controls-') as directory:
        scratch = Path(directory)
        result['local_classification'] = local_classification.classify(
            inputs, consensus, local, args.audit_cnf, args.audit_local, scratch)
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
        inputs, cert = audit.load_inputs(args.upstream)
        for key in [(0,126,0,0), (29,0), (0,12), (-1,0), (0,False)]:
            try:
                audit.matrix(inputs, cert, consensus, key)
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
        raw = audit.matrix(inputs, cert, consensus, (0,0))
        fixed = consumer.specification(*list(consumer.cases(inputs, cert))[0][1:], consensus)
        _, variables, clauses = consumer.encode(fixed)
        outside = next(v for e, v in variables.items() if e[1] >= 40)
        for bad_variables, bad_clauses in [(dict(list(variables.items())[1:]), clauses),
                                           (variables, clauses | {(outside,)})]:
            try:
                audit.check_support(raw, bad_variables, bad_clauses, consensus)
            except ValueError:
                rejected += 1
            else:
                raise ValueError('changed physical scope accepted')
        # Reject changed coverage maps, undeclared freedom and false local certificates.
        bad_consensuses = []
        changed = deepcopy(consensus)
        changed['interfaces'] = [10, 11]
        bad_consensuses.append(changed)
        changed = deepcopy(consensus)
        changed['second_to_first'][0] = changed['second_to_first'][1]
        bad_consensuses.append(changed)
        changed = deepcopy(consensus)
        changed['free_common_edges'].pop()
        bad_consensuses.append(changed)
        for changed in bad_consensuses:
            try:
                audit.validate_consensus(inputs, changed)
            except ValueError:
                rejected += 1
            else:
                raise ValueError('false consensus accepted')
        for field, value in [('conflict_edges', local['conflict_edges'][:-1]),
                             ('required_meeting_sets', [[3, 5]]),
                             ('models', local['models'][:-1]),
                             ('dense_models', [441]),
                             ('model_sha256', '0'*64)]:
            changed = deepcopy(local)
            changed[field] = value
            try:
                local_classification.classify(inputs, consensus, changed,
                                               args.audit_cnf, args.audit_local, scratch)
            except ValueError:
                rejected += 1
            else:
                raise ValueError('false local certificate accepted')
        for raw in [b'2'*230, b'2'*232, b'0'*231, b'2'*231, b'3'*231, b'0'*210+b'2'*21]:
            (scratch/'bad-local.matrix').write_bytes(raw)
            run = subprocess.run([args.audit_local, str(scratch/'bad-local.matrix'),
                                  str(scratch/'bad-local.models')], capture_output=True)
            audit.require(run.returncode != 0, 'malformed local matrix accepted')
            rejected += 1
    result.update(status='VERIFIED_TWENTY_EDGE_CLASSIFICATION_COVERAGE_AND_KERNEL_CONTROLS',
                  small_formulas=formulas, full_assignments=assignments,
                  satisfying_assignments=accepted, corruptions_rejected=rejected,
                  omitted_vertex_relaxation_checked=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
