#!/usr/bin/env python3
"""Compare the published all-width templates to the independent width-five orbit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections.abc import Iterable

import verify as fixed

Type = tuple[int, int, int, int]
State = frozenset[Type]


def leq(left: Type, right: Type) -> bool:
    return all(x <= y for x, y in zip(left, right, strict=True))


def maximal(types: Iterable[Type]) -> State:
    candidates = frozenset(types)
    return frozenset(
        item
        for item in candidates
        if not any(item != other and leq(item, other) for other in candidates)
    )


def clip(k: int, m: int, types: Iterable[Type]) -> State:
    return maximal(
        (a, i, b, j)
        for a, i, b, j in types
        if a in (0, 1) and 0 <= i < k and b in (0, 1) and 0 <= j < m
    )


def published_prefix(k: int, m: int, t: int) -> State:
    q = m - 1
    if t == 0:
        return frozenset(
            {(0, 0, 0, 2), (0, 0, 1, 1), (0, 2, 0, 0),
             (1, 0, 1, 0), (1, 1, 0, 0)}
        )
    if t == 1:
        return frozenset({(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1)})
    if t == 2:
        return frozenset({(0, 0, 1, q), (1, 0, 1, 0), (1, k - 1, 0, 0)})
    if t == 3:
        return frozenset(
            {(0, k - 1, 0, q), (0, k - 1, 1, q - 1), (1, k - 2, 0, q)}
        )
    u = k - t + 4
    terms: list[Type] = []
    terms += [(0, i, 0, q - (i - u)) for i in range(u, k)]
    terms.append((0, u - 2, 1, q))
    terms += [(0, i, 1, q - (i - u + 1)) for i in range(u, k)]
    terms += [(1, i, 0, q - (i - u + 1)) for i in range(u - 1, k - 1)]
    terms.append((1, k - 1, 0, q - (t - 3)))
    terms += [(1, i, 1, q - (i - u + 3)) for i in range(u - 3, k)]
    return clip(k, m, terms)


def published_weight(k: int, a: int, i: int, b: int) -> int:
    if a == 0 and b == 0:
        return k if i == 0 else k - i - 1
    if a == 0 and b == 1:
        return k - 1 if i == 0 else k - i - 2
    if a == 1 and b == 0:
        return -2 if i == k - 1 else k - i - 2
    return k - i - 4


def published_wave(k: int, m: int, s: int) -> State:
    return clip(
        k,
        m,
        (
            (a, i, b, s + published_weight(k, a, i, b))
            for a, i, b in itertools.product((0, 1), range(k), (0, 1))
        ),
    )


def published_tail(k: int, m: int, r: int) -> State:
    terms: list[Type] = [(0, 0, 0, r + 2), (0, r + 2, 0, 0)]
    terms += [(0, i, 0, r + 1 - i) for i in range(1, r + 1)]
    terms.append((0, 0, 1, r + 1))
    terms += [(0, i, 1, r - i) for i in range(1, r + 1)]
    terms += [(1, i, 0, r - i) for i in range(r)]
    terms.append((1, r + 1, 0, 0))
    terms += [(1, i, 1, r - 2 - i) for i in range(r - 1)]
    return clip(k, m, terms)


def published_orbit(k: int, m: int) -> list[State]:
    q = m - 1
    result = [published_prefix(k, m, t) for t in range(k + 3)]
    result.extend(published_wave(k, m, s) for s in range(q - k + 2, 0, -1))
    result.extend(published_tail(k, m, r) for r in range(k - 2, 0, -1))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=200)
    args = parser.parse_args()
    if args.max_m < 5:
        parser.error("--max-m must be at least 5")
    record: list[tuple[int, list[list[Type]]]] = []
    cases = states = 0
    for m in range(5, args.max_m + 1):
        expected = fixed.predicted_orbit(m)
        actual = published_orbit(5, m)
        if actual != expected:
            raise AssertionError(f"B_(5,{m}): target specialization differs")
        record.append((m, [sorted(current) for current in actual]))
        cases += 1
        states += len(actual)
    digest = hashlib.sha256(
        json.dumps(record, separators=(",", ":")).encode()
    ).hexdigest()
    print(
        "EXACT SPECIALIZATION MATCH "
        f"B_(5,m), m=5..{args.max_m}; cases={cases}; states={states}"
    )
    print(f"MATCH_SHA256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
