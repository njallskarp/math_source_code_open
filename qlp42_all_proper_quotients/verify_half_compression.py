#!/usr/bin/env python3
"""Classify the length-two compressions of a norm-32 QLP-42 residual.

The even and odd positions form the two cells of the quotient modulo two.
This verifier derives every possible pair of Gaussian cell sums and then
quotients the list by symmetries that preserve the real residual target.
"""

from __future__ import annotations

from collections import deque

HALF_LENGTH = 21
TOTAL_PSD = 86

# Representatives (alpha_even.real, alpha_even.imag,
#                  beta_even.real, beta_even.imag).
REPRESENTATIVES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)


def is_sum_of_21_roots(real: int, imag: int) -> bool:
    """The diamond-and-parity criterion for a sum of 21 fourth roots."""

    return (
        abs(real) + abs(imag) <= HALF_LENGTH
        and (real + imag - HALF_LENGTH) % 2 == 0
    )


def eligible(compression: tuple[int, int, int, int]) -> bool:
    p, q, x, y = compression
    return (
        is_sum_of_21_roots(p, q)
        and is_sum_of_21_roots(-p, -q)
        and is_sum_of_21_roots(x, y)
        and is_sum_of_21_roots(1 - x, 1 - y)
        and 4 * (p * p + q * q) + (2 * x - 1) ** 2 + (2 * y - 1) ** 2
        == TOTAL_PSD
    )


def generators(
    compression: tuple[int, int, int, int],
) -> tuple[tuple[int, int, int, int], ...]:
    p, q, x, y = compression
    return (
        # Multiply A by i.  A has sum zero, so its phase is free.
        (-q, p, x, y),
        # Shift both sequences by one place, swapping even and odd cells.
        (-p, -q, 1 - x, 1 - y),
        # Conjugate both sequences and multiply B by i to restore sum 1+i.
        (p, -q, y, x),
    )


def orbit(seed: tuple[int, int, int, int]) -> frozenset[tuple[int, int, int, int]]:
    found = {seed}
    pending = deque([seed])
    while pending:
        current = pending.popleft()
        for image in generators(current):
            if image not in found:
                found.add(image)
                pending.append(image)
    return frozenset(found)


def main() -> None:
    # The PSD equation bounds every coordinate by five, but use the natural
    # cell-sum range so the finite classification does not rely on that
    # observation.
    solutions = {
        (p, q, x, y)
        for p in range(-HALF_LENGTH, HALF_LENGTH + 1)
        for q in range(-HALF_LENGTH, HALF_LENGTH + 1)
        for x in range(-HALF_LENGTH, HALF_LENGTH + 1)
        for y in range(-HALF_LENGTH, HALF_LENGTH + 1)
        if eligible((p, q, x, y))
    }
    assert len(solutions) == 88

    representative_orbits = [orbit(representative) for representative in REPRESENTATIVES]
    assert all(representative in solutions for representative in REPRESENTATIVES)
    assert all(current <= solutions for current in representative_orbits)
    assert all(
        left.isdisjoint(right)
        for index, left in enumerate(representative_orbits)
        for right in representative_orbits[index + 1 :]
    )
    assert set().union(*representative_orbits) == solutions

    norms = sorted({p * p + q * q for p, q, _, _ in solutions})
    assert norms == [1, 9, 13, 17]
    print("eligible_labeled_compressions=88")
    print("symmetry_orbits=6")
    print("alpha_even_squared_norms=" + repr(norms))
    for index, representative in enumerate(REPRESENTATIVES):
        print(
            f"orbit_{index}_representative={representative}; "
            f"size={len(representative_orbits[index])}"
        )
    print("half-compression classification passed")


if __name__ == "__main__":
    main()
