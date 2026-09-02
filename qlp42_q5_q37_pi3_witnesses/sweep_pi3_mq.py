#!/usr/bin/env python3
"""Parallel bounded MQ/SAT sweep for exact-checkable QLP-42 pi^3 witnesses."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
from pathlib import Path

from solve_pi3_mq import encode_problem, state_index
from sweep_pi3_local import FIELDS, existing


def solve_job(job: tuple[int, int, int], time_limit: float) -> tuple[str, dict[str, str] | None]:
    q_value, orbit, case_id = job
    encoding, cells, support = encode_problem(q_value, orbit, case_id)
    satisfiable, model = encoding.solver.solve(time_limit=time_limit)
    if satisfiable is None:
        return "unknown", None
    if not satisfiable:
        return "unsat", None
    words = []
    for family, support_mask in enumerate(support):
        word = []
        for position, bits in enumerate(cells[family]):
            values = tuple(int(model[variable]) for variable in bits)
            word.append(state_index(values, (support_mask >> position) & 1))
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
    return "sat", dict(zip(FIELDS, values, strict=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--time-limit", type=float, default=5.0)
    parser.add_argument("--uncovered-only", action="store_true")
    args = parser.parse_args()
    rows = existing(args.output)
    covered = {(int(row["q"]), int(row["orbit"])) for row in rows.values()}
    jobs = [
        (q_value, orbit, case_id)
        for q_value in (5, 37)
        for orbit in range(18)
        for case_id in range(6)
        if (q_value, orbit, case_id) not in rows
        and (not args.uncovered_only or (q_value, orbit) not in covered)
    ]
    status_counts = {"sat": 0, "unsat": 0, "unknown": 0}
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(solve_job, job, args.time_limit): job for job in jobs}
        for completed, future in enumerate(concurrent.futures.as_completed(futures), 1):
            job = futures[future]
            status, row = future.result()
            status_counts[status] += 1
            if row is not None:
                rows[job] = row
            print(
                f"completed={completed}/{len(jobs)};job={job};status={status};"
                f"total_witnesses={len(rows)}",
                flush=True,
            )
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows[key] for key in sorted(rows))
    print(f"witnesses={len(rows)};missing={216-len(rows)};statuses={status_counts}")


if __name__ == "__main__":
    main()
