#!/usr/bin/env python3
"""Streaming deterministic unrestricted-CNF sweep for all QLP-42 pi^4 cells."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from sweep_pi4_hints import read_rows, write_rows


def job_key(job: tuple[int, int, int]) -> str:
    return "/".join(map(str, job))


def read_evidence(path: Path) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    records = document.get("records")
    if not isinstance(records, dict):
        raise RuntimeError("evidence file has no records object")
    return records


def write_evidence(path: Path, records: dict[str, dict[str, object]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    document = {"format": 1, "records": {key: records[key] for key in sorted(records)}}
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(document, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def solve_job(
    job: tuple[int, int, int], cadical: str, time_limit: int
) -> tuple[dict[str, str] | None, dict[str, object]]:
    q_value, orbit, case_id = job
    directory = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix=f"qlp42-pi4-{q_value}-{orbit}-{case_id}-") as raw:
        temporary = Path(raw)
        cnf = temporary / "cell.cnf"
        metadata = temporary / "cell.json"
        export = subprocess.run(
            [
                sys.executable,
                str(directory / "export_pi4_cnf.py"),
                str(q_value),
                str(orbit),
                str(case_id),
                "--cnf",
                str(cnf),
                "--metadata",
                str(metadata),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        details = json.loads(metadata.read_text(encoding="utf-8"))
        started = time.monotonic()
        solved = subprocess.run(
            [cadical, "-t", str(time_limit), str(cnf)],
            check=False,
            capture_output=True,
            text=True,
        )
        wall_seconds = time.monotonic() - started
        statuses = [
            line[2:]
            for line in solved.stdout.splitlines()
            if line.startswith("s ")
        ]
        record: dict[str, object] = {
            "q": q_value,
            "orbit": orbit,
            "case": case_id,
            "solver_exit_code": solved.returncode,
            "solver_status_lines": statuses,
            "solver_wall_seconds": round(wall_seconds, 6),
            "time_limit_seconds": time_limit,
            "cnf_sha256": details["cnf_sha256"],
            "cnf_variables": details["cnf_variables"],
            "cnf_clauses": details["cnf_clauses"],
            "export_summary": export.stdout.strip(),
        }
        if solved.returncode == 10 and statuses == ["SATISFIABLE"]:
            solver_output = temporary / "solver.out"
            solver_output.write_text(solved.stdout, encoding="utf-8", newline="\n")
            decoded = subprocess.run(
                [
                    sys.executable,
                    str(directory / "decode_pi4_cadical.py"),
                    "--metadata",
                    str(metadata),
                    "--solver-output",
                    str(solver_output),
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            fields = decoded.split("\t")
            if len(fields) != 7:
                raise RuntimeError(f"decoder returned malformed row: {decoded!r}")
            names = (
                "q", "orbit", "case", "a_mask_hex", "b_mask_hex",
                "states_a", "states_b",
            )
            row = dict(zip(names, fields, strict=True))
            if (int(row["q"]), int(row["orbit"]), int(row["case"])) != job:
                raise RuntimeError("decoded row key does not match scheduled job")
            record["status"] = "SAT"
            return row, record
        if solved.returncode == 20 and statuses == ["UNSATISFIABLE"]:
            record["status"] = "UNSAT_UNVERIFIED"
            return None, record
        record["status"] = "UNKNOWN"
        return None, record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence-output", type=Path, required=True)
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--time-limit", type=int, default=60)
    args = parser.parse_args()
    if args.workers < 1 or args.time_limit < 1:
        parser.error("workers and time-limit must be positive")
    if not args.cadical.is_file() or not os.access(args.cadical, os.X_OK):
        parser.error("--cadical must name an executable file")

    rows = read_rows(args.input)
    expected = {
        (q_value, orbit, case_id)
        for q_value in (5, 37)
        for orbit in range(18)
        for case_id in range(6)
    }
    if not set(rows) <= expected:
        raise RuntimeError("input contains an unexpected key")
    output_rows = read_rows(args.output)
    if output_rows and not set(rows) <= set(output_rows):
        raise RuntimeError("resumed output omits an input witness")
    if output_rows:
        rows = output_rows
    records = read_evidence(args.evidence_output)
    record_jobs = {tuple(map(int, key.split("/"))) for key in records}
    if not record_jobs <= expected:
        raise RuntimeError("evidence contains an unexpected key")
    jobs = sorted(expected - set(rows) - record_jobs)
    scheduled = set(jobs)
    completed: set[tuple[int, int, int]] = set()

    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(solve_job, job, str(args.cadical), args.time_limit): job
            for job in jobs
        }
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            job = futures[future]
            row, record = future.result()
            if job in completed:
                raise RuntimeError(f"duplicate completed job: {job}")
            completed.add(job)
            if row is not None:
                rows[job] = row
                write_rows(args.output, rows)
            records[job_key(job)] = record
            write_evidence(args.evidence_output, records)
            print(
                f"completed={count}/{len(jobs)};job={job};"
                f"status={record['status']};wall={record['solver_wall_seconds']};"
                f"witnesses={len(rows)}",
                flush=True,
            )
    if completed != scheduled:
        raise RuntimeError(f"incomplete scheduled partition: {sorted(scheduled-completed)}")
    write_rows(args.output, rows)
    statuses: dict[str, int] = {}
    for record in records.values():
        status = str(record["status"])
        statuses[status] = statuses.get(status, 0) + 1
    print(
        f"scheduled={len(jobs)};completed={len(completed)};"
        f"witnesses={len(rows)};statuses={json.dumps(statuses,sort_keys=True)}"
    )


if __name__ == "__main__":
    main()
