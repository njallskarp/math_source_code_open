#!/usr/bin/env python3
"""Exact-arithmetic verifier for a current lower bound on Collatz cycles."""

import json


# Barina (2025): every positive starting value n < 2^71 reaches 1.
BARINA_EXCLUSIVE_LIMIT = 1 << 71

# Corrected Hercher (2023), Corollary 29: X_0 at least this threshold
# implies more than 1.375e11 odd entries in every nontrivial shortcut cycle.
HERCHER_X0_THRESHOLD = 1536 * (1 << 60)
HERCHER_STRICT_ODD_BOUND = 137_500_000_000

# Rational bounds on log_2(3), certified without floating point by exact
# integer comparisons.  They are tailored to determine floor(K*log_2(3))
# at the smallest K allowed by Hercher's strict odd-entry bound.
LOG2_3_LOWER_NUMERATOR = 1_686_221
LOG2_3_LOWER_DENOMINATOR = 1_063_887
LOG2_3_UPPER_NUMERATOR = 301_994
LOG2_3_UPPER_DENOMINATOR = 190_537


def verify() -> dict[str, int | bool]:
    x0_from_barina = BARINA_EXCLUSIVE_LIMIT - 1
    assert x0_from_barina >= HERCHER_X0_THRESHOLD

    odd_entries_min = HERCHER_STRICT_ODD_BOUND + 1

    p = LOG2_3_LOWER_NUMERATOR
    q = LOG2_3_LOWER_DENOMINATOR
    assert pow(3, q) > pow(2, p)

    upper_p = LOG2_3_UPPER_NUMERATOR
    upper_q = LOG2_3_UPPER_DENOMINATOR
    assert pow(3, upper_q) < pow(2, upper_p)

    # If K and L are the odd- and even-entry counts for Hercher's shortcut
    # map, going once around a cycle gives 2^(K+L) > 3^K.  The certified
    # rational lower bound log_2(3) > p/q therefore gives K+L > pK/q.
    lower_floor = (p * odd_entries_min) // q
    upper_floor = (upper_p * odd_entries_min) // upper_q
    assert lower_floor == upper_floor
    shortcut_entries_min = lower_floor + 1
    assert q * (shortcut_entries_min - 1) <= p * odd_entries_min
    assert q * shortcut_entries_min > p * odd_entries_min

    # Each odd shortcut transition represents two transitions of the
    # classical map, while each even shortcut transition represents one.
    classical_entries_min = shortcut_entries_min + odd_entries_min

    expected = {
        "barina_exclusive_limit": 2_361_183_241_434_822_606_848,
        "hercher_x0_threshold": 1_770_887_431_076_116_955_136,
        "odd_entries_min": 137_500_000_001,
        "shortcut_entries_min": 217_932_343_851,
        "classical_entries_min": 355_432_343_852,
    }
    actual = {
        "barina_exclusive_limit": BARINA_EXCLUSIVE_LIMIT,
        "hercher_x0_threshold": HERCHER_X0_THRESHOLD,
        "odd_entries_min": odd_entries_min,
        "shortcut_entries_min": shortcut_entries_min,
        "classical_entries_min": classical_entries_min,
    }
    assert actual == expected

    return {
        **actual,
        "barina_implies_hercher_hypothesis": True,
        "exact_log_product_floor_certified": True,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
