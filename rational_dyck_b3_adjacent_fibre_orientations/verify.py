#!/usr/bin/env python3
"""Exact audit of the complete adjacent-fibre matching orientation on D(a,3).

The universal proof is in README.md.  This checker reconstructs the run-block
matrices, the Dyck-valid orientation lemma, every within-layer gap identity,
and the complete comparison table over a configurable finite range.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import permutations
from math import gcd

Run = tuple[int, int, int]
Matrix = tuple[tuple[int, int], tuple[int, int]]


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


def matching_score(runs: Run) -> int:
    product = matrix_multiply(
        matrix_multiply(k_matrix(runs[0]), k_matrix(runs[1])),
        k_matrix(runs[2]),
    )
    return product[1][0]


def is_dyck_run(runs: Run, a: int) -> bool:
    r, s, t = runs
    return min(runs) >= 0 and r + s + t == a and 3 * r >= a and 3 * (r + s) >= 2 * a


def partitions(a: int) -> list[Run]:
    output: list[Run] = []
    for z in range(a // 3 + 1):
        for y in range(z, a + 1):
            x = a - y - z
            if x >= y:
                output.append((x, y, z))
    return sorted(output, key=lambda part: (part[2], -part[0]))


def valid_orientations(part: Run, a: int) -> tuple[Run, ...]:
    x, y, z = part
    if not (x >= y >= z >= 0 and x + y + z == a and gcd(a, 3) == 1):
        raise ValueError("requires a sorted partition at a coprime endpoint")
    h = x + z - 2 * y
    if h == 0:
        raise AssertionError("h=a-3y cannot vanish when gcd(a,3)=1")
    candidates = [(x, y, z), (x, z, y) if h > 0 else (y, x, z)]
    return tuple(dict.fromkeys(candidates))


def brute_valid_orientations(part: Run, a: int) -> tuple[Run, ...]:
    return tuple(sorted(run for run in set(permutations(part)) if is_dyck_run(run, a)))


def orientation_gain(part: Run, oriented: Run) -> int:
    """Return M(oriented)-M(canonical), including its exact swap formula."""
    x, y, z = part
    canonical = (x, y, z)
    if oriented == canonical:
        return 0
    h = x + z - 2 * y
    if h > 0:
        if oriented != (x, z, y):
            raise ValueError("not the positive-h alternative")
        formula = 2 * fibonacci(2 * (y - z)) * fibonacci(2 * x - 1)
    else:
        if oriented != (y, x, z):
            raise ValueError("not the negative-h alternative")
        formula = 2 * fibonacci(2 * (x - y)) * fibonacci(2 * z + 3)
    actual = matching_score(oriented) - matching_score(canonical)
    if actual != formula or formula <= 0:
        raise AssertionError((part, oriented, actual, formula))
    return formula


def within_drop(x: int, y: int, z: int) -> int:
    d = x - y
    if d < 2:
        raise ValueError("within-layer transition requires x-y>=2")
    return 2 * (
        fibonacci(2 * d - 4) * fibonacci(2 * z + 3)
        + fibonacci(2 * d - 2) * fibonacci(2 * z + 1)
    )


def reversal_gap(x: int, y: int, z: int) -> int:
    d, e = x - y, y - z
    return 2 * (
        fibonacci(2 * e + 2) * fibonacci(2 * x - 3)
        - fibonacci(2 * d - 4) * fibonacci(2 * z + 3)
        - fibonacci(2 * d - 2) * fibonacci(2 * z + 1)
    )


def predicted_reversal(upper_part: Run, lower_part: Run, upper: Run, lower: Run) -> bool:
    x, y, z = upper_part
    if upper_part[2] != lower_part[2]:
        return False
    return (
        x + z - 2 * y > 3
        and y > z
        and upper == (x, y, z)
        and lower == (x - 1, z, y + 1)
    )


def audit_within_transition(upper_part: Run, lower_part: Run, a: int) -> list[list[object]]:
    x, y, z = upper_part
    d, e, h = x - y, y - z, x + z - 2 * y
    if lower_part != (x - 1, y + 1, z) or d < 2:
        raise ValueError("not a consecutive within-layer transition")
    upper_runs = valid_orientations(upper_part, a)
    lower_runs = valid_orientations(lower_part, a)
    upper_canonical, lower_canonical = upper_part, lower_part
    drop = within_drop(x, y, z)
    if matching_score(upper_canonical) - matching_score(lower_canonical) != drop:
        raise AssertionError("canonical within-layer drop identity failed")

    for run in upper_runs:
        orientation_gain(upper_part, run)
    for run in lower_runs:
        orientation_gain(lower_part, run)

    lower_alternative = lower_runs[-1]
    if lower_alternative != lower_canonical:
        gap_to_upper_canonical = matching_score(lower_alternative) - matching_score(upper_canonical)
        if h < 3:
            expected = -2 * fibonacci(2 * d - 2) * fibonacci(2 * z + 1)
            if gap_to_upper_canonical != expected or expected >= 0:
                raise AssertionError("low-h comparison identity failed")
        else:
            expected = reversal_gap(x, y, z)
            if gap_to_upper_canonical != expected:
                raise AssertionError("high-h comparison identity failed")
            if (expected > 0) != (e > 0):
                raise AssertionError("high-h sign boundary failed")

    upper_alternative = upper_runs[-1]
    if h > 3 and lower_alternative != lower_canonical:
        expected = -6 * fibonacci(2 * d - 4) * fibonacci(2 * z + 1)
        actual = matching_score(lower_alternative) - matching_score(upper_alternative)
        if actual != expected or expected >= 0:
            raise AssertionError("alternative-to-alternative identity failed")

    rows: list[list[object]] = []
    for upper in upper_runs:
        for lower in lower_runs:
            gap = matching_score(lower) - matching_score(upper)
            predicted = predicted_reversal(upper_part, lower_part, upper, lower)
            if (gap > 0) != predicted or gap == 0:
                raise AssertionError((a, upper_part, lower_part, upper, lower, gap, predicted))
            rows.append(
                [a, "within", list(upper_part), list(lower_part), list(upper), list(lower), gap, predicted]
            )
    return rows


def audit_inter_transition(upper_part: Run, lower_part: Run, a: int) -> list[list[object]]:
    if upper_part[2] == lower_part[2]:
        raise ValueError("not an inter-layer transition")
    upper_runs = valid_orientations(upper_part, a)
    lower_runs = valid_orientations(lower_part, a)
    if len(lower_runs) != 1 or len(upper_runs) not in (1, 2):
        raise AssertionError("unexpected inter-layer orientation shape")
    upper_canonical, lower_canonical = upper_part, lower_part
    if matching_score(lower_canonical) >= matching_score(upper_canonical):
        raise AssertionError("canonical inter-layer matching drop failed")
    for run in upper_runs:
        orientation_gain(upper_part, run)
    rows: list[list[object]] = []
    for upper in upper_runs:
        for lower in lower_runs:
            gap = matching_score(lower) - matching_score(upper)
            if gap >= 0:
                raise AssertionError((a, upper_part, lower_part, upper, lower, gap))
            rows.append(
                [a, "inter", list(upper_part), list(lower_part), list(upper), list(lower), gap, False]
            )
    return rows


def audit(max_a: int) -> dict[str, int | str]:
    if max_a < 4:
        raise ValueError("max_a must be at least 4")
    digest = hashlib.sha256()
    endpoints = partition_count = transition_count = cross_pairs = reversals = 0
    within_count = inter_count = 0
    for a in range(4, max_a + 1):
        if gcd(a, 3) != 1:
            continue
        parts = partitions(a)
        for part in parts:
            if sorted(valid_orientations(part, a)) != list(brute_valid_orientations(part, a)):
                raise AssertionError((a, part, valid_orientations(part, a), brute_valid_orientations(part, a)))
        for upper_part, lower_part in zip(parts, parts[1:]):
            if upper_part[2] == lower_part[2]:
                rows = audit_within_transition(upper_part, lower_part, a)
                within_count += 1
            else:
                rows = audit_inter_transition(upper_part, lower_part, a)
                inter_count += 1
            for row in rows:
                digest.update(json.dumps(row, separators=(",", ":")).encode() + b"\n")
                reversals += bool(row[-1])
            cross_pairs += len(rows)
            transition_count += 1
        endpoints += 1
        partition_count += len(parts)
    return {
        "endpoints": endpoints,
        "partitions": partition_count,
        "transitions": transition_count,
        "within": within_count,
        "inter": inter_count,
        "cross_pairs": cross_pairs,
        "reversals": reversals,
        "row_sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=180)
    args = parser.parse_args()
    result = audit(args.max_a)
    fields = "; ".join(f"{key}={value}" for key, value in result.items())
    print(f"EXACT VERIFIED COMPLETE D(a,3) ADJACENT-FIBRE ORIENTATION; 4<=a<={args.max_a}; {fields}")


if __name__ == "__main__":
    main()
