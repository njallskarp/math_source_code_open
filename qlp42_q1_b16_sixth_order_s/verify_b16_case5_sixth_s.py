#!/usr/bin/env python3
"""Run both exhaustive case-5 sixth-order S implementations."""

from __future__ import annotations

import hashlib
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FIFTH_S_SHA256 = "fac0710d70794f6543b1a667fbac413d196b41dc75ed030c317b3d43613fe05c"
FIFTH_S_TABLE_SHA256 = "528186dc709f546cd6fd1aa746ffcba0d8f1d3b7cbcc7a250ceb13b4df75af6d"
CPP_SHA256 = "4016be38220c662d0feb1ae4139184ad9e424ba0ddf7d7e1652f9435163e6fc7"
NUMPY_AUDIT_SHA256 = "12c4f07fbed366c22b2ec552cb52e1b79034503f90c2247338451d9649e9de95"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def main() -> None:
    directory = Path(__file__).resolve().parent
    predecessor = directory.parent / "qlp42_q1_b16_fifth_order_s"
    fifth_s = predecessor / "verify_b16_case5_fifth_s.py"
    fifth_s_table = predecessor / "orbit_table.tsv"
    cpp = directory / "verify_sixth_s.cpp"
    independent = directory / "independent_numpy_audit.py"
    assert digest(fifth_s) == FIFTH_S_SHA256
    assert digest(fifth_s_table) == FIFTH_S_TABLE_SHA256
    assert digest(cpp) == CPP_SHA256
    assert digest(independent) == NUMPY_AUDIT_SHA256

    with tempfile.TemporaryDirectory(prefix="qlp42-sixth-s-") as temporary:
        executable = Path(temporary) / "verify_sixth_s"
        subprocess.run(compiler_command(cpp, executable), check=True)
        def run_cpp(*arguments: str) -> str:
            return subprocess.run(
                [str(executable), *arguments], cwd=directory,
                check=True, text=True, capture_output=True,
            ).stdout
        output = run_cpp()
        table = run_cpp("--dump-table")

    expected_output = (directory / "verification_output.txt").read_text(encoding="utf-8")
    expected_table = (directory / "orbit_table.tsv").read_text(encoding="utf-8")
    assert output == expected_output
    assert table == expected_table
    independent_table = subprocess.run(
        [sys.executable, str(independent)], cwd=directory,
        check=True, text=True, capture_output=True,
    ).stdout
    assert independent_table == expected_table
    print(output, end="")
    print("independent_direct_mod8_classifications=16")


if __name__ == "__main__":
    main()
