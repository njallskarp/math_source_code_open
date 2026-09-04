#!/usr/bin/env python3
"""Inspect endpoint support of the target's boundary certificate polynomials.

This is a transparent audit of inherited target code, not an independent
implementation.  It reconstructs the post-substitution polynomials that the
target verifier summarizes, then checks which terms survive at U=0 and V=0.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


def load_target(path: Path):
    spec = importlib.util.spec_from_file_location("dyck_b3_target_verify", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load target verifier at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def boundary_polynomials(v, parity: int):
    if parity == 0:
        first = (v.X, v.X, v.Z)
        second = (
            v.X**2 * v.Z**-1 * v.Laurent.constant(v.LAMBDA**-2),
            v.Z * v.Laurent.constant(v.LAMBDA),
            v.Z * v.Laurent.constant(v.LAMBDA),
        )
        minimum_gap = 2
    elif parity == 1:
        first = (v.X * v.Laurent.constant(v.LAMBDA), v.X, v.Z)
        second = (
            v.X**2 * v.Z**-1 * v.Laurent.constant(v.LAMBDA**-1),
            v.Z * v.Laurent.constant(v.LAMBDA),
            v.Z * v.Laurent.constant(v.LAMBDA),
        )
        minimum_gap = 1
    else:
        raise ValueError("parity must be zero or one")

    t1, q1 = v.scaled_trace_q(*first)
    a1 = v.scaled_a(*first)
    t2, q2 = v.scaled_trace_q(*second)
    a2 = v.scaled_a(*second)
    expressions = {
        "trace_drop": t1 - t2,
        "q_drop": q1 - q2,
        "a_over_trace_cross": a1 * t2 - a2 * t1,
    }
    x_replacement = v.Z * v.Laurent.constant(v.LAMBDA**minimum_gap) * (1 + v.U)
    output = {}
    for name, expression in expressions.items():
        polynomial, _ = expression.clear_laurent()
        polynomial = polynomial.substitute_polynomial(0, x_replacement)
        polynomial, _ = polynomial.clear_laurent()
        polynomial = polynomial.substitute_polynomial(2, 1 + v.V)
        polynomial, _ = polynomial.clear_laurent()
        polynomial.positivity_summary()
        output[name] = polynomial
    return output


def main() -> None:
    default_target = Path(__file__).resolve().parent.parent / "rational_dyck_b3_lagrange" / "verify.py"
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-verifier", type=Path, default=default_target)
    args = parser.parse_args()
    target = load_target(args.target_verifier.resolve())

    summaries = []
    for parity in (0, 1):
        for name, polynomial in boundary_polynomials(target, parity).items():
            exponents = list(polynomial.terms)
            summary = (
                parity,
                name,
                len(exponents),
                sum(exponent[3] == 0 for exponent in exponents),
                sum(exponent[4] == 0 for exponent in exponents),
                sum(exponent[3] == 0 and exponent[4] == 0 for exponent in exponents),
                min(exponent[3] for exponent in exponents),
                min(exponent[4] for exponent in exponents),
            )
            summaries.append(summary)
            print(
                f"parity={summary[0]} name={summary[1]} terms={summary[2]} "
                f"U0_terms={summary[3]} V0_terms={summary[4]} "
                f"UV0_terms={summary[5]} min_U_exp={summary[6]} min_V_exp={summary[7]}"
            )

    odd_q = next(row for row in summaries if row[0] == 1 and row[1] == "q_drop")
    if not (odd_q[3] == 0 and odd_q[6] == 1):
        raise AssertionError("expected the odd q-drop certificate to have a factor U")
    for row in summaries:
        if row is odd_q:
            continue
        if row[5] == 0:
            raise AssertionError(f"certificate lacks a positive U=V=0 term: {row}")
    print(
        "DOMAIN AUDIT PASSED; odd q_drop is U-divisible; "
        "target strictness uses gcd(a,3)=1 to exclude U=0"
    )


if __name__ == "__main__":
    main()
