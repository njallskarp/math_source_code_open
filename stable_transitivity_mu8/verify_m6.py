#!/usr/bin/env python3
"""Exact verifier for the G8 completion structure and scale-six profiles."""

from __future__ import annotations

import argparse
import collections
import itertools
import re
from hashlib import sha256
from pathlib import Path

from verify_certificate import PAIRS, agrees, order_vectors, parse_certificate

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
EDGE_INDEX = {pair: edge for edge, pair in enumerate(PAIRS)}

PROFILE_HEADER = "CERTIFICATE stable_transitivity_m6_v1 n=8 classes=96 orders=20 margin=13"
MAP_HEADER = "CERTIFICATE stable_transitivity_g8_maps_v1 classes=96 completions=256"
PROFILE_ROW = re.compile(
    r"CLASS (?P<index>\d+) tournament=(?P<tournament>\d+) profile=(?P<profile>.+)"
)
SUPPORT_ROW = re.compile(r"SUPPORT (?P<index>\d+) g8_to_t=(?P<permutation>[\d,]+)")
COMPLETION_ROW = re.compile(
    r"COMPLETION (?P<bits>[01]{8}) class=(?P<index>\d+) "
    r"completion_to_t=(?P<permutation>[\d,]+)"
)


def permutation(text: str) -> tuple[int, ...]:
    result = tuple(int(value) for value in text.split(","))
    if sorted(result) != list(range(8)):
        raise ValueError("malformed vertex permutation")
    return result


