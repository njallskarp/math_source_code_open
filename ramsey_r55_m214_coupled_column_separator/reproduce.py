#!/usr/bin/env python3
"""Regenerate the pinned full OPB and check the rational interval exactly."""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


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
    work.mkdir(parents=True, exist_ok=False)
    p3160, p3228, p3254, p3274, p3323 = [work / f"m214-{h}.opb"
                                       for h in (3160, 3228, 3254, 3274, 3323)]
    run(REPO / "ramsey_r55_m214_integrated_pair_roots/generate_opb.py", "--output", p3160)
    run(REPO / "ramsey_r55_m214_all_c_footprint_bound/build.py",
        "--prior-opb", p3160, "--output-opb", p3228)
    p3160.unlink()
    run(REPO / "ramsey_r55_m214_blue_pair_footprints/build.py",
        "--prior-opb", p3228, "--output-opb", p3254)
    p3228.unlink()
    run(REPO / "ramsey_r55_m214_pair_cell_c5_lift/build.py",
        "--certificate", work / "pair-roots.tsv", "--suffix", work / "pair.opbpart",
        "--prior-opb", p3254, "--output-opb", p3274)
    p3254.unlink()
    (work / "pair.opbpart").unlink()
    run(REPO / "ramsey_r55_m214_pair_column_hull/build.py",
        "--certificate", work / "column-roots.tsv", "--suffix", work / "column.opbpart",
        "--prior-opb", p3274, "--output-opb", p3323)
    p3274.unlink()
    (work / "column.opbpart").unlink()
    run(HERE / "witness.py", "--output", work / "endpoints.tsv")
    result = run(HERE / "verify.py", "--vector", work / "endpoints.tsv", "--opb", p3323)
    expected = (HERE / "EXPECTED_RESULT.json").read_text()
    if result != expected:
        raise ValueError("complete verification differs from EXPECTED_RESULT.json: " + result)
    print(result, end="")


if __name__ == "__main__":
    main()
