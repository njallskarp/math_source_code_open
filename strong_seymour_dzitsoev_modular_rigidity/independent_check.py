#!/usr/bin/env python3
"""Independent set-based audit in the Bai--Li--Park/Dzitsoev labeling."""

from __future__ import annotations

import hashlib
import itertools
import json

# Published labeling from Bai--Li--Park, Remark 3.1.
PUBLISHED_OUT = (
    frozenset((1, 4, 5)),
    frozenset((3, 4, 5)),
    frozenset((0, 1, 3)),
    frozenset((0, 4)),
    frozenset((2, 5)),
    frozenset((2, 3)),
)
PUBLISHED_SIZES = (7, 3, 11, 3, 9, 3)
PUBLISHED_TO_CANONICAL = (5, 4, 0, 1, 3, 2)


def module(arcs: tuple[frozenset[int], ...], chosen: frozenset[int]) -> bool:
    for vertex in set(range(len(arcs))).difference(chosen):
        seen = arcs[vertex].intersection(chosen)
        if seen and seen != chosen:
            return False
    return True


def pair_hull(
    arcs: tuple[frozenset[int], ...], first: int, second: int
) -> frozenset[int]:
    chosen = {first, second}
    while True:
        additions = {
            vertex
            for vertex in range(len(arcs))
            if vertex not in chosen
            and 0 < len(arcs[vertex].intersection(chosen)) < len(chosen)
        }
        if not additions:
            return frozenset(chosen)
        chosen.update(additions)


def expand() -> tuple[tuple[frozenset[int], ...], tuple[tuple[int, ...], ...]]:
    fibers = []
    cursor = 0
    for size in PUBLISHED_SIZES:
        fibers.append(tuple(range(cursor, cursor + size)))
        cursor += size
    arcs = [set() for _ in range(cursor)]
    for fiber_index, fiber in enumerate(fibers):
        for position, source in enumerate(fiber):
            arcs[source].update(fiber[position + 1 :])
            for target_index in PUBLISHED_OUT[fiber_index]:
                arcs[source].update(fibers[target_index])
    return tuple(frozenset(row) for row in arcs), tuple(fibers)


def canonical_vertex_map(fibers: tuple[tuple[int, ...], ...]) -> dict[int, int]:
    canonical_sizes = [0] * len(fibers)
    for old, new in enumerate(PUBLISHED_TO_CANONICAL):
        canonical_sizes[new] = len(fibers[old])
    starts = []
    cursor = 0
    for size in canonical_sizes:
        starts.append(cursor)
        cursor += size
    return {
        old_vertex: starts[PUBLISHED_TO_CANONICAL[old_fiber]] + position
        for old_fiber, fiber in enumerate(fibers)
        for position, old_vertex in enumerate(fiber)
    }


def canonical_adjacency_hash(
    arcs: tuple[frozenset[int], ...], mapping: dict[int, int]
) -> str:
    rows = [set() for _ in arcs]
    for source, targets in enumerate(arcs):
        rows[mapping[source]].update(mapping[target] for target in targets)
    payload = "".join(
        f"{source}:" + ",".join(map(str, sorted(targets))) + "\n"
        for source, targets in enumerate(rows)
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def canonical_pair_hash(
    arcs: tuple[frozenset[int], ...], mapping: dict[int, int]
) -> str:
    inverse = {new: old for old, new in mapping.items()}
    width = (len(arcs) + 3) // 4
    lines = []
    for first in range(len(arcs)):
        for second in range(first + 1, len(arcs)):
            old_hull = pair_hull(arcs, inverse[first], inverse[second])
            mask = sum(1 << mapping[vertex] for vertex in old_hull)
            lines.append(f"{first},{second}:{mask:0{width}x}\n")
    return hashlib.sha256("".join(lines).encode("ascii")).hexdigest()


def main() -> None:
    quotient_modules = []
    for size in range(2, 6):
        for chosen in itertools.combinations(range(6), size):
            if module(PUBLISHED_OUT, frozenset(chosen)):
                quotient_modules.append(chosen)
    if quotient_modules:
        raise AssertionError("published quotient has a nontrivial module")

    automorphisms = []
    for permutation in itertools.permutations(range(6)):
        if all(
            ((target in PUBLISHED_OUT[source]) ==
             (permutation[target] in PUBLISHED_OUT[permutation[source]]))
            for source in range(6)
            for target in range(6)
        ):
            automorphisms.append(permutation)
    if automorphisms != [tuple(range(6))]:
        raise AssertionError("published quotient has a nonidentity automorphism")

    arcs, fibers = expand()
    owner = {
        vertex: fiber_index
        for fiber_index, fiber in enumerate(fibers)
        for vertex in fiber
    }
    full = frozenset(range(len(arcs)))
    cross = within = 0
    for first, second in itertools.combinations(range(len(arcs)), 2):
        hull = pair_hull(arcs, first, second)
        if owner[first] != owner[second]:
            cross += 1
            if hull != full:
                raise AssertionError("cross-fiber pair has a proper homogeneous hull")
        else:
            within += 1
            fiber = fibers[owner[first]]
            lo, hi = fiber.index(first), fiber.index(second)
            if hull != frozenset(fiber[lo : hi + 1]):
                raise AssertionError("within-fiber hull is not an interval")

    proper_modules = set()
    for fiber in fibers:
        for bits in range(1, 1 << len(fiber)):
            chosen = frozenset(
                fiber[position]
                for position in range(len(fiber))
                if bits & (1 << position)
            )
            if module(arcs, chosen):
                proper_modules.add(chosen)
    modules = proper_modules | {frozenset(), full}
    if len(modules) != 159 or any(not module(arcs, chosen) for chosen in modules):
        raise AssertionError("unexpected homogeneous-set family")
    maximal = tuple(
        chosen
        for chosen in proper_modules
        if not any(chosen < other for other in proper_modules)
    )
    if {frozenset(fiber) for fiber in fibers} != set(maximal):
        raise AssertionError("maximal proper modules are not the six fibers")

    mapping = canonical_vertex_map(fibers)
    canonical_modules = sorted(
        sum(1 << mapping[vertex] for vertex in chosen) for chosen in modules
    )
    width = (len(arcs) + 3) // 4
    module_payload = "".join(
        f"{chosen:0{width}x}\n" for chosen in canonical_modules
    ).encode("ascii")
    print(json.dumps({
        "canonical_adjacency_sha256": canonical_adjacency_hash(arcs, mapping),
        "canonical_module_family_sha256": hashlib.sha256(module_payload).hexdigest(),
        "canonical_pair_closure_sha256": canonical_pair_hash(arcs, mapping),
        "cross_pair_closures_full": cross,
        "maximal_proper_modules": len(maximal),
        "modules_including_empty_and_full": len(modules),
        "quotient_automorphisms": len(automorphisms),
        "quotient_nontrivial_modules": len(quotient_modules),
        "same_fiber_pair_closures_interval": within,
        "status": "INDEPENDENT DZITSOEV MODULAR AUDIT VERIFIED",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
