#!/usr/bin/env python3
"""Exact q-Pascal verification of KOH and the width-five a=1 expansion."""

from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math


Polynomial = tuple[int, ...]
ZERO: Polynomial = ()
ONE: Polynomial = (1,)


def trim(values: list[int]) -> Polynomial:
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(*polys: Polynomial) -> Polynomial:
    result = [0] * max((len(poly) for poly in polys), default=0)
    for poly in polys:
        for degree, coefficient in enumerate(poly):
            result[degree] += coefficient
    return trim(result)


def mul(left: Polynomial, right: Polynomial) -> Polynomial:
    if not left or not right:
        return ZERO
    result = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return trim(result)


def shift(poly: Polynomial, degree: int) -> Polynomial:
    return (0,) * degree + poly if poly else ZERO


@lru_cache(maxsize=None)
def gaussian(n: int, r: int) -> Polynomial:
    if r < 0 or r > n or n < 0:
        return ZERO
    r = min(r, n - r)
    if r == 0:
        return ONE
    return add(gaussian(n - 1, r), shift(gaussian(n - 1, r - 1), n - r))


def partitions(total: int, maximum: int | None = None) -> list[tuple[int, ...]]:
    if total == 0:
        return [()]
    maximum = total if maximum is None else min(maximum, total)
    result = []
    for first in range(maximum, 0, -1):
        result.extend((first,) + tail for tail in partitions(total - first, first))
    return result


def koh_data(partition: tuple[int, ...], width: int) -> tuple[int, tuple[tuple[int, int], ...]]:
    """Return exponent and (top,bottom) factors for rectangle width."""
    exponent = 2 * sum(math.comb(part, 2) for part in partition)
    cumulative = [0]
    for part in partition:
        cumulative.append(cumulative[-1] + part)
    cumulative.append(cumulative[-1])
    factors = []
    for j, part in enumerate(partition, start=1):
        following = partition[j] if j < len(partition) else 0
        bottom = part - following
        if bottom:
            top = j * (width + 2) - cumulative[j - 1] - cumulative[j + 1]
            factors.append((top, bottom))
    return exponent, tuple(factors)


def koh_term(partition: tuple[int, ...], width: int) -> Polynomial:
    exponent, factors = koh_data(partition, width)
    result = ONE
    for top, bottom in factors:
        result = mul(result, gaussian(top, bottom))
    return shift(result, exponent)


def koh_sum(parts: int, width: int) -> Polynomial:
    return add(*(koh_term(partition, width) for partition in partitions(parts)))


def explicit_width_five(k: int) -> Polynomial:
    terms = [
        gaussian(5 * k + 1, 1),
        shift(mul(gaussian(k - 1, 1), gaussian(4 * k - 1, 1)), 2),
        shift(mul(gaussian(2 * k - 3, 1), gaussian(3 * k - 3, 1)), 4),
        shift(mul(gaussian(k - 2, 2), gaussian(3 * k - 3, 1)), 6),
        shift(mul(gaussian(k - 3, 1), gaussian(2 * k - 4, 2)), 8),
        shift(mul(gaussian(k - 3, 3), gaussian(2 * k - 5, 1)), 12),
        shift(gaussian(k - 3, 5), 20),
    ]
    return add(*terms)


def symbolic_width_five_record() -> list[dict[str, object]]:
    # Store each top as alpha*k+beta, derived at k=11 and k=12.
    record = []
    for partition in partitions(5):
        exponent, at_eleven = koh_data(partition, 11)
        _, at_twelve = koh_data(partition, 12)
        affine_factors = []
        for (top_11, bottom), (top_12, bottom_12) in zip(at_eleven, at_twelve, strict=True):
            assert bottom == bottom_12
            alpha = top_12 - top_11
            beta = top_11 - 11 * alpha
            affine_factors.append([alpha, beta, bottom])
        record.append(
            {"exponent": exponent, "factors": affine_factors, "partition": list(partition)}
        )
    return record


EXPECTED_WIDTH_FIVE_RECORD = [
    {"exponent": 20, "factors": [[1, -3, 5]], "partition": [5]},
    {"exponent": 12, "factors": [[1, -3, 3], [2, -5, 1]], "partition": [4, 1]},
    {"exponent": 8, "factors": [[1, -3, 1], [2, -4, 2]], "partition": [3, 2]},
    {"exponent": 6, "factors": [[1, -2, 2], [3, -3, 1]], "partition": [3, 1, 1]},
    {"exponent": 4, "factors": [[2, -3, 1], [3, -3, 1]], "partition": [2, 2, 1]},
    {"exponent": 2, "factors": [[1, -1, 1], [4, -1, 1]], "partition": [2, 1, 1, 1]},
    {"exponent": 0, "factors": [[5, 1, 1]], "partition": [1, 1, 1, 1, 1]},
]
EXPECTED_RECORD_SHA256 = "2ed9293c891669589170bf172bbec8b54860bf69ef2d295be84d65c125566a94"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-parts", type=int, default=9)
    parser.add_argument("--max-width", type=int, default=16)
    parser.add_argument("--max-k", type=int, default=100)
    args = parser.parse_args()
    if args.max_parts < 5 or args.max_width < args.max_parts or args.max_k < 5:
        parser.error("need --max-parts >= 5, --max-width >= --max-parts, and --max-k >= 5")

    record = symbolic_width_five_record()
    assert record == EXPECTED_WIDTH_FIVE_RECORD
    digest = hashlib.sha256(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if not EXPECTED_RECORD_SHA256.startswith("__"):
        assert digest == EXPECTED_RECORD_SHA256

    # Definition-level verification of the general KOH formula.
    cases = 0
    for parts in range(2, args.max_parts + 1):
        for width in range(parts, args.max_width + 1):
            partition_data = [
                (partition, *koh_data(partition, width)) for partition in partitions(parts)
            ]
            assert all(exponent % 2 == 0 for _, exponent, _ in partition_data)
            for _, exponent, factors in partition_data:
                factor_degree = sum(bottom * (top - bottom) for top, bottom in factors)
                assert 2 * exponent + factor_degree == parts * width
            zero_exponents = [
                (partition, factors)
                for partition, exponent, factors in partition_data
                if exponent == 0
            ]
            assert zero_exponents == [((1,) * parts, ((parts * width + 1, 1),))]
            assert all(exponent >= 2 for partition, exponent, _ in partition_data if partition != (1,) * parts)
            assert koh_sum(parts, width) == gaussian(parts + width, parts), (parts, width)
            cases += 1

    # Transcription audit for all canonical width-five boundary parameters.
    for k in range(5, args.max_k + 1):
        assert explicit_width_five(k) == gaussian(k + 5, 5), k
        assert explicit_width_five(k) == koh_sum(5, k), ("KOH transcription", k)

    print("exact q-Pascal KOH verification passed")
    print(f"general KOH cases={cases}; 2<=parts<={args.max_parts}, parts<=width<={args.max_width}")
    print(f"explicit width-five identity checked for 5<=k<={args.max_k}")
    print(f"width-five structural record SHA-256: {digest}")


if __name__ == "__main__":
    main()
