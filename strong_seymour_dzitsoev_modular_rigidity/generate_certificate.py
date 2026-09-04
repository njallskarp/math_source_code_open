#!/usr/bin/env python3
"""Generate the compact certificate for Dzitsoev modular rigidity."""

from __future__ import annotations

import hashlib
import itertools
import json

QUOTIENT_ORDER = 6
QUOTIENT_MASK = 345
MINIMUM_SIZES = (11, 3, 3, 9, 3, 7)
PAIRS = tuple(
    (first, second)
    for first in range(QUOTIENT_ORDER)
    for second in range(first + 1, QUOTIENT_ORDER)
)


def quotient_rows(mask: int = QUOTIENT_MASK) -> tuple[int, ...]:
    rows = [0] * QUOTIENT_ORDER
    for bit, (first, second) in enumerate(PAIRS):
        source, target = (
            (first, second) if mask & (1 << bit) else (second, first)
        )
        rows[source] |= 1 << target
    return tuple(rows)


def is_module(rows: tuple[int, ...], subset: int) -> bool:
    full = (1 << len(rows)) - 1
    outside = full ^ subset
    for vertex in range(len(rows)):
        if outside & (1 << vertex):
            seen = rows[vertex] & subset
            if seen not in (0, subset):
                return False
    return True


def closure_trace(rows: tuple[int, ...], seed: int) -> tuple[int, ...]:
    """Close a set under outside vertices that distinguish two current vertices."""
    full = (1 << len(rows)) - 1
    current = seed
    trace = [current]
    while current != full:
        additions = 0
        for vertex in range(len(rows)):
            bit = 1 << vertex
            if current & bit:
                continue
            seen = rows[vertex] & current
            if seen not in (0, current):
                additions |= bit
        if not additions:
            break
        current |= additions
        trace.append(current)
    return tuple(trace)


