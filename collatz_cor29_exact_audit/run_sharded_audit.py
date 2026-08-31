#!/usr/bin/env python3
"""Run, resume, validate, and aggregate deterministic exact-audit shards."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import os
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path


SUM_FIELDS = (
    "generated",
    "pruned_exact",
    "decision_disagreements",
    "corrected_multiplier_disagreements",
    "float_multiplier_below_exact",
    "float_multiplier_above_exact",
    "second_branch_disagreements",
)

WITNESS_FIELDS = (
    "minimum_margin_origin",
    "minimum_margin_depth",
    "minimum_margin_path_length",
    "minimum_margin_path",
    "minimum_margin_mean_num",
    "minimum_margin_mean_den",
    "minimum_margin_rest_start",
    "minimum_margin_exact_multiplier",
    "minimum_margin_corrected_start",
)


def parse_key_values(text: str, *, stop_at_states: bool = False) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if stop_at_states and line == "--states--":
            break
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as target:
            target.write(text)
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def shard_path(results_directory: Path, index: int, count: int) -> Path:
    return results_directory / f"shard_{index:06d}_of_{count:06d}.txt"


def validate_shard(
    values: dict[str, str],
    *,
    frontier_hash: str,
    binary_hash: str,
    split_depth: int,
    target_depth: int,
    c: int,
    frontier_states: int,
    shard_index: int,
    shard_count: int,
) -> None:
    expected = {
        "frontier_sha256": frontier_hash,
        "binary_sha256": binary_hash,
        "mode": "shard",
        "split_depth": str(split_depth),
        "target_depth": str(target_depth),
        "c": str(c),
        "frontier_states": str(frontier_states),
        "shard_index": str(shard_index),
        "shard_count": str(shard_count),
    }
    for key, value in expected.items():
        if values.get(key) != value:
            raise ValueError(
                f"shard {shard_index} has {key}={values.get(key)!r}, expected {value!r}"
            )
    required = set(SUM_FIELDS) | {
        "selected_states",
        "frontier",
        "maximum_multiplier_error",
        "minimum_scaled_margin",
    }
    if values.get("minimum_scaled_margin") != "none":
        required.update(WITNESS_FIELDS)
    missing = sorted(required - values.keys())
    if missing:
        raise ValueError(f"shard {shard_index} is missing fields: {missing}")


def run_one_shard(
    *,
    binary: Path,
    frontier: Path,
    frontier_hash: str,
    binary_hash: str,
    split_depth: int,
    target_depth: int,
    c: int,
    frontier_states: int,
    shard_index: int,
    shard_count: int,
    result_path: Path,
) -> tuple[int, bool]:
    if result_path.exists():
        values = parse_key_values(result_path.read_text(encoding="utf-8"))
        validate_shard(
            values,
            frontier_hash=frontier_hash,
            binary_hash=binary_hash,
            split_depth=split_depth,
            target_depth=target_depth,
            c=c,
            frontier_states=frontier_states,
            shard_index=shard_index,
            shard_count=shard_count,
        )
        return shard_index, False

    completed = subprocess.run(
        [
            str(binary),
            "--frontier-in",
            str(frontier),
            "--depth",
            str(target_depth),
            "--shard-index",
            str(shard_index),
            "--shard-count",
            str(shard_count),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    text = (
        f"frontier_sha256={frontier_hash}\n"
        f"binary_sha256={binary_hash}\n"
        f"{completed.stdout}"
    )
    values = parse_key_values(text)
    validate_shard(
        values,
        frontier_hash=frontier_hash,
        binary_hash=binary_hash,
        split_depth=split_depth,
        target_depth=target_depth,
        c=c,
        frontier_states=frontier_states,
        shard_index=shard_index,
        shard_count=shard_count,
    )
    atomic_write(result_path, text)
    return shard_index, True


def aggregate(
    frontier_values: dict[str, str],
    shard_values: list[dict[str, str]],
    *,
    frontier_hash: str,
    binary_hash: str,
    target_depth: int,
) -> str:
    split_depth = int(frontier_values["split_depth"])
    c = int(frontier_values["c"])
    frontier_states = int(frontier_values["states"])
    shard_count = len(shard_values)

    totals = {
        field: int(frontier_values[f"root_{field}"]) for field in SUM_FIELDS
    }
    final_frontier = 0
    selected_states = 0
    maximum_error = int(frontier_values["root_maximum_multiplier_error"])
    minimum_margin = Fraction(frontier_values["root_minimum_scaled_margin"])
    witness = {
        field: frontier_values[f"root_{field}"] for field in WITNESS_FIELDS
    }

    for shard_index, values in enumerate(shard_values):
        validate_shard(
            values,
            frontier_hash=frontier_hash,
            binary_hash=binary_hash,
            split_depth=split_depth,
            target_depth=target_depth,
            c=c,
            frontier_states=frontier_states,
            shard_index=shard_index,
            shard_count=shard_count,
        )
        selected_states += int(values["selected_states"])
        final_frontier += int(values["frontier"])
        for field in SUM_FIELDS:
            totals[field] += int(values[field])
        maximum_error = max(maximum_error, int(values["maximum_multiplier_error"]))
        margin_text = values["minimum_scaled_margin"]
        if margin_text != "none":
            shard_margin = Fraction(margin_text)
            if shard_margin < minimum_margin:
                minimum_margin = shard_margin
                witness = {field: values[field] for field in WITNESS_FIELDS}

    if selected_states != frontier_states:
        raise ValueError(
            f"shards cover {selected_states} states, expected {frontier_states}"
        )

    lines = [
        "format=collatz_cor29_aggregate_v2",
        f"frontier_sha256={frontier_hash}",
        f"binary_sha256={binary_hash}",
        f"split_depth={split_depth}",
        f"target_depth={target_depth}",
        f"c={c}",
        f"shard_count={shard_count}",
        f"selected_states={selected_states}",
        f"generated={totals['generated']}",
        f"pruned_exact={totals['pruned_exact']}",
        f"frontier={final_frontier}",
        f"decision_disagreements={totals['decision_disagreements']}",
        "corrected_multiplier_disagreements="
        f"{totals['corrected_multiplier_disagreements']}",
        f"float_multiplier_below_exact={totals['float_multiplier_below_exact']}",
        f"float_multiplier_above_exact={totals['float_multiplier_above_exact']}",
        f"maximum_multiplier_error={maximum_error}",
        "second_branch_disagreements="
        f"{totals['second_branch_disagreements']}",
        "minimum_scaled_margin="
        f"{minimum_margin.numerator}/{minimum_margin.denominator}",
        *(f"{field}={witness[field]}" for field in WITNESS_FIELDS),
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--frontier", type=Path, required=True)
    parser.add_argument("--depth", type=int, required=True)
    parser.add_argument("--shard-count", type=int, required=True)
    parser.add_argument("--jobs", type=int, default=max(1, os.cpu_count() or 1))
    parser.add_argument("--results-directory", type=Path, required=True)
    parser.add_argument("--aggregate-out", type=Path)
    args = parser.parse_args()

    if args.shard_count <= 0 or args.jobs <= 0:
        parser.error("shard count and jobs must be positive")
    if not args.binary.is_file() or not args.frontier.is_file():
        parser.error("binary and frontier must be existing files")

    frontier_text = args.frontier.read_text(encoding="utf-8")
    frontier_values = parse_key_values(frontier_text, stop_at_states=True)
    if frontier_values.get("format") not in {
        "collatz_cor29_frontier_v1",
        "collatz_cor29_frontier_v2",
    }:
        parser.error("unsupported frontier format")
    if frontier_values.get("format") != "collatz_cor29_frontier_v2":
        parser.error("frontier v2 is required for margin-witness aggregation")
    split_depth = int(frontier_values["split_depth"])
    c = int(frontier_values["c"])
    frontier_states = int(frontier_values["states"])
    if args.depth <= split_depth:
        parser.error("target depth must exceed split depth")
    frontier_hash = file_sha256(args.frontier)
    binary_hash = file_sha256(args.binary)

    args.results_directory.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = [
            executor.submit(
                run_one_shard,
                binary=args.binary,
                frontier=args.frontier,
                frontier_hash=frontier_hash,
                binary_hash=binary_hash,
                split_depth=split_depth,
                target_depth=args.depth,
                c=c,
                frontier_states=frontier_states,
                shard_index=index,
                shard_count=args.shard_count,
                result_path=shard_path(args.results_directory, index, args.shard_count),
            )
            for index in range(args.shard_count)
        ]
        for future in concurrent.futures.as_completed(futures):
            index, created = future.result()
            print(f"shard={index} status={'computed' if created else 'reused'}")

    shards = [
        parse_key_values(
            shard_path(args.results_directory, index, args.shard_count).read_text(
                encoding="utf-8"
            )
        )
        for index in range(args.shard_count)
    ]
    result = aggregate(
        frontier_values, shards, frontier_hash=frontier_hash,
        binary_hash=binary_hash,
        target_depth=args.depth
    )
    print(result, end="")
    if args.aggregate_out is not None:
        atomic_write(args.aggregate_out, result)


if __name__ == "__main__":
    main()
