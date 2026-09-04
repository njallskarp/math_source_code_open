#!/usr/bin/env python3
"""Generate the exact six-quotient Hall multicover certificate."""

from __future__ import annotations

import base64
import itertools
import json
from fractions import Fraction

ORDER = 6
PAIRS = tuple((i, j) for i in range(ORDER) for j in range(i + 1, ORDER))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
FEASIBLE_CODE = 0xFFFF
DZITSOEV_CANONICAL_MASK = 345
PUBLISHED_MASK = 21465
PUBLISHED_SIZES = (7, 3, 11, 3, 9, 3)
CANONICAL_MINIMUM_SIZES = (11, 3, 3, 9, 3, 7)


def relabel(mask: int, permutation: tuple[int, ...]) -> int:
    """Relabel by the map old vertex -> permutation[old vertex]."""
    answer = 0
    for bit, (low, high) in enumerate(PAIRS):
        source, target = (low, high) if mask >> bit & 1 else (high, low)
        source, target = permutation[source], permutation[target]
        new_low, new_high = sorted((source, target))
        if source == new_low:
            answer |= 1 << PAIR_INDEX[(new_low, new_high)]
    return answer


def quotient_representatives() -> tuple[int, ...]:
    """Partition all labeled tournaments into relabeling orbits."""
    permutations = tuple(itertools.permutations(range(ORDER)))
    remaining = set(range(1 << len(PAIRS)))
    representatives: list[int] = []
    while remaining:
        representative = min(remaining)
        orbit = {relabel(representative, permutation) for permutation in permutations}
        if min(orbit) != representative or not orbit <= remaining:
            raise AssertionError("tournament orbit partition failed")
        remaining.difference_update(orbit)
        representatives.append(representative)
    if len(representatives) != 56:
        raise AssertionError("expected 56 six-vertex tournament types")
    return tuple(representatives)


def tournament_out(mask: int) -> tuple[frozenset[int], ...]:
    out = [set() for _ in range(ORDER)]
    for bit, (low, high) in enumerate(PAIRS):
        source, target = (low, high) if mask >> bit & 1 else (high, low)
        out[source].add(target)
    return tuple(frozenset(row) for row in out)


def set_mask(vertices: set[int] | frozenset[int]) -> int:
    return sum(1 << vertex for vertex in vertices)


def closed_rows(
    out: tuple[frozenset[int], ...], root: int
) -> tuple[tuple[int, int, tuple[int, ...]], ...]:
    """Return (source mask, neighbor mask, signed incidence row)."""
    first = out[root]
    reached = set().union(*(out[head] for head in first)) if first else set()
    second = frozenset(reached.difference(first, {root}))
    rows = []
    for source_mask in range(1, 1 << ORDER):
        source = frozenset(vertex for vertex in first if source_mask >> vertex & 1)
        if not source or set_mask(source) != source_mask:
            continue
        neighbors = frozenset(
            target
            for target in second
            if any(target in out[vertex] for vertex in source)
        )
        closure = frozenset(
            vertex for vertex in first if (out[vertex] & second) <= neighbors
        )
        if closure != source:
            continue
        row = tuple(
            int(vertex in source) - int(vertex in neighbors)
            for vertex in range(ORDER)
        )
        rows.append((source_mask, set_mask(neighbors), row))
    return tuple(rows)


MULTIPLIERS = tuple(
    sorted(
        (coefficients for coefficients in itertools.product(range(4), repeat=ORDER) if any(coefficients)),
        key=lambda coefficients: (sum(coefficients), max(coefficients), coefficients),
    )
)


def blocking_multiplier(rows: tuple[tuple[int, ...], ...]) -> tuple[int, ...] | None:
    for coefficients in MULTIPLIERS:
        total = tuple(
            sum(coefficients[root] * rows[root][column] for root in range(ORDER))
            for column in range(ORDER)
        )
        if max(total) <= 0:
            return coefficients
    return None


def encode_multiplier(coefficients: tuple[int, ...]) -> int:
    return sum(value << (2 * index) for index, value in enumerate(coefficients))


def solve_exact(matrix: tuple[tuple[int, ...], ...]) -> tuple[Fraction, ...]:
    augmented = [
        [Fraction(value) for value in row] + [Fraction(1)] for row in matrix
    ]
    for column in range(ORDER):
        pivot = next(
            (row for row in range(column, ORDER) if augmented[row][column]), None
        )
        if pivot is None:
            raise ValueError("singular matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(ORDER):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    augmented[row][index] - scale * augmented[column][index]
                    for index in range(ORDER + 1)
                ]
    return tuple(augmented[row][-1] for row in range(ORDER))


