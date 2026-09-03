#!/usr/bin/env python3
"""Standalone definition-level checker for the all-residue a=2 mantle."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

SUPPORT = (1, 2, 11)
PAIR_MODES = (2, 11)
SPECIAL_RESIDUES = (1, 10)
EXPECTED_CERTIFICATE_SHA256 = (
    "601a48ad69abef99c6279c8420492c16c9000120069affad74686388d4ccca4e"
)
EXPECTED_SEEDS = {
    1: (2, 11, 23), 2: (2, 9, 24), 3: (2, 9, 25),
    4: (2, 9, 26), 5: (2, 9, 27), 6: (2, 9, 28),
    7: (2, 9, 29), 8: (2, 9, 30), 9: (2, 13, 20),
    10: (2, 13, 21), 11: (2, 11, 22),
}


def cyclic_length(u: int, v: int, order: int) -> int:
    difference = abs(u - v)
    return min(difference, order - difference)


def changed_edges(path: list[int], mode: int, cut: int) -> list[tuple[int, int]]:
    order = len(path)
    changed = []
    for u, v in zip(path, path[1:]):
        old = cyclic_length(u, v, order)
        uu = u if u <= cut else u + mode
        vv = v if v <= cut else v + mode
        if cyclic_length(uu, vv, order + mode) > old:
            changed.append((u, v))
    return changed


def verify_growth(path: list[int], mode: int, cut: int) -> None:
    order = len(path)
    assert mode - 1 <= cut <= order - 1 - mode
    critical = set(range(cut - mode + 1, cut + 1))
    incidence: Counter[int] = Counter()
    for u, v in changed_edges(path, mode, cut):
        assert u in critical or v in critical
        if u in critical:
            incidence[u] += 1
        if v in critical:
            incidence[v] += 1
    assert all(incidence[vertex] == 1 for vertex in critical)


def verify_realization(path: list[int], counts: tuple[int, int, int]) -> None:
    order = sum(counts) + 1
    assert sorted(path) == list(range(order))
    observed = Counter(cyclic_length(u, v, order) for u, v in zip(path, path[1:]))
    assert observed == Counter(dict(zip(SUPPORT, counts)))


def advance(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    inserted_cut = cuts[inserted_mode]
    verify_growth(path, inserted_mode, inserted_cut)
    critical = set(range(inserted_cut - inserted_mode + 1, inserted_cut + 1))
    changed = set(changed_edges(path, inserted_mode, inserted_cut))
    embedded = {
        vertex: vertex if vertex <= inserted_cut else vertex + inserted_mode
        for vertex in path
    }
    child = [embedded[path[0]]]
    for u, v in zip(path, path[1:]):
        if (u, v) in changed:
            inside = [vertex for vertex in (u, v) if vertex in critical]
            assert len(inside) == 1
            child.append(inside[0] + inserted_mode)
        child.append(embedded[v])
    child_cuts = {
        mode: cut if cut <= inserted_cut else cut + inserted_mode
        for mode, cut in cuts.items()
    }
    for mode, cut in child_cuts.items():
        verify_growth(child, mode, cut)
    return child, child_cuts


def check(certificate: Path, grid: int) -> dict[str, object]:
    assert grid >= 1
    raw = certificate.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_CERTIFICATE_SHA256
    data = json.loads(raw)
    assert data["schema"] == "bhr-a2-mantle-v1"
    assert tuple(data["support"]) == SUPPORT
    assert len(data["cases"]) == 11
    assert data["source_context"]["source_certificate_sha256"] == (
        "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c"
    )
    assert data["source_context"]["trimodal_certificate_sha256"] == (
        "532470ffe31ff3e5acb4da51a78c15f172d2d00db6816dd43d5dc44a243bc059"
    )
    assert data["source_context"]["trimodal_successor_links_checked"] == 11

    digest = hashlib.sha256()
    seed_digest = hashlib.sha256()
    seen = set()
    paths_checked = transitions = squares = derivation_steps = 0
    two_mode_sources = existing_sources = 0
    for case in sorted(data["cases"], key=lambda item: item["residue_case"]):
        base = tuple(case["residue_case"])
        assert base[:2] == (1, 1) and 1 <= base[2] <= 11
        assert case["source_witness_index"] == 0
        seen.add(base)
        residue = base[2]
        modes = SUPPORT if residue in SPECIAL_RESIDUES else PAIR_MODES
        if residue in SPECIAL_RESIDUES:
            assert case["provenance"] == "rederived_existing_trimodal_safe_seed"
            existing_sources += 1
        else:
            assert case["provenance"] == "a2_source_two_mode_derivation_retaining_mode_1"
            two_mode_sources += 1

        source = case["source"]
        source_counts = tuple(source["counts"])
        source_path = source["path"]
        source_cuts = {int(mode): cut for mode, cut in source["selected_growth_cuts"].items()}
        assert tuple(source_cuts) == SUPPORT
        assert source_counts[0] == (1 if residue in SPECIAL_RESIDUES else 2)
        assert source_counts[1] % 2 == 1
        assert (source_counts[2] - residue) % 11 == 0
        verify_realization(source_path, source_counts)
        for mode, cut in source_cuts.items():
            verify_growth(source_path, mode, cut)

        endpoints = []
        for order in itertools.permutations(modes):
            state = (source_path, source_cuts)
            for mode in order:
                state = advance(*state, mode)
                derivation_steps += 1
            endpoints.append(state)
        assert all(endpoint == endpoints[0] for endpoint in endpoints)

        seed = case["safe_seed"]
        seed_counts = tuple(seed["counts"])
        seed_path = seed["path"]
        seed_cuts = {int(mode): cut for mode, cut in seed["selected_growth_cuts"].items()}
        assert seed_counts == EXPECTED_SEEDS[residue]
        assert endpoints[0] == (seed_path, seed_cuts)
        verify_realization(seed_path, seed_counts)
        for mode, cut in seed_cuts.items():
            verify_growth(seed_path, mode, cut)
        assert max(
            cyclic_length(u, v, len(seed_path)) for u, v in zip(seed_path, seed_path[1:])
        ) == 11
        assert 2 * 11 + sum(PAIR_MODES) <= len(seed_path)
        seed_digest.update(
            json.dumps([residue, seed_path], separators=(",", ":")).encode()
        )
        seed_digest.update(b"\n")

        family: dict[
            tuple[int, int, int], tuple[list[int], dict[int, int]]
        ] = {}
        p_state = (seed_path, seed_cuts)
        for p in range(grid + 2):
            q_state = p_state
            for q in range(grid + 2):
                r_state = q_state
                for r in range(grid + 2):
                    path, cuts = r_state
                    verify_realization(
                        path,
                        (2 + p, seed_counts[1] + 2 * q, seed_counts[2] + 11 * r),
                    )
                    family[p, q, r] = r_state
                    digest.update(
                        json.dumps(
                            [residue, p, q, r, cuts, path],
                            separators=(",", ":"), sort_keys=True,
                        ).encode()
                    )
                    digest.update(b"\n")
                    paths_checked += 1
                    r_state = advance(*r_state, 11)
                q_state = advance(*q_state, 2)
            p_state = advance(*p_state, 1)

        for p, q, r in itertools.product(range(grid + 1), repeat=3):
            state = family[p, q, r]
            for coordinate, mode in enumerate(SUPPORT):
                index = [p, q, r]
                index[coordinate] += 1
                assert advance(*state, mode) == family[tuple(index)]
                transitions += 1
            for first, second in itertools.combinations(SUPPORT, 2):
                assert advance(*advance(*state, first), second) == advance(
                    *advance(*state, second), first
                )
                squares += 1

    assert seen == {(1, 1, residue) for residue in range(1, 12)}
    assert (two_mode_sources, existing_sources, derivation_steps) == (9, 2, 72)
    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "residue_classes": len(seen),
        "two_mode_sources": two_mode_sources,
        "existing_safe_residues_rederived": existing_sources,
        "source_derivation_steps": derivation_steps,
        "minimum_seed_order": min(sum(counts) + 1 for counts in EXPECTED_SEEDS.values()),
        "seed_paths_sha256": seed_digest.hexdigest(),
        "safe_margin": "35<=36",
        "grid": grid,
        "family_paths_checked": paths_checked,
        "coordinate_transitions_checked": transitions,
        "commuting_squares_checked": squares,
        "record_sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=3)
    args = parser.parse_args()
    for key, value in check(args.certificate, args.grid).items():
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
