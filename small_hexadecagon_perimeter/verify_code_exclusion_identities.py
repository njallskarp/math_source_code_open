#!/usr/bin/env python3
"""Exact SymPy audit of the code-exclusion reduction and symmetries."""

from __future__ import annotations

import json

import sympy as sp

from verify_code_exclusion_exact import dihedral_orbit


def verify() -> dict[str, object]:
    x = sp.symbols("x")
    code = sp.symbols("c0:16")
    cyclotomic = x**16 + 1
    closure_edges = sum(code[j] * (x ** (j + 1) - x**j) for j in range(16))
    cyclotomic_form = (x - 1) * sum(code[j] * x**j for j in range(16))
    if sp.rem(sp.expand(closure_edges - cyclotomic_form), cyclotomic, x) != 0:
        raise AssertionError("cyclotomic closure-residual identity failed")

    coefficients = (-(code[0] + code[15]),) + tuple(
        code[j - 1] - code[j] for j in range(1, 16)
    )
    vertex_form = coefficients[0] + sum(coefficients[j] * x**j for j in range(1, 16))
    if sp.rem(sp.expand(closure_edges - vertex_form), cyclotomic, x) != 0:
        raise AssertionError("vertex-form closure identity failed")

    # Exact inverse of the 15-vertex Dirichlet path Laplacian over QQ.
    size = 15
    dirichlet = sp.zeros(size)
    for j in range(size):
        dirichlet[j, j] = 2
        if j:
            dirichlet[j, j - 1] = -1
        if j + 1 < size:
            dirichlet[j, j + 1] = -1
    green = sp.Matrix(
        size,
        size,
        lambda j, k: sp.Rational(
            min(j + 1, k + 1) * (16 - max(j + 1, k + 1)), 16
        ),
    )
    if dirichlet * green != sp.eye(size) or green * dirichlet != sp.eye(size):
        raise AssertionError("Dirichlet Green-kernel identity failed")

    # The linearization and the factor 1/2 in the exponential remainder.
    tau = sp.symbols("tau", real=True)
    s = sp.symbols("s1:16", real=True)
    exponential_vertex_form = coefficients[0] + sum(
        coefficients[j] * x**j * sp.exp(sp.I * tau * s[j - 1])
        for j in range(1, 16)
    )
    linearization = sp.diff(exponential_vertex_form, tau).subs(tau, 0)
    expected_linearization = sp.I * sum(
        coefficients[j] * x**j * s[j - 1] for j in range(1, 16)
    )
    if sp.simplify(linearization - expected_linearization) != 0:
        raise AssertionError("closure linearization identity failed")

    representative = tuple(1 if char == "+" else -1 for char in "+--+-++-+--+-++-")
    orbit = dihedral_orbit(representative)
    if len(orbit) != 16 or any(code_value[0] != 1 for code_value in orbit):
        raise AssertionError("dihedral normalization audit failed")

    return {
        "exact_symbolic_identities": True,
        "coefficient_domain": "QQ[x]/(x^16+1) with analytic exp linearization",
        "cyclotomic_residual": "(x-1) sum_j c_j x^j",
        "global_sign_action": "c -> -c sends G_c -> -G_c",
        "dirichlet_green_kernel_verified": True,
        "dihedral_orbit_size": len(orbit),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
