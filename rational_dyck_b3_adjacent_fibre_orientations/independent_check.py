#!/usr/bin/env python3
"""Definition-level audit of adjacent-fibre matching orientations on D(a,3).

This checker imports no contributor module.  It generates every carrier path,
evaluates matching scores by scalar continuants, evaluates every cyclic
Lagrange shift exactly with Fraction, reconstructs the realized fibres, and
checks every cross-fibre comparison.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from math import gcd

Path = tuple[str, ...]
Run = tuple[int, int, int]


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


def matching_score(path: Path) -> int:
    return continuant(coefficient_word(path))


def lagrange_square(path: Path) -> Fraction:
    period = (2,) + coefficient_word(path)
    trace = continuant(period) + continuant(period[1:-1])
    denominators = [
        continuant((period[index:] + period[:index])[1:])
        for index in range(len(period))
    ]
    return Fraction(trace * trace - 4, min(denominators) ** 2)


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


def run_triple(path: Path) -> Run:
    runs: list[int] = []
    count = 0
    for step in path:
        if step == "R":
            count += 1
        else:
            runs.append(count)
            count = 0
    if count or len(runs) != 3:
        raise AssertionError("D(a,3) path must end at its third U")
    return runs[0], runs[1], runs[2]


def predicted_reversal(upper_part: Run, lower_part: Run, upper: Run, lower: Run) -> bool:
    x, y, z = upper_part
    return (
        upper_part[2] == lower_part[2]
        and x + z - 2 * y > 3
        and y > z
        and upper == (x, y, z)
        and lower == (x - 1, z, y + 1)
    )


def check_endpoint(a: int) -> tuple[int, int, int, int, int, list[list[object]]]:
    carrier = carrier_paths(a)
    matching = {path: matching_score(path) for path in carrier}
    levels: dict[Fraction, list[Path]] = defaultdict(list)
    for path in carrier:
        levels[lagrange_square(path)].append(path)
    ordered_levels = sorted(levels.items(), reverse=True)

    rows: list[list[object]] = []
    reversals = within = inter = cross_pairs = 0
    previous_part: Run | None = None
    for _, paths in ordered_levels:
        parts = {tuple(sorted(run_triple(path), reverse=True)) for path in paths}
        if len(parts) != 1:
            raise AssertionError((a, parts))
        part = parts.pop()
        if previous_part is not None:
            upper_part, lower_part = previous_part, part
            transition_kind = "within" if upper_part[2] == lower_part[2] else "inter"
            within += transition_kind == "within"
            inter += transition_kind == "inter"
            upper_paths = previous_paths
            for upper_path in upper_paths:
                for lower_path in paths:
                    upper, lower = run_triple(upper_path), run_triple(lower_path)
                    gap = matching[lower_path] - matching[upper_path]
                    predicted = predicted_reversal(upper_part, lower_part, upper, lower)
                    if (gap > 0) != predicted or gap == 0:
                        raise AssertionError((a, upper_part, lower_part, upper, lower, gap, predicted))
                    rows.append(
                        [
                            a,
                            transition_kind,
                            list(upper_part),
                            list(lower_part),
                            list(upper),
                            list(lower),
                            matching[upper_path],
                            matching[lower_path],
                            gap,
                            predicted,
                        ]
                    )
                    cross_pairs += 1
                    reversals += predicted
        previous_part, previous_paths = part, paths
    return len(carrier), len(ordered_levels), within, inter, reversals, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-a", type=int, default=60)
    args = parser.parse_args()
    if args.max_a < 4:
        raise SystemExit("--max-a must be at least 4")

    digest = hashlib.sha256()
    endpoints = path_count = level_count = within = inter = reversals = cross_pairs = 0
    for a in range(4, args.max_a + 1):
        if gcd(a, 3) != 1:
            continue
        paths, levels, endpoint_within, endpoint_inter, endpoint_reversals, rows = check_endpoint(a)
        endpoints += 1
        path_count += paths
        level_count += levels
        within += endpoint_within
        inter += endpoint_inter
        reversals += endpoint_reversals
        cross_pairs += len(rows)
        for row in rows:
            digest.update(json.dumps(row, separators=(",", ":")).encode() + b"\n")

    print(
        "INDEPENDENT VERIFIED COMPLETE D(a,3) ADJACENT-FIBRE ORIENTATION; "
        f"4<=a<={args.max_a}; endpoints={endpoints}; paths={path_count}; levels={level_count}; "
        f"within={within}; inter={inter}; cross_pairs={cross_pairs}; reversals={reversals}; "
        f"row_sha256={digest.hexdigest()}"
    )


if __name__ == "__main__":
    main()
