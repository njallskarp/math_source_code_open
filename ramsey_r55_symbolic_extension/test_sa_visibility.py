#!/usr/bin/env python3
"""Regression test requiring agreement of both exact SA visibility checkers."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parent


def run(name: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(ROOT / name)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    derivation = run("derive_sa_visibility.py")
    verification = run("verify_sa_visibility.py")
    assert derivation["arithmetic"] == verification["arithmetic"] == "exact fractions"
    assert derivation["atom_count"] == verification["partial_assignment_count"] == 3529
    assert derivation["inequality_check_count"] == verification["inequality_check_count"] == 14116
    assert derivation["minimum_uniform_slack"] == verification["minimum_uniform_slack"]
    assert verification["verified"] is True
    print("two independent exact implementations agree")


if __name__ == "__main__":
    main()
