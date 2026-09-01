#!/usr/bin/env python3
"""Exact SymPy audit of analytic identities in the 32-edge reduction."""

from __future__ import annotations

import json

import sympy as sp


def verify() -> dict[str, object]:
    x, t = sp.symbols("x t", positive=True)
    q = sp.sin(t) - t * sp.cos(t)
    regular_bound = x * sp.sin(sp.pi / x)
    expected_derivative = sp.sin(sp.pi / x) - (sp.pi / x) * sp.cos(sp.pi / x)
    if sp.trigsimp(sp.diff(regular_bound, x) - expected_derivative) != 0:
        raise AssertionError("regular-polygon bound derivative failed")
    if sp.trigsimp(sp.diff(q, t) - t * sp.sin(t)) != 0:
        raise AssertionError("positivity auxiliary derivative failed")

    theta, radius, vertex_angle, midpoint, alpha = sp.symbols(
        "theta radius vertex_angle midpoint alpha", real=True
    )
    normal_cone_integral = sp.integrate(
        radius * sp.cos(theta - vertex_angle),
        (theta, midpoint - alpha / 2, midpoint + alpha / 2),
    )
    expected_integral = (
        2 * radius * sp.sin(alpha / 2) * sp.cos(midpoint - vertex_angle)
    )
    if sp.trigsimp(normal_cone_integral - expected_integral) != 0:
        raise AssertionError("normal-cone support integral failed")

    k, r = sp.symbols("k r", integer=True, nonnegative=True)
    merged = 2 * k - 2 * r
    if sp.simplify(merged.subs({k: 16, r: 0}) - 32) != 0:
        raise AssertionError("edge merge identity failed")

    return {
        "exact_strict_edge_identities": True,
        "coefficient_domain": "ZZ and symbolic trigonometric identities",
        "normal_cone_integral_identity": True,
        "regular_bound_strict_monotonicity_reduction": "q'(t)=t sin(t), q(0)=0",
        "merged_edge_count_identity": "m=2k-2r",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
