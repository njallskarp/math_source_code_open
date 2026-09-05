#!/usr/bin/env python3
"""Generate compact isomorphism maps to one canonical 20-arc G8 obstacle."""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

from verify_certificate import PAIRS, parse_certificate

G8_ARCS = (
    (0, 1), (0, 2), (0, 3), (4, 0), (6, 0), (7, 0),
    (1, 3), (1, 4), (5, 1), (1, 6), (7, 1), (2, 3),
    (2, 4), (5, 2), (6, 2), (2, 7), (3, 5), (3, 6),
    (3, 7), (4, 5),
)
G8_MISSING = (
    (0, 5), (1, 2), (3, 4), (4, 6),
    (4, 7), (5, 6), (5, 7), (6, 7),
)


def tournament_arc(tournament: int, edge: int) -> tuple[int, int]:
    left, right = PAIRS[edge]
    return (left, right) if (tournament >> edge) & 1 else (right, left)


def support(tournament: int, dual: tuple[int, ...]) -> frozenset[tuple[int, int]]:
    return frozenset(tournament_arc(tournament, edge) for edge in dual)


def relabel_tournament(tournament: int, permutation: tuple[int, ...]) -> int:
    old_bits = {(i, j): edge for edge, (i, j) in enumerate(PAIRS)}

    def old_arc(left: int, right: int) -> bool:
        if left < right:
            return bool((tournament >> old_bits[(left, right)]) & 1)
        return not bool((tournament >> old_bits[(right, left)]) & 1)

    return sum(
        int(old_arc(permutation[i], permutation[j])) << edge
        for edge, (i, j) in enumerate(PAIRS)
    )


def canonical(
    tournament: int, permutations: list[tuple[int, ...]]
) -> tuple[int, tuple[int, ...]]:
    best = None
    witness = None
    for permutation in permutations:
        image = relabel_tournament(tournament, permutation)
        if best is None or image < best:
            best = image
            witness = permutation
    assert best is not None and witness is not None
    return best, witness


def completion(bits: int) -> int:
    arc_set = set(G8_ARCS)
    for position, (left, right) in enumerate(G8_MISSING):
        arc_set.add((left, right) if (bits >> position) & 1 else (right, left))
    return sum(
        int((left, right) in arc_set) << edge
        for edge, (left, right) in enumerate(PAIRS)
    )


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for index, value in enumerate(permutation):
        result[value] = index
    return tuple(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radial-certificate", type=Path, default=Path("certificate.txt"))
    parser.add_argument("--output", type=Path, default=Path("g8_maps.txt"))
    args = parser.parse_args()

    records = parse_certificate(args.radial_certificate)
    permutations = list(itertools.permutations(range(8)))
    rows = [
        "CERTIFICATE stable_transitivity_g8_maps_v1 classes=96 completions=256",
        "# SUPPORT <source-index> g8_to_t=<permutation>",
    ]
    g8 = frozenset(G8_ARCS)
    for source_index, tournament, dual, _ in records:
        target = support(tournament, dual)
        witness = next(
            permutation
            for permutation in permutations
            if frozenset((permutation[a], permutation[b]) for a, b in g8) == target
        )
        rows.append(f"SUPPORT {source_index} g8_to_t={','.join(map(str, witness))}")

    canonical_obstructions: dict[int, tuple[int, tuple[int, ...]]] = {}
    for source_index, tournament, _, _ in records:
        canonical_mask, witness = canonical(tournament, permutations)
        if canonical_mask in canonical_obstructions:
            raise ValueError("source obstruction representatives are isomorphic")
        canonical_obstructions[canonical_mask] = (source_index, witness)

    rows.append("# COMPLETION <8-bit-index> class=<source-index> completion_to_t=<permutation>")
    used = set()
    for bits in range(256):
        tournament = completion(bits)
        canonical_mask, completion_to_canonical = canonical(tournament, permutations)
        source_index, source_to_canonical = canonical_obstructions[canonical_mask]
        source_inverse = inverse(source_to_canonical)
        completion_to_source = tuple(
            completion_to_canonical[source_inverse[index]] for index in range(8)
        )
        if relabel_tournament(tournament, completion_to_source) != next(
            source_tournament
            for index, source_tournament, _, _ in records
            if index == source_index
        ):
            raise AssertionError("composed completion isomorphism failed")
        rows.append(
            f"COMPLETION {bits:08b} class={source_index} "
            f"completion_to_t={','.join(map(str, completion_to_source))}"
        )
        used.add(source_index)
        print(f"generated completion {bits + 1}/256", flush=True)
    if len(used) != 96:
        raise AssertionError(f"completion map reaches {len(used)} classes, not 96")
    args.output.write_text("\n".join(rows) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
