#!/usr/bin/env python3
"""Definition-level audit of the D(a,3) interior matching sign rule.

This program imports no contributor module.  It generates every carrier word,
uses scalar continuants for matching scores, evaluates exact squared Lagrange
scores at every cyclic cut, and checks cover adjacency against all score levels.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import gcd

Path = tuple[str, ...]


def continuant(digits: tuple[int, ...]) -> int:
    if not digits:
        return 1
    older, old = 1, digits[0]
    for digit in digits[1:]:
        older, old = old, digit * old + older
    return old


def coefficient_word(path: Path) -> tuple[int, ...]:
    digits: list[int] = []
    for left, right in zip(path, path[1:]):
        digits.extend((1, 1) if left == right else (2,))
    return tuple(digits)


def matching_number(path: Path) -> int:
    return continuant(coefficient_word(path))


def lagrange_square(path: Path) -> Fraction:
    period = (2,) + coefficient_word(path)
    trace = continuant(period) + continuant(period[1:-1])
    denominators = [
        continuant((period[index:] + period[:index])[1:])
        for index in range(len(period))
    ]
    return Fraction(trace * trace - 4, min(denominators) ** 2)


def fibonacci(index: int) -> int:
    older, old = 0, 1
    for _ in range(index):
        older, old = old, older + old
    return older


def carrier_paths(a: int) -> list[Path]:
    output: list[Path] = []

    def visit(right: int, up: int, prefix: list[str]) -> None:
        if right == a and up == 3:
            output.append(tuple(prefix))
            return
        if right < a:
            prefix.append("R")
            visit(right + 1, up, prefix)
            prefix.pop()
        if up < 3 and a * (up + 1) <= 3 * right:
            prefix.append("U")
            visit(right, up + 1, prefix)
            prefix.pop()

    visit(0, 0, [])
    return output


def named_paths(x: int, y: int, z: int) -> tuple[Path, Path]:
    p = tuple("R" * x + "U" + "R" * y + "U" + "R" * z + "U")
    q = tuple("R" * (x - 1) + "U" + "R" * z + "U" + "R" * (y + 1) + "U")
    return p, q


def check_endpoint(a: int) -> tuple[int, int, int, list[list[int]]]:
    carrier = carrier_paths(a)
    matching = {path: matching_number(path) for path in carrier}
    lagrange = {path: lagrange_square(path) for path in carrier}
    levels = sorted(set(lagrange.values()), reverse=True)
    level_index = {score: index for index, score in enumerate(levels)}
    rows: list[list[int]] = []
    reversals = diagonal = 0

    for y in range(1, (a - 3) // 3 + 1):
        for z in range(y + 1):
            x = a - y - z
            p, q = named_paths(x, y, z)
            assert p in lagrange and q in lagrange
            assert level_index[lagrange[q]] == level_index[lagrange[p]] + 1

            d, e = x - y, y - z
            formula = 2 * (
                fibonacci(2 * e + 2) * fibonacci(2 * x - 3)
                - fibonacci(2 * d - 4) * fibonacci(2 * z + 3)
                - fibonacci(2 * d - 2) * fibonacci(2 * z + 1)
            )
            gap = matching[q] - matching[p]
            assert gap == formula
            if z < y:
                assert gap > 0
                reversals += 1
            else:
                assert gap == -6 * fibonacci(2 * z + 1) * fibonacci(2 * d - 4) < 0
                diagonal += 1
            rows.append(
                [
                    a,
                    x,
                    y,
                    z,
                    matching[p],
                    matching[q],
                    lagrange[p].numerator,
                    lagrange[p].denominator,
                    lagrange[q].numerator,
                    lagrange[q].denominator,
                ]
            )
    return len(carrier), reversals, diagonal, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=60)
    args = parser.parse_args()
    if args.max_a < 7:
        raise SystemExit("--max-a must be at least 7")

    digest = hashlib.sha256()
    endpoints = path_count = reversals = diagonal = 0
    for a in range(7, args.max_a + 1):
        if gcd(a, 3) != 1:
            continue
        count, endpoint_reversals, endpoint_diagonal, rows = check_endpoint(a)
        endpoints += 1
        path_count += count
        reversals += endpoint_reversals
        diagonal += endpoint_diagonal
        for row in rows:
            digest.update(json.dumps(row, separators=(",", ":")).encode() + b"\n")

    print(
        "INDEPENDENT VERIFIED D(a,3) interior sign rule from definitions; "
        f"7<=a<={args.max_a}; endpoints={endpoints}; paths={path_count}; "
        f"reversals={reversals}; diagonal_obstructions={diagonal}; "
        f"row_sha256={digest.hexdigest()}"
    )


if __name__ == "__main__":
    main()
