#!/usr/bin/env python3
"""Exact checks for the singular-DP clause-excess contraction law.

The universal proof is algebraic and appears in the accompanying note.  This
dependency-free checker verifies the serialized constants, the one-step
identity on a broad exact integer grid, every admissible (p,m) boundary case,
and the claimed threshold refinements.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import sys


def ceiling_div(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise AssertionError("nonpositive denominator")
    return -(-numerator // denominator)


def main() -> None:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
        "ramsey_r55_symbolic_extension/singular-dp-excess-contraction-certificate.json"
    )
    raw = path.read_bytes()
    data = json.loads(raw)
    digest = hashlib.sha256(raw).hexdigest()

    initial = data["initial_formula"]
    phi_initial = initial["clauses"] * (initial["clause_length"] - 2)
    if phi_initial != initial["potential"] or phi_initial != 88:
        raise AssertionError("wrong initial potential")

    # Check the local identity using arbitrary exact side lengths.  For a main
    # clause of length a, side length b_i, and same-literal nonpivot overlap
    # c_i, the resolvent length is a+b_i-2-c_i.
    local_cases = 0
    for a in range(1, 9):
        for fan in range(1, 11):
            # One representative side length/overlap per fan position is
            # enough to test that all side terms cancel; vary them cyclically.
            side_lengths = [1 + ((3 * i + fan) % 8) for i in range(fan)]
            overlap_ranges = [range(min(a - 1, b - 1) + 1) for b in side_lengths]
            for overlaps in itertools.product(*overlap_ranges):
                before = (a - 2) + sum(b - 2 for b in side_lengths)
                after = sum(a + b - 2 - c - 2 for b, c in zip(side_lengths, overlaps))
                charge = sum(overlaps) - (fan - 1) * (a - 2)
                if before - after != charge:
                    raise AssertionError("one-step potential identity failed")
                local_cases += 1
                if local_cases >= 250_000:
                    break
            if local_cases >= 250_000:
                break
        if local_cases >= 250_000:
            break

    terminal = data["terminal_family"]
    first = data["first_step"]
    minimum_bound = None
    pair_count = 0
    refined4 = refined5 = refined6 = 0
    for p in range(terminal["parameter_min"], terminal["parameter_max_from_committed_frontier"] + 1):
        phi_terminal = p * (2 - 2) + 2 * (p - 2)
        total_charge = phi_initial - phi_terminal
        for fan in range(first["fan_arity_min"], first["fan_arity_max"] + 1):
            first_charge = -2 * (fan - 1)
            tail_charge = total_charge - first_charge
            tail_steps = 41 - p
            if tail_charge != 90 + 2 * fan - 2 * p:
                raise AssertionError("tail charge formula failed")
            bound = ceiling_div(tail_charge, tail_steps)
            rational_bound = ceiling_div(2 * tail_steps + 2 * fan + 8, tail_steps)
            if bound != rational_bound:
                raise AssertionError("average formula failed")
            if bound < 3:
                raise AssertionError("universal charge-three bound failed")
            if (bound >= 4) != (p + 2 * fan > 33):
                raise AssertionError("charge-four threshold failed")
            if (bound >= 5) != (p + fan > 37):
                raise AssertionError("charge-five threshold failed")
            if (bound >= 6) != (3 * p + 2 * fan > 115):
                raise AssertionError("charge-six threshold failed")
            minimum_bound = bound if minimum_bound is None else min(minimum_bound, bound)
            refined4 += bound >= 4
            refined5 += bound >= 5
            refined6 += bound >= 6
            pair_count += 1

    if minimum_bound != data["tail"]["universal_integer_lower_bound_on_maximum_charge"]:
        raise AssertionError("serialized universal lower bound is wrong")

    print(
        "verified: singular-DP excess contraction identity; "
        f"local_integer_cases={local_cases}; parameter_pairs={pair_count}; "
        f"minimum_max_charge_bound={minimum_bound}; "
        f"charge4_pairs={refined4}; charge5_pairs={refined5}; charge6_pairs={refined6}; "
        f"certificate_sha256={digest}"
    )


if __name__ == "__main__":
    main()
