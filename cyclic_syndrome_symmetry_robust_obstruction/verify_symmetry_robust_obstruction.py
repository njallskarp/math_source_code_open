#!/usr/bin/env python3
"""Definition-level certificate for the length-9 symmetry-robust obstruction."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
from math import gcd
import platform


N = 9
M = 4
AXES = {
    "A": frozenset((0, 1, 2, 3)),
    "B": frozenset((0, 1, 3, 6)),
}
UNITS = tuple(u for u in range(1, N) if gcd(u, N) == 1)
TARGET = (5, 0)


def polynomial(axis: frozenset[int]) -> int:
    return sum(1 << j for j in axis)


def polynomial_mod(dividend: int, divisor: int) -> int:
    if divisor == 0:
        raise ZeroDivisionError
    while dividend and dividend.bit_length() >= divisor.bit_length():
        dividend ^= divisor << (dividend.bit_length() - divisor.bit_length())
    return dividend


def polynomial_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, polynomial_mod(left, right)
    return left


def syndrome(axis: frozenset[int], sigma: int) -> int:
    """Evaluate D_a(sigma) from the defining cyclic sum over F_2."""
    out = 0
    for s in range(1, M + 1):
        coordinate = 0
        for j in range(N):
            sign_difference = ((sigma >> j) ^ (sigma >> ((j + s) % N))) & 1
            axis_difference = (j in axis) ^ (((j + s) % N) in axis)
            coordinate ^= sign_difference & axis_difference
        out |= coordinate << (s - 1)
    return out


def gaussian_sum(axis: frozenset[int], sigma: int) -> tuple[int, int]:
    real = sum((1 if not (sigma >> j) & 1 else -1) for j in range(N) if j not in axis)
    imag = sum((1 if not (sigma >> j) & 1 else -1) for j in axis)
    return real, imag


def coordinate_set(vector: int) -> tuple[int, ...]:
    return tuple(s for s in range(1, M + 1) if (vector >> (s - 1)) & 1)


def exact_fiber(axis: frozenset[int]) -> Counter[int]:
    return Counter(
        syndrome(axis, sigma)
        for sigma in range(1 << N)
        if gaussian_sum(axis, sigma) == TARGET
    )


def binary_rank(vectors: set[int]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                vector ^= pivots[pivot]
            else:
                pivots[pivot] = vector
                break
    return len(pivots)


def canonical_distance(value: int) -> int:
    value %= N
    return min(value, N - value)


def permute_syndrome(vector: int, unit: int) -> int:
    out = 0
    for s in range(1, M + 1):
        if (vector >> (s - 1)) & 1:
            out |= 1 << (canonical_distance(unit * s) - 1)
    return out


def unit_closure(fiber: set[int]) -> set[int]:
    return {permute_syndrome(vector, unit) for vector in fiber for unit in UNITS}


def transform_axis(axis: frozenset[int], unit: int, translate: int) -> frozenset[int]:
    return frozenset((unit * j + translate) % N for j in axis)


def affine_orbit(axis: frozenset[int]) -> set[frozenset[int]]:
    return {
        transform_axis(axis, unit, translate)
        for unit in UNITS
        for translate in range(N)
    }


def divisible_pair_count(axis: frozenset[int]) -> int:
    return sum((left - right) % 3 == 0 for left, right in combinations(sorted(axis), 2))


def format_counter(counter: Counter[int]) -> str:
    return ",".join(
        f"{coordinate_set(vector)}:{counter[vector]}" for vector in sorted(counter)
    )


def format_set(vectors: set[int]) -> str:
    return ",".join(str(coordinate_set(vector)) for vector in sorted(vectors))


def main() -> None:
    modulus = (1 << N) | 1  # x^9+1 over F_2
    fibers = {name: exact_fiber(axis) for name, axis in AXES.items()}
    images = {
        name: {syndrome(axis, sigma) for sigma in range(1 << N)}
        for name, axis in AXES.items()
    }
    gcds = {
        name: polynomial_gcd(polynomial(axis), modulus)
        for name, axis in AXES.items()
    }
    closures = {name: unit_closure(set(fiber)) for name, fiber in fibers.items()}
    pair_counts = {name: divisible_pair_count(axis) for name, axis in AXES.items()}

    expected_a = Counter({0: 2, (1 << 0) | (1 << 2): 4})
    expected_b = Counter(
        {
            (1 << 0) | (1 << 1): 2,
            (1 << 0) | (1 << 3): 2,
            (1 << 1) | (1 << 3): 2,
        }
    )

    assert gcds == {"A": 0b11, "B": 0b11}
    assert all(len(image) == 1 << M and binary_rank(image) == M for image in images.values())
    assert fibers == {"A": expected_a, "B": expected_b}
    assert sum(fibers["A"].values()) == sum(fibers["B"].values()) == 6
    assert all(vector.bit_count() % 2 == 0 for fiber in fibers.values() for vector in fiber)
    assert pair_counts == {"A": 1, "B": 3}
    assert AXES["B"] not in affine_orbit(AXES["A"])
    assert closures["A"].isdisjoint(closures["B"])
    assert closures["A"] == {
        0,
        (1 << 2) | (1 << 0),
        (1 << 2) | (1 << 1),
        (1 << 2) | (1 << 3),
    }
    assert closures["B"] == {
        (1 << 0) | (1 << 1),
        (1 << 0) | (1 << 3),
        (1 << 1) | (1 << 3),
    }

    core = [
        f"python={platform.python_version()}",
        "n=9,m=4,target=5+0i",
        f"units={UNITS}",
        f"gcds={gcds}",
        f"image_sizes={{'A': {len(images['A'])}, 'B': {len(images['B'])}}}",
        f"fiber_A={format_counter(fibers['A'])}",
        f"fiber_B={format_counter(fibers['B'])}",
        f"unit_closure_A={format_set(closures['A'])}",
        f"unit_closure_B={format_set(closures['B'])}",
        f"divisible_pair_counts={pair_counts}",
        f"affine_orbit_size_A={len(affine_orbit(AXES['A']))}",
        "symmetry_robust_intersection=empty",
    ]
    audit_hash = sha256(("\n".join(core) + "\n").encode()).hexdigest()
    print("\n".join(core))
    print(f"audit_stream_sha256={audit_hash}")
    print("symmetry_robust_obstruction=verified")


if __name__ == "__main__":
    main()
