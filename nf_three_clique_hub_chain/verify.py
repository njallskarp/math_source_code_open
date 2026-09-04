#!/usr/bin/env python3
"""Exact all-parameter certificate for the hubbed K3--Km--K3 NF orbit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from dataclasses import dataclass

Type = tuple[int, int, int, int, int, int]
Base = tuple[int, int, int, int, int]
State = frozenset[Type]

BASES: tuple[Base, ...] = tuple(
    itertools.product((0, 1), range(3), (0, 1), (0, 1), range(3))
)


@dataclass(frozen=True, order=True)
class Affine:
    """An integer-affine expression slope*q + intercept."""

    slope: int
    intercept: int

    def at(self, q: int) -> int:
        return self.slope * q + self.intercept

    def minus_one(self) -> Affine:
        return Affine(self.slope, self.intercept - 1)


Template = dict[Base, Affine]


def leq(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return all(x <= y for x, y in zip(left, right, strict=True))


def base_of(type_: Type) -> Base:
    return type_[:3] + type_[4:]


def insert_height(base: Base, height: int) -> Type:
    return base[:3] + (height,) + base[3:]


def maximal(types: itertools.chain[Type] | list[Type] | set[Type]) -> State:
    candidates = frozenset(types)
    return frozenset(
        candidate
        for candidate in candidates
        if not any(
            candidate != other and leq(candidate, other) for other in candidates
        )
    )


def parse_template(text: str) -> Template:
    result: Template = {}
    for token in text.split():
        key, value = token.split(":", maxsplit=1)
        if len(key) != 5 or any(char not in "012" for char in key):
            raise ValueError(f"bad base key {key!r}")
        base = tuple(map(int, key))
        if base not in BASES or base in result:
            raise ValueError(f"bad or duplicate base {base}")
        if value == "q":
            expression = Affine(1, 0)
        elif value.startswith("q-"):
            expression = Affine(1, -int(value[2:]))
        else:
            expression = Affine(0, int(value))
        result[base] = expression
    return result


# A type is written as (a,i,b,j,c,k).  The table key suppresses the variable
# middle ordinary count j and writes the base z=(a,i,b,c,k).
PREFIX: tuple[Template, ...] = (
    parse_template(
        "00000:2 00002:0 00011:0 00100:1 00110:0 02000:0 10100:0 11000:0"
    ),
    parse_template("01001:1 01010:1 01101:0 10001:1 10010:1"),
    parse_template("00112:q 10112:0 12012:0 12100:q 12110:0"),
    parse_template(
        "02012:q 02102:q 02111:q 02112:q-1 11012:q 11102:q "
        "11111:q 12002:q 12011:q 12102:q-1"
    ),
    parse_template(
        "01112:q 02002:q 02011:q 02102:q-1 10112:q 11002:q "
        "11011:q 11112:q-1 12012:q-1 12101:q 12110:q 12111:q-1 "
        "12112:q-2"
    ),
    parse_template(
        "00112:q 01012:q 01102:q 01111:q 01112:q-1 02012:q-1 "
        "02101:q 02110:q 02111:q-1 02112:q-2 10012:q 10102:q "
        "10111:q 10112:q-1 11012:q-1 11101:q 11102:q-1 11110:q "
        "11111:q-1 11112:q-2 12001:q 12002:q-1 12010:q 12011:q-1 "
        "12012:q-2 12100:q 12101:q-1 12102:q-2 12110:q-1 12111:q-2 "
        "12112:q-3"
    ),
    parse_template(
        "00012:q 00102:q 00111:q 00112:q-1 01012:q-1 01101:q "
        "01110:q 01111:q-1 01112:q-2 02002:q 02011:q 02012:q-2 "
        "02100:q 02102:q-1 02110:q-1 02111:q-2 02112:q-3 10012:q-1 "
        "10101:q 10102:q-1 10110:q 10111:q-1 10112:q-2 11002:q "
        "11011:q 11012:q-2 11100:q 11101:q-1 11102:q-2 11110:q-1 "
        "11111:q-2 11112:q-3 12000:q 12001:q-1 12002:q-2 12010:q-1 "
        "12011:q-2 12012:q-3 12100:q-1 12101:q-2 12102:q-3 12110:q-2 "
        "12111:q-3 12112:q-4"
    ),
    parse_template(
        "00012:q-1 00101:q 00110:q 00111:q-1 00112:q-2 01002:q "
        "01011:q 01012:q-2 01100:q 01102:q-1 01110:q-1 01111:q-2 "
        "01112:q-3 02001:q 02002:q-1 02010:q 02011:q-1 02012:q-3 "
        "02101:q-1 02102:q-2 02110:q-2 02111:q-3 02112:q-4 10002:q "
        "10011:q 10012:q-2 10100:q 10101:q-1 10102:q-2 10110:q-1 "
        "10111:q-2 10112:q-3 11001:q 11002:q-1 11010:q 11011:q-1 "
        "11012:q-3 11100:q-1 11101:q-2 11102:q-3 11110:q-2 11111:q-3 "
        "11112:q-4 12000:q-1 12001:q-2 12002:q-3 12010:q-2 12011:q-3 "
        "12012:q-4 12100:q-2 12101:q-3 12102:q-4 12110:q-3 12111:q-4 "
        "12112:q-5"
    ),
    parse_template(
        "00002:q 00011:q 00012:q-2 00100:q 00102:q-1 00110:q-1 "
        "00111:q-2 00112:q-3 01001:q 01002:q-1 01010:q 01011:q-1 "
        "01012:q-3 01101:q-1 01102:q-2 01110:q-2 01111:q-3 01112:q-4 "
        "02000:q 02001:q-1 02002:q-2 02010:q-1 02011:q-2 02012:q-4 "
        "02100:q-1 02101:q-2 02102:q-3 02110:q-3 02111:q-4 02112:q-5 "
        "10001:q 10002:q-1 10010:q 10011:q-1 10012:q-3 10100:q-1 "
        "10101:q-2 10102:q-3 10110:q-2 10111:q-3 10112:q-4 11000:q "
        "11001:q-1 11002:q-2 11010:q-1 11011:q-2 11012:q-4 11100:q-2 "
        "11101:q-3 11102:q-4 11110:q-3 11111:q-4 11112:q-5 12000:q-2 "
        "12001:q-3 12002:q-4 12010:q-3 12011:q-4 12012:q-5 12100:q-3 "
        "12101:q-4 12102:q-5 12110:q-4 12111:q-5 12112:q-6"
    ),
)

TAIL = parse_template(
    "00000:3 00001:1 00010:1 00012:0 00100:2 00101:0 01000:1 "
    "01001:0 01010:0 01100:0 10000:1 10001:0 10010:0 12000:0"
)

# For local end type (distinguished bit, ordinary count), use index 3*a+i.
# The wave weight is minus the appropriate entry of the b=0 or b=1 matrix.
COST_BY_MIDDLE_BIT: tuple[tuple[tuple[int, ...], ...], ...] = (
    (
        (0, 2, 3, 2, 3, 5),
        (2, 3, 4, 3, 4, 6),
        (3, 4, 5, 4, 5, 7),
        (2, 3, 4, 3, 4, 6),
        (3, 4, 5, 4, 5, 7),
        (5, 6, 7, 6, 7, 8),
    ),
    (
        (1, 3, 4, 4, 5, 6),
        (3, 4, 5, 5, 6, 7),
        (4, 5, 6, 6, 7, 8),
        (4, 5, 6, 5, 6, 7),
        (5, 6, 7, 6, 7, 8),
        (6, 7, 8, 7, 8, 9),
    ),
)


def wave_weight(base: Base) -> int:
    a, i, b, c, k = base
    return -COST_BY_MIDDLE_BIT[b][3 * a + i][3 * c + k]


WEIGHT: dict[Base, int] = {base: wave_weight(base) for base in BASES}


def instantiate(template: Template, q: int) -> State:
    if q < 2:
        raise ValueError("q=m-1 must be at least 2")
    return maximal(
        [
            insert_height(base, expression.at(q))
            for base, expression in template.items()
            if 0 <= expression.at(q) <= q
        ]
    )


def wave(s: int, q: int) -> State:
    # Strict order reversal of WEIGHT (checked below on every cover) means
    # that no two surviving fibre tops can contain one another.
    return frozenset(
        insert_height(base, s + weight)
        for base, weight in WEIGHT.items()
        if 0 <= s + weight <= q
    )


def delta_types(facets: State, q: int) -> State:
    """Apply NF exactly in the S2 x S_(m-1) x S2 type quotient."""
    tops: list[Type] = []
    for base in BASES:
        thresholds = [
            facet[3]
            for facet in facets
            if leq(base_of(facet), base)
        ]
        height = min(thresholds) - 1 if thresholds else q
        if height >= 0:
            tops.append(insert_height(base, height))
    return maximal(tops)


def predicted_orbit(q: int) -> list[State]:
    if q < 2:
        raise ValueError("q=m-1 must be at least 2")
    result = [instantiate(template, q) for template in PREFIX]
    result.extend(wave(s, q) for s in range(q + 2, 3, -1))
    result.append(instantiate(TAIL, q))
    return result


def affine_leq(left: Affine, right: Affine, cutoff: int) -> bool:
    """Return left(q)<=right(q) for every integer q>=cutoff."""
    return left.slope <= right.slope and left.at(cutoff) <= right.at(cutoff)


def affine_min(expressions: list[Affine], cutoff: int) -> Affine:
    winners = [
        expression
        for expression in expressions
        if all(affine_leq(expression, other, cutoff) for other in expressions)
    ]
    if not winners:
        raise AssertionError(f"affine minimum crosses after q={cutoff}")
    return winners[0]


def normalize_affine(candidates: Template, cutoff: int) -> Template:
    valid = {
        base: expression
        for base, expression in candidates.items()
        if expression.at(cutoff) >= 0
        and expression.at(cutoff) <= cutoff
        and (expression.slope == 0 or expression.intercept <= 0)
    }
    return {
        base: expression
        for base, expression in valid.items()
        if not any(
            base != other_base
            and leq(base, other_base)
            and affine_leq(expression, other_expression, cutoff)
            for other_base, other_expression in valid.items()
        )
    }


def delta_affine(facets: Template, cutoff: int) -> Template:
    candidates: Template = {}
    for base in BASES:
        thresholds = [
            expression.minus_one()
            for facet_base, expression in facets.items()
            if leq(facet_base, base)
        ]
        candidates[base] = (
            affine_min(thresholds, cutoff) if thresholds else Affine(1, 0)
        )
    return normalize_affine(candidates, cutoff)


def verify_symbolic_prefix() -> int:
    """Prove the fixed prefix for all q>=9 by exact affine inequalities."""
    cutoff = 9
    transitions = 0
    for before, after in zip(PREFIX, PREFIX[1:], strict=False):
        if delta_affine(before, cutoff) != after:
            raise AssertionError("symbolic prefix transition mismatch")
        transitions += 1
    wave_entrance = {
        base: Affine(1, 2 + weight)
        for base, weight in WEIGHT.items()
        if weight <= -2
    }
    if delta_affine(PREFIX[-1], cutoff) != wave_entrance:
        raise AssertionError("symbolic P_8 -> A_(q+2) mismatch")
    return transitions + 1


def verify_weight_order() -> int:
    covers = 0
    maxima = (1, 2, 1, 1, 2)
    for base in BASES:
        for coordinate, maximum in enumerate(maxima):
            if base[coordinate] == maximum:
                continue
            successor = list(base)
            successor[coordinate] += 1
            successor_base = tuple(successor)
            covers += 1
            if WEIGHT[base] <= WEIGHT[successor_base]:
                raise AssertionError(
                    f"weight is not strictly order-reversing: {base}, {successor_base}"
                )
    if covers != 204:
        raise AssertionError(f"expected 204 base-poset covers, got {covers}")
    return covers


def verify_wave_regimes() -> int:
    """Check every lower/upper clipping regime for A_s -> A_(s-1)."""
    regimes = 0
    # lower=9 represents all s>=9; gap=0 represents all q-s>=0.
    for lower in (5, 6, 7, 8, 9):
        for gap in (-2, -1, 0):
            s = lower
            q = s + gap
            if delta_types(wave(s, q), q) != wave(s - 1, q):
                raise AssertionError(f"wave regime failed at s={s}, q={q}")
            regimes += 1
    return regimes


def verify_endpoints() -> int:
    checks = 0
    # A_4 and its image are q-independent once q>=4; q=2,3 are the two clips.
    for q in (2, 3, 4):
        if delta_types(wave(4, q), q) != instantiate(TAIL, q):
            raise AssertionError(f"A_4 -> T failed at q={q}")
        checks += 1
    # T -> P_0 is affine-stable for q>=3, with q=2 checked separately.
    if delta_types(instantiate(TAIL, 2), 2) != instantiate(PREFIX[0], 2):
        raise AssertionError("T -> P_0 failed at q=2")
    checks += 1
    if delta_affine(TAIL, 3) != PREFIX[0]:
        raise AssertionError("symbolic T -> P_0 failed for q>=3")
    return checks + 1


def verify_small_prefix_exceptions() -> int:
    """Cover all clips below the affine cutoff q=9."""
    checks = 0
    for q in range(2, 9):
        states = [instantiate(template, q) for template in PREFIX]
        for before, after in zip(states, states[1:], strict=False):
            if delta_types(before, q) != after:
                raise AssertionError(f"small prefix failed at q={q}")
            checks += 1
        if delta_types(states[-1], q) != wave(q + 2, q):
            raise AssertionError(f"small wave entrance failed at q={q}")
        checks += 1
    return checks


def state_record(state: State) -> list[list[int]]:
    return [list(type_) for type_ in sorted(state)]


def verify_regression(max_m: int) -> tuple[int, int, str]:
    cases = transitions = 0
    record: list[tuple[int, list[list[list[int]]]]] = []
    for m in range(3, max_m + 1):
        q = m - 1
        orbit = predicted_orbit(q)
        if len(orbit) != m + 8:
            raise AssertionError(f"m={m}: period template has wrong length")
        for step, state in enumerate(orbit):
            expected = orbit[(step + 1) % len(orbit)]
            if delta_types(state, q) != expected:
                raise AssertionError(f"m={m}, step={step}: transition mismatch")
            transitions += 1
            if step and all(sum(type_) == 2 for type_ in state):
                raise AssertionError(f"m={m}, step={step}: unexpected graph state")
        cases += 1
        record.append((m, [state_record(state) for state in orbit]))
    digest = hashlib.sha256(
        json.dumps(record, separators=(",", ":")).encode()
    ).hexdigest()
    return cases, transitions, digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=80)
    args = parser.parse_args()
    if args.max_m < 3:
        parser.error("--max-m must be at least 3")

    prefix_transitions = verify_symbolic_prefix()
    small_prefix_checks = verify_small_prefix_exceptions()
    cover_checks = verify_weight_order()
    wave_regimes = verify_wave_regimes()
    endpoint_checks = verify_endpoints()
    cases, transitions, digest = verify_regression(args.max_m)
    print(
        "VERIFIED hubbed K3--Km--K3 all-parameter NF recurrence; "
        f"m=3..{args.max_m}; cases={cases}; transitions={transitions}; "
        f"symbolic_prefix={prefix_transitions}; small_prefix={small_prefix_checks}; "
        f"weight_covers={cover_checks}; wave_regimes={wave_regimes}; "
        f"endpoints={endpoint_checks}; NF(H_m)=m+8"
    )
    print(f"ORBIT_SHA256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
