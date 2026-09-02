#!/usr/bin/env python3
"""Deterministic parallel restart driver for the exact-checkable pi^3 witness search."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import subprocess
from pathlib import Path

FIELDS = ("q", "orbit", "case", "a_mask_hex", "b_mask_hex", "states_a", "states_b")


def existing(path: Path) -> dict[tuple[int, int, int], dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return {(int(row["q"]), int(row["orbit"]), int(row["case"])): row for row in rows}


def search(
    binary: Path,
    frontier: Path,
    job: tuple[int, int, int],
    iterations: int,
    start_restart: int,
    restarts: int,
) -> dict[str, str] | None:
    q_value, orbit, case_id = job
    for restart in range(start_restart, start_restart + restarts):
        seed = q_value * 1_000_000_000 + orbit * 1_000_000 + case_id * 10_000 + restart
        result = subprocess.run(
            [
                str(binary),
                str(frontier),
                str(q_value),
                str(orbit),
                str(case_id),
                str(iterations),
                str(seed),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            values = result.stdout.strip().split("\t")
            assert len(values) == len(FIELDS)
            return dict(zip(FIELDS, values, strict=True))
        assert result.returncode == 1
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--frontier", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=500_000)
    parser.add_argument("--start-restart", type=int, default=0)
    parser.add_argument("--restarts", type=int, default=10)
    args = parser.parse_args()

    rows = existing(args.output)
    jobs = [
        (q_value, orbit, case_id)
        for q_value in (5, 37)
        for orbit in range(18)
        for case_id in range(6)
        if (q_value, orbit, case_id) not in rows
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_jobs = {
            executor.submit(
                search,
                args.binary.resolve(),
                args.frontier.resolve(),
                job,
                args.iterations,
                args.start_restart,
                args.restarts,
            ): job
            for job in jobs
        }
        for completed, future in enumerate(
            concurrent.futures.as_completed(future_jobs), 1
        ):
            job = future_jobs[future]
            row = future.result()
            if row is not None:
                rows[job] = row
            print(
                f"completed={completed}/{len(jobs)};job={job};"
                f"found={int(row is not None)};total_witnesses={len(rows)}",
                flush=True,
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows[key] for key in sorted(rows))
    print(f"witnesses={len(rows)};missing={216-len(rows)}")


if __name__ == "__main__":
    main()
