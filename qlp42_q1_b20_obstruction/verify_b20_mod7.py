#!/usr/bin/env python3
"""Independent exact mod-7 obstruction for the q=1, b=20 QLP-42 branch."""

from __future__ import annotations

from itertools import product
from pathlib import Path

G = tuple[int, int]
LENGTH = 21
QUOTIENT = 7
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def multiply_conjugate(left: G, right: G) -> G:
    return (
        left[0] * right[0] + left[1] * right[1],
        left[1] * right[0] - left[0] * right[1],
    )


def root_sum_domain(count: int) -> tuple[G, ...]:
    formula = {
        (real, imag)
        for real in range(-count, count + 1)
        for imag in range(-count, count + 1)
        if abs(real) + abs(imag) <= count
        and (real + imag - count) % 2 == 0
    }
    reachable = {(0, 0)}
    for _ in range(count):
        reachable = {add(partial, root) for partial in reachable for root in ROOTS}
    assert formula == reachable
    return tuple(sorted(formula))


def derive_target() -> tuple[tuple[int, ...], tuple[int, ...]]:
    original = (20,) + (-1,) * (LENGTH - 1)
    compressed = tuple(
        sum(original[residue + QUOTIENT * block] for block in range(3))
        for residue in range(QUOTIENT)
    )
    assert compressed == (18,) + (-3,) * (QUOTIENT - 1)
    return original, compressed


def periodic_correlation(word: tuple[G, ...], shift: int) -> G:
    terms = (
        multiply_conjugate(word[index], word[(index + shift) % len(word)])
        for index in range(len(word))
    )
    return tuple(map(sum, zip(*terms, strict=True)))


def main() -> None:
    _, target = derive_target()
    d2 = root_sum_domain(2)
    d3 = root_sum_domain(3)
    d3_set = set(d3)
    counts = {
        "sum_zero_tuples": 0,
        "energy_18_tuples": 0,
        "shift_1_tuples": 0,
        "shifts_1_2_tuples": 0,
    }

    for first in d2:
        for middle in product(d3, repeat=5):
            prefix = (first, *middle)
            last = (
                -sum(value[0] for value in prefix),
                -sum(value[1] for value in prefix),
            )
            if last not in d3_set:
                continue
            word = (*prefix, last)
            counts["sum_zero_tuples"] += 1
            if sum(real * real + imag * imag for real, imag in word) != target[0]:
                continue
            counts["energy_18_tuples"] += 1
            if periodic_correlation(word, 1) != (target[1], 0):
                continue
            counts["shift_1_tuples"] += 1
            if periodic_correlation(word, 2) != (target[2], 0):
                continue
            counts["shifts_1_2_tuples"] += 1

    assert counts == {
        "sum_zero_tuples": 2_795_584,
        "energy_18_tuples": 60_024,
        "shift_1_tuples": 656,
        "shifts_1_2_tuples": 0,
    }
    output = [
        f"d2_size={len(d2)}",
        f"d3_size={len(d3)}",
        f"raw_domain_tuples={len(d2) * len(d3) ** 6}",
        *(f"{name}={value}" for name, value in counts.items()),
        "solutions=0",
        "certificate=verified",
    ]
    assert (Path(__file__).parent / "verification_output.txt").read_text(
        encoding="utf-8"
    ) == "\n".join(output) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
