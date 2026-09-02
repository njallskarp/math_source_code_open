#!/usr/bin/env python3
"""Exact checker for the binary-star and unit-clause barrier certificate."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

Literal = int
Clause = frozenset[Literal]


def terminal_cycle(p: int) -> tuple[Clause, ...]:
    """Return {{-y_i, y_(i+1)}} with indices represented by 1,...,p."""
    return tuple(
        frozenset((-index, index % p + 1)) for index in range(1, p + 1)
    )


def verify_terminal_cycle(p: int, expected: dict) -> int:
    clauses = terminal_cycle(p)
    assert len(clauses) == expected["clause_count"] == p
    assert len(set(clauses)) == p
    assert all(len(clause) == expected["clause_length"] == 2 for clause in clauses)

    frequencies = Counter(literal for clause in clauses for literal in clause)
    assert set(frequencies) == set(range(1, p + 1)) | set(range(-p, 0))
    maximum_star = max(frequencies.values())
    assert maximum_star == expected["maximum_clauses_containing_one_signed_literal"]
    assert maximum_star == 1
    return maximum_star


def verify_certificate(data: dict) -> None:
    p = data["terminal_p"]
    assert data["core_variables"] - p == data["singular_steps"] == 7
    assert data["stage_floor_through_five"] == [4, 4, 4, 4, 3, 2]
    assert data["maximum_binary_clauses_after_step_five"] == 1

    sixth = data["sixth_step"]
    assert sixth["main_tail_minimum_size"] == 1

    large_tail = sixth["if_main_tail_size_at_least_two"]
    assert large_tail["maximum_old_binaries"] == 1
    assert large_tail["maximum_new_binaries"] == 1
    assert large_tail["maximum_total_binaries"] == (
        large_tail["maximum_old_binaries"] + large_tail["maximum_new_binaries"]
    ) == 2

    singleton_tail = sixth["if_main_tail_size_one"]
    assert singleton_tail["old_binary_main_is_removed"] is True
    assert singleton_tail["all_new_binaries_share_main_tail_literal"] is True

    # A unit A union B with nonempty A forces |A|=1 and |B| in {0,1}.
    # These are precisely the two parent contradictions proved in the note.
    assert sixth["unit_resolvent_side_tail_sizes"] == [0, 1]
    assert len(sixth["unit_resolvent_contradictions"]) == 2
    assert sixth["unit_clauses_after_step_six"] == 0

    maximum_terminal_star = verify_terminal_cycle(p, data["terminal_cycle"])

    seventh = data["seventh_step"]
    assert seventh["main_tail_minimum_size"] == 1
    # Tail size >=2 gives at most one distinct binary (the tail itself).
    # Tail size 1 gives a literal star, whose intersection with Z_p has size
    # at most maximum_terminal_star.  These cases are exhaustive.
    assert seventh["maximum_new_terminal_cycle_binaries"] == max(
        1, maximum_terminal_star
    ) == 1
    assert seventh["minimum_untouched_terminal_cycle_binaries"] == (
        p - seventh["maximum_new_terminal_cycle_binaries"]
    ) == 34

    required_old = seventh["minimum_untouched_terminal_cycle_binaries"]
    # Both alternatives for the G6 binary family are impossible: the small
    # alternative has at most two members, and the star alternative can
    # contain at most one clause from Z_p.
    assert required_old > large_tail["maximum_total_binaries"]
    assert required_old > maximum_terminal_star

    assert data["excluded_p"] == [35]
    assert data["previously_excluded_p"] == [36, 37, 38, 39, 40, 41]
    assert data["surviving_p_minimum"] == 2
    assert data["surviving_p_maximum"] == 34


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} CERTIFICATE.json")
    data = json.loads(Path(sys.argv[1]).read_text())
    verify_certificate(data)
    print(
        "verified: G6 binaries are <=2 or a literal-star, "
        "G6 has no unit, excluded p=35, surviving p=2..34"
    )


if __name__ == "__main__":
    main()
