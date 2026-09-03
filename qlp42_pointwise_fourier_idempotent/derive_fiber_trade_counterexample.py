#!/usr/bin/env python3
"""Exact cyclotomic derivation for the QLP-42 three-fiber counterexample."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

Gaussian = tuple[int, int]
State = tuple[int, int, int, int, int, int]

N = 21
P = 7
Q = 3
MU4: tuple[Gaussian, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
PHI21_LOW_TO_HIGH = (1, -1, 0, 1, -1, 0, 1, 0, -1, 1, 0, -1, 1)


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def divide_by_one_plus_i(value: Gaussian) -> Gaussian:
    real, imag = value
    assert (real + imag) % 2 == 0
    assert (imag - real) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def local_states() -> tuple[State, ...]:
    states = []
    for x_value in MU4:
        for y_value in MU4:
            s_value = divide_by_one_plus_i(subtract(x_value, y_value))
            h_value = divide_by_one_plus_i(add(x_value, y_value))
            product = multiply(s_value, conjugate(h_value))
            epsilon = product[1]
            assert product[0] == 0 and epsilon in (-1, 0, 1)
            states.append((*s_value, *h_value, abs(epsilon), epsilon))
    assert len(states) == len(set(states)) == 16
    return tuple(states)


STATES = local_states()


def counts(word: list[int]) -> tuple[int, ...]:
    histogram = Counter(word)
    return tuple(histogram.get(index, 0) for index in range(16))


def aggregate(word: list[int]) -> tuple[int, ...]:
    return tuple(
        sum(STATES[label][coordinate] for label in word)
        for coordinate in range(6)
    )


def crt_index(row: int, column: int) -> int:
    candidates = [
        value
        for value in range(N)
        if value % P == row and value % Q == column
    ]
    assert len(candidates) == 1
    return candidates[0]


def as_cyclic_word(row_major: list[int]) -> list[int]:
    cyclic = [-1] * N
    for row in range(P):
        for column in range(Q):
            cyclic[crt_index(row, column)] = row_major[Q * row + column]
    assert -1 not in cyclic
    return cyclic


def reduce_mod_phi21(coefficients: list[int]) -> tuple[int, ...]:
    work = coefficients + [0] * max(0, N - len(coefficients))
    degree = len(PHI21_LOW_TO_HIGH) - 1
    for exponent in range(len(work) - 1, degree - 1, -1):
        leading = work[exponent]
        if leading == 0:
            continue
        shift = exponent - degree
        for index, coefficient in enumerate(PHI21_LOW_TO_HIGH):
            work[shift + index] -= leading * coefficient
    return tuple(work[:degree])


def primitive_remainders(
    first: list[int], second: list[int]
) -> tuple[tuple[int, ...], ...]:
    first_cyclic = as_cyclic_word(first)
    second_cyclic = as_cyclic_word(second)
    result = []
    for label in range(16):
        difference = [
            int(second_cyclic[index] == label)
            - int(first_cyclic[index] == label)
            for index in range(N)
        ]
        result.append(reduce_mod_phi21(difference))
    return tuple(result)


def main() -> None:
    certificate_path = Path(__file__).with_name("fiber_trade_counterexample.json")
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    assert certificate["schema"] == "qlp42-pointwise-fiber-trade-counterexample-v1"

    for family in ("A", "B"):
        first = certificate["first"][family]
        second = certificate["second"][family]
        assert len(first) == len(second) == N
        assert all(
            isinstance(label, int) and 0 <= label < 16
            for label in first + second
        )
        expected_counts = tuple(certificate["state_counts"][family])
        assert counts(first) == counts(second) == expected_counts
        assert aggregate(first) == aggregate(second)
        target = certificate["family_targets"][family]
        parameters = certificate["family_parameters"][family]
        expected = (
            *target["S"],
            *target["H"],
            parameters["q"],
            parameters["sigma"],
        )
        assert aggregate(first) == tuple(expected)
        remainders = primitive_remainders(first, second)
        assert all(
            all(coefficient == 0 for coefficient in remainder)
            for remainder in remainders
        )

    total_q = sum(
        certificate["family_parameters"][family]["q"]
        for family in ("A", "B")
    )
    total_sigma = sum(
        certificate["family_parameters"][family]["sigma"]
        for family in ("A", "B")
    )
    assert (total_q, total_sigma) == (
        certificate["global_parameters"]["q"],
        certificate["global_parameters"]["sigma"],
    )

    first_support = [
        STATES[label][4] for label in certificate["first"]["A"]
    ]
    second_support = [
        STATES[label][4] for label in certificate["second"]["A"]
    ]
    support_difference = sum(
        left != right
        for left, right in zip(first_support, second_support, strict=True)
    )
    assert (
        support_difference
        == certificate["expected"]["quarter_support_symmetric_difference"]
        == 6
    )

    changed_rows = sum(
        certificate["first"]["A"][Q * row : Q * (row + 1)]
        != certificate["second"]["A"][Q * row : Q * (row + 1)]
        for row in range(P)
    )
    assert (
        changed_rows
        == certificate["expected"]["changed_three_cell_fibers"]
        == 2
    )

    print("cyclotomic_domain=Z[z]/Phi_21")
    print("primitive_indicator_remainders_nonzero=0")
    print("production_derivation=verified")


if __name__ == "__main__":
    main()
