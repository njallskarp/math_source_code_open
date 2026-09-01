#!/usr/bin/env python3
"""Independent Arb verification of the fixed-code uniqueness constants."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx

HERE = Path(__file__).resolve().parent


def verify() -> dict[str, object]:
    data = json.loads((HERE / "uniqueness_certificate.json").read_text())
    ctx.prec = int(data["arb_precision_bits"])
    lower_gap = arb(data["gap_lower"])
    upper_gap = arb(data["gap_upper"])
    radius_squared = arb(data["squared_l2_radius_upper"])
    claimed_m = arb(data["strong_convexity_lower"])
    claimed_sigma = arb(data["constraint_singular_value_lower"])
    claimed_gradient = arb(data["gradient_norm_upper"])
    claimed_multiplier = arb(data["multiplier_norm_upper"])
    claimed_margin = arb(data["uniqueness_margin_lower"])

    signs = [1 if symbol == "+" else -1 for symbol in data["half_code"]]
    if len(signs) != 16 or any(symbol not in "+-" for symbol in data["half_code"]):
        raise ValueError("the half code must contain sixteen signs")
    coefficients = [signs[j - 1] - signs[j] for j in range(1, 16)]
    switches = [j for j, coefficient in enumerate(coefficients, start=1) if coefficient]
    if switches != [1, 3, 4, 5, 7, 8, 9, 11, 12, 13, 15]:
        raise AssertionError("unexpected switch set")
    if any(abs(coefficient) != 2 for coefficient in coefficients if coefficient):
        raise AssertionError("unexpected closure coefficient")

    sin_pi_32 = (arb.pi() / 32).sin()
    radius = radius_squared.sqrt()
    strong_convexity = 2 * (lower_gap / 2).sin() * sin_pi_32**2
    path_coordinate_norm = radius / (2 * sin_pi_32)
    z_modulus = 1 + 2 * arb(11).sqrt() * path_coordinate_norm
    sigma_squared = 2 * (11 - z_modulus)
    sigma = sigma_squared.sqrt()
    gradient = (upper_gap / 2).sin() * radius
    multiplier = gradient / sigma
    margin = strong_convexity - 2 * multiplier

    if not strong_convexity > claimed_m:
        raise AssertionError("strong-convexity lower bound failed")
    if not sigma_squared > 0:
        raise AssertionError("constraint singular-value lower bound failed")
    if not sigma > claimed_sigma:
        raise AssertionError("constraint singular-value lower bound failed")
    if not gradient < claimed_gradient:
        raise AssertionError("objective-gradient upper bound failed")
    if not multiplier < claimed_multiplier:
        raise AssertionError("KKT multiplier upper bound failed")
    if not margin > claimed_margin:
        raise AssertionError("the two-point uniqueness margin is not positive")

    return {
        "arb_certificate": True,
        "precision_bits": ctx.prec,
        "switch_set": switches,
        "strong_convexity": strong_convexity.str(30),
        "path_coordinate_norm": path_coordinate_norm.str(30),
        "z_modulus_upper": z_modulus.str(30),
        "constraint_singular_value": sigma.str(30),
        "gradient_norm_upper": gradient.str(30),
        "multiplier_norm_upper": multiplier.str(30),
        "uniqueness_margin": margin.str(30),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
