#!/usr/bin/env python3
"""Independent driver and witness audit for the case-5 fifth-order H filter."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

N = 21
PI = (1, 1)
G = tuple[int, int]
FOURTH_SHA256 = "a5f616a19e241bcdced0962a2843631d1bb13a30de41cfbc05a2c0999e74bacf"
FIFTH_S_SHA256 = "fac0710d70794f6543b1a667fbac413d196b41dc75ed030c317b3d43613fe05c"
FIFTH_S_TABLE_SHA256 = "528186dc709f546cd6fd1aa746ffcba0d8f1d3b7cbcc7a250ceb13b4df75af6d"
CPP_SHA256 = "7a030270eb7d14dd2d2cf86879a83142d2002c5f2520e42e1ca6512d633da65e"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_fourth(directory: Path):
    path = directory.parent / "qlp42_q1_b16_fourth_order" / "verify_b16_fourth_order.py"
    assert digest(path) == FOURTH_SHA256
    spec = importlib.util.spec_from_file_location("fifth_h_fourth_dependency", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
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


def parse_positions(text: str) -> list[int]:
    return [int(value) for value in text.split(",")]


def bits(text: str) -> list[int]:
    return [int(value) for value in text]


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def audit_witnesses(fourth, directory: Path) -> int:
    with (directory / "witnesses.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 15
    for row in rows:
        a_s_positions = set(parse_positions(row["a_opposite_orbit_representative"]))
        a_h_positions = [position for position in range(N) if position not in a_s_positions]
        a_axes = bits(row["a_h_axes"])
        a_signs = bits(row["a_h_signs"])
        assert len(a_h_positions) == len(a_axes) == len(a_signs) == 16
        a = [(0, 0)] * N
        for position, axis, sign in zip(a_h_positions, a_axes, a_signs, strict=True):
            a[position] = fourth.multiply(PI, fourth.unit(axis, sign))

        equal_positions = parse_positions(row["b_equal_positions"])
        equal_word = sum(1 << position for position in equal_positions)
        b_word = ((1 << N) - 1) ^ equal_word ^ 1
        theta = fourth.theta_values(fourth.load_dependency(), b_word)
        shifts = [shift for shift in range(1, 11) if not (b_word >> shift) & 1]
        b_axes = bits(row["b_h_axes"])
        b_plus = bits(row["b_h_plus_signs"])
        b_minus = bits(row["b_h_minus_signs"])
        assert len(shifts) == len(b_axes) == len(b_plus) == len(b_minus) == 2
        b = [(0, 0)] * N
        for shift, axis, plus_sign, minus_sign in zip(
            shifts, b_axes, b_plus, b_minus, strict=True
        ):
            b[shift] = fourth.multiply(PI, fourth.unit(axis, plus_sign))
            b[N - shift] = fourth.multiply(
                PI, fourth.unit(axis ^ theta[shift - 1], minus_sign)
            )
        b[0] = fourth.unit(0, int(row["b_h_center_sign"]))
        assert tuple(map(sum, zip(*a, strict=True))) == (0, 0)
        assert tuple(map(sum, zip(*b, strict=True))) == (1, 0)
        for shift in range(1, 11):
            residual = fourth.subtract(
                fourth.add(fourth.paf(a, shift), fourth.paf(b, shift)), (-2, 0)
            )
            for _ in range(5):
                residual = fourth.div_pi(residual)
    return len(rows)


def main() -> None:
    directory = Path(__file__).resolve().parent
    fifth_s_directory = directory.parent / "qlp42_q1_b16_fifth_order_s"
    fifth_s = fifth_s_directory / "verify_b16_case5_fifth_s.py"
    fifth_s_table = fifth_s_directory / "orbit_table.tsv"
    source = directory / "verify_fifth_h.cpp"
    assert digest(fifth_s) == FIFTH_S_SHA256
    assert digest(fifth_s_table) == FIFTH_S_TABLE_SHA256
    assert digest(source) == CPP_SHA256
    fourth = load_fourth(directory)

    with tempfile.TemporaryDirectory(prefix="qlp42-fifth-h-") as temporary:
        executable = Path(temporary) / "verify_fifth_h"
        subprocess.run(compiler_command(source, executable), check=True)
        def run(*arguments: str) -> str:
            return subprocess.run(
                [str(executable), *arguments], cwd=directory,
                check=True, text=True, capture_output=True,
            ).stdout
        output = run()
        assert output == (directory / "verification_output.txt").read_text(encoding="utf-8")
        assert run("--dump-table") == (directory / "orbit_table.tsv").read_text(encoding="utf-8")
        assert run("--dump-witnesses") == (directory / "witnesses.tsv").read_text(encoding="utf-8")

    witness_checks = audit_witnesses(fourth, directory)
    print(output, end="")
    print(f"independent_python_full_witness_checks={witness_checks}")


if __name__ == "__main__":
    main()
