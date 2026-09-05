#!/usr/bin/env python3
"""Exact arithmetic audit for the girth-sensitive cubic-density theorem."""

from fractions import Fraction
import hashlib


G_MAX = 80
A_MAX = 5000


def density_bound(g: int) -> Fraction:
    return Fraction(4 * (g - 1), 5 * g - 3)


def exact_b_max(a: int, g: int) -> int:
    """Largest b permitted by 4b <= a + 2 floor(a/(g-1))."""
    return (a + 2 * (a // (g - 1))) // 4


def audit() -> tuple[int, str]:
    digest = hashlib.sha256()
    profiles = 0

    for g in range(3, G_MAX + 1):
        s = g - 1
        lower = density_bound(g)
        assert lower < 1

        if g > 3:
            assert density_bound(g) > density_bound(g - 1)

        for a in range(1, A_MAX + 1):
            q_max = a // s
            rhs = a + 2 * q_max
            b_max = exact_b_max(a, g)

            # Independent maximization over all possible component counts q.
            brute = max((a + 2 * q) // 4 for q in range(q_max + 1))
            assert b_max == brute
            assert 4 * b_max <= rhs < 4 * (b_max + 1)

            # Cross-multiplied rational consequence a/(a+b) >= bound.
            assert a * (5 * g - 3) >= (a + b_max) * 4 * (g - 1)

            record = f"{g},{a},{q_max},{rhs},{b_max}\n".encode("ascii")
            digest.update(record)
            profiles += 1

    assert density_bound(3) == Fraction(2, 3)
    assert density_bound(5) == Fraction(8, 11)
    assert density_bound(6) == Fraction(20, 27)
    assert density_bound(G_MAX) < Fraction(4, 5)

    return profiles, digest.hexdigest()


def main() -> None:
    profiles, stream_hash = audit()
    print(f"audited profiles: {profiles}")
    print(f"range: 3 <= g <= {G_MAX}, 1 <= a <= {A_MAX}")
    print("exact bound: 4b <= a + 2 floor(a/(g-1))")
    print("g=3 density: 2/3")
    print("g=5 density: 8/11")
    print("g=6 density: 20/27")
    print(f"profile stream sha256: {stream_hash}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
