"""A valid compressed quadruple discarded by the withdrawn QLP(64) cover."""
from itertools import product
import json

ROWS = (
    (-2, 0, 1, 0, 0, 0, 1, 0),
    (-2, 3, -1, -1, 0, -1, -1, 3),
    (-2, -1, 0, 1, 2, 1, 0, -1),
    (-1, 0, 2, 0, -2, 0, 2, 0),
)


def paf(x):
    n = len(x)
    return tuple(sum(x[j]*x[(j+k) % n] for j in range(n)) for k in range(n))


def realize(z):
    """Independent orbit enumeration within each reflected residue-class group."""
    unseen = set(range(64))
    groups = {}
    while unseen:
        j = min(unseen)
        orbit = tuple(sorted({j, -j % 64}))
        unseen.difference_update(orbit)
        key = tuple(sorted({v % 8 for v in orbit}))
        groups.setdefault(key, []).append(orbit)
    x = [0]*64
    for residues, orbits in sorted(groups.items()):
        for signs in product((-1, 1), repeat=len(orbits)):
            sums = {r: 0 for r in residues}
            for orbit, sign in zip(orbits, signs):
                for j in orbit:
                    sums[j % 8] += sign
            if all(sums[r] == 2*z[r] for r in residues):
                for orbit, sign in zip(orbits, signs):
                    for j in orbit:
                        x[j] = sign
                break
        else:
            raise AssertionError('no realization')
    return tuple(x)


def main():
    parents = tuple(tuple(r[j]+r[j+4] for j in range(4)) for r in ROWS)
    for rows, d, bound, target in ((ROWS, 8, 4, (57,)+(-8,)*7),
                                  (parents, 4, 8, (49,)+(-16,)*3)):
        for r, s in zip(rows, (0, 0, 0, 1)):
            assert sum(r) == s and max(map(abs, r)) <= bound
            assert all(r[j] == r[-j % d] for j in range(d))
            assert (r[0]-bound-s) % 2 == 0
            assert (r[d//2]-bound) % 2 == 0
        assert tuple(sum(paf(r)[k] for r in rows) for k in range(d)) == target
    # The invalid guard tested child-quarter parity, not child-midpoint parity.
    discarded_rows = [i for i, p in enumerate(parents) if (p[2]//2-4) % 2]
    assert discarded_rows == [0, 1]
    words = []
    realizations = []
    for z, s in zip(ROWS, (0, 0, 0, 1)):
        x = realize(z)
        assert sum(x) == 2*s
        assert all(x[j] == x[-j % 64] for j in range(64))
        assert tuple(sum(x[j+8*t] for t in range(8))//2 for j in range(8)) == z
        realizations.append(x)
        words.append(format(sum(1 << j for j, v in enumerate(x) if v == -1), '016x'))
    failures = sum(sum(paf(x)[k] for x in realizations) != -4 for k in range(1, 64))
    assert failures > 0
    result = {'valid_child_length': 8, 'valid_parent_length': 4,
                      'combined_child_paf': [57]+[-8]*7,
                      'discarded_rows': discarded_rows,
                      'normalized_full_binary_realizations_hex': words,
                      'full_real_correlation_failures': failures,
                      'is_qlp_counterexample': False}
    import sys
    from pathlib import Path
    if '--check' in sys.argv:
        assert result == json.loads(Path(__file__).with_name('expected.json').read_text())
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
