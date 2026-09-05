#!/usr/bin/env python3
"""Exact arithmetic audit for the order-2k equality-scope obstruction."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def ore_parameters(k: int, leaves: int) -> tuple[int, int]:
    """Order and size after a binary Ore-composition tree with `leaves` K_k leaves."""
    require(k >= 3, "k must be at least 3")
    require(leaves >= 1, "the composition tree must have a leaf")
    clique_edges = k * (k - 1) // 2
    return 1 + leaves * (k - 1), leaves * (clique_edges - 1) + 1


def recursive_ore_parameters(k: int, leaves: int) -> tuple[int, int]:
    """Independently replay the composition recurrences using a balanced split."""
    if leaves == 1:
        return k, k * (k - 1) // 2
    left = leaves // 2
    right = leaves - left
    n_left, m_left = recursive_ore_parameters(k, left)
    n_right, m_right = recursive_ore_parameters(k, right)
    return n_left + n_right - 1, m_left + m_right - 1


def ky_raw_floor(k: int, n: int) -> Fraction:
    numerator = (k + 1) * (k - 2) * n - k * (k - 3)
    return Fraction(numerator, 2 * (k - 1))


def ceiling(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def row_record(k: int, t: int) -> dict[str, int | Fraction]:
    n = 2 * k
    m = k * k - 3 + t
    excess = 2 * m - (k - 1) * n
    potential = (k - 2) * (k + 1) * n - 2 * (k - 1) * m
    ore_potential = k * (k - 3)
    deficit = ore_potential - potential
    raw_floor = ky_raw_floor(k, n)
    return {
        "n": n,
        "m": m,
        "excess": excess,
        "potential": potential,
        "deficit": deficit,
        "raw_floor": raw_floor,
        "rounded_floor": ceiling(raw_floor),
        "integer_gap": m - ceiling(raw_floor),
        "raw_gap": Fraction(m) - raw_floor,
    }


def main() -> None:
    records: list[str] = []

    for k in range(3, 101):
        for leaves in range(1, 33):
            closed = ore_parameters(k, leaves)
            replay = recursive_ore_parameters(k, leaves)
            require(closed == replay, "Ore recurrence mismatch")
            require((closed[0] - 1) % (k - 1) == 0, "Ore order congruence failed")
        require((2 * k - 1) % (k - 1) != 0, "order 2k unexpectedly is an Ore order")

        for t in range(3):
            row = row_record(k, t)
            require(row["excess"] == 2 * k - 6 + 2 * t, "excess identity failed")
            require(
                row["potential"] == 2 * k - 6 - 2 * (k - 1) * t,
                "potential identity failed",
            )
            require(
                row["deficit"] == (k - 2) * (k - 3) + 2 * (k - 1) * t,
                "potential-deficit identity failed",
            )
            require(
                row["raw_gap"] == Fraction(row["deficit"], 2 * (k - 1)),
                "raw edge-gap identity failed",
            )

    for leaves in range(1, 5):
        n, m = ore_parameters(29, leaves)
        line = f"ore k=29 leaves={leaves} n={n} m={m}"
        records.append(line)
        print(line)

    for t in range(3):
        row = row_record(29, t)
        raw_floor = row["raw_floor"]
        raw_gap = row["raw_gap"]
        line = (
            f"row t={t} n={row['n']} m={row['m']} X={row['excess']} "
            f"rho={row['potential']} delta={row['deficit']} "
            f"KY_raw={raw_floor.numerator}/{raw_floor.denominator} "
            f"KY_ceil={row['rounded_floor']} integer_gap={row['integer_gap']} "
            f"raw_gap={raw_gap.numerator}/{raw_gap.denominator}"
        )
        records.append(line)
        print(line)

    certificate = sha256(("\n".join(records) + "\n").encode()).hexdigest()
    print(f"certificate_sha256={certificate}")


if __name__ == "__main__":
    main()
