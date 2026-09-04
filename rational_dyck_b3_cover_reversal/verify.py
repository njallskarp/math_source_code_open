#!/usr/bin/env python3
"""Exact matrix audit for a two-parameter D(a,3) cover-reversal family.

The universal argument is written in README.md.  This standard-library checker
reconstructs every displayed matching-score identity with integer matrices and
checks the family over a configurable finite range.  It does not evaluate
Lagrange scores; independent_check.py does that directly from definitions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import gcd
from typing import Iterable, Sequence

Matrix = tuple[tuple[int, int], tuple[int, int]]
Path = tuple[str, ...]


def fibonacci(index: int) -> int:
    """Return F_index for index >= -1, using F_-1=1."""
    if index == -1:
        return 1
    if index < -1:
        raise ValueError("Fibonacci index must be at least -1")
    previous, current = 0, 1
    for _ in range(index):
        previous, current = current, previous + current
    return previous


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
    previous2, previous1 = 1, digits[0]
    for digit in digits[1:]:
        previous2, previous1 = previous1, digit * previous1 + previous2
    return previous1


def coefficient_word(path: Sequence[str]) -> tuple[int, ...]:
    output: list[int] = []
    for left, right in zip(path, path[1:]):
        output.extend((1, 1) if left == right else (2,))
    return tuple(output)


def matching_number(path: Sequence[str]) -> int:
    return continuant(coefficient_word(path))


def path_p(x: int, y: int) -> Path:
    return tuple("R" * x + "U" + "R" * y + "UU")


def path_q(x: int, y: int) -> Path:
    return tuple("R" * (x - 1) + "UU" + "R" * (y + 1) + "U")


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


def family_parameters(max_x: int, coprime_only: bool = True) -> Iterable[tuple[int, int]]:
    for y in range(1, max_x + 1):
        for x in range(2 * y + 3, max_x + 1):
            if not coprime_only or gcd(x + y, 3) == 1:
                yield x, y


def matching_gap_formula(x: int, y: int) -> int:
    d = x - y
    return 2 * (
        fibonacci(2 * y + 2) * fibonacci(2 * x - 3)
        - 2 * fibonacci(2 * d - 4)
        - fibonacci(2 * d - 2)
    )


def matching_gap_lower_bound(x: int, y: int) -> int:
    return 10 * fibonacci(2 * (x - y) - 3)


def audit_pair(x: int, y: int) -> list[int]:
    if y < 1 or x < 2 * y + 3:
        raise ValueError("family requires y>=1 and x>=2y+3")
    a = x + y
    p, q = path_p(x, y), path_q(x, y)
    assert is_rational_dyck(p, a)
    assert is_rational_dyck(q, a)

    matching_p = matching_number(p)
    matching_q = matching_number(q)
    assert matching_p == q_score((x, y, 0))
    assert matching_q == q_score((x - 1, 0, y + 1))

    canonical_lower = q_score((x - 1, y + 1, 0))
    d = x - y
    within_drop = 2 * (
        2 * fibonacci(2 * d - 4) + fibonacci(2 * d - 2)
    )
    permutation_gain = 2 * fibonacci(2 * y + 2) * fibonacci(2 * x - 3)
    assert matching_p - canonical_lower == within_drop
    assert matching_q - canonical_lower == permutation_gain

    gap = matching_q - matching_p
    formula = matching_gap_formula(x, y)
    lower_bound = matching_gap_lower_bound(x, y)
    assert gap == formula
    assert gap >= lower_bound > 0
    assert (gap == lower_bound) == (y == 1)
    return [x, y, a, matching_p, matching_q, gap, lower_bound]


def audit(max_x: int) -> tuple[int, int, str]:
    if max_x < 5:
        raise ValueError("max_x must be at least 5")
    rows = [audit_pair(x, y) for x, y in family_parameters(max_x)]
    if not rows:
        raise AssertionError("finite audit unexpectedly found no family members")
    payload = (json.dumps(rows, separators=(",", ":")) + "\n").encode()
    noncoatom = sum(y >= 2 for _, y in family_parameters(max_x))
    return len(rows), noncoatom, hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-x", type=int, default=250)
    args = parser.parse_args()
    count, noncoatom, digest = audit(args.max_x)
    print(
        "EXACT VERIFIED D(a,3) LAGRANGE-COVER MATCHING REVERSALS; "
        f"x<={args.max_x}; pairs={count}; noncoatom_pairs={noncoatom}; "
        f"row_sha256={digest}"
    )


if __name__ == "__main__":
    main()
