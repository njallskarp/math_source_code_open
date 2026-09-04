#!/usr/bin/env python3
"""Independent exact checks for the Hamming multi-box review.

CPython 3.12+, standard library only.  This is corroboration for the proofs in
README.md, not a finite substitute for their universal arguments.
"""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement, product
from math import prod


Cell = tuple[int, ...]


def cells(sides: tuple[int, ...]) -> tuple[Cell, ...]:
    return tuple(product(*(range(side) for side in sides)))


def adjacency_masks(vertices: tuple[Cell, ...]) -> tuple[int, ...]:
    masks: list[int] = []
    for i, left in enumerate(vertices):
        mask = 0
        for j, right in enumerate(vertices):
            if i != j and sum(a != b for a, b in zip(left, right, strict=True)) == 1:
                mask |= 1 << j
        masks.append(mask)
    return tuple(masks)


def induced_min_degree(mask: int, neighbors: tuple[int, ...]) -> int:
    return min((mask & neighbors[i]).bit_count() for i in range(len(neighbors)) if mask >> i & 1)


def subset_masks(order: int, sizes: range):
    for size in sizes:
        for chosen in combinations(range(order), size):
            yield sum(1 << i for i in chosen)


def audit_shell_optimization(max_h: int = 40, max_dimension: int = 8) -> int:
    """Dynamic programming, rather than profile-product enumeration."""
    checked = 0
    for h in range(2, max_h + 1):
        best = {0: 0}  # total first-shell degree -> largest sum of squares
        for dimension in range(1, max_dimension + 1):
            nxt: dict[int, int] = {}
            for total, squares in best.items():
                for value in range(h):
                    new_total = total + value
                    nxt[new_total] = max(nxt.get(new_total, -1), squares + value * value)
            best = nxt
            if dimension < 2:
                continue
            equality_totals: list[int] = []
            for total, max_squares in best.items():
                if total < h:
                    continue
                twice_bound = 2 * (1 + total) + h * total - max_squares
                assert twice_bound >= 4 * h
                if twice_bound == 4 * h:
                    equality_totals.append(total)
                checked += 1
            assert equality_totals == [h]
            assert best[h] == (h - 1) ** 2 + 1
    return checked


def equality_profile(mask: int, vertices: tuple[Cell, ...], h: int) -> bool:
    """Check the local profile forced by equality in the shell argument."""
    for i, vertex in enumerate(vertices):
        if not (mask >> i) & 1:
            continue
        counts = []
        for axis in range(len(vertex)):
            line_count = sum(
                1
                for j, other in enumerate(vertices)
                if (mask >> j) & 1
                and j != i
                and all(other[k] == vertex[k] for k in range(len(vertex)) if k != axis)
            )
            if line_count:
                counts.append(line_count)
        assert sorted(counts) == [1, h - 1]
    return True


def audit_small_boxes(max_volume: int = 14) -> tuple[int, int, int]:
    boxes = short_subsets = equality_sets = 0
    for s in range(3, 7):
        h = s - 1
        for dimension in range(2, 5):
            for sides in combinations_with_replacement(range(1, h + 1), dimension):
                # Nondecreasing sides avoid coordinate-permutation duplicates.
                order = prod(sides)
                if order < h + 1 or order > max_volume:
                    continue
                vertices = cells(sides)
                neighbors = adjacency_masks(vertices)
                boxes += 1
                for mask in subset_masks(order, range(1, min(2 * h, order + 1))):
                    assert induced_min_degree(mask, neighbors) < h
                    short_subsets += 1
                if order >= 2 * h:
                    for mask in subset_masks(order, range(2 * h, 2 * h + 1)):
                        if induced_min_degree(mask, neighbors) >= h:
                            equality_profile(mask, vertices, h)
                            equality_sets += 1
    return boxes, short_subsets, equality_sets


def audit_cube_bipartitions() -> int:
    vertices = cells((2, 2, 2))
    neighbors = adjacency_masks(vertices)
    full = (1 << len(vertices)) - 1
    partitions = 0
    # Force vertex 0 into the first part to count unordered bipartitions once.
    for mask in subset_masks(8, range(4, 5)):
        if not mask & 1:
            continue
        other = full ^ mask
        if induced_min_degree(mask, neighbors) >= 2 and induced_min_degree(other, neighbors) >= 2:
            partitions += 1
    assert partitions == 3
    return partitions


def audit_volume_classification(max_s: int = 64) -> tuple[int, tuple[tuple[int, int, int, int], ...]]:
    checked = 0
    survivors: list[tuple[int, int, int, int]] = []
    for s in range(2, max_s + 1):
        for residues in product(range(1, s), repeat=3):
            volume = prod(residues)
            quotient = volume // s
            if quotient < 2:
                continue
            checked += 1
            if quotient * (2 * s - 2) <= volume:
                survivors.append((s, *residues))
    assert survivors == [(3, 2, 2, 2)]
    return checked, tuple(survivors)


def audit_general_volume_classification(
    max_s: int = 16, max_dimension: int = 7
) -> tuple[int, tuple[tuple[int, tuple[int, ...]], ...]]:
    """Bounded audit of the proved arbitrary-dimensional refinement."""
    checked = 0
    normalized_survivors: set[tuple[int, tuple[int, ...]]] = set()
    for s in range(2, max_s + 1):
        for dimension in range(1, max_dimension + 1):
            for residues in combinations_with_replacement(range(1, s), dimension):
                volume = prod(residues)
                quotient = volume // s
                if quotient < 2:
                    continue
                checked += 1
                if quotient * (2 * s - 2) <= volume:
                    assert s == 3
                    assert residues.count(2) == 3
                    assert all(value in (1, 2) for value in residues)
                    normalized_survivors.add((s, tuple(value for value in residues if value != 1)))
    survivors = tuple(sorted(normalized_survivors))
    assert survivors == ((3, (2, 2, 2)),)
    return checked, survivors


