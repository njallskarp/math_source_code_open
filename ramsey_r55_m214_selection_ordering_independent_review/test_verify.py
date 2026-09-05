#!/usr/bin/env python3
"""Negative calibrations for the independent selection-order audit."""

from verify_review import CELLS, WEIGHTS, check_key_dominance, check_schedule_closure, schedule, verify


def must_reject(function, label: str) -> None:
    try:
        function()
    except AssertionError:
        print(f"PASS rejects_{label}")
        return
    raise AssertionError(f"accepted {label}")


def main() -> None:
    assert len(verify()) == 6
    adjacent_only = [
        (cell[index], cell[index + 1])
        for cell in CELLS
        for index in range(len(cell) - 1)
    ]
    must_reject(lambda: check_schedule_closure(adjacent_only), "noncomposable_adjacent_schedule")

    import verify_review

    original = verify_review.WEIGHTS
    try:
        verify_review.WEIGHTS = (4096, 256, 14, 1)
        must_reject(check_key_dominance, "nondominant_weight")
    finally:
        verify_review.WEIGHTS = original
    assert WEIGHTS == (4096, 256, 16, 1)


if __name__ == "__main__":
    main()
