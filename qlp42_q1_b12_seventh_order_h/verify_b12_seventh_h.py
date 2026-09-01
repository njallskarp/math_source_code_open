#!/usr/bin/env python3
"""End-to-end verifier for the QLP-42 q=1, b=12 seventh-order H closure."""

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
    "full_seventh_h.cpp": "87b5fecb68a5e4fb345ae8f0418a00db5474376a117a6f69358a66aa22019f57",
    "independent_numpy.py": "75474d7d47eff9c7c70af114e80baccdb2ae5ef2761f5a7899a9bbf803ae89ff",
}
PROTOTYPE_SHA256 = "ab9808ab51d8c1a39d68897f4b0bf4c43179067b8f6dff4a69209a9e72f90ca4"
DIRECT_NUMPY_SHA256 = "baafcf32595790a4522818e1befb033017e4e0e0743f0124e9fa06df486a4688"
B12_CPP_SHA256 = "d8995d341e111c329191d3e9fef9e777c186c50ebb80db8d08e7d503283749cf"
B14_CPP_SHA256 = "a861b0275d259d2f687d5aa9cd28a2a167cc05222ea1b4439f933e43a2ef6cb1"
THIRD_ORDER_SHA256 = "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"

EXPECTED = (
    "input_sixth_h_orbit_incidences=79\n"
    "input_sixth_h_rows=77\n"
    "input_unique_a_supports=77\n"
    "input_unique_b_masks=18\n"
    "supports_completed=77\n"
    "seventh_h_surviving_case0_orbits=0\n"
    "seventh_h_surviving_case2_orbits=0\n"
    "seventh_h_surviving_case0_masks=0\n"
    "seventh_h_surviving_case2_masks=0\n"
    "seventh_h_surviving_rows=0\n"
    "h_a_seventh_fingerprint_range=106600-213444\n"
    "h_b_seventh_fingerprint_range=296-338\n"
    "h_b_exact_assignment_range=608-676\n"
    "h_a_exact_assignments=65740752\n"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compiler_command(source: Path, output: Path) -> list[str]:
    compiler = (
        os.environ.get("CXX")
        or shutil.which("g++-16")
        or shutil.which("g++-15")
        or shutil.which("g++")
        or shutil.which("c++")
    )
    assert compiler is not None, "a C++20 compiler is required"
    command = [compiler]
    if platform.system() == "Darwin" and "g++" not in Path(compiler).name:
        sdk = subprocess.run(
            ["xcrun", "--show-sdk-path"], check=True, text=True, capture_output=True
        ).stdout.strip()
        sdk_cpp = Path(sdk) / "usr" / "include" / "c++" / "v1"
        if sdk_cpp.is_dir():
            command += ["-isysroot", sdk, f"-I{sdk_cpp}", "-stdlib=libc++"]
    return command + [
        "-O3", "-std=c++20", "-UNDEBUG", "-Wall", "-Wextra", "-pedantic",
        str(source), "-o", str(output),
    ]


def main() -> None:
    directory = Path(__file__).resolve().parent
    for name, expected in HASHES.items():
        assert digest(directory / name) == expected
    inherited = directory.parent / "qlp42_q1_b12_sixth_order_h"
    assert digest(inherited / "prototype_sixth_h.cpp") == PROTOTYPE_SHA256
    assert digest(inherited / "independent_numpy.py") == DIRECT_NUMPY_SHA256
    assert digest(
        directory.parent / "qlp42_q1_b12_sixth_order_s" / "independent_cpp.cpp"
    ) == B12_CPP_SHA256
    assert digest(
        directory.parent / "qlp42_q1_b14_sixth_order_s" / "independent_cpp.cpp"
    ) == B14_CPP_SHA256
    assert digest(
        directory.parent / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py"
    ) == THIRD_ORDER_SHA256

    with tempfile.TemporaryDirectory(prefix="qlp42-b12-seventh-h-") as temporary:
        executable = Path(temporary) / "full_seventh_h"
        subprocess.run(
            compiler_command(directory / "full_seventh_h.cpp", executable),
            check=True,
        )
        cpp_output = subprocess.run(
            [str(executable), "--quiet"],
            cwd=directory,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        frontier = subprocess.run(
            [str(executable), "--dump-sixth-frontier"],
            cwd=directory,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        numpy_output = subprocess.run(
            [sys.executable, str(directory / "independent_numpy.py"), "--quiet"],
            cwd=directory,
            input=frontier,
            check=True,
            text=True,
            capture_output=True,
        ).stdout

    assert cpp_output == EXPECTED + (
        "h_a_quadratic_direct_checks=12457984\n"
        "h_a_quadratic_global_audits=157696\n"
        "full_seventh_h_certificate=verified\n"
    )
    assert numpy_output == EXPECTED + (
        "h_a_direct_paf_evaluations=65740752\n"
        "independent_seventh_numpy_certificate=verified\n"
    )
    print(cpp_output, end="")
    print(numpy_output, end="")
    print("full_two_implementation_seventh_h_certificate=verified")


if __name__ == "__main__":
    main()
