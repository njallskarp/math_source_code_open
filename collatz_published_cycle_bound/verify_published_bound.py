#!/usr/bin/env python3
"""Exact certificate for the 2025 published Collatz cycle-length bound.

The only analytic input is the conditional interval

    log_2(3) < N/K < log_2(3) + 1/(3*A*ln(2)),

with A = 4.37e21.  Hercher's Corollary 29 computation targets this
mean-reciprocal bound; Barina reports the resulting cycle-length bound.

All logarithm comparisons below use rational interval arithmetic.  There is
no floating-point arithmetic and no construction of enormous integer powers.
"""

from fractions import Fraction


A = 4_370_000_000_000_000_000_000

# A lower convergent, the claimed least-denominator admissible upper
# convergent, and the preceding upper semiconvergent of log_2(3).
LOWER = Fraction(103_768_467_013, 65_470_613_321)
TARGET = Fraction(217_976_794_617, 137_528_045_312)
PREVIOUS_UPPER = Fraction(114_208_327_604, 72_057_431_991)


def log_bounds(x: Fraction, terms: int = 120) -> tuple[Fraction, Fraction]:
    """Return rigorous rational lower/upper bounds for ln(x), x > 0.

    We use

        ln(x) = 2 * sum_{k>=0} z^(2k+1)/(2k+1),
        z = (x-1)/(x+1),

    and bound the positive tail by replacing every remaining denominator by
    its first value and summing the resulting geometric series.
    """

    if x <= 0:
        raise ValueError("x must be positive")
    z = (x - 1) / (x + 1)
    if abs(z) >= 1:
        raise ValueError("atanh series requires |z| < 1")

    partial = Fraction(0)
    z_power = z
    z_squared = z * z
    for k in range(terms):
        partial += 2 * z_power / (2 * k + 1)
        z_power *= z_squared

    tail_upper = 2 * z_power / ((2 * terms + 1) * (1 - z_squared))
    return partial, partial + tail_upper


def certify() -> dict[str, int | bool]:
    ln2_lo, ln2_hi = log_bounds(Fraction(2))
    ln3_lo, ln3_hi = log_bounds(Fraction(3))
    interval_increment_after_multiplying_by_ln2 = Fraction(1, 3 * A)

    lower_is_below_log2_3 = (
        LOWER.numerator * ln2_hi < LOWER.denominator * ln3_lo
    )
    target_is_above_log2_3 = (
        TARGET.numerator * ln2_lo > TARGET.denominator * ln3_hi
    )
    target_is_below_interval_top = (
        TARGET.numerator * ln2_hi
        < TARGET.denominator
        * (ln3_lo + interval_increment_after_multiplying_by_ln2)
    )
    previous_upper_is_above_interval_top = (
        PREVIOUS_UPPER.numerator * ln2_lo
        > PREVIOUS_UPPER.denominator
        * (ln3_hi + interval_increment_after_multiplying_by_ln2)
    )

    # These determinant-one identities are compact Farey-neighbor
    # certificates.  Any rational strictly between either neighbor pair has
    # denominator at least the sum of the two denominators.
    lower_target_determinant = (
        TARGET.numerator * LOWER.denominator
        - LOWER.numerator * TARGET.denominator
    )
    target_previous_upper_determinant = (
        PREVIOUS_UPPER.numerator * TARGET.denominator
        - TARGET.numerator * PREVIOUS_UPPER.denominator
    )

    target_numerator_is_ceiling = (
        (TARGET.numerator - 1) * ln2_hi < TARGET.denominator * ln3_lo
        and target_is_above_log2_3
    )

    checks = {
        "lower_is_below_log2_3": lower_is_below_log2_3,
        "target_is_above_log2_3": target_is_above_log2_3,
        "target_is_below_interval_top": target_is_below_interval_top,
        "previous_upper_is_above_interval_top": previous_upper_is_above_interval_top,
        "lower_target_determinant": lower_target_determinant,
        "target_previous_upper_determinant": target_previous_upper_determinant,
        "target_numerator_is_ceiling": target_numerator_is_ceiling,
    }
    assert all(value is True or value == 1 for value in checks.values())

    result: dict[str, int | bool] = dict(checks)
    result.update(
        {
            "minimum_odd_entries": TARGET.denominator,
            "minimum_shortcut_entries": TARGET.numerator,
            "minimum_classical_entries": TARGET.numerator + TARGET.denominator,
        }
    )
    return result


if __name__ == "__main__":
    for name, value in certify().items():
        print(f"{name}={value}")
