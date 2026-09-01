#!/usr/bin/env python3
"""Dependency-free rational certificate for the perimeter boundary band."""

from __future__ import annotations

import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rational(text: str) -> Fraction:
    return Fraction(text)


def arctan_interval_reciprocal(denominator: int, pairs: int) -> tuple[Fraction, Fraction]:
    """Alternating-series enclosure of atan(1/denominator)."""
    x = Fraction(1, denominator)
    upper = Fraction(0)
    for k in range(2 * pairs + 1):
        term = x ** (2 * k + 1) / (2 * k + 1)
        upper += term if k % 2 == 0 else -term
    next_k = 2 * pairs + 1
    lower = upper - x ** (2 * next_k + 1) / (2 * next_k + 1)
    return lower, upper


def pi_interval(pairs: int) -> tuple[Fraction, Fraction]:
    """Machin: pi = 16 atan(1/5) - 4 atan(1/239)."""
    a_lower, a_upper = arctan_interval_reciprocal(5, pairs)
    b_lower, b_upper = arctan_interval_reciprocal(239, pairs)
    return 16 * a_lower - 4 * b_upper, 16 * a_upper - 4 * b_lower


def sin_partial(x: Fraction, last_index: int) -> Fraction:
    term = x
    total = term
    for k in range(1, last_index + 1):
        term *= -x * x / ((2 * k) * (2 * k + 1))
        total += term
    return total


def sin_interval(
    lower: Fraction, upper: Fraction, pairs: int
) -> tuple[Fraction, Fraction]:
    """Enclose sin([lower,upper]) for 0 <= lower <= upper <= 1."""
    if not (0 <= lower <= upper <= 1):
        raise ValueError("the monotone alternating sine enclosure needs [0,1]")
    lower_value = sin_partial(lower, 2 * pairs + 1)
    upper_value = sin_partial(upper, 2 * pairs)
    return lower_value, upper_value


def envelope_interval(
    x: Fraction,
    n: int,
    pi_bounds: tuple[Fraction, Fraction],
    sine_pairs: int,
) -> tuple[Fraction, Fraction]:
    """Enclose 2 sin(x/2)+2(n-1)sin((pi-x)/(2(n-1)))."""
    pi_lower, pi_upper = pi_bounds
    first_lower, first_upper = sin_interval(x / 2, x / 2, sine_pairs)
    second_lower, second_upper = sin_interval(
        (pi_lower - x) / (2 * (n - 1)),
        (pi_upper - x) / (2 * (n - 1)),
        sine_pairs,
    )
    return (
        2 * first_lower + 2 * (n - 1) * second_lower,
        2 * first_upper + 2 * (n - 1) * second_upper,
    )


def decimal_string(value: Fraction, digits: int = 36) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def verify() -> dict[str, object]:
    data = json.loads((HERE / "boundary_certificate.json").read_text())
    n = int(data["n"])
    threshold = rational(data["perimeter_threshold"])
    lower_gap = rational(data["gap_lower"])
    upper_gap = rational(data["gap_upper"])
    l2_bound = rational(data["squared_l2_radius_upper"])
    volume_bound = rational(data["simplex_volume_fraction_upper"])
    sine_pairs = int(data["sine_series_pairs"])
    pi_bounds = pi_interval(int(data["machin_arctan_pairs"]))
    pi_lower, pi_upper = pi_bounds

    if not (16 * lower_gap < pi_lower < pi_upper < 16 * upper_gap):
        raise AssertionError("gap cut points do not straddle pi/16")

    lower_envelope = envelope_interval(lower_gap, n, pi_bounds, sine_pairs)
    upper_envelope = envelope_interval(upper_gap, n, pi_bounds, sine_pairs)
    if not lower_envelope[1] < threshold:
        raise AssertionError("lower endpoint envelope is not below threshold")
    if not upper_envelope[1] < threshold:
        raise AssertionError("upper endpoint envelope is not below threshold")

    # The capped-simplex volume formula after y_j=delta_j-lower_gap.
    width = upper_gap - lower_gap
    shifted_sum_lower = pi_lower - n * lower_gap
    shifted_sum_upper = pi_upper - n * lower_gap
    if not shifted_sum_lower - 8 * width > 0:
        raise AssertionError("the inclusion-exclusion truncation misses k=8")
    if not shifted_sum_upper - 9 * width < 0:
        raise AssertionError("the inclusion-exclusion truncation needs k=9")
    numerator_lower = Fraction(0)
    numerator_upper = Fraction(0)
    for k in range(9):
        term_lower = math.comb(n, k) * (shifted_sum_lower - k * width) ** (n - 1)
        term_upper = math.comb(n, k) * (shifted_sum_upper - k * width) ** (n - 1)
        if k % 2 == 0:
            numerator_lower += term_lower
            numerator_upper += term_upper
        else:
            numerator_lower -= term_upper
            numerator_upper -= term_lower
    if not numerator_lower > 0:
        raise AssertionError("capped-simplex volume lower bound is not positive")
    volume_ratio_upper = numerator_upper / pi_lower ** (n - 1)
    if not volume_ratio_upper < volume_bound:
        raise AssertionError("capped-simplex volume bound failed")

    # Strong concavity of h(x)=2 sin(x/2) on the certified band.
    sine_alpha_lower, _ = sin_interval(lower_gap / 2, lower_gap / 2, sine_pairs)
    regular_sine = sin_interval(pi_lower / (2 * n), pi_upper / (2 * n), sine_pairs)
    regular_perimeter_upper = 2 * n * regular_sine[1]
    squared_l2_upper = 4 * (regular_perimeter_upper - threshold) / sine_alpha_lower
    if not squared_l2_upper < l2_bound:
        raise AssertionError("squared L2 concentration bound failed")

    return {
        "rational_certificate": True,
        "pi_interval_width_upper": decimal_string(pi_upper - pi_lower, 12),
        "lower_endpoint_margin_lower": decimal_string(
            threshold - lower_envelope[1], 18
        ),
        "upper_endpoint_margin_lower": decimal_string(
            threshold - upper_envelope[1], 18
        ),
        "simplex_volume_fraction_upper": decimal_string(volume_ratio_upper, 18),
        "squared_l2_radius_upper": decimal_string(squared_l2_upper, 18),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
