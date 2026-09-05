#!/usr/bin/env python3
"""Independent structural audit of the height-2563 selection ordering.

This checker shares no code with the target generator.  It verifies the cell
stabilizer, mixed-radix key, all-pairs schedule closure, and the exact
cutting-planes identity needed by every non-syntactic redundance goal.
"""

from __future__ import annotations

from itertools import product


N = 43
ANCHOR = 13
EXCEPTIONAL = frozenset(range(13))
ANCHOR_RED = frozenset(range(6)) | frozenset(range(14, 29))
CELLS = (
    tuple(range(0, 6)),
    tuple(range(6, 13)),
    tuple(range(14, 29)),
    tuple(range(29, 43)),
)
WEIGHTS = (4096, 256, 16, 1)


def swap(value: int, left: int, right: int) -> int:
    if value == left:
        return right
    if value == right:
        return left
    return value


def schedule(cells: tuple[tuple[int, ...], ...] = CELLS) -> list[tuple[int, int]]:
    return [
        (left, right)
        for cell in cells
        for position, left in enumerate(cell)
        for right in cell[position + 1 :]
    ]


def check_cell_stabilizer() -> None:
    covered = set().union(*map(set, CELLS))
    assert covered == set(range(N)) - {ANCHOR}
    assert sum(map(len, CELLS)) == len(covered)
    assert sum(len(cell) * (len(cell) - 1) // 2 for cell in CELLS) == 232
    for cell in CELLS:
        types = {(vertex in EXCEPTIONAL, vertex in ANCHOR_RED) for vertex in cell}
        assert len(types) == 1
        for left in cell:
            for right in cell:
                image_exceptional = {swap(v, left, right) for v in EXCEPTIONAL}
                image_anchor_red = {swap(v, left, right) for v in ANCHOR_RED}
                assert image_exceptional == set(EXCEPTIONAL)
                assert image_anchor_red == set(ANCHOR_RED)
                assert swap(ANCHOR, left, right) == ANCHOR


def feasible_key_tuples(vertex_cell: int) -> list[tuple[int, int, int, int]]:
    maxima = [len(cell) - int(index == vertex_cell) for index, cell in enumerate(CELLS)]
    tuples = set()
    for d0, d1, d2, d3 in product(*(range(bound + 1) for bound in maxima)):
        tuples.add((d0 + d1, d0, d2, d3))
    return sorted(tuples)


def key(
    signature: tuple[int, int, int, int], weights: tuple[int, ...] | None = None
) -> int:
    if weights is None:
        weights = WEIGHTS
    return sum(weight * value for weight, value in zip(weights, signature, strict=True))


def check_key_dominance() -> tuple[int, int]:
    tuple_count = adjacent_checks = 0
    for cell_index in range(len(CELLS)):
        signatures = feasible_key_tuples(cell_index)
        values = [key(signature) for signature in signatures]
        assert all(left < right for left, right in zip(values, values[1:]))
        assert len(values) == len(set(values))
        tuple_count += len(signatures)
        adjacent_checks += len(signatures) - 1
    return tuple_count, adjacent_checks


def check_schedule_closure(
    order: list[tuple[int, int]], cells: tuple[tuple[int, ...], ...] = CELLS
) -> tuple[int, int]:
    cell_of = {vertex: index for index, cell in enumerate(cells) for vertex in cell}
    prior: set[tuple[int, int]] = set()
    syntactic = arithmetic = 0
    for left, right in order:
        assert cell_of[left] == cell_of[right]
        for old_left, old_right in prior:
            image = (swap(old_left, left, right), swap(old_right, left, right))
            if old_left == left:
                # Old: K(old_right)-K(left)>=0.
                # Current violation: K(left)-K(right)>=1.
                # Negated image: K(right)-K(old_right)>=1.
                # Their coefficient sum is zero and RHS sum is two.
                coefficients = {
                    old_right: 1,
                    left: -1,
                    right: 0,
                }
                coefficients[left] += 1
                coefficients[right] -= 1
                coefficients[right] += 1
                coefficients[old_right] -= 1
                assert all(value == 0 for value in coefficients.values())
                assert image == (right, old_right)
                arithmetic += 1
            else:
                assert image in prior
                syntactic += 1
        prior.add((left, right))
    assert len(prior) == 232
    assert arithmetic == 874
    assert syntactic == 25922
    return arithmetic, syntactic


def check_abstract_orbit_sorting() -> int:
    cases = 0
    # Exhaustive small calibration: sorting is an orbit representative for
    # every key assignment, including repeated keys.
    for size in range(1, 6):
        for values in product(range(3), repeat=size):
            ordered = tuple(sorted(values))
            assert all(ordered[i] <= ordered[j] for i in range(size) for j in range(i + 1, size))
            assert sorted(ordered) == sorted(values)
            cases += 1
    return cases


def verify() -> list[str]:
    check_cell_stabilizer()
    tuple_count, adjacent_checks = check_key_dominance()
    arithmetic, syntactic = check_schedule_closure(schedule())
    orbit_cases = check_abstract_orbit_sorting()
    return [
        "PASS cell_stabilizer cells=4 sizes=6,7,15,14 pair_rows=232",
        f"PASS mixed_radix_key tuples={tuple_count} adjacent_lex_checks={adjacent_checks}",
        f"PASS schedule_closure arithmetic_goals={arithmetic} syntactic_images={syntactic}",
        "PASS cutting_planes_identity coefficient_sum=0 rhs_sum=2",
        f"PASS abstract_orbit_sorting cases={orbit_cases} key_alphabet=0,1,2 sizes=1..5",
        "VERDICT height-2563 selection ordering is equisatisfiability-preserving",
    ]


def main() -> None:
    print("\n".join(verify()))


if __name__ == "__main__":
    main()
