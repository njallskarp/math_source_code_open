#!/usr/bin/env python3
"""Replay and independently check a minimum-margin witness from an aggregate."""

from __future__ import annotations

import argparse
import hashlib
import struct
from fractions import Fraction
from pathlib import Path

from audit_prefix import A, Audit, State, child_state


def parse_values(path: Path, *, stop_at_states: bool = False) -> dict[str, str]:
    values: dict[str, str] = {}
    with path.open(encoding="utf-8") as source:
        for raw_line in source:
            line = raw_line.rstrip("\n")
            if stop_at_states and line == "--states--":
                break
            if "=" in line:
                key, value = line.split("=", 1)
                values[key] = value
    return values


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_binary64(bits: str) -> float:
    return struct.unpack(">d", struct.pack(">Q", int(bits, 16)))[0]


def initial_state() -> State:
    return State(
        rest_start=1,
        odd=1,
        rest_it=2,
        mean_sum=Fraction(1),
        mean_min=Fraction(1),
        min_factor=Fraction(1),
        mean_float=1.0,
        mean_min_float=1.0,
        factor_float=1.5,
        min_factor_float=1.0,
        rest_start_float=1.0,
    )


def read_frontier_state(path: Path, wanted_index: int) -> State:
    in_states = False
    with path.open(encoding="utf-8") as source:
        for raw_line in source:
            line = raw_line.rstrip("\n")
            if line == "--states--":
                in_states = True
                continue
            if not in_states:
                continue
            fields = line.split("\t")
            index = int(fields[0])
            if index < wanted_index:
                continue
            if index != wanted_index or len(fields) != 14:
                raise ValueError(f"frontier state {wanted_index} is missing")
            odd = int(fields[2])
            return State(
                rest_start=int(fields[1]),
                odd=odd,
                rest_it=int(fields[3]),
                mean_sum=Fraction(int(fields[4]), 3**odd),
                mean_min=Fraction(int(fields[5]), int(fields[6])),
                min_factor=Fraction(int(fields[7]), int(fields[8])),
                mean_float=parse_binary64(fields[9]),
                mean_min_float=parse_binary64(fields[10]),
                factor_float=parse_binary64(fields[11]),
                min_factor_float=parse_binary64(fields[12]),
                rest_start_float=parse_binary64(fields[13]),
            )
    raise ValueError(f"frontier state {wanted_index} is missing")


