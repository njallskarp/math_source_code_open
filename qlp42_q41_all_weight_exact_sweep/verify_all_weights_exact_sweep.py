#!/usr/bin/env python3
"""Build, shard, merge, and independently replay the all-weight certificate."""

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
PRIMARY = HERE / "verify_all_weights_exact_sweep.cpp"
INDEPENDENT = HERE / "independent_numpy_frontier.py"
EXPECTED_STREAM_SHA256 = "294a1448ee1ca8b5051985a3771027d97432311215f7f13bd09c027fe3434c42"
N = 21
FULL = (1 << N) - 1
WEIGHTS = (0, 4, 8, 12, 16, 20)
EXPECTED_WORDS = {0: 1, 4: 5_985, 8: 203_490, 12: 293_930, 16: 20_349, 20: 21}
EXPECTED_ORBITS = {0: 1, 4: 285, 8: 9_690, 12: 14_000, 16: 969, 20: 1}
SENTINEL = (1 << 64) - 1


def rotate(mask: int, shift: int) -> int:
    shift %= N
    if shift == 0:
        return mask & FULL
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def expected_orbits() -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    for weight in WEIGHTS:
        multiplicities: Counter[int] = Counter()
        for positions in combinations(range(N), weight):
            value = sum(1 << position for position in positions)
            representative = min(rotate(value, shift) for shift in range(N))
            multiplicities[representative] += 1
        assert len(multiplicities) == EXPECTED_ORBITS[weight]
        assert sum(multiplicities.values()) == EXPECTED_WORDS[weight]
        if weight == 12:
            assert Counter(multiplicities.values()) == Counter({21: 13_995, 7: 5})
        else:
            expected_size = 1 if weight == 0 else 21
            assert set(multiplicities.values()) == {expected_size}
        result.update({(weight, orbit): size for orbit, size in multiplicities.items()})
    assert len(result) == 24_946
    return result


def parse_output(
    output: str,
) -> tuple[dict[str, str], str, dict[tuple[int, int], str]]:
    before, after = output.split("stream_begin\n", 1)
    stream, tail = after.split("stream_end\n", 1)
    assert not tail
    lines = stream.splitlines()
    header = lines[0]
    columns = header.split("\t")
    records: dict[tuple[int, int], str] = {}
    for line in lines[1:]:
        fields = dict(zip(columns, line.split("\t"), strict=True))
        key = (int(fields["weight"]), int(fields["b_axis"], 16))
        assert key not in records
        records[key] = line
    summary = dict(line.split("=", 1) for line in before.splitlines() if "=" in line)
    return summary, header, records


def run_binary(
    binary: Path, shard_count: int, shard_index: int
) -> tuple[dict[str, str], str, dict[tuple[int, int], str]]:
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
        sys.stderr.write(
            f"shard_{shard_index}_of_{shard_count}_log_begin\n"
            f"{process.stderr}"
            f"shard_{shard_index}_of_{shard_count}_log_end\n"
        )
    return parse_output(process.stdout)


def is_constant(key: str) -> bool:
    return (
        key in {"weights", "manifest_b_axis_words", "manifest_b_rotation_orbits", "manifest_signatures"}
        or "_manifest_b_axis_words" in key
        or "_manifest_b_rotation_orbits" in key
        or key.endswith("_admissible_cases")
        or key.endswith("_b_exact_sum_assignments_per_orbit")
    )


def aggregate_summaries(shards: list[dict[str, str]]) -> dict[str, str]:
    assert shards
    keys = set(shards[0])
    assert all(set(shard) == keys for shard in shards)
    result: dict[str, str] = {}
    ignored_suffixes = ("_first_empty_order", "_exclusion")
    ignored = {"shard_count", "shard_index", "q41_all_weight_exclusion"}
    for key in sorted(keys):
        values = [shard[key] for shard in shards]
        if key in ignored or key.endswith(ignored_suffixes):
            continue
        if is_constant(key):
            assert len(set(values)) == 1, key
            result[key] = values[0]
        elif key.endswith("_b_fingerprint_min"):
            numeric = [int(value) for value in values if int(value) != SENTINEL]
            result[key] = str(min(numeric) if numeric else SENTINEL)
        elif key.endswith("_b_fingerprint_max"):
            result[key] = str(max(map(int, values)))
        else:
            result[key] = str(sum(map(int, values)))

    global_survivors = 0
    for weight in WEIGHTS:
        first_empty = 0
        for power in range(4, 13):
            if int(result[f"weight_{weight}_order_{power}_surviving_axis_orbits"]) == 0:
                first_empty = power
                break
        result[f"weight_{weight}_first_empty_order"] = str(first_empty)
        survivors = int(result[f"weight_{weight}_exact_hs_surviving_axis_case_orbits"])
        result[f"weight_{weight}_exclusion"] = "verified" if survivors == 0 else "not_obtained"
        global_survivors += survivors
    result["all_weight_exact_hs_surviving_axis_case_orbits"] = str(global_survivors)
    result["q41_all_weight_exclusion"] = "verified" if global_survivors == 0 else "not_obtained"
    return result


