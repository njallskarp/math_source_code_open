"""Independent local-wave check for the least leading cancellation.

Requires SymPy 1.14.0.  This does not import the standard-library verifier or
use its common-denominator reconstruction.
"""

from __future__ import annotations

import sympy as sp

LEFT = (4, 4, 3, 3, 3, 3, 1)
RIGHT = (3, 3, 3, 3, 3, 2, 2, 2)


def pole_wave(
    partition: tuple[int, ...], alpha: sp.Expr, order: int, n: sp.Symbol
) -> sp.Expr:
    """Coefficient polynomial contributed by the pole at alpha."""
    u = sp.symbols("u")
    t = alpha * (1 - u)
    series = 1 / ((1 - t) * sp.prod(1 - t**part for part in partition))
    analytic = sp.cancel(u**order * series)
    jet = sp.series(analytic, u, 0, order).removeO().expand()
    return sp.expand(
        sum(
            sp.simplify(jet.coeff(u, index))
            * sp.expand_func(sp.binomial(n + order - index - 1, order - index - 1))
            for index in range(order)
        )
    )


def main() -> None:
    n = sp.symbols("n", integer=True, real=True)
    zeta = (-1 + sp.sqrt(-3)) / 2
    left_order = sum(part % 3 == 0 for part in LEFT)
    right_order = sum(part % 3 == 0 for part in RIGHT)

    cross_wave = sp.cancel(
        pole_wave(LEFT, zeta, left_order, n)
        * pole_wave(RIGHT, sp.Integer(1), len(RIGHT) + 1, n)
        + pole_wave(LEFT, sp.Integer(1), len(LEFT) + 1, n)
        * pole_wave(RIGHT, zeta, right_order, n)
    )
    coefficient_polynomial = sp.Poly(
        sp.expand(cross_wave), n, extension=sp.sqrt(-3)
    )
    actual_order = coefficient_polynomial.degree() + 1
    nominal_order = left_order + len(RIGHT)
    determinant_zero = left_order + right_order
    assert nominal_order == 12
    assert actual_order == 11
    assert determinant_zero == 9

    m, c, e, left_width, right_width = sp.symbols(
        "m c e W_lambda W_nu", integer=True
    )
    r = m + e
    s = c + e
    subleading_difference = (
        (m - 1) * (left_width + 1) / 2
        + s * (right_width + 1) / 2
        - r * (left_width + 1) / 2
        - (c - 1) * (right_width + 1) / 2
    )
    assert sp.simplify(
        subleading_difference - (e + 1) * (right_width - left_width) / 2
    ) == 0

    print(
        "INDEPENDENT maximal-prime jet; "
        f"nominal_order={nominal_order}; actual_order={actual_order}; "
        f"determinant_zero={determinant_zero}; "
        f"residual_order={actual_order - determinant_zero}; "
        "subleading_identity=verified"
    )


if __name__ == "__main__":
    main()
