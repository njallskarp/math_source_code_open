#!/usr/bin/env python3
"""Exact audits for the dominant-factor majority C-colouring theorem.

The universal proof is in DOMINANT_FACTOR_THEOREM.md.  This checker audits its
integer endpoint reduction, bounded coordinate-level shell profiles, and one
small Hamming graph directly from the definition.
"""

from __future__ import annotations

import argparse
import itertools


def doubled_coarse_bound(h: int, a: int, b: int) -> int:
    """Return 2 Q(a,b), avoiding fractions."""
    return 2 + a * (h + 2 - a) + b * (h + 2 - b)


def doubled_shell_bound(h: int, profile: tuple[int, ...]) -> int:
    """Return twice the right side of the unmerged shell inequality."""
    return 2 + 2 * sum(profile) + sum(x * (h - x) for x in profile)


def audit_coarse(max_dominant: int) -> tuple[int, int, int]:
    pairs = 0
    profiles = 0
    strict_margin = None
    for dominant in range(3, max_dominant + 1):
        for minor_sum in range(1, dominant - 1):
            pairs += 1
            degree = dominant + minor_sum
            h = (degree + 1) // 2
            ell = degree // 2
            assert dominant >= minor_sum + 2
            assert h < dominant
            for a in range(ell):
                for b in range(minor_sum + 1):
                    if a + b < h:
                        continue
                    profiles += 1
                    bound2 = doubled_coarse_bound(h, a, b)
                    assert bound2 >= 2 * (dominant + 1)
                    if minor_sum >= 2:
                        margin = bound2 - 2 * (dominant + 1)
                        assert margin >= 2
                        strict_margin = margin if strict_margin is None else min(strict_margin, margin)
    assert strict_margin is not None
    return pairs, profiles, strict_margin


def nonincreasing_tuples(length: int, maximum: int):
    for values in itertools.product(range(1, maximum + 1), repeat=length):
        if all(values[i] >= values[i + 1] for i in range(length - 1)):
            yield values


def audit_structured(
    max_dimension: int, max_minor: int, max_dominant: int
) -> tuple[int, int]:
    parameter_tuples = 0
    profiles = 0
    for dimension in range(2, max_dimension + 1):
        for minors in nonincreasing_tuples(dimension - 1, max_minor):
            minor_sum = sum(minors)
            first_min = max(minors[0], minor_sum + 2)
            for dominant in range(first_min, max_dominant + 1):
                parameter_tuples += 1
                degree = dominant + minor_sum
                h = (degree + 1) // 2
                ell = degree // 2
                for a in range(ell):
                    for tail in itertools.product(*(range(x + 1) for x in minors)):
                        profile = (a,) + tail
                        if sum(profile) < h:
                            continue
                        profiles += 1
                        bound2 = doubled_shell_bound(h, profile)
                        assert bound2 >= 2 * (dominant + 1)
                        if dimension >= 3:
                            assert bound2 >= 2 * (dominant + 2)
    return parameter_tuples, profiles


def hamming_adjacency(sizes: tuple[int, ...]) -> tuple[list[tuple[int, ...]], list[int]]:
    vertices = list(itertools.product(*(range(size) for size in sizes)))
    masks: list[int] = []
    for vertex in vertices:
        mask = 0
        for j, other in enumerate(vertices):
            if sum(x != y for x, y in zip(vertex, other)) == 1:
                mask |= 1 << j
        masks.append(mask)
    return vertices, masks


def audit_boundary_graph() -> tuple[int, int]:
    """Check all extendable minimal classes in K_5 square K_2 square K_2.

    Besides internal minimum degree, a class in a full majority colouring must
    give every outside vertex at most floor(D/2) neighbours in that class.
    The latter is the external-fibre constraint used in the proof.
    """
    sizes = (5, 2, 2)
    vertices, adjacency = hamming_adjacency(sizes)
    degree = sum(size - 1 for size in sizes)
    h = (degree + 1) // 2
    ell = degree // 2
    dominant_order = sizes[0]
    checked = 0
    feasible_size_five: list[frozenset[int]] = []
    for subset_size in range(h + 1, dominant_order + 1):
        for subset in itertools.combinations(range(len(vertices)), subset_size):
            checked += 1
            mask = sum(1 << index for index in subset)
            internally_legal = all(
                (adjacency[index] & mask).bit_count() >= h for index in subset
            )
            externally_compatible = all(
                (adjacency[index] & mask).bit_count() <= ell
                for index in range(len(vertices))
                if not (mask >> index) & 1
            )
            if internally_legal and externally_compatible:
                assert subset_size == dominant_order
                feasible_size_five.append(frozenset(subset))

    fibres = {
        frozenset(
            index
            for index, vertex in enumerate(vertices)
            if vertex[1:] == fixed_tail
        )
        for fixed_tail in itertools.product(range(2), repeat=2)
    }
    assert set(feasible_size_five) == fibres
    return checked, len(feasible_size_five)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-dominant", type=int, default=201)
    parser.add_argument("--max-dimension", type=int, default=5)
    parser.add_argument("--max-minor", type=int, default=4)
    args = parser.parse_args()
    if args.max_dominant < 5 or args.max_dimension < 2 or args.max_minor < 1:
        parser.error("bounds are too small for the documented audits")

    pairs, coarse_profiles, margin = audit_coarse(args.max_dominant)
    tuples, structured_profiles = audit_structured(
        args.max_dimension, args.max_minor, min(args.max_dominant, 24)
    )
    subsets, feasible = audit_boundary_graph()

    print(f"dominant pairs checked: {pairs}")
    print(f"coarse shell profiles checked: {coarse_profiles}")
    print(f"structured parameter tuples checked: {tuples}")
    print(f"structured shell profiles checked: {structured_profiles}")
    print(f"K5xK2xK2 candidate subsets checked: {subsets}")
    print(f"K5xK2xK2 feasible size-5 subsets: {feasible}")
    print(f"minimum doubled strict-margin (S>=2): {margin}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
