#!/usr/bin/env python3
"""Exact checker for the S_13 Poonen dual and its one-block repair obstruction.

All sets on [9] are encoded by 9-bit integers.  This checker uses only Python
integer and set operations; it does not trust the solver used during discovery.
"""

from __future__ import annotations

import hashlib
import itertools
import json


N = 9
FULL = (1 << N) - 1

# Multipliers for B_0,...,B_11 below.  Their weighted frequency-row sum is
# strictly negative in every coordinate.
FARKAS = (50, 50, 3, 3, 72, 25, 25, 1, 1, 118, 1025, 118)
EXPECTED_AGGREGATE = (-2, -2, -12, -12, -6, -6, -6, -2, -2)

# The only opaque member of the compact dual.  The other eleven witness
# families are generated from short rules in build_witnesses().
OPAQUE_B = (
    0, 4, 7, 8, 11, 12, 15, 16, 20, 23, 24, 27, 28, 31, 32, 36, 39, 40,
    43, 44, 47, 48, 51, 52, 55, 56, 59, 60, 63, 64, 68, 71, 72, 75, 76,
    79, 80, 83, 84, 87, 88, 91, 92, 95, 96, 100, 103, 104, 107, 108,
    111, 112, 115, 116, 119, 120, 123, 124, 127, 128, 132, 135, 136,
    139, 140, 143, 144, 148, 151, 152, 155, 156, 159, 160, 164, 167,
    168, 171, 172, 175, 176, 179, 180, 183, 184, 187, 188, 191, 192,
    196, 199, 200, 203, 204, 207, 208, 211, 212, 215, 216, 219, 220,
    223, 224, 228, 231, 232, 235, 236, 239, 240, 243, 244, 247, 248,
    251, 252, 255, 256, 260, 263, 264, 267, 268, 271, 272, 276, 279,
    280, 283, 284, 287, 288, 292, 295, 296, 299, 300, 303, 304, 307,
    308, 311, 312, 315, 316, 319, 320, 324, 327, 328, 331, 332, 335,
    336, 339, 340, 343, 344, 347, 348, 351, 352, 356, 359, 360, 363,
    364, 367, 368, 371, 372, 375, 376, 379, 380, 383, 384, 388, 391,
    392, 395, 396, 399, 400, 404, 407, 408, 411, 412, 415, 416, 420,
    423, 424, 427, 428, 431, 432, 435, 436, 439, 440, 443, 444, 447,
    448, 452, 455, 456, 459, 460, 463, 464, 467, 468, 471, 472, 475,
    476, 479, 480, 484, 487, 488, 491, 492, 495, 496, 499, 500, 503,
    504, 507, 508, 511,
)

# For each orbit representative g, one weight satisfying every inequality of
# the canonically repaired dual B -> B union {S union g : S in B}.
REPAIR_WEIGHTS = {
    29: (4, 3, 3, 3, 2, 0, 0, 0, 1),
    45: (4, 3, 3, 3, 0, 2, 1, 0, 0),
    53: (6, 6, 4, 4, 5, 5, 2, 0, 0),
    60: (1, 1, 1, 1, 1, 1, 0, 0, 0),
    99: (3, 3, 2, 2, 2, 2, 2, 0, 0),
    101: (3, 3, 2, 2, 2, 2, 2, 0, 0),
    108: (1, 1, 1, 1, 0, 1, 1, 0, 0),
    113: (3, 3, 2, 2, 2, 2, 2, 0, 0),
    116: (1, 1, 1, 0, 1, 1, 1, 0, 0),
    141: (4, 3, 3, 3, 1, 0, 0, 2, 0),
    147: (6, 6, 4, 4, 4, 3, 3, 2, 0),
    149: (4, 3, 3, 2, 2, 2, 2, 2, 0),
    156: (1, 1, 1, 1, 1, 0, 0, 1, 0),
    163: (6, 6, 4, 4, 2, 3, 3, 3, 1),
    165: (7, 6, 5, 1, 4, 5, 2, 1, 1),
    172: (1, 1, 1, 1, 0, 1, 0, 1, 0),
    177: (7, 6, 3, 3, 3, 5, 1, 4, 0),
    180: (2, 2, 2, 1, 2, 2, 1, 1, 1),
    225: (3, 3, 2, 2, 2, 2, 2, 0, 0),
    228: (3, 3, 2, 2, 2, 2, 2, 0, 0),
    240: (3, 3, 2, 2, 2, 2, 2, 0, 0),
    387: (6, 6, 4, 4, 2, 3, 1, 3, 3),
    389: (5, 5, 4, 3, 3, 3, 2, 2, 2),
    396: (1, 1, 1, 1, 0, 0, 0, 1, 1),
    401: (6, 5, 0, 3, 4, 3, 0, 4, 4),
    404: (3, 3, 3, 2, 3, 2, 2, 2, 2),
    417: (6, 5, 3, 0, 2, 4, 3, 4, 3),
    420: (5, 5, 4, 3, 3, 4, 2, 1, 2),
    432: (6, 6, 4, 4, 5, 2, 3, 4, 4),
    480: (3, 3, 2, 2, 2, 2, 2, 0, 0),
}


def mask(items: tuple[int, ...]) -> int:
    return sum(1 << (item - 1) for item in items)


def lex_blocks() -> tuple[int, ...]:
    return tuple(mask(block) for block in itertools.combinations(range(1, N + 1), 4))


