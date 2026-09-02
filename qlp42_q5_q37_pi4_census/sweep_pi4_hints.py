#!/usr/bin/env python3
"""Deterministic parallel sweep of all 216 QLP-42 pi^4 cells."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import os
import random
from pathlib import Path

from solve_pi4_mq import assumptions_from_words, decode_model, encode_problem

FIELDS = (
    "q",
    "orbit",
    "case",
    "a_mask_hex",
    "b_mask_hex",
    "states_a",
    "states_b",
)


def read_rows(path: Path) -> dict[tuple[int, int, int], dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    result: dict[tuple[int, int, int], dict[str, str]] = {}
    for row in rows:
        key = tuple(int(row[field]) for field in ("q", "orbit", "case"))
        if key in result:
            raise RuntimeError(f"duplicate key in {path}: {key}")
        result[key] = {field: row[field] for field in FIELDS}
    return result


def write_rows(path: Path, rows: dict[tuple[int, int, int], dict[str, str]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows[key] for key in sorted(rows))
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def solve_job(
    job: tuple[int, int, int],
    hint: dict[str, str],
    free_cell_counts: tuple[int, ...],
    trials: int,
    time_limit: float,
    batch: int,
) -> tuple[dict[str, str] | None, int, int]:
    q_value, orbit, case_id = job
    encoding, cells, support = encode_problem(q_value, orbit, case_id)
    attempts = 0
    unknown = 0
    words = (hint["states_a"], hint["states_b"])
    for stage, free_cell_count in enumerate(free_cell_counts):
        for trial in range(trials):
            seed = (
                q_value * 10**12
                + orbit * 10**9
                + case_id * 10**6
                + batch * 10**4
                + stage * trials
                + trial
            )
            free = set(random.Random(seed).sample(range(42), free_cell_count))
            assumptions = assumptions_from_words(cells, words, free)
            satisfiable, model = encoding.solver.solve(
                assumptions=assumptions, time_limit=time_limit
            )
            attempts += 1
            unknown += satisfiable is None
            if satisfiable:
                assert model is not None
                states_a, states_b = decode_model(cells, support, model)
                values = (
                    str(q_value),
                    str(orbit),
                    str(case_id),
                    f"{support[0]:06x}",
                    f"{support[1]:06x}",
                    states_a,
                    states_b,
                )
                return dict(zip(FIELDS, values, strict=True)), attempts, unknown
    return None, attempts, unknown


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--time-limit", type=float, default=1.0)
    parser.add_argument("--trials", type=int, default=8)
    parser.add_argument("--free-cells", type=int, action="append")
    parser.add_argument("--batch", type=int, default=0)
    args = parser.parse_args()
    if args.workers < 1 or args.trials < 1 or args.time_limit <= 0:
        parser.error("workers, trials, and time-limit must be positive")
    free_cell_counts = tuple(args.free_cells or (12, 18, 24, 30, 36, 42))
    if any(count < 0 or count > 42 for count in free_cell_counts):
        parser.error("each free-cell count must lie in 0,...,42")

    hints = read_rows(args.input)
    expected = {
        (q_value, orbit, case_id)
        for q_value in (5, 37)
        for orbit in range(18)
        for case_id in range(6)
    }
    if set(hints) != expected:
        raise RuntimeError(f"input does not cover exactly 216 cells")
    rows = read_rows(args.output)
    if not set(rows) <= expected:
        raise RuntimeError("output contains an unexpected key")
    jobs = sorted(expected - set(rows))

    completed_keys: set[tuple[int, int, int]] = set()
    found = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                solve_job,
                job,
                hints[job],
                free_cell_counts,
                args.trials,
                args.time_limit,
                args.batch,
            ): job
            for job in jobs
        }
        for completed, future in enumerate(concurrent.futures.as_completed(futures), 1):
            job = futures[future]
            row, attempts, unknown = future.result()
            if job in completed_keys:
                raise RuntimeError(f"duplicate completed job: {job}")
            completed_keys.add(job)
            if row is not None:
                rows[job] = row
                found += 1
                write_rows(args.output, rows)
            print(
                f"completed={completed}/{len(jobs)};job={job};"
                f"found={int(row is not None)};attempts={attempts};"
                f"unknown={unknown};total_witnesses={len(rows)}",
                flush=True,
            )
    if completed_keys != set(jobs):
        raise RuntimeError(
            f"incomplete partition: missing={sorted(set(jobs) - completed_keys)}"
        )
    write_rows(args.output, rows)
    print(
        f"jobs={len(jobs)};completed={len(completed_keys)};found={found};"
        f"witnesses={len(rows)};missing={216-len(rows)}"
    )


if __name__ == "__main__":
    main()