def automorphisms(rows: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    order = len(rows)
    answer = []
    for permutation in itertools.permutations(range(order)):
        valid = True
        for source in range(order):
            for target in range(order):
                before = bool(rows[source] & (1 << target))
                after = bool(rows[permutation[source]] & (1 << permutation[target]))
                if before != after:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            answer.append(permutation)
    return tuple(answer)


def expand(
    quotient: tuple[int, ...], sizes: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    starts = []
    cursor = 0
    for size in sizes:
        starts.append(cursor)
        cursor += size
    fibers = tuple(
        sum(1 << vertex for vertex in range(start, start + size))
        for start, size in zip(starts, sizes)
    )
    rows = [0] * cursor
    for fiber_index, (start, size) in enumerate(zip(starts, sizes)):
        for position in range(size):
            vertex = start + position
            rows[vertex] |= sum(
                1 << later for later in range(vertex + 1, start + size)
            )
            for target_index, target_fiber in enumerate(fibers):
                if quotient[fiber_index] & (1 << target_index):
                    rows[vertex] |= target_fiber
    return tuple(rows), fibers


def hash_adjacency(rows: tuple[int, ...]) -> str:
    payload = "".join(
        f"{source}:" + ",".join(
            str(target)
            for target in range(len(rows))
            if row & (1 << target)
        ) + "\n"
        for source, row in enumerate(rows)
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def pair_closure_records(rows: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (first, second, closure_trace(rows, (1 << first) | (1 << second))[-1])
        for first in range(len(rows))
        for second in range(first + 1, len(rows))
    )


def hash_pair_closures(records: tuple[tuple[int, int, int], ...]) -> str:
    width = (max(record[2].bit_length() for record in records) + 3) // 4
    payload = "".join(
        f"{first},{second}:{closed:0{width}x}\n"
        for first, second, closed in records
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def interval_modules(fibers: tuple[int, ...]) -> tuple[int, ...]:
    answer = {0, sum(fibers)}
    for fiber in fibers:
        vertices = tuple(vertex for vertex in range(fiber.bit_length()) if fiber >> vertex & 1)
        for first in range(len(vertices)):
            current = 0
            for last in range(first, len(vertices)):
                current |= 1 << vertices[last]
                answer.add(current)
    return tuple(sorted(answer))


def hash_modules(modules: tuple[int, ...], order: int) -> str:
    width = (order + 3) // 4
    payload = "".join(f"{module:0{width}x}\n" for module in modules).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def maximal_proper_modules(modules: tuple[int, ...], full: int) -> tuple[int, ...]:
    proper = tuple(module for module in modules if module != full)
    return tuple(
        module
        for module in proper
        if module and not any(
            module != other and module & ~other == 0 for other in proper
        )
    )


def mask_string(mask: int, order: int) -> str:
    return "".join(str(vertex) for vertex in range(order) if mask >> vertex & 1)


def build_certificate() -> dict[str, object]:
    quotient = quotient_rows()
    full_quotient = (1 << QUOTIENT_ORDER) - 1
    nontrivial_modules = tuple(
        subset
        for subset in range(1, full_quotient)
        if subset.bit_count() >= 2 and is_module(quotient, subset)
    )
    if nontrivial_modules:
        raise AssertionError("Dzitsoev quotient is not prime")

    traces = {}
    for first, second in PAIRS:
        trace = closure_trace(quotient, (1 << first) | (1 << second))
        if trace[-1] != full_quotient:
            raise AssertionError("a quotient pair failed to force the whole quotient")
        traces[f"{first}{second}"] = [
            mask_string(subset, QUOTIENT_ORDER) for subset in trace
        ]

    quotient_automorphisms = automorphisms(quotient)
    if quotient_automorphisms != (tuple(range(QUOTIENT_ORDER)),):
        raise AssertionError("Dzitsoev quotient is not rigid")

    expanded, fibers = expand(quotient, MINIMUM_SIZES)
    order = len(expanded)
    full = (1 << order) - 1
    if any(not is_module(expanded, fiber) for fiber in fibers):
        raise AssertionError("a prescribed fiber is not a module")

    records = pair_closure_records(expanded)
    owner = {
        vertex: fiber_index
        for fiber_index, fiber in enumerate(fibers)
        for vertex in range(order)
        if fiber >> vertex & 1
    }
    cross = tuple(
        record for record in records if owner[record[0]] != owner[record[1]]
    )
    within = tuple(
        record for record in records if owner[record[0]] == owner[record[1]]
    )
    if any(closed != full for _, _, closed in cross):
        raise AssertionError("a cross-fiber pair has a proper module closure")
    for first, second, closed in within:
        interval = sum(1 << vertex for vertex in range(first, second + 1))
        if closed != interval:
            raise AssertionError("same-fiber pair closure is not its transitive interval")

    modules = interval_modules(fibers)
    if any(not is_module(expanded, module) for module in modules):
        raise AssertionError("the claimed module family contains a nonmodule")
    maximal = maximal_proper_modules(modules, full)
    if maximal != fibers:
        raise AssertionError("the maximal proper modules are not exactly the fibers")

    return {
        "canonical_quotient_mask": QUOTIENT_MASK,
        "expanded_adjacency_sha256": hash_adjacency(expanded),
        "expanded_order": order,
        "expanded_pair_closure_sha256": hash_pair_closures(records),
        "fiber_sizes": list(MINIMUM_SIZES),
        "maximal_proper_modules_hex": [f"{fiber:09x}" for fiber in fibers],
        "module_count_including_empty_and_full": len(modules),
        "module_family_sha256": hash_modules(modules, order),
        "pair_counts": {
            "cross_fiber_forcing_full": len(cross),
            "same_fiber_forcing_interval": len(within),
            "total": len(records),
        },
        "quotient_automorphism_count": len(quotient_automorphisms),
        "quotient_pair_closure_traces": traces,
        "schema": "strong-seymour-dzitsoev-modular-rigidity-v1",
    }


def main() -> None:
    print(json.dumps(build_certificate(), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