def read_profiles(path: Path) -> list[tuple[int, int, tuple[tuple[int, int], ...]]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != PROFILE_HEADER:
        raise ValueError("wrong scale-six profile header")
    records = []
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        match = PROFILE_ROW.fullmatch(line)
        if match is None:
            raise ValueError("malformed scale-six profile row")
        profile = []
        for term in match["profile"].split(","):
            order, multiplicity = term.split(":")
            profile.append((int(order), int(multiplicity)))
        records.append(
            (int(match["index"]), int(match["tournament"]), tuple(profile))
        )
    return records


def read_maps(
    path: Path,
) -> tuple[
    list[tuple[int, tuple[int, ...]]],
    list[tuple[int, int, tuple[int, ...]]],
]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != MAP_HEADER:
        raise ValueError("wrong G8 map header")
    supports = []
    completions = []
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        support_match = SUPPORT_ROW.fullmatch(line)
        if support_match is not None:
            supports.append(
                (
                    int(support_match["index"]),
                    permutation(support_match["permutation"]),
                )
            )
            continue
        completion_match = COMPLETION_ROW.fullmatch(line)
        if completion_match is not None:
            completions.append(
                (
                    int(completion_match["bits"], 2),
                    int(completion_match["index"]),
                    permutation(completion_match["permutation"]),
                )
            )
            continue
        raise ValueError("malformed G8 map row")
    return supports, completions


def tournament_arc(tournament: int, edge: int) -> tuple[int, int]:
    left, right = PAIRS[edge]
    return (left, right) if (tournament >> edge) & 1 else (right, left)


def make_completion(bits: int) -> int:
    arcs = set(G8_ARCS)
    for position, (left, right) in enumerate(G8_MISSING):
        arcs.add((left, right) if (bits >> position) & 1 else (right, left))
    return sum(
        int((left, right) in arcs) << edge
        for edge, (left, right) in enumerate(PAIRS)
    )


def relabel_definition(tournament: int, mapping: tuple[int, ...]) -> int:
    adjacency = [[False] * 8 for _ in range(8)]
    for edge in range(28):
        tail, head = tournament_arc(tournament, edge)
        adjacency[tail][head] = True
    return sum(
        int(adjacency[mapping[left]][mapping[right]]) << edge
        for edge, (left, right) in enumerate(PAIRS)
    )


def predicts_arc(order: tuple[int, ...], arc: tuple[int, int]) -> int:
    left, right = arc
    if left < right:
        edge = EDGE_INDEX[(left, right)]
        return order[edge]
    edge = EDGE_INDEX[(right, left)]
    return 1 - order[edge]


def verify(
    radial_certificate: Path,
    profiles_path: Path,
    maps_path: Path,
) -> str:
    radial = parse_certificate(radial_certificate)
    radial_by_index = {
        index: (tournament, dual) for index, tournament, dual, _ in radial
    }
    if len(radial_by_index) != 96:
        raise ValueError("expected 96 radial records")
    profiles = read_profiles(profiles_path)
    supports, completion_maps = read_maps(maps_path)
    if len(profiles) != 96 or len(supports) != 96 or len(completion_maps) != 256:
        raise ValueError("wrong certificate record count")
    if [index for index, _, _ in profiles] != list(radial_by_index):
        raise ValueError("profile order does not match radial certificate")
    if [index for index, _ in supports] != list(radial_by_index):
        raise ValueError("support-map order does not match radial certificate")

    g8 = frozenset(G8_ARCS)
    if len(g8) != 20 or len(G8_MISSING) != 8:
        raise AssertionError("wrong canonical G8 dimensions")
    if {frozenset(arc) for arc in g8} & {frozenset(pair) for pair in G8_MISSING}:
        raise AssertionError("G8 arcs and missing pairs overlap")
    if len({frozenset(arc) for arc in g8} | {frozenset(pair) for pair in G8_MISSING}) != 28:
        raise AssertionError("G8 does not partition the pairs")

    vertex_permutations = list(itertools.permutations(range(8)))
    automorphisms = sum(
        frozenset((p[a], p[b]) for a, b in g8) == g8
        for p in vertex_permutations
    )
    if automorphisms != 2:
        raise AssertionError(f"canonical G8 has {automorphisms} automorphisms")

    orders = order_vectors()
    g8_hits = [sum(predicts_arc(order, arc) for arc in g8) for order in orders]
    maximum_hits = max(g8_hits)
    tight_orders = sum(hits == maximum_hits for hits in g8_hits)
    if maximum_hits != 13 or tight_orders != 832:
        raise AssertionError("wrong canonical G8 ordering statistics")

    for index, mapping in supports:
        tournament, dual = radial_by_index[index]
        mapped_g8 = frozenset((mapping[a], mapping[b]) for a, b in g8)
        target = frozenset(tournament_arc(tournament, edge) for edge in dual)
        if mapped_g8 != target:
            raise ValueError(f"class {index}: support is not the mapped canonical G8")

    profile_terms = 0
    maximum_multiplicity = 0
    arc_checks = 0
    for index, tournament, profile in profiles:
        source_tournament, _ = radial_by_index[index]
        if tournament != source_tournament:
            raise ValueError(f"class {index}: tournament mismatch")
        order_indices = [order for order, _ in profile]
        if len(order_indices) != len(set(order_indices)):
            raise ValueError(f"class {index}: repeated order index")
        if any(order < 0 or order >= len(orders) for order in order_indices):
            raise ValueError(f"class {index}: order index out of range")
        if any(multiplicity <= 0 for _, multiplicity in profile):
            raise ValueError(f"class {index}: nonpositive multiplicity")
        if sum(multiplicity for _, multiplicity in profile) != 20:
            raise ValueError(f"class {index}: profile does not contain 20 orders")
        for edge in range(28):
            count = sum(
                multiplicity * agrees(tournament, orders[order], edge)
                for order, multiplicity in profile
            )
            if count != 13:
                raise ValueError(f"class {index}: edge {edge} count {count} != 13")
            arc_checks += 1
        profile_terms += len(profile)
        maximum_multiplicity = max(
            maximum_multiplicity, *(multiplicity for _, multiplicity in profile)
        )

    source_tournaments = {
        index: tournament for index, (tournament, _) in radial_by_index.items()
    }
    bits_seen = set()
    class_multiplicity: collections.Counter[int] = collections.Counter()
    for bits, index, mapping in completion_maps:
        if bits in bits_seen:
            raise ValueError("repeated G8 completion")
        bits_seen.add(bits)
        if index not in source_tournaments:
            raise ValueError("completion maps to an unknown source class")
        if relabel_definition(make_completion(bits), mapping) != source_tournaments[index]:
            raise ValueError(f"completion {bits:08b}: claimed isomorphism fails")
        class_multiplicity[index] += 1
    if bits_seen != set(range(256)) or len(class_multiplicity) != 96:
        raise ValueError("G8 completion map is incomplete")
    multiplicity_distribution = collections.Counter(class_multiplicity.values())
    if multiplicity_distribution != {2: 72, 4: 16, 6: 8}:
        raise ValueError("unexpected G8 completion multiplicities")

    # For 6qT and a stabilizer of size a, the transformed profile has
    # 6q+2a orders and predicts every G8 arc 6q+a times.  The maximum-13
    # inequality forces a>=7q; the 20-order profiles attain equality at q=1.
    for q in range(1, 101):
        for a in range(7 * q):
            if 20 * (6 * q + a) <= 13 * (6 * q + 2 * a):
                raise AssertionError("symbolic lower-bound inequality failed")
        if 20 * (6 * q + 7 * q) != 13 * (6 * q + 14 * q):
            raise AssertionError("scale-six equality arithmetic failed")

    rows = [
        "classes=96",
        f"g8_arcs={len(g8)} missing_pairs={len(G8_MISSING)} automorphisms={automorphisms}",
        f"orders={len(orders)} g8_tight_orders={tight_orders} g8_maximum_hits={maximum_hits}",
        "completions=256 completion_classes=96 multiplicities=2:72,4:16,6:8",
        f"profiles=96 profile_orders=1920 profile_terms={profile_terms} maximum_multiplicity={maximum_multiplicity}",
        f"arc_count_checks={arc_checks}",
        "exact_ray=m(6qT)=7q_for_all_q>=1",
    ]
    canonical = "\n".join(rows)
    return canonical + "\naudit_sha256=" + sha256(canonical.encode("ascii")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radial-certificate", type=Path, default=Path("certificate.txt"))
    parser.add_argument("--profiles", type=Path, default=Path("m6_profiles.txt"))
    parser.add_argument("--maps", type=Path, default=Path("g8_maps.txt"))
    args = parser.parse_args()
    print(verify(args.radial_certificate, args.profiles, args.maps))


if __name__ == "__main__":
    main()
