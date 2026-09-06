#!/usr/bin/env python3
"""Regenerate the full base formula and check the reanchored moment repair."""

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PRIOR_SHA = "d22f99e88b6242d86552a50437120b0c0f55ff40849c637e38f9b32a0c9c599b"


def run(script, *args):
    result = subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                            check=True, text=True, capture_output=True)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path, help="new directory outside the source repository")
    args = parser.parse_args()
    work = args.work.resolve()
    if work == REPO or REPO in work.parents:
        raise ValueError("generated state must be outside the source repository")
    prior = REPO / "ramsey_r55_m214_coupled_column_separator/reproduce.py"
    if hashlib.sha256(prior.read_bytes()).hexdigest() != PRIOR_SHA:
        raise ValueError("changed predecessor reproducer")
    work.mkdir(parents=True, exist_ok=False)
    # Reuse the published predecessor chain and its complete verification.
    run(prior, work / "prior")
    run(HERE / "test_check.py")
    run(HERE / "witness.py", "--output", work / "points.tsv")
    result = run(HERE / "check.py", "--vector", work / "points.tsv",
                 "--opb", work / "prior/m214-3323.opb")
    if result != (HERE / "EXPECTED_RESULT.json").read_text():
        raise ValueError("complete verification differs from EXPECTED_RESULT.json: " + result)
    print(result, end="")


if __name__ == "__main__":
    main()
