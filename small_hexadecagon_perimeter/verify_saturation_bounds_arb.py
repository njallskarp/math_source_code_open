#!/usr/bin/env python3
"""Independent 512-bit Arb verification of the saturation inequalities."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


HERE = Path(__file__).resolve().parent


def verify() -> dict[str, object]:
    data = json.loads((HERE / "saturation_certificate.json").read_text())
    ctx.prec = int(data["arb_precision_bits"])
    threshold = arb(data["perimeter_threshold"])
    deficit_claim = arb(data["difference_body_deficit_upper"])
    omega_lower = arb(data["normal_cone_width_lower"])
    omega_upper = arb(data["normal_cone_width_upper"])
    radius_lower = arb(data["radius_lower"])
    delta_upper = arb(data["normal_radial_offset_upper"])
    separation_claim = arb(data["projective_separation_lower"])
    ratio_claim = arb(data["tangent_ratio_upper"])
    projective_claim = arb(data["kkt_projective_distance_upper"])
    pi = arb.pi()

    deficit = 64 * (pi / 32).sin() - 2 * threshold
    if not (deficit > 0 and deficit < deficit_claim):
        raise AssertionError("candidate-level difference-body deficit failed")

    def normal_cone_envelope(t: arb) -> arb:
        return 2 * (t / 2).sin() + 62 * ((2 * pi - t) / 62).sin()

    lower_envelope = normal_cone_envelope(omega_lower)
    upper_envelope = normal_cone_envelope(omega_upper)
    if not lower_envelope < 2 * threshold:
        raise AssertionError("lower normal-cone cut is not excluded")
    if not upper_envelope < 2 * threshold:
        raise AssertionError("upper normal-cone cut is not excluded")

    radial_loss = 2 * (1 - radius_lower) * (omega_lower / 2).sin()
    angular_loss = (
        2
        * radius_lower
        * (omega_lower / 2).sin()
        * (1 - delta_upper.cos())
    )
    if not radial_loss > deficit:
        raise AssertionError("radius localization failed")
    if not angular_loss > deficit:
        raise AssertionError("normal-radial angular localization failed")

    separation = omega_lower - 2 * delta_upper
    ratio = (
        (omega_upper / 2).sin()
        / (omega_lower / 2).sin()
        * delta_upper.sin()
    )
    projective = pi * ratio / 2 + delta_upper
    if not separation >= separation_claim:
        raise AssertionError("projective separation lower bound failed")
    if not ratio < ratio_claim:
        raise AssertionError("KKT tangent ratio failed")
    if not projective < projective_claim < separation_claim:
        raise AssertionError("final projective contradiction failed")

    return {
        "arb_certificate": True,
        "precision_bits": ctx.prec,
        "difference_body_deficit": deficit.str(30),
        "lower_cone_cut_margin": (2 * threshold - lower_envelope).str(30),
        "upper_cone_cut_margin": (2 * threshold - upper_envelope).str(30),
        "radial_exclusion_margin": (radial_loss - deficit).str(30),
        "angular_exclusion_margin": (angular_loss - deficit).str(30),
        "projective_separation": separation.str(30),
        "tangent_ratio": ratio.str(30),
        "kkt_projective_distance": projective.str(30),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
