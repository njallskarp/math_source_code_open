#!/usr/bin/env python3
"""Independent 512-bit Arb comparison for the strict 32-edge reduction."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


HERE = Path(__file__).resolve().parent


def verify() -> dict[str, object]:
    data = json.loads((HERE / "strict_edge_certificate.json").read_text())
    ctx.prec = int(data["arb_precision_bits"])
    threshold = arb(data["candidate_perimeter_lower"])
    m = int(data["largest_nonstrict_difference_body_edge_count"])
    regular_half_perimeter = m * (arb.pi() / m).sin()
    claimed_upper = arb(data["regular_30_half_perimeter_upper"])
    claimed_margin = arb(data["candidate_margin_lower"])
    margin = threshold - regular_half_perimeter
    if not regular_half_perimeter < claimed_upper < threshold:
        raise AssertionError("Arb regular 30-gon comparison failed")
    if not margin > claimed_margin:
        raise AssertionError("Arb candidate margin failed")
    return {
        "arb_strict_edge_certificate": True,
        "precision_bits": ctx.prec,
        "regular_30_half_perimeter": regular_half_perimeter.str(40),
        "candidate_margin": margin.str(40),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
