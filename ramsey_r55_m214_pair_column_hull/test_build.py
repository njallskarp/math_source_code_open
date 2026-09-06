#!/usr/bin/env python3
"""Small exact tests for the pair-column convex-hull generator."""

from __future__ import annotations

import tempfile
from fractions import Fraction
from pathlib import Path

import build
import derive_fractional_certificate as fractional
import verify_fractional


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rejected(callable_object) -> None:
    try:
        callable_object()
    except (ValueError, IndexError, KeyError):
        return
    raise AssertionError("malformed input accepted")


def main() -> None:
    check(len(build.ROOT_KEYS) == 389, "roots")
    check([sum(key[1] == c for key in build.ROOT_KEYS) for c in range(9, 14)] == [78, 78, 78, 78, 77], "root census")
    check(len(build.MISSED_KEYS) == 10_612, "missed support")
    check(build.SUFFIX_ROWS == 13_078, "suffix rows")
    check([build.ROWS_BY_C[c] for c in range(9, 14)] == [45, 40, 33, 24, 26], "row profile")

    states = 0
    active_equalities = 0
    for common in range(9, 14):
        pair_count = (41 - common) * (40 - common) // 2
        for exceptional in (False, True):
            shift, lower, upper, tangents = build.hull_parameters(common, exceptional)
            check(lower == (14 if exceptional else 13), "lower endpoint")
            check(upper == shift + 4, "upper endpoint")
            for a in range(common):
                for total in (0, pair_count):
                    for tangent in tangents:
                        rhs_active = tangent * shift - tangent * (tangent + 1) // 2
                        guard = rhs_active + tangent * (common - 1)
                        check(total - tangent * a >= -tangent * (common - 1), "inactive lower guard")
                        states += 1
                    slope_twice = lower + upper - 1
                    rhs_active = lower * upper - slope_twice * shift
                    guard = rhs_active + 2 * pair_count
                    check(-2 * total + slope_twice * a >= -2 * pair_count, "inactive upper guard")
                    check(guard == rhs_active + 2 * pair_count, "upper guard arithmetic")
                    states += 1
            for a in range(common - 9, 5):
                b = shift + a
                total = b * (b - 1) // 2
                lower_slacks = []
                for tangent in tangents:
                    rhs = tangent * shift - tangent * (tangent + 1) // 2
                    slack = total - tangent * a - rhs
                    check(slack >= 0, "active lower facet")
                    lower_slacks.append(slack)
                check(min(lower_slacks) == 0, "lower envelope not exact")
                slope_twice = lower + upper - 1
                rhs = lower * upper - slope_twice * shift
                check(-2 * total + slope_twice * a >= rhs, "active upper chord")
                active_equalities += 1

    check(build.ROOT_KEYS[48] == ("E8", 13, 0, "A"), "witness root")
    check(len(fractional.orbit_table()) == 171, "triangle orbits")
    verify_fractional.check_edge_certificate(Path("edge_parameters.tsv"))
    verify_fractional.parse_certificate(Path("triangle_orbits.tsv"))

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        edge_raw = Path("edge_parameters.tsv").read_text(encoding="ascii")
        orbit_raw = Path("triangle_orbits.tsv").read_text(encoding="ascii")
        bad_edge = root / "bad_edge.tsv"
        bad_edge.write_text(edge_raw.replace("pA\t5/6", "pA\t4/6", 1), encoding="ascii")
        rejected(lambda: verify_fractional.check_edge_certificate(bad_edge))
        bad_orbit = root / "bad_orbit.tsv"
        bad_orbit.write_text(orbit_raw.replace("\t0\t", "\t2\t", 1), encoding="ascii")
        rejected(lambda: verify_fractional.parse_certificate(bad_orbit))
        truncated = root / "truncated.tsv"
        truncated.write_text("\n".join(orbit_raw.splitlines()[:-1]) + "\n", encoding="ascii")
        rejected(lambda: verify_fractional.parse_certificate(truncated))

    check(Fraction(6) < Fraction(78), "strict witness separation")
    print(
        f"PASS guard_states={states} active_integer_points={active_equalities} "
        "malformed_controls=3 strict_gap=72"
    )


if __name__ == "__main__":
    main()
