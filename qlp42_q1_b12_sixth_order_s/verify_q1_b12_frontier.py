#!/usr/bin/env python3
"""End-to-end driver for the direct QLP-42 q=1, b=12 S frontier."""

from __future__ import annotations

import hashlib
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HASHES = {
    "prototype_numpy.py": "89badfca8170e0830336b4b7d1e823095966b473b7bf418935e9bae0c5b5af88",
    "prototype_seventh_s.py": "ef2ff2f6efcb269c41dfc81423124893ac154d543ab87089abcc25f63931689f",
    "prototype_eighth_s.py": "bf03d1ee7b96e9ff67c83735d5c59b3570a1337319d56a331705417f80b5e907",
    "independent_cpp.cpp": "31eb9386649ba375464ae99f657c0aef55d50744dea25798c31e7b12e8d477e4",
}
B14_CPP_SHA256 = "a861b0275d259d2f687d5aa9cd28a2a167cc05222ea1b4439f933e43a2ef6cb1"
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


def compiler_command(source: Path, output: Path) -> list[str]:
    compiler = os.environ.get("CXX") or shutil.which("c++")
    assert compiler is not None, "a C++20 compiler is required"
    command = [compiler]
    if platform.system() == "Darwin":
        sdk = subprocess.run(
            ["xcrun", "--show-sdk-path"], check=True, text=True, capture_output=True
        ).stdout.strip()
        sdk_cpp = Path(sdk) / "usr" / "include" / "c++" / "v1"
        if sdk_cpp.is_dir():
            command += ["-isysroot", sdk, f"-I{sdk_cpp}", "-stdlib=libc++"]
    return command + [
        "-O3", "-std=c++20", "-Wall", "-Wextra", "-pedantic",
        str(source), "-o", str(output),
    ]


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

    eighth_output = run(directory, "prototype_eighth_s.py")
    assert "eighth_order_surviving_orbits=303,178,92,1,1,0\n" in eighth_output
    assert "eighth_order_surviving_masks=29,26,20,1,1,0\n" in eighth_output
    assert "eighth_order_surviving_rows=493\n" in eighth_output
    assert eighth_output.endswith("prototype_certificate=verified\n")

    b14_cpp = directory.parent / "qlp42_q1_b14_sixth_order_s" / "independent_cpp.cpp"
    assert digest(b14_cpp) == B14_CPP_SHA256
    with tempfile.TemporaryDirectory(prefix="qlp42-b12-") as temporary:
        executable = Path(temporary) / "independent_cpp"
        subprocess.run(
            compiler_command(directory / "independent_cpp.cpp", executable), check=True
        )
        independent_output = subprocess.run(
            [str(executable), "--quiet"],
            cwd=directory,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
    assert independent_output == (
        "input_b_masks=98\n"
        "input_labeled_type_pairs=76377\n"
        "input_rotation_orbits_per_case=3637\n"
        "sixth_order_surviving_orbits=1686,1398,1427,850,850,304\n"
        "seventh_order_surviving_orbits=303,180,92,5,5,0\n"
        "eighth_order_surviving_orbits=303,178,92,1,1,0\n"
        "eighth_order_surviving_masks=29,26,20,1,1,0\n"
        "sixth_survivor_rows=2523\n"
        "seventh_survivor_rows=499\n"
        "eighth_survivor_rows=493\n"
        "quadratic_interpolation_direct_audits=671104\n"
        "independent_cpp_certificate=verified\n"
    )

    print("input_b_masks=98")
    print("input_labeled_type_pairs=76377")
    print("input_rotation_orbits_per_case=3637")
    print("sixth_order_surviving_orbits=1686,1398,1427,850,850,304")
    print("seventh_order_surviving_orbits=303,180,92,5,5,0")
    print("seventh_order_surviving_masks=29,27,20,3,3,0")
    print("seventh_order_surviving_rows=499")
    print("eighth_order_surviving_orbits=303,178,92,1,1,0")
    print("eighth_order_surviving_masks=29,26,20,1,1,0")
    print("eighth_order_surviving_rows=493")
    print("direct_numpy_certificate=verified")
    print("independent_cpp_certificate=verified")
    print("two_implementation_certificate=verified")


if __name__ == "__main__":
    main()
