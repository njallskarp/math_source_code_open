#!/usr/bin/env python3
"""Build and cross-check the independent q=1, b=10 sixth-H scans."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path


CPP_SHA256 = "e4a89f69e39b62a70582ee33be29d6dc27bea135cf454716478df2636471a22a"
NUMPY_SHA256 = "959ea6e001a807b7fc831d559593d012720264bae4e6a42d6e540cd3abd3c039"
CPP_DEPENDENCY_SHA256 = "a861b0275d259d2f687d5aa9cd28a2a167cc05222ea1b4439f933e43a2ef6cb1"
PYTHON_DEPENDENCY_SHA256 = "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(output: str):
    values = {}
    frontier = []
    for line in output.splitlines():
        key, value = line.split("=", 1)
        if key == "frontier_pair":
            frontier.append(tuple(map(int, value.split(","))))
        else:
            values[key] = value
    assert frontier == sorted(frontier)
    assert len(frontier) == len(set(frontier))
    return values, frontier


def main() -> None:
    directory = Path(__file__).resolve().parent
    cpp = directory / "explore_b10.cpp"
    numpy_source = directory / "independent_numpy.py"
    cpp_dependency = directory.parent / "qlp42_q1_b14_sixth_order_s" / "independent_cpp.cpp"
    python_dependency = (
        directory.parent / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py"
    )
    assert digest(cpp) == CPP_SHA256
    assert digest(numpy_source) == NUMPY_SHA256
    assert digest(cpp_dependency) == CPP_DEPENDENCY_SHA256
    assert digest(python_dependency) == PYTHON_DEPENDENCY_SHA256

    compiler = shutil.which("g++-16") or shutil.which("g++")
    assert compiler is not None
    with tempfile.TemporaryDirectory(prefix="b10-sixth-h-") as temporary:
        executable = Path(temporary) / "b10_sixth_h"
        subprocess.run(
            [
                compiler,
                "-std=c++20",
                "-O3",
                "-UNDEBUG",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(cpp),
                "-o",
                str(executable),
            ],
            check=True,
        )
        cpp_result = subprocess.run(
            [str(executable)], check=True, text=True, capture_output=True
        )
    numpy_result = subprocess.run(
        ["python3", str(numpy_source)], check=True, text=True, capture_output=True
    )
    cpp_values, cpp_frontier = parse(cpp_result.stdout)
    numpy_values, numpy_frontier = parse(numpy_result.stdout)

    expected = {
        "input_b_masks": "140",
        "input_labeled_type_pairs": "56490",
        "input_rotation_orbits_per_case": "2690",
        "unique_a_supports": "1972",
        "h_b_fixed_plus_1_minmax": "0,0",
        "h_b_fixed_minus_1_minmax": "3384,3384",
        "h6_b_fingerprint_range": "1564-1692",
        "h6_a_exact_assignments": "125229888",
        "h6_surviving_orbit_pairs": "198",
        "h6_surviving_b_masks": "64",
    }
    for key, value in expected.items():
        assert cpp_values[key] == value
        assert numpy_values[key] == value
    assert cpp_values["orientation_resolved_by_exact_sums"] == "verified"
    assert cpp_values["sixth_order_h_scan"] == "verified"
    assert numpy_values["independent_direct_numpy_scan"] == "verified"
    assert cpp_frontier == numpy_frontier
    assert len(cpp_frontier) == 198

    encoded = "".join(f"{a},{b}\n" for a, b in cpp_frontier).encode()
    frontier_sha256 = hashlib.sha256(encoded).hexdigest()
    print("input_rotation_orbit_pairs=2690")
    print("input_case_incidences=16140")
    print("forced_h_b_center=-1")
    print("positive_center_h_b_exact_assignments=0")
    print("negative_center_h_b_exact_assignments=3384")
    print("sixth_h_surviving_orbit_pairs=198")
    print("sixth_h_surviving_case_incidences=1188")
    print("sixth_h_surviving_b_masks=64")
    print(f"frontier_sha256={frontier_sha256}")
    print("independent_implementations_agree=verified")


if __name__ == "__main__":
    main()
