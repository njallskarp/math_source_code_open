#!/usr/bin/env python3
"""End-to-end certificate for the QLP-42 q=1, b=16 shell obstruction."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HASHES = {
    "prototype_numpy.py": "73e7911bbf037238634675c052694e2859d4800db87d428a181aa56b5714d807",
    "prototype_sixth_h.cpp": "921f54ca25f32f896c3466f37e3e1805daef4572b2ccc8b0bd47b7630abe002c",
    "prototype_seventh_s.py": "821c659cca0785431561eaaccd001b57803873d4fabfb0806c6368ad8e6f2a2b",
    "independent_sixth_cpp.cpp": "1771a9b8b0f7d3bd2cf5c48f6900cf148ff93ff2af9ed07dda44cf8127fa82c1",
    "independent_seventh_cpp.cpp": "6d0be4f87ad01151813eb1c4be254601d09dff732d5a0aa616f02ff440bc39f0",
    "input_orbits.tsv": "b9e6abba1ee6b79bc89d3b18d5383abff0191c1298046f10667212bbb48c9f9c",
    "sixth_orbit_table.tsv": "8fc9a9da00f2da658495143dfa99d28e2771f4155816afced2d9834edd560e19",
    "sixth_verification_output.txt": "47c92a3124429425a5766f3d72dd4438b391a683ccfba9b010c98abf4771394a",
    "seventh_verification_output.txt": "4877d2d2dfb8b75e3a940ceba1741d28aeb59a23702e1594308cd07884172564",
}
FOURTH_SHA256 = "a5f616a19e241bcdced0962a2843631d1bb13a30de41cfbc05a2c0999e74bacf"
SUM_SHA256 = "d0ecc7b462f6a3e87eb1a3feb0acb13dcd326ddcc83cd84c6aa23c48349fc730"
CASE5_CPP_SHA256 = "4016be38220c662d0feb1ae4139184ad9e424ba0ddf7d7e1652f9435163e6fc7"
CASE5_OUTPUT_SHA256 = "229fab033e6389de8eb25a56b4e9c72baedfe170979a2427dfd33d1ecf7a1a57"
N = 21


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str, expected: str):
    assert digest(path) == expected
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


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


def positions(word: int) -> str:
    return ",".join(str(index) for index in range(N) if (word >> index) & 1)


def verify_input_orbits(directory: Path) -> None:
    fourth = load_module(
        directory.parent / "qlp42_q1_b16_fourth_order" / "verify_b16_fourth_order.py",
        "shell_fourth",
        FOURTH_SHA256,
    )
    sums = load_module(
        directory.parent / "qlp42_q1_b16_sum_intersection" / "verify_b16_sum_intersection.py",
        "shell_sums",
        SUM_SHA256,
    )
    base_module = fourth.load_dependency()
    survivors = sums.orbit_representatives(fourth, base_module)
    assert len(survivors) == 32
    rows = []
    full = (1 << N) - 1
    for result in survivors:
        equal_word = full ^ result.b_word ^ 1
        rows.append((positions(equal_word), positions(result.a_word), result.rank))
    rows.sort()
    expected = "b_equal_positions\ta_opposite_orbit_representative\tfourth_order_rank\n"
    expected += "".join("\t".join(map(str, row)) + "\n" for row in rows)
    assert expected == (directory / "input_orbits.tsv").read_text(encoding="utf-8")


def main() -> None:
    directory = Path(__file__).resolve().parent
    for name, expected in HASHES.items():
        assert digest(directory / name) == expected
    verify_input_orbits(directory)

    case5 = directory.parent / "qlp42_q1_b16_sixth_order_s"
    assert digest(case5 / "verify_sixth_s.cpp") == CASE5_CPP_SHA256
    assert digest(case5 / "verification_output.txt") == CASE5_OUTPUT_SHA256
    case5_output = (case5 / "verification_output.txt").read_text(encoding="utf-8")
    assert "sixth_s_surviving_a_rotation_orbits=0\n" in case5_output

    with tempfile.TemporaryDirectory(prefix="qlp42-shell-") as temporary:
        temporary_path = Path(temporary)
        sixth = temporary_path / "independent_sixth"
        seventh = temporary_path / "independent_seventh"
        subprocess.run(
            compiler_command(directory / "independent_sixth_cpp.cpp", sixth), check=True
        )
        subprocess.run(
            compiler_command(directory / "independent_seventh_cpp.cpp", seventh), check=True
        )
        sixth_output = subprocess.run(
            [str(sixth)], cwd=directory, check=True, text=True, capture_output=True
        ).stdout
        sixth_table = subprocess.run(
            [str(sixth), "--dump-table"], cwd=directory,
            check=True, text=True, capture_output=True,
        ).stdout
        seventh_cpp = subprocess.run(
            [str(seventh)], cwd=directory, check=True, text=True, capture_output=True
        ).stdout

    expected_sixth = (directory / "sixth_verification_output.txt").read_text(encoding="utf-8")
    expected_table = (directory / "sixth_orbit_table.tsv").read_text(encoding="utf-8")
    expected_seventh = (directory / "seventh_verification_output.txt").read_text(encoding="utf-8")
    assert sixth_output == expected_sixth
    assert sixth_table == expected_table
    sixth_numpy = subprocess.run(
        [sys.executable, str(directory / "prototype_numpy.py"), "--dump-table"],
        cwd=directory, check=True, text=True, capture_output=True,
    ).stdout
    assert sixth_numpy == expected_table
    seventh_numpy = subprocess.run(
        [sys.executable, str(directory / "prototype_seventh_s.py")],
        cwd=directory, check=True, text=True, capture_output=True,
    ).stdout
    assert seventh_cpp == expected_seventh
    assert seventh_numpy == expected_seventh

    print(sixth_output, end="")
    print(expected_seventh, end="")
    print("independent_sixth_classifications=160")
    print("independent_seventh_classifications=2")
    print("case5_prior_certificate=verified")
    print("q1_b16_shell=excluded")


if __name__ == "__main__":
    main()
