#!/usr/bin/env python3
"""Exact hull, guard, common-neighbor, and parser controls."""

import itertools as it
import math
from fractions import Fraction as F

from check import hull_slacks, require, row_slacks


def reject(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError("corruption accepted")


def main():
    hull_vertices = guards = 0
    for c in range(9, 14):
        for dsum in range(40, 43):
            p = math.comb(41-c, 2)
            K = 64-c-dsum
            constant = 45-c-dsum
            for s in range(K+1):
                require(min(hull_slacks(c, dsum, p, s, math.comb(s, 2), 1, 1, 1)) >= 0,
                        "binomial hull vertex")
                hull_vertices += 1
            for s, q, (y, x) in it.product((constant, constant+c+39), (0, p),
                                           ((0, 0), (0, 1), (1, 0))):
                require(min(hull_slacks(c, dsum, p, s, q, y, x, 1)) >= 0,
                        "inactive box guard")
                guards += 1
    # The common-blue count identity on every pair of red-neighbor sets.
    identities = 0
    for n in range(7):
        all_bits = (1 << n)-1
        for a, b in it.product(range(1 << n), repeat=2):
            shared_red = (a & b).bit_count()
            shared_blue = ((a | b) ^ all_bits).bit_count()
            require(shared_blue == n-a.bit_count()-b.bit_count()+shared_red, "two-color identity")
            pair_count = sum(not ((a | b) >> i & 1) and not ((a | b) >> j & 1)
                             for i, j in it.combinations(range(n), 2))
            require(pair_count == math.comb(shared_blue, 2), "common-blue moment")
            identities += 1
    # Direct Fraction arithmetic independently checks the three-point parser.
    vector = [(0, 0, 0), (2, 3, 4), (5, 1, 3), (1, 2, 0)]
    rows = 0
    for coefficients in it.product(range(-2, 3), repeat=3):
        terms = " ".join(f"{c:+d} x{i}" for i, c in enumerate(coefficients, 1))
        expected = tuple(sum(F(c*vector[i][k], 6) for i, c in enumerate(coefficients, 1))
                         for k in range(3))
        relation, slacks = row_slacks((terms+" >= 0 ;").encode(), vector, 6)
        require(relation == b">=" and tuple(F(x, 6) for x in slacks) == expected, "row arithmetic")
        rows += 1
    malformed = [b"+1 x0 >= 0 ;", b"+1 x4 >= 0 ;", b"+1 y1 >= 0 ;",
                 b"+1 x1 >= 0", b"+1 x1 <= 0 ;", b"+1 x1 >= 0 ; extra"]
    for row in malformed:
        reject(lambda row=row: row_slacks(row, vector, 6))
    # Previous family cannot satisfy the new active chord at any allowed rho.
    require(2*78*F(3, 14) > 8, "old family separation")
    require(78*F(10, 39) == 20 and 7*F(3, 14) == F(3, 2), "new interval endpoints")
    print(f"PASS hull_vertices={hull_vertices} inactive_guards={guards} "
          f"identities={identities} row_comparisons={rows} malformed_rows={len(malformed)}")


if __name__ == "__main__":
    main()
