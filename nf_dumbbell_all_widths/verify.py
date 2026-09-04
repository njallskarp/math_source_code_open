#!/usr/bin/env python3
"""Exact type checks for the complete dumbbell NF orbit formula."""

from __future__ import annotations

import argparse
import itertools
import sys
from collections.abc import Iterable

Type = tuple[int, int, int, int]
State = frozenset[Type]
Base = tuple[int, int, int]


def leq(left: Type, right: Type) -> bool:
    return all(x <= y for x, y in zip(left, right, strict=True))


def maximal(types: Iterable[Type], k: int) -> State:
    """Maximal types, using suffix maxima on the four base chains."""
    by_base: dict[Base, int] = {}
    for a, i, b, j in types:
        base = (a, i, b)
        by_base[base] = max(j, by_base.get(base, -1))
    if not by_base:
        return frozenset()

    suffix = {(a, b): [-1] * (k + 1) for a in (0, 1) for b in (0, 1)}
    for a in (0, 1):
        for b in (0, 1):
            for i in range(k - 1, -1, -1):
                suffix[a, b][i] = max(
                    by_base.get((a, i, b), -1), suffix[a, b][i + 1]
                )

    result: list[Type] = []
    for (a, i, b), j in by_base.items():
        strict_upper = suffix[a, b][i + 1]
        if a == 0:
            strict_upper = max(strict_upper, suffix[1, b][i])
        if b == 0:
            strict_upper = max(strict_upper, suffix[a, 1][i])
        if a == 0 and b == 0:
            strict_upper = max(strict_upper, suffix[1, 1][i])
        if strict_upper < j:
            result.append((a, i, b, j))
    return frozenset(result)


def clip(k: int, m: int, types: Iterable[Type]) -> State:
    """Discard out-of-box terms and restore maximality."""
    return maximal(
        (
            (a, i, b, j)
            for a, i, b, j in types
            if a in (0, 1) and 0 <= i < k and b in (0, 1) and 0 <= j < m
        ),
        k,
    )


def delta_types(facets: State, k: int, m: int) -> State:
    """Apply delta_NF in the lossless S_(k-1) x S_(m-1) quotient."""
    infinity = m + 1
    exact = {
        (a, i, b): infinity
        for a, i, b in itertools.product((0, 1), range(k), (0, 1))
    }
    for a, i, b, j in facets:
        exact[a, i, b] = min(exact[a, i, b], j)

    tops: list[Type] = []
    for a in (0, 1):
        for b in (0, 1):
            threshold = infinity
            for i in range(k):
                threshold = min(
                    threshold,
                    *(
                        exact[aa, i, bb]
                        for aa in range(a + 1)
                        for bb in range(b + 1)
                    ),
                )
                height = threshold - 1 if threshold != infinity else m - 1
                if height >= 0:
                    tops.append((a, i, b, height))
    return maximal(tops, k)


def initial_state(k: int, m: int) -> State:
    """Facet types of B_(k,m), with the distinguished bridge x_0 y_0."""
    if k < 3 or m < 3:
        raise ValueError("this formula requires k,m >= 3")
    return frozenset(
        {
            (0, 0, 0, 2),
            (0, 0, 1, 1),
            (0, 2, 0, 0),
            (1, 0, 1, 0),
            (1, 1, 0, 0),
        }
    )


def prefix_state(k: int, m: int, t: int) -> State:
    """The explicit prefix P_0,...,P_(k+2), assuming 3 <= k <= m."""
    q = m - 1
    if t == 0:
        return initial_state(k, m)
    if t == 1:
        return frozenset({(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1)})
    if t == 2:
        return frozenset({(0, 0, 1, q), (1, 0, 1, 0), (1, k - 1, 0, 0)})
    if t == 3:
        return frozenset(
            {(0, k - 1, 0, q), (0, k - 1, 1, q - 1), (1, k - 2, 0, q)}
        )
    if not 4 <= t <= k + 2:
        raise ValueError("prefix index must satisfy 0 <= t <= k+2")

    u = k - t + 4
    terms: list[Type] = []
    terms += [(0, i, 0, q - (i - u)) for i in range(max(0, u), k)]
    terms.append((0, u - 2, 1, q))
    terms += [(0, i, 1, q - (i - u + 1)) for i in range(max(0, u), k)]
    terms += [
        (1, i, 0, q - (i - u + 1))
        for i in range(max(0, u - 1), k - 1)
    ]
    terms.append((1, k - 1, 0, q - (t - 3)))
    terms += [
        (1, i, 1, q - (i - u + 3))
        for i in range(max(0, u - 3), k)
    ]
    return clip(k, m, terms)


