#!/usr/bin/env python3
"""Clean-room checks for the modular residue-slab Hamming construction.

CPython 3.12+, standard library only.  This file intentionally imports no
researcher code.  Small rectangle bases are found by exact-cover search rather
than by the target's cyclic rectangle construction.
"""

from __future__ import annotations

import itertools
import math
import sys
from functools import lru_cache
from typing import Iterable, Sequence


Cell = tuple[int, ...]
Part = tuple[Cell, ...]


def is_coordinate_line(part: Sequence[Cell]) -> bool:
    """Return whether every cell in a nonempty part varies in at most one axis."""
    if not part:
        return False
    dimension = len(part[0])
    if any(len(cell) != dimension for cell in part):
        return False
    return any(
        all(
            all(cell[j] == part[0][j] for j in range(dimension) if j != axis)
            for cell in part
        )
        for axis in range(dimension)
    )


def verify_partition(dimensions: Sequence[int], parts: Sequence[Part], s: int) -> None:
    expected = set(itertools.product(*(range(side) for side in dimensions)))
    seen: set[Cell] = set()
    for part in parts:
        assert len(part) >= s
        assert len(set(part)) == len(part)
        assert is_coordinate_line(part)
        assert seen.isdisjoint(part)
        seen.update(part)
    assert seen == expected
    assert len(parts) == math.prod(dimensions) // s


def exact_cover_rectangle(m: int, n: int, s: int) -> tuple[list[Part], int]:
    """Find an optimal line partition by definition-level exact-cover search.

    If q=floor(m*n/s) parts cover the rectangle, their total excess over s is
    r=(m*n) mod s.  Hence it suffices to generate row/column subsets of sizes
    s,...,s+r.  The search is deliberately limited to small audit instances.
    """
    if s < 2 or m < s or n < s:
        raise ValueError("require m,n >= s >= 2")
    volume = m * n
    quotient, remainder = divmod(volume, s)
    candidates: list[tuple[int, Part]] = []
    by_cell: list[list[int]] = [[] for _ in range(volume)]

    def add(part: Part) -> None:
        mask = sum(1 << (row * n + column) for row, column in part)
        index = len(candidates)
        candidates.append((mask, part))
        for row, column in part:
            by_cell[row * n + column].append(index)

    maximum_size = s + remainder
    for row in range(m):
        for size in range(s, min(n, maximum_size) + 1):
            for columns in itertools.combinations(range(n), size):
                add(tuple((row, column) for column in columns))
    for column in range(n):
        for size in range(s, min(m, maximum_size) + 1):
            for rows in itertools.combinations(range(m), size):
                add(tuple((row, column) for row in rows))

    full_mask = (1 << volume) - 1
    nodes = 0

    @lru_cache(maxsize=None)
    def search(covered: int, used: int) -> tuple[int, ...] | None:
        nonlocal nodes
        nodes += 1
        parts_left = quotient - used
        cells_left = volume - covered.bit_count()
        if parts_left == 0:
            return () if covered == full_mask else None
        if cells_left < parts_left * s or cells_left > parts_left * maximum_size:
            return None

        uncovered = [i for i in range(volume) if not (covered >> i) & 1]
        pivot = min(
            uncovered,
            key=lambda cell: sum(
                1 for candidate in by_cell[cell] if not (candidates[candidate][0] & covered)
            ),
        )
        viable = [
            candidate
            for candidate in by_cell[pivot]
            if not (candidates[candidate][0] & covered)
        ]
        viable.sort(key=lambda candidate: (-len(candidates[candidate][1]), candidate))
        for candidate in viable:
            mask, _ = candidates[candidate]
            suffix = search(covered | mask, used + 1)
            if suffix is not None:
                return (candidate,) + suffix
        return None

    witness = search(0, 0)
    if witness is None:
        raise AssertionError(f"no exact cover found for {(m, n, s)}")
    parts = [candidates[index][1] for index in witness]
    verify_partition((m, n), parts, s)
    return parts, nodes


def residue_slab_extend(
    base_parts: Sequence[Part], base_dimensions: Sequence[int], p: int, s: int
) -> list[Part]:
    """Apply the claimed composition to an independently supplied base cover."""
    volume = math.prod(base_dimensions)
    quotient, tau = divmod(volume, s)
    slabs, c = divmod(p, s)
    if len(base_parts) != quotient:
        raise ValueError("base part count is not optimal")
    if c * tau >= s:
        raise ValueError("residue-slab criterion fails")

    result: list[Part] = []
    for cell in itertools.product(*(range(side) for side in base_dimensions)):
        for slab in range(slabs):
            result.append(tuple(cell + (z,) for z in range(slab * s, (slab + 1) * s)))
    for z in range(slabs * s, p):
        result.extend(tuple(cell + (z,) for cell in part) for part in base_parts)
    return result


def audit_composition_arithmetic(max_s: int, max_volume: int, max_p: int) -> int:
    """Check the exact deficit formula for the prescribed composition scheme."""
    checked = 0
    for s in range(2, max_s + 1):
        for volume in range(1, max_volume + 1):
            quotient, tau = divmod(volume, s)
            for p in range(1, max_p + 1):
                slabs, c = divmod(p, s)
                constructed = slabs * volume + c * quotient
                deficit = (volume * p) // s - constructed
                assert deficit == (c * tau) // s
                assert (deficit == 0) == (c * tau < s)
                checked += 1
    return checked


