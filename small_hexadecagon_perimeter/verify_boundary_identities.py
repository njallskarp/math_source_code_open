#!/usr/bin/env python3
"""Exact SymPy audit of the boundary-envelope derivatives."""

from __future__ import annotations

import json

import sympy as sp


def verify() -> dict[str, object]:
    x = sp.symbols("x", real=True)
    n = sp.Integer(16)
    h = 2 * sp.sin(x / 2)
    envelope = h + 2 * (n - 1) * sp.sin((sp.pi - x) / (2 * (n - 1)))
    expected_first = sp.cos(x / 2) - sp.cos((sp.pi - x) / (2 * (n - 1)))
    expected_second = (
        -sp.sin(x / 2) / 2
        - sp.sin((sp.pi - x) / (2 * (n - 1))) / (2 * (n - 1))
    )
    if sp.trigsimp(sp.diff(envelope, x) - expected_first) != 0:
        raise AssertionError("first-derivative identity failed")
    if sp.trigsimp(sp.diff(envelope, x, 2) - expected_second) != 0:
        raise AssertionError("second-derivative identity failed")
    if sp.trigsimp(sp.diff(h, x, 2) + sp.sin(x / 2) / 2) != 0:
        raise AssertionError("strong-concavity identity failed")
    stationary = sp.solve(sp.Eq(x / 2, (sp.pi - x) / (2 * (n - 1))), x)
    if stationary != [sp.pi / n]:
        raise AssertionError("unexpected envelope stationary point")
    return {
        "exact_symbolic_identities": True,
        "coefficient_domain": "QQ(pi) with analytic sin/cos",
        "envelope_stationary_point": "pi/16",
        "envelope_strict_concavity_on_open_simplex": True,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