def wave_weight(k: int, base: Base) -> int:
    a, i, b = base
    if a == 0 and b == 0:
        return k if i == 0 else k - i - 1
    if a == 0 and b == 1:
        return k - 1 if i == 0 else k - i - 2
    if a == 1 and b == 0:
        return -2 if i == k - 1 else k - i - 2
    return k - i - 4


def wave_state(k: int, m: int, s: int) -> State:
    q = m - 1
    if not 1 <= s <= q - k + 2:
        raise ValueError("wave index must satisfy 1 <= s <= q-k+2")
    return clip(
        k,
        m,
        (
            (a, i, b, s + wave_weight(k, (a, i, b)))
            for a, i, b in itertools.product((0, 1), range(k), (0, 1))
        ),
    )


def tail_state(k: int, m: int, r: int) -> State:
    """The explicit lower-bound tail R_r, for 1 <= r <= k-2."""
    if not 1 <= r <= k - 2:
        raise ValueError("tail index must satisfy 1 <= r <= k-2")
    terms: list[Type] = [(0, 0, 0, r + 2), (0, r + 2, 0, 0)]
    terms += [(0, i, 0, r + 1 - i) for i in range(1, r + 1)]
    terms.append((0, 0, 1, r + 1))
    terms += [(0, i, 1, r - i) for i in range(1, r + 1)]
    terms += [(1, i, 0, r - i) for i in range(r)]
    terms.append((1, r + 1, 0, 0))
    terms += [(1, i, 1, r - 2 - i) for i in range(r - 1)]
    return clip(k, m, terms)


def predicted_orbit(k: int, m: int) -> list[State]:
    if not 3 <= k <= m:
        raise ValueError("use clique symmetry to require 3 <= k <= m")
    q = m - 1
    result = [prefix_state(k, m, t) for t in range(k + 3)]
    result += [wave_state(k, m, s) for s in range(q - k + 2, 0, -1)]
    result += [tail_state(k, m, r) for r in range(k - 2, 0, -1)]
    return result


def verify_weight_monotonicity(max_k: int) -> None:
    for k in range(3, max_k + 1):
        bases = list(itertools.product((0, 1), range(k), (0, 1)))
        for left, right in itertools.permutations(bases, 2):
            if all(x <= y for x, y in zip(left, right, strict=True)):
                if wave_weight(k, left) <= wave_weight(k, right):
                    raise AssertionError(
                        f"k={k}: weight not strictly decreasing: {left} <= {right}"
                    )


def verify_grid(max_k: int, extra_m: int) -> tuple[int, int, int]:
    cases = states = transitions = 0
    for k in range(3, max_k + 1):
        for m in range(k, k + extra_m + 1):
            orbit = predicted_orbit(k, m)
            if len(orbit) != k + m + 2:
                raise AssertionError(f"k={k},m={m}: wrong length {len(orbit)}")
            if len(set(orbit)) != len(orbit):
                raise AssertionError(f"k={k},m={m}: premature labelled repetition")
            if any(sum(x) != 2 for x in orbit[0] | orbit[1]):
                raise AssertionError(f"k={k},m={m}: first states are not graphs")
            for t, state in enumerate(orbit[2:], start=2):
                if max(map(sum, state)) < 3:
                    raise AssertionError(f"k={k},m={m},t={t}: no large facet")
            for left, right in itertools.pairwise(orbit):
                if delta_types(left, k, m) != right:
                    raise AssertionError(f"k={k},m={m}: failed transition")
                transitions += 1
            if delta_types(orbit[-1], k, m) != orbit[0]:
                raise AssertionError(f"k={k},m={m}: orbit does not close")
            transitions += 1
            cases += 1
            states += len(orbit)
    return cases, states, transitions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=24)
    parser.add_argument("--extra-m", type=int, default=24)
    args = parser.parse_args()
    if args.max_k < 3:
        parser.error("--max-k must be at least 3")
    if args.extra_m < 0:
        parser.error("--extra-m must be nonnegative")
    verify_weight_monotonicity(args.max_k)
    cases, states, transitions = verify_grid(args.max_k, args.extra_m)
    print(
        "VERIFIED universal dumbbell orbit templates; "
        f"3<=k<={args.max_k}; k<=m<=k+{args.extra_m}; "
        f"cases={cases}; states={states}; transitions={transitions}; "
        "NF(B_(k,m))=k+m+2"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
