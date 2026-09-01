#!/usr/bin/env python3
"""Direct subset-XOR audit of the exact H_B sum-one syndrome theorem."""

from __future__ import annotations

from itertools import combinations
from random import Random

N = 21
FULL = (1 << N) - 1


def d_columns(mask: int) -> tuple[int, ...]:
    columns = []
    for index in range(N):
        column = 0
        for shift in range(1, 11):
            bit = ((mask >> ((index + shift) % N)) ^ (mask >> ((index - shift) % N))) & 1
            column |= bit << (shift - 1)
        columns.append(column)
    return tuple(columns)


def binary_rank(vectors: list[int] | tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def exact_subset_xors(columns: list[int], choose: int) -> set[int]:
    result = set()
    for selection in combinations(columns, choose):
        value = 0
        for column in selection:
            value ^= column
        result.add(value)
    return result


def direct_support(mask: int) -> set[int]:
    weight = mask.bit_count()
    assert weight % 2 == 0
    columns = d_columns(mask)
    real = [columns[index] for index in range(N) if not ((mask >> index) & 1)]
    imaginary = [columns[index] for index in range(N) if (mask >> index) & 1]
    real_support = exact_subset_xors(real, (len(real) - 1) // 2)
    imaginary_support = exact_subset_xors(imaginary, len(imaginary) // 2)
    return {left ^ right for left in real_support for right in imaginary_support}


def affine_dimension(support: set[int]) -> int:
    origin = next(iter(support))
    dimension = binary_rank([value ^ origin for value in support])
    assert len(support) == 1 << dimension
    return dimension


def sample_masks() -> list[int]:
    by_rank: dict[int, int] = {}
    for mask in range(1 << N):
        if mask.bit_count() & 1:
            continue
        rank = binary_rank(d_columns(mask))
        by_rank.setdefault(rank, mask)
        if len(by_rank) == 8:
            break
    assert set(by_rank) == {0, 1, 3, 4, 6, 7, 9, 10}

    result = set(by_rank.values())
    rng = Random(0x4842_0001)
    while len(result) < 256:
        mask = rng.randrange(1 << N)
        if mask.bit_count() % 2 == 0:
            result.add(mask)
    return sorted(result)


def main() -> None:
    masks = sample_masks()
    ranks = set()
    for mask in masks:
        rank = binary_rank(d_columns(mask))
        support = direct_support(mask)
        dimension = affine_dimension(support)
        assert dimension == (0 if rank == 0 else rank - 1)
        ranks.add(rank)
    print(f"direct_subset_axis_words={len(masks)}")
    print("rank_coverage=" + ",".join(map(str, sorted(ranks))))
    print("direct_affine_supports=verified")
    print("independent_sample_check=verified")


if __name__ == "__main__":
    main()
