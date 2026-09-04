#!/usr/bin/env python3
"""Definition-level finite check of the D(a,3) Lagrange partition chain.

This file does not import verify.py.  It generates binary Dyck words, encodes
adjacencies literally, and evaluates cyclic Lagrange squares with scalar
continuants rather than the symbolic 2x2 matrix algebra used in the proof
certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from math import gcd


def continuant(digits: tuple[int, ...]) -> int:
    if not digits:
        return 1
    previous2 = 1
    previous1 = digits[0]
    for digit in digits[1:]:
        previous2, previous1 = previous1, digit * previous1 + previous2
    return previous1


def coefficient_word(path: tuple[str, ...]) -> tuple[int, ...]:
    output = [2]  # cyclic closing edge: final U to initial R
    for left, right in zip(path, path[1:]):
        if left == right:
            output.extend((1, 1))
        else:
            output.append(2)
    return tuple(output)


def lagrange_square(path: tuple[str, ...]) -> Fraction:
    period = coefficient_word(path)
    trace = continuant(period) + continuant(period[1:-1])
    q_min = min(
        continuant((period[index:] + period[:index])[1:])
        for index in range(len(period))
    )
    return Fraction(trace * trace - 4, q_min * q_min)


def dyck_paths(a: int) -> list[tuple[str, ...]]:
    output: list[tuple[str, ...]] = []

    def visit(r_count: int, u_count: int, word: list[str]) -> None:
        if r_count == a and u_count == 3:
            output.append(tuple(word))
            return
        if r_count < a:
            word.append("R")
            visit(r_count + 1, u_count, word)
            word.pop()
        if u_count < 3 and a * (u_count + 1) <= 3 * r_count:
            word.append("U")
            visit(r_count, u_count + 1, word)
            word.pop()

    visit(0, 0, [])
    return output


def run_triple(path: tuple[str, ...]) -> tuple[int, int, int]:
    runs: list[int] = []
    count = 0
    for step in path:
        if step == "R":
            count += 1
        else:
            runs.append(count)
            count = 0
    if count or len(runs) != 3:
        raise AssertionError("D(a,3) path must end in its third U")
    return tuple(runs)  # type: ignore[return-value]


def partitions(a: int) -> list[tuple[int, int, int]]:
    result = []
    for z in range(a // 3 + 1):
        for y in range(z, a + 1):
            x = a - y - z
            if x >= y:
                result.append((x, y, z))
    return sorted(result, key=lambda part: (part[2], -part[0]))


def check_endpoint(a: int) -> list[object]:
    paths = dyck_paths(a)
    levels: dict[Fraction, list[tuple[str, ...]]] = defaultdict(list)
    for path in paths:
        levels[lagrange_square(path)].append(path)

    decreasing = sorted(levels.items(), reverse=True)
    expected = partitions(a)
    obtained: list[tuple[int, int, int]] = []
    rows: list[object] = []
    for score, level in decreasing:
        level_parts = {tuple(sorted(run_triple(path), reverse=True)) for path in level}
        if len(level_parts) != 1:
            raise AssertionError(f"a={a}: a score level joins partitions {level_parts}")
        part = level_parts.pop()
        obtained.append(part)
        triples = sorted(run_triple(path) for path in level)
        rows.append([a, list(part), score.numerator, score.denominator, [list(t) for t in triples]])
    if obtained != expected:
        raise AssertionError(f"a={a}: partition-chain mismatch\n{obtained}\n{expected}")

    expected_triples = {
        (r, s, a - r - s)
        for r in range(a + 1)
        for s in range(a - r + 1)
        if 3 * r >= a and 3 * (r + s) >= 2 * a
    }
    actual_triples = {run_triple(path) for path in paths}
    if actual_triples != expected_triples:
        raise AssertionError(f"a={a}: Dyck run-condition mismatch")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=60)
    args = parser.parse_args()
    if args.max_a < 4:
        raise SystemExit("--max-a must be at least 4")

    all_rows: list[object] = []
    path_count = 0
    endpoint_count = 0
    for a in range(4, args.max_a + 1):
        if gcd(a, 3) != 1:
            continue
        rows = check_endpoint(a)
        all_rows.extend(rows)
        path_count += len(dyck_paths(a))
        endpoint_count += 1
    payload = (json.dumps(all_rows, separators=(",", ":")) + "\n").encode()
    digest = hashlib.sha256(payload).hexdigest()
    print(
        "INDEPENDENT VERIFIED D(a,3) Lagrange levels from definitions; "
        f"4<=a<={args.max_a}; endpoints={endpoint_count}; paths={path_count}; "
        f"levels={len(all_rows)}; level_sha256={digest}"
    )


if __name__ == "__main__":
    main()
