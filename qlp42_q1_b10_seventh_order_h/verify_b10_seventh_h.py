#!/usr/bin/env python3
"""Build and cross-check the independent q=1, b=10 seventh-H scans."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path


CPP_SHA256 = "b1af07b0d0d63adbac64b57e654b2410cfbfd1c2b143684ac8ea83cdecd0d28d"
NUMPY_SHA256 = "7a61dda941579656aad7c05c0c38b8ba92b121f3ab80baf72b16053ed153b58b"
CPP_FRONTIER_SHA256 = "e4a89f69e39b62a70582ee33be29d6dc27bea135cf454716478df2636471a22a"
CPP_RESIDUE_SHA256 = "a861b0275d259d2f687d5aa9cd28a2a167cc05222ea1b4439f933e43a2ef6cb1"
PYTHON_FRONTIER_SHA256 = "959ea6e001a807b7fc831d559593d012720264bae4e6a42d6e540cd3abd3c039"
PYTHON_TYPES_SHA256 = "904b2a5ceae881a90350aa8b818589f599e10ece10b3dfcced1123d28f5a6b15"
EXPECTED_FRONTIER_SHA256 = "e73bdd9cf30807550ef62b04698823e5d9379de43a1cac14d73e74bb47732ea1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(output: str) -> dict[str, str]:
    values = {}
    for line in output.splitlines():
        key, value = line.split("=", 1)
        values[key] = value
    return values


def frontier_digest(output: str) -> str:
    lines = output.splitlines()
    assert lines[0] == "a_s_word\tb_s_word"
    pairs = [tuple(map(int, line.split("\t"))) for line in lines[1:]]
    assert pairs == sorted(pairs)
    assert len(pairs) == len(set(pairs)) == 198
    assert len({a for a, _ in pairs}) == 192
    assert len({b for _, b in pairs}) == 64
    encoded = "".join(f"{a},{b}\n" for a, b in pairs).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    directory = Path(__file__).resolve().parent
    files = {
        directory / "full_seventh_h.cpp": CPP_SHA256,
        directory / "independent_numpy.py": NUMPY_SHA256,
        directory.parent / "qlp42_q1_b10_frontier" / "explore_b10.cpp": CPP_FRONTIER_SHA256,
        directory.parent / "qlp42_q1_b14_sixth_order_s" / "independent_cpp.cpp": CPP_RESIDUE_SHA256,
        directory.parent / "qlp42_q1_b10_frontier" / "independent_numpy.py": PYTHON_FRONTIER_SHA256,
        directory.parent / "qlp42_q1_third_order_types" / "verify_q1_third_order_types.py": PYTHON_TYPES_SHA256,
    }
    for path, expected in files.items():
        assert digest(path) == expected

    compiler = shutil.which("g++-16") or shutil.which("g++")
    assert compiler is not None
    with tempfile.TemporaryDirectory(prefix="b10-seventh-h-") as temporary:
        executable = Path(temporary) / "b10_seventh_h"
        subprocess.run(
            [
                compiler,
                "-std=c++20",
                "-O3",
                "-UNDEBUG",
                "-Wall",
                "-Wextra",
                "-pedantic",
                str(directory / "full_seventh_h.cpp"),
                "-o",
                str(executable),
            ],
            check=True,
        )
        primary = subprocess.run(
            [str(executable), "--quiet"], check=True, text=True, capture_output=True
        )
        dumped = subprocess.run(
            [str(executable), "--dump-sixth-frontier"],
            check=True,
            text=True,
            capture_output=True,
        )
    assert frontier_digest(dumped.stdout) == EXPECTED_FRONTIER_SHA256
    independent = subprocess.run(
        ["python3", str(directory / "independent_numpy.py")],
        input=dumped.stdout,
        check=True,
        text=True,
        capture_output=True,
    )

    primary_values = parse(primary.stdout)
    independent_values = parse(independent.stdout)
    expected = {
        "input_sixth_h_orbit_pairs": "198",
        "input_sixth_h_case_incidences": "1188",
        "input_unique_a_supports": "192",
        "input_unique_b_masks": "64",
        "supports_completed": "192",
        "seventh_h_surviving_orbit_pairs": "0",
        "seventh_h_surviving_case_incidences": "0",
        "seventh_h_surviving_b_masks": "0",
        "h_a_seventh_fingerprint_range": "7961-15876",
        "h_b_seventh_fingerprint_range": "1660-1692",
        "h_b_exact_assignments": "3384",
        "h_a_exact_assignments": "12192768",
    }
    for key, value in expected.items():
        assert primary_values[key] == value
        assert independent_values[key] == value
    assert primary_values["full_seventh_h_certificate"] == "verified"
    assert independent_values["independent_direct_numpy_certificate"] == "verified"

    print("input_sixth_h_orbit_pairs=198")
    print("input_sixth_h_case_incidences=1188")
    print("seventh_h_surviving_orbit_pairs=0")
    print("seventh_h_surviving_case_incidences=0")
    print("b10_shell_excluded_by_seventh_h=verified")
    print(f"sixth_frontier_sha256={EXPECTED_FRONTIER_SHA256}")
    print("independent_implementations_agree=verified")


if __name__ == "__main__":
    main()
