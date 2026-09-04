#!/usr/bin/env python3
"""Definition-level audit of the D(a,3) cover-reversal family.

This file imports no contributor module.  It generates every rational-Dyck
word, evaluates matching scores by scalar continuants, evaluates exact squared
Lagrange scores at every cyclic cut, and checks that each proposed pair lies in
consecutive Lagrange score levels with the opposite matching orientation.
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
    previous, current = 0, 1
    for _ in range(index):
        previous, current = current, previous + current
    return previous


def paths(a: int) -> list[Path]:
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


def named_paths(x: int, y: int) -> tuple[Path, Path]:
    p = tuple("R" * x + "U" + "R" * y + "UU")
    q = tuple("R" * (x - 1) + "UU" + "R" * (y + 1) + "U")
    return p, q


def check_endpoint(a: int) -> tuple[int, int, list[list[int]]]:
    carrier = paths(a)
    lagrange = {path: lagrange_square(path) for path in carrier}
    matching = {path: matching_number(path) for path in carrier}
    levels = sorted(set(lagrange.values()), reverse=True)
    level_index = {score: index for index, score in enumerate(levels)}
    rows: list[list[int]] = []
    noncoatom = 0

    for y in range(1, (a - 3) // 3 + 1):
        x = a - y
        p, q = named_paths(x, y)
        assert p in lagrange and q in lagrange
        assert level_index[lagrange[q]] == level_index[lagrange[p]] + 1
        assert matching[q] > matching[p]

        d = x - y
        formula = 2 * (
            fibonacci(2 * y + 2) * fibonacci(2 * x - 3)
            - 2 * fibonacci(2 * d - 4)
            - fibonacci(2 * d - 2)
        )
        assert matching[q] - matching[p] == formula
        rows.append(
            [
                a,
                x,
                y,
                matching[p],
                matching[q],
                lagrange[p].numerator,
                lagrange[p].denominator,
                lagrange[q].numerator,
                lagrange[q].denominator,
            ]
        )
        noncoatom += y >= 2
    return len(carrier), noncoatom, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=60)
    args = parser.parse_args()
    if args.max_a < 7:
        raise SystemExit("--max-a must be at least 7")

    all_rows: list[list[int]] = []
    path_count = endpoint_count = noncoatom = 0
    for a in range(7, args.max_a + 1):
        if gcd(a, 3) != 1:
            continue
        count, endpoint_noncoatom, rows = check_endpoint(a)
        path_count += count
        endpoint_count += 1
        noncoatom += endpoint_noncoatom
        all_rows.extend(rows)

    payload = (json.dumps(all_rows, separators=(",", ":")) + "\n").encode()
    digest = hashlib.sha256(payload).hexdigest()
    print(
        "INDEPENDENT VERIFIED D(a,3) cover reversals from definitions; "
        f"7<=a<={args.max_a}; endpoints={endpoint_count}; paths={path_count}; "
        f"pairs={len(all_rows)}; noncoatom_pairs={noncoatom}; "
        f"row_sha256={digest}"
    )


if __name__ == "__main__":
    main()
