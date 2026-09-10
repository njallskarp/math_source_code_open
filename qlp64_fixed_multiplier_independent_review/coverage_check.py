"""Direct length-8 box enumeration, independent of the doubling generator.

This quantifies its erroneous quarter-position filter. It does not construct
a QLP(64), or assert that any omitted compressed tuple lifts to a QLP.
"""
from itertools import product
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


def paf(r):
    return tuple(sum(r[j]*r[(j+k) % 8] for j in range(8)) for k in range(8))


def canon(q):
    return tuple(sorted(min(r, tuple(-v for v in r)) for r in q[:3]))+(q[3],)


def rows(s):
    result = []
    # Enumerate all symmetric rows in [-4,4]^8 directly, without parents.
    for a, b, c, d, e in product(range(-4, 5), repeat=5):
        r = (a, b, c, d, e, d, c, b)
        if sum(r) == s and a % 2 == s and e % 2 == 0 and sum(v*v for v in r) <= 57:
            result.append(r)
    return result


def realize(z, h):
    """Choose full binary orbit values by their residue-class negative counts."""
    remaining = set(range(64))
    groups = {}
    while remaining:
        j = min(remaining)
        orbit = {j, h*j % 64}
        remaining -= orbit
        residues = tuple(sorted({v % 8 for v in orbit}))
        groups.setdefault(residues, []).append(orbit)
    word = [1]*64
    for residues, orbits in groups.items():
        for selection in product((0, 1), repeat=len(orbits)):
            counts = {r: sum(sum(j % 8 == r for j in orbit) for bit, orbit in zip(selection, orbits) if bit)
                      for r in residues}
            if all(counts[r] == 4-z[r] for r in residues):
                for bit, orbit in zip(selection, orbits):
                    if bit:
                        for j in orbit:
                            word[j] = -1
                break
        else:
            raise RuntimeError('no full binary realization')
    if not all(word[j] == word[h*j % 64] for j in range(64)):
        raise RuntimeError('realization invariance failure')
    if tuple(sum(word[j+8*t] for t in range(8))//2 for j in range(8)) != z:
        raise RuntimeError('realization compression failure')
    if sum(word) != 2*sum(z):
        raise RuntimeError('realization sum failure')
    return word


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Compare with the compact published expected census')
    parser.add_argument('--historical-module', help='Optional archived compress.py to compare after independent enumeration')
    args = parser.parse_args()
    zero, special = rows(0), rows(1)
    correlations = {r: paf(r) for r in zero+special}
    left = {}
    for a, b in product(zero, repeat=2):
        key = tuple(x+y for x, y in zip(correlations[a], correlations[b]))
        left.setdefault(key, []).append((a, b))
    wanted = (57,)+(-8,)*7
    full = set()
    labelled = 0
    retained_labelled = 0
    retained = set()
    for c, d in product(zero, special):
        key = tuple(t-x-y for t, x, y in zip(wanted, correlations[c], correlations[d]))
        for a, b in left.get(key, ()):
            q = (a, b, c, d)
            labelled += 1
            full.add(canon(q))
            # In a 4 -> 8 lift the extra source guard is z[2] even.
            if all(r[2] % 2 == 0 for r in q):
                retained_labelled += 1
                retained.add(canon(q))
    if not retained < full:
        raise RuntimeError('expected strict loss of valid compressed tuples')
    if args.historical_module:
        spec = importlib.util.spec_from_file_location('historical_compress', args.historical_module)
        source = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(source)
        zr, sr = source.root_rows(0), source.root_rows(1)
        roots = {source.canonical(q) for q in source.match((zr,zr,zr,sr),source.target(4))}
        if set(source.extend(roots)) != retained:
            raise RuntimeError('actual historical generator differs from retained census')
    example = min(full-retained)
    # Check every excluded tuple folds to a valid root, not just the example.
    for q in full:
        parent = [tuple(r[j]+r[j+4] for j in range(4)) for r in q]
        for i, r in enumerate(parent):
            if not (sum(r) == (i == 3) and max(map(abs, r)) <= 8
                    and r[0] % 2 == (i == 3) and r[2] % 2 == 0
                    and r[1] == r[3] and sum(x*x for x in r) <= 49):
                raise RuntimeError('invalid folded root')
        values = tuple(sum(r[j]*r[(j+k) % 4] for r in parent for j in range(4)) for k in range(4))
        if values != (49, -16, -16, -16):
            raise RuntimeError('folded root correlations fail')
    data = (json.dumps(sorted(full), separators=(',', ':'))+'\n').encode()
    realizations = []
    for h in (31, 63):
        words = [realize(z, h) for z in example]
        failures = sum(sum(sum(r[j]*r[(j+k)%64] for j in range(64)) for r in words) != -4
                       for k in range(1,64))
        if not failures:
            raise RuntimeError('unexpected QLP(64) witness: inspect before proceeding')
        realizations.append(dict(multiplier=h, full_real_correlation_failures=failures,
                                 binary_words_hex=[format(sum(1<<j for j,v in enumerate(r) if v == -1),'016x')
                                                   for r in words]))
    report = dict(status='PASS', length=8, eligible_rows=[len(zero),len(special)],
                  labelled=labelled, canonical=len(full),
                  retained_labelled=retained_labelled, retained_canonical=len(retained),
                  omitted_canonical=len(full-retained),
                  all_folded_roots_valid=True, canonical_sha256=hashlib.sha256(data).hexdigest(),
                  omitted_example=example,
                  example_paf=[sum(paf(r)[k] for r in example) for k in range(8)],
                  full_binary_realizations=realizations,
                  is_qlp_counterexample=False)
    if args.check:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())['coverage_audit']
        if json.loads(json.dumps(report)) != expected:
            raise RuntimeError('census differs from the published expected result')
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
