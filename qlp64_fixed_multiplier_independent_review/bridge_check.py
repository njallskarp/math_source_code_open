"""Independent small-order checks of pairing/sign coverage and affine closure.

All acceptance arithmetic is integer arithmetic. No reviewed module is imported.
"""
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def corr(a, b, k):
    return sum(x*b[(j+k) % len(a)] for j, x in enumerate(a))


def gray(x, y):
    return tuple(((a+b)//2, (a-b)//2) for a, b in zip(x, y))


def gaussian_paf(a, k):
    re = im = 0
    for j, (x, y) in enumerate(a):
        u, v = a[(j+k) % len(a)]
        re += x*u+y*v
        im += y*u-x*v
    return re, im


def canonical(q):
    zero = [min(r, tuple(-x for x in r)) for r in q[:3]]
    return tuple(sorted(zero))+(q[3],)


def small_pairs(n, h):
    groups = []
    for total in (0, 2):
        group = []
        for negatives in combinations(range(n), (n-total)//2):
            negative = set(negatives)
            r = tuple(-1 if j in negative else 1 for j in range(n))
            if all(r[j] == r[h*j % n] for j in range(n)):
                group.append(r)
        groups.append(group)
    zero, special = groups
    # Ground truth is the literal Gaussian definition for the labelled pairs
    # A=G(q0,q1), B=G(q3,q2), not the real/skew matching formulation.
    actual = {}
    labelled = positives = real_only = 0
    for q in product(zero, zero, zero, special):
        labelled += 1
        a, b = gray(q[0], q[1]), gray(q[3], q[2])
        values = []
        for k in range(1, n):
            ar, ai = gaussian_paf(a, k)
            br, bi = gaussian_paf(b, k)
            values.append((ar+br, ai+bi))
        valid = all(v == (-2, 0) for v in values)
        positives += valid
        real_only += all(v[0] == -2 for v in values) and not valid
        c = canonical(q)
        actual[c] = actual.get(c, False) or valid
        # Independently validate the Gray identity at every lag, including 0.
        for k in range(n):
            re, im = gaussian_paf(a, k)
            require(2*re == corr(q[0], q[0], k)+corr(q[1], q[1], k), 'Gray real identity')
            require(2*im == corr(q[0], q[1], k)-corr(q[1], q[0], k), 'Gray skew identity')
    for q, exists in actual.items():
        real = all(sum(corr(r, r, k) for r in q) == -4 for k in range(1, n))
        matched = False
        if real:
            for mate in range(3):
                i, j = [r for r in range(3) if r != mate]
                left = tuple(corr(q[i], q[j], k)-corr(q[j], q[i], k) for k in range(1, n))
                right = tuple(corr(q[mate], q[3], k)-corr(q[3], q[mate], k) for k in range(1, n))
                matched |= left == right or left == tuple(-x for x in right)
        require(matched == exists, 'pairing/sign quotient disagrees with Gaussian definition')
    return dict(length=n, multiplier=h, zero_rows=len(zero), special_rows=len(special),
                labelled_quadruples=labelled, normalized_qlps=positives,
                real_only_non_qlps=real_only, canonical_quadruples=len(actual))


def orbits(n, permutation):
    unused = set(range(n))
    result = []
    while unused:
        start = min(unused)
        orbit = []
        j = start
        while j not in orbit:
            orbit.append(j)
            unused.remove(j)
            j = permutation[j]
        require(j == start, 'not a permutation cycle')
        result.append(orbit)
    return result


def structural():
    half_checks = 0
    for n in (4, 8):
        h, m = 1+n//2, n//2
        cycles = orbits(n, [h*j % n for j in range(n)])
        for values in product(((1, 0), (0, 1), (-1, 0), (0, -1)), repeat=len(cycles)):
            row = [None]*n
            for cycle, value in zip(cycles, values):
                for j in cycle:
                    row[j] = value
            lhs = gaussian_paf(row, m)
            rhs = sum((row[j][0]+row[j+m][0])**2+(row[j][1]+row[j+m][1])**2
                      for j in range(0, m, 2))
            require(lhs == (rhs, 0) and rhs >= 0, 'half-period positivity identity')
            half_checks += 1
    affine = fixed_point_free = 0
    for h in range(1, 64, 2):
        if h != 1:
            t = h
            while t*t % 64 != 1:
                t = t*t % 64
            require(t in (31, 33, 63), 'missing involution')
        for b in range(64):
            p = [(h*j+b) % 64 for j in range(64)]
            cycles = orbits(64, p)
            require(all(len(c) & (len(c)-1) == 0 for c in cycles), 'non-power-two affine cycle')
            fixed = [c[0] for c in cycles if len(c) == 1]
            if not fixed:
                require(all(len(c) % 2 == 0 for c in cycles), 'odd cycle without fixed point')
                fixed_point_free += 1
            else:
                origin = fixed[0]
                require(all((p[(j+origin) % 64]-origin) % 64 == h*j % 64 for j in range(64)),
                        'fixed-point conjugation failed')
            affine += 1
    return dict(half_period_words=half_checks, affine_maps=affine,
                fixed_point_free_affine_maps=fixed_point_free, nonidentity_units=31)


def main():
    cases = [small_pairs(n, h) for n, h in ((4, 1), (4, 3), (8, 3), (8, 7), (10, 9))]
    require(sum(c['normalized_qlps'] for c in cases) > 0, 'no positive controls')
    require(sum(c['real_only_non_qlps'] for c in cases) > 0, 'no skew-sensitive controls')
    print(json.dumps(dict(status='PASS', small_order=cases, structural=structural()), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
