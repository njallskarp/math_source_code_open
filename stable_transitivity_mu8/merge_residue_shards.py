#!/usr/bin/env python3
"""Merge independently generated residue-profile shards in canonical order."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from verify_certificate import parse_certificate

HEADER = "CERTIFICATE stable_transitivity_residue_profiles_v1 n=8"
COMMENT = (
    "# CLASS <source-index> tournament=<mask> dilation=<d> "
    "stabilizer=<a> deficit=<delta> candidates=<count> "
    "profile=<order-index:multiplicity,...>"
)
ROW = re.compile(r"CLASS (?P<index>\d+) .* dilation=(?P<dilation>\d+) .*")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radial-certificate", type=Path, default=Path("certificate.txt"))
    parser.add_argument("--output", type=Path, default=Path("residue_profiles.txt"))
    parser.add_argument("shards", nargs="+", type=Path)
    args = parser.parse_args()

    rows: dict[tuple[int, int], str] = {}
    for shard in args.shards:
        lines = shard.read_text(encoding="ascii").splitlines()
        if lines[:2] != [HEADER, COMMENT]:
            raise ValueError(f"{shard}: wrong header")
        for line in lines[2:]:
            match = ROW.fullmatch(line)
            if match is None:
                raise ValueError(f"{shard}: malformed row")
            key = (int(match["index"]), int(match["dilation"]))
            if key in rows:
                raise ValueError(f"duplicate profile {key}")
            rows[key] = line

    expected = [
        (source_index, dilation)
        for source_index, _, _, _ in parse_certificate(args.radial_certificate)
        for dilation in range(2, 6)
    ]
    if set(rows) != set(expected):
        missing = sorted(set(expected) - set(rows))
        extra = sorted(set(rows) - set(expected))
        raise ValueError(f"wrong profile coverage: missing={missing} extra={extra}")
    output = [HEADER, COMMENT, *(rows[key] for key in expected)]
    args.output.write_text("\n".join(output) + "\n", encoding="ascii")
    print(f"merged_shards={len(args.shards)} profiles={len(expected)}")


if __name__ == "__main__":
    main()
