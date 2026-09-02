#!/usr/bin/env python3
"""Independent checks for the singular-DP excess-contraction audit.

This program does not import, execute, or read the producer's checker or
certificate.  It performs three separate checks:

1. an exact coefficient audit of the one-step potential identity;
2. exhaustive enumeration of all minimally unsatisfiable clause-sets on at
   most three variables in the tested clause-count range, including every
   singular pivot and its set-CNF collision conditions;
3. exact integer verification of the global tail arithmetic and threshold
   equivalences over the broader range 2 <= p <= 40.

It additionally reads the producer blobs directly from Git to verify their
advertised hashes and the Markdown/math-delimiter conventions of the note.
Blob integrity is source inspection, not mathematical evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import subprocess
from pathlib import Path


PRODUCER_COMMIT = "8b7abff2623c1811318b3ec7f64489fb92a974e0"
PRODUCER_FILES = {
    "ramsey_r55_symbolic_extension/singular-dp-excess-contraction-law.md":
        "5dd3736bedab026d1a757c923b3bab1ba31d5f1f748da09d8b28c325caf9f70b",
    "ramsey_r55_symbolic_extension/singular-dp-excess-contraction-certificate.json":
        "1220086a69e6fa93d07122a90a5033f551601ecf4d4bebd0ebbfefdfc3b8a5d1",
    "ramsey_r55_symbolic_extension/verify_singular_dp_excess_contraction.py":
        "de08b5ddb2849627399e4f3dc3dd2c619a32a37ea7b032560b3924a82970552a",
}


Clause = frozenset[int]
Formula = frozenset[Clause]


def variables(formula: Formula) -> frozenset[int]:
    return frozenset(abs(lit) for clause in formula for lit in clause)


def clause_satisfying_mask(clause: Clause, nvars: int) -> int:
    mask = 0
    for assignment in range(1 << nvars):
        if any(
            bool(assignment & (1 << (abs(lit) - 1))) == (lit > 0)
            for lit in clause
        ):
            mask |= 1 << assignment
    return mask


def satisfying_mask(formula: Formula, nvars: int) -> int:
    mask = (1 << (1 << nvars)) - 1
    for clause in formula:
        mask &= clause_satisfying_mask(clause, nvars)
    return mask


def is_minimally_unsatisfiable(formula: Formula, nvars: int) -> bool:
    if satisfying_mask(formula, nvars):
        return False
    return all(satisfying_mask(formula - {clause}, nvars) for clause in formula)


def all_nonempty_clauses(nvars: int) -> list[Clause]:
    clauses: list[Clause] = []
    for signs in itertools.product((-1, 0, 1), repeat=nvars):
        if all(sign == 0 for sign in signs):
            continue
        clauses.append(
            frozenset(sign * (index + 1) for index, sign in enumerate(signs) if sign)
        )
    return clauses


def oriented_singular_pivots(formula: Formula) -> list[tuple[int, Clause, list[Clause]]]:
    pivots: list[tuple[int, Clause, list[Clause]]] = []
    for var in sorted(variables(formula)):
        positive = [clause for clause in formula if var in clause]
        negative = [clause for clause in formula if -var in clause]
        if min(len(positive), len(negative)) != 1:
            continue
        # In the 1-singular case either orientation gives the same DP step;
        # choose the positive occurrence as main to count it once.
        if len(positive) == 1:
            pivots.append((var, positive[0], negative))
        else:
            pivots.append((-var, negative[0], positive))
    return pivots


def singular_dp_audit(formula: Formula, nvars: int) -> int:
    audited = 0
    for pivot_lit, main, sides in oriented_singular_pivots(formula):
        audited += 1
        pivot_var = abs(pivot_lit)
        main_tail = main - {pivot_lit}
        unaffected = frozenset(
            clause for clause in formula if pivot_var not in {abs(lit) for lit in clause}
        )
        candidates: list[Clause | None] = []
        for side in sides:
            side_tail = side - {-pivot_lit}
            extra_clashes = any(-lit in side_tail for lit in main_tail)
            candidates.append(None if extra_clashes else main_tail | side_tail)

        # Kullmann--Zhao Lemma 3(a)--(c), tested directly here.
        assert all(candidate is not None for candidate in candidates)
        resolvents = [candidate for candidate in candidates if candidate is not None]
        assert len(set(resolvents)) == len(sides)
        assert set(resolvents).isdisjoint(unaffected)

        reduced = unaffected | frozenset(resolvents)
        assert len(reduced) == len(formula) - 1
        assert variables(reduced) == variables(formula) - {pivot_var}
        assert is_minimally_unsatisfiable(reduced, nvars)
        assert len(reduced) - len(variables(reduced)) == len(formula) - nvars

        a = len(main)
        overlaps = []
        for side in sides:
            side_tail = side - {-pivot_lit}
            overlaps.append(len(main_tail & side_tail))
        sigma = sum(overlaps) - (len(sides) - 1) * (a - 2)
        phi_before = sum(len(clause) - 2 for clause in formula)
        phi_after = sum(len(clause) - 2 for clause in reduced)
        assert phi_before - phi_after == sigma
    return audited


def exhaustive_small_mu_audit(max_variables: int = 3) -> tuple[int, int]:
    mu_count = 0
    pivot_count = 0
    for nvars in range(1, max_variables + 1):
        clauses = all_nonempty_clauses(nvars)
        for clause_count in range(nvars + 1, min(nvars + 3, len(clauses)) + 1):
            for chosen in itertools.combinations(clauses, clause_count):
                formula = frozenset(chosen)
                if variables(formula) != frozenset(range(1, nvars + 1)):
                    continue
                if not is_minimally_unsatisfiable(formula, nvars):
                    continue
                mu_count += 1
                pivot_count += singular_dp_audit(formula, nvars)
    assert mu_count > 0 and pivot_count > 0
    return mu_count, pivot_count


def coefficient_identity_audit(max_fan: int = 20) -> None:
    """Compare coefficients after expanding both sides of the local law."""
    for m in range(1, max_fan + 1):
        # Coordinates are [constant, a, b_1..b_m, c_1..c_m].
        before = [-2 * (m + 1), 1] + [1] * m + [0] * m
        after = [-4 * m, m] + [1] * m + [-1] * m
        difference = [left - right for left, right in zip(before, after)]
        sigma = [2 * (m - 1), -(m - 1)] + [0] * m + [1] * m
        assert difference == sigma


def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


def global_arithmetic_audit() -> int:
    pairs = 0
    for p in range(2, 41):
        terminal_phi = p * (2 - 2) + 2 * (p - 2)
        assert terminal_phi == 2 * p - 4
        total_charge = 88 - terminal_phi
        assert total_charge == 92 - 2 * p
        tail_steps = 41 - p
        for m in range(1, 41):
            pairs += 1
            first_charge = -(m - 1) * (4 - 2)
            tail_charge = total_charge - first_charge
            assert first_charge == -2 * (m - 1)
            assert tail_charge == 90 + 2 * m - 2 * p
            assert tail_charge == 2 * tail_steps + 2 * m + 8
            lower_bound = ceil_div(tail_charge, tail_steps)
            assert lower_bound >= 3
            assert (lower_bound >= 4) == (p + 2 * m > 33)
            assert (lower_bound >= 5) == (p + m > 37)
            assert (lower_bound >= 6) == (3 * p + 2 * m > 115)

    # The concentration average needs a nonempty post-first tail.  Thus
    # p <= 40 is the logical requirement; p <= 33 is contextual to the
    # current Ramsey frontier.
    assert 41 - 40 == 1
    assert 41 - 41 == 0
    return pairs


def git_blob(repo: Path, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{PRODUCER_COMMIT}:{path}"]
    )


def strip_inline_code(line: str) -> str:
    pieces = line.split("`")
    return "".join(piece for index, piece in enumerate(pieces) if index % 2 == 0)


def source_integrity_and_markdown_audit(repo: Path) -> None:
    blobs = {path: git_blob(repo, path) for path in PRODUCER_FILES}
    for path, expected in PRODUCER_FILES.items():
        assert hashlib.sha256(blobs[path]).hexdigest() == expected

    note_path = next(path for path in PRODUCER_FILES if path.endswith(".md"))
    note = blobs[note_path].decode("utf-8")
    assert len(note) > 8_000
    assert note.startswith("# A global excess-contraction law")
    assert "## The potential and one-step identity" in note
    assert "## Scope and trust boundary" in note

    in_fence = False
    prose_lines: list[str] = []
    for line in note.splitlines():
        if line.startswith("~~~") or line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            prose_lines.append(strip_inline_code(line))
    assert not in_fence
    prose = "\n".join(prose_lines)
    assert "$" not in prose
    assert prose.count(r"\(") == prose.count(r"\)")
    assert prose.count(r"\[") == prose.count(r"\]")
    assert prose.count(r"\(") > 0 and prose.count(r"\[") > 0

    display_depth = 0
    for line in prose_lines:
        display_depth += line.count(r"\[")
        if r"\begin{" in line or r"\end{" in line:
            assert display_depth > 0
        display_depth -= line.count(r"\]")
        assert display_depth >= 0
    assert display_depth == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="path to the math_source_code_open checkout",
    )
    args = parser.parse_args()

    source_integrity_and_markdown_audit(args.repo.resolve())
    coefficient_identity_audit()
    mu_count, pivot_count = exhaustive_small_mu_audit()
    arithmetic_pairs = global_arithmetic_audit()

    print("PASS: producer blob hashes and Markdown delimiters")
    print("PASS: exact coefficient identity for fan arities 1..20")
    print(
        "PASS: exhaustive small-MU collision/potential audit "
        f"({mu_count} MU clause-sets, {pivot_count} singular pivots)"
    )
    print(
        "PASS: endpoint, tail, and threshold arithmetic "
        f"({arithmetic_pairs} pairs, 2 <= p <= 40, 1 <= m <= 40)"
    )
    print("PASS: p <= 40 is sufficient for the nonempty-tail argument")


if __name__ == "__main__":
    main()