def exact_correction(state: State, depth: int, convergence_bound: int) -> tuple[int, int]:
    multiplier = 0
    if state.rest_start * state.min_factor < convergence_bound:
        modulus = 1 << depth
        value = (
            Fraction(convergence_bound, 1) / state.min_factor - state.rest_start
        ) / modulus
        multiplier = -(-value.numerator // value.denominator)
    return multiplier, state.rest_start + multiplier * (1 << depth)


def reconstruct_frontier_state(
    wanted_index: int, split_depth: int, convergence_bound: int
) -> State:
    audit = Audit()
    frontier_index = 0

    def visit(state: State, nr: int, path: str) -> State | None:
        nonlocal frontier_index
        second_exact = state.rest_start + (1 << nr) <= A
        for second_branch in (False, True):
            if second_branch and not second_exact:
                continue
            child_path = path + ("1" if second_branch else "0")
            child, exact_keep, _ = child_state(
                state,
                nr,
                second_branch,
                convergence_bound,
                audit,
                child_path,
            )
            if not exact_keep:
                continue
            if nr + 1 == split_depth:
                if frontier_index == wanted_index:
                    return child
                frontier_index += 1
            else:
                found = visit(child, nr + 1, child_path)
                if found is not None:
                    return found
        return None

    result = visit(initial_state(), 1, "")
    if result is None:
        raise ValueError(f"frontier state {wanted_index} was not reconstructed")
    return result


def verify(
    aggregate_path: Path,
    frontier_path: Path,
    binary_path: Path | None,
    *,
    reconstruct_origin: bool,
) -> None:
    aggregate = parse_values(aggregate_path)
    frontier = parse_values(frontier_path, stop_at_states=True)
    if aggregate.get("format") != "collatz_cor29_aggregate_v2":
        raise ValueError("aggregate v2 is required")
    if frontier.get("format") != "collatz_cor29_frontier_v2":
        raise ValueError("frontier v2 is required")
    if sha256(frontier_path) != aggregate["frontier_sha256"]:
        raise ValueError("frontier SHA-256 does not match the aggregate")
    if binary_path is not None and sha256(binary_path) != aggregate["binary_sha256"]:
        raise ValueError("binary SHA-256 does not match the aggregate")

    origin = aggregate["minimum_margin_origin"]
    path = aggregate["minimum_margin_path"]
    if len(path) != int(aggregate["minimum_margin_path_length"]):
        raise ValueError("witness path length is inconsistent")
    if any(bit not in "01" for bit in path):
        raise ValueError("witness path is not binary")

    if origin == "root":
        state = initial_state()
        nr = 1
    else:
        state = read_frontier_state(frontier_path, int(origin))
        nr = int(frontier["split_depth"])

    convergence_bound = int(frontier["c"]) * (1 << 60)
    if origin != "root" and reconstruct_origin:
        reconstructed = reconstruct_frontier_state(
            int(origin), int(frontier["split_depth"]), convergence_bound
        )
        exact_fields = (
            "rest_start",
            "odd",
            "rest_it",
            "mean_sum",
            "mean_min",
            "min_factor",
        )
        if any(
            getattr(reconstructed, field) != getattr(state, field)
            for field in exact_fields
        ):
            raise ValueError(
                "independently reconstructed exact frontier state differs"
            )

    audit = Audit()
    for offset, bit in enumerate(path):
        second_branch = bit == "1"
        if second_branch and state.rest_start + (1 << nr) > A:
            raise ValueError(f"inadmissible second branch at depth {nr + 1}")
        child, exact_keep, _ = child_state(
            state,
            nr,
            second_branch,
            convergence_bound,
            audit,
            path[: offset + 1],
        )
        if not exact_keep and offset + 1 != len(path):
            raise ValueError(f"witness passes through a pruned state at depth {nr + 1}")
        state = child
        nr += 1

    if nr != int(aggregate["minimum_margin_depth"]):
        raise ValueError("witness depth is inconsistent")
    multiplier, corrected_start = exact_correction(state, nr, convergence_bound)
    local_mean = state.mean_min / corrected_start
    margin = abs(A * local_mean - 1)

    expected = {
        "minimum_scaled_margin": f"{margin.numerator}/{margin.denominator}",
        "minimum_margin_mean_num": str(state.mean_min.numerator),
        "minimum_margin_mean_den": str(state.mean_min.denominator),
        "minimum_margin_rest_start": str(state.rest_start),
        "minimum_margin_exact_multiplier": str(multiplier),
        "minimum_margin_corrected_start": str(corrected_start),
    }
    for field, value in expected.items():
        if aggregate.get(field) != value:
            raise ValueError(
                f"{field}={aggregate.get(field)!r}, replay produced {value!r}"
            )

    print("witness_verified=true")
    print(f"origin={origin}")
    print(f"origin_reconstructed={int(origin == 'root' or reconstruct_origin)}")
    print(f"depth={nr}")
    print(f"path={path}")
    print(f"exact_keep={int(A * local_mean >= 1)}")
    print(f"minimum_scaled_margin={margin.numerator}/{margin.denominator}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aggregate", type=Path, required=True)
    parser.add_argument("--frontier", type=Path, required=True)
    parser.add_argument("--binary", type=Path)
    parser.add_argument(
        "--skip-origin-reconstruction",
        action="store_true",
        help="trust the serialized frontier origin instead of rebuilding it in Python",
    )
    args = parser.parse_args()
    verify(
        args.aggregate,
        args.frontier,
        args.binary,
        reconstruct_origin=not args.skip_origin_reconstruction,
    )


if __name__ == "__main__":
    main()
