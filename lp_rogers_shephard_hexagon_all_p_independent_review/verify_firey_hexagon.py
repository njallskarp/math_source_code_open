#!/usr/bin/env python3
"""Independent symbolic and numerical checks for the Firey hexagon formula.

The symbolic layer works in characteristic zero over rational-function
identities in independent symbols, with the displayed normalization relations
checked as explicit residuals.  The numerical layer reconstructs the Firey
body directly as a circumscribed polygon from sampled support half-planes; it
does not use the target's sector-area formula for the reconstruction.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform

import mpmath as mp
import sympy as sp


def symbolic_checks() -> list[str]:
    a, b, alpha, beta, ell, c, arc = sp.symbols(
        "a b alpha beta L c S", positive=True
    )
    q, t, u = sp.symbols("q t u", positive=True)

    # The two endpoints of the intervening exposed face.
    p_vec = sp.Matrix([a * alpha - beta, (1 + b) * alpha])
    q_vec = sp.Matrix([-(1 + a) * beta, alpha - b * beta])
    det_pq = sp.det(sp.Matrix.hstack(p_vec, q_vec))
    expected_j = a * alpha**2 + (a + b) * alpha * beta + b * beta**2
    assert sp.expand(det_pq - expected_j) == 0
    assert sp.expand(expected_j - (alpha + beta) * (a * alpha + b * beta)) == 0

    # Area assembly and deficit subtraction.
    j = ell * (alpha + beta)
    area = (1 + a) + (1 + b) + j + (1 + b) * arc + (1 + a) * (c - arc)
    deficit = (2 + c) * (1 + a + b) - area
    expected_deficit = a + b - j + a * arc + b * (c - arc)
    assert sp.expand(deficit - expected_deficit) == 0

    # Differentiate D=t+u-alpha-beta+tS+u(c-S) using the endpoint identities.
    dt = -(q - 1) * u / alpha
    du = (q - 1) * u / beta
    dalpha = -u / t
    darc = 1 / t
    derivative = (
        dt
        + du
        - dalpha
        - 1
        + dt * arc
        + t * darc
        + du * (c - arc)
        - u * darc
    )
    claimed_derivative = (q - 1) * u / beta * (
        (1 + c - arc) - beta / alpha * (1 + arc)
    )
    assert sp.cancel(derivative - claimed_derivative) == 0

    # S'=1/t has residual (alpha*t+beta*u-1)/t before normalization.
    arc_derivative_residual = sp.factor(alpha + beta * u / t - 1 / t)
    assert arc_derivative_residual == (alpha * t + beta * u - 1) / t

    # New sharp upper estimate: if t>=u, S<=beta/t.  Substitution leaves
    # t^2-(t*alpha+u*beta)=t^2-1 after t*alpha+u*beta=1.
    upper_residual = t - alpha - beta + (t - u) * beta / t
    assert sp.cancel(upper_residual - (t - alpha - u * beta / t)) == 0
    normalized_residual = sp.expand(t * upper_residual - (t**2 - 1))
    assert normalized_residual == 1 - alpha * t - beta * u

    return [
        "determinant_and_factorization=OK",
        "area_and_deficit_assembly=OK",
        "deficit_derivative=OK",
        "arc_derivative_normalization=OK",
        "sharp_upper_bound_reduction=OK",
    ]


def support_value(theta: float, p: float, a: float, b: float) -> float:
    x = math.cos(theta)
    y = math.sin(theta)
    middle = a * x + b * y
    h_k = max(x, 0.0) + max(middle, 0.0) + max(y, 0.0)
    h_minus_k = max(-x, 0.0) + max(-middle, 0.0) + max(-y, 0.0)
    return (h_k**p + h_minus_k**p) ** (1.0 / p)


def circumscribed_support_area(p: float, a: float, b: float, n: int) -> float:
    """Area of the polygon cut out by n equally spaced support half-planes."""
    delta = 2.0 * math.pi / n
    corner = math.pi / 2 + math.atan2(b, a)
    candidates = [i * delta for i in range(n)]
    candidates.extend([corner, (corner + math.pi) % (2 * math.pi)])
    candidates.sort()
    normals: list[float] = []
    for theta in candidates:
        if not normals or theta - normals[-1] > 1.0e-13:
            normals.append(theta)

    def vertex(i: int) -> tuple[float, float]:
        theta = normals[i]
        theta_next = normals[(i + 1) % len(normals)]
        if theta_next <= theta:
            theta_next += 2 * math.pi
        c0, s0 = math.cos(theta), math.sin(theta)
        c1, s1 = math.cos(theta_next), math.sin(theta_next)
        det = math.sin(theta_next - theta)
        h0 = support_value(theta, p, a, b)
        h1 = support_value(theta_next, p, a, b)
        return (
            (h0 * s1 - h1 * s0) / det,
            (-h0 * c1 + h1 * c0) / det,
        )

    first = vertex(0)
    previous = first
    twice_area = 0.0
    for i in range(1, len(normals)):
        current = vertex(i)
        twice_area += previous[0] * current[1] - previous[1] * current[0]
        previous = current
    twice_area += previous[0] * first[1] - previous[1] * first[0]
    return 0.5 * twice_area


def formula_values(p: float, a: float, b: float) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    p_mp = mp.mpf(str(p))
    a_mp = mp.mpf(str(a))
    b_mp = mp.mpf(str(b))
    q = p_mp / (p_mp - 1)
    ell = (a_mp**p_mp + b_mp**p_mp) ** (1 / p_mp)
    t, u = a_mp / ell, b_mp / ell
    alpha, beta = t ** (p_mp - 1), u ** (p_mp - 1)
    c_q = 2 * mp.gamma(1 + 1 / q) ** 2 / mp.gamma(1 + 2 / q)
    arc = 2 * mp.quad(lambda y: (1 - y**q) ** (1 / q), [0, beta]) - alpha * beta
    j = ell * (alpha + beta)
    area = (1 + a_mp) + (1 + b_mp) + j + (1 + b_mp) * arc + (1 + a_mp) * (c_q - arc)
    deficit = (2 + c_q) * (1 + a_mp + b_mp) - area
    return area, deficit, c_q


def numerical_checks() -> tuple[list[dict[str, str]], str]:
    cases = [
        (1.10, 1.0, 1.0),
        (1.25, 4.0, 0.2),
        (1.50, 0.3, 2.7),
        (2.00, 1.0, 1.0),
        (3.00, 2.0, 0.5),
        (10.0, 7.0, 4.0),
    ]
    records: list[dict[str, str]] = []
    for p, a, b in cases:
        predicted, deficit, c_q = formula_values(p, a, b)
        area_low = circumscribed_support_area(p, a, b, 131072)
        area_high = circumscribed_support_area(p, a, b, 262144)
        error_low = abs(area_low - float(predicted))
        error_high = abs(area_high - float(predicted))
        if not (error_high < error_low and error_high < 1.0e-7):
            raise AssertionError((p, a, b, error_low, error_high))
        if not deficit > 0:
            raise AssertionError((p, a, b, "nonpositive deficit"))
        if p >= 2:
            scale = min(mp.mpf(str(a)), mp.mpf(str(b)))
            if not (c_q * scale <= deficit < (1 + c_q) * scale):
                raise AssertionError((p, a, b, "sharp stability bound failed"))
        records.append(
            {
                "p": f"{p:.2f}",
                "a": f"{a:.2f}",
                "b": f"{b:.2f}",
                "formula_area": f"{float(predicted):.12f}",
                "halfplane_area_262144": f"{area_high:.12f}",
                "abs_error_262144": f"{error_high:.3e}",
                "deficit": f"{float(deficit):.12f}",
            }
        )
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return records, hashlib.sha256(canonical.encode()).hexdigest()


def main() -> None:
    mp.mp.dps = 60
    print(f"Python={platform.python_version()}")
    print(f"SymPy={sp.__version__}")
    print(f"mpmath={mp.__version__}")
    for line in symbolic_checks():
        print(line)
    records, digest = numerical_checks()
    for record in records:
        print(
            "case "
            + " ".join(f"{key}={value}" for key, value in record.items())
        )
    print(f"numerical_cases_sha256={digest}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
