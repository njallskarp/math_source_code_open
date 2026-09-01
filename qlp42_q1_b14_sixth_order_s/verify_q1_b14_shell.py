#!/usr/bin/env python3
"""End-to-end driver for the direct QLP-42 q=1, b=14 S-component scan."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

HASHES = {
    "prototype_numpy.py": "96d919fa3170b55ca61c14099a31deefe41ff7063d85f315e25c9d6f6a48d3d2",
    "prototype_seventh_s.py": "9c14edb8072390892b900f6d7594bc2e6edb8902efedc55c093ea96d86dcfc2e",
    "prototype_eighth_s.py": "2f6855befcc100f95286fa0453a7833f4d1e755a44e29e1894ed29a4628b274f",
}
EXPECTED_A_PHASES = [1225, 441, 441, 245, 245, 147]
EXPECTED_B_PHASES = [31750, 93498, 50760, 93498, 93498, 164728]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(directory: Path, name: str) -> str:
    return subprocess.run(
        [sys.executable, str(directory / name)],
        cwd=directory,
        check=True,
        text=True,
        capture_output=True,
    ).stdout


def table(output: str) -> list[list[str]]:
    lines = output.splitlines()
    header = next(
        index for index, line in enumerate(lines) if line.startswith("case\ta_phase_assignments")
    )
    rows = [line.split("\t") for line in lines[header + 1 : header + 7]]
    assert [int(row[0]) for row in rows] == list(range(6))
    return rows


def main() -> None:
    directory = Path(__file__).resolve().parent
    for name, expected in HASHES.items():
        assert digest(directory / name) == expected

    sixth_output = run(directory, "prototype_numpy.py")
    sixth_rows = table(sixth_output)
    assert [int(row[1]) for row in sixth_rows] == EXPECTED_A_PHASES
    assert [set(map(int, row[2].split(","))) for row in sixth_rows] == [
        {count} for count in EXPECTED_B_PHASES
    ]
    assert [int(row[4]) for row in sixth_rows] == [24, 29, 7, 32, 32, 12]
    assert [int(row[5]) for row in sixth_rows] == [9, 13, 3, 16, 16, 6]
    assert "survivor_rows=94\n" in sixth_output
    assert sixth_output.endswith("prototype_certificate=verified\n")

    seventh_output = run(directory, "prototype_seventh_s.py")
    seventh_rows = table(seventh_output)
    assert [int(row[1]) for row in seventh_rows] == EXPECTED_A_PHASES
    assert [set(map(int, row[2].split(","))) for row in seventh_rows] == [
        {count} for count in EXPECTED_B_PHASES
    ]
    assert [int(row[4]) for row in seventh_rows] == [0, 0, 0, 2, 2, 0]
    assert [int(row[5]) for row in seventh_rows] == [0, 0, 0, 1, 1, 0]
    assert "survivor_rows=2\n" in seventh_output
    assert seventh_output.endswith("prototype_certificate=verified\n")

    eighth_output = run(directory, "prototype_eighth_s.py")
    rows = [line.split("\t") for line in eighth_output.splitlines()[1:5]]
    assert len(rows) == 4
    assert {int(row[0]) for row in rows} == {3, 4}
    assert {int(row[2]) for row in rows} == {245}
    assert {int(row[3]) for row in rows} == {93498}
    assert {int(row[4]) for row in rows} == {93498}
    assert {int(row[5]) for row in rows} == {0}
    assert "eighth_order_surviving_orbits=0\n" in eighth_output
    assert eighth_output.endswith("prototype_certificate=verified\n")

    print("input_b_masks=56")
    print("input_labeled_type_pairs=6762")
    print("input_rotation_orbits_per_case=322")
    print("sixth_order_surviving_orbits=24,29,7,32,32,12")
    print("seventh_order_surviving_orbits=0,0,0,2,2,0")
    print("eighth_order_surviving_orbits=0,0,0,0,0,0")
    print("q1_b14_shell=excluded")
    print("direct_numpy_certificate=verified")


if __name__ == "__main__":
    main()
