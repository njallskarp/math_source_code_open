#!/usr/bin/env python3
"""Dependency-free exact verifier for QLP-42 pi^4 witness rows."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PI3_DIRECTORY = Path(__file__).resolve().parent.parent / "qlp42_q5_q37_pi3_witnesses"
sys.path.insert(0, str(PI3_DIRECTORY))

from verify_pi3_witnesses import (  # noqa: E402
    N,
    STATES,
    add,
    conjugate,
    multiply,
    read_supports,
    subtract,
    target,
    verify_row as verify_pi3_row,
)


def verify_row(row: dict[str, str], supports: dict[int, list[tuple[int, int]]]) -> None:
    verify_pi3_row(row, supports)
    words = (
        [int(character, 16) for character in row["states_a"]],
        [int(character, 16) for character in row["states_b"]],
    )
    for component in ("s", "h"):
        for shift in range(1, 11):
            correlation = (0, 0)
            for family in range(2):
                for position in range(N):
                    left = STATES[words[family][position]][component]
                    right = STATES[words[family][(position + shift) % N]][component]
                    correlation = add(  # type: ignore[arg-type]
                        correlation,
                        multiply(left, conjugate(right)),  # type: ignore[arg-type]
                    )
            residual = subtract(correlation, target(component, shift))
            assert residual[0] % 4 == 0 and residual[1] % 4 == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    with args.manifest.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    keys = [(int(row["q"]), int(row["orbit"]), int(row["case"])) for row in rows]
    assert len(keys) == len(set(keys))
    expected = {
        (q_value, orbit, case_id)
        for q_value in (5, 37)
        for orbit in range(18)
        for case_id in range(6)
    }
    assert set(keys) <= expected
    if args.require_complete:
        assert set(keys) == expected and len(rows) == 216
    supports = read_supports()
    for row in rows:
        verify_row(row, supports)
    print(f"rows={len(rows)};unique_keys={len(keys)};pi4_witnesses=verified")


if __name__ == "__main__":
    main()
