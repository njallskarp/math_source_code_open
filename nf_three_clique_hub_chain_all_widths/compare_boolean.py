#!/usr/bin/env python3
"""Expand type classes and compare them entry-for-entry with Boolean replay."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json

import independent_check
import verify


def choices_mask(vertices: range, count: int) -> list[int]:
    return [sum(1 << vertex for vertex in chosen) for chosen in itertools.combinations(vertices, count)]


def expand_type(type_: verify.Type, n: int, m: int, ell: int) -> set[int]:
    a, i, b, j, c, k = type_
    result: set[int] = set()
    for left, middle, right in itertools.product(
        choices_mask(range(1, n), i),
        choices_mask(range(n + 1, n + m), j),
        choices_mask(range(n + m + 1, n + m + ell), k),
    ):
        hubs = (a << 0) | (b << n) | (c << (n + m))
        result.add(hubs | left | middle | right)
    return result


def expand_state(state: verify.State, n: int, m: int, ell: int) -> frozenset[int]:
    answer: set[int] = set()
    for type_ in state:
        answer.update(expand_type(type_, n, m, ell))
    return frozenset(answer)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", nargs="*", default=["3,3,3", "3,3,4"])
    args = parser.parse_args()
    parsed = [tuple(map(int, item.split(","))) for item in args.cases]
    records = []
    facets = states = 0
    for dims in parsed:
        if len(dims) != 3 or min(dims) < 3:
            raise SystemExit("each case must be n,m,ell with all widths at least 3")
        predicted = [expand_state(state, *dims) for state in verify.predicted_orbit(*dims)]
        direct = independent_check.orbit(*dims)
        if predicted != direct:
            raise AssertionError(f"expanded type orbit mismatch for {dims}")
        records.append([[mask for mask in sorted(state)] for state in predicted])
        states += len(predicted)
        facets += sum(map(len, predicted))
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    print(
        "MATCHED all-width type recurrence and Boolean facets entry-for-entry; "
        f"cases={len(parsed)}; states={states}; facets={facets}"
    )
    print(f"EXPANDED_ORBIT_SHA256={digest}")


if __name__ == "__main__":
    main()
