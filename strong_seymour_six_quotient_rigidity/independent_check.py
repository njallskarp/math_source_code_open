#!/usr/bin/env python3
"""Independent replay of the six-quotient multicover certificate."""

from __future__ import annotations

import base64
import hashlib
import itertools
import json
from math import prod
from pathlib import Path

ORDER = 6
PAIRS = tuple((i, j) for i in range(ORDER) for j in range(i + 1, ORDER))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
FEASIBLE_CODE = 0xFFFF
CERTIFICATE_PATH = Path(__file__).with_name("certificate.json")


def adjacency(mask: int) -> tuple[tuple[bool, ...], ...]:
    matrix = [[False] * ORDER for _ in range(ORDER)]
    for bit, (first, second) in enumerate(PAIRS):
        source, target = (first, second) if mask & (1 << bit) else (second, first)
        matrix[source][target] = True
    return tuple(tuple(row) for row in matrix)


def relabel(mask: int, permutation: tuple[int, ...]) -> int:
    old = adjacency(mask)
    new = [[False] * ORDER for _ in range(ORDER)]
    for source in range(ORDER):
        for target in range(ORDER):
            if old[source][target]:
                new[permutation[source]][permutation[target]] = True
    answer = 0
    for bit, (first, second) in enumerate(PAIRS):
        if new[first][second]:
            answer |= 1 << bit
    return answer


def validate_orbit_partition(representatives: tuple[int, ...]) -> None:
    covered: set[int] = set()
    permutations = tuple(itertools.permutations(range(ORDER)))
    for representative in representatives:
        orbit = {relabel(representative, permutation) for permutation in permutations}
        if representative != min(orbit) or covered & orbit:
            raise AssertionError("invalid canonical tournament orbit")
        covered.update(orbit)
    if covered != set(range(1 << len(PAIRS))):
        raise AssertionError("the quotient list does not cover all labeled tournaments")


def bitmask(vertices: tuple[int, ...] | list[int] | set[int]) -> int:
    return sum(1 << vertex for vertex in vertices)


def closed_options(
    arcs: tuple[tuple[bool, ...], ...], root: int
) -> tuple[tuple[int, int, tuple[int, ...]], ...]:
    first = tuple(vertex for vertex in range(ORDER) if arcs[root][vertex])
    second = tuple(
        vertex
        for vertex in range(ORDER)
        if vertex != root
        and not arcs[root][vertex]
        and any(arcs[root][middle] and arcs[middle][vertex] for middle in range(ORDER))
    )
    answer = []
    for count in range(1, len(first) + 1):
        for chosen_tuple in itertools.combinations(first, count):
            chosen = set(chosen_tuple)
            neighbors = {
                target
                for target in second
                if any(arcs[source][target] for source in chosen)
            }
            closure = {
                source
                for source in first
                if all(not arcs[source][target] or target in neighbors for target in second)
            }
            if closure != chosen:
                continue
            row = tuple(
                int(vertex in chosen) - int(vertex in neighbors)
                for vertex in range(ORDER)
            )
            answer.append((bitmask(chosen), bitmask(neighbors), row))
    answer.sort()
    return tuple(answer)


def decode_coefficients(code: int) -> tuple[int, ...]:
    if not 0 < code < (1 << (2 * ORDER)):
        raise AssertionError("invalid multicover code")
    return tuple((code >> (2 * root)) & 3 for root in range(ORDER))


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    total = 0
    for permutation in itertools.permutations(range(ORDER)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(ORDER)
            for j in range(i + 1, ORDER)
        )
        term = prod(matrix[row][permutation[row]] for row in range(ORDER))
        total += -term if inversions % 2 else term
    return total


def verify_feasible_entry(
    entry: dict[str, object],
    choices: tuple[int, ...],
    options: tuple[tuple[tuple[int, int, tuple[int, ...]], ...], ...],
) -> None:
    matrix = tuple(options[root][choices[root]][2] for root in range(ORDER))
    source_masks = [options[root][choices[root]][0] for root in range(ORDER)]
    neighbor_masks = [options[root][choices[root]][1] for root in range(ORDER)]
    weights = tuple(int(value) for value in entry["weights"])
    dual = tuple(int(value) for value in entry["dual"])
    if (
        list(choices) != entry["choices"]
        or source_masks != entry["source_masks"]
        or neighbor_masks != entry["neighbor_masks"]
        or determinant(matrix) != -1
        or min(weights + dual) <= 0
        or sum(weights) != entry["total"]
    ):
        raise AssertionError("malformed feasible-chamber certificate")
    if any(
        sum(matrix[root][column] * weights[column] for column in range(ORDER)) != 1
        for root in range(ORDER)
    ):
        raise AssertionError("primal chamber witness does not have unit defects")
    if any(
        sum(matrix[root][column] * dual[root] for root in range(ORDER)) != 1
        for column in range(ORDER)
    ):
        raise AssertionError("dual multipliers do not sum the rows to all-ones")
    if sum(dual) != sum(weights):
        raise AssertionError("primal and dual objectives differ")


