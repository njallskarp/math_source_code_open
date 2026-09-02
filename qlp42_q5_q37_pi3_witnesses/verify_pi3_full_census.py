#!/usr/bin/env python3
"""Exact definition-level verification of the complete QLP-42 pi^3 census."""

from __future__ import annotations

from collections import Counter
from csv import DictReader
from pathlib import Path

from verify_pi3_witnesses import read_supports, verify_row


def main() -> None:
    path = Path(__file__).parent / "full_witnesses.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(DictReader(handle, delimiter="\t"))
    keys = {(int(row["q"]), int(row["orbit"]), int(row["case"])) for row in rows}
    expected = {
        (q_value, orbit, case_id)
        for q_value in (5, 37)
        for orbit in range(18)
        for case_id in range(6)
    }
    assert len(rows) == len(keys) == len(expected) == 216
    assert keys == expected

    supports = read_supports()
    for row in rows:
        verify_row(row, supports)
    branches = Counter(int(row["q"]) for row in rows)
    cases = Counter((int(row["q"]), int(row["case"])) for row in rows)
    assert branches == Counter({5: 108, 37: 108})
    assert cases == Counter(
        {(q_value, case_id): 18 for q_value in (5, 37) for case_id in range(6)}
    )
    print("rows=216;q5_rows=108;q37_rows=108;all_cells=216")
    print("full_census_certificate=verified")


if __name__ == "__main__":
    main()
