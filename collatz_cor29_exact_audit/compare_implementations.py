#!/usr/bin/env python3
"""Compare the Python reference and compact-invariant C++ auditors."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> dict[str, str]:
    completed = subprocess.run(
        command, check=True, capture_output=True, text=True
    )
    result: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--depth", type=int, action="append", default=[])
    parser.add_argument("--c", type=int, default=1536)
    args = parser.parse_args()

    depths = args.depth or [12, 16, 20]
    reference = Path(__file__).with_name("audit_prefix.py")
    for depth in depths:
        python_result = run(
            [sys.executable, str(reference), "--depth", str(depth), "--c", str(args.c)]
        )
        cpp_result = run(
            [str(args.binary), "--depth", str(depth), "--c", str(args.c)]
        )
        cpp_result.pop("elapsed_seconds", None)
        if cpp_result != python_result:
            differing_keys = sorted(set(cpp_result) | set(python_result))
            differences = [
                f"{key}: python={python_result.get(key)!r}, cpp={cpp_result.get(key)!r}"
                for key in differing_keys
                if python_result.get(key) != cpp_result.get(key)
            ]
            raise SystemExit(
                f"depth {depth} disagrees:\n" + "\n".join(differences)
            )
        print(f"depth={depth}: exact match")


if __name__ == "__main__":
    main()
