#!/usr/bin/env python3
"""Verify exact positive-definite completions of all shifted Gram fibers."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

Gaussian = tuple[Fraction, Fraction]
IntegerGaussian = tuple[int, int]


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


def divide_by_real(value: Gaussian, divisor: Fraction) -> Gaussian:
    return value[0] / divisor, value[1] / divisor


def norm(value: IntegerGaussian) -> int:
    return value[0] * value[0] + value[1] * value[1]


def balanced_word(total: int) -> tuple[int, list[int]]:
    quotient, remainder = divmod(total, 20)
    word = [
        int((index + 1) * remainder // 20 > index * remainder // 20)
        for index in range(20)
    ]
    assert sum(word) == remainder
    return quotient, word


def rotate_left(word: list[int], amount: int) -> list[int]:
    assert 0 <= amount < len(word)
    return word[amount:] + word[:amount]


def load_certificate() -> dict:
    path = Path(__file__).with_name("completion_certificate.json")
    certificate = json.loads(path.read_text(encoding="utf-8"))
    assert certificate["length"] == 21
    assert certificate["branches"] == [5, 37]
    assert certificate["default_rotation"] == [0, 0]
    assert certificate["expected_distinct_case_sigma_pairs"] == 228
    assert certificate["expected_branch_labeled_fiber_points"] == 264
    return certificate


def rotation_map(certificate: dict) -> dict[tuple[int, int], tuple[int, int]]:
    result = {}
    for row in certificate["exceptional_rotations"]:
        key = row["case"], row["sigma"]
        assert key not in result
        result[key] = row["real"], row["imaginary"]
    assert len(result) == 5
    return result


def completion(
    beta: IntegerGaussian,
    sigma: int,
    rotations: tuple[int, int],
) -> list[IntegerGaussian]:
    real_quotient, real_word = balanced_word(beta[0])
    imag_quotient, imag_word = balanced_word(beta[1] - sigma)
    real_word = rotate_left(real_word, rotations[0])
    imag_word = rotate_left(imag_word, rotations[1])
    values = [(0, sigma)] + [
        (
            real_quotient + real_word[index],
            imag_quotient + imag_word[index],
        )
        for index in range(20)
    ]
    assert tuple(map(sum, zip(*values, strict=True))) == beta
    return values


def target_s(shift: int) -> int:
    if shift == 0:
        return 43
    if shift in (4, 17):
        return -2
    if shift in (10, 11):
        return 2
    return 0


def schur_matrix(
    cross: list[IntegerGaussian], beta: IntegerGaussian
) -> list[list[Gaussian]]:
    size = 21
    circulant = [
        [cross[(column - row) % size] for column in range(size)]
        for row in range(size)
    ]
    beta_norm = norm(beta)
    matrix = []
    for row in range(size):
        matrix_row = []
        for column in range(size):
            value: IntegerGaussian = (
                43 * target_s((column - row) % size) - 2 * beta_norm,
                0,
            )
            for index in range(size):
                product = multiply(
                    circulant[row][index],
                    conjugate(circulant[column][index]),
                )
                value = subtract(value, product)
            matrix_row.append((Fraction(value[0]), Fraction(value[1])))
        matrix.append(matrix_row)
    for row in range(size):
        for column in range(size):
            assert matrix[row][column] == conjugate(matrix[column][row])
    return matrix


def full_shifted_gram(cross: list[IntegerGaussian]) -> list[list[Gaussian]]:
    size = 21
    gram_s = [
        [
            (Fraction(target_s((column - row) % size)), Fraction(0))
            for column in range(size)
        ]
        for row in range(size)
    ]
    gram_h = [
        [
            (Fraction(41 if row == column else -2), Fraction(0))
            for column in range(size)
        ]
        for row in range(size)
    ]
    cross_block = [
        [
            (
                Fraction(cross[(column - row) % size][0]),
                Fraction(cross[(column - row) % size][1]),
            )
            for column in range(size)
        ]
        for row in range(size)
    ]
    upper = [gram_s[row] + cross_block[row] for row in range(size)]
    lower = [
        [conjugate(cross_block[column][row]) for column in range(size)]
        + gram_h[row]
        for row in range(size)
    ]
    matrix = upper + lower
    for row in range(2 * size):
        for column in range(2 * size):
            assert matrix[row][column] == conjugate(matrix[column][row])
    return matrix


def positive_definite_ldl(matrix: list[list[Gaussian]]) -> None:
    size = len(matrix)
    lower = [[(Fraction(0), Fraction(0)) for _ in range(size)] for _ in range(size)]
    pivots: list[Fraction] = []

    for column in range(size):
        pivot = matrix[column][column]
        for index, previous_pivot in enumerate(pivots):
            term = multiply(
                multiply(lower[column][index], (previous_pivot, Fraction(0))),
                conjugate(lower[column][index]),
            )
            pivot = subtract(pivot, term)
        assert pivot[1] == 0
        assert pivot[0] > 0
        pivots.append(pivot[0])
        lower[column][column] = (Fraction(1), Fraction(0))

        for row in range(column + 1, size):
            entry = matrix[row][column]
            for index, previous_pivot in enumerate(pivots[:-1]):
                term = multiply(
                    multiply(lower[row][index], (previous_pivot, Fraction(0))),
                    conjugate(lower[column][index]),
                )
                entry = subtract(entry, term)
            lower[row][column] = divide_by_real(entry, pivot[0])


def main() -> None:
    certificate = load_certificate()
    cases = [tuple(case) for case in certificate["cases"]]
    assert cases == [(4, -5), (4, -3), (0, -5), (4, -1), (4, 1), (0, -3)]
    exceptions = rotation_map(certificate)

    distinct_pairs = set()
    branch_labeled_points = 0
    positive_completions = 0
    direct_block_checks = 0

    for branch in certificate["branches"]:
        for case_index, beta in enumerate(cases):
            for sigma in range(-branch, branch + 1, 2):
                rotations = exceptions.get((case_index, sigma), (0, 0))
                cross = completion(beta, sigma, rotations)
                matrix = schur_matrix(cross, beta)
                positive_definite_ldl(matrix)
                distinct_pairs.add((case_index, sigma))
                branch_labeled_points += 1
                positive_completions += 1

                if branch == 37 and sigma in (-37, 37):
                    positive_definite_ldl(full_shifted_gram(cross))
                    direct_block_checks += 1

    assert len(distinct_pairs) == certificate["expected_distinct_case_sigma_pairs"]
    assert branch_labeled_points == certificate["expected_branch_labeled_fiber_points"]
    assert positive_completions == branch_labeled_points
    assert direct_block_checks == 12

    print(f"distinct_case_sigma_pairs={len(distinct_pairs)}")
    print(f"branch_labeled_fiber_points={branch_labeled_points}")
    print(f"positive_definite_completions={positive_completions}")
    print(f"nondefault_rotation_pairs={len(exceptions)}")
    print(f"direct_block_checks={direct_block_checks}")
    print("arithmetic=exact_rational_gaussian")
    print("shifted_gram_mechanism=exhausted")
    print("certificate=verified")


if __name__ == "__main__":
    main()
