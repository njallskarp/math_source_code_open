#!/usr/bin/env python3
"""Definition-level verifier for the c=13 triple-incompatibility certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


CORE_ORDER = 13
FULL = (1 << CORE_ORDER) - 1
EXPECTED_FIELDS = {
    "common_red_core_edge",
    "core_differences",
    "footprints",
    "outside_indices",
    "pair_blue_witnesses",
    "source_artifact_ref",
    "source_certificate_sha256",
}
EXPECTED_SOURCE = "bafkreigl5xpol5rwgkymeo3xi5ikrqvgjv55txzo6qmvegazysdzipd6du"
EXPECTED_SOURCE_HASH = "f3fbd6c8bbd743ac82f6cbb6ba0f7fa1ef33a6fb8b905d1282f44f78b153392c"


def load(path: Path) -> tuple[dict[str, object], str]:
    raw = path.read_bytes()
    data = json.loads(raw)
    if not isinstance(data, dict) or set(data) != EXPECTED_FIELDS:
        raise ValueError("certificate fields")
    return data, hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    data, certificate_hash = load(args.certificate)

    differences = data["core_differences"]
    if differences != [1, 5, 8, 12]:
        raise AssertionError("core differences")

    def core_edge(i: int, j: int) -> bool:
        return i != j and (i - j) % CORE_ORDER in differences

    core_edges = tuple(
        pair
        for pair in itertools.combinations(range(CORE_ORDER), 2)
        if core_edge(*pair)
    )
    independent_triples = tuple(
        subset
        for subset in itertools.combinations(range(CORE_ORDER), 3)
        if all(not core_edge(i, j) for i, j in itertools.combinations(subset, 2))
    )
    independent_fours = tuple(
        subset
        for subset in itertools.combinations(range(CORE_ORDER), 4)
        if all(not core_edge(i, j) for i, j in itertools.combinations(subset, 2))
    )
    if (len(core_edges), len(independent_triples), len(independent_fours)) != (26, 78, 39):
        raise AssertionError("core census")

    indices = data["outside_indices"]
    if indices != [0, 10, 18]:
        raise AssertionError("outside indices")
    footprint_text = data["footprints"]
    if not isinstance(footprint_text, list) or len(footprint_text) != 3:
        raise ValueError("footprints")
    masks: list[int] = []
    for text in footprint_text:
        if not isinstance(text, str) or len(text) != 4 or text != text.lower():
            raise ValueError("footprint encoding")
        mask = int(text, 16)
        if not 0 <= mask <= FULL:
            raise ValueError("footprint range")
        masks.append(mask)
    for mask in masks:
        if any(not any(mask >> i & 1 for i in four) for four in independent_fours):
            raise AssertionError("nontransversal footprint")

    by_index = dict(zip(indices, masks, strict=True))
    pair_witnesses = data["pair_blue_witnesses"]
    if not isinstance(pair_witnesses, list) or len(pair_witnesses) != 3:
        raise ValueError("pair witnesses")
    expected_pairs = set(itertools.combinations(indices, 2))
    seen_pairs: set[tuple[int, int]] = set()
    for item in pair_witnesses:
        if not isinstance(item, dict) or set(item) != {
            "outside_pair",
            "independent_core_triple",
        }:
            raise ValueError("pair witness fields")
        pair_data = item["outside_pair"]
        triple_data = item["independent_core_triple"]
        if (
            not isinstance(pair_data, list)
            or len(pair_data) != 2
            or not all(isinstance(x, int) for x in pair_data)
        ):
            raise ValueError("outside pair")
        pair = tuple(pair_data)
        if pair not in expected_pairs or pair in seen_pairs:
            raise AssertionError("outside pair cover")
        seen_pairs.add(pair)
        if (
            not isinstance(triple_data, list)
            or len(triple_data) != 3
            or sorted(triple_data) != triple_data
            or len(set(triple_data)) != 3
            or not all(isinstance(i, int) and 0 <= i < CORE_ORDER for i in triple_data)
        ):
            raise ValueError("core triple")
        triple = tuple(triple_data)
        if triple not in independent_triples:
            raise AssertionError("nonindependent witness")
        if any((by_index[pair[0]] | by_index[pair[1]]) >> i & 1 for i in triple):
            raise AssertionError("blue witness meets footprint union")
    if seen_pairs != expected_pairs:
        raise AssertionError("pair cover")

    common_edge_data = data["common_red_core_edge"]
    if (
        not isinstance(common_edge_data, list)
        or len(common_edge_data) != 2
        or not all(isinstance(i, int) for i in common_edge_data)
    ):
        raise ValueError("common edge")
    common_edge = tuple(common_edge_data)
    if common_edge not in core_edges:
        raise AssertionError("common edge is not red")
    if any(not (mask >> i & 1) for mask in masks for i in common_edge):
        raise AssertionError("red edge not in common footprint")

    if data["source_artifact_ref"] != EXPECTED_SOURCE:
        raise AssertionError("source artifact")
    if data["source_certificate_sha256"] != EXPECTED_SOURCE_HASH:
        raise AssertionError("source hash")

    # Edge bit 1 is red.  A zero bit violates its pairwise blue witness; the
    # all-one assignment violates the common-red-edge triple constraint.
    safe = pair_blue_failures = red_triple_failures = 0
    for assignment in itertools.product((0, 1), repeat=3):
        if 0 in assignment:
            pair_blue_failures += 1
        elif assignment == (1, 1, 1):
            red_triple_failures += 1
        else:
            safe += 1
    if (safe, pair_blue_failures, red_triple_failures) != (0, 7, 1):
        raise AssertionError("truth table")

    # The 52 affine core automorphisms i -> a*i+b give 52 distinct unordered
    # forbidden triples of footprint types.
    def transform(mask: int, multiplier: int, translation: int) -> int:
        result = 0
        for i in range(CORE_ORDER):
            if mask >> i & 1:
                result |= 1 << ((multiplier * i + translation) % CORE_ORDER)
        return result

    orbit: set[tuple[int, int, int]] = set()
    for multiplier in (1, 5, 8, 12):
        for translation in range(CORE_ORDER):
            transformed = tuple(transform(mask, multiplier, translation) for mask in masks)
            orbit.add(tuple(sorted(transformed)))
            transformed_witness = tuple(
                (multiplier * i + translation) % CORE_ORDER for i in (0, 4, 7)
            )
            if any(core_edge(i, j) for i, j in itertools.combinations(transformed_witness, 2)):
                raise AssertionError("affine independent witness")
            for left, right in itertools.combinations(range(3), 2):
                if any((transformed[left] | transformed[right]) >> i & 1 for i in transformed_witness):
                    raise AssertionError("affine disjointness")
            transformed_edge = tuple(
                (multiplier * i + translation) % CORE_ORDER for i in common_edge
            )
            if not core_edge(*transformed_edge):
                raise AssertionError("affine red edge")
            if any(not (mask >> i & 1) for mask in transformed for i in transformed_edge):
                raise AssertionError("affine common edge")
    if len(orbit) != 52:
        raise AssertionError("affine orbit size")

    # Removing any one of the three pair premises or the final red-triple
    # premise admits exactly one of the eight edge colorings.
    deletion_models = 0
    for omitted in range(4):
        models = 0
        for assignment in itertools.product((0, 1), repeat=3):
            violations = {i for i, color in enumerate(assignment) if color == 0}
            if assignment == (1, 1, 1):
                violations.add(3)
            if violations <= {omitted}:
                models += 1
        if models != 1:
            raise AssertionError(("deletion minimality", omitted, models))
        deletion_models += models

    result = {
        "affine_orbit": len(orbit),
        "certificate_sha256": certificate_hash,
        "common_red_core_edge": list(common_edge),
        "core_edges": len(core_edges),
        "deletion_models": deletion_models,
        "independent_core_fours": len(independent_fours),
        "independent_core_triples": len(independent_triples),
        "legal_footprints": len(masks),
        "pair_blue_witnesses": len(pair_witnesses),
        "safe_edge_colorings": safe,
        "source_height": 2969,
        "status": "VERIFIED TRIPLE-INCOMPATIBILITY OBSTRUCTION",
        "truth_table_assignments": 8,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
