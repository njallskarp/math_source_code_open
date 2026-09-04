#!/usr/bin/env python3
"""Independent checks using reduced words and direct plane-partition enumeration."""

from __future__ import annotations

import functools
import hashlib
import math


def adjacent_swap(w: tuple[int, ...], i: int) -> tuple[int, ...]:
    out = list(w)
    out[i], out[i + 1] = out[i + 1], out[i]
    return tuple(out)


@functools.cache
def weighted_reduced_words(w: tuple[int, ...]) -> int:
    """Sum of products of 1-based letters over all reduced words."""
    descents = [i for i in range(len(w) - 1) if w[i] > w[i + 1]]
    if not descents:
        return 1
    return sum((i + 1) * weighted_reduced_words(adjacent_swap(w, i)) for i in descents)


def inversion_count(w: tuple[int, ...]) -> int:
    return sum(a > b for i, a in enumerate(w) for b in w[i + 1 :])


def macdonald_upsilon(w: tuple[int, ...]) -> int:
    numerator = weighted_reduced_words(w)
    denominator = math.factorial(inversion_count(w))
    assert numerator % denominator == 0
    return numerator // denominator


def rectangle_permutation(a: int, b: int, c: int) -> tuple[int, ...]:
    return tuple(range(c)) + tuple(range(c + b, c + b + a)) + tuple(range(c, c + b))


def rows(width: int, ceiling: tuple[int, ...]) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []

    def extend(prefix: tuple[int, ...], maximum: int) -> None:
        column = len(prefix)
        if column == width:
            result.append(prefix)
            return
        for value in range(min(maximum, ceiling[column]), -1, -1):
            extend(prefix + (value,), value)

    extend((), ceiling[0])
    return result


@functools.cache
def plane_partitions(height: int, width: int, ceiling: tuple[int, ...]) -> int:
    """Count weakly decreasing arrays with the supplied top row ceiling."""
    if height == 0:
        return 1
    return sum(plane_partitions(height - 1, width, row) for row in rows(width, ceiling))


def count_plane_partitions(a: int, b: int, c: int) -> int:
    return plane_partitions(a, b, (c,) * b)


def main() -> None:
    cases = [
        (1, 1, 1, 2),
        (1, 1, 2, 3),
        (1, 2, 1, 2),
        (2, 1, 1, 2),
        (2, 2, 1, 2),
    ]
    digest = hashlib.sha256()
    for a, b, c, k in cases:
        base_w = rectangle_permutation(a, b, c)
        large_w = rectangle_permutation(k * a, k * b, k * c)
        base_words = macdonald_upsilon(base_w)
        large_words = macdonald_upsilon(large_w)
        base_arrays = count_plane_partitions(a, b, c)
        large_arrays = count_plane_partitions(k * a, k * b, k * c)
        assert base_words == base_arrays
        assert large_words == large_arrays
        assert large_words >= base_words ** (k * k)
        line = f"a={a} b={b} c={c} k={k} count={base_words}->{large_words}"
        digest.update((line + "\n").encode())
        print(line)
    print(
        f"PASS independent cases={len(cases)} digest={digest.hexdigest()} "
        f"reduced_word_cache={weighted_reduced_words.cache_info().currsize} "
        f"plane_partition_cache={plane_partitions.cache_info().currsize}"
    )


if __name__ == "__main__":
    main()
