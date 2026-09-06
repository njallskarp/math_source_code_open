"""Exact, offline audit of the small height-2713 attainment counterexample.

Python 3.12+; standard library. All-chord minimization replaces the upstream
hull-stack construction. A fixed-length dynamic program then minimizes the
integer population cost. Neither computation proves a crossing inequality.
"""
from fractions import Fraction
from hashlib import sha256
from json import dumps
from math import ceil, comb


def base(n, q):
    """Transcription of the source's stated base formulas, not their proofs."""
    caps = (3*n-6, 4*n-8, 5*n-10, (11*n-23)//2, 6*n-12)
    return max(0, q-3*n+6,
               ceil(Fraction(sum(max(0, q-e) for e in caps), 2)),
               ceil(Fraction(45*q-203*(n-2), 9)),
               ceil(Fraction(37*q-155*(n-2), 9)))


def all_chords(row, x):
    """Minimize over all one/two-support real mixtures of the integer entries."""
    assert 0 <= x <= len(row)-1
    costs = [Fraction(row[a]) for a in range(len(row)) if a == x]
    costs.extend(row[a] + Fraction(row[b]-row[a], b-a)*(x-a)
                 for a in range(len(row)) for b in range(a+1, len(row))
                 if a <= x <= b)
    return min(costs)


def small_rows():
    rows = {}
    for n in range(3, 8):
        rows[n] = [max([base(n, q)] + [
            ceil(comb(n, s) * all_chords(
                rows[s], Fraction(q*comb(n-2, s-2), comb(n, s)))
                 / comb(n-4, s-4)) for s in range(4, n)])
            for q in range(comb(n, 2)+1)]
    return rows


def discrete_minimum(row, population, total):
    """Exact DP: state is (number of entries, sum), value is minimum cost.

    Every next entry in the complete domain is tried. Pruning above the target
    total is sound here because all allowed entries are nonnegative.
    """
    assert population >= 0 and total >= 0 and row
    costs = {0: 0}
    for _ in range(population):
        following = {}
        for t, cost in costs.items():
            for x, value in enumerate(row):
                if t+x <= total:
                    new = cost+value
                    if t+x not in following or new < following[t+x]:
                        following[t+x] = new
        costs = following
    return costs.get(total)


def main():
    rows = small_rows()
    expected = {3: [0]*4, 4: [0]*7, 5: [0]*10+[1],
                6: [0]*13+[1, 2, 3], 7: [0]*16+[1, 2, 3, 4, 6, 7]}
    assert rows == expected  # all 60 entries, not only an aggregate
    digest = sha256(dumps(rows, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert digest == 'e6dc4b1e50a339c8bad85dd01959946ae7acbd687f24d2a85fbd679da3eb1013'
    row = rows[7]
    n, s, q = 9, 7, 33
    N, T, survival = comb(n, s), q*comb(n-2, s-2), comb(n-4, s-4)
    assert (N, T, survival) == (36, 693, 10)
    slope, intercept = Fraction(3, 2), Fraction(-49, 2)
    assert all(slope*x+intercept <= row[x] for x in range(22))
    assert [x for x in range(22) if slope*x+intercept == row[x]] == [19, 21]
    relaxed = N*all_chords(row, Fraction(T, N))
    assert relaxed == Fraction(315, 2)
    assert Fraction(T-N*19, 21-19) == Fraction(9, 2)
    minimum = discrete_minimum(row, N, T)
    witness = [21]*4 + [20] + [19]*31
    assert len(witness) == N and sum(witness) == T
    assert sum(row[x] for x in witness) == minimum == 158
    assert ceil(relaxed/survival) == ceil(Fraction(minimum, survival)) == 16
    # Degenerate/infeasible DP states and a toy nonconvex table.
    assert discrete_minimum([0, 2, 2], 0, 0) == 0
    assert discrete_minimum([0, 2, 2], 0, 1) is None
    assert discrete_minimum([0, 2, 2], 1, 1) == 2
    assert all_chords([0, 2, 2], Fraction(1)) == 1
    assert discrete_minimum([0, 2, 2], 2, 5) is None
    print('rows_3_to_7_entries=60; exact_match=True')
    print('rows_sha256='+digest)
    print('n=9; s=7; q=33; population=36; total=693; survival=10')
    print('contacts=19,21; upper_multiplicity=9/2')
    print('relaxed=315/2; integer_minimum=158; witness=31*19+1*20+4*21')
    print('rounded_crossing_bound_before=16; after=16')
    print('verdict=ATTAINMENT_CLAIM_FALSE_LOWER_BOUND_UNAFFECTED')


if __name__ == '__main__':
    main()