def run_sweep(
    binary: Path, workers: int
) -> tuple[dict[str, str], str, dict[tuple[int, int], str], float]:
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        runs = list(
            executor.map(
                lambda index: run_binary(binary, workers, index),
                range(workers),
            )
        )
    elapsed = time.perf_counter() - started
    headers = {run[1] for run in runs}
    assert len(headers) == 1
    records: dict[tuple[int, int], str] = {}
    for _, _, shard_records in runs:
        assert records.keys().isdisjoint(shard_records)
        records.update(shard_records)
    return aggregate_summaries([run[0] for run in runs]), headers.pop(), records, elapsed


def canonical_stream(header: str, records: dict[tuple[int, int], str]) -> str:
    return header + "\n" + "\n".join(records[key] for key in sorted(records)) + "\n"


def check_manifest(
    records: dict[tuple[int, int], str], expected: dict[tuple[int, int], int], header: str
) -> None:
    assert set(records) == set(expected)
    columns = header.split("\t")
    for key, line in records.items():
        fields = dict(zip(columns, line.split("\t"), strict=True))
        assert int(fields["weight"]) == key[0]
        assert int(fields["b_axis"], 16) == key[1]
        assert int(fields["orbit_size"]) == expected[key]


def regression_checks(summary: dict[str, str]) -> None:
    assert summary["processed_signatures"] == "512"
    assert summary["a_tables_built"] == "512"
    assert sum(int(summary[f"weight_{weight}_b_exact_sum_assignments_evaluated"]) for weight in WEIGHTS) == 2_960_716_672
    for weight in WEIGHTS:
        assert int(summary[f"weight_{weight}_b_axis_words"]) == EXPECTED_WORDS[weight]
        assert int(summary[f"weight_{weight}_b_rotation_orbits"]) == EXPECTED_ORBITS[weight]

    known = {
        "weight_4_order_7_surviving_axis_orbits": "54",
        "weight_4_order_12_surviving_axis_orbits": "42",
        "weight_4_order_12_b_orbits_with_survivors": "9",
        "weight_4_exact_hs_surviving_axis_case_orbits": "0",
        "weight_16_order_7_surviving_axis_orbits": "36",
        "weight_16_order_12_surviving_axis_orbits": "24",
        "weight_16_order_12_b_orbits_with_survivors": "12",
        "weight_16_exact_hs_surviving_axis_case_orbits": "0",
        "weight_20_order_7_surviving_axis_orbits": "0",
        "weight_20_exact_hs_surviving_axis_case_orbits": "0",
    }
    for key, value in known.items():
        assert summary[key] == value, (key, summary[key], value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workers",
        default="8,3",
        help="comma-separated production and replay worker counts",
    )
    parser.add_argument("--sanitizers", action="store_true")
    parser.add_argument("--skip-independent", action="store_true")
    args = parser.parse_args()
    worker_counts = list(dict.fromkeys(int(value) for value in args.workers.split(",")))
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

    expected = expected_orbits()
    with tempfile.TemporaryDirectory(prefix="qlp42_all_weight_") as temporary:
        binary = Path(temporary) / "verify_all_weights_exact_sweep"
        subprocess.run([compiler, *flags, str(PRIMARY), "-o", str(binary)], check=True)

        baseline_summary: dict[str, str] | None = None
        baseline_header = ""
        baseline_records: dict[tuple[int, int], str] = {}
        timings: list[tuple[int, float]] = []
        for workers in worker_counts:
            summary, header, records, elapsed = run_sweep(binary, workers)
            timings.append((workers, elapsed))
            check_manifest(records, expected, header)
            regression_checks(summary)
            if baseline_summary is None:
                baseline_summary = summary
                baseline_header = header
                baseline_records = records
            else:
                assert summary == baseline_summary
                assert header == baseline_header
                assert records == baseline_records

        assert baseline_summary is not None
        stream = canonical_stream(baseline_header, baseline_records)
        digest = hashlib.sha256(stream.encode("utf-8")).hexdigest()
        if EXPECTED_STREAM_SHA256:
            assert digest == EXPECTED_STREAM_SHA256

        independent_output = "independent_verifier=skipped\n"
        if not args.skip_independent:
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
            independent_output = independent.stdout

        for key in sorted(baseline_summary):
            print(f"{key}={baseline_summary[key]}")
        print(f"canonical_orbit_stream_sha256={digest}")
        print("parallel_worker_counts=" + ",".join(map(str, worker_counts)))
        print("parallel_manifest_complete=yes")
        print(
            "parallel_matches_entrywise="
            + ("yes" if len(worker_counts) > 1 else "single_partition_in_this_run")
        )
        print(independent_output, end="")
        print(f"sanitizers={'enabled' if args.sanitizers else 'disabled'}")
        print("implementations_agree=yes" if not args.skip_independent else "implementations_agree=not_checked")
        for workers, elapsed in timings:
            sys.stderr.write(f"parallel_{workers}_wall_seconds={elapsed:.3f}\n")


if __name__ == "__main__":
    main()