def audit_small_exact_covers() -> tuple[int, int, int]:
    """Use clean-room base covers to check old-failing/new-passing examples."""
    cases = ((2, 2, 1, 2), (3, 3, 3, 2), (4, 5, 4, 3), (5, 6, 5, 4))
    nodes = 0
    cells = 0
    for m, n, p, s in cases:
        base, case_nodes = exact_cover_rectangle(m, n, s)
        nodes += case_nodes
        extended = residue_slab_extend(base, (m, n), p, s)
        verify_partition((m, n, p), extended, s)
        cells += m * n * p
        tau = (m * n) % s
        assert (p % s) * tau < s
        if (m, n, p, s) != cases[0]:
            assert p * tau >= s
    return len(cases), nodes, cells


def shell_bound_profiles(max_side: int) -> tuple[int, int]:
    """Directly enumerate capped first-shell profiles for the cited upper bound."""
    parameters = 0
    profiles = 0
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    caps = (n1 - 1, n2 - 1, n3 - 1, n4 - 1)
                    h = (sum(caps) + 1) // 2
                    if h < caps[0]:
                        continue
                    s = h - caps[0] + 1
                    if s < 2:
                        continue
                    parameters += 1
                    target_twice = 2 * n1 * s
                    for profile in itertools.product(*(range(cap + 1) for cap in caps)):
                        total = sum(profile)
                        if total < h:
                            continue
                        lower_bound_twice = 2 * (1 + total) + sum(
                            value * (h - value) for value in profile
                        )
                        assert lower_bound_twice >= target_twice
                        profiles += 1
    return parameters, profiles


def prior_criteria(sides: Sequence[int], s: int) -> tuple[bool, bool, bool, bool]:
    residues = tuple(side % s for side in sides)
    residue_product = math.prod(residues)
    divisibility = any(residue == 0 for residue in residues)
    mixed_radix = residue_product < s
    one_box = s <= residue_product < 2 * s and sum(residues) >= s + 2
    cubic_exception = s == 3 and residues == (2, 2, 2)
    return divisibility, mixed_radix, one_box, cubic_exception


def has_residue_slab_order(sides: Sequence[int], s: int) -> bool:
    for first, second in itertools.combinations(range(3), 2):
        remaining = 3 - first - second
        if sides[first] < s or sides[second] < s:
            continue
        if (sides[remaining] % s) * ((sides[first] * sides[second]) % s) < s:
            return True
    return False


def has_old_layer_order(sides: Sequence[int], s: int) -> bool:
    for first, second in itertools.combinations(range(3), 2):
        remaining = 3 - first - second
        if sides[first] < s or sides[second] < s:
            continue
        if sides[remaining] * ((sides[first] * sides[second]) % s) < s:
            return True
    return False


def smallest_new_hamming_cases(max_side: int) -> tuple[tuple[tuple[int, ...], int, int], ...]:
    witnesses: list[tuple[tuple[int, ...], int, int]] = []
    for n1 in range(2, max_side + 1):
        for n2 in range(2, n1 + 1):
            for n3 in range(2, n2 + 1):
                for n4 in range(2, n3 + 1):
                    orders = (n1, n2, n3, n4)
                    deficits = tuple(order - 1 for order in orders)
                    h = (sum(deficits) + 1) // 2
                    if h < deficits[0]:
                        continue
                    s = h - deficits[0] + 1
                    sides = orders[1:]
                    if not has_residue_slab_order(sides, s) or has_old_layer_order(sides, s):
                        continue
                    if any(prior_criteria(sides, s)):
                        continue
                    witnesses.append((orders, s, math.prod(sides) // s))
    witnesses.sort(key=lambda item: (max(item[0]), item[0]))
    minimum = max(witnesses[0][0])
    return tuple(witness for witness in witnesses if max(witness[0]) == minimum)


def audit_infinite_family(max_k: int) -> int:
    for k in range(2, max_k + 1):
        orders = (3 * k + 6, 3 * k + 2, 2 * k + 3, 2 * k + 3)
        deficits = tuple(order - 1 for order in orders)
        h = (sum(deficits) + 1) // 2
        s = h - deficits[0] + 1
        assert h == 5 * k + 5 and s == 2 * k + 1
        assert tuple(side % s for side in orders[1:]) == (k + 1, 2, 2)
        assert has_residue_slab_order(orders[1:], s)
        assert not has_old_layer_order(orders[1:], s)
        assert not any(prior_criteria(orders[1:], s))
        quotient = 6 * k * k + 19 * k + 16
        assert math.prod(orders[1:]) == s * quotient + 2
    return max_k - 1


def main() -> None:
    arithmetic = audit_composition_arithmetic(64, 512, 512)
    covers, search_nodes, cells = audit_small_exact_covers()
    shell_parameters, shell_profiles = shell_bound_profiles(14)
    witnesses = smallest_new_hamming_cases(12)
    family = audit_infinite_family(100_000)

    print(f"python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"composition arithmetic triples checked: {arithmetic}")
    print(f"clean-room exact-cover bases and extensions: {covers}")
    print(f"exact-cover search states visited: {search_nodes}")
    print(f"cells in explicit extended covers: {cells}")
    print(f"near-triangle parameter quadruples checked: {shell_parameters}")
    print(f"feasible first-shell profiles checked: {shell_profiles}")
    for orders, s, quotient in witnesses:
        print(f"smallest new Hamming case: orders={orders}, s={s}, quotient={quotient}")
    print(f"explicit-family indices checked: {family}")
    print("all independent checks passed")


if __name__ == "__main__":
    main()
