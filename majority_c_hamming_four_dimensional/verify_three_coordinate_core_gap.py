#!/usr/bin/env python3
"""Exact audit for the three-coordinate Hamming-core gap.

CPython 3.12+, standard library only.  The universal theorem is proved in
THREE_COORDINATE_CORE_GAP.md.  This checker exhausts small hosts directly
from the Hamming-distance definition and audits the shell-profile arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections.abc import Iterator, Sequence


Cell = tuple[int, ...]


DEFAULT_HOSTS = (
    (3, 3),
    (4, 3),
    (5, 2),
    (2, 2, 2),
    (3, 2, 2),
    (4, 2, 2),
    (3, 3, 2),
    (2, 2, 2, 2),
)


def vertices(sides: Sequence[int]) -> tuple[Cell, ...]:
    return tuple(itertools.product(*(range(side) for side in sides)))


def neighbor_masks(cells: Sequence[Cell]) -> tuple[int, ...]:
    masks: list[int] = []
    for left in cells:
        mask = 0
        for index, right in enumerate(cells):
            if sum(a != b for a, b in zip(left, right, strict=True)) == 1:
                mask |= 1 << index
        masks.append(mask)
    return tuple(masks)


def selected_indices(mask: int) -> Iterator[int]:
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def minimum_degree(mask: int, adjacency: Sequence[int]) -> int:
    return min((adjacency[index] & mask).bit_count() for index in selected_indices(mask))


def support_dimension(mask: int, cells: Sequence[Cell]) -> int:
    chosen = tuple(cells[index] for index in selected_indices(mask))
    return sum(len({cell[axis] for cell in chosen}) > 1 for axis in range(len(cells[0])))


def canonical_witness(sides: Sequence[int], mask: int, cells: Sequence[Cell]) -> bytes:
    chosen = [cells[index] for index in selected_indices(mask)]
    return json.dumps((tuple(sides), chosen), separators=(",", ":")).encode("ascii")


def audit_hosts(hosts: Sequence[Sequence[int]] = DEFAULT_HOSTS) -> dict[str, int | str]:
    totals = {
        "hosts": 0,
        "subsets": 0,
        "cores": 0,
        "three_coordinate_cores": 0,
        "near_extremal": 0,
        "equality": 0,
    }
    digest = hashlib.sha256()
    for sides in hosts:
        cells = vertices(sides)
        adjacency = neighbor_masks(cells)
        totals["hosts"] += 1
        for mask in range(1, 1 << len(cells)):
            totals["subsets"] += 1
            degree = minimum_degree(mask, adjacency)
            if degree < 2:
                continue
            totals["cores"] += 1
            size = mask.bit_count()
            dimension = support_dimension(mask, cells)
            if size <= 2 * degree + 1:
                totals["near_extremal"] += 1
                if dimension > 2:
                    raise AssertionError(
                        f"near-extremal counterexample in {tuple(sides)}: mask={mask}"
                    )
            if dimension >= 3:
                totals["three_coordinate_cores"] += 1
                if size < 2 * degree + 2:
                    raise AssertionError(
                        f"dimension-gap failure in {tuple(sides)}: mask={mask}"
                    )
                if size == 2 * degree + 2:
                    totals["equality"] += 1
                    digest.update(canonical_witness(sides, mask, cells) + b"\n")
    totals["digest"] = digest.hexdigest()
    return totals


def integer_partitions(total: int, cap: int, ceiling: int | None = None) -> Iterator[tuple[int, ...]]:
    if total == 0:
        yield ()
        return
    top = min(total, cap, total if ceiling is None else ceiling)
    for first in range(top, 0, -1):
        for tail in integer_partitions(total - first, cap, first):
            yield (first,) + tail


def feasible_shell_profiles(h: int) -> tuple[tuple[int, ...], ...]:
    profiles: list[tuple[int, ...]] = []
    for degree in range(h, 2 * h + 1):
        for profile in integer_partitions(degree, h - 1):
            doubled_lower_bound = 2 * (1 + degree) + sum(
                count * (h - count) for count in profile
            )
            if doubled_lower_bound <= 2 * (2 * h + 1):
                profiles.append(profile)
    return tuple(profiles)


def expected_profiles(h: int) -> set[tuple[int, ...]]:
    if h == 2:
        return {(1, 1)}
    if h == 3:
        return {(2, 1), (2, 2), (1, 1, 1)}
    if h == 4:
        return {(3, 1), (2, 2)}
    return {(h - 1, 1)}


def audit_profiles(max_h: int) -> dict[str, int | str]:
    tested = 0
    survivors = 0
    digest = hashlib.sha256()
    for h in range(2, max_h + 1):
        profiles = feasible_shell_profiles(h)
        if set(profiles) != expected_profiles(h):
            raise AssertionError(f"unexpected shell profiles for h={h}: {profiles}")
        tested += sum(
            1
            for degree in range(h, 2 * h + 1)
            for _ in integer_partitions(degree, h - 1)
        )
        survivors += len(profiles)
        digest.update(json.dumps((h, profiles), separators=(",", ":")).encode("ascii") + b"\n")
    return {"tested": tested, "survivors": survivors, "digest": digest.hexdigest()}


def mask_for(cells: Sequence[Cell], chosen: Sequence[Cell]) -> int:
    indices = {cell: index for index, cell in enumerate(cells)}
    return sum(1 << indices[cell] for cell in chosen)


def verify_boundary_examples() -> dict[str, int]:
    cube_cells = vertices((2, 2, 2))
    adjacency = neighbor_masks(cube_cells)
    six_cycle = tuple(cell for cell in cube_cells if cell not in ((0, 0, 0), (1, 1, 1)))
    cycle_mask = mask_for(cube_cells, six_cycle)
    cube_mask = (1 << len(cube_cells)) - 1
    if (cycle_mask.bit_count(), minimum_degree(cycle_mask, adjacency), support_dimension(cycle_mask, cube_cells)) != (6, 2, 3):
        raise AssertionError("six-cycle boundary example failed")
    if (cube_mask.bit_count(), minimum_degree(cube_mask, adjacency), support_dimension(cube_mask, cube_cells)) != (8, 3, 3):
        raise AssertionError("cube boundary example failed")

    grid_cells = vertices((3, 3))
    grid_adjacency = neighbor_masks(grid_cells)
    grid_mask = (1 << len(grid_cells)) - 1
    if (grid_mask.bit_count(), minimum_degree(grid_mask, grid_adjacency), support_dimension(grid_mask, grid_cells)) != (9, 4, 2):
        raise AssertionError("three-by-three grid control failed")
    return {"six_cycle": 6, "cube": 8, "grid": 9}


def audit_mutations() -> int:
    cells = vertices((2, 2, 2))
    adjacency = neighbor_masks(cells)
    chosen = tuple(cell for cell in cells if cell not in ((0, 0, 0), (1, 1, 1)))
    rejected = 0

    damaged = mask_for(cells, chosen[:-1])
    if minimum_degree(damaged, adjacency) < 2:
        rejected += 1

    flattened = tuple((x, y, 0) for x in range(2) for y in range(2))
    flat_mask = mask_for(cells, flattened)
    if support_dimension(flat_mask, cells) == 2:
        rejected += 1

    try:
        minimum_degree(0, adjacency)
    except ValueError:
        rejected += 1

    if rejected != 3:
        raise AssertionError("mutation/control audit failed")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-max-h", type=int, default=24)
    args = parser.parse_args()
    if args.profile_max_h < 5:
        parser.error("profile-max-h must be at least 5")

    host_stats = audit_hosts()
    profile_stats = audit_profiles(args.profile_max_h)
    examples = verify_boundary_examples()
    rejected = audit_mutations()

    print(f"Hamming hosts exhausted: {host_stats['hosts']}")
    print(f"nonempty subsets checked: {host_stats['subsets']}")
    print(f"minimum-degree-at-least-2 cores: {host_stats['cores']}")
    print(f"three-coordinate cores checked: {host_stats['three_coordinate_cores']}")
    print(f"near-extremal cores confined to two coordinates: {host_stats['near_extremal']}")
    print(f"dimension-gap equality witnesses: {host_stats['equality']}")
    print(f"equality-witness SHA-256: {host_stats['digest']}")
    print(f"shell profiles enumerated through h={args.profile_max_h}: {profile_stats['tested']}")
    print(f"shell profiles surviving the size bound: {profile_stats['survivors']}")
    print(f"shell-profile SHA-256: {profile_stats['digest']}")
    print(f"boundary example orders (cycle/cube/grid): {examples['six_cycle']}/{examples['cube']}/{examples['grid']}")
    print(f"mutations/controls rejected: {rejected}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
