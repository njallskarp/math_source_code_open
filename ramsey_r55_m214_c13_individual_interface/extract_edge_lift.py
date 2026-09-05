#!/usr/bin/env python3
"""Decode a feasible SCIP edge-lift solution into the compact certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_solution(path: Path) -> set[str]:
    ones: set[str] = set()
    status = None
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("solution status:"):
            status = line.split(":", 1)[1].strip()
            continue
        fields = line.split()
        if len(fields) < 2:
            continue
        try:
            value = float(fields[1])
        except ValueError:
            continue
        if abs(value - round(value)) > 1e-7 or round(value) not in (0, 1):
            raise ValueError((fields[0], value))
        if round(value) == 1:
            ones.add(fields[0])
    if status not in ("feasible solution found", "optimal solution found"):
        raise ValueError(("nonfeasible solution", status))
    return ones


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("solution", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text(encoding="ascii"))
    if set(data) != {"core_e", "footprints", "outside_e", "outside_red_edges", "pivot"}:
        raise ValueError("certificate fields")
    ones = parse_solution(args.solution)
    data["outside_red_edges"] = [
        [x, y]
        for x in range(28)
        for y in range(x + 1, 28)
        if f"e_{x:02d}_{y:02d}" in ones
    ]
    args.output.write_text(
        json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="ascii",
    )


if __name__ == "__main__":
    main()
