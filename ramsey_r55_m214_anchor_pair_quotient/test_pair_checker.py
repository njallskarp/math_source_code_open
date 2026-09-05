#!/usr/bin/env python3
"""Negative controls for the independent C++ pair-table checker."""

from __future__ import annotations

import argparse
import csv
import subprocess
import tempfile
from pathlib import Path


def run(checker: Path, table: Path) -> bool:
    return subprocess.run(
        (str(checker), str(table)), stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, check=False,
    ).returncode == 0


def write(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="ascii", newline="") as destination:
        out = csv.writer(destination, dialect="unix")
        out.writerow(header)
        out.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--types", type=Path, required=True)
    args = parser.parse_args()
    checker = args.checker.resolve(strict=True)
    table = args.types.resolve(strict=True)
    with table.open(encoding="ascii", newline="") as source:
        records = list(csv.reader(source))
    header, rows = records[0], records[1:]
    if not run(checker, table):
        raise AssertionError("valid table rejected")
    with tempfile.TemporaryDirectory() as raw:
        directory = Path(raw)
        missing = directory / "missing.tsv"
        write(missing, header, rows[:-1])
        if run(checker, missing):
            raise AssertionError("missing type accepted")
        changed = directory / "changed.tsv"
        altered = [row[:] for row in rows]
        altered[0][4] = str(int(altered[0][4]) + 1)
        write(changed, header, altered)
        if run(checker, changed):
            raise AssertionError("changed cell accepted")
        duplicate = directory / "duplicate.tsv"
        write(duplicate, header, rows[:-1] + [rows[0]])
        if run(checker, duplicate):
            raise AssertionError("duplicate/missing key accepted")
    print("PASS pair_checker_controls valid=accepted missing/changed/duplicate=rejected")


if __name__ == "__main__":
    main()
