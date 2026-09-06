#!/usr/bin/env python3
"""Boundary tests for the cyclic-minor and blue-equivalence calculations."""

from verify_rank import bareiss_determinant, blue_from_red, cyclic_triple_matrix


def main() -> None:
    checked = []
    for order in range(4, 33):
        determinant = bareiss_determinant(cyclic_triple_matrix(order))
        expected = 0 if order % 3 == 0 else 3
        if determinant != expected:
            raise AssertionError((order, determinant, expected))
        checked.append(order)

    rejected = 0
    for mark, pivot in ((0, 1), (-1, 0), (2, 0)):
        try:
            blue_from_red(mark, pivot, 100)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError(("accepted invalid case", mark, pivot))

    if blue_from_red(0, 0, 99) != 101:
        raise AssertionError("unmarked affine identity")
    if blue_from_red(1, 0, 92) != 108:
        raise AssertionError("marked affine identity")
    if blue_from_red(1, 1, 92) != 106:
        raise AssertionError("pivot affine identity")

    print(
        f"PASS cyclic_orders={checked[0]}..{checked[-1]} "
        f"invalid_cases_rejected={rejected} affine_checks=3"
    )


if __name__ == "__main__":
    main()
