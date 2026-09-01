#!/usr/bin/env python3
"""Dependency-free exact verifier for the 74-clause signed-K4 MUS."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pathlib


DATA_SHA256 = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"
ORDER = 42


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_graph6_independently(record: bytes) -> list[set[int]]:
    if not record or record[0] - 63 != ORDER:
        raise ValueError("invalid order-42 graph6 record")
    payload: list[int] = []
    for byte in record[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        payload.extend((value >> shift) & 1 for shift in (5, 4, 3, 2, 1, 0))
    needed = ORDER * (ORDER - 1) // 2
    if len(payload) < needed:
        raise ValueError("truncated graph6 payload")
    adjacency = [set() for _ in range(ORDER)]
    position = 0
    for right in range(1, ORDER):
        for left in range(right):
            if payload[position]:
                adjacency[left].add(right)
                adjacency[right].add(left)
            position += 1
    return adjacency


def enumerate_signed_clauses(adjacency: list[set[int]]):
    result = []
    for vertices in itertools.combinations(range(ORDER), 4):
        edge_count = sum(right in adjacency[left] for left, right in itertools.combinations(vertices, 2))
        if edge_count == 6:
            result.append(("red", vertices, tuple(-(v + 1) for v in vertices)))
        elif edge_count == 0:
            result.append(("blue", vertices, tuple(v + 1 for v in vertices)))
    return result


def clause_satisfied(clause: tuple[int, ...], assignment: str) -> bool:
    return any((literal > 0) == (assignment[abs(literal) - 1] == "1") for literal in clause)


def assign_literal(values: dict[int, bool], literal: int) -> bool:
    variable = abs(literal)
    value = literal > 0
    previous = values.get(variable)
    if previous is not None and previous != value:
        return False
    values[variable] = value
    return True


def unit_conflict(clauses: list[tuple[int, ...]], assumptions: list[int]) -> bool:
    values: dict[int, bool] = {}
    for literal in assumptions:
        if not assign_literal(values, literal):
            return True
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            if any(values.get(abs(lit)) == (lit > 0) for lit in clause):
                continue
            unassigned = [lit for lit in clause if abs(lit) not in values]
            if not unassigned:
                return True
            if len(unassigned) == 1:
                if not assign_literal(values, unassigned[0]):
                    return True
                changed = True
    return False


def parse_proof_clause(line: str) -> tuple[bool, tuple[int, ...]]:
    fields = line.split()
    deletion = bool(fields and fields[0] == "d")
    if deletion:
        fields = fields[1:]
    if not fields or fields[-1] != "0":
        raise ValueError(f"malformed DRUP line: {line!r}")
    literals = tuple(int(field) for field in fields[:-1])
    if any(literal == 0 or abs(literal) > ORDER for literal in literals):
        raise ValueError("proof literal outside 1..42")
    return deletion, literals


def check_drup(base: list[tuple[int, ...]], proof: list[str]) -> int:
    clauses = list(base)
    saw_empty = False
    additions = 0
    for line in proof:
        deletion, clause = parse_proof_clause(line)
        if deletion:
            try:
                clauses.remove(clause)
            except ValueError as error:
                raise ValueError("DRUP deletes a missing clause") from error
            continue
        if not unit_conflict(clauses, [-literal for literal in clause]):
            raise ValueError(f"non-RUP proof addition: {line}")
        clauses.append(clause)
        additions += 1
        saw_empty |= not clause
    if not saw_empty:
        raise ValueError("DRUP proof does not derive the empty clause")
    return additions


def verify(data_path: pathlib.Path, certificate_path: pathlib.Path) -> dict[str, object]:
    if sha256(data_path) != DATA_SHA256:
        raise ValueError("authoritative graph6 file SHA-256 mismatch")
    records = data_path.read_bytes().splitlines()
    certificate = json.loads(certificate_path.read_text())
    source = certificate["source"]
    if source["sha256"] != DATA_SHA256 or source["record_count"] != len(records):
        raise ValueError("certificate source manifest mismatch")
    graph_index = source["graph_index"]
    record = records[graph_index]
    if hashlib.sha256(record).hexdigest() != source["graph6_record_sha256"]:
        raise ValueError("graph6 record hash mismatch")

    full = enumerate_signed_clauses(decode_graph6_independently(record))
    manifest = certificate["full_system"]
    red_count = sum(color == "red" for color, _vertices, _clause in full)
    blue_count = len(full) - red_count
    if (len(full), red_count, blue_count) != (
        manifest["clause_count"], manifest["red_clause_count"], manifest["blue_clause_count"]
    ):
        raise ValueError("full signed-K4 system counts mismatch")

    core_records = certificate["core"]["clauses"]
    core: list[tuple[int, ...]] = []
    covered: set[int] = set()
    colors: list[str] = []
    for expected_core_index, item in enumerate(core_records):
        if item["core_index"] != expected_core_index:
            raise ValueError("noncanonical core ordering")
        full_index = item["full_clause_index"]
        color, vertices, clause = full[full_index]
        if item["color"] != color or item["vertices_zero_based"] != list(vertices):
            raise ValueError("core K4 classification mismatch")
        if item["dimacs_clause"] != list(clause):
            raise ValueError("core DIMACS clause mismatch")
        core.append(clause)
        covered.update(vertices)
        colors.append(color)

    core_manifest = certificate["core"]
    if (len(core), colors.count("red"), colors.count("blue"), len(covered)) != (
        core_manifest["clause_count"], core_manifest["red_clause_count"],
        core_manifest["blue_clause_count"], core_manifest["covered_vertex_count"],
    ):
        raise ValueError("core summary mismatch")

    proof_additions = check_drup(core, certificate["drup_proof"])

    witnesses = certificate["deletion_witnesses"]
    if len(witnesses) != len(core):
        raise ValueError("one deletion witness per core clause is required")
    assignments: set[str] = set()
    for expected_removed, witness in enumerate(witnesses):
        if witness["removed_core_index"] != expected_removed:
            raise ValueError("deletion witnesses are out of order")
        assignment = witness["assignment"]
        if len(assignment) != ORDER or set(assignment) - {"0", "1"}:
            raise ValueError("invalid deletion witness bit string")
        for clause_index, clause in enumerate(core):
            satisfied = clause_satisfied(clause, assignment)
            if clause_index == expected_removed:
                if satisfied:
                    raise ValueError("deletion witness also satisfies the removed clause")
            elif not satisfied:
                raise ValueError("deletion witness violates a retained clause")
        assignments.add(assignment)
    if len(assignments) != len(core):
        raise ValueError("deletion witnesses are not distinct")

    return {
        "verified": True,
        "arithmetic": "exact Boolean logic",
        "full_clause_count": len(full),
        "core_clause_count": len(core),
        "red_core_clauses": colors.count("red"),
        "blue_core_clauses": colors.count("blue"),
        "covered_vertices": len(covered),
        "drup_additions": proof_additions,
        "deletion_witnesses": len(witnesses),
        "conclusion": "the core is unsatisfiable and subset-minimal",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6", type=pathlib.Path)
    parser.add_argument("certificate", type=pathlib.Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.graph6, args.certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
