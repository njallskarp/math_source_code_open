#!/usr/bin/env python3
"""Exact verifier for the length-42 proper-quotient residual lattice."""

from __future__ import annotations

from fractions import Fraction

N = 42
DIVISORS = (6, 14, 21)

# Coefficients are stored in ascending order.
PHI_42 = [1, 1, 0, -1, -1, 0, 1, 0, -1, -1, 0, 1, 1]
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


def rational_rank(integer_matrix: list[list[int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in integer_matrix]
    rows = len(matrix)
    columns = len(matrix[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][column]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                value - multiple * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


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
    product = convolve(PHI_42, PROPER_FACTOR)
    expected = [-1] + [0] * 41 + [1]
    assert product == expected
    assert all(PROPER_FACTOR[30 - index] == -coefficient
               for index, coefficient in enumerate(PROPER_FACTOR))

    pushforward: list[list[int]] = []
    for divisor in DIVISORS:
        for residue in range(divisor):
            pushforward.append(
                [int(index % divisor == residue) for index in range(N)]
            )
    rank = rational_rank(pushforward)
    assert rank == 30

    kernel_basis: list[list[int]] = []
    for shift in range(12):
        vector = [0] * N
        for index, coefficient in enumerate(PROPER_FACTOR):
            vector[index + shift] = coefficient
        kernel_basis.append(vector)
        assert all(
            sum(row[index] * vector[index] for index in range(N)) == 0
            for row in pushforward
        )
    assert rational_rank(kernel_basis) == 12

    # Integral Hermitian residuals have coefficientwise divisibility by 1+i.
    # Write H=(1+i)G.  The anti-reciprocity condition becomes
    # G_{12-k}=i*conj(G_k), with G_6=(1+i)t.
    lattice_basis: list[list[int]] = []
    for index in range(1, 6):
        for value in (1 + 0j, 1j):
            g = [0j] * 12
            g[index] = value
            g[12 - index] = 1j * value.conjugate()
            residual = [(1 + 1j) * coefficient for coefficient in convolve(PROPER_FACTOR, g)]
            lattice_basis.append(
                [int(value.real) for value in residual]
                + [int(value.imag) for value in residual]
            )
    g = [0j] * 12
    g[6] = 1 + 1j
    residual = [(1 + 1j) * coefficient for coefficient in convolve(PROPER_FACTOR, g)]
    lattice_basis.append(
        [int(value.real) for value in residual]
        + [int(value.imag) for value in residual]
    )

    for encoded in lattice_basis:
        values = [complex(encoded[index], encoded[N + index]) for index in range(N)]
        assert values[0] == 0
        assert all(values[N - shift] == values[shift].conjugate() for shift in range(1, N))
        assert all((int(value.real) + int(value.imag)) % 2 == 0 for value in values)
        assert all(
            sum(values[index] for index in range(residue, N, divisor)) == 0
            for divisor in DIVISORS
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

    print(f"pushforward_rank={rank}; kernel_dimension={N-rank}")
    print(f"hermitian_integral_lattice_dimension={len(lattice_basis)}")
    print("gram=" + repr(gram))
    print("M_minus_I_LDL_pivots=" + repr(pivots))
    print("exact kernel and positive-definiteness checks passed")


if __name__ == "__main__":
    main()
