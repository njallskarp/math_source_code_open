#!/usr/bin/env python3
"""Generate an equisatisfiable all-pairs cell ordering and its VeriPB proof."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path


N = 43
EDGE_COUNT = N * (N - 1) // 2
TRIANGLE_COUNT = N * (N - 1) * (N - 2) // 6
VARIABLE_COUNT = EDGE_COUNT + TRIANGLE_COUNT
BASE_ROWS = 1_974_731
BASE_EQUALITIES = 128
BASE_INTERNAL_CONSTRAINTS = BASE_ROWS + BASE_EQUALITIES
BASE_SHA256 = "88aa294709836a0a707b2203da2176d420a3608353db21cc741dfa9bedf89a58"
CELLS = (
    tuple(range(0, 6)),
    tuple(range(6, 13)),
    tuple(range(14, 29)),
    tuple(range(29, 43)),
)
CELL_WEIGHTS = (4352, 4096, 16, 1)
ORDER_PAIRS = tuple(
    (left, right)
    for cell in CELLS
    for left_index, left in enumerate(cell)
    for right in cell[left_index + 1 :]
)
ORDER_ROWS = len(ORDER_PAIRS)
OUTPUT_ROWS = BASE_ROWS + ORDER_ROWS
BASE_HEADER = (
    f"* #variable= {VARIABLE_COUNT} #constraint= {BASE_ROWS} "
    f"#equal= {BASE_EQUALITIES} intsize= 64\n"
).encode("ascii")
OUTPUT_HEADER = (
    f"* #variable= {VARIABLE_COUNT} #constraint= {OUTPUT_ROWS} "
    f"#equal= {BASE_EQUALITIES} intsize= 64\n"
).encode("ascii")


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    if not 0 <= i < j < N:
        raise ValueError(f"invalid edge ({i},{j})")
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


TRIANGLE_IDS = {
    triple: EDGE_COUNT + rank
    for rank, triple in enumerate(itertools.combinations(range(N), 3), 1)
}


def key_terms(vertex: int, sign: int) -> dict[int, int]:
    terms: dict[int, int] = {}
    for cell, weight in zip(CELLS, CELL_WEIGHTS, strict=True):
        for other in cell:
            if other == vertex:
                continue
            variable = edge_id(vertex, other)
            terms[variable] = terms.get(variable, 0) + sign * weight
    return terms


def order_row(left: int, right: int) -> str:
    """Return K(right)-K(left)>=0 in canonical OPB syntax."""
    coefficients = key_terms(right, 1)
    for variable, coefficient in key_terms(left, -1).items():
        coefficients[variable] = coefficients.get(variable, 0) + coefficient
    terms = [
        (coefficient, variable)
        for variable, coefficient in sorted(coefficients.items())
        if coefficient
    ]
    return " ".join(f"{coefficient:+d} x{variable}" for coefficient, variable in terms) + " >= 0 ;"


def swap_vertex(vertex: int, left: int, right: int) -> int:
    if vertex == left:
        return right
    if vertex == right:
        return left
    return vertex


def transposition(left: int, right: int) -> list[tuple[int, int]]:
    """Nontrivial variable map induced by the vertex transposition (left right)."""
    result: list[tuple[int, int]] = []
    for i, j in itertools.combinations(range(N), 2):
        mapped = tuple(sorted((swap_vertex(i, left, right), swap_vertex(j, left, right))))
        source_id = edge_id(i, j)
        target_id = edge_id(*mapped)
        if source_id != target_id:
            result.append((source_id, target_id))
    for triple, source_id in TRIANGLE_IDS.items():
        mapped = tuple(sorted(swap_vertex(vertex, left, right) for vertex in triple))
        target_id = TRIANGLE_IDS[mapped]
        if source_id != target_id:
            result.append((source_id, target_id))
    result.sort()
    if len(result) != 2 * ((N - 2) + ((N - 2) * (N - 3) // 2)):
        raise AssertionError((left, right, len(result)))
    if sorted(target for _, target in result) != sorted(source for source, _ in result):
        raise AssertionError("substitution is not a permutation")
    return result


def write_formula(source: Path, destination: Path) -> dict[str, int | str]:
    source_hash = hashlib.sha256()
    output_hash = hashlib.sha256()
    bytes_written = 0
    lines_written = 0
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()
    try:
        with source.open("rb") as incoming, temporary.open("wb") as outgoing:
            header = incoming.readline()
            source_hash.update(header)
            if header != BASE_HEADER:
                raise ValueError("input header is not the pinned base header")
            outgoing.write(OUTPUT_HEADER)
            output_hash.update(OUTPUT_HEADER)
            bytes_written += len(OUTPUT_HEADER)
            lines_written += 1
            base_rows = 0
            for line in incoming:
                source_hash.update(line)
                outgoing.write(line)
                output_hash.update(line)
                bytes_written += len(line)
                lines_written += 1
                base_rows += 1
            if base_rows != BASE_ROWS:
                raise ValueError(f"base has {base_rows} rows, expected {BASE_ROWS}")
            if source_hash.hexdigest() != BASE_SHA256:
                raise ValueError("input SHA-256 does not match the pinned base")
            for left, right in ORDER_PAIRS:
                line = (order_row(left, right) + "\n").encode("ascii")
                outgoing.write(line)
                output_hash.update(line)
                bytes_written += len(line)
                lines_written += 1
            outgoing.flush()
            os.fsync(outgoing.fileno())
        os.replace(temporary, destination)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise
    if lines_written != OUTPUT_ROWS + 1:
        raise AssertionError(lines_written)
    return {
        "bytes": bytes_written,
        "constraints": OUTPUT_ROWS,
        "equalities": BASE_EQUALITIES,
        "lines": lines_written,
        "order_rows": ORDER_ROWS,
        "sha256": output_hash.hexdigest(),
        "variables": VARIABLE_COUNT,
    }


def write_proof(destination: Path) -> dict[str, int | str]:
    proof_hash = hashlib.sha256()
    bytes_written = 0
    lines_written = 0
    temporary = destination.with_name(destination.name + ".partial")
    if temporary.exists():
        temporary.unlink()

    def emit(raw, text: str) -> None:
        nonlocal bytes_written, lines_written
        data = (text + "\n").encode("ascii")
        raw.write(data)
        proof_hash.update(data)
        bytes_written += len(data)
        lines_written += 1

    try:
        with temporary.open("wb") as raw:
            emit(raw, "pseudo-Boolean proof version 3.0")
            emit(raw, f"f {BASE_INTERNAL_CONSTRAINTS};")
            earlier_same_pivot: dict[int, list[tuple[int, int]]] = {}
            explicit_goals = 0
            next_constraint_id = BASE_INTERNAL_CONSTRAINTS + 1
            for left, right in ORDER_PAIRS:
                witness = " ".join(
                    f"x{source} -> x{target}" for source, target in transposition(left, right)
                )
                proof_constraint = order_row(left, right).removesuffix(" ;")
                prefix = f"red {proof_constraint} : {witness}"
                earlier = earlier_same_pivot.setdefault(left, [])
                if not earlier:
                    emit(raw, prefix + ";")
                    current_constraint_id = next_constraint_id
                    next_constraint_id += 1
                else:
                    emit(raw, prefix + " : subproof")
                    # One temporary premise is allocated for the negated new
                    # row; each explicit proofgoal then allocates its negated
                    # goal and the displayed cutting-planes contradiction.
                    inversion_premise_id = next_constraint_id
                    current_constraint_id = inversion_premise_id + 1 + 2 * len(earlier)
                    next_constraint_id = current_constraint_id + 1
                    for _old_right, old_constraint_id in earlier:
                        emit(raw, f"  proofgoal {old_constraint_id}")
                        emit(
                            raw,
                            f"    pol {old_constraint_id} {inversion_premise_id} + -1 +;",
                        )
                        emit(raw, "  qed;")
                        explicit_goals += 1
                    emit(raw, "qed;")
                emit(raw, "core id -1;")
                earlier.append((right, current_constraint_id))
            emit(raw, "output EQUISATISFIABLE FILE;")
            emit(raw, "conclusion NONE;")
            emit(raw, "end pseudo-Boolean proof;")
            raw.flush()
            os.fsync(raw.fileno())
        os.replace(temporary, destination)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise
    return {
        "bytes": bytes_written,
        "explicit_cutting_planes_goals": explicit_goals,
        "lines": lines_written,
        "order_rows": ORDER_ROWS,
        "sha256": proof_hash.hexdigest(),
        "substitution_mappings_per_row": len(transposition(0, 1)),
        "veripb_format": "3.0",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    args = parser.parse_args()
    paths = [args.input.resolve(), args.output.resolve(), args.proof.resolve()]
    if len(set(paths)) != 3:
        raise ValueError("input, output, and proof paths must be distinct")
    summary = {
        "formula": write_formula(paths[0], paths[1]),
        "proof": write_proof(paths[2]),
    }
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
