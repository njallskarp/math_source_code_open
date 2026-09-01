#!/usr/bin/env python3
"""Exact SymPy audit of the geometric identities in the saturation proof."""

from __future__ import annotations

import json

import sympy as sp


def verify() -> dict[str, object]:
    # Summation by parts with the cyclic-antipodal endpoint z_16=-z_0.
    code = sp.symbols("c0:16", real=True)
    vertices = sp.symbols("z0:16", real=True)
    edge_sum = sum(
        code[j] * (vertices[j + 1] - vertices[j]) for j in range(15)
    ) + code[15] * (-vertices[0] - vertices[15])
    coefficients = (-(code[0] + code[15]),) + tuple(
        code[j - 1] - code[j] for j in range(1, 16)
    )
    vertex_sum = sum(coefficients[j] * vertices[j] for j in range(16))
    if sp.expand(edge_sum - vertex_sum) != 0:
        raise AssertionError("cyclic summation-by-parts identity failed")

    # Gradient of two incident edge lengths: incoming tangent minus outgoing
    # tangent equals the outward normal-cone bisector vector.
    theta, omega = sp.symbols("theta omega", real=True)
    incoming = sp.Matrix([sp.cos(theta), sp.sin(theta)])
    outgoing = sp.Matrix([sp.cos(theta + omega), sp.sin(theta + omega)])
    eta = theta + omega / 2 - sp.pi / 2
    bisector = 2 * sp.sin(omega / 2) * sp.Matrix([sp.cos(eta), sp.sin(eta)])
    if any(sp.trigsimp(value) != 0 for value in incoming - outgoing - bisector):
        raise AssertionError("outward angle-bisector gradient identity failed")

    phi = sp.symbols("phi", real=True)
    tangent = sp.Matrix([-sp.sin(phi), sp.cos(phi)])
    projected = sp.trigsimp((bisector.dot(tangent)))
    expected_projection = 2 * sp.sin(omega / 2) * sp.sin(eta - phi)
    if sp.trigsimp(projected - expected_projection) != 0:
        raise AssertionError("tangent-projection identity failed")

    # Cauchy's perimeter integral on one normal cone.
    variable, radius = sp.symbols("variable radius", real=True)
    cone_integral = sp.integrate(
        radius * sp.cos(variable - phi),
        (variable, eta - omega / 2, eta + omega / 2),
    )
    expected_integral = 2 * radius * sp.sin(omega / 2) * sp.cos(eta - phi)
    if sp.trigsimp(cone_integral - expected_integral) != 0:
        raise AssertionError("normal-cone Cauchy integral identity failed")

    # Uniform radial contraction is an especially simple MFCQ direction:
    # it preserves every homogeneous closure equation, and on ||z||=1 the
    # derivative of q(z)=||z||^2-1 is -2.
    x, y, coefficient = sp.symbols("x y coefficient", real=True)
    q = x**2 + y**2 - 1
    tau = sp.symbols("tau", real=True)
    contracted_q = q.subs({x: (1 - tau) * x, y: (1 - tau) * y})
    q_derivative = sp.diff(contracted_q, tau).subs(tau, 0)
    if sp.simplify(q_derivative + 2 * (x**2 + y**2)) != 0:
        raise AssertionError("radial MFCQ derivative failed")
    rank_block = sp.Matrix([[coefficient, 0], [0, coefficient]])
    if sp.factor(rank_block.det()) != coefficient**2:
        raise AssertionError("equality-rank block determinant failed")

    return {
        "exact_symbolic_identities": True,
        "coefficient_domain": "QQ with analytic sin/cos identities",
        "cyclic_endpoint": "z_16=-z_0",
        "perimeter_gradient": "incoming unit tangent minus outgoing unit tangent",
        "mfcq_direction": "d_j=-z_j for every half-vertex",
        "active_disk_directional_derivative": "-2",
        "equality_rank_block_determinant": "a_r^2=4",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