def transpose(matrix: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(matrix[row][column] for row in range(ORDER)) for column in range(ORDER))


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    work = [list(row) for row in matrix]
    sign = 1
    denominator = 1
    for column in range(ORDER - 1):
        pivot = next((row for row in range(column, ORDER) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        for row in range(column + 1, ORDER):
            for target in range(column + 1, ORDER):
                numerator = (
                    work[row][target] * pivot_value
                    - work[row][column] * work[column][target]
                )
                if numerator % denominator:
                    raise AssertionError("Bareiss division was not exact")
                work[row][target] = numerator // denominator
            work[row][column] = 0
        denominator = pivot_value
    return sign * work[-1][-1]


def fraction_as_int(value: Fraction) -> int:
    if value.denominator != 1:
        raise AssertionError(f"expected an integer, found {value}")
    return value.numerator


def build_certificate() -> dict[str, object]:
    quotient_entries = []
    feasible_entries = []
    blocked_chambers = 0
    feasible_chambers = 0
    zero_root_quotients = 0
    all_chambers = 0

    for mask in quotient_representatives():
        out = tournament_out(mask)
        root_rows = tuple(closed_rows(out, root) for root in range(ORDER))
        root_counts = tuple(len(rows) for rows in root_rows)
        codes = bytearray()
        if 0 in root_counts:
            zero_root_quotients += 1
        else:
            for choices in itertools.product(*(range(count) for count in root_counts)):
                matrix = tuple(root_rows[root][choices[root]][2] for root in range(ORDER))
                coefficients = blocking_multiplier(matrix)
                if coefficients is not None:
                    code = encode_multiplier(coefficients)
                    if not 0 < code < FEASIBLE_CODE:
                        raise AssertionError("invalid multiplier code")
                    blocked_chambers += 1
                else:
                    code = FEASIBLE_CODE
                    weights = solve_exact(matrix)
                    dual = solve_exact(transpose(matrix))
                    if any(value <= 0 for value in weights + dual):
                        raise AssertionError("uncertified chamber survived multiplier search")
                    if determinant(matrix) != -1:
                        raise AssertionError("feasible chamber is not unimodular with determinant -1")
                    weight_ints = tuple(fraction_as_int(value) for value in weights)
                    dual_ints = tuple(fraction_as_int(value) for value in dual)
                    feasible_entries.append(
                        {
                            "choices": list(choices),
                            "dual": list(dual_ints),
                            "mask": mask,
                            "source_masks": [
                                root_rows[root][choices[root]][0] for root in range(ORDER)
                            ],
                            "neighbor_masks": [
                                root_rows[root][choices[root]][1] for root in range(ORDER)
                            ],
                            "total": sum(weight_ints),
                            "weights": list(weight_ints),
                        }
                    )
                    feasible_chambers += 1
                codes.extend(code.to_bytes(2, "big"))
                all_chambers += 1
        quotient_entries.append(
            {
                "codes_base64": base64.b64encode(codes).decode("ascii"),
                "mask": mask,
                "root_counts": list(root_counts),
            }
        )

    feasible_entries.sort(key=lambda entry: (entry["total"], entry["choices"]))
    totals = [entry["total"] for entry in feasible_entries]
    if (
        zero_root_quotients != 12
        or all_chambers != 3603
        or blocked_chambers != 3591
        or feasible_chambers != 12
        or {entry["mask"] for entry in feasible_entries} != {DZITSOEV_CANONICAL_MASK}
        or totals != [36, 39, 42, 42, 45, 48, 48, 54, 56, 64, 72, 88]
        or feasible_entries[0]["weights"] != list(CANONICAL_MINIMUM_SIZES)
    ):
        raise AssertionError("unexpected six-quotient classification")

    return {
        "blocked_chambers": blocked_chambers,
        "canonical_minimum_sizes": list(CANONICAL_MINIMUM_SIZES),
        "canonical_quotient_mask": DZITSOEV_CANONICAL_MASK,
        "chambers": all_chambers,
        "coefficient_bound": 3,
        "feasible": feasible_entries,
        "feasible_chambers": feasible_chambers,
        "format": "strong-seymour-six-quotient-multicover-v1",
        "mask_convention": "lexicographic unordered pairs; bit 1 means low vertex dominates high",
        "pairs": [list(pair) for pair in PAIRS],
        "published_quotient_mask": PUBLISHED_MASK,
        "published_sizes": list(PUBLISHED_SIZES),
        "quotients": quotient_entries,
        "zero_root_quotients": zero_root_quotients,
    }


def main() -> None:
    print(json.dumps(build_certificate(), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
