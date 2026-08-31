#!/usr/bin/env python3
"""Exact-vs-binary64 prefix audit of Hercher's Corollary 29 search.

This mirrors the residue-tree state transitions in the official
``collatz_cycle.cpp`` while carrying a second, exact rational state.  It is a
prefix auditor, not a reproduction of the original depth-300 computation.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache


A = 4_370_000_000_000_000_000_000
DEFAULT_C = 1536


@lru_cache(maxsize=None)
def correction_factor_exact(odd: int, rest: int, last_step_odd: bool) -> Fraction:
    residue = rest % 729
    candidates = [Fraction(1)]
    if odd >= 1 and not last_step_odd and residue % 3 == 2:
        candidates.append(
            Fraction(2, 3)
            * correction_factor_exact(odd - 1, rest // 3 * 2 + 1, False)
        )
    if odd >= 2 and residue % 9 == 4:
        candidates.append(
            Fraction(8, 9)
            * correction_factor_exact(odd - 2, rest // 9 * 8 + 3, False)
        )
    if odd >= 4 and residue % 81 == 10:
        candidates.append(
            Fraction(64, 81)
            * correction_factor_exact(odd - 4, rest // 81 * 64 + 7, False)
        )
    if odd >= 5 and residue % 243 == 182:
        candidates.append(
            Fraction(128, 243)
            * correction_factor_exact(odd - 5, rest // 243 * 128 + 95, False)
        )
    sixth_predecessors = {
        91: 63,
        410: 287,
        433: 303,
        524: 367,
        587: 411,
        604: 423,
        661: 463,
        695: 487,
    }
    if odd >= 6 and residue in sixth_predecessors:
        candidates.append(
            Fraction(512, 729)
            * correction_factor_exact(
                odd - 6,
                rest // 729 * 512 + sixth_predecessors[residue],
                False,
            )
        )
    return min(candidates)


@lru_cache(maxsize=None)
def correction_factor_float(odd: int, rest: int, last_step_odd: bool) -> float:
    residue = rest % 729
    candidates = [1.0]
    if odd >= 1 and not last_step_odd and residue % 3 == 2:
        candidates.append(
            (2.0 / 3.0)
            * correction_factor_float(odd - 1, rest // 3 * 2 + 1, False)
        )
    if odd >= 2 and residue % 9 == 4:
        candidates.append(
            (8.0 / 9.0)
            * correction_factor_float(odd - 2, rest // 9 * 8 + 3, False)
        )
    if odd >= 4 and residue % 81 == 10:
        candidates.append(
            (64.0 / 81.0)
            * correction_factor_float(odd - 4, rest // 81 * 64 + 7, False)
        )
    if odd >= 5 and residue % 243 == 182:
        candidates.append(
            (128.0 / 243.0)
            * correction_factor_float(odd - 5, rest // 243 * 128 + 95, False)
        )
    sixth_predecessors = {
        91: 63,
        410: 287,
        433: 303,
        524: 367,
        587: 411,
        604: 423,
        661: 463,
        695: 487,
    }
    if odd >= 6 and residue in sixth_predecessors:
        candidates.append(
            (512.0 / 729.0)
            * correction_factor_float(
                odd - 6,
                rest // 729 * 512 + sixth_predecessors[residue],
                False,
            )
        )
    return min(candidates)


@dataclass(frozen=True)
class State:
    rest_start: int
    odd: int
    rest_it: int
    mean_sum: Fraction
    mean_min: Fraction
    min_factor: Fraction
    mean_float: float
    mean_min_float: float
    factor_float: float
    min_factor_float: float
    rest_start_float: float


@dataclass
class Audit:
    generated: int = 0
    pruned_exact: int = 0
    frontier: int = 0
    decision_disagreements: int = 0
    corrected_multiplier_disagreements: int = 0
    float_multiplier_below_exact: int = 0
    float_multiplier_above_exact: int = 0
    maximum_multiplier_error: int = 0
    second_branch_disagreements: int = 0
    minimum_scaled_margin: Fraction | None = None

    def record_margin(self, local_mean: Fraction) -> None:
        margin = abs(A * local_mean - 1)
        if self.minimum_scaled_margin is None or margin < self.minimum_scaled_margin:
            self.minimum_scaled_margin = margin


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def child_state(
    state: State,
    nr: int,
    second_branch: bool,
    convergence_bound: int,
    audit: Audit,
) -> tuple[State, bool, bool]:
    rest_start = state.rest_start + ((1 << nr) if second_branch else 0)
    rest_start_float = state.rest_start_float + (float(1 << nr) if second_branch else 0.0)
    rest_it = state.rest_it + ((3**state.odd) if second_branch else 0)

    if (rest_it & 1) == 0:
        odd = state.odd
        rest_it //= 2
        mean_sum = state.mean_sum
        mean_min = state.mean_min
        mean_float = state.mean_float
        mean_min_float = state.mean_min_float
        factor_float = state.factor_float * 0.5
        last_step_odd = False
    else:
        odd = state.odd + 1
        rest_it = rest_it + rest_it // 2 + 1
        reciprocal_factor = Fraction(1 << nr, 3**state.odd)
        mean_sum = state.mean_sum + reciprocal_factor
        current_mean = mean_sum / odd
        mean_min = min(state.mean_min, current_mean)
        mean_float = (
            state.mean_float * state.odd + 1.0 / state.factor_float
        ) / odd
        mean_min_float = min(state.mean_min_float, mean_float)
        factor_float = state.factor_float * 1.5
        last_step_odd = True

    exact_factor = Fraction(3**odd, 1 << (nr + 1))
    min_factor = min(
        state.min_factor,
        exact_factor * correction_factor_exact(odd, rest_it, last_step_odd),
    )
    min_factor_float = min(
        state.min_factor_float,
        factor_float * correction_factor_float(odd, rest_it, last_step_odd),
    )

    exact_corrected_start = rest_start
    exact_multiplier = 0
    if Fraction(rest_start) * min_factor < convergence_bound:
        modulus = 1 << (nr + 1)
        exact_multiplier = ceil_fraction(
            (Fraction(convergence_bound, 1) / min_factor - rest_start) / modulus
        )
        exact_corrected_start += exact_multiplier * modulus

    float_corrected_start = rest_start_float
    float_multiplier = 0
    bound_float = float(convergence_bound)
    if rest_start_float * min_factor_float < bound_float:
        float_multiplier = math.ceil(
            (bound_float / min_factor_float - rest_start_float) / float(1 << (nr + 1))
        )
        float_corrected_start += float_multiplier * float(1 << (nr + 1))

    if exact_multiplier != float_multiplier:
        audit.corrected_multiplier_disagreements += 1
        if float_multiplier < exact_multiplier:
            audit.float_multiplier_below_exact += 1
        else:
            audit.float_multiplier_above_exact += 1
        audit.maximum_multiplier_error = max(
            audit.maximum_multiplier_error, abs(float_multiplier - exact_multiplier)
        )

    local_mean = mean_min / exact_corrected_start
    local_mean_float = mean_min_float / float_corrected_start
    exact_keep = A * local_mean >= 1
    float_keep = local_mean_float >= 1.0 / float(A)
    if exact_keep != float_keep:
        audit.decision_disagreements += 1
    audit.record_margin(local_mean)

    return (
        State(
            rest_start=rest_start,
            odd=odd,
            rest_it=rest_it,
            mean_sum=mean_sum,
            mean_min=mean_min,
            min_factor=min_factor,
            mean_float=mean_float,
            mean_min_float=mean_min_float,
            factor_float=factor_float,
            min_factor_float=min_factor_float,
            rest_start_float=rest_start_float,
        ),
        exact_keep,
        float_keep,
    )


def audit_prefix(depth: int, c: int = DEFAULT_C) -> Audit:
    if not 2 <= depth <= 72:
        raise ValueError("depth must lie between 2 and 72")
    convergence_bound = c * (1 << 60)
    audit = Audit()
    start = State(
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

    def visit(state: State, nr: int) -> None:
        second_exact = state.rest_start + (1 << nr) <= A
        second_float = state.rest_start_float + float(1 << nr) <= 1.0 / (1.0 / float(A))
        if second_exact != second_float:
            audit.second_branch_disagreements += 1

        for second_branch in (False, True):
            if second_branch and not second_exact:
                continue
            audit.generated += 1
            child, exact_keep, _ = child_state(
                state, nr, second_branch, convergence_bound, audit
            )
            if not exact_keep:
                audit.pruned_exact += 1
            elif nr + 1 == depth:
                audit.frontier += 1
            else:
                visit(child, nr + 1)

    visit(start, 1)
    return audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=20)
    parser.add_argument("--c", type=int, default=DEFAULT_C)
    args = parser.parse_args()
    audit = audit_prefix(args.depth, args.c)
    print(f"depth={args.depth}")
    print(f"c={args.c}")
    print(f"generated={audit.generated}")
    print(f"pruned_exact={audit.pruned_exact}")
    print(f"frontier={audit.frontier}")
    print(f"decision_disagreements={audit.decision_disagreements}")
    print(
        "corrected_multiplier_disagreements="
        f"{audit.corrected_multiplier_disagreements}"
    )
    print(f"float_multiplier_below_exact={audit.float_multiplier_below_exact}")
    print(f"float_multiplier_above_exact={audit.float_multiplier_above_exact}")
    print(f"maximum_multiplier_error={audit.maximum_multiplier_error}")
    print(f"second_branch_disagreements={audit.second_branch_disagreements}")
    assert audit.minimum_scaled_margin is not None
    print(
        "minimum_scaled_margin="
        f"{audit.minimum_scaled_margin.numerator}/{audit.minimum_scaled_margin.denominator}"
    )


if __name__ == "__main__":
    main()
