#!/usr/bin/env python3
"""Entry-level bridge between the type certificate and Boolean NF replay."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys

import independent_check
import verify


def subset_masks(vertices: tuple[int, ...], count: int) -> list[int]:
    return [
        sum(1 << vertex for vertex in choice)
        for choice in itertools.combinations(vertices, count)
    ]


def expand_type(type_: verify.Type, m: int) -> set[int]:
    a, i, b, j, c, k = type_
    factors = (
        (1 << 0,) if a else (0,),
        subset_masks((1, 2), i),
        (1 << 3,) if b else (0,),
        subset_masks(tuple(range(4, m + 3)), j),
        (1 << (m + 3),) if c else (0,),
        subset_masks((m + 4, m + 5), k),
    )
    return {sum(parts) for parts in itertools.product(*factors)}


def expand_state(state: verify.State, m: int) -> frozenset[int]:
    result: set[int] = set()
    for type_ in state:
        orbit = expand_type(type_, m)
        if result.intersection(orbit):
            raise AssertionError(f"overlapping type orbits at m={m}, type={type_}")
        result.update(orbit)
    return frozenset(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=6)
    args = parser.parse_args()
    if not 3 <= args.max_m <= 7:
        parser.error("the Boolean comparison supports 3 <= --max-m <= 7")

    cases = states = facets = 0
    record: list[tuple[int, list[list[int]]]] = []
    for m in range(3, args.max_m + 1):
        predicted = verify.predicted_orbit(m - 1)
        direct = independent_check.labelled_orbit(m)
        if len(predicted) != len(direct):
            raise AssertionError(f"m={m}: orbit lengths differ")
        expanded: list[frozenset[int]] = []
        for step, (type_state, boolean_state) in enumerate(zip(predicted, direct)):
            expanded_state = expand_state(type_state, m)
            if expanded_state != boolean_state:
                raise AssertionError(f"m={m}, step={step}: facet entries differ")
            expanded.append(expanded_state)
            states += 1
            facets += len(expanded_state)
        cases += 1
        record.append((m, [sorted(state) for state in expanded]))

    digest = hashlib.sha256(
        json.dumps(record, separators=(",", ":")).encode()
    ).hexdigest()
    print(
        "MATCHED type and Boolean facets entry-for-entry; "
        f"m=3..{args.max_m}; cases={cases}; states={states}; facets={facets}"
    )
    print(f"EXPANDED_ORBIT_SHA256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
