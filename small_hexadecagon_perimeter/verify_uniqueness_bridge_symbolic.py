#!/usr/bin/env python3
"""Dependency-free rational certificate for the fixed-code uniqueness bridge.

The mathematical interpretation is documented in README.md.  This checker
does no floating-point arithmetic: pi comes from Machin's formula, sine from
alternating Taylor sums, and square roots from integer square roots.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

from verify_boundary_band_symbolic import pi_interval, sin_interval


HERE = Path(__file__).resolve().parent


def rational(text: str) -> Fraction:
    return Fraction(text)


def sqrt_interval(value: Fraction, decimal_digits: int) -> tuple[Fraction, Fraction]:
    """Return adjacent decimal rationals enclosing sqrt(value)."""
    if value < 0:
        raise ValueError("square root requires a nonnegative rational")
    scale = 10**decimal_digits
    quotient = value.numerator * scale * scale // value.denominator
    floor_scaled_root = math.isqrt(quotient)
    lower = Fraction(floor_scaled_root, scale)
    upper = Fraction(floor_scaled_root + 1, scale)
    if not lower * lower <= value < upper * upper:
        raise AssertionError("integer square-root enclosure failed")
    return lower, upper


def decimal_string(value: Fraction, digits: int = 36) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def switch_set(code: str) -> tuple[list[int], list[int]]:
    signs = [1 if symbol == "+" else -1 for symbol in code]
    if len(signs) != 16 or any(symbol not in "+-" for symbol in code):
        raise ValueError("the half code must contain sixteen signs")
    coefficients = [signs[j - 1] - signs[j] for j in range(1, 16)]
    switches = [j for j, coefficient in enumerate(coefficients, start=1) if coefficient]
    return switches, coefficients


def verify() -> dict[str, object]:
    data = json.loads((HERE / "uniqueness_certificate.json").read_text())
    if int(data["n"]) != 16:
        raise AssertionError("this certificate is specialized to n=16")

    lower_gap = rational(data["gap_lower"])
    upper_gap = rational(data["gap_upper"])
    radius_squared = rational(data["squared_l2_radius_upper"])
    claimed_m = rational(data["strong_convexity_lower"])
    claimed_sigma = rational(data["constraint_singular_value_lower"])
    claimed_gradient = rational(data["gradient_norm_upper"])
    claimed_multiplier = rational(data["multiplier_norm_upper"])
    claimed_margin = rational(data["uniqueness_margin_lower"])
    sine_pairs = int(data["sine_series_pairs"])
    sqrt_digits = int(data["sqrt_decimal_digits"])
    pi_lower, pi_upper = pi_interval(int(data["machin_arctan_pairs"]))

    switches, coefficients = switch_set(data["half_code"])
    expected_switches = [1, 3, 4, 5, 7, 8, 9, 11, 12, 13, 15]
    if switches != expected_switches:
        raise AssertionError("unexpected switch set")
    if any(abs(coefficient) != 2 for coefficient in coefficients if coefficient):
        raise AssertionError("nonzero closure coefficients must have magnitude two")
    # At regular angles zeta=exp(i*pi/8), the complement of the switch set
    # in {1,...,15} is {2,6,10,14}.  Those four roots sum to zero, while all
    # fifteen nontrivial sixteenth roots sum to -1.  Hence Z_0=-1 exactly.
    if sorted(set(range(1, 16)) - set(switches)) != [2, 6, 10, 14]:
        raise AssertionError("regular root-of-unity cancellation failed")

    sin_a_half_lower, _ = sin_interval(
        lower_gap / 2, lower_gap / 2, sine_pairs
    )
    sin_b_half = sin_interval(upper_gap / 2, upper_gap / 2, sine_pairs)
    sin_pi_32 = sin_interval(pi_lower / 32, pi_upper / 32, sine_pairs)

    # H_f >= (sin(alpha/2)/2) D^T D and
    # lambda_min(D^T D)=4 sin^2(pi/32) for the 15-vertex Dirichlet path.
    strong_convexity_lower = (
        2 * sin_a_half_lower * sin_pi_32[0] * sin_pi_32[0]
    )
    if not strong_convexity_lower > claimed_m:
        raise AssertionError("strong-convexity lower bound failed")

    _, radius_upper = sqrt_interval(radius_squared, sqrt_digits)
    _, sqrt_eleven_upper = sqrt_interval(Fraction(11), sqrt_digits)

    # x_j=delta_j-pi/16 and s_j=sum_{k<j}x_k obey
    # ||s|| <= ||x||/(2 sin(pi/32)).  If
    # Z=sum_{j in S} exp(2 i phi_j), then |Z| <= 1+2 sqrt(11)||s||.
    path_coordinate_norm_upper = radius_upper / (2 * sin_pi_32[0])
    z_modulus_upper = (
        1 + 2 * sqrt_eleven_upper * path_coordinate_norm_upper
    )
    sigma_squared_lower = 2 * (11 - z_modulus_upper)
    if not sigma_squared_lower > 0:
        raise AssertionError("constraint rank lower bound is nonpositive")
    sigma_lower, _ = sqrt_interval(sigma_squared_lower, sqrt_digits)
    if not sigma_lower > claimed_sigma:
        raise AssertionError("constraint singular-value lower bound failed")

    # grad f is a first difference of cos(delta_j/2).  The incidence norm is
    # at most 2 and |d cos(t/2)/dt| <= sin(beta/2)/2.
    gradient_upper = sin_b_half[1] * radius_upper
    if not gradient_upper < claimed_gradient:
        raise AssertionError("objective-gradient upper bound failed")

    multiplier_upper = gradient_upper / sigma_lower
    if not multiplier_upper < claimed_multiplier:
        raise AssertionError("KKT multiplier upper bound failed")

    # Each closure coefficient has magnitude two.  Taylor's 1/2 factor turns
    # ||D^2 g[d,d]|| <= 2||d||^2 into ||Jd|| <= ||d||^2 at feasible endpoints.
    uniqueness_margin_lower = strong_convexity_lower - 2 * multiplier_upper
    if not uniqueness_margin_lower > claimed_margin:
        raise AssertionError("the two-point uniqueness margin is not positive")

    return {
        "rational_certificate": True,
        "switch_set": switches,
        "strong_convexity_lower": decimal_string(strong_convexity_lower, 24),
        "path_coordinate_norm_upper": decimal_string(
            path_coordinate_norm_upper, 24
        ),
        "z_modulus_upper": decimal_string(z_modulus_upper, 24),
        "constraint_singular_value_lower": decimal_string(sigma_lower, 24),
        "gradient_norm_upper": decimal_string(gradient_upper, 24),
        "multiplier_norm_upper": decimal_string(multiplier_upper, 24),
        "uniqueness_margin_lower": decimal_string(uniqueness_margin_lower, 24),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
