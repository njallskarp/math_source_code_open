#!/usr/bin/env python3
"""Exact algebra for the coefficientwise-even QLP-42 residual lattice."""

from __future__ import annotations

from fractions import Fraction
from math import gcd

N = 42
PROPER_FACTOR = [0] * 31
for exponent, coefficient in {
    0: -1,
    1: 1,
    2: -1,
    7: -1,
    8: 1,
    9: -1,
    21: 1,
    22: -1,
    23: 1,
    28: 1,
    29: -1,
    30: 1,
}.items():
    PROPER_FACTOR[exponent] = coefficient


def convolve(left: list[complex | int], right: list[complex | int]) -> list[complex]:
    result = [0j] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def exact_ldl_pivots(integer_matrix: list[list[int]]) -> list[Fraction]:
    dimension = len(integer_matrix)
    lower = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    diagonal = [Fraction(0) for _ in range(dimension)]
    for row in range(dimension):
        lower[row][row] = 1
        diagonal[row] = Fraction(integer_matrix[row][row]) - sum(
            lower[row][k] * lower[row][k] * diagonal[k] for k in range(row)
        )
        assert diagonal[row] > 0
        for future in range(row + 1, dimension):
            numerator = Fraction(integer_matrix[future][row]) - sum(
                lower[future][k] * lower[row][k] * diagonal[k]
                for k in range(row)
            )
            lower[future][row] = numerator / diagonal[row]
    return diagonal


def main() -> None:
    # If every residual coefficient is even, then E=P H and P(0)=-1 imply
    # coefficientwise that H is even.  Write H=2G.  Anti-reciprocity gives
    # G_(12-k)=-conj(G_k), with G_6 purely imaginary.
    lattice_basis: list[list[int]] = []
    for index in range(1, 6):
        for value in (1 + 0j, 1j):
            g = [0j] * 12
            g[index] = value
            g[12 - index] = -value.conjugate()
            residual = [2 * coefficient for coefficient in convolve(PROPER_FACTOR, g)]
            lattice_basis.append(
                [int(value.real) for value in residual]
                + [int(value.imag) for value in residual]
            )
    g = [0j] * 12
    g[6] = 1j
    residual = [2 * coefficient for coefficient in convolve(PROPER_FACTOR, g)]
    lattice_basis.append(
        [int(value.real) for value in residual]
        + [int(value.imag) for value in residual]
    )

    assert len(lattice_basis) == 11
    for encoded in lattice_basis:
        values = [complex(encoded[index], encoded[N + index]) for index in range(N)]
        assert values[0] == 0
        assert all(values[N - shift] == values[shift].conjugate() for shift in range(1, N))
        assert all(int(value.real) % 2 == 0 and int(value.imag) % 2 == 0 for value in values)
        assert all(
            sum(values[index] for index in range(residue, N, divisor)) == 0
            for divisor in (6, 14, 21)
            for residue in range(divisor)
        )

    gram = [
        [sum(left * right for left, right in zip(row, column)) for column in lattice_basis]
        for row in lattice_basis
    ]
    gram_minus_identity = [
        [value - int(row == column) for column, value in enumerate(values)]
        for row, values in enumerate(gram)
    ]
    pivots = exact_ldl_pivots(gram_minus_identity)

    shortest_parameters = ((0, 0, 0, 1, 1), (0, 1, 1, 0, 0), (1, 1, 0, -1, -1))

    def shortest_residual(parameters: tuple[int, ...]) -> tuple[complex, ...]:
        g = [0j] * 12
        for index, value in enumerate(parameters, start=1):
            g[index] = value
            g[12 - index] = -value
        return tuple(2 * coefficient for coefficient in convolve(PROPER_FACTOR, g))

    signed_shortest = {
        tuple(sign * value for value in shortest_residual(parameters))
        for parameters in shortest_parameters
        for sign in (1, -1)
    }
    assert len(signed_shortest) == 6
    assert all(sum(int(value.real) ** 2 + int(value.imag) ** 2 for value in e) == 32
               for e in signed_shortest)
    representative = shortest_residual(shortest_parameters[0])
    decimation_orbit = {
        tuple(representative[(unit * shift) % N] for shift in range(N))
        for unit in range(N)
        if gcd(unit, N) == 1
    }
    assert decimation_orbit == signed_shortest

    print("even_residual_lattice_dimension=11")
    print("gram=" + repr(gram))
    print("M_minus_I_LDL_pivots=" + repr(pivots))
    print("norm_32_signed_vectors=6; one_decimation_orbit=true")
    print(
        "representative_nonzero="
        + repr(
            [(index, int(value.real), int(value.imag))
             for index, value in enumerate(representative) if value]
        )
    )
    print("coefficientwise-even lattice checks passed")


if __name__ == "__main__":
    main()
