#!/usr/bin/env python3
"""Solver-free audit of the selection-order preservation schedule."""

from __future__ import annotations


CELLS = (
    tuple(range(0, 6)),
    tuple(range(6, 13)),
    tuple(range(14, 29)),
    tuple(range(29, 43)),
)


def swap(value: int, left: int, right: int) -> int:
    if value == left:
        return right
    if value == right:
        return left
    return value


def main() -> None:
    pairs = [
        (left, right)
        for cell in CELLS
        for left_index, left in enumerate(cell)
        for right in cell[left_index + 1 :]
    ]
    if len(pairs) != 232 or len(set(pairs)) != 232:
        raise AssertionError("all-pairs schedule mismatch")

    prior: set[tuple[int, int]] = set()
    arithmetic_goals = 0
    syntactic_images = 0
    for left, right in pairs:
        for old_left, old_right in prior:
            image = (swap(old_left, left, right), swap(old_right, left, right))
            if old_left == left:
                # K(left)<=K(old_right) maps to K(right)<=K(old_right).
                # It follows from the old row plus the strict current inversion.
                if image != (right, old_right) or not old_right < right:
                    raise AssertionError((left, right, old_left, old_right, image))
                arithmetic_goals += 1
            else:
                if image not in prior:
                    raise AssertionError((left, right, old_left, old_right, image))
                syntactic_images += 1
        prior.add((left, right))

    # Exhaustively test the only non-syntactic implication over a range wider
    # than needed for its order-theoretic content.
    scalar_cases = 0
    for key_i in range(9):
        for key_j in range(9):
            for key_k in range(9):
                if key_i <= key_k and key_i >= key_j + 1:
                    if key_j > key_k:
                        raise AssertionError((key_i, key_j, key_k))
                    scalar_cases += 1

    if arithmetic_goals != 874:
        raise AssertionError(arithmetic_goals)
    print(
        "PASS selection_schedule "
        f"rows={len(pairs)} arithmetic_goals={arithmetic_goals} "
        f"syntactic_images={syntactic_images}"
    )
    print(f"PASS strict_inversion_scalar_cases={scalar_cases} range=0..8")


if __name__ == "__main__":
    main()
