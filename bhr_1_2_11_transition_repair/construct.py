#!/usr/bin/env python3
"""Explicit constructors for the repaired BHR {1,2,11}, c=4 orthant."""

from __future__ import annotations

import argparse
import json

BOUNDARY_SEED = [
    19, 21, 10, 8, 6, 17, 15, 13, 11, 9, 7, 18, 16, 14, 12, 1, 3, 5,
    4, 2, 0, 20,
]


def interior_path(p: int, q: int) -> list[int]:
    """Return P[p,q], realizing {1^(2+p),2^(18+2q),11^4}."""
    if p < 0 or q < 0:
        raise ValueError("p and q must be nonnegative")
    return (
        [20 + p + 2 * q]
        + list(range(18 + p + 2 * q, 18 + p - 1, -2))
        + list(range(17 + p, 17, -1))
        + [16, 5, 7, 9, 11, 13, 12, 10, 8]
        + [22 + p + 2 * q, 24 + p + 2 * q]
        + [1, 3, 14, 15, 17, 6, 4, 2, 0]
        + [23 + p + 2 * q, 21 + p + 2 * q]
        + list(range(19 + p + 2 * q, 19 + p - 1, -2))
    )


def boundary_one_path(p: int) -> list[int]:
    """Return the b=16 ray after p repetitions of 1-growth at cut 0."""
    if p < 0:
        raise ValueError("p must be nonnegative")
    out: list[int] = []
    i = 0
    while i < len(BOUNDARY_SEED):
        if BOUNDARY_SEED[i : i + 2] == [2, 0]:
            out.append(2 + p)
            out.extend(range(p, -1, -1))
            i += 2
        else:
            y = BOUNDARY_SEED[i]
            out.append(0 if y == 0 else y + p)
            i += 1
    return out


def boundary_two_path(q: int) -> list[int]:
    """Return the a=1 ray after q repetitions of 2-growth at cut 1."""
    if q < 0:
        raise ValueError("q must be nonnegative")
    out: list[int] = []
    i = 0
    while i < len(BOUNDARY_SEED):
        pair = BOUNDARY_SEED[i : i + 2]
        if pair == [1, 3]:
            out.append(1)
            out.extend(range(3, 3 + 2 * q + 1, 2))
            i += 2
        elif pair == [2, 0]:
            out.append(2 + 2 * q)
            out.extend(range(2 * q, -1, -2))
            i += 2
        else:
            y = BOUNDARY_SEED[i]
            out.append(y if y <= 1 else y + 2 * q)
            i += 1
    return out


def construct(a: int, b: int, c: int) -> tuple[str, list[int]]:
    """Construct exactly the orthant a>=1, even b>=16, c=4."""
    if c != 4 or a < 1 or b < 16 or b % 2:
        raise ValueError("this construction requires a>=1, even b>=16, and c=4")
    if a == 1:
        return "boundary-two", boundary_two_path((b - 16) // 2)
    if b == 16:
        return "boundary-one", boundary_one_path(a - 1)
    return "interior", interior_path(a - 2, (b - 18) // 2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--b", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    args = parser.parse_args()
    family, path = construct(args.a, args.b, args.c)
    print(
        json.dumps(
            {"counts": [args.a, args.b, args.c], "family": family, "path": path},
            separators=(",", ":"),
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

