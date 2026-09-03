#!/usr/bin/env python3
"""Standalone checker for the (1,9+2q,25+11r) BHR slab."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

SUPPORT = (1, 2, 11)
MODES = (2, 11)
EXPECTED_SEED_COUNTS = (1, 9, 25)
EXPECTED_SEED_CUTS = {2: 2, 11: 13}
EXPECTED_CHANGED = {
    2: [(2, 4), (1, 3)],
    11: [
        (6, 17),
        (19, 8),
        (10, 21),
        (23, 12),
        (13, 24),
        (22, 11),
        (9, 20),
        (18, 7),
        (5, 16),
        (4, 15),
        (3, 14),
    ],
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
    observed = Counter(
        cyclic_length(u, v, order) for u, v in zip(path, path[1:])
    )
    assert observed == Counter(dict(zip(SUPPORT, counts)))


def transported_cut(tested: int, inserted: int, size: int) -> int:
    return tested if tested <= inserted else tested + size


def advance(
    path: list[int], cuts: dict[int, int], inserted_mode: int
) -> tuple[list[int], dict[int, int]]:
    inserted_cut = cuts[inserted_mode]
    verify_growth(path, inserted_mode, inserted_cut)
    critical = set(
        range(inserted_cut - inserted_mode + 1, inserted_cut + 1)
    )
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
        mode: transported_cut(cuts[mode], inserted_cut, inserted_mode)
        for mode in MODES
    }
    for mode in MODES:
        verify_growth(child, mode, child_cuts[mode])
    return child, child_cuts


def check(certificate: Path, grid: int) -> dict[str, object]:
    assert grid >= 1
    raw = certificate.read_bytes()
    data = json.loads(raw)
    assert data["schema"] == "bhr-small-a-c3-slab-v1"
    assert tuple(data["support"]) == SUPPORT

    derivation = data["derivation"]
    source_path = derivation["path"]
    source_cuts = {int(mode): cut for mode, cut in derivation["selected_growth_cuts"].items()}
    verify_realization(source_path, (1, 7, 14))
    for mode in MODES:
        verify_growth(source_path, mode, source_cuts[mode])
    endpoints = []
    for order in itertools.permutations(MODES):
        state = (source_path, source_cuts)
        for mode in order:
            state = advance(*state, mode)
        endpoints.append(state)
    assert endpoints[0] == endpoints[1]

    seed = data["seed"]
    seed_path = seed["path"]
    seed_cuts = {int(mode): cut for mode, cut in seed["selected_growth_cuts"].items()}
    assert tuple(seed["counts"]) == EXPECTED_SEED_COUNTS
    assert seed_cuts == EXPECTED_SEED_CUTS
    assert endpoints[0] == (seed_path, seed_cuts)
    verify_realization(seed_path, EXPECTED_SEED_COUNTS)
    for mode in MODES:
        verify_growth(seed_path, mode, seed_cuts[mode])
        assert changed_edges(seed_path, mode, seed_cuts[mode]) == EXPECTED_CHANGED[mode]
    assert max(
        cyclic_length(u, v, len(seed_path))
        for u, v in zip(seed_path, seed_path[1:])
    ) == 11
    assert 2 * 11 + sum(MODES) <= len(seed_path)

    family: dict[tuple[int, int], tuple[list[int], dict[int, int]]] = {}
    digest = hashlib.sha256()
    q_state = (seed_path, seed_cuts)
    for q in range(grid + 2):
        r_state = q_state
        for r in range(grid + 2):
            path, cuts = r_state
            verify_realization(path, (1, 9 + 2 * q, 25 + 11 * r))
            family[q, r] = r_state
            digest.update(
                json.dumps([q, r, cuts, path], separators=(",", ":"), sort_keys=True).encode()
            )
            digest.update(b"\n")
            r_state = advance(*r_state, 11)
        q_state = advance(*q_state, 2)

    transitions = squares = 0
    for q, r in itertools.product(range(grid + 1), repeat=2):
        state = family[q, r]
        assert advance(*state, 2) == family[q + 1, r]
        assert advance(*state, 11) == family[q, r + 1]
        assert advance(*advance(*state, 2), 11) == advance(*advance(*state, 11), 2)
        transitions += 2
        squares += 1

    path_bytes = json.dumps(seed_path, separators=(",", ":")).encode()
    return {
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "seed_path_sha256": hashlib.sha256(path_bytes).hexdigest(),
        "seed_order": len(seed_path),
        "growth_cuts": seed_cuts,
        "safe_margin": "35<=36",
        "grid": grid,
        "family_paths_checked": len(family),
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
