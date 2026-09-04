#!/usr/bin/env python3
"""Clean-room audit of the interior D(a,3) reversal family.

This file intentionally imports no contributor module.  It enumerates D(a,3)
by its three horizontal run lengths, evaluates finite continued fractions by
literal 2-by-2 products, and evaluates each periodic Lagrange score by the
fixed-point discriminants of every cyclic product.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import gcd

Matrix = tuple[tuple[int, int], tuple[int, int]]
Triple = tuple[int, int, int]

IDENTITY: Matrix = ((1, 0), (0, 1))


def multiply(left: Matrix, right: Matrix) -> Matrix:
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


def digit_matrix(digit: int) -> Matrix:
    if digit not in (1, 2):
        raise ValueError("continued-fraction digits must be 1 or 2")
    return ((digit, 1), (1, 0))


def run_word(runs: Triple) -> str:
    r, s, t = runs
    if min(runs) < 0:
        raise ValueError("run lengths must be nonnegative")
    return "R" * r + "U" + "R" * s + "U" + "R" * t + "U"


def coefficient_digits(runs: Triple) -> tuple[int, ...]:
    word = run_word(runs)
    digits: list[int] = []
    for left, right in zip(word, word[1:]):
        digits.extend((1, 1) if left == right else (2,))
    return tuple(digits)


def product(matrices: tuple[Matrix, ...]) -> Matrix:
    answer = IDENTITY
    for matrix in matrices:
        answer = multiply(answer, matrix)
    return answer


def matching_number(runs: Triple) -> int:
    """Numerator of the finite continued fraction attached to the path."""
    matrices = tuple(digit_matrix(digit) for digit in coefficient_digits(runs))
    return product(matrices)[0][0]


def lagrange_square(runs: Triple) -> Fraction:
    """Maximum squared fixed-point gap over every cyclic period shift."""
    period = (2,) + coefficient_digits(runs)
    matrices = tuple(digit_matrix(digit) for digit in period)
    count = len(matrices)

    prefixes: list[Matrix] = [IDENTITY]
    for matrix in matrices:
        prefixes.append(multiply(prefixes[-1], matrix))
    suffixes: list[Matrix] = [IDENTITY] * (count + 1)
    for index in range(count - 1, -1, -1):
        suffixes[index] = multiply(matrices[index], suffixes[index + 1])

    candidates: list[Fraction] = []
    for index in range(count):
        # Product for the rotation M_i ... M_(n-1) M_0 ... M_(i-1).
        a, b, c, d = (
            value
            for row in multiply(suffixes[index], prefixes[index])
            for value in row
        )
        if c == 0:
            raise AssertionError("positive period unexpectedly has C=0")
        discriminant = (a - d) * (a - d) + 4 * b * c
        candidates.append(Fraction(discriminant, c * c))
    return max(candidates)


def fibonacci(index: int) -> int:
    if index < 0:
        raise ValueError("this audit only uses nonnegative Fibonacci indices")
    older, old = 0, 1
    for _ in range(index):
        older, old = old, older + old
    return older


def target_gap_formula(x: int, y: int, z: int) -> int:
    d = x - y
    e = y - z
    return 2 * (
        fibonacci(2 * e + 2) * fibonacci(2 * x - 3)
        - fibonacci(2 * d - 4) * fibonacci(2 * z + 3)
        - fibonacci(2 * d - 2) * fibonacci(2 * z + 1)
    )


def carrier(a: int) -> list[Triple]:
    """All D(a,3) paths, via their unique R^r U R^s U R^t U form."""
    if a < 1:
        raise ValueError("a must be positive")
    paths: list[Triple] = []
    for r in range(a + 1):
        for s in range(a - r + 1):
            t = a - r - s
            if 3 * r >= a and 3 * (r + s) >= 2 * a:
                paths.append((r, s, t))
    return paths


def audit_endpoint(a: int) -> tuple[int, int, int, list[list[int]]]:
    if a < 7 or gcd(a, 3) != 1:
        raise ValueError("target scope requires a>=7 and gcd(a,3)=1")

    paths = carrier(a)
    scores = {runs: lagrange_square(runs) for runs in paths}
    matchings = {runs: matching_number(runs) for runs in paths}
    levels = sorted(set(scores.values()), reverse=True)
    level_index = {score: index for index, score in enumerate(levels)}

    rows: list[list[int]] = []
    reversal_count = diagonal_count = 0
    n = (a - 3) // 3
    for y in range(1, n + 1):
        for z in range(y + 1):
            x = a - y - z
            upper = (x, y, z)
            lower = (x - 1, z, y + 1)
            if upper not in scores or lower not in scores:
                raise AssertionError("named path is not rational-Dyck")
            if level_index[scores[lower]] != level_index[scores[upper]] + 1:
                raise AssertionError("named pair is not a Lagrange cover")

            gap = matchings[lower] - matchings[upper]
            if gap != target_gap_formula(x, y, z):
                raise AssertionError("matching gap formula mismatch")
            if z < y:
                if gap <= 0:
                    raise AssertionError("off-diagonal pair is not reversed")
                reversal_count += 1
            else:
                diagonal_formula = -6 * fibonacci(2 * z + 1) * fibonacci(2 * (x - y) - 4)
                if gap != diagonal_formula or gap >= 0:
                    raise AssertionError("diagonal sign formula mismatch")
                diagonal_count += 1

            rows.append(
                [
                    a,
                    x,
                    y,
                    z,
                    level_index[scores[upper]],
                    level_index[scores[lower]],
                    matchings[upper],
                    matchings[lower],
                    gap,
                    scores[upper].numerator,
                    scores[upper].denominator,
                    scores[lower].numerator,
                    scores[lower].denominator,
                ]
            )

    if reversal_count != n * (n + 1) // 2 or diagonal_count != n:
        raise AssertionError("per-endpoint count formula mismatch")
    return len(paths), reversal_count, diagonal_count, rows


def audit(max_a: int) -> tuple[int, int, int, int, str]:
    if max_a < 7:
        raise ValueError("max_a must be at least 7")
    digest = hashlib.sha256()
    endpoints = path_count = reversals = diagonal = 0
    for a in range(7, max_a + 1):
        if gcd(a, 3) != 1:
            continue
        count, endpoint_reversals, endpoint_diagonal, rows = audit_endpoint(a)
        endpoints += 1
        path_count += count
        reversals += endpoint_reversals
        diagonal += endpoint_diagonal
        for row in rows:
            digest.update(json.dumps(row, separators=(",", ":")).encode() + b"\n")
    return endpoints, path_count, reversals, diagonal, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=90)
    args = parser.parse_args()
    endpoints, paths, reversals, diagonal, digest = audit(args.max_a)
    print("CLEAN-ROOM MATRIX AUDIT PASSED")
    print(f"range=7..{args.max_a}")
    print(f"coprime_endpoints={endpoints}")
    print(f"carrier_paths={paths}")
    print(f"off_diagonal_reversals={reversals}")
    print(f"diagonal_agreements={diagonal}")
    print(f"row_sha256={digest}")


if __name__ == "__main__":
    main()
