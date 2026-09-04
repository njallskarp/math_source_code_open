#!/usr/bin/env python3
"""Exact matrix audit for the D(a,3) interior matching sign rule.

The universal Fibonacci proof is in README.md.  This checker reconstructs the
matching matrices, the exact gap decomposition, its positive lower bound, and
the diagonal obstruction for every parameter tuple in a configurable range.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import gcd
from typing import Sequence

Matrix = tuple[tuple[int, int], tuple[int, int]]
Path = tuple[str, ...]


def fibonacci(index: int) -> int:
    if index == -1:
        return 1
    if index < -1:
        raise ValueError("Fibonacci index must be at least -1")
    older, old = 0, 1
    for _ in range(index):
        older, old = old, older + old
    return older


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def k_matrix(run: int) -> Matrix:
    if run < 0:
        raise ValueError("run length must be nonnegative")
    return (
        (fibonacci(2 * run + 3), fibonacci(2 * run + 1)),
        (fibonacci(2 * run + 1), fibonacci(2 * run - 1)),
    )


def q_score(runs: tuple[int, int, int]) -> int:
    product = matrix_multiply(
        matrix_multiply(k_matrix(runs[0]), k_matrix(runs[1])),
        k_matrix(runs[2]),
    )
    return product[1][0]


def continuant(digits: Sequence[int]) -> int:
    if not digits:
        return 1
    older, old = 1, digits[0]
    for digit in digits[1:]:
        older, old = old, digit * old + older
    return old


def coefficient_word(path: Sequence[str]) -> tuple[int, ...]:
    output: list[int] = []
    for left, right in zip(path, path[1:]):
        output.extend((1, 1) if left == right else (2,))
    return tuple(output)


def matching_number(path: Sequence[str]) -> int:
    return continuant(coefficient_word(path))


def named_paths(x: int, y: int, z: int) -> tuple[Path, Path]:
    p = tuple("R" * x + "U" + "R" * y + "U" + "R" * z + "U")
    q = tuple("R" * (x - 1) + "U" + "R" * z + "U" + "R" * (y + 1) + "U")
    return p, q


def is_rational_dyck(path: Sequence[str], a: int, b: int = 3) -> bool:
    right = up = 0
    for step in path:
        if step == "R":
            right += 1
        elif step == "U":
            up += 1
        else:
            return False
        if a * up > b * right:
            return False
    return right == a and up == b


def matching_gap_formula(x: int, y: int, z: int) -> int:
    d = x - y
    e = y - z
    return 2 * (
        fibonacci(2 * e + 2) * fibonacci(2 * x - 3)
        - fibonacci(2 * d - 4) * fibonacci(2 * z + 3)
        - fibonacci(2 * d - 2) * fibonacci(2 * z + 1)
    )


def positive_gap_lower_bound(x: int, y: int, z: int) -> int:
    if not z < y:
        raise ValueError("positive lower bound requires z<y")
    d = x - y
    return 2 * (
        5 * fibonacci(2 * z + 1) * fibonacci(2 * d - 3)
        + fibonacci(2 * z)
        * (3 * fibonacci(2 * d - 3) + 2 * fibonacci(2 * d - 4))
    )


def audit_transition(a: int, y: int, z: int) -> tuple[str, list[int]]:
    if gcd(a, 3) != 1 or y < 1 or z < 0 or z > y or a < 3 * y + 3:
        raise ValueError("requires gcd(a,3)=1, y>=1, 0<=z<=y, a>=3y+3")
    x = a - y - z
    d, e = x - y, y - z
    assert x >= y >= z
    assert d - e == a - 3 * y >= 3

    p, q = named_paths(x, y, z)
    assert is_rational_dyck(p, a)
    assert is_rational_dyck(q, a)
    matching_p, matching_q = matching_number(p), matching_number(q)
    assert matching_p == q_score((x, y, z))
    assert matching_q == q_score((x - 1, z, y + 1))

    canonical_lower = q_score((x - 1, y + 1, z))
    within_drop = 2 * (
        fibonacci(2 * d - 4) * fibonacci(2 * z + 3)
        + fibonacci(2 * d - 2) * fibonacci(2 * z + 1)
    )
    permutation_gain = 2 * fibonacci(2 * e + 2) * fibonacci(2 * x - 3)
    assert matching_p - canonical_lower == within_drop
    assert matching_q - canonical_lower == permutation_gain

    gap = matching_q - matching_p
    assert gap == matching_gap_formula(x, y, z)
    if e:
        first = (
            fibonacci(2 * e + 2) * fibonacci(2 * d + 2 * e - 3)
            - 2 * fibonacci(2 * d - 4)
            - fibonacci(2 * d - 2)
        )
        second = (
            fibonacci(2 * e + 2) * fibonacci(2 * d + 2 * e - 4)
            - fibonacci(2 * d - 4)
        )
        assert gap // 2 == fibonacci(2 * z + 1) * first + fibonacci(2 * z) * second
        assert first >= 5 * fibonacci(2 * d - 3)
        assert second >= 3 * fibonacci(2 * d - 3) + 2 * fibonacci(2 * d - 4)
        bound = positive_gap_lower_bound(x, y, z)
        assert gap >= bound > 0
        assert (gap == bound) == (e == 1)
        kind = "reversal"
    else:
        obstruction = -6 * fibonacci(2 * z + 1) * fibonacci(2 * d - 4)
        assert gap == obstruction < 0
        bound = obstruction
        kind = "diagonal"
    return kind, [a, x, y, z, matching_p, matching_q, gap, bound]


def audit(max_a: int) -> tuple[int, int, int, str]:
    if max_a < 7:
        raise ValueError("max_a must be at least 7")
    digest = hashlib.sha256()
    endpoints = reversals = diagonal = 0
    for a in range(7, max_a + 1):
        if gcd(a, 3) != 1:
            continue
        endpoint_has_transition = False
        for y in range(1, (a - 3) // 3 + 1):
            for z in range(y + 1):
                kind, row = audit_transition(a, y, z)
                digest.update(json.dumps(row, separators=(",", ":")).encode() + b"\n")
                reversals += kind == "reversal"
                diagonal += kind == "diagonal"
                endpoint_has_transition = True
        endpoints += endpoint_has_transition
    if not reversals or not diagonal:
        raise AssertionError("audit found no transitions")
    return endpoints, reversals, diagonal, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=150)
    args = parser.parse_args()
    endpoints, reversals, diagonal, digest = audit(args.max_a)
    print(
        "EXACT VERIFIED D(a,3) INTERIOR MATCHING SIGN RULE; "
        f"7<=a<={args.max_a}; endpoints={endpoints}; reversals={reversals}; "
        f"diagonal_obstructions={diagonal}; row_sha256={digest}"
    )


if __name__ == "__main__":
    main()
