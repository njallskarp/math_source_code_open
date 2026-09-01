#!/usr/bin/env python3
"""End-to-end driver for the direct QLP-42 q=1, b=12 S frontier."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

HASHES = {
    "prototype_numpy.py": "89badfca8170e0830336b4b7d1e823095966b473b7bf418935e9bae0c5b5af88",
    "prototype_seventh_s.py": "ef2ff2f6efcb269c41dfc81423124893ac154d543ab87089abcc25f63931689f",
}
EXPECTED_A_PHASES = [15_876, 7_056, 7_056, 4_536, 4_536, 3_024]


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
    assert [int(row[1]) for row in rows] == EXPECTED_A_PHASES
    return rows


def main() -> None:
    directory = Path(__file__).resolve().parent
    for name, expected in HASHES.items():
        assert digest(directory / name) == expected

    sixth_output = run(directory, "prototype_numpy.py")
    sixth_rows = table(sixth_output)
    assert [int(row[4]) for row in sixth_rows] == [1686, 1398, 1427, 850, 850, 304]
    assert [int(row[5]) for row in sixth_rows] == [98, 89, 88, 98, 98, 80]
    assert "survivor_rows=2523\n" in sixth_output
    assert sixth_output.endswith("prototype_certificate=verified\n")

    seventh_output = run(directory, "prototype_seventh_s.py")
    seventh_rows = table(seventh_output)
    assert [int(row[4]) for row in seventh_rows] == [303, 180, 92, 5, 5, 0]
    assert [int(row[5]) for row in seventh_rows] == [29, 27, 20, 3, 3, 0]
    assert "survivor_rows=499\n" in seventh_output
    assert seventh_output.endswith("prototype_certificate=verified\n")

    print("input_b_masks=98")
    print("input_labeled_type_pairs=76377")
    print("input_rotation_orbits_per_case=3637")
    print("sixth_order_surviving_orbits=1686,1398,1427,850,850,304")
    print("seventh_order_surviving_orbits=303,180,92,5,5,0")
    print("seventh_order_surviving_masks=29,27,20,3,3,0")
    print("seventh_order_surviving_rows=499")
    print("direct_numpy_certificate=verified")


if __name__ == "__main__":
    main()
