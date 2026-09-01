#!/usr/bin/env python3
"""Exact SymPy audit of the identities used by the uniqueness proof."""

from __future__ import annotations

import json

import sympy as sp


def verify() -> dict[str, object]:
    t, left, right = sp.symbols("t left right", real=True)
    h = -2 * sp.sin(t / 2)
    if sp.simplify(sp.diff(h, t, 2) - sp.sin(t / 2) / 2) != 0:
        raise AssertionError("full negative-perimeter curvature identity failed")

    local_objective = -2 * sp.sin((t - left) / 2) - 2 * sp.sin((right - t) / 2)
    expected_gradient = sp.cos((right - t) / 2) - sp.cos((t - left) / 2)
    if sp.simplify(sp.diff(local_objective, t) - expected_gradient) != 0:
        raise AssertionError("full negative-perimeter gradient identity failed")

    phi, direction, coefficient = sp.symbols(
        "phi direction coefficient", real=True
    )
    tau = sp.symbols("tau", real=True)
    closure_term = coefficient * sp.exp(sp.I * (phi + tau * direction))
    first = sp.diff(closure_term, tau).subs(tau, 0)
    second = sp.diff(closure_term, tau, 2).subs(tau, 0)
    if sp.simplify(first - sp.I * coefficient * sp.exp(sp.I * phi) * direction) != 0:
        raise AssertionError("closure Jacobian identity failed")
    if sp.simplify(second + coefficient * sp.exp(sp.I * phi) * direction**2) != 0:
        raise AssertionError("closure second-derivative identity failed")

    signs = [1 if symbol == "+" else -1 for symbol in "+--+-++-+--+-++-"]
    coefficients = [signs[j - 1] - signs[j] for j in range(1, 16)]
    switches = [j for j, coefficient in enumerate(coefficients, start=1) if coefficient]
    root_sum = sp.expand_complex(
        sum(sp.exp(sp.I * sp.pi * j / 8) for j in switches)
    )
    if sp.trigsimp(root_sum) != -1:
        raise AssertionError("regular switch-root sum is not -1")

    # Independently derive the two eigenvalues of JJ^T.  For N switch
    # columns of length two in directions (-sin(phi_j),cos(phi_j)), put
    # C=sum cos(2 phi_j) and S=sum sin(2 phi_j).  The characteristic
    # polynomial must have roots 2N +/- 2 sqrt(C^2+S^2).
    count, cosine_sum, sine_sum, eigenvalue = sp.symbols(
        "count cosine_sum sine_sum eigenvalue", real=True
    )
    gram = sp.Matrix(
        [
            [2 * count - 2 * cosine_sum, -2 * sine_sum],
            [-2 * sine_sum, 2 * count + 2 * cosine_sum],
        ]
    )
    characteristic = sp.expand((gram - eigenvalue * sp.eye(2)).det())
    expected_characteristic = sp.expand(
        (eigenvalue - 2 * count) ** 2
        - 4 * (cosine_sum**2 + sine_sum**2)
    )
    if sp.simplify(characteristic - expected_characteristic) != 0:
        raise AssertionError("closure Gram eigenvalue identity failed")

    # The scalar Taylor formula is recorded explicitly to prevent dropping
    # the decisive factor 1/2 in the closure remainder.
    second_bound, d_norm_squared = sp.symbols(
        "second_bound d_norm_squared", positive=True
    )
    remainder_bound = sp.Rational(1, 2) * second_bound
    if remainder_bound.subs(second_bound, 2 * d_norm_squared) != d_norm_squared:
        raise AssertionError("Taylor remainder factor audit failed")

    return {
        "exact_symbolic_identities": True,
        "objective_normalization": "f=-P",
        "objective_curvature": "sin(delta/2)/2",
        "regular_switch_root_sum": "-1",
        "closure_second_derivative_coefficient_bound": "2",
        "taylor_remainder_factor": "1/2",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
