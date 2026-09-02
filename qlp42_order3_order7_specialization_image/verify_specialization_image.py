#!/usr/bin/env python3
"""Definition-level exact checker for the order-3/order-7 image theorem.

Polynomial coefficients below are tuples of integers representing universal
linear forms.  Verifying the identities on this basis proves them for every
specialization of the parameters in any commutative ring, hence over Z[i].
"""

from __future__ import annotations

from typing import Iterable


NVAR = 9  # a0,a1,b0,...,b5,c
ZERO = (0,) * NVAR


def scalar(value: int, index: int) -> tuple[int, ...]:
    out = [0] * NVAR
    out[index] = value
    return tuple(out)


def vadd(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(left, right, strict=True))


def vscale(value: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(value * x for x in vector)


def trim(poly: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    while len(poly) > 1 and poly[-1] == ZERO:
        poly.pop()
    return poly


def padd(
    left: list[tuple[int, ...]], right: list[tuple[int, ...]]
) -> list[tuple[int, ...]]:
    out = [ZERO] * max(len(left), len(right))
    for j in range(len(out)):
        a = left[j] if j < len(left) else ZERO
        b = right[j] if j < len(right) else ZERO
        out[j] = vadd(a, b)
    return trim(out)


def pmul_int(
    linear: list[tuple[int, ...]], integer: Iterable[int]
) -> list[tuple[int, ...]]:
    integer = list(integer)
    out = [ZERO] * (len(linear) + len(integer) - 1)
    for j, vector in enumerate(linear):
        for k, coefficient in enumerate(integer):
            out[j + k] = vadd(out[j + k], vscale(coefficient, vector))
    return trim(out)


def premainder_monic(
    poly: list[tuple[int, ...]], modulus: list[int]
) -> list[tuple[int, ...]]:
    assert modulus[-1] == 1
    out = poly[:]
    degree = len(modulus) - 1
    while len(out) - 1 >= degree:
        lead = out[-1]
        shift = len(out) - len(modulus)
        for j, coefficient in enumerate(modulus):
            out[shift + j] = vadd(out[shift + j], vscale(-coefficient, lead))
        trim(out)
    return out


def eval_one(poly: list[tuple[int, ...]]) -> tuple[int, ...]:
    out = ZERO
    for coefficient in poly:
        out = vadd(out, coefficient)
    return out


def imul(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for j, a in enumerate(left):
        for k, b in enumerate(right):
            out[j + k] += a * b
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def iadd(left: list[int], right: list[int]) -> list[int]:
    out = [0] * max(len(left), len(right))
    for j in range(len(out)):
        out[j] = (left[j] if j < len(left) else 0) + (
            right[j] if j < len(right) else 0
        )
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def monomial_remainder_sum(power: int, modulus: list[int]) -> int:
    poly = [ZERO] * power + [scalar(1, 0)]
    return eval_one(premainder_monic(poly, modulus))[0]


def main() -> None:
    phi3 = [1, 1, 1]
    phi7 = [1] * 7
    x4_plus_x = [0, 1, 0, 0, 1]

    bezout = iadd(phi7, [-x for x in imul(x4_plus_x, phi3)])
    assert bezout == [1]
    assert sum(phi3) == 3 and sum(phi7) == 7

    # Necessity for every f of degree <21 follows by Z-linearity from these
    # monomial congruences.
    for power in range(21):
        assert (1 - monomial_remainder_sum(power, phi3)) % 3 == 0
        assert (1 - monomial_remainder_sum(power, phi7)) % 7 == 0

    a = [scalar(1, 0), scalar(1, 1)]
    b = [scalar(1, 2 + j) for j in range(6)]
    c = [scalar(1, 8)]
    one_minus_phi7 = [1 - phi7[0]] + [-x for x in phi7[1:]]
    f0 = padd(pmul_int(a, phi7), pmul_int(b, one_minus_phi7))
    f = padd(f0, pmul_int(c, imul(phi3, phi7)))

    assert premainder_monic(f, phi3) == a
    assert premainder_monic(f, phi7) == b

    expected_at_one = [0] * NVAR
    expected_at_one[0] = 7
    expected_at_one[1] = 7
    for j in range(2, 8):
        expected_at_one[j] = -6
    expected_at_one[8] = 21
    assert eval_one(f) == tuple(expected_at_one)
    assert len(f) - 1 <= 11

    print("ring=Z[i]")
    print("bezout=verified")
    print("resultant_phi3_phi7=1")
    print("necessity_basis=21_monomials")
    print("sufficiency_basis=9_parameters")
    print(f"degree_bound={len(f)-1}<21")
    print("specialization_image=verified")


if __name__ == "__main__":
    main()