def union_closure(generators: tuple[int, ...] | set[int]) -> set[int]:
    closure = {0}
    for generator in generators:
        closure |= {member | generator for member in tuple(closure)}
    return closure


def special_family(closure: set[int], omitted: int) -> set[int]:
    base = tuple(member for member in range(1 << N) if not member & (1 << omitted))
    return {a | b for a in closure for b in base}


def build_witnesses(a_closure: set[int]) -> tuple[frozenset[int], ...]:
    witnesses = [frozenset(special_family(a_closure, omitted)) for omitted in range(N)]
    # B_9: if element 4 occurs, then both core elements 1 and 2 occur.
    witnesses.append(frozenset(member for member in range(1 << N) if not member & 8 or member & 3 == 3))
    witnesses.append(frozenset(OPAQUE_B))
    # B_11: the element-3 analogue of B_9.
    witnesses.append(frozenset(member for member in range(1 << N) if not member & 4 or member & 3 == 3))
    return tuple(witnesses)


def frequency_row(family: frozenset[int] | set[int]) -> tuple[int, ...]:
    size = len(family)
    return tuple(2 * sum(bool(member & (1 << i)) for member in family) - size for i in range(N))


def is_union_closed(family: frozenset[int] | set[int]) -> bool:
    return all(left | right in family for left in family for right in family)


def is_stable(family: frozenset[int] | set[int], closure: set[int]) -> bool:
    return all(member | generator in family for member in family for generator in closure)


def permute_mask(member: int, permutation: tuple[int, ...]) -> int:
    return sum(1 << permutation[i] for i in range(N) if member & (1 << i))


def subgroup() -> tuple[tuple[int, ...], ...]:
    swaps = ((0, 1), (2, 3), (5, 6), (7, 8))
    permutations = []
    for choices in itertools.product((False, True), repeat=len(swaps)):
        permutation = list(range(N))
        for chosen, (left, right) in zip(choices, swaps):
            if chosen:
                permutation[left], permutation[right] = permutation[right], permutation[left]
        permutations.append(tuple(permutation))
    return tuple(permutations)


def permute_weights(weights: tuple[int, ...], permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * N
    for old, new in enumerate(permutation):
        result[new] = weights[old]
    return tuple(result)


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right))


def main() -> None:
    a = lex_blocks()[:13]
    assert len(a) == len(set(a)) == 13
    assert all(member.bit_count() == 4 for member in a)
    assert __import__("functools").reduce(int.__or__, a) == FULL
    a_closure = union_closure(a)
    witnesses = build_witnesses(a_closure)
    assert len(witnesses) == len(set(witnesses)) == 12
    assert all(is_union_closed(family) for family in witnesses)
    assert all(is_stable(family, a_closure) for family in witnesses)

    rows = tuple(frequency_row(family) for family in witnesses)
    aggregate = tuple(sum(FARKAS[j] * rows[j][i] for j in range(len(rows))) for i in range(N))
    assert aggregate == EXPECTED_AGGREGATE
    assert all(multiplier >= 0 for multiplier in FARKAS)
    assert all(entry < 0 for entry in aggregate)

    permutations = subgroup()
    assert len(permutations) == 16
    a_set = set(a)
    witness_set = set(witnesses)
    assert all({permute_mask(member, permutation) for member in a} == a_set for permutation in permutations)
    assert all(
        frozenset(permute_mask(member, permutation) for member in family) in witness_set
        for permutation in permutations
        for family in witnesses
    )

    remaining = set(lex_blocks()) - a_set
    assert len(remaining) == 113
    orbit_map: dict[int, tuple[int, tuple[int, ...]]] = {}
    while remaining:
        representative = min(remaining)
        orbit = {permute_mask(representative, permutation) for permutation in permutations} - a_set
        for member in orbit:
            choices = [permutation for permutation in permutations if permute_mask(representative, permutation) == member]
            assert choices
            orbit_map[member] = (representative, choices[0])
        remaining -= orbit
    assert set(REPAIR_WEIGHTS) == {representative for representative, _ in orbit_map.values()}
    assert len(REPAIR_WEIGHTS) == 30
    assert len(orbit_map) == 113

    lost_counts = []
    repair_checks = 0
    for added, (representative, permutation) in sorted(orbit_map.items()):
        lost = sum(any(member | added not in family for member in family) for family in witnesses)
        lost_counts.append(lost)
        weights = permute_weights(REPAIR_WEIGHTS[representative], permutation)
        assert any(weights) and all(weight >= 0 for weight in weights)
        extended_closure = union_closure(set(a) | {added})
        for family in witnesses:
            repaired = frozenset(set(family) | {member | added for member in family})
            # The closure lemma in README proves union closure; the following
            # direct check covers stability under the entire extended closure.
            assert is_stable(repaired, extended_closure)
            assert dot(frequency_row(repaired), weights) >= 0
            repair_checks += 1
    assert min(lost_counts) == 4

    certificate = {
        "A": list(a),
        "witnesses": [sorted(family) for family in witnesses],
        "farkas": list(FARKAS),
        "aggregate": list(aggregate),
        "repair_weights": {str(key): list(value) for key, value in sorted(REPAIR_WEIGHTS.items())},
    }
    canonical = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    print(f"PASS base_non_fc witnesses={len(witnesses)} aggregate={list(aggregate)}")
    print(
        "PASS transition_obstruction "
        f"added_blocks={len(orbit_map)} subgroup_orbits={len(REPAIR_WEIGHTS)} "
        f"min_destabilized={min(lost_counts)} repair_checks={repair_checks}"
    )
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
