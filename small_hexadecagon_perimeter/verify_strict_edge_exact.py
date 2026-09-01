#!/usr/bin/env python3
"""Dependency-free exact certificate for the strict 32-edge reduction.

The geometric proof is in CONSOLIDATED_AUDIT.md.  This checker verifies the
finite edge-count dichotomy and the only numerical comparison used there.
All proof decisions use integer or Fraction arithmetic.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def arctan_reciprocal_interval(
    denominator: int, pairs: int
) -> tuple[Fraction, Fraction]:
    """Alternating-series enclosure of atan(1/denominator)."""
    x = Fraction(1, denominator)
    upper = sum(
        ((-1) ** k) * x ** (2 * k + 1) / (2 * k + 1)
        for k in range(2 * pairs + 1)
    )
    next_k = 2 * pairs + 1
    lower = upper - x ** (2 * next_k + 1) / (2 * next_k + 1)
    return lower, upper


def pi_interval(pairs: int) -> tuple[Fraction, Fraction]:
    """Machin enclosure pi=16 atan(1/5)-4 atan(1/239)."""
    a_lo, a_hi = arctan_reciprocal_interval(5, pairs)
    b_lo, b_hi = arctan_reciprocal_interval(239, pairs)
    return 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo


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
    """Monotone alternating enclosure of sin([lower,upper]) in [0,1]."""
    if not 0 <= lower <= upper <= 1:
        raise ValueError("sine enclosure requires an interval in [0,1]")
    return sin_partial(lower, 2 * pairs + 1), sin_partial(upper, 2 * pairs)


def edge_count_rows(maximum_edges: int) -> list[tuple[int, int, int]]:
    """Return (k,r,m), where m=2k-2r is the merged edge count.

    Here k is the genuine edge count of P and r is the number of unordered
    antipodal direction pairs in its edge-direction set.  The direction sets
    of P and -P intersect in exactly 2r directions.
    """
    return [
        (k, r, 2 * k - 2 * r)
        for k in range(3, maximum_edges + 1)
        for r in range(k // 2 + 1)
    ]


def verify() -> dict[str, object]:
    data = json.loads((HERE / "strict_edge_certificate.json").read_text())
    boundary = json.loads((HERE / "boundary_certificate.json").read_text())
    threshold = Fraction(data["candidate_perimeter_lower"])
    if threshold != Fraction(boundary["perimeter_threshold"]):
        raise AssertionError("strict-edge threshold is not the certified p0")

    maximum_edges = int(data["maximum_input_edges"])
    maximum_z_edges = int(data["maximum_difference_body_edges"])
    nonstrict_maximum = int(data["largest_nonstrict_difference_body_edge_count"])
    rows = edge_count_rows(maximum_edges)
    for k, antipodal_pairs, merged_edges in rows:
        if merged_edges % 2:
            raise AssertionError("central symmetry did not give an even edge count")
        strict_case = k == maximum_edges and antipodal_pairs == 0
        if strict_case:
            if merged_edges != maximum_z_edges:
                raise AssertionError("the strict case does not have 32 edges")
        elif merged_edges > nonstrict_maximum:
            raise AssertionError("a nonstrict merged edge list exceeds 30 edges")

    pi_lo, pi_hi = pi_interval(int(data["machin_arctan_pairs"]))
    sine_lo, sine_hi = sin_interval(
        pi_lo / nonstrict_maximum,
        pi_hi / nonstrict_maximum,
        int(data["sine_series_pairs"]),
    )
    regular_upper = nonstrict_maximum * sine_hi
    claimed_upper = Fraction(data["regular_30_half_perimeter_upper"])
    claimed_margin = Fraction(data["candidate_margin_lower"])
    if not regular_upper < claimed_upper < threshold:
        raise AssertionError("regular 30-gon half-perimeter upper bound failed")
    if not threshold - regular_upper > claimed_margin:
        raise AssertionError("candidate separation margin failed")

    return {
        "exact_strict_edge_certificate": True,
        "arithmetic": "integer/Fraction Machin-Taylor intervals",
        "edge_count_cases_checked": len(rows),
        "unique_32_edge_case": {"genuine_P_edges": 16, "antipodal_pairs": 0},
        "nonstrict_edge_count_upper": nonstrict_maximum,
        "regular_30_half_perimeter_upper": data[
            "regular_30_half_perimeter_upper"
        ],
        "candidate_margin_lower": data["candidate_margin_lower"],
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
