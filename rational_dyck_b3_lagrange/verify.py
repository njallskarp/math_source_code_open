#!/usr/bin/env python3
"""Exact symbolic verifier for the D(a,3) Lagrange-level theorem.

The coefficient field is Q(phi), phi^2 = phi + 1.  Laurent-polynomial
identities are built from the 2x2 period matrices.  Positivity certificates
are checked coefficient by coefficient after multiplication by positive
monomials and, for the two boundary cases, the substitutions described in
README.md.  Only the Python standard library is used.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable

VARS = ("X", "Y", "Z", "U", "V")
NVAR = len(VARS)
ZERO_EXP = (0,) * NVAR


@dataclass(frozen=True)
class QPhi:
    """a+b*phi in Q(phi), where phi^2=phi+1."""

    a: Fraction
    b: Fraction = Fraction(0)

    def __add__(self, other: object) -> "QPhi":
        other = qphi(other)
        return QPhi(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self) -> "QPhi":
        return QPhi(-self.a, -self.b)

    def __sub__(self, other: object) -> "QPhi":
        return self + (-qphi(other))

    def __rsub__(self, other: object) -> "QPhi":
        return qphi(other) - self

    def __mul__(self, other: object) -> "QPhi":
        if not isinstance(other, (QPhi, int, Fraction)):
            return NotImplemented
        other = qphi(other)
        # phi^2=phi+1
        return QPhi(
            self.a * other.a + self.b * other.b,
            self.a * other.b + self.b * other.a + self.b * other.b,
        )

    __rmul__ = __mul__

    def inverse(self) -> "QPhi":
        # (a+b phi)(a+b-b phi)=a^2+ab-b^2.
        norm = self.a * self.a + self.a * self.b - self.b * self.b
        if norm == 0:
            raise ZeroDivisionError
        return QPhi((self.a + self.b) / norm, -self.b / norm)

    def __truediv__(self, other: object) -> "QPhi":
        return self * qphi(other).inverse()

    def __pow__(self, exponent: int) -> "QPhi":
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        result = ONE_Q
        base = self
        power = exponent
        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1
        return result

    def sign(self) -> int:
        """Return the exact real sign under phi=(1+sqrt(5))/2."""
        # a+b phi = (2a+b+b sqrt(5))/2.
        rational = 2 * self.a + self.b
        radical = self.b
        if radical == 0:
            return (rational > 0) - (rational < 0)
        if radical > 0:
            if rational >= 0:
                return 1
            comparison = 5 * radical * radical - rational * rational
            return (comparison > 0) - (comparison < 0)
        if rational <= 0:
            return -1
        comparison = rational * rational - 5 * radical * radical
        return (comparison > 0) - (comparison < 0)

    def canonical(self) -> list[list[int]]:
        return [
            [self.a.numerator, self.a.denominator],
            [self.b.numerator, self.b.denominator],
        ]


def qphi(value: object) -> QPhi:
    if isinstance(value, QPhi):
        return value
    return QPhi(Fraction(value))


ZERO_Q = QPhi(Fraction(0))
ONE_Q = QPhi(Fraction(1))
PHI = QPhi(Fraction(0), Fraction(1))
LAMBDA = ONE_Q + PHI  # phi^2


class Laurent:
    """Sparse Laurent polynomial over Q(phi) in VARS."""

    def __init__(self, terms: dict[tuple[int, ...], QPhi] | None = None):
        self.terms: dict[tuple[int, ...], QPhi] = {}
        for exponent, coefficient in (terms or {}).items():
            if len(exponent) != NVAR:
                raise ValueError("wrong exponent dimension")
            coefficient = qphi(coefficient)
            if coefficient != ZERO_Q:
                self.terms[exponent] = coefficient

    @staticmethod
    def constant(value: object) -> "Laurent":
        coefficient = qphi(value)
        return Laurent({ZERO_EXP: coefficient}) if coefficient != ZERO_Q else Laurent()

    @staticmethod
    def variable(index: int) -> "Laurent":
        exponent = [0] * NVAR
        exponent[index] = 1
        return Laurent({tuple(exponent): ONE_Q})

    def __add__(self, other: object) -> "Laurent":
        other = poly(other)
        result = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            new = result.get(exponent, ZERO_Q) + coefficient
            if new == ZERO_Q:
                result.pop(exponent, None)
            else:
                result[exponent] = new
        return Laurent(result)

    __radd__ = __add__

    def __neg__(self) -> "Laurent":
        return Laurent({exponent: -coefficient for exponent, coefficient in self.terms.items()})

    def __sub__(self, other: object) -> "Laurent":
        return self + (-poly(other))

    def __rsub__(self, other: object) -> "Laurent":
        return poly(other) - self

    def __mul__(self, other: object) -> "Laurent":
        other = poly(other)
        result: dict[tuple[int, ...], QPhi] = {}
        for left_exp, left_coefficient in self.terms.items():
            for right_exp, right_coefficient in other.terms.items():
                exponent = tuple(a + b for a, b in zip(left_exp, right_exp))
                coefficient = result.get(exponent, ZERO_Q) + left_coefficient * right_coefficient
                if coefficient == ZERO_Q:
                    result.pop(exponent, None)
                else:
                    result[exponent] = coefficient
        return Laurent(result)

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "Laurent":
        if exponent < 0:
            if len(self.terms) != 1:
                raise ValueError("only monomials can have negative powers")
            (monomial, coefficient), = self.terms.items()
            return Laurent({tuple(-e * (-exponent) for e in monomial): coefficient ** exponent})
        result = Laurent.constant(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1
        return result

    def scale(self, coefficient: object) -> "Laurent":
        return self * Laurent.constant(coefficient)

    def substitute_monomials(self, replacements: dict[int, "Laurent"]) -> "Laurent":
        result = Laurent()
        for exponent, coefficient in self.terms.items():
            term = Laurent.constant(coefficient)
            for index, power in enumerate(exponent):
                base = replacements.get(index, VARIABLES[index])
                term *= base ** power
            result += term
        return result

    def clear_laurent(self) -> tuple["Laurent", tuple[int, ...]]:
        if not self.terms:
            return self, ZERO_EXP
        shifts = tuple(max(0, -min(e[i] for e in self.terms)) for i in range(NVAR))
        shifted = {
            tuple(e + shift for e, shift in zip(exponent, shifts)): coefficient
            for exponent, coefficient in self.terms.items()
        }
        return Laurent(shifted), shifts

    def substitute_polynomial(self, index: int, replacement: "Laurent") -> "Laurent":
        if any(exponent[index] < 0 for exponent in self.terms):
            raise ValueError("clear negative exponents before polynomial substitution")
        result = Laurent()
        for exponent, coefficient in self.terms.items():
            base_exp = list(exponent)
            power = base_exp[index]
            base_exp[index] = 0
            term = Laurent({tuple(base_exp): coefficient}) * (replacement ** power)
            result += term
        return result

    def is_zero(self) -> bool:
        return not self.terms

    def positivity_summary(self) -> dict[str, object]:
        if not self.terms:
            raise AssertionError("zero polynomial is not a strict certificate")
        signs = [coefficient.sign() for coefficient in self.terms.values()]
        if min(signs) <= 0:
            bad = [
                (exponent, coefficient)
                for exponent, coefficient in self.terms.items()
                if coefficient.sign() <= 0
            ]
            raise AssertionError(f"nonpositive certificate coefficients: {bad[:4]}")
        payload = self.canonical_bytes()
        return {
            "terms": len(self.terms),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }

    def canonical_bytes(self) -> bytes:
        rows = []
        for exponent in sorted(self.terms):
            rows.append([list(exponent), self.terms[exponent].canonical()])
        return (json.dumps(rows, separators=(",", ":"), sort_keys=False) + "\n").encode()


def poly(value: object) -> Laurent:
    if isinstance(value, Laurent):
        return value
    if isinstance(value, QPhi):
        return Laurent.constant(value)
    return Laurent.constant(value)


VARIABLES = tuple(Laurent.variable(index) for index in range(NVAR))
X, Y, Z, U, V = VARIABLES

Matrix = tuple[tuple[Laurent, Laurent], tuple[Laurent, Laurent]]


def matrix_mul(left: Matrix, right: Matrix) -> Matrix:
    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def scaled_k(variable: Laurent) -> Matrix:
    """Return (2*phi-1) K_n after setting variable=phi^(2n)."""
    inverse = variable ** -1
    return (
        (((2 * PHI + 1) * variable) + ((2 * PHI - 3) * inverse),
         (PHI * variable) + ((PHI - 1) * inverse)),
        (((PHI * variable) + ((PHI - 1) * inverse)),
         ((PHI - 1) * variable) + (PHI * inverse)),
    )


def scaled_trace_q(x: Laurent, y: Laurent, z: Laurent) -> tuple[Laurent, Laurent]:
    product = matrix_mul(matrix_mul(scaled_k(x), scaled_k(y)), scaled_k(z))
    return product[0][0] + product[1][1], product[1][0]


def scaled_a(x: Laurent, y: Laurent, z: Laurent) -> Laurent:
    """Return (2*phi-1)^2 F_(2y+1) F_(2(x-z)-2)."""
    first = PHI * y + (PHI - 1) * (y ** -1)
    w = x * (z ** -1) * Laurent.constant(LAMBDA ** -1)
    second = w - w ** -1
    return first * second


def positive_after_clear(expression: Laurent) -> dict[str, object]:
    cleared, shifts = expression.clear_laurent()
    summary = cleared.positivity_summary()
    summary["clear_shift"] = list(shifts)
    return summary


def within_layer_certificates() -> dict[str, dict[str, object]]:
    t1, q1 = scaled_trace_q(X, Y, Z)
    a1 = scaled_a(X, Y, Z)
    replacements = {
        0: X * Laurent.constant(LAMBDA ** -1),
        1: Y * Laurent.constant(LAMBDA),
    }
    t2 = t1.substitute_monomials(replacements)
    q2 = q1.substitute_monomials(replacements)
    a2 = a1.substitute_monomials(replacements)
    return {
        "a_over_trace_cross": positive_after_clear(a1 * t2 - a2 * t1),
    }


def boundary_certificates(parity: int) -> dict[str, dict[str, object]]:
    # Here X is lambda^r and Z is lambda^z.  The first triple is
    # (r,r,z) for parity 0 and (r+1,r,z) for parity 1.
    if parity == 0:
        first = (X, X, Z)
        second = (
            X ** 2 * Z ** -1 * Laurent.constant(LAMBDA ** -2),
            Z * Laurent.constant(LAMBDA),
            Z * Laurent.constant(LAMBDA),
        )
        minimum_gap = 2
    elif parity == 1:
        first = (X * Laurent.constant(LAMBDA), X, Z)
        second = (
            X ** 2 * Z ** -1 * Laurent.constant(LAMBDA ** -1),
            Z * Laurent.constant(LAMBDA),
            Z * Laurent.constant(LAMBDA),
        )
        minimum_gap = 1
    else:
        raise ValueError("parity must be 0 or 1")

    t1, q1 = scaled_trace_q(*first)
    a1 = scaled_a(*first)
    t2, q2 = scaled_trace_q(*second)
    a2 = scaled_a(*second)

    expressions = {
        "trace_drop": t1 - t2,
        "q_drop": q1 - q2,
        "a_over_trace_cross": a1 * t2 - a2 * t1,
    }
    output: dict[str, dict[str, object]] = {}
    # Write lambda^(r-z)=lambda^minimum_gap*(1+U), U>=0, then
    # lambda^z=1+V, V>=0.  Clear Laurent monomials before each
    # non-monomial substitution; every cleared factor is positive.
    x_replacement = Z * Laurent.constant(LAMBDA ** minimum_gap) * (1 + U)
    for name, expression in expressions.items():
        cleared1, shift1 = expression.clear_laurent()
        substituted1 = cleared1.substitute_polynomial(0, x_replacement)
        cleared2, shift2 = substituted1.clear_laurent()
        substituted2 = cleared2.substitute_polynomial(2, 1 + V)
        cleared3, shift3 = substituted2.clear_laurent()
        summary = cleared3.positivity_summary()
        summary["clear_shifts"] = [list(shift1), list(shift2), list(shift3)]
        output[name] = summary
    return output


def identity_certificates() -> dict[str, str]:
    t, q = scaled_trace_q(X, Y, Z)
    a = scaled_a(X, Y, Z)
    sqrt_five = 2 * PHI - 1
    identity = t - 3 * q - 6 * sqrt_five * a
    if not identity.is_zero():
        raise AssertionError("trace-q Fibonacci identity failed")
    t_yzx, _ = scaled_trace_q(Y, Z, X)
    t_zyx, _ = scaled_trace_q(Z, Y, X)
    if not (t - t_yzx).is_zero() or not (t - t_zyx).is_zero():
        raise AssertionError("trace permutation identities failed")
    return {
        "trace_q": "t-3q=6(2phi-1)a_scaled",
        "trace_symmetry": "tr(KxKyKz) is invariant under S3",
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": 1,
        "coefficient_field": "Q(phi), phi^2=phi+1, phi=(1+sqrt(5))/2",
        "variables": list(VARS),
        "identities": identity_certificates(),
        "within_layer": within_layer_certificates(),
        "boundary_even": boundary_certificates(0),
        "boundary_odd": boundary_certificates(1),
    }


def main() -> None:
    expected_path = Path(__file__).with_name("CERTIFICATE.json")
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    actual = build_certificate()
    if actual != expected:
        raise SystemExit("CERTIFICATE MISMATCH: regenerate and inspect before replacing")
    digest = hashlib.sha256(
        (json.dumps(actual, sort_keys=True, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    term_total = sum(
        item["terms"]
        for section in ("within_layer", "boundary_even", "boundary_odd")
        for item in actual[section].values()
    )
    print(
        "SYMBOLIC VERIFIED D(a,3) Lagrange partition chain; "
        f"certificates=7; positive_terms={term_total}; certificate_sha256={digest}"
    )


if __name__ == "__main__":
    main()
