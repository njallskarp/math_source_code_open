#!/usr/bin/env python3
"""Verify the exact combinatorial coverage claimed for the 67 pi^4 rows."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from verify_pi4_witnesses import read_supports, verify_row


def main() -> None:
    path = Path(__file__).parent / "pi4_witnesses.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    keys = {(int(row["q"]), int(row["orbit"]), int(row["case"])) for row in rows}
    assert len(rows) == len(keys) == 67
    for row in rows:
        verify_row(row, read_supports())

    branches = Counter(q_value for q_value, _, _ in keys)
    assert branches == Counter({5: 38, 37: 29})
    q5_orbits = {orbit for q_value, orbit, _ in keys if q_value == 5}
    q37_orbits = {orbit for q_value, orbit, _ in keys if q_value == 37}
    assert q5_orbits == set(range(18))
    assert q37_orbits == {0, 1, 2, 4, 6, 7, 8, 9, 10, 11, 13, 14, 16}
    cases = Counter((q_value, case_id) for q_value, _, case_id in keys)
    assert cases == Counter(
        {
            (5, 0): 6,
            (5, 1): 6,
            (5, 2): 9,
            (5, 3): 8,
            (5, 4): 6,
            (5, 5): 3,
            (37, 0): 6,
            (37, 1): 2,
            (37, 3): 6,
            (37, 4): 9,
            (37, 5): 6,
        }
    )
    print("rows=67;q5_rows=38;q37_rows=29")
    print("q5_support_orbits=18;q37_support_orbits=13")
    print("pi4_manifest_coverage=verified")


if __name__ == "__main__":
    main()
