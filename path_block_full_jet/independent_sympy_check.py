"""Independent SymPy check of the width-63 cube-root jet witness.

Requires SymPy 1.14.0.  This file imports no code from the primary verifier.
It expands only the four local coefficients needed for the claimed result.
"""

from __future__ import annotations

import sympy as sp

LEFT = (9, 7, 6, 4, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1)
RIGHT = (11, 7, 6, 4, 4, 4, 4, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1)


def local_jet(
    partition: tuple[int, ...], alpha: sp.Expr, at_one: bool, cutoff: int
) -> list[sp.Expr]:
    u = sp.symbols("u")
    result: list[sp.Expr] = [sp.Integer(1)] + [sp.Integer(0)] * (cutoff - 1)
    for weight in (1, *partition):
        denominator = 1 - (alpha * (1 - u)) ** weight
        if at_one or weight % 3 == 0:
            denominator = sp.cancel(denominator / u)
        denominator = sp.Poly(sp.expand(denominator), u, extension=sp.sqrt(-3))
        coefficients = [denominator.nth(index) for index in range(cutoff)]
        inverse = [sp.Integer(0)] * cutoff
        inverse[0] = sp.cancel(1 / coefficients[0])
        for degree in range(1, cutoff):
            inverse[degree] = sp.cancel(
                -sum(
                    coefficients[index] * inverse[degree - index]
                    for index in range(1, degree + 1)
                )
                / coefficients[0]
            )
        product = [sp.Integer(0)] * cutoff
        for i, left in enumerate(result):
            for j, right in enumerate(inverse[: cutoff - i]):
                product[i + j] += left * right
        result = [sp.cancel(entry) for entry in product]
    return result


def wave_top(
    partition: tuple[int, ...], alpha: sp.Expr, order: int, depth: int
) -> list[sp.Expr]:
    n = sp.symbols("n")
    jet = local_jet(partition, alpha, alpha == 1, depth + 1)
    wave = sum(
        jet[index]
        * sp.prod(n + shift for shift in range(1, order - index))
        / sp.factorial(order - index - 1)
        for index in range(min(order, depth + 1))
    )
    polynomial = sp.Poly(sp.expand(wave), n, extension=sp.sqrt(-3))
    return [
        sp.simplify(polynomial.coeff_monomial(n ** (order - 1 - drop)))
        for drop in range(depth + 1)
    ]


def product_top(left: list[sp.Expr], right: list[sp.Expr]) -> list[sp.Expr]:
    return [
        sp.simplify(sum(left[index] * right[drop - index] for index in range(drop + 1)))
        for drop in range(len(left))
    ]


def main() -> None:
    if sp.__version__ != "1.14.0":
        raise RuntimeError(f"expected SymPy 1.14.0, found {sp.__version__}")
    zeta = (-1 + sp.sqrt(-3)) / 2
    depth = 3
    left_root_order = sum(part % 3 == 0 for part in LEFT)
    right_root_order = sum(part % 3 == 0 for part in RIGHT)
    first = product_top(
        wave_top(LEFT, zeta, left_root_order, depth),
        wave_top(RIGHT, sp.Integer(1), len(RIGHT) + 1, depth),
    )
    second = product_top(
        wave_top(LEFT, sp.Integer(1), len(LEFT) + 1, depth),
        wave_top(RIGHT, zeta, right_root_order, depth),
    )
    cross = [sp.simplify(a + b) for a, b in zip(first, second, strict=True)]
    assert cross[:3] == [0, 0, 0]
    assert cross[3] != 0

    leading = first[0]
    normalized = sp.simplify(first[3] / leading - second[3] / (-leading))
    expected = sp.Rational(40895, 12) + sp.Rational(40895, 6) * zeta
    assert sp.simplify(normalized - expected) == 0

    nominal_order = left_root_order + len(RIGHT)
    actual_order = nominal_order - 3
    determinant_zero = left_root_order + right_root_order
    assert (nominal_order, actual_order, determinant_zero) == (28, 25, 14)
    print(
        "INDEPENDENT maximal cube-root jet; "
        "cancelled_orders=3; actual_order=25; determinant_zero=14; "
        "residual_order=11"
    )


if __name__ == "__main__":
    main()
