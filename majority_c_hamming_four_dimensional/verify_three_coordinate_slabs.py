#!/usr/bin/env python3
"""Exact audits for three-coordinate residue-slab composition.

CPython 3.12+, standard library only. The universal claims are proved in
THREE_COORDINATE_SLABS.md. This checker imports the already audited cyclic
rectangle constructor, reconstructs bounded three-dimensional partitions,
maps the four-dimensional parameter region, and checks the explicit family.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections.abc import Sequence

from verify_cross_boundary import is_line_part, rectangle_partition


Cell = tuple[int, ...]
Part = tuple[Cell, ...]


def qualifying_slab_pair(
    sides: Sequence[int], s: int
) -> tuple[int, int, int] | None:
    if s < 2:
        return None
    for first, second in itertools.combinations(range(3), 2):
        remaining = 3 - first - second
        if sides[first] < s or sides[second] < s:
            continue
        pair_remainder = (sides[first] * sides[second]) % s
        third_remainder = sides[remaining] % s
        if third_remainder * pair_remainder < s:
            return first, second, remaining
    return None


def qualifying_old_pair(
    sides: Sequence[int], s: int
) -> tuple[int, int, int] | None:
    if s < 2:
        return None
    for first, second in itertools.combinations(range(3), 2):
        remaining = 3 - first - second
        if sides[first] < s or sides[second] < s:
            continue
        pair_remainder = (sides[first] * sides[second]) % s
        if sides[remaining] * pair_remainder < s:
            return first, second, remaining
    return None


def previous_residue_exact(sides: Sequence[int], s: int) -> bool:
    residues = [side % s for side in sides]
    residue_volume = math.prod(residues)
    if residue_volume < s:
        return True
    if (
        s <= residue_volume < 2 * s
        and sum(residues) >= s + len(sides) - 1
    ):
        return True
    return s == 3 and residues == [2, 2, 2]


def slab_partition(m: int, n: int, p: int, s: int) -> list[Part]:
    if s < 2 or m < s or n < s or p < 1:
        raise ValueError("require s>=2, m,n>=s, and p>=1")
    rectangle = rectangle_partition(m, n, s)
    return extend_partition(rectangle, (m, n), p, s)


def extend_partition(
    base_parts: Sequence[Part],
    base_dimensions: Sequence[int],
    p: int,
    s: int,
) -> list[Part]:
    """Implement the dimension-free modular composition lemma."""
    if s < 2 or p < 1 or not base_dimensions:
        raise ValueError("require s>=2, p>=1, and a nonempty base box")
    base_volume = math.prod(base_dimensions)
    slab_quotient, residual_layers = divmod(p, s)
    base_quotient, base_remainder = divmod(base_volume, s)
    if len(base_parts) != base_quotient:
        raise ValueError("base partition does not have the optimal part count")
    if residual_layers * base_remainder >= s:
        raise ValueError("modular composition criterion is false")

    parts: list[Part] = []
    slab_cut = slab_quotient * s
    for base_cell in itertools.product(*(range(side) for side in base_dimensions)):
        for block in range(slab_quotient):
            parts.append(
                tuple(
                    base_cell + (last,)
                    for last in range(block * s, (block + 1) * s)
                )
            )

    for last in range(slab_cut, p):
        for base_part in base_parts:
            parts.append(tuple(cell + (last,) for cell in base_part))

    assert len(parts) == slab_quotient * base_volume + residual_layers * base_quotient
    return parts


def embedded_minor_partition(sides: Sequence[int], s: int) -> list[Part]:
    witness = qualifying_slab_pair(sides, s)
    if witness is None:
        raise ValueError("no qualifying residue-slab coordinate order")
    first, second, remaining = witness
    local_parts = slab_partition(
        sides[first], sides[second], sides[remaining], s
    )
    parts: list[Part] = []
    for local_part in local_parts:
        embedded: list[Cell] = []
        for left, right, last in local_part:
            cell = [0, 0, 0]
            cell[first] = left
            cell[second] = right
            cell[remaining] = last
            embedded.append(tuple(cell))
        parts.append(tuple(embedded))
    return parts


def check_box(m: int, n: int, p: int, s: int) -> tuple[int, int]:
    parts = slab_partition(m, n, p, s)
    expected = set(itertools.product(range(m), range(n), range(p)))
    seen: set[Cell] = set()
    for part in parts:
        assert len(part) >= s
        assert len(set(part)) == len(part)
        assert is_line_part(part)
        assert seen.isdisjoint(part)
        seen.update(part)
    assert seen == expected
    assert len(parts) == (m * n * p) // s
    return len(parts), len(seen)


def audit_boxes(max_s: int, side_margin: int) -> tuple[int, int, int, int]:
    instances = 0
    parts_checked = 0
    cells_checked = 0
    genuinely_iterated = 0
    for s in range(2, max_s + 1):
        for m in range(s, 2 * s + side_margin + 1):
            for n in range(s, 2 * s + side_margin + 1):
                pair_remainder = (m * n) % s
                for p in range(1, 2 * s + side_margin + 1):
                    if (p % s) * pair_remainder >= s:
                        continue
                    count, volume = check_box(m, n, p, s)
                    instances += 1
                    parts_checked += count
                    cells_checked += volume
                    if p * pair_remainder >= s:
                        genuinely_iterated += 1
    return instances, parts_checked, cells_checked, genuinely_iterated


def audit_parameters(max_side: int) -> tuple[int, int, int, int]:
    near_triangle = 0
    slab_exact = 0
    beyond_old_layering = 0
    beyond_all_previous = 0
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    deficits = [n1 - 1, n2 - 1, n3 - 1, n4 - 1]
                    h = (sum(deficits) + 1) // 2
                    if h < deficits[0]:
                        continue
                    near_triangle += 1
                    s = h - deficits[0] + 1
                    sides = [n2, n3, n4]
                    if qualifying_slab_pair(sides, s) is None:
                        continue
                    slab_exact += 1
                    if qualifying_old_pair(sides, s) is not None:
                        continue
                    beyond_old_layering += 1
                    if not previous_residue_exact(sides, s):
                        beyond_all_previous += 1
    return near_triangle, slab_exact, beyond_old_layering, beyond_all_previous


def audit_hamming_constructions(max_side: int) -> tuple[int, int, int]:
    instances = 0
    parts_checked = 0
    cells_checked = 0
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    deficits = [n1 - 1, n2 - 1, n3 - 1, n4 - 1]
                    h = (sum(deficits) + 1) // 2
                    if h < deficits[0]:
                        continue
                    s = h - deficits[0] + 1
                    sides = [n2, n3, n4]
                    if qualifying_slab_pair(sides, s) is None:
                        continue
                    parts = embedded_minor_partition(sides, s)
                    expected = set(itertools.product(*(range(side) for side in sides)))
                    seen: set[Cell] = set()
                    for part in parts:
                        assert len(part) >= s
                        assert len(set(part)) == len(part)
                        assert is_line_part(part)
                        assert deficits[0] + len(part) - 1 >= h
                        assert seen.isdisjoint(part)
                        seen.update(part)
                    assert seen == expected
                    assert len(parts) == math.prod(sides) // s
                    instances += 1
                    parts_checked += len(parts)
                    cells_checked += len(seen)
    return instances, parts_checked, cells_checked


def audit_infinite_family(max_k: int, reconstruct_max_k: int) -> tuple[int, int, int]:
    checked = 0
    reconstructed = 0
    reconstructed_parts = 0
    for k in range(2, max_k + 1):
        s = 2 * k + 1
        orders = [3 * k + 6, 3 * k + 2, 2 * k + 3, 2 * k + 3]
        assert orders == sorted(orders, reverse=True)
        deficits = [order - 1 for order in orders]
        h = (sum(deficits) + 1) // 2
        assert h == 5 * k + 5
        assert h - deficits[0] + 1 == s
        residues = [order % s for order in orders[1:]]
        assert residues == [k + 1, 2, 2]
        assert math.prod(residues) == 2 * s + 2
        pair_remainders = {
            (residues[first] * residues[second]) % s
            for first, second in itertools.combinations(range(3), 2)
        }
        assert pair_remainders == {1, 4}
        assert qualifying_old_pair(orders[1:], s) is None
        assert qualifying_slab_pair(orders[1:], s) is not None
        expected = 6 * k * k + 19 * k + 16
        assert math.prod(orders[1:]) == s * expected + 2
        assert not previous_residue_exact(orders[1:], s)
        checked += 1

        if k <= reconstruct_max_k:
            parts = embedded_minor_partition(orders[1:], s)
            assert len(parts) == expected
            assert all(len(part) >= s and is_line_part(part) for part in parts)
            reconstructed += 1
            reconstructed_parts += len(parts)
    return checked, reconstructed, reconstructed_parts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--box-max-s", type=int, default=10)
    parser.add_argument("--box-side-margin", type=int, default=2)
    parser.add_argument("--parameter-max-side", type=int, default=60)
    parser.add_argument("--hamming-max-side", type=int, default=16)
    parser.add_argument("--family-max-k", type=int, default=10000)
    parser.add_argument("--family-reconstruct-max-k", type=int, default=5)
    args = parser.parse_args()

    boxes = audit_boxes(args.box_max_s, args.box_side_margin)
    parameters = audit_parameters(args.parameter_max_side)
    hamming = audit_hamming_constructions(args.hamming_max_side)
    family = audit_infinite_family(
        args.family_max_k, args.family_reconstruct_max_k
    )

    print(f"three-dimensional box partitions reconstructed: {boxes[0]}")
    print(f"three-dimensional line parts checked: {boxes[1]}")
    print(f"three-dimensional cells checked: {boxes[2]}")
    print(f"boxes beyond the old layerwise criterion: {boxes[3]}")
    print(f"four-dimensional near-triangle parameters checked: {parameters[0]}")
    print(f"residue-slab parameters detected: {parameters[1]}")
    print(f"parameters beyond old layerwise criterion: {parameters[2]}")
    print(f"parameters beyond every previous exact criterion: {parameters[3]}")
    print(f"lifted Hamming partitions reconstructed: {hamming[0]}")
    print(f"lifted Hamming line parts checked: {hamming[1]}")
    print(f"lifted Hamming minor cells checked: {hamming[2]}")
    print(f"explicit infinite-family indices checked: {family[0]}")
    print(f"explicit family partitions reconstructed: {family[1]}")
    print(f"explicit family line parts checked: {family[2]}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
