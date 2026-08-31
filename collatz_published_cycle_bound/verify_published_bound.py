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

# The lower convergent after TARGET and the next upper semiconvergent.  They
# describe the next discrete jump in the same Diophantine method.
NEXT_LOWER = Fraction(1_193_652_440_098, 753_110_839_881)
NEXT_TARGET = Fraction(1_411_629_234_715, 890_638_885_193)


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


def reciprocal_threshold_bounds(
    upper: Fraction,
    ln2_lo: Fraction,
    ln2_hi: Fraction,
    ln3_lo: Fraction,
    ln3_hi: Fraction,
) -> tuple[Fraction, Fraction]:
    """Bound A where delta + 1/(3*A*ln(2)) equals ``upper``.

    The exact threshold is q/(3*(p*ln(2)-q*ln(3))) for upper = p/q.
    """

    difference_lo = upper.numerator * ln2_lo - upper.denominator * ln3_hi
    difference_hi = upper.numerator * ln2_hi - upper.denominator * ln3_lo
    assert difference_lo > 0
    return (
        Fraction(upper.denominator, 3 * difference_hi),
        Fraction(upper.denominator, 3 * difference_lo),
    )


def enclosing_consecutive_integers(bounds: tuple[Fraction, Fraction]) -> tuple[int, int]:
    lower, upper = bounds
    floor_lower = lower.numerator // lower.denominator
    ceil_upper = -(-upper.numerator // upper.denominator)
    assert floor_lower + 1 == ceil_upper
    return floor_lower, ceil_upper


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

    next_lower_is_below_log2_3 = (
        NEXT_LOWER.numerator * ln2_hi < NEXT_LOWER.denominator * ln3_lo
    )
    next_target_is_above_log2_3 = (
        NEXT_TARGET.numerator * ln2_lo > NEXT_TARGET.denominator * ln3_hi
    )
    next_farey_determinant = (
        NEXT_TARGET.numerator * NEXT_LOWER.denominator
        - NEXT_LOWER.numerator * NEXT_TARGET.denominator
    )

    entry_floor, entry_ceiling = enclosing_consecutive_integers(
        reciprocal_threshold_bounds(
            PREVIOUS_UPPER, ln2_lo, ln2_hi, ln3_lo, ln3_hi
        )
    )
    target_floor, target_ceiling = enclosing_consecutive_integers(
        reciprocal_threshold_bounds(TARGET, ln2_lo, ln2_hi, ln3_lo, ln3_hi)
    )
    next_floor, next_ceiling = enclosing_consecutive_integers(
        reciprocal_threshold_bounds(NEXT_TARGET, ln2_lo, ln2_hi, ln3_lo, ln3_hi)
    )

    checks = {
        "lower_is_below_log2_3": lower_is_below_log2_3,
        "target_is_above_log2_3": target_is_above_log2_3,
        "target_is_below_interval_top": target_is_below_interval_top,
        "previous_upper_is_above_interval_top": previous_upper_is_above_interval_top,
        "lower_target_determinant": lower_target_determinant,
        "target_previous_upper_determinant": target_previous_upper_determinant,
        "target_numerator_is_ceiling": target_numerator_is_ceiling,
        "next_lower_is_below_log2_3": next_lower_is_below_log2_3,
        "next_target_is_above_log2_3": next_target_is_above_log2_3,
        "next_farey_determinant": next_farey_determinant,
    }
    assert all(value is True or value == 1 for value in checks.values())

    result: dict[str, int | bool] = dict(checks)
    result.update(
        {
            "minimum_odd_entries": TARGET.denominator,
            "minimum_shortcut_entries": TARGET.numerator,
            "minimum_classical_entries": TARGET.numerator + TARGET.denominator,
            "current_phase_entry_threshold_floor": entry_floor,
            "current_phase_entry_threshold_ceiling": entry_ceiling,
            "next_phase_entry_threshold_floor": target_floor,
            "next_phase_entry_threshold_ceiling": target_ceiling,
            "next_phase_exit_threshold_floor": next_floor,
            "next_phase_exit_threshold_ceiling": next_ceiling,
            "next_phase_minimum_odd_entries": NEXT_TARGET.denominator,
            "next_phase_minimum_shortcut_entries": NEXT_TARGET.numerator,
            "next_phase_minimum_classical_entries": (
                NEXT_TARGET.numerator + NEXT_TARGET.denominator
            ),
        }
    )
    return result


if __name__ == "__main__":
    for name, value in certify().items():
        print(f"{name}={value}")
