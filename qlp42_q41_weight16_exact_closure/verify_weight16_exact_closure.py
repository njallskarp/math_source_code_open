#!/usr/bin/env python3
"""Compile, run, hash, and independently replay the weight-16 certificate."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
PRIMARY = HERE / "verify_weight16_exact_closure.cpp"
INDEPENDENT = HERE / "independent_numpy_frontier.py"
EXPECTED_STREAM_SHA256 = "e46bcdc794b24be06743b4ecdca8a1d9feb5e501fd8e78981ad71165b2ef307b"


def parse_summary(text: str) -> dict[str, str]:
    return dict(line.split("=", 1) for line in text.splitlines() if "=" in line)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sanitizers", action="store_true")
    args = parser.parse_args()

    compiler = os.environ.get("CXX") or shutil.which("g++-16") or "clang++"
    flags = ["-std=c++20", "-O3", "-Wall", "-Wextra", "-pedantic"]
    if args.sanitizers:
        flags = [
            "-std=c++20",
            "-O1",
            "-g",
            "-fno-omit-frame-pointer",
            "-fsanitize=address,undefined",
            "-Wall",
            "-Wextra",
            "-pedantic",
        ]

    with tempfile.TemporaryDirectory(prefix="qlp42_weight16_") as temporary:
        binary = Path(temporary) / "verify_weight16_exact_closure"
        subprocess.run([compiler, *flags, str(PRIMARY), "-o", str(binary)], check=True)
        environment = os.environ.copy()
        environment.setdefault("ASAN_OPTIONS", "detect_leaks=0")
        primary = subprocess.run(
            [str(binary), "--stream"],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        if primary.stderr:
            sys.stderr.write(primary.stderr)

        before, after = primary.stdout.split("stream_begin\n", 1)
        stream, tail = after.split("stream_end\n", 1)
        assert not tail
        stream_bytes = stream.encode("utf-8")
        digest = hashlib.sha256(stream_bytes).hexdigest()
        if EXPECTED_STREAM_SHA256:
            assert digest == EXPECTED_STREAM_SHA256

        summary = parse_summary(before)
        expected = {
            "b_axis_words": "20349",
            "b_rotation_orbits": "969",
            "b_exact_sum_assignments_per_orbit": "128700",
            "order_7_surviving_axis_orbits": "36",
            "order_12_surviving_axis_orbits": "24",
            "order_12_b_orbits_with_survivors": "12",
            "exact_hs_surviving_axis_case_orbits": "0",
            "full_weight16_exclusion": "verified",
        }
        for key, value in expected.items():
            assert summary[key] == value, (key, summary[key], value)

        stream_file = Path(temporary) / "canonical_orbit_stream.txt"
        stream_file.write_text(
            "stream_begin\n" + stream + "stream_end\n", encoding="utf-8"
        )
        independent = subprocess.run(
            [sys.executable, str(INDEPENDENT), "--stream", str(stream_file)],
            check=True,
            capture_output=True,
            text=True,
        )

        print(before, end="")
        print(f"canonical_orbit_stream_sha256={digest}")
        print(independent.stdout, end="")
        print(f"sanitizers={'enabled' if args.sanitizers else 'disabled'}")
        print("implementations_agree=yes")


if __name__ == "__main__":
    main()
