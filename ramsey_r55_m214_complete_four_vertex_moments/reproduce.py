#!/usr/bin/env python3
"""Regenerate and check the predecessor, then all physical four-vertex moments."""

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PRIOR_SHA = "37bdd8a6d9045682f7a0ab4e4f6068f33a2783489a4481bbaec394192405bf0b"


def run(script, *args):
    result = subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                            check=True, text=True, capture_output=True)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path, help="new directory outside the repository")
    args = parser.parse_args()
    work = args.work.resolve()
    if work == REPO or REPO in work.parents:
        raise ValueError("generated state must be outside the source repository")
    prior = REPO / "ramsey_r55_m214_global_star_moments/reproduce.py"
    if hashlib.sha256(prior.read_bytes()).hexdigest() != PRIOR_SHA:
        raise ValueError("changed predecessor reproducer")
    work.mkdir(parents=True, exist_ok=False)
    run(prior, work / "prior")
    run(HERE / "test_validate.py")
    run(HERE / "witness.py", "--vector", work / "points.tsv", "--moments", work / "moments.tsv", "--four", work / "four-atoms.tsv")
    result = run(HERE / "validate.py", "--vector", work / "points.tsv",
                 "--moments", work / "moments.tsv", "--four", work / "four-atoms.tsv",
                 "--old-vector", work / "prior/points.tsv", "--old-moments", work / "prior/moments.tsv",
                 "--opb", work / "prior/prior/prior/m214-3323.opb")
    if result != (HERE / "EXPECTED_RESULT.json").read_text():
        raise ValueError("complete check differs from EXPECTED_RESULT.json: " + result)
    print(result, end="")


if __name__ == "__main__":
    main()