def exceptional_labels(sides: tuple[int, ...]) -> dict[Cell, tuple[int, ...]]:
    """Assign every cell directly to a stripped triple or one residual face."""
    residues = tuple(side % 3 for side in sides)
    assert all(residue in (1, 2) for residue in residues)
    assert residues.count(2) == 3
    labels: dict[Cell, tuple[int, ...]] = {}
    tails = tuple(side - residue for side, residue in zip(sides, residues, strict=True))
    for vertex in cells(sides):
        for axis in range(len(sides)):
            if vertex[axis] < tails[axis] and all(vertex[j] >= tails[j] for j in range(axis)):
                fixed = tuple(vertex[j] for j in range(len(sides)) if j != axis)
                labels[vertex] = (axis, vertex[axis] // 3, *fixed)
                break
        else:
            face_axis = residues.index(2)
            labels[vertex] = (len(sides), vertex[face_axis] - tails[face_axis])
    return labels


def verify_exceptional_partition(sides: tuple[int, ...]) -> int:
    labels = exceptional_labels(sides)
    parts: dict[tuple[int, ...], list[Cell]] = {}
    for vertex, label in labels.items():
        parts.setdefault(label, []).append(vertex)
    assert len(parts) == prod(sides) // 3
    for part in parts.values():
        vertices = tuple(part)
        assert induced_min_degree((1 << len(vertices)) - 1, adjacency_masks(vertices)) >= 2
    return len(parts)


def audit_generalized_constructions() -> tuple[int, int]:
    instances = parts = 0
    for dimension in range(3, 6):
        for exceptional_axes in combinations(range(dimension), 3):
            for exceptional_quotients in product(range(2), repeat=3):
                quotient_by_axis = dict(zip(exceptional_axes, exceptional_quotients, strict=True))
                sides = tuple(
                    3 * quotient_by_axis[axis] + 2 if axis in quotient_by_axis else 4
                    for axis in range(dimension)
                )
                parts += verify_exceptional_partition(sides)
                instances += 1
    return instances, parts


def audit_constructions(max_q: int = 5) -> tuple[int, int, int]:
    partitions = parts = family_parameters = 0
    for q2, q3, q4 in product(range(max_q + 1), repeat=3):
        sides = (3 * q2 + 2, 3 * q3 + 2, 3 * q4 + 2)
        parts += verify_exceptional_partition(sides)
        partitions += 1

    for q2 in range(51):
        for q3 in range(q2 + 1):
            for q4 in range(q3 + 1):
                if q3 + q4 == 0:
                    continue
                total_q = q2 + q3 + q4
                for epsilon in (0, 1):
                    orders = (3 * total_q + epsilon, 3 * q2 + 2, 3 * q3 + 2, 3 * q4 + 2)
                    assert tuple(sorted(orders, reverse=True)) == orders
                    deficits = tuple(order - 1 for order in orders)
                    h = (sum(deficits) + 1) // 2
                    assert h == 3 * total_q + epsilon + 1
                    assert h - deficits[0] + 1 == 3
                    formula = (
                        9 * q2 * q3 * q4
                        + 6 * (q2 * q3 + q2 * q4 + q3 * q4)
                        + 4 * total_q
                        + 2
                    )
                    assert prod(orders[1:]) // 3 == formula
                    family_parameters += 1

    # Definition-level check of the advertised K_7 x K_5 x K_5 x K_2 witness.
    sample_sides = (5, 5, 2)
    sample_parts = verify_exceptional_partition(sample_sides)
    assert sample_parts == 16
    assert (7 - 1) + 2 == 8 == ((7 - 1) + (5 - 1) + (5 - 1) + (2 - 1) + 1) // 2
    return partitions, parts, family_parameters


def main() -> None:
    shell_states = audit_shell_optimization()
    boxes, short_subsets, equality_sets = audit_small_boxes()
    cube_partitions = audit_cube_bipartitions()
    volume_tuples, survivors = audit_volume_classification()
    general_volume_tuples, general_survivors = audit_general_volume_classification()
    partitions, parts, family_parameters = audit_constructions()
    generalized_partitions, generalized_parts = audit_generalized_constructions()
    print(f"shell DP states checked: {shell_states}")
    print(f"small boxes checked: {boxes}")
    print(f"subsets below 2s-2 checked: {short_subsets}")
    print(f"sharp equality sets checked: {equality_sets}")
    print(f"legal unordered [2]^3 bipartitions: {cube_partitions}")
    print(f"three-residue tuples checked: {volume_tuples}")
    print(f"volume-bound survivors: {survivors}")
    print(f"general residue profiles checked: {general_volume_tuples}")
    print(f"normalized general survivors: {general_survivors}")
    print(f"exceptional partitions checked: {partitions}")
    print(f"exceptional parts checked: {parts}")
    print(f"higher-dimensional exceptional partitions checked: {generalized_partitions}")
    print(f"higher-dimensional exceptional parts checked: {generalized_parts}")
    print(f"family parameter points checked: {family_parameters}")
    print("independent exact checks passed")


if __name__ == "__main__":
    main()
