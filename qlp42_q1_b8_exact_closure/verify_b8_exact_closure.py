#!/usr/bin/env python3
"""Build and run both exact QLP-42 q=1, b=8 proof routes."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


NUMPY_SHA256 = "aab9dd06160041c78063058da7a59a5ca4d18a580e67ff0b38957c39760bb82b"
SCALAR_SHA256 = "466c072bf92280717c5f2dc3be9a3388ad17357bf0859531536156f6ce5d427e"
THIRD_ORDER_SHA256 = "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"
CPP_TYPES_SHA256 = "a861b0275d259d2f687d5aa9cd28a2a167cc05222ea1b4439f933e43a2ef6cb1"
EXACT_H_FRONTIER_SHA256 = "0e3fa74a39e7a5ff91ef3d56a33a5f1a62a9528839f6facfdd47e2b789418cfd"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(output: str) -> dict[str, str]:
    result = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def run(command: list[str], cwd: Path) -> tuple[str, float]:
    start = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return completed.stdout, time.monotonic() - start


def main() -> None:
    directory = Path(__file__).resolve().parent
    repository = directory.parent
    numpy_source = directory / "independent_numpy.py"
    scalar_source = directory / "independent_scalar.cpp"
    third_order = repository / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py"
    cpp_types = repository / "qlp42_q1_b14_sixth_order_s" / "independent_cpp.cpp"
    assert digest(numpy_source) == NUMPY_SHA256
    assert digest(scalar_source) == SCALAR_SHA256
    assert digest(third_order) == THIRD_ORDER_SHA256
    assert digest(cpp_types) == CPP_TYPES_SHA256

    compiler = shutil.which("g++-16") or shutil.which("g++")
    assert compiler is not None, "GCC with C++20 support is required"
    with tempfile.TemporaryDirectory(prefix="qlp42-b8-") as temporary:
        executable = Path(temporary) / "independent_scalar"
        subprocess.run(
            [
                compiler,
                "-std=c++20",
                "-O3",
                "-Wall",
                "-Wextra",
                "-Wpedantic",
                str(scalar_source),
                "-o",
                str(executable),
            ],
            cwd=repository,
            check=True,
        )

        dump, _ = run([str(executable), "--dump-input"], repository)
        lines = dump.splitlines()
        assert lines[0] == "a_s_word\tb_s_word"
        rows = [tuple(map(int, line.split("\t"))) for line in lines[1:]]
        assert len(rows) == len(set(rows)) == 40
        assert len({left for left, _ in rows}) == 40
        assert len({right for _, right in rows}) == 11
        stream = "".join(f"{left},{right}\n" for left, right in rows).encode()
        assert hashlib.sha256(stream).hexdigest() == EXACT_H_FRONTIER_SHA256

        scalar_output, scalar_seconds = run([str(executable), "--quiet"], repository)
        numpy_output, numpy_seconds = run([sys.executable, str(numpy_source)], repository)

    scalar = parse(scalar_output)
    numpy = parse(numpy_output)
    assert scalar["input_exact_h_frontier_sha256"] == EXACT_H_FRONTIER_SHA256
    assert numpy["exact_h_frontier_sha256"] == EXACT_H_FRONTIER_SHA256
    assert scalar["s_b_exact_assignments_by_case"] == numpy["s_b_exact_assignments_by_case"]
    assert scalar["exact_s_surviving_case_incidences"] == "0"
    assert numpy["exact_s_surviving_case_incidences"] == "0"
    assert scalar["exact_s_surviving_orbit_pairs"] == "0"
    assert numpy["exact_s_surviving_orbit_pairs"] == "0"
    assert scalar["q1_b8_shell"] == "excluded"
    assert numpy["q1_b8_shell"] == "excluded"
    assert scalar["linear_hash_matches"] == "0"
    assert numpy["exact_s_hash_false_positive_rows"] == "0"

    print("source_hashes=verified")
    print(f"exact_h_frontier_sha256={EXACT_H_FRONTIER_SHA256}")
    print("input_rotation_orbits_per_case=2350")
    print("sixth_h_orbit_pairs=739")
    print("seventh_h_orbit_pairs=54")
    print("exact_h_orbit_pairs=40")
    print("exact_s_surviving_case_incidences=0")
    print("exact_s_surviving_orbit_pairs=0")
    print("q1_b8_shell=excluded")
    print(f"scalar_cpp_seconds={scalar_seconds:.2f}")
    print(f"definition_numpy_seconds={numpy_seconds:.2f}")
    print("dual_implementation_certificate=verified")


if __name__ == "__main__":
    main()
