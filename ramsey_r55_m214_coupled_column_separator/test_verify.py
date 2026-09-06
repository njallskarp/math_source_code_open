#!/usr/bin/env python3
"""Small definition-level controls and deliberate certificate rejection."""

import itertools as it
import math
from collections import Counter
from fractions import Fraction as F

import verify


def reject(call):
    try:
        call()
    except (ValueError, ZeroDivisionError):
        return
    raise ValueError("corruption accepted")


def main():
    # Direct subset incidence checks of the new rational pair moments.
    subset_count = 0
    for n, k, first, second in [(13, 7, F(7, 13), F(7, 26)),
                                (15, 6, F(2, 5), F(1, 7))]:
        single, pair = Counter(), Counter()
        for subset in it.combinations(range(n), k):
            single.update(subset)
            pair.update(it.combinations(subset, 2))
            subset_count += 1
        count = math.comb(n, k)
        verify.require(all(F(single[v], count) == first for v in range(n)), "first moments")
        verify.require(all(F(pair[p], count) == second for p in it.combinations(range(n), 2)),
                       "second moments")
    verify.require(F(7, 13)*F(2, 5) == F(14, 65), "mixed moment")

    # Independent literal pair counting for the q-to-binomial identity.
    identities = 0
    for n in range(7):
        for a in range(1 << n):
            for b in range(1 << n):
                common = [v for v in range(n) if (a >> v) & (b >> v) & 1]
                direct = sum(((a >> i) & (a >> j) & (b >> i) & (b >> j) & 1)
                             for i, j in it.combinations(range(n), 2))
                verify.require(direct == math.comb(len(common), 2), "q identity")
                identities += 1

    # Integer-scaled evaluator versus Fraction evaluation on mixed-sign rows.
    lo, delta, denominator = [0, 2, 3, 5], [0, 1, -2, 0], 6
    checked = 0
    for coefficients in it.product(range(-2, 3), repeat=3):
        sums = [sum(F(c*(lo[i]+t*delta[i]), denominator)
                    for i, c in enumerate(coefficients, 1)) for t in (0, 1)]
        rhs = min(sums).__floor__()
        terms = " ".join(f"{c:+d} x{i}" for i, c in enumerate(coefficients, 1))
        verify.evaluate_row(f"{terms} >= {rhs} ;".encode(), lo, delta, denominator)
        reject(lambda: verify.evaluate_row(f"{terms} >= {rhs+1} ;".encode(),
                                           lo, delta, denominator))
        checked += 1
    malformed = [b"+1 x0 >= 0 ;", b"+1 x4 >= 0 ;", b"+1 y1 >= 0 ;",
                 b"+1 x1 >= 0", b"+1 x1 <= 0 ;", b"+1 x1 = 0 ;",
                 b"+1 x1 >= 1 ;", b"+1 x1 >= 0 ; extra"]
    for row in malformed:
        reject(lambda row=row: verify.evaluate_row(row, lo, delta, denominator))
    print(f"PASS subsets={subset_count} identities={identities} "
          f"fraction_comparisons={checked} rejected_rows={checked+len(malformed)}")


if __name__ == "__main__":
    main()
