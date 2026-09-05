#!/usr/bin/env python3
"""Independent closed-form audit of the two Gallai packing gaps."""

from __future__ import annotations

from hashlib import sha256


def phi(u: int) -> int:
    return u * (u + 1) // 2


def main() -> None:
    # n=50, sum of block increments at most 49.
    n50_cases = {
        "K26_no_K25_or_K24": phi(25) + phi(22) + phi(2),
        "one_K25_one_K24": phi(24) + phi(23) + phi(2),
        "one_K25_no_K24": phi(24) + phi(22) + phi(3),
        "no_K26_or_K25": 2 * phi(23) + phi(3),
    }
    n50_above = {
        "two_K25": 2 * phi(24),
        "K26_plus_K24": phi(25) + phi(23),
    }
    assert max(n50_cases.values()) == 581
    assert min(n50_above.values()) == 600

    # n=49, sum of block increments at most 48.
    n49_cases = {
        "K26_no_clique_K23_or_larger": phi(25) + phi(21) + phi(2),
        "one_K25_no_K24": phi(24) + phi(22) + phi(2),
        "no_K26_or_K25": 2 * phi(23) + phi(2),
    }
    n49_above = {
        "K26_plus_K23": phi(25) + phi(22),
        "K25_plus_K24": phi(24) + phi(23),
        "two_K25": 2 * phi(24),
    }
    assert max(n49_cases.values()) == 559
    assert min(n49_above.values()) == 576

    # The degree identity is checked without profile-specific table data.
    assert 769 - (5 * 27 + 53) + 1 == 582
    assert 769 - (5 * 27 + 53) + 10 == 591
    assert 769 - (6 * 27 + 53) + 6 == 560
    assert 769 - (6 * 27 + 53) + 15 == 569

    lines = [
        "PASS independent Gallai spectrum-gap audit",
        "n=50 below_max=581 above_min=600 forbidden=582..599",
        "n=49 below_max=559 above_min=576 forbidden=560..575",
        "degree_identity nlow=50 eL=581+eR eR=1..10 gives=582..591",
        "degree_identity nlow=49 eL=554+eR eR=6..15 gives=560..569",
    ]
    digest = sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    lines.append(f"audit_sha256={digest}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
