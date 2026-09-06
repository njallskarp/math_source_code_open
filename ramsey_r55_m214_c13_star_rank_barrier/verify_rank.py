#!/usr/bin/env python3
"""Verify the exact outside-star rank barrier for the M=214,c=13 branch."""

from __future__ import annotations

import json
from fractions import Fraction


OUTSIDE_ORDER = 28


def cyclic_triple_matrix(order: int) -> list[list[int]]:
    if order < 4:
        raise ValueError("order")
    return [
        [int(vertex in {column, (column + 1) % order, (column + 2) % order})
         for column in range(order)]
        for vertex in range(order)
    ]


def bareiss_determinant(source: list[list[int]]) -> int:
    order = len(source)
    if order == 0 or any(len(row) != order for row in source):
        raise ValueError("square matrix")
    matrix = [row[:] for row in source]
    sign = 1
    previous = 1
    for pivot_column in range(order - 1):
        pivot_row = next(
            (row for row in range(pivot_column, order) if matrix[row][pivot_column]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_column:
            matrix[pivot_column], matrix[pivot_row] = (
                matrix[pivot_row], matrix[pivot_column]
            )
            sign = -sign
        pivot = matrix[pivot_column][pivot_column]
        for row in range(pivot_column + 1, order):
            for column in range(pivot_column + 1, order):
                numerator = (
                    matrix[row][column] * pivot
                    - matrix[row][pivot_column] * matrix[pivot_column][column]
                )
                if numerator % previous:
                    raise ArithmeticError("nonexact Bareiss division")
                matrix[row][column] = numerator // previous
        previous = pivot
        for row in range(pivot_column + 1, order):
            matrix[row][pivot_column] = 0
    return sign * matrix[-1][-1]


def rational_rank(source: list[list[int]]) -> int:
    if not source:
        return 0
    matrix = [[Fraction(value) for value in row] for row in source]
    rows = len(matrix)
    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise ValueError("ragged matrix")
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][column]
        matrix[rank] = [entry / value for entry in matrix[rank]]
        for row in range(rows):
            if row == rank or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [
                left - value * right
                for left, right in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def blue_from_red(mark: int, pivot: int, red_triangles: int) -> int:
    if mark not in (0, 1) or pivot not in (0, 1) or pivot > mark:
        raise ValueError("mark/pivot")
    red_degree = 21 - mark
    red_e_incidence = 6 + 2 * pivot
    total_red_degree = 13 * 20 + 30 * 21
    red_neighbor_degree_sum = 21 * red_degree - red_e_incidence
    red_cut = red_neighbor_degree_sum - red_degree - 2 * red_triangles
    blue_neighbor_degree_sum = (
        total_red_degree - red_degree - red_neighbor_degree_sum
    )
    red_inside_blue = (blue_neighbor_degree_sum - red_cut) // 2
    blue_degree = 42 - red_degree
    return blue_degree * (blue_degree - 1) // 2 - red_inside_blue


def main() -> None:
    matrix = cyclic_triple_matrix(OUTSIDE_ORDER)
    if any(sum(matrix[row][column] for row in range(OUTSIDE_ORDER)) != 3
           for column in range(OUTSIDE_ORDER)):
        raise AssertionError("column weight")
    determinant = bareiss_determinant(matrix)
    if determinant != 3:
        raise AssertionError(("determinant", determinant))

    # Coefficients lambda whose sums on all triples are constant form exactly
    # the all-ones line. Differences against {0,1,2} give a rank-27 system.
    reference = {0, 1, 2}
    difference_rows: list[list[int]] = []
    for i in range(OUTSIDE_ORDER):
        for j in range(i + 1, OUTSIDE_ORDER):
            for k in range(j + 1, OUTSIDE_ORDER):
                triple = {i, j, k}
                if triple == reference:
                    continue
                difference_rows.append([
                    int(vertex in triple) - int(vertex in reference)
                    for vertex in range(OUTSIDE_ORDER)
                ])
    difference_rank = rational_rank(difference_rows)
    if difference_rank != OUTSIDE_ORDER - 1:
        raise AssertionError(("difference rank", difference_rank))
    if any(sum(row) for row in difference_rows):
        raise AssertionError("ones not in kernel")

    cases = []
    for mark, pivot, red_target, blue_target in (
        (0, 0, 100, 100),
        (1, 0, 93, 107),
        (1, 1, 93, 105),
    ):
        actual = blue_from_red(mark, pivot, red_target)
        if actual != blue_target:
            raise AssertionError((mark, pivot, actual, blue_target))
        cases.append([mark, pivot, red_target, actual])

    print(json.dumps({
        "blue_equivalence": cases,
        "constant_triple_sum_kernel_dimension": OUTSIDE_ORDER - difference_rank,
        "cyclic_minor_determinant": determinant,
        "outside_order": OUTSIDE_ORDER,
        "post_total_independent_star_directions": OUTSIDE_ORDER - 1,
        "status": "VERIFIED OUTSIDE-STAR RANK BARRIER",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
