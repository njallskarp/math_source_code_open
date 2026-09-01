#!/usr/bin/env python3
"""Dependency-free rational certificate for the saturation inequalities."""

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


def cos_partial(x: Fraction, last_index: int) -> Fraction:
    term = Fraction(1)
    total = term
    for k in range(1, last_index + 1):
        term *= -x * x / ((2 * k - 1) * (2 * k))
        total += term
    return total


def cos_interval(
    lower: Fraction, upper: Fraction, pairs: int
) -> tuple[Fraction, Fraction]:
    """Enclose cos([lower,upper]) for 0 <= lower <= upper <= 1."""
    if not (0 <= lower <= upper <= 1):
        raise ValueError("the monotone alternating cosine enclosure needs [0,1]")
    return cos_partial(upper, 2 * pairs + 1), cos_partial(lower, 2 * pairs)


def decimal_string(value: Fraction, digits: int = 36) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def verify() -> dict[str, object]:
    data = json.loads((HERE / "saturation_certificate.json").read_text())
    threshold = rational(data["perimeter_threshold"])
    deficit_claim = rational(data["difference_body_deficit_upper"])
    omega_lower = rational(data["normal_cone_width_lower"])
    omega_upper = rational(data["normal_cone_width_upper"])
    radius_lower = rational(data["radius_lower"])
    delta_upper = rational(data["normal_radial_offset_upper"])
    separation_claim = rational(data["projective_separation_lower"])
    ratio_claim = rational(data["tangent_ratio_upper"])
    projective_claim = rational(data["kkt_projective_distance_upper"])
    sine_pairs = int(data["sine_series_pairs"])
    pi_lower, pi_upper = pi_interval(int(data["machin_arctan_pairs"]))

    sin_pi_32 = sin_interval(pi_lower / 32, pi_upper / 32, sine_pairs)
    deficit_upper = 64 * sin_pi_32[1] - 2 * threshold
    if not 0 < deficit_upper < deficit_claim:
        raise AssertionError("candidate-level difference-body deficit failed")

    def normal_cone_envelope(t: Fraction) -> tuple[Fraction, Fraction]:
        first = sin_interval(t / 2, t / 2, sine_pairs)
        second = sin_interval(
            (2 * pi_lower - t) / 62,
            (2 * pi_upper - t) / 62,
            sine_pairs,
        )
        return 2 * first[0] + 62 * second[0], 2 * first[1] + 62 * second[1]

    lower_envelope = normal_cone_envelope(omega_lower)
    upper_envelope = normal_cone_envelope(omega_upper)
    if not lower_envelope[1] < 2 * threshold:
        raise AssertionError("lower normal-cone cut is not excluded")
    if not upper_envelope[1] < 2 * threshold:
        raise AssertionError("upper normal-cone cut is not excluded")

    sin_half_omega_lower = sin_interval(
        omega_lower / 2, omega_lower / 2, sine_pairs
    )
    radial_loss_lower = (
        2 * (1 - radius_lower) * sin_half_omega_lower[0]
    )
    if not radial_loss_lower > deficit_upper:
        raise AssertionError("radius localization failed")

    cos_delta = cos_interval(delta_upper, delta_upper, sine_pairs)
    angular_loss_lower = (
        2
        * radius_lower
        * sin_half_omega_lower[0]
        * (1 - cos_delta[1])
    )
    if not angular_loss_lower > deficit_upper:
        raise AssertionError("normal-radial angular localization failed")

    separation_lower = omega_lower - 2 * delta_upper
    if not separation_lower >= separation_claim:
        raise AssertionError("projective separation lower bound failed")

    sin_half_omega_upper = sin_interval(
        omega_upper / 2, omega_upper / 2, sine_pairs
    )
    sin_delta = sin_interval(delta_upper, delta_upper, sine_pairs)
    tangent_ratio_upper = (
        sin_half_omega_upper[1]
        * sin_delta[1]
        / sin_half_omega_lower[0]
    )
    if not tangent_ratio_upper < ratio_claim:
        raise AssertionError("KKT tangent ratio failed")

    kkt_projective_upper = pi_upper * tangent_ratio_upper / 2 + delta_upper
    if not kkt_projective_upper < projective_claim:
        raise AssertionError("KKT projective-distance bound failed")
    if not projective_claim < separation_claim:
        raise AssertionError("the final projective contradiction has no margin")

    return {
        "rational_certificate": True,
        "difference_body_deficit_upper": decimal_string(deficit_upper, 24),
        "lower_cone_cut_margin_lower": decimal_string(
            2 * threshold - lower_envelope[1], 24
        ),
        "upper_cone_cut_margin_lower": decimal_string(
            2 * threshold - upper_envelope[1], 24
        ),
        "radial_exclusion_margin_lower": decimal_string(
            radial_loss_lower - deficit_upper, 24
        ),
        "angular_exclusion_margin_lower": decimal_string(
            angular_loss_lower - deficit_upper, 24
        ),
        "projective_separation_lower": decimal_string(separation_lower, 12),
        "tangent_ratio_upper": decimal_string(tangent_ratio_upper, 24),
        "kkt_projective_distance_upper": decimal_string(
            kkt_projective_upper, 24
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
