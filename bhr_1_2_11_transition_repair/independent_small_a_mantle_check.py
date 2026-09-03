#!/usr/bin/env python3
"""Standalone checker for the eleven small-a BHR mantle slabs."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

SUPPORT = (1, 2, 11)
MODES = (2, 11)
EXPECTED_CERTIFICATE_SHA256 = (
    "7669175bf86a2ad4938bc1cd8a1aae8e7a64b5e59bcfc4904b6e6b4d7646a192"
)
EXPECTED_SEEDS = {
    1: (1, 11, 23), 2: (1, 11, 24), 3: (1, 9, 25),
    4: (1, 9, 26), 5: (1, 9, 27), 6: (1, 9, 28),
    7: (1, 9, 29), 8: (1, 9, 30), 9: (1, 15, 20),
    10: (1, 13, 21), 11: (1, 13, 22),
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
    for mode in MODES:
        verify_growth(child, mode, child_cuts[mode])
    return child, child_cuts


def check(certificate: Path, grid: int) -> dict[str, object]:
    assert grid >= 1
    raw = certificate.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_CERTIFICATE_SHA256
    data = json.loads(raw)
    assert data["schema"] == "bhr-small-a-mantle-v1"
    assert tuple(data["support"]) == SUPPORT
    assert len(data["cases"]) == 11

    digest = hashlib.sha256()
    seed_set_hash = hashlib.sha256()
    paths_checked = transitions = squares = derivation_steps = 0
    seen = set()
    for case in data["cases"]:
        base = tuple(case["residue_case"])
        assert base[:2] == (1, 1) and 1 <= base[2] <= 11
        seen.add(base)
        source = case["source"]
        source_counts = tuple(source["counts"])
        source_path = source["path"]
        source_cuts = {int(mode): cut for mode, cut in source["selected_growth_cuts"].items()}
        assert source_counts[0] == 1 and source_counts[1] % 2 == 1
        assert (source_counts[2] - base[2]) % 11 == 0
        assert set(source_cuts) == set(MODES)
        verify_realization(source_path, source_counts)
        for mode in MODES:
            verify_growth(source_path, mode, source_cuts[mode])

        endpoints = []
        for order in itertools.permutations(MODES):
            state = (source_path, source_cuts)
            for mode in order:
                state = advance(*state, mode)
                derivation_steps += 1
            endpoints.append(state)
        assert endpoints[0] == endpoints[1]

        seed = case["safe_seed"]
        seed_counts = tuple(seed["counts"])
        seed_path = seed["path"]
        seed_cuts = {int(mode): cut for mode, cut in seed["selected_growth_cuts"].items()}
        assert seed_counts == EXPECTED_SEEDS[base[2]]
        assert seed_counts == (source_counts[0], source_counts[1] + 2, source_counts[2] + 11)
        assert endpoints[0] == (seed_path, seed_cuts)
        verify_realization(seed_path, seed_counts)
        for mode in MODES:
            verify_growth(seed_path, mode, seed_cuts[mode])
        assert max(
            cyclic_length(u, v, len(seed_path)) for u, v in zip(seed_path, seed_path[1:])
        ) == 11
        assert 2 * 11 + sum(MODES) <= len(seed_path)
        seed_set_hash.update(
            json.dumps([base[2], seed_path], separators=(",", ":")).encode()
        )
        seed_set_hash.update(b"\n")

        family: dict[tuple[int, int], tuple[list[int], dict[int, int]]] = {}
        q_state = (seed_path, seed_cuts)
        for q in range(grid + 2):
            r_state = q_state
            for r in range(grid + 2):
                path, cuts = r_state
                verify_realization(path, (1, seed_counts[1] + 2 * q, seed_counts[2] + 11 * r))
                family[q, r] = r_state
                digest.update(
                    json.dumps([base[2], q, r, cuts, path], separators=(",", ":"), sort_keys=True).encode()
                )
                digest.update(b"\n")
                paths_checked += 1
                r_state = advance(*r_state, 11)
            q_state = advance(*q_state, 2)

        for q, r in itertools.product(range(grid + 1), repeat=2):
            state = family[q, r]
            assert advance(*state, 2) == family[q + 1, r]
            assert advance(*state, 11) == family[q, r + 1]
            assert advance(*advance(*state, 2), 11) == advance(*advance(*state, 11), 2)
            transitions += 2
            squares += 1

    assert seen == {(1, 1, c) for c in range(1, 12)}
    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "residue_classes": len(seen),
        "source_derivation_steps": derivation_steps,
        "minimum_seed_order": min(sum(counts) + 1 for counts in EXPECTED_SEEDS.values()),
        "seed_paths_sha256": seed_set_hash.hexdigest(),
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
    parser.add_argument("--grid", type=int, default=6)
    args = parser.parse_args()
    for key, value in check(args.certificate, args.grid).items():
        if isinstance(value, dict):
            value = json.dumps(value, separators=(",", ":"), sort_keys=True)
        print(f"{key}={value}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
