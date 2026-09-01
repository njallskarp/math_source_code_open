#!/usr/bin/env python3
"""Build, run, and cross-check both exact q=41 weight-20 verifiers."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CPP = HERE / "verify_weight20_seventh_h.cpp"
NUMPY = HERE / "independent_numpy.py"

EXPECTED = {
    "b_exact_sum_assignments": "184756",
    "b_fourth_fingerprints": "512",
    "b_fifth_fingerprints": "72688",
    "b_sixth_fingerprints": "92128",
    "b_seventh_fingerprints": "92854",
    "b_exact_paf_vectors": "92854",
    "s_b_exact_sum_assignments": "125970",
    "s_b_fourth_fingerprints": "511",
    "a_exact_sum_assignments": "127704",
    "fourth_order_h_compatible_assignments": "127704",
    "fifth_order_h_compatible_assignments": "16272",
    "sixth_order_h_compatible_assignments": "720",
    "seventh_order_h_compatible_assignments": "0",
    "exact_h_compatible_assignments": "0",
    "fourth_order_h_surviving_a_axes": "512",
    "fifth_order_h_surviving_a_axes": "418",
    "sixth_order_h_surviving_a_axes": "4",
    "seventh_order_h_surviving_a_axes": "0",
    "exact_h_surviving_a_axes": "0",
    "case_3_all_sums_fourth_order_a_axes": "388",
    "case_3_all_sums_plus_fifth_h_a_axes": "317",
}


def compiler_command(output: Path, sanitizers: bool) -> list[str]:
    compiler = os.environ.get("CXX") or shutil.which("clang++") or shutil.which("g++")
    if compiler is None:
        raise RuntimeError("no C++20 compiler found")
    flags = ["-std=c++20", "-Wall", "-Wextra", "-pedantic"]
    if sanitizers:
        flags += [
            "-O1",
            "-g",
            "-fsanitize=address,undefined",
            "-fno-omit-frame-pointer",
        ]
    else:
        flags += ["-O3"]
    if platform.system() == "Darwin" and shutil.which("xcrun"):
        sdk = subprocess.run(
            ["xcrun", "--show-sdk-path"], check=True, text=True, capture_output=True
        ).stdout.strip()
        flags += ["-isystem", str(Path(sdk) / "usr/include/c++/v1")]
    return [compiler, *flags, str(CPP), "-o", str(output)]


def parse(text: str) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    sixth_axes: list[str] = []
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key == "sixth_order_a_axis":
            sixth_axes.append(value)
        else:
            values[key] = value
    return values, sixth_axes


def verify(cpp_text: str, numpy_text: str) -> None:
    cpp, cpp_axes = parse(cpp_text)
    numpy, _ = parse(numpy_text)
    for key, expected in EXPECTED.items():
        assert cpp.get(key) == expected, (key, cpp.get(key), expected)
    assert cpp_axes == ["0", "356", "667", "1023"]

    translations = {
        "b_order_4_fingerprints": "b_fourth_fingerprints",
        "b_order_5_fingerprints": "b_fifth_fingerprints",
        "b_order_6_fingerprints": "b_sixth_fingerprints",
        "b_order_7_fingerprints": "b_seventh_fingerprints",
        "order_4_h_compatible_assignments": "fourth_order_h_compatible_assignments",
        "order_5_h_compatible_assignments": "fifth_order_h_compatible_assignments",
        "order_6_h_compatible_assignments": "sixth_order_h_compatible_assignments",
        "order_7_h_compatible_assignments": "seventh_order_h_compatible_assignments",
        "order_4_h_surviving_a_axes": "fourth_order_h_surviving_a_axes",
        "order_5_h_surviving_a_axes": "fifth_order_h_surviving_a_axes",
        "order_6_h_surviving_a_axes": "sixth_order_h_surviving_a_axes",
        "order_7_h_surviving_a_axes": "seventh_order_h_surviving_a_axes",
    }
    for numpy_key, cpp_key in translations.items():
        assert numpy.get(numpy_key) == cpp[cpp_key], (numpy_key, cpp_key)
    for key in (
        "b_exact_sum_assignments",
        "b_exact_paf_vectors",
        "s_b_exact_sum_assignments",
        "s_b_fourth_fingerprints",
        "a_exact_sum_assignments",
        "case_3_all_sums_fourth_order_a_axes",
        "case_3_all_sums_plus_fifth_h_a_axes",
    ):
        assert numpy.get(key) == cpp[key], key
    assert numpy.get("sixth_order_a_axes") == "0,356,667,1023"
    assert numpy.get("seventh_order_weight20_exclusion") == "verified"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sanitizers", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="qlp42-q41-weight20-") as temporary:
        executable = Path(temporary) / "verify_weight20_seventh_h"
        subprocess.run(compiler_command(executable, args.sanitizers), check=True)
        cpp = subprocess.run([str(executable)], check=True, text=True, capture_output=True)
    numpy = subprocess.run(
        [sys.executable, str(NUMPY)], check=True, text=True, capture_output=True
    )
    verify(cpp.stdout, numpy.stdout)
    print(cpp.stdout, end="")
    print("independent_numpy_summary=matched")
    print("sixth_order_a_axes=0,356,667,1023")
    print(f"sanitizers={'enabled' if args.sanitizers else 'disabled'}")
    print("independent_agreement=verified")
    print("seventh_order_weight20_exclusion=verified")


if __name__ == "__main__":
    main()
