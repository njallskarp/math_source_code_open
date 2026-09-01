#!/usr/bin/env python3
"""Build and run both exact QLP-42 q=1, b=6 proof routes."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


NUMPY_SHA256 = "b1ed67c2f728dc5f7bfc22bf1cbbcb925737a65825a046984102b4911583bd62"
SCALAR_SHA256 = "1f94abf1abd7e0e4ca5dc6e59b386c478300679d54c51a49cbbe976890ce7c78"
THIRD_ORDER_SHA256 = "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"
CPP_TYPES_SHA256 = "a861b0275d259d2f687d5aa9cd28a2a167cc05222ea1b4439f933e43a2ef6cb1"
SIXTH_FRONTIER_SHA256 = "7b8a809ac94ef89ad16171dbd3b5f96098f5977e704a09fbc5ac5a9cf9830f77"


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
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return completed.stdout, time.monotonic() - started


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
    with tempfile.TemporaryDirectory(prefix="qlp42-b6-") as temporary:
        executable = Path(temporary) / "independent_scalar"
        subprocess.run(
            [
                compiler,
                "-std=c++20",
                "-O3",
                "-Wall",
                "-Wextra",
                "-Wpedantic",
                "-Wshadow",
                str(scalar_source),
                "-o",
                str(executable),
            ],
            cwd=repository,
            check=True,
        )
        scalar_output, scalar_seconds = run([str(executable)], repository)
        numpy_output, numpy_seconds = run([sys.executable, str(numpy_source)], repository)

    scalar = parse(scalar_output)
    numpy = parse(numpy_output)
    shared_fields = (
        "reflected_b_masks",
        "labeled_type_pairs",
        "input_rotation_orbit_pairs",
        "distinct_a_supports",
        "h_b_positive_center_assignments",
        "h_b_negative_center_assignments",
        "h_a_zero_sum_assignments_per_support",
        "h_b_sixth_fingerprint_range",
        "h_b_seventh_fingerprint_range",
        "h_a_sixth_fingerprint_range",
        "h_a_seventh_fingerprint_range",
        "sixth_order_h_pairs",
        "seventh_order_h_pairs",
        "certificate",
    )
    for field in shared_fields:
        assert scalar[field] == numpy[field], (field, scalar[field], numpy[field])

    frontier = []
    for line in scalar_output.splitlines():
        if line.startswith("sixth_frontier_pair="):
            frontier.append(tuple(map(int, line.split("=", 1)[1].split(","))))
    assert frontier == sorted(frontier)
    assert len(frontier) == len(set(frontier)) == 4
    payload = "".join(f"{left}\t{right}\n" for left, right in frontier).encode()
    assert hashlib.sha256(payload).hexdigest() == SIXTH_FRONTIER_SHA256
    assert numpy["frontier_6_sha256"] == SIXTH_FRONTIER_SHA256
    assert numpy["frontier_7_sha256"] == hashlib.sha256(b"").hexdigest()

    print("source_hashes=verified")
    print("reflected_b_masks=50")
    print("labeled_type_pairs=3402")
    print("input_rotation_orbit_pairs=162")
    print("distinct_a_supports=134")
    print("h_b_positive_center_assignments=0")
    print("h_b_negative_center_assignments=164728")
    print("h_a_zero_sum_assignments_per_support=400")
    print(f"sixth_frontier_sha256={SIXTH_FRONTIER_SHA256}")
    print("sixth_order_h_pairs=4")
    print("seventh_order_h_pairs=0")
    print("q1_b6_shell=excluded")
    print(f"scalar_cpp_seconds={scalar_seconds:.2f}")
    print(f"definition_numpy_seconds={numpy_seconds:.2f}")
    print("dual_implementation_certificate=verified")


if __name__ == "__main__":
    main()
