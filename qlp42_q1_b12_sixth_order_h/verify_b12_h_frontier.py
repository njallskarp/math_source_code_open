#!/usr/bin/env python3
"""End-to-end verifier for the QLP-42 q=1, b=12 H reduction."""

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
    "prototype_sixth_h.cpp": "ab9808ab51d8c1a39d68897f4b0bf4c43179067b8f6dff4a69209a9e72f90ca4",
    "independent_numpy.py": "baafcf32595790a4522818e1befb033017e4e0e0743f0124e9fa06df486a4688",
    "precomputed_full_h.cpp": "bc225346f58952b5411fcda30e1a82c5d3e364347367ed43906a1cd817db57af",
    "independent_full_numpy.py": "64ab4c857eec2d4c961e098520deb03ca6a4e8b342fe5d365b273a00887495e4",
}
B12_CPP_SHA256 = "d8995d341e111c329191d3e9fef9e777c186c50ebb80db8d08e7d503283749cf"
B14_CPP_SHA256 = "a861b0275d259d2f687d5aa9cd28a2a167cc05222ea1b4439f933e43a2ef6cb1"
THIRD_ORDER_SHA256 = "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compiler_command(source: Path, output: Path) -> list[str]:
    compiler = os.environ.get("CXX") or shutil.which("c++")
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
        "-O3", "-std=c++20", "-Wall", "-Wextra", "-pedantic",
        str(source), "-o", str(output),
    ]


def main() -> None:
    directory = Path(__file__).resolve().parent
    for name, expected in HASHES.items():
        assert digest(directory / name) == expected
    b12_cpp = directory.parent / "qlp42_q1_b12_sixth_order_s" / "independent_cpp.cpp"
    b14_cpp = directory.parent / "qlp42_q1_b14_sixth_order_s" / "independent_cpp.cpp"
    third = directory.parent / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py"
    assert digest(b12_cpp) == B12_CPP_SHA256
    assert digest(b14_cpp) == B14_CPP_SHA256
    assert digest(third) == THIRD_ORDER_SHA256

    numpy_output = subprocess.run(
        [sys.executable, str(directory / "independent_numpy.py")],
        cwd=directory,
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    assert numpy_output == (
        "input_b_masks=98\n"
        "positive_center_h_b_exact_assignment_range=608-676\n"
        "positive_center_h_b_fingerprint_range=260-338\n"
        "negative_center_h_b_exact_assignments=0\n"
        "case3_h_center=1\n"
        "case3_h_b_exact_assignments=608\n"
        "case3_h_b_fingerprints=304\n"
        "case3_h_a_exact_assignments=853776\n"
        "case3_h_a_needed_fingerprints=101390\n"
        "case3_direct_paf_evaluations=853776\n"
        "case3_sixth_h_intersection=0\n"
        "case4_h_center=-1\n"
        "case4_h_b_exact_assignments=0\n"
        "case4_sixth_h_intersection=0\n"
        "independent_numpy_certificate=verified\n"
    )

    with tempfile.TemporaryDirectory(prefix="qlp42-b12-h-") as temporary:
        executable = Path(temporary) / "prototype_sixth_h"
        full_executable = Path(temporary) / "precomputed_full_h"
        subprocess.run(
            compiler_command(directory / "prototype_sixth_h.cpp", executable),
            check=True,
        )
        subprocess.run(
            compiler_command(directory / "precomputed_full_h.cpp", full_executable),
            check=True,
        )
        cpp_output = subprocess.run(
            [str(executable), "--quiet"],
            cwd=directory,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        full_cpp_output = subprocess.run(
            [str(full_executable), "--quiet"],
            cwd=directory,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        frontier = subprocess.run(
            [str(full_executable), "--dump-frontier"],
            cwd=directory,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        full_numpy_output = subprocess.run(
            [sys.executable, str(directory / "independent_full_numpy.py"), "--quiet"],
            cwd=directory,
            input=frontier,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
    assert cpp_output == (
        "input_b_masks=98\n"
        "negative_center_h_b_exact_assignments=0\n"
        "exact_h_sum_eliminated_cases=1,4,5\n"
        "target_cases=3,4\n"
        "case3_sixth_h_surviving_orbits=0\n"
        "case4_sixth_h_surviving_orbits=0\n"
        "remaining_case02_orbit_incidences=395\n"
        "remaining_case02_rows=375\n"
        "remaining_case02_unique_a_supports=345\n"
        "remaining_case02_unique_b_masks=29\n"
        "remaining_case02_unique_pairs=375\n"
        "h_classifications=2\n"
        "h_axes_examined=2048\n"
        "h_affine_direct_audits=2048\n"
        "prototype_certificate=verified\n"
    )
    assert full_cpp_output == (
        "input_case02_orbit_incidences=395\n"
        "input_case02_rows=375\n"
        "input_unique_a_supports=345\n"
        "input_unique_b_masks=29\n"
        "supports_completed=345\n"
        "sixth_h_surviving_case0_orbits=61\n"
        "sixth_h_surviving_case2_orbits=18\n"
        "sixth_h_surviving_case0_masks=17\n"
        "sixth_h_surviving_case2_masks=8\n"
        "sixth_h_surviving_rows=77\n"
        "h_a_fingerprint_range=96962-213199\n"
        "h_a_exact_assignments=294552720\n"
        "h_a_affine_direct_audits=706560\n"
        "full_precomputed_certificate=verified\n"
    )
    assert full_numpy_output == (
        "input_case02_orbit_incidences=395\n"
        "input_case02_rows=375\n"
        "input_unique_a_supports=345\n"
        "input_unique_b_masks=29\n"
        "supports_completed=345\n"
        "sixth_h_surviving_case0_orbits=61\n"
        "sixth_h_surviving_case2_orbits=18\n"
        "sixth_h_surviving_case0_masks=17\n"
        "sixth_h_surviving_case2_masks=8\n"
        "sixth_h_surviving_rows=77\n"
        "h_a_fingerprint_range=96962-213199\n"
        "h_a_exact_assignments=294552720\n"
        "h_a_direct_paf_evaluations=294552720\n"
        "independent_full_numpy_certificate=verified\n"
    )
    print(numpy_output, end="")
    print(cpp_output, end="")
    print(full_cpp_output, end="")
    print(full_numpy_output, end="")
    print("full_two_implementation_certificate=verified")


if __name__ == "__main__":
    main()
