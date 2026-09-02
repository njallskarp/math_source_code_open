#!/usr/bin/env python3
"""Exhaustive local ANF tests and fixed-word end-to-end encoding checks."""

from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent
PI3_DIRECTORY = DIRECTORY.parent / "qlp42_q5_q37_pi3_witnesses"
sys.path[:0] = [str(DIRECTORY), str(PI3_DIRECTORY)]

from generate_pi3_witnesses import STATES, conjugate, multiply  # noqa: E402
from solve_pi3_mq import state_index  # noqa: E402
from solve_pi4_mq import (  # noqa: E402
    assumptions_from_words,
    encode_problem,
    product_coordinate_anf,
)
from sweep_pi4_hints import read_rows, write_rows  # noqa: E402
from verify_pi3_witnesses import read_supports  # noqa: E402
from verify_pi4_witnesses import verify_row  # noqa: E402


def evaluate_anf(masks: tuple[int, ...], assignment: int) -> int:
    value = 0
    for mask in masks:
        value ^= int(mask & assignment == mask)
    return value


def check_local_anfs() -> None:
    checks = 0
    for left_quarter in range(2):
        for right_quarter in range(2):
            for component in ("s", "h"):
                for coordinate in range(2):
                    for bit in range(2):
                        masks = product_coordinate_anf(
                            left_quarter,
                            right_quarter,
                            component,
                            coordinate,
                            bit,
                        )
                        for assignment in range(64):
                            left_bits = tuple((assignment >> bit) & 1 for bit in range(3))
                            right_bits = tuple(
                                (assignment >> (bit + 3)) & 1 for bit in range(3)
                            )
                            left = state_index(left_bits, left_quarter)
                            right = state_index(right_bits, right_quarter)
                            coordinate_value = multiply(
                                STATES[left][component],  # type: ignore[arg-type]
                                conjugate(STATES[right][component]),  # type: ignore[arg-type]
                            )[coordinate]
                            expected = ((coordinate_value % 4) >> bit) & 1
                            assert evaluate_anf(masks, assignment) == expected
                            checks += 1
    assert checks == 2048
    print("local_truth_table_checks=2048")


def direct_pi4(row: dict[str, str]) -> bool:
    try:
        verify_row(row, read_supports())
    except AssertionError:
        return False
    return True


def check_fixed_words() -> None:
    path = PI3_DIRECTORY / "full_witnesses.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    selected = [rows[index] for index in (0, 17, 53, 107, 108, 143, 179, 215)]
    for row in selected:
        q_value, orbit, case_id = (int(row[field]) for field in ("q", "orbit", "case"))
        encoding, cells, _ = encode_problem(q_value, orbit, case_id)
        assumptions = assumptions_from_words(
            cells, (row["states_a"], row["states_b"]), set()
        )
        satisfiable, _ = encoding.solver.solve(assumptions=assumptions)
        assert bool(satisfiable) == direct_pi4(row)
        print(
            f"fixed_word=q{q_value}/o{orbit}/c{case_id};"
            f"pi4={int(bool(satisfiable))}"
        )
    print("fixed_word_equivalence_checks=8")


def check_serialization() -> None:
    row = {
        "q": "5",
        "orbit": "0",
        "case": "1",
        "a_mask_hex": "000000",
        "b_mask_hex": "004183",
        "states_a": "5af22d0f728a0d5fd2757",
        "states_b": "6c882054ca522f62a2f02",
    }
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "rows.tsv"
        write_rows(path, {(5, 0, 1): row})
        assert b"\r\n" not in path.read_bytes()
        assert read_rows(path) == {(5, 0, 1): row}
    print("lf_serialization_regression=passed")


def main() -> None:
    check_local_anfs()
    check_fixed_words()
    check_serialization()
    print("pi4_encoding_regression=passed")


if __name__ == "__main__":
    main()
