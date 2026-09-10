"""Independent bounded enumeration and Gaussian-integer checks of the cover."""
from itertools import product
import json
from pathlib import Path
import search


def reference_paf(p):
    n = len(p)
    return tuple(sum(p[j]*p[(j+k) % n] for j in range(n)) for k in range(n))


def reference_axes(p):
    """Imaginary autocorrelation of 2*G(p,reverse(p)), without polynomial squares."""
    n = len(p)
    real = [p[j]+p[-j % n] for j in range(n)]
    imag = [p[j]-p[-j % n] for j in range(n)]
    return all(sum(imag[j]*real[(j+k) % n]-real[j]*imag[(j+k) % n]
                   for j in range(n)) == 0 for k in range(n))


def roots_audit():
    ps, rs, ss = set(), set(), set()
    for row in product(range(-8, 9), repeat=4):
        norm = sum(v*v for v in row)
        if sum(row) == 0 and 2*norm <= 49 and reference_axes(row):
            ps.add(row)
        if row[1] != row[3] or norm > 49:
            continue
        for s, out in ((0, rs), (1, ss)):
            if sum(row) == s and (row[0]-s) % 2 == 0 and row[2] % 2 == 0:
                out.add(row)
    generated = search.root_rows()
    assert tuple(map(set, generated)) == (ps, rs, ss)
    correlations = {r: reference_paf(r) for r in ps | rs | ss}
    wanted = (49, -16, -16, -16)
    triples = {q for q in product(ps, rs, ss)
               if tuple(2*a+b+c for a, b, c in zip(*(correlations[r] for r in q)))
               == wanted}
    assert triples == set(search.match(*generated, search.target(4)))
    return {'root_row_counts': [len(ps), len(rs), len(ss)],
            'direct_triples': len(triples)}


def lift_audit():
    mixed, symmetric = {}, ({}, {})
    axis_checks = 0
    for child in product((-1, 0, 1), repeat=8):
        reference = reference_axes(child)
        assert search.axes(child) == reference
        axis_checks += 1
        parent = tuple(child[j]+child[j+4] for j in range(4))
        if sum(child) == 0 and reference:
            mixed.setdefault(parent, set()).add(child)
        if all(child[j] == child[-j % 8] for j in range(8)):
            for s in (0, 1):
                if sum(child) == s and (child[0]-1-s) % 2 == 0 and (child[4]-1) % 2 == 0:
                    symmetric[s].setdefault(parent, set()).add(child)
    mixed_parents = symmetric_parents = 0
    for parent in product(range(-2, 3), repeat=4):
        if sum(parent) == 0 and reference_axes(parent):
            assert set(search.mixed_lifts(parent, 1, 8)) == mixed.get(parent, set())
            mixed_parents += 1
        if parent[1] == parent[3]:
            for s in (0, 1):
                if sum(parent) == s:
                    assert set(search.symmetric_lifts(parent, s, 1, 8)) == symmetric[s].get(parent, set())
                    symmetric_parents += 1
    return {'ternary_axis_checks': axis_checks,
            'mixed_parents_including_empty': mixed_parents,
            'mixed_nonempty_parents': len(mixed),
            'mixed_children': sum(map(len, mixed.values())),
            'symmetric_parents_including_empty': symmetric_parents,
            'symmetric_nonempty_parents': [len(g) for g in symmetric],
            'symmetric_children': [sum(map(len, g.values())) for g in symmetric]}


def alphabet_audit():
    total = invariant = 0
    for n in range(2, 66, 2):
        fixed = 0
        # Counts (a+1,b+1,a,b) have Gaussian sum 1+i and length n.
        for a in range(n//2):
            b = n//2-1-a
            counts = (a+1, b+1, a, b)
            assert sum(counts) == n
            total += 1
            if counts[0] == counts[1] and counts[2] == counts[3]:
                fixed += 1
        assert fixed == (1 if n % 4 == 2 else 0)
        invariant += fixed
    return {'normalized_count_vectors': total,
            'conjugating_invariant_vectors': invariant,
            'positive_controls_lengths_2_mod_4': 16,
            'invariant_vectors_at_lengths_0_mod_4': 0}


def run():
    return {'roots': roots_audit(), 'lifts': lift_audit(),
            'alphabet': alphabet_audit()}


if __name__ == '__main__':
    import sys
    result = run()
    if '--check' in sys.argv:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        assert result == expected['audit']
    print(json.dumps(result, sort_keys=True, indent=2))
