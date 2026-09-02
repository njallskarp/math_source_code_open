#!/usr/bin/env python3
"""Build, shard, merge, and independently replay the weight-4 certificate."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
from itertools import combinations
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
PRIMARY = HERE / "verify_weight4_exact_closure.cpp"
INDEPENDENT = HERE / "independent_numpy_frontier.py"
EXPECTED_STREAM_SHA256 = "d500ed89afbb5bf98c66afd93236b0f508dc447081835d3c16f461e5ddf79924"
N = 21
FULL = (1 << N) - 1


def rotate(mask: int, shift: int) -> int:
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def expected_orbits() -> set[int]:
    multiplicities: Counter[int] = Counter()
    for positions in combinations(range(N), 4):
        value = sum(1 << position for position in positions)
        representative = min(rotate(value, shift) for shift in range(N))
        multiplicities[representative] += 1
    assert len(multiplicities) == 285
    assert set(multiplicities.values()) == {21}
    assert sum(multiplicities.values()) == 5_985
    return set(multiplicities)


def parse_output(text: str) -> tuple[dict[str, str], str, dict[int, str], str]:
    before, after = text.split("stream_begin\n", 1)
    stream, tail = after.split("stream_end\n", 1)
    assert not tail
    lines = stream.splitlines()
    header = lines[0]
    records: dict[int, str] = {}
    for line in lines[1:]:
        orbit = int(line.split("\t", 1)[0], 16)
        assert orbit not in records
        records[orbit] = line
    summary = dict(line.split("=", 1) for line in before.splitlines() if "=" in line)
    assert len(records) == int(summary["b_rotation_orbits"])
    return summary, header, records, before


def run_binary(binary: Path, shard_count: int, shard_index: int) -> tuple[dict[str, str], str, dict[int, str], str]:
    environment = os.environ.copy()
    environment.setdefault("ASAN_OPTIONS", "detect_leaks=0")
    process = subprocess.run(
        [
            str(binary),
            "--stream",
            "--shard-count",
            str(shard_count),
            "--shard-index",
            str(shard_index),
        ],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    if process.stderr:
        sys.stderr.write(f"shard_{shard_index}_log_begin\n{process.stderr}shard_{shard_index}_log_end\n")
    return parse_output(process.stdout)


def assert_shard_aggregate(serial: dict[str, str], shards: list[dict[str, str]]) -> None:
    constants = (
        "b_axis_weight",
        "manifest_b_axis_words",
        "manifest_b_rotation_orbits",
        "b_exact_sum_assignments_per_orbit",
    )
    for key in constants:
        assert all(shard[key] == serial[key] for shard in shards), key

    additive = [
        "b_axis_words",
        "b_rotation_orbits",
        "b_signatures",
        "b_exact_sum_assignments_evaluated",
        "a_assignment_orbit_checks",
        "direct_paf_audits",
        "deepened_seventh_order_b_orbits",
        "deepened_signatures",
        "exact_s_b_assignments_evaluated",
        "exact_s_a_assignments_evaluated",
        "exact_hs_surviving_axis_case_orbits",
    ]
    for case_index in range(6):
        additive.extend(
            [
                f"case_{case_index}_exact_h_input_axis_orbits",
                f"case_{case_index}_exact_hs_surviving_axis_orbits",
            ]
        )
    for power in range(4, 13):
        additive.extend(
            [
                f"order_{power}_b_fingerprint_sum",
                f"order_{power}_b_orbits_with_survivors",
                f"order_{power}_surviving_axis_orbits",
                f"order_{power}_surviving_labeled_axis_pairs",
                f"order_{power}_compatible_a_assignments",
            ]
        )
    for key in additive:
        assert sum(int(shard[key]) for shard in shards) == int(serial[key]), key

    sentinel = (1 << 64) - 1
    for power in range(4, 13):
        minima = [int(shard[f"order_{power}_b_fingerprint_min"]) for shard in shards]
        minima = [value for value in minima if value != sentinel]
        maxima = [int(shard[f"order_{power}_b_fingerprint_max"]) for shard in shards]
        assert min(minima) == int(serial[f"order_{power}_b_fingerprint_min"])
        assert max(maxima) == int(serial[f"order_{power}_b_fingerprint_max"])


def canonical_stream(header: str, records: dict[int, str]) -> str:
    return header + "\n" + "\n".join(records[key] for key in sorted(records)) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workers",
        help="comma-separated deterministic regression worker counts",
    )
    parser.add_argument("--sanitizers", action="store_true")
    args = parser.parse_args()
    if args.workers:
        worker_counts = list(dict.fromkeys(int(value) for value in args.workers.split(",")))
    elif args.sanitizers:
        worker_counts = [2]
    else:
        worker_counts = list(dict.fromkeys([2, 3, min(8, os.cpu_count() or 1)]))
    assert worker_counts and all(1 <= value <= 32 for value in worker_counts)

    compiler = os.environ.get("CXX") or shutil.which("g++-16") or "clang++"
    flags = ["-std=c++20", "-O3", "-Wall", "-Wextra", "-pedantic"]
    if args.sanitizers:
        flags = [
            "-std=c++20",
            "-O1",
            "-g",
            "-fno-omit-frame-pointer",
            "-fsanitize=address,undefined",
            "-Wall",
            "-Wextra",
            "-pedantic",
        ]

    with tempfile.TemporaryDirectory(prefix="qlp42_weight4_") as temporary:
        binary = Path(temporary) / "verify_weight4_exact_closure"
        subprocess.run([compiler, *flags, str(PRIMARY), "-o", str(binary)], check=True)

        serial_start = time.perf_counter()
        serial, serial_header, serial_records, serial_text = run_binary(binary, 1, 0)
        serial_seconds = time.perf_counter() - serial_start
        assert set(serial_records) == expected_orbits()

        parallel_timings: list[tuple[int, float]] = []
        for workers in worker_counts:
            parallel_start = time.perf_counter()
            with ThreadPoolExecutor(max_workers=workers) as executor:
                shard_runs = list(
                    executor.map(
                        lambda index: run_binary(binary, workers, index),
                        range(workers),
                    )
                )
            parallel_seconds = time.perf_counter() - parallel_start
            parallel_timings.append((workers, parallel_seconds))
            shard_summaries = [run[0] for run in shard_runs]
            assert_shard_aggregate(serial, shard_summaries)
            assert all(run[1] == serial_header for run in shard_runs)

            parallel_records: dict[int, str] = {}
            for _, _, records, _ in shard_runs:
                assert parallel_records.keys().isdisjoint(records.keys())
                parallel_records.update(records)
            assert set(parallel_records) == expected_orbits()
            assert parallel_records == serial_records

        stream = canonical_stream(serial_header, serial_records)
        digest = hashlib.sha256(stream.encode("utf-8")).hexdigest()
        if EXPECTED_STREAM_SHA256:
            assert digest == EXPECTED_STREAM_SHA256

        expected = {
            "b_axis_words": "5985",
            "b_rotation_orbits": "285",
            "order_7_surviving_axis_orbits": "54",
            "order_12_surviving_axis_orbits": "42",
            "order_12_b_orbits_with_survivors": "9",
            "exact_hs_surviving_axis_case_orbits": "0",
            "full_weight4_exclusion": "verified",
        }
        for key, value in expected.items():
            assert serial[key] == value, (key, serial[key], value)

        stream_file = Path(temporary) / "canonical_orbit_stream.txt"
        stream_file.write_text(
            "stream_begin\n" + stream + "stream_end\n", encoding="utf-8"
        )
        independent = subprocess.run(
            [sys.executable, str(INDEPENDENT), "--stream", str(stream_file)],
            check=True,
            capture_output=True,
            text=True,
        )

        print(serial_text, end="")
        print(f"canonical_orbit_stream_sha256={digest}")
        print("parallel_worker_counts=" + ",".join(map(str, worker_counts)))
        print("parallel_manifest_complete=yes")
        print("parallel_matches_serial_entrywise=yes")
        print(independent.stdout, end="")
        print(f"sanitizers={'enabled' if args.sanitizers else 'disabled'}")
        print("implementations_agree=yes")
        sys.stderr.write(f"serial_wall_seconds={serial_seconds:.3f}\n")
        for workers, seconds in parallel_timings:
            sys.stderr.write(f"parallel_{workers}_wall_seconds={seconds:.3f}\n")


if __name__ == "__main__":
    main()
