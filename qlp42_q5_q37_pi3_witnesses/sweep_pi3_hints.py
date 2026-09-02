#!/usr/bin/env python3
"""Deterministic parallel local-hint sweep for unresolved QLP-42 pi^3 cells."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import os
import random
from pathlib import Path

from solve_pi3_mq import encode_problem, state_index
from sweep_pi3_local import FIELDS, existing


def assumptions_from_hint(
    cells: list[list[list[int]]],
    hint: dict[str, str],
    free: set[int],
) -> list[int]:
    assumptions = []
    for family, field in enumerate(("states_a", "states_b")):
        word = hint[field]
        assert len(word) == 21
        for position, character in enumerate(word):
            cell = 21 * family + position
            if cell in free:
                continue
            state = int(character, 16)
            x_phase, y_phase = divmod(state, 4)
            values = (x_phase & 1, x_phase >> 1, y_phase >> 1)
            for variable, value in zip(cells[family][position], values, strict=True):
                assumptions.append(variable if value else -variable)
    return assumptions


def solve_job(
    job: tuple[int, int, int],
    hints: list[dict[str, str]],
    free_cell_counts: tuple[int, ...],
    trials: int,
    time_limit: float,
    batch: int,
) -> tuple[dict[str, str] | None, int, int]:
    q_value, orbit, case_id = job
    encoding, cells, support = encode_problem(q_value, orbit, case_id)
    attempts = 0
    unknown = 0
    for stage, free_cell_count in enumerate(free_cell_counts):
        for trial in range(trials):
            hint = hints[trial % len(hints)]
            seed = (
                q_value * 10**12
                + orbit * 10**9
                + case_id * 10**6
                + batch * 10**4
                + stage * trials
                + trial
            )
            generator = random.Random(seed)
            free = set(generator.sample(range(42), free_cell_count))
            assumptions = assumptions_from_hint(cells, hint, free)
            satisfiable, model = encoding.solver.solve(
                assumptions=assumptions, time_limit=time_limit
            )
            attempts += 1
            unknown += satisfiable is None
            if not satisfiable:
                continue
            words = []
            for family, support_mask in enumerate(support):
                word = []
                for position, bits in enumerate(cells[family]):
                    values = tuple(int(model[variable]) for variable in bits)
                    word.append(
                        state_index(values, (support_mask >> position) & 1)
                    )
                words.append(word)
            encode = lambda word: "".join(format(state, "x") for state in word)
            values = (
                str(q_value),
                str(orbit),
                str(case_id),
                f"{support[0]:06x}",
                f"{support[1]:06x}",
                encode(words[0]),
                encode(words[1]),
            )
            return dict(zip(FIELDS, values, strict=True)), attempts, unknown
    return None, attempts, unknown


def write_rows(path: Path, rows: dict[tuple[int, int, int], dict[str, str]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows[key] for key in sorted(rows))
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--time-limit", type=float, default=1.0)
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--free-cells", type=int, action="append")
    parser.add_argument("--batch", type=int, default=0)
    args = parser.parse_args()
    if args.workers < 1 or args.trials < 1 or args.time_limit <= 0:
        parser.error("workers, trials, and time-limit must be positive")
    free_cell_counts = tuple(args.free_cells or (18, 24, 30, 36))
    if any(count < 0 or count > 42 for count in free_cell_counts):
        parser.error("each free-cell count must lie in 0,...,42")

    rows = existing(args.input)
    if len(rows) != len(set(rows)):
        raise RuntimeError("duplicate input key")
    hints_by_support: dict[tuple[int, int], list[dict[str, str]]] = {}
    for key in sorted(rows):
        q_value, orbit, _ = key
        hints_by_support.setdefault((q_value, orbit), []).append(rows[key])
    expected_supports = {(q, orbit) for q in (5, 37) for orbit in range(18)}
    if set(hints_by_support) != expected_supports:
        missing = sorted(expected_supports - set(hints_by_support))
        raise RuntimeError(f"input lacks support-orbit hints: {missing}")

    jobs = [
        (q_value, orbit, case_id)
        for q_value in (5, 37)
        for orbit in range(18)
        for case_id in range(6)
        if (q_value, orbit, case_id) not in rows
    ]
    completed_keys: set[tuple[int, int, int]] = set()
    found = 0
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=args.workers
    ) as executor:
        futures = {
            executor.submit(
                solve_job,
                job,
                hints_by_support[(job[0], job[1])],
                free_cell_counts,
                args.trials,
                args.time_limit,
                args.batch,
            ): job
            for job in jobs
        }
        for completed, future in enumerate(
            concurrent.futures.as_completed(futures), 1
        ):
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
    expected_jobs = set(jobs)
    if completed_keys != expected_jobs:
        raise RuntimeError(
            f"incomplete partition: missing={sorted(expected_jobs-completed_keys)}"
        )
    write_rows(args.output, rows)
    print(
        f"jobs={len(jobs)};completed={len(completed_keys)};found={found};"
        f"witnesses={len(rows)};missing={216-len(rows)}"
    )


if __name__ == "__main__":
    main()