def expanded_tournament(mask: int, sizes: tuple[int, ...]) -> tuple[frozenset[int], ...]:
    quotient = adjacency(mask)
    clusters = []
    next_vertex = 0
    for size in sizes:
        cluster = tuple(range(next_vertex, next_vertex + size))
        clusters.append(cluster)
        next_vertex += size
    arcs = [set() for _ in range(next_vertex)]
    for cluster in clusters:
        for position, source in enumerate(cluster):
            arcs[source].update(cluster[position + 1 :])
    for source_cluster in range(ORDER):
        for target_cluster in range(ORDER):
            if quotient[source_cluster][target_cluster]:
                for source in clusters[source_cluster]:
                    arcs[source].update(clusters[target_cluster])
    return tuple(frozenset(row) for row in arcs)


def has_covering_matching(
    arcs: tuple[frozenset[int], ...], left: frozenset[int], right: frozenset[int]
) -> bool:
    matched: dict[int, int] = {}

    def augment(source: int, seen: set[int]) -> bool:
        for target in sorted(arcs[source] & right):
            if target in seen:
                continue
            seen.add(target)
            if target not in matched or augment(matched[target], seen):
                matched[target] = source
                return True
        return False

    return all(augment(source, set()) for source in sorted(left))


def strong_vertices(arcs: tuple[frozenset[int], ...]) -> tuple[int, ...]:
    answer = []
    for vertex, first in enumerate(arcs):
        reached = set().union(*(arcs[head] for head in first)) if first else set()
        second = frozenset(reached.difference(first, {vertex}))
        if has_covering_matching(arcs, first, second):
            answer.append(vertex)
    return tuple(answer)


def main() -> None:
    raw = CERTIFICATE_PATH.read_bytes()
    certificate = json.loads(raw)
    quotient_entries = certificate["quotients"]
    representatives = tuple(int(entry["mask"]) for entry in quotient_entries)
    validate_orbit_partition(representatives)

    feasible_lookup = {
        (int(entry["mask"]), tuple(entry["choices"])): entry
        for entry in certificate["feasible"]
    }
    used_feasible: set[tuple[int, tuple[int, ...]]] = set()
    blocked = 0
    feasible = 0
    zero_root = 0
    chambers = 0
    audit = hashlib.sha256()

    for quotient_entry in quotient_entries:
        mask = int(quotient_entry["mask"])
        arcs = adjacency(mask)
        options = tuple(closed_options(arcs, root) for root in range(ORDER))
        counts = tuple(len(root_options) for root_options in options)
        if list(counts) != quotient_entry["root_counts"]:
            raise AssertionError("root closure count mismatch")
        encoded = base64.b64decode(quotient_entry["codes_base64"], validate=True)
        expected_length = 0 if 0 in counts else 2 * prod(counts)
        if len(encoded) != expected_length:
            raise AssertionError("multicover stream length mismatch")
        if 0 in counts:
            zero_root += 1
            continue

        offset = 0
        for choices in itertools.product(*(range(count) for count in counts)):
            code = int.from_bytes(encoded[offset : offset + 2], "big")
            offset += 2
            matrix = tuple(options[root][choices[root]][2] for root in range(ORDER))
            if code == FEASIBLE_CODE:
                key = (mask, choices)
                entry = feasible_lookup.get(key)
                if entry is None:
                    raise AssertionError("missing feasible chamber entry")
                verify_feasible_entry(entry, choices, options)
                used_feasible.add(key)
                feasible += 1
            else:
                coefficients = decode_coefficients(code)
                if not any(coefficients):
                    raise AssertionError("zero multicover cannot block a chamber")
                coordinate_sum = tuple(
                    sum(
                        coefficients[root] * matrix[root][column]
                        for root in range(ORDER)
                    )
                    for column in range(ORDER)
                )
                if max(coordinate_sum) > 0:
                    raise AssertionError("invalid multicover obstruction")
                blocked += 1
            audit.update(f"{mask}|{choices}|{code}\n".encode("ascii"))
            chambers += 1

    if used_feasible != set(feasible_lookup):
        raise AssertionError("unused feasible chamber entry")
    totals = sorted(int(entry["total"]) for entry in certificate["feasible"])
    if (
        (zero_root, chambers, blocked, feasible) != (12, 3603, 3591, 12)
        or totals != [36, 39, 42, 42, 45, 48, 48, 54, 56, 64, 72, 88]
        or {int(entry["mask"]) for entry in certificate["feasible"]} != {345}
    ):
        raise AssertionError("unexpected independent classification summary")

    published_permutation = (5, 4, 0, 1, 3, 2)
    if relabel(21465, published_permutation) != 345:
        raise AssertionError("published quotient relabeling failed")
    published_sizes = (7, 3, 11, 3, 9, 3)
    canonical_sizes = [0] * ORDER
    for old, new in enumerate(published_permutation):
        canonical_sizes[new] = published_sizes[old]
    if tuple(canonical_sizes) != (11, 3, 3, 9, 3, 7):
        raise AssertionError("published size relabeling failed")
    if strong_vertices(expanded_tournament(345, tuple(canonical_sizes))):
        raise AssertionError("canonical order-36 tournament has a strong vertex")

    print(
        json.dumps(
            {
                "audit_sha256": audit.hexdigest(),
                "blocked_chambers": blocked,
                "certificate_sha256": hashlib.sha256(raw).hexdigest(),
                "closure_chambers": chambers,
                "direct_order36_strong_vertices": [],
                "feasible_chambers": feasible,
                "minimum": min(totals),
                "quotient_types": len(representatives),
                "status": "INDEPENDENT MULTICOVER REPLAY VERIFIED",
                "unique_feasible_quotient": 345,
                "zero_root_quotients": zero_root,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
