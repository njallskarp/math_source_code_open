#!/usr/bin/env python3
"""Exact audits for the near-triangle Hamming-graph class-size theorem."""

from __future__ import annotations

import argparse
import itertools


def shell_bound_twice(h: int, profile: tuple[int, ...]) -> int:
    """Twice 1+A+1/2 sum a_i(h-a_i), using Python integers."""
    return 2 + 2 * sum(profile) + sum(a * (h - a) for a in profile)


def greedy_profile(total: int, caps: tuple[int, ...]) -> tuple[int, ...]:
    result = []
    remaining = total
    for cap in caps:
        take = min(cap, remaining)
        result.append(take)
        remaining -= take
    assert remaining == 0
    return tuple(result)


def audit_greedy(max_side: int) -> tuple[int, int]:
    parameter_sets = 0
    totals = 0
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    caps = (n1 - 1, n2 - 1, n3 - 1, n4 - 1)
                    degree = sum(caps)
                    h = (degree + 1) // 2
                    if h < caps[0]:
                        continue
                    parameter_sets += 1
                    r = h - caps[0]
                    s = r + 1
                    target_twice = 2 * n1 * s
                    assert 0 <= r <= caps[1]
                    for total in range(h, degree + 1):
                        totals += 1
                        greedy = greedy_profile(total, caps)
                        bound = shell_bound_twice(h, greedy)
                        assert bound >= target_twice
    return parameter_sets, totals


def audit_full_profiles(max_side: int) -> tuple[int, int]:
    parameter_sets = 0
    profiles = 0
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    caps = (n1 - 1, n2 - 1, n3 - 1, n4 - 1)
                    h = (sum(caps) + 1) // 2
                    if h < caps[0]:
                        continue
                    parameter_sets += 1
                    target_twice = 2 * n1 * (h - caps[0] + 1)
                    for profile in itertools.product(*(range(cap + 1) for cap in caps)):
                        if sum(profile) < h:
                            continue
                        profiles += 1
                        greedy = greedy_profile(sum(profile), caps)
                        assert sum(x * x for x in profile) <= sum(x * x for x in greedy)
                        assert shell_bound_twice(h, profile) >= target_twice
    return parameter_sets, profiles


def hamming_graph(sizes: tuple[int, ...]) -> tuple[list[tuple[int, ...]], list[int]]:
    vertices = list(itertools.product(*(range(size) for size in sizes)))
    adjacency = []
    for vertex in vertices:
        mask = 0
        for index, other in enumerate(vertices):
            if sum(x != y for x, y in zip(vertex, other)) == 1:
                mask |= 1 << index
        adjacency.append(mask)
    return vertices, adjacency


def audit_small_graph() -> tuple[int, int, int]:
    """Enumerate all potentially too-small classes in K3 x K2 x K2 x K2."""
    sizes = (3, 2, 2, 2)
    vertices, adjacency = hamming_graph(sizes)
    degree = sum(size - 1 for size in sizes)
    h = (degree + 1) // 2
    r = h - (sizes[0] - 1)
    target = sizes[0] * (r + 1)
    checked = 0
    feasible_at_target: list[frozenset[int]] = []
    for subset_size in range(h + 1, target + 1):
        for subset in itertools.combinations(range(len(vertices)), subset_size):
            checked += 1
            mask = sum(1 << index for index in subset)
            if all((adjacency[index] & mask).bit_count() >= h for index in subset):
                assert subset_size == target
                feasible_at_target.append(frozenset(subset))

    expected_rectangles = set()
    for direction in range(1, 4):
        other_directions = [axis for axis in range(1, 4) if axis != direction]
        for fixed in itertools.product(*(range(sizes[axis]) for axis in other_directions)):
            rectangle = frozenset(
                index
                for index, vertex in enumerate(vertices)
                if all(vertex[axis] == value for axis, value in zip(other_directions, fixed))
            )
            expected_rectangles.add(rectangle)
    assert set(feasible_at_target) == expected_rectangles
    return checked, len(feasible_at_target), target


def audit_divisible_constructions(max_side: int) -> int:
    checked = 0
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    sizes = (n1, n2, n3, n4)
                    caps = tuple(size - 1 for size in sizes)
                    h = (sum(caps) + 1) // 2
                    if h < caps[0]:
                        continue
                    s = h - caps[0] + 1
                    for direction in range(1, 4):
                        if sizes[direction] % s:
                            continue
                        checked += 1
                        class_size = sizes[0] * s
                        internal_degree = caps[0] + s - 1
                        class_count = 1
                        for index, size in enumerate(sizes[1:], start=1):
                            class_count *= size // s if index == direction else size
                        assert internal_degree == h
                        assert class_size * class_count == n1 * n2 * n3 * n4
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--greedy-max-side", type=int, default=35)
    parser.add_argument("--profile-max-side", type=int, default=9)
    parser.add_argument("--construction-max-side", type=int, default=25)
    args = parser.parse_args()
    if min(args.greedy_max_side, args.profile_max_side, args.construction_max_side) < 3:
        parser.error("all audit bounds must be at least 3")

    greedy_parameters, totals = audit_greedy(args.greedy_max_side)
    profile_parameters, profiles = audit_full_profiles(args.profile_max_side)
    constructions = audit_divisible_constructions(args.construction_max_side)
    subsets, feasible, target = audit_small_graph()

    print(f"greedy parameter quadruples checked: {greedy_parameters}")
    print(f"greedy total-shell sizes checked: {totals}")
    print(f"full-profile parameter quadruples checked: {profile_parameters}")
    print(f"full shell profiles checked: {profiles}")
    print(f"divisible constructions checked: {constructions}")
    print(f"K3xK2xK2xK2 candidate subsets checked: {subsets}")
    print(f"K3xK2xK2xK2 feasible size-{target} subsets: {feasible}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
