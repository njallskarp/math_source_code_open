#!/usr/bin/env python3
"""Independent Arb verification of the angle-gap boundary certificate."""

from __future__ import annotations

import json
import math
from pathlib import Path

from flint import arb, ctx


HERE = Path(__file__).resolve().parent


def verify() -> dict[str, object]:
    data = json.loads((HERE / "boundary_certificate.json").read_text())
    ctx.prec = int(data["arb_precision_bits"])
    n = int(data["n"])
    threshold = arb(data["perimeter_threshold"])
    lower_gap = arb(data["gap_lower"])
    upper_gap = arb(data["gap_upper"])
    l2_bound = arb(data["squared_l2_radius_upper"])
    volume_bound = arb(data["simplex_volume_fraction_upper"])
    pi = arb.pi()

    def envelope(x: arb) -> arb:
        return 2 * (x / 2).sin() + 2 * (n - 1) * (
            (pi - x) / (2 * (n - 1))
        ).sin()

    lower_value = envelope(lower_gap)
    upper_value = envelope(upper_gap)
    if not (16 * lower_gap < pi < 16 * upper_gap):
        raise AssertionError("gap cut points do not straddle pi/16")
    if not lower_value < threshold:
        raise AssertionError("lower endpoint envelope is not below threshold")
    if not upper_value < threshold:
        raise AssertionError("upper endpoint envelope is not below threshold")

    width = upper_gap - lower_gap
    shifted_sum = pi - n * lower_gap
    if not shifted_sum - 8 * width > 0:
        raise AssertionError("the inclusion-exclusion truncation misses k=8")
    if not shifted_sum - 9 * width < 0:
        raise AssertionError("the inclusion-exclusion truncation needs k=9")
    numerator = arb(0)
    for k in range(9):
        numerator += (
            (-1) ** k
            * math.comb(n, k)
            * (shifted_sum - k * width) ** (n - 1)
        )
    volume_ratio = numerator / pi ** (n - 1)
    if not (volume_ratio > 0 and volume_ratio < volume_bound):
        raise AssertionError("capped-simplex volume bound failed")

    regular_perimeter = 2 * n * (pi / (2 * n)).sin()
    squared_l2_radius = 4 * (regular_perimeter - threshold) / (lower_gap / 2).sin()
    if not squared_l2_radius < l2_bound:
        raise AssertionError("squared L2 concentration bound failed")

    return {
        "arb_certificate": True,
        "precision_bits": ctx.prec,
        "lower_endpoint_margin": (threshold - lower_value).str(24),
        "upper_endpoint_margin": (threshold - upper_value).str(24),
        "simplex_volume_fraction": volume_ratio.str(24),
        "squared_l2_radius": squared_l2_radius.str(24),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
