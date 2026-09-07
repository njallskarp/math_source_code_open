#!/usr/bin/env python3
"""Independent audit of the zero-free affine-duplication cut exclusion.

This checker imports no module from the reviewed package.  It independently
enumerates the stabilizer orbits and admissible doubled-pair colours, checks
the physical rank/count claims, and audits every regenerated DIMACS formula
against the definition-level 23-side projection and exact threshold semantics.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path


SOURCE_COMMIT = "a960dc16a0377c12e93d1ed5afd6da92fe10b833"
EXPECTED_FILES = 20
EXPECTED_BYTES = 62125
EXPECTED_AUDIT_SHA256 = "b9576cec9cf6258b2b750ae6a2cd277d4fff89a2aea16e78ed6eb75d73585d39"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parity(value: int) -> int:
    return value.bit_count() & 1


def dot(left: int, right: int) -> int:
    return parity(left & right)


def gf2_rank(rows: list[int] | tuple[int, ...]) -> int:
    basis: dict[int, int] = {}
    for original in rows:
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return len(basis)


def linear_image(columns: tuple[int, int, int, int], vector: int) -> int:
    image = 0
    for coordinate, column in enumerate(columns):
        if vector >> coordinate & 1:
            image ^= column
    return image


def source_audit(source: Path) -> dict:
    require(source.is_dir(), "missing source directory")
    commit = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(commit == SOURCE_COMMIT, "wrong reviewed source commit")

    manifest = {}
    for line in (source / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        require(name not in manifest, "duplicate manifest name")
        data = (source / name).read_bytes()
        require(sha256(data) == digest, "source manifest mismatch: " + name)
        manifest[name] = digest
    files = sorted(path.name for path in source.iterdir() if path.is_file())
    require(len(files) == EXPECTED_FILES, "unexpected source file count")
    require(set(files) == set(manifest) | {"SHA256SUMS"}, "manifest coverage")
    total_bytes = sum((source / name).stat().st_size for name in files)
    require(total_bytes == EXPECTED_BYTES, "unexpected source byte count")
    require(sha256((source / "expected_audit.json").read_bytes()) == EXPECTED_AUDIT_SHA256,
            "published audit identity")
    return {
        "commit": commit,
        "files": len(files),
        "bytes": total_bytes,
        "manifest_entries": len(manifest),
    }


def structural_audit() -> tuple[dict, list[tuple[int, ...]]]:
    # Enumerate all 2^16 matrices, then select GL(4,2) and the e1 stabilizer.
    invertible = []
    stabilizer = []
    for word in range(1 << 16):
        columns = tuple((word >> (4 * column)) & 15 for column in range(4))
        if gf2_rank(columns) == 4:
            invertible.append(columns)
            if linear_image(columns, 1) == 1:
                stabilizer.append(columns)
    require(len(invertible) == 20160, "GL(4,2) order")
    require(len(stabilizer) == 1344, "affine-hyperplane stabilizer order")

    all_sets = list(itertools.combinations(range(1, 16), 5))
    unseen = set(all_sets)
    orbits = []
    for doubled in all_sets:
        if doubled not in unseen:
            continue
        orbit = {
            tuple(sorted(linear_image(matrix, label) for label in doubled))
            for matrix in stabilizer
        }
        require(orbit <= unseen, "stabilizer orbits overlap")
        unseen -= orbit
        orbits.append((min(orbit), len(orbit)))
    require(not unseen and len(orbits) == 16, "five-set orbit coverage")
    require(sum(size for _, size in orbits) == 3003, "orbit-size sum")
    representatives = [representative for representative, _ in orbits]

    # Solve for every dual action literally and check all nonzero contacts.
    physical_contacts = 0
    odd = set(range(1, 16, 2))
    for matrix in stabilizer:
        primal = {x: linear_image(matrix, x) for x in range(16)}
        dual = {}
        for y in range(16):
            candidates = [
                z for z in range(16)
                if all(dot(primal[1 << coordinate], z) == dot(1 << coordinate, y)
                       for coordinate in range(4))
            ]
            require(len(candidates) == 1, "dual-map uniqueness")
            dual[y] = candidates[0]
        require(set(primal.values()) == set(range(16)), "primal bijection")
        require(set(dual.values()) == set(range(16)), "dual bijection")
        require({dual[y] for y in odd} == odd, "odd affine hyperplane preservation")
        for x in range(1, 16):
            for y in range(1, 16):
                require(dot(primal[x], dual[y]) == dot(x, y), "contact transport")
                physical_contacts += 1
    require(physical_contacts == 302400, "physical contact total")

    B = list(range(1, 16)) + list(range(1, 16, 2))
    cell_sizes = Counter()
    pair_assignments = 0
    survivors = 0
    for x in range(1, 16):
        for z in range(1, 16):
            if x != z:
                size = sum(dot(x, y) == 1 and dot(z, y) == 0 for y in B)
                cell_sizes[size] += 1
                require((size <= 5) == (z == 1), "mixed-pair contact-cell criterion")
    require(cell_sizes == {4: 14, 6: 168, 8: 28}, "ordered cell-size distribution")

    for doubled in all_sets:
        retained = []
        for colours in itertools.product((0, 1), repeat=5):
            pair_assignments += 1
            colour = dict(zip(doubled, colours))
            if colour.get(1) == 1:
                continue
            if any(
                colour[x] == 1
                and colour[z] == 0
                and sum(dot(x, y) == 1 and dot(z, y) == 0 for y in B) > 5
                for x in doubled
                for z in doubled
                if x != z
            ):
                continue
            retained.append(colours)
        expected = [
            tuple(0 for _ in doubled),
            tuple(0 if label == 1 else 1 for label in doubled),
        ]
        require(retained == expected, "pair-colour branch classification")
        survivors += len(retained)
    require((pair_assignments, survivors) == (96096, 6006), "pair-colour totals")

    # Check the cut ranks and absence of zero rows/columns for every D.
    rank_profiles = Counter()
    mask23 = (1 << 23) - 1
    for doubled in all_sets:
        A = list(range(1, 16)) + list(doubled)
        red_rows = [sum(dot(x, y) << column for column, y in enumerate(B)) for x in A]
        blue_rows = [row ^ mask23 for row in red_rows]
        require(all(row not in (0, mask23) for row in red_rows), "zero cut row")
        require(all(any(dot(x, y) for x in A) and any(not dot(x, y) for x in A) for y in B),
                "zero cut column")
        profile = (gf2_rank(red_rows), gf2_rank(blue_rows))
        require(profile == (4, 5), "cut-rank profile")
        rank_profiles[profile] += 1

    physical_cross_matrices = (
        15 * math.comb(15, 5) * math.factorial(20) * math.factorial(23)
        // (2**13 * 20160)
    )
    require(physical_cross_matrices == 17154780486757774613743095705600000000,
            "physical cross-matrix count")
    orbit_reconstruction = sum(
        size * 15 * math.factorial(20) * math.factorial(23) // (2**13 * 20160)
        for _, size in orbits
    )
    require(orbit_reconstruction == physical_cross_matrices, "orbit count reconciliation")
    require(math.comb(20, 2) + math.comb(23, 2) == 443, "free internal edge count")

    return {
        "gl4_order": len(invertible),
        "stabilizer_order": len(stabilizer),
        "five_sets": len(all_sets),
        "orbits": [{"representative": list(rep), "size": size} for rep, size in orbits],
        "physical_contacts": physical_contacts,
        "ordered_cell_sizes": dict(sorted(cell_sizes.items())),
        "pair_assignments": pair_assignments,
        "surviving_pair_assignments": survivors,
        "rank_profiles": {str(key): value for key, value in sorted(rank_profiles.items())},
        "physical_cross_matrices": physical_cross_matrices,
        "free_internal_edges": 443,
    }, representatives


def parse_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    lines = path.read_text().splitlines()
    require(lines, "empty DIMACS")
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ["p", "cnf"], "DIMACS header")
    variables, declared = map(int, header[2:])
    clauses = []
    for line in lines[1:]:
        literals = tuple(map(int, line.split()))
        require(literals and literals[-1] == 0, "DIMACS clause terminator")
        clause = literals[:-1]
        require(all(1 <= abs(lit) <= variables for lit in clause), "literal domain")
        require(len(clause) == len(set(clause)), "duplicate literal")
        require(not any(-lit in clause for lit in clause), "tautological clause")
        clauses.append(clause)
    require(len(clauses) == declared, "DIMACS clause count")
    return variables, clauses


def physical_projection(doubled: tuple[int, ...], mode: int) -> tuple[set[frozenset[int]], list[int], list[int]]:
    B = list(range(1, 16)) + list(range(1, 16, 2))
    A = list(range(1, 16)) + list(doubled)
    edge_variables = {
        pair: index + 1 for index, pair in enumerate(itertools.combinations(range(23), 2))
    }
    clauses: set[frozenset[int]] = set()

    def forbid(vertices: tuple[int, ...], colour: int) -> None:
        sign = 1 if colour == 0 else -1
        clauses.add(frozenset(sign * edge_variables[pair]
                              for pair in itertools.combinations(vertices, 2)))

    for vertices in itertools.combinations(range(23), 5):
        forbid(vertices, 0)
        forbid(vertices, 1)
    for vertices in itertools.combinations(range(23), 4):
        for colour in (0, 1):
            if any(all(dot(x, B[vertex]) == colour for vertex in vertices) for x in range(1, 16)):
                forbid(vertices, colour)
    for x in doubled:
        colour = 0 if x == 1 else mode
        contacts = [vertex for vertex, y in enumerate(B) if dot(x, y) == colour]
        for vertices in itertools.combinations(contacts, 3):
            forbid(vertices, colour)

    cross_degrees = [sum(dot(x, y) for x in A) for y in B]
    return clauses, cross_degrees, B


def literal_value(literal: int, assignment: dict[int, bool]) -> bool:
    return assignment[abs(literal)] == (literal > 0)


def audit_formula(path: Path, doubled: tuple[int, ...], mode: int) -> dict:
    variables, clauses = parse_dimacs(path)
    split = next((index for index, clause in enumerate(clauses)
                  if any(abs(literal) > 253 for literal in clause)), len(clauses))
    expected, cross_degrees, _ = physical_projection(doubled, mode)
    actual_physical = [frozenset(clause) for clause in clauses[:split]]
    require(len(actual_physical) == len(set(actual_physical)), "duplicate physical clause")
    require(set(actual_physical) == expected, "physical projection mismatch")

    edge_variables = {
        pair: index + 1 for index, pair in enumerate(itertools.combinations(range(23), 2))
    }
    cursor = split
    next_variable = 253
    gates = 0
    truth_assignments = 0
    for vertex in range(23):
        lower = 18 - cross_degrees[vertex]
        upper = 24 - cross_degrees[vertex]
        require(0 < lower <= upper < 22, "degree-bound range")
        inputs = [edge_variables[tuple(sorted((other, vertex)))]
                  for other in range(23) if other != vertex]
        old: dict[int, int | bool] = {0: True}
        for prefix, edge in enumerate(inputs, 1):
            new: dict[int, int | bool] = {0: True}
            for threshold in range(1, min(prefix, upper + 1) + 1):
                next_variable += 1
                output = next_variable
                left = old.get(threshold, False)
                lower_prefix = old.get(threshold - 1, False)
                start = cursor
                while cursor < len(clauses) and max(map(abs, clauses[cursor]), default=0) == output:
                    cursor += 1
                block = clauses[start:cursor]
                require(block and all(any(abs(literal) == output for literal in clause) for clause in block),
                        "threshold gate block")
                local = sorted({abs(literal) for clause in block for literal in clause})
                expected_local = {output, edge}
                expected_local |= {value for value in (left, lower_prefix) if type(value) is int}
                require(set(local) == expected_local, "threshold gate variable scope")
                for word in itertools.product((False, True), repeat=len(local)):
                    assignment = dict(zip(local, word))
                    cnf_value = all(any(literal_value(literal, assignment) for literal in clause)
                                    for clause in block)
                    left_value = left if type(left) is bool else assignment[left]
                    lower_value = lower_prefix if type(lower_prefix) is bool else assignment[lower_prefix]
                    recurrence = bool(left_value or (assignment[edge] and lower_value))
                    require(cnf_value == (assignment[output] == recurrence),
                            "threshold recurrence semantics")
                    truth_assignments += 1
                new[threshold] = output
                gates += 1
            old = new
        require(cursor + 2 <= len(clauses), "missing degree units")
        require(clauses[cursor] == (old[lower],), "lower degree unit")
        require(clauses[cursor + 1] == (-old[upper + 1],), "upper degree unit")
        cursor += 2
    require(cursor == len(clauses), "extra formula clauses")
    require(next_variable == variables, "auxiliary variable coverage")
    return {
        "branch": None,
        "physical_clauses": len(expected),
        "variables": variables,
        "clauses": len(clauses),
        "threshold_gates": gates,
        "gate_truth_assignments": truth_assignments,
        "cnf_bytes": path.stat().st_size,
        "cnf_sha256": sha256(path.read_bytes()),
    }


def replay_audit(source: Path, replay: Path, representatives: list[tuple[int, ...]]) -> dict:
    require(replay.is_dir(), "missing replay directory")
    expected_cases = json.loads((source / "expected_cases.json").read_text())
    require(type(expected_cases) is list and len(expected_cases) == 32, "expected case count")
    expected_by_branch = {entry["branch"]: entry for entry in expected_cases}
    require(len(expected_by_branch) == 32, "duplicate expected branch")

    totals = Counter()
    proof_bytes_read = 0
    formula_results = []
    for orbit, doubled in enumerate(representatives):
        for mode in (0, 1):
            branch = f"o{orbit:02d}c{mode}"
            case = expected_by_branch[branch]
            require(tuple(case["D"]) == doubled and case["mode"] == mode, "branch metadata")
            directory = replay / "runs" / branch
            formula = directory / "input.cnf"
            proof = directory / "proof.drat"
            require(formula.is_file() and proof.is_file() and proof.stat().st_size > 0,
                    "missing physical replay evidence")
            result = audit_formula(formula, doubled, mode)
            result["branch"] = branch
            require(result["cnf_sha256"] == case["cnf_sha256"], "formula identity")
            require(result["cnf_bytes"] == case["cnf_bytes"], "formula size")
            require(result["variables"] == case["variables"], "formula variable count")
            require(result["clauses"] == case["clauses"], "formula clause count")
            proof_data = proof.read_bytes()
            proof_bytes_read += len(proof_data)
            require(sha256(proof_data) == case["proof_sha256"], "proof identity")
            require(len(proof_data) == case["proof_bytes"], "proof size")
            for key in ("physical_clauses", "threshold_gates", "gate_truth_assignments"):
                totals[key] += result[key]
            totals["formula_bytes"] += result["cnf_bytes"]
            totals["clauses"] += result["clauses"]
            formula_results.append(result)

    require(set(expected_by_branch) == {result["branch"] for result in formula_results},
            "branch coverage")
    require(totals["formula_bytes"] == 111618212, "total formula bytes")
    require(totals["clauses"] == 3149477, "total formula clauses")
    require(totals["threshold_gates"] == 161328, "total threshold gates")
    require(totals["gate_truth_assignments"] == 2370368, "gate truth-table total")
    require(proof_bytes_read == 188371117, "total proof bytes")

    replay_record = json.loads((replay / "reproduction.json").read_text())
    require(replay_record["status"] == "COMPLETE_AFFINE_DUPLICATION_FAMILY_EXCLUDED",
            "replay status")
    require(replay_record["canonical_branches"] == 32, "replay branch count")
    require(replay_record["all_proofs_physically_checked"] is True, "proof-check status")
    require(replay_record["saved_solver_statuses_trusted"] is False, "saved-status trust")
    require({entry["branch"] for entry in replay_record["proofs"]} == set(expected_by_branch),
            "proof-check branch coverage")
    for entry in replay_record["proofs"]:
        expected = expected_by_branch[entry["branch"]]
        require(entry["proof_sha256"] == expected["proof_sha256"], "checked proof hash")
        require(entry["proof_bytes"] == expected["proof_bytes"], "checked proof bytes")

    return {
        "branches": len(formula_results),
        "formula_bytes": totals["formula_bytes"],
        "clauses": totals["clauses"],
        "physical_clauses": totals["physical_clauses"],
        "threshold_gates": totals["threshold_gates"],
        "gate_truth_assignments": totals["gate_truth_assignments"],
        "proof_bytes": proof_bytes_read,
        "proofs_physically_checked_by_public_replay": 32,
        "replay_seconds": replay_record["replay_seconds"],
        "child_peak_rss_kib": replay_record["child_peak_rss_kib"],
    }


def main() -> None:
    require(len(sys.argv) == 3, "usage: independent_check.py SOURCE_DIR REPLAY_DIR")
    source = Path(sys.argv[1]).resolve()
    replay = Path(sys.argv[2]).resolve()
    source_result = source_audit(source)
    structure_result, representatives = structural_audit()
    replay_result = replay_audit(source, replay, representatives)
    evidence = {
        "status": "INDEPENDENT_AFFINE_DUPLICATION_CUT_REVIEW_ACCEPTED",
        "source": source_result,
        "structure": structure_result,
        "replay": replay_result,
        "trust": {
            "imported": ["R(4,5)<=25", "standard DRAT soundness"],
            "remaining": [
                "written reduction",
                "reviewer CPython checker",
                "pinned drat-trim C checker",
                "Docker amd64 emulation",
                "SHA-256",
                "ordinary hardware",
            ],
        },
    }
    encoded = json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()
    evidence["evidence_sha256"] = sha256(encoded)
    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    main()
