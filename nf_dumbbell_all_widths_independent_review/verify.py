#!/usr/bin/env python3
"""Exact symbolic and definition-level checks for the NF orbit of B_(5,m)."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections.abc import Iterable
from dataclasses import dataclass

Type = tuple[int, int, int, int]
TypeAntichain = frozenset[Type]
Base = tuple[int, int, int]


@dataclass(frozen=True, order=True)
class QAffine:
    """The integer-affine expression slope*q + intercept."""

    slope: int
    intercept: int

    def at(self, q: int) -> int:
        return self.slope * q + self.intercept

    def minus_one(self) -> QAffine:
        return QAffine(self.slope, self.intercept - 1)


def const(value: int) -> QAffine:
    return QAffine(0, value)


def qminus(value: int) -> QAffine:
    return QAffine(1, -value)


WEIGHT: dict[Base, int] = {
    (0, 0, 0): 4,
    (0, 0, 1): 3,
    (0, 1, 0): 2,
    (0, 1, 1): 1,
    (0, 2, 0): 1,
    (0, 2, 1): 0,
    (0, 3, 0): 0,
    (0, 3, 1): -1,
    (0, 4, 0): -1,
    (0, 4, 1): -2,
    (1, 0, 0): 2,
    (1, 0, 1): 0,
    (1, 1, 0): 1,
    (1, 1, 1): -1,
    (1, 2, 0): 0,
    (1, 2, 1): -2,
    (1, 3, 0): -1,
    (1, 3, 1): -3,
    (1, 4, 0): -3,
    (1, 4, 1): -4,
}


def state(**entries: QAffine) -> dict[Base, QAffine]:
    """Build a symbolic state from keys such as b031 (base 031)."""
    result: dict[Base, QAffine] = {}
    for key, value in entries.items():
        if len(key) != 4 or key[0] != "b":
            raise ValueError(f"bad symbolic base {key}")
        base = tuple(map(int, key[1:]))
        if base in result:
            raise ValueError(f"duplicate symbolic base {base}")
        result[base] = value
    return result


PREFIX: tuple[dict[Base, QAffine], ...] = (
    state(b000=const(2), b001=const(1), b020=const(0), b101=const(0), b110=const(0)),
    state(b010=const(1), b011=const(0), b100=const(1)),
    state(b001=qminus(0), b101=const(0), b140=const(0)),
    state(b040=qminus(0), b041=qminus(1), b130=qminus(0)),
    state(b031=qminus(0), b121=qminus(0), b131=qminus(1), b140=qminus(1), b141=qminus(2)),
    state(
        b021=qminus(0), b040=qminus(0), b041=qminus(1), b111=qminus(0),
        b121=qminus(1), b130=qminus(0), b131=qminus(2), b140=qminus(2),
        b141=qminus(3),
    ),
    state(
        b011=qminus(0), b030=qminus(0), b031=qminus(1), b040=qminus(1),
        b041=qminus(2), b101=qminus(0), b111=qminus(1), b120=qminus(0),
        b121=qminus(2), b130=qminus(1), b131=qminus(3), b140=qminus(3),
        b141=qminus(4),
    ),
    state(
        b001=qminus(0), b020=qminus(0), b021=qminus(1), b030=qminus(1),
        b031=qminus(2), b040=qminus(2), b041=qminus(3), b101=qminus(1),
        b110=qminus(0), b111=qminus(2), b120=qminus(1), b121=qminus(3),
        b130=qminus(2), b131=qminus(4), b140=qminus(4), b141=qminus(5),
    ),
    state(
        b010=qminus(0), b011=qminus(1), b020=qminus(1), b021=qminus(2),
        b030=qminus(2), b031=qminus(3), b040=qminus(3), b041=qminus(4),
        b100=qminus(0), b101=qminus(2), b110=qminus(1), b111=qminus(3),
        b120=qminus(2), b121=qminus(4), b130=qminus(3), b131=qminus(5),
        b140=qminus(5), b141=qminus(6),
    ),
    state(
        b001=qminus(0), b010=qminus(1), b011=qminus(2), b020=qminus(2),
        b021=qminus(3), b030=qminus(3), b031=qminus(4), b040=qminus(4),
        b041=qminus(5), b100=qminus(1), b101=qminus(3), b110=qminus(2),
        b111=qminus(4), b120=qminus(3), b121=qminus(5), b130=qminus(4),
        b131=qminus(6), b140=qminus(6), b141=qminus(7),
    ),
)


U = state(
    b000=const(5), b001=const(4), b010=const(3), b011=const(2),
    b020=const(2), b021=const(1), b030=const(1), b031=const(0),
    b100=const(3), b101=const(1), b110=const(2), b111=const(0),
    b120=const(1), b140=const(0),
)

V = state(
    b000=const(4), b001=const(3), b010=const(2), b011=const(1),
    b020=const(1), b021=const(0), b040=const(0), b100=const(2),
    b101=const(0), b110=const(1), b130=const(0),
)

T = state(
    b000=const(3), b001=const(2), b010=const(1), b011=const(0),
    b030=const(0), b100=const(1), b120=const(0),
)

U1 = state(
    b011=const(1), b030=const(1), b031=const(0), b101=const(1),
    b111=const(0), b120=const(1), b140=const(0),
)

V1 = state(
    b001=const(1), b020=const(1), b021=const(0), b040=const(0),
    b101=const(0), b110=const(1), b130=const(0),
)

U2 = state(
    b001=const(2), b020=const(2), b021=const(1), b030=const(1),
    b031=const(0), b101=const(1), b110=const(2), b111=const(0),
    b120=const(1), b140=const(0),
)


def leq(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return all(x <= y for x, y in zip(left, right, strict=True))


def maximal(types: Iterable[Type]) -> TypeAntichain:
    candidates = frozenset(types)
    return frozenset(
        candidate
        for candidate in candidates
        if not any(candidate != other and leq(candidate, other) for other in candidates)
    )


def all_types(m: int) -> Iterable[Type]:
    if m < 2:
        raise ValueError("m must be at least 2")
    return itertools.product((0, 1), range(5), (0, 1), range(m))


def delta_types(facets: TypeAntichain, m: int) -> TypeAntichain:
    """Apply delta_NF exactly in the S_4 x S_(m-1) type quotient."""
    fibre_tops: list[Type] = []
    for x0, x_count, y0 in itertools.product((0, 1), range(5), (0, 1)):
        base = (x0, x_count, y0)
        thresholds = [
            facet[3]
            for facet in facets
            if all(facet[index] <= base[index] for index in range(3))
        ]
        height = min(thresholds) - 1 if thresholds else m - 1
        if height >= 0:
            fibre_tops.append((*base, height))
    return maximal(fibre_tops)


def instantiate(formula: dict[Base, QAffine], q: int) -> TypeAntichain:
    """Clip an affine formula to [0,q] and restore maximality."""
    return maximal(
        (*base, expression.at(q))
        for base, expression in formula.items()
        if 0 <= expression.at(q) <= q
    )


def prefix_types(m: int) -> list[TypeAntichain]:
    q = m - 1
    return [instantiate(formula, q) for formula in PREFIX]


def wave_formula(offset: int) -> dict[Base, QAffine]:
    """Formula for A_(q-offset)."""
    return {base: QAffine(1, weight - offset) for base, weight in WEIGHT.items()}


def wave_types(s: int, m: int) -> TypeAntichain:
    q = m - 1
    return maximal(
        (*base, s + weight)
        for base, weight in WEIGHT.items()
        if 0 <= s + weight <= q
    )


def predicted_orbit(m: int) -> list[TypeAntichain]:
    if m < 2:
        raise ValueError("m must be at least 2")
    q = m - 1
    prefix = prefix_types(m)
    if q == 1:
        return prefix[:6] + [instantiate(U1, q), instantiate(V1, q), instantiate(T, q)]
    if q == 2:
        return prefix[:7] + [instantiate(U2, q), instantiate(V, q), instantiate(T, q)]
    if q == 3:
        return prefix[:8] + [instantiate(U, q), instantiate(V, q), instantiate(T, q)]
    if q == 4:
        return prefix[:9] + [instantiate(U, q), instantiate(V, q), instantiate(T, q)]
    result = prefix
    if q >= 6:
        result.extend(wave_types(s, m) for s in range(q - 4, 1, -1))
    result.extend((instantiate(U, q), instantiate(V, q), instantiate(T, q)))
    return result


def eventually_le(left: QAffine, right: QAffine, cutoff: int) -> bool:
    slope = left.slope - right.slope
    value = left.at(cutoff) - right.at(cutoff)
    return slope <= 0 and value <= 0


def normalize_affine(
    candidates: dict[Base, QAffine], cutoff: int
) -> dict[Base, QAffine]:
    """Keep nonnegative eventual fibre tops maximal for every q>=cutoff."""
    if any(expression.slope not in (0, 1) for expression in candidates.values()):
        raise AssertionError("certificate only supports slopes zero and one")
    nonnegative = {
        base: expression
        for base, expression in candidates.items()
        if expression.slope >= 0 and expression.at(cutoff) >= 0
    }
    if any(expression.at(cutoff) > cutoff for expression in nonnegative.values()):
        raise AssertionError("symbolic height exceeds q at the cutoff")
    result: dict[Base, QAffine] = {}
    for base, expression in nonnegative.items():
        dominated = any(
            base != other_base
            and leq(base, other_base)
            and eventually_le(expression, other_expression, cutoff)
            for other_base, other_expression in nonnegative.items()
        )
        if not dominated:
            result[base] = expression
    return result


def delta_affine(
    facets: dict[Base, QAffine], cutoff: int
) -> dict[Base, QAffine]:
    """Apply the fibre-height operator in eventual affine arithmetic."""
    candidates: dict[Base, QAffine] = {}
    for base in WEIGHT:
        thresholds = [
            expression
            for facet_base, expression in facets.items()
            if leq(facet_base, base)
        ]
        if not thresholds:
            candidates[base] = qminus(0)
            continue
        minima = [
            expression
            for expression in thresholds
            if all(eventually_le(expression, other, cutoff) for other in thresholds)
        ]
        if not minima:
            raise AssertionError(f"no eventual minimum over base {base}")
        if len(set(minima)) != 1:
            raise AssertionError(f"nonunique affine minimum over base {base}: {minima}")
        candidates[base] = minima[0].minus_one()
    return normalize_affine(candidates, cutoff)


def affine_cutoff() -> int:
    """Choose a point beyond every possible ordering crossing in the certificate."""
    formulas = list(PREFIX) + [wave_formula(4), U, V, T]
    expressions = [qminus(0)] + [value for formula in formulas for value in formula.values()]
    intercept_span = max(
        abs(left.intercept - right.intercept)
        for left, right in itertools.product(expressions, repeat=2)
    )
    return max(7, intercept_span + 2)


def verify_symbolic_certificate() -> tuple[int, int, int]:
    """Verify the finite eventual-affine proof and generic wave identity."""
    cutoff = affine_cutoff()
    transitions = list(zip(PREFIX[:-1], PREFIX[1:], strict=True))
    transitions.append((PREFIX[-1], wave_formula(4)))
    a3 = {base: const(3 + weight) for base, weight in WEIGHT.items() if 3 + weight >= 0}
    a2 = {base: const(2 + weight) for base, weight in WEIGHT.items() if 2 + weight >= 0}
    transitions.extend(((a3, a2), (a2, U), (U, V), (V, T), (T, PREFIX[0])))
    for index, (left, right) in enumerate(transitions):
        actual = delta_affine(normalize_affine(left, cutoff), cutoff)
        expected = normalize_affine(right, cutoff)
        if actual != expected:
            raise AssertionError(f"symbolic transition {index} failed: {actual} != {expected}")

    comparable_checks = 0
    minimum_checks = 0
    for left, right in itertools.permutations(WEIGHT, 2):
        if leq(left, right):
            comparable_checks += 1
            if not WEIGHT[left] > WEIGHT[right]:
                raise AssertionError(f"wave weights do not decrease: {left} <= {right}")
    for base in WEIGHT:
        predecessor_weights = [weight for other, weight in WEIGHT.items() if leq(other, base)]
        minimum_checks += len(predecessor_weights)
        if min(predecessor_weights) != WEIGHT[base]:
            raise AssertionError(f"wave minimum identity fails at {base}")

    # These are every clipping/order chamber below eventual stabilization.
    for q in range(1, cutoff):
        m = q + 1
        orbit = predicted_orbit(m)
        if len(orbit) != q + 8:
            raise AssertionError(f"q={q}: incorrect boundary orbit length")
        for left, right in itertools.pairwise(orbit):
            if delta_types(left, m) != right:
                raise AssertionError(f"q={q}: incorrect boundary transition")
        if delta_types(orbit[-1], m) != orbit[0]:
            raise AssertionError(f"q={q}: boundary orbit does not close")
    return cutoff, len(transitions), comparable_checks + minimum_checks


def verify_type_formula(max_m: int) -> tuple[int, int]:
    states = transitions = 0
    for m in range(2, max_m + 1):
        orbit = predicted_orbit(m)
        if len(orbit) != m + 7:
            raise AssertionError(f"m={m}: wrong orbit length {len(orbit)}")
        if len(set(orbit)) != len(orbit):
            raise AssertionError(f"m={m}: premature labelled repetition")
        for left, right in itertools.pairwise(orbit):
            if delta_types(left, m) != right:
                raise AssertionError(f"m={m}: incorrect internal transition")
            transitions += 1
        if delta_types(orbit[-1], m) != orbit[0]:
            raise AssertionError(f"m={m}: orbit does not close")
        transitions += 1
        states += len(orbit)
    return states, transitions


def verify_nongraph_states(max_m: int) -> None:
    for m in range(2, max_m + 1):
        orbit = predicted_orbit(m)
        if any(sum(t) != 2 for t in orbit[0] | orbit[1]):
            raise AssertionError(f"m={m}: first two states should be graphs")
        for step, current in enumerate(orbit[2:], start=2):
            if max(map(sum, current)) < 3:
                raise AssertionError(f"m={m}, step={step}: expected a facet of size >=3")


def expand_types(types: TypeAntichain, m: int) -> frozenset[int]:
    ordinary_x_bits = (1, 2, 3, 4)
    ordinary_y_bits = range(6, m + 5)
    result: set[int] = set()
    for x0, x_count, y0, y_count in types:
        fixed = x0 | (y0 << 5)
        for chosen_x in itertools.combinations(ordinary_x_bits, x_count):
            for chosen_y in itertools.combinations(ordinary_y_bits, y_count):
                mask = fixed
                for bit in itertools.chain(chosen_x, chosen_y):
                    mask |= 1 << bit
                result.add(mask)
    return frozenset(result)


def delta_masks(facets: frozenset[int], vertex_count: int) -> frozenset[int]:
    admissible = {
        candidate
        for candidate in range(1 << vertex_count)
        if not any(candidate & facet == facet for facet in facets)
    }
    return frozenset(
        candidate
        for candidate in admissible
        if all(
            candidate | (1 << bit) not in admissible
            for bit in range(vertex_count)
            if not candidate & (1 << bit)
        )
    )


def verify_definition_level(direct_max_m: int) -> tuple[int, int]:
    states = facets_checked = 0
    for m in range(2, direct_max_m + 1):
        orbit = predicted_orbit(m)
        actual = expand_types(orbit[0], m)
        for expected_types in orbit:
            expected = expand_types(expected_types, m)
            if actual != expected:
                raise AssertionError(f"definition-level mismatch for m={m}")
            states += 1
            facets_checked += len(actual)
            actual = delta_masks(actual, m + 5)
        if actual != expand_types(orbit[0], m):
            raise AssertionError(f"definition-level orbit does not close for m={m}")
    return states, facets_checked


def result_hash(cutoff: int) -> str:
    payload = {
        "cutoff": cutoff,
        "prefix": [
            sorted((*base, value.slope, value.intercept) for base, value in formula.items())
            for formula in PREFIX
        ],
        "weight": sorted((*base, weight) for base, weight in WEIGHT.items()),
        "tails": {
            name: sorted((*base, value.slope, value.intercept) for base, value in formula.items())
            for name, formula in (("U", U), ("V", V), ("T", T), ("U1", U1), ("V1", V1), ("U2", U2))
        },
        "periods": [(m, len(predicted_orbit(m))) for m in range(2, cutoff + 2)],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=500)
    parser.add_argument("--direct-max-m", type=int, default=8)
    args = parser.parse_args()
    if args.max_m < 2:
        parser.error("--max-m must be at least 2")
    if not 2 <= args.direct_max_m <= min(args.max_m, 9):
        parser.error("require 2 <= --direct-max-m <= min(--max-m,9)")
    cutoff, symbolic_transitions, order_checks = verify_symbolic_certificate()
    states, transitions = verify_type_formula(args.max_m)
    verify_nongraph_states(args.max_m)
    direct_states, facets = verify_definition_level(args.direct_max_m)
    print(
        "SYMBOLIC CERTIFICATE "
        f"q>={cutoff}; affine_transitions={symbolic_transitions}; "
        f"wave_order_checks={order_checks}; exact_boundary_q=1..{cutoff - 1}"
    )
    print(
        "VERIFIED "
        f"B_(5,m), m=2..{args.max_m}; type_states={states}; "
        f"type_transitions={transitions}; definition_states={direct_states}; "
        f"expanded_facets={facets}; NF(B_(5,m))=m+7"
    )
    print(f"RESULT_SHA256={result_hash(cutoff)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
