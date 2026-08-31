#!/usr/bin/env python3
"""Exact certificate for the Goethals--Seidel slice obstruction at QLP-42.

All arithmetic is in Z[i].  The program verifies an explicit quaternary
sequence A whose periodic autocorrelation is concentrated at shift 21, derives
the required autocorrelation of a putative partner B on the shortest residual
shell, and exhausts the possible support patterns of the half-difference of B.
"""

from __future__ import annotations

from itertools import combinations, product

N = 42
HALF = 21
ROOT = {
    "1": (1, 0),
    "i": (0, 1),
    "-": (-1, 0),
    "j": (0, -1),
}

# This is the Gray image of a symmetric-complementary-ternary construction
# with parameters p=21 and q=41.  The literal string is the certificate; no
# external construction theorem is trusted by this verifier.
A_WORD = "i1-jj11j1i-1j-i--ii1-1-1ii--i-j1-i1j11jj-1"

NEGATIVE_RESIDUAL = {4, 11, 31, 38}
POSITIVE_RESIDUAL = {10, 17, 25, 32}


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def multiply(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: tuple[int, int]) -> tuple[int, int]:
    return value[0], -value[1]


def paf(sequence: list[tuple[int, int]]) -> list[tuple[int, int]]:
    size = len(sequence)
    return [
        sum_gaussian(
            multiply(sequence[index], conjugate(sequence[(index + shift) % size]))
            for index in range(size)
        )
        for shift in range(size)
    ]


def sum_gaussian(values) -> tuple[int, int]:
    real = 0
    imaginary = 0
    for value in values:
        real += value[0]
        imaginary += value[1]
    return real, imaginary


def required_combined_paf(shift: int) -> tuple[int, int]:
    if shift == 0:
        return N + N, 0
    if shift in NEGATIVE_RESIDUAL:
        return -4, 0
    if shift in POSITIVE_RESIDUAL:
        return 0, 0
    return -2, 0


def support(values: list[tuple[int, int]]) -> set[int]:
    return {index for index, value in enumerate(values) if value != (0, 0)}


def main() -> None:
    assert len(A_WORD) == N
    a = [ROOT[symbol] for symbol in A_WORD]
    a_paf = paf(a)
    assert sum_gaussian(a) == (1, 1)
    assert a_paf[0] == (N, 0)
    assert a_paf[HALF] == (-40, 0)
    assert all(
        a_paf[shift] == (0, 0)
        for shift in range(1, N)
        if shift != HALF
    )

    b_required = [
        add(required_combined_paf(shift), (-a_paf[shift][0], -a_paf[shift][1]))
        for shift in range(N)
    ]
    assert b_required[0] == (N, 0)
    assert b_required[HALF] == (38, 0)

    # For the even-index CRT section x_j=B_(22j mod 42) and its translate
    # y_j=B_(22j+21 mod 42), put R_j=x_j-y_j.  Direct expansion gives
    #
    #   PAF_B(s)-PAF_B(s+21) = (-1)^s PAF_R(s),  1 <= s <= 20.
    #
    # The target difference has four nonzero shifts.
    target_difference = [
        (
            b_required[shift][0] - b_required[shift + HALF][0],
            b_required[shift][1] - b_required[shift + HALF][1],
        )
        for shift in range(HALF)
    ]
    assert support(target_difference) == {0, 4, 10, 11, 17}

    # PAF_B(21)=38 means 42-4*opposite-2*quarter_turn=38, so either
    # (opposite, quarter_turn)=(1,0) or (0,2).  Thus R has support one or two.
    defect_solutions = [
        (opposite, quarter_turn)
        for opposite in range(HALF + 1)
        for quarter_turn in range(HALF + 1)
        if 42 - 4 * opposite - 2 * quarter_turn == 38
    ]
    assert defect_solutions == [(0, 2), (1, 0)]

    opposite_values = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    quarter_turn_values = list(product((-1, 1), repeat=2))
    matches = 0

    # Exhaust the one-opposite case.  A one-point sequence has zero
    # out-of-phase autocorrelation.
    for position in range(HALF):
        for value in opposite_values:
            residual = [(0, 0)] * HALF
            residual[position] = value
            residual_paf = paf(residual)
            candidate = [
                (
                    ((-1) ** shift) * residual_paf[shift][0],
                    ((-1) ** shift) * residual_paf[shift][1],
                )
                for shift in range(HALF)
            ]
            matches += candidate[1:] == target_difference[1:]

    # Exhaust the two-quarter-turn case.  Its out-of-phase autocorrelation is
    # supported only at the two signed differences of the support positions.
    for first, second in combinations(range(HALF), 2):
        for first_value, second_value in product(quarter_turn_values, repeat=2):
            residual = [(0, 0)] * HALF
            residual[first] = first_value
            residual[second] = second_value
            residual_paf = paf(residual)
            assert len(support(residual_paf) - {0}) == 2
            candidate = [
                (
                    ((-1) ** shift) * residual_paf[shift][0],
                    ((-1) ** shift) * residual_paf[shift][1],
                )
                for shift in range(HALF)
            ]
            matches += candidate[1:] == target_difference[1:]

    assert matches == 0
    print(f"A={A_WORD}")
    print("sum(A)=1+i")
    print("nonzero out-of-phase PAF(A)={21:-40}")
    print("required PAF(B,21)=38")
    print("half-difference target support={4,10,11,17}")
    print("defect cases={(one opposite),(two quarter-turns)}")
    print("exhaustive half-difference matches=0")
    print("certificate=verified")


if __name__ == "__main__":
    main()
