#!/usr/bin/env python3
"""Exact GF(2) checks for the CRT rank proof at compressed length 23."""

from __future__ import annotations


F = sum(1 << degree for degree in (11, 9, 7, 6, 5, 1, 0))
G = sum(1 << degree for degree in (11, 10, 6, 5, 4, 2, 0))
PHI23 = (1 << 23) - 1


def degree(poly: int) -> int:
    return poly.bit_length() - 1


def multiply(left: int, right: int) -> int:
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        right >>= 1
    return result


def remainder(dividend: int, divisor: int) -> int:
    divisor_degree = degree(divisor)
    while degree(dividend) >= divisor_degree:
        dividend ^= divisor << (degree(dividend) - divisor_degree)
    return dividend


def gcd(left: int, right: int) -> int:
    while right:
        left, right = right, remainder(left, right)
    return left


def square_mod(value: int, modulus: int) -> int:
    result = 0
    bit = 0
    while value:
        if value & 1:
            result ^= 1 << (2 * bit)
        value >>= 1
        bit += 1
    return remainder(result, modulus)


def reciprocal(poly: int) -> int:
    d = degree(poly)
    return sum(((poly >> bit) & 1) << (d - bit) for bit in range(d + 1))


def irreducible_degree_11(poly: int) -> bool:
    x = 0b10
    power = x
    for exponent in range(1, 12):
        power = square_mod(power, poly)
        if exponent <= 5 and gcd(power ^ x, poly) != 1:
            return False
    return power == x


def main() -> None:
    assert multiply(F, G) == PHI23
    assert reciprocal(F) == G and reciprocal(G) == F
    assert irreducible_degree_11(F)
    assert irreducible_degree_11(G)
    value = 1
    order = None
    for exponent in range(1, 23):
        value = (2 * value) % 23
        if value == 1:
            order = exponent
            break
    assert order == 11
    print("ord_23_of_2=11")
    print("phi23_factor_degrees=11,11")
    print("factor_1=x^11+x^9+x^7+x^6+x^5+x+1")
    print("factor_2=x^11+x^10+x^6+x^5+x^4+x^2+1")
    print("factors_are_reciprocal=verified")
    print("factors_are_irreducible=verified")
    print("crt_rank_certificate=verified")


if __name__ == "__main__":
    main()
