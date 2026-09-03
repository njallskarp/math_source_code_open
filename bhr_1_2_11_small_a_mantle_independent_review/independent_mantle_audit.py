#!/usr/bin/env python3
"""Clean-room audit of the eleven-residue BHR small-a mantle certificate.

This checker imports no target code.  It verifies the certificate directly from
the definitions, compares the two source-growth orders, checks a finite family
grid by two independent operation routes, and exhausts the local two-cut edge
configurations at every order from the sharp margin 35 through the largest
seed order 41.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import platform


SUPPORT = (1, 2, 11)
MODES = (2, 11)
PINNED_CERTIFICATE_SHA256 = (
    "7669175bf86a2ad4938bc1cd8a1aae8e7a64b5e59bcfc4904b6e6b4d7646a192"
)
EXPECTED_SEEDS = {
    1: (1, 11, 23),
    2: (1, 11, 24),
    3: (1, 9, 25),
    4: (1, 9, 26),
    5: (1, 9, 27),
    6: (1, 9, 28),
    7: (1, 9, 29),
    8: (1, 9, 30),
    9: (1, 15, 20),
    10: (1, 13, 21),
    11: (1, 13, 22),
}


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AuditFailure(str(message))


def circle_length(a: int, b: int, order: int) -> int:
    clockwise = (b - a) % order
    return min(clockwise, order - clockwise)


def embedded(vertex: int, mode: int, cut: int) -> int:
    return vertex if vertex <= cut else vertex + mode


def length_increases(a: int, b: int, order: int, mode: int, cut: int) -> bool:
    before = circle_length(a, b, order)
    after = circle_length(embedded(a, mode, cut), embedded(b, mode, cut), order + mode)
    return after > before


def critical_vertices(mode: int, cut: int) -> set[int]:
    return set(range(cut - mode + 1, cut + 1))


def growth_incidence(path: list[int], mode: int, cut: int) -> Counter[int]:
    order = len(path)
    require(mode - 1 <= cut <= order - 1 - mode, ("cut range", order, mode, cut))
    critical = critical_vertices(mode, cut)
    incidence: Counter[int] = Counter()
    for a, b in zip(path, path[1:]):
        if not length_increases(a, b, order, mode, cut):
            continue
        endpoints = critical.intersection((a, b))
        require(len(endpoints) == 1, ("changed edge endpoint", order, mode, cut, a, b))
        incidence.update(endpoints)
    require(
        all(incidence[v] == 1 for v in critical),
        ("growth incidence", order, mode, cut, dict(incidence)),
    )
    return incidence


def apply_growth(path: list[int], mode: int, cut: int) -> list[int]:
    """Apply the definition-level edge subdivision for one growth mode."""
    growth_incidence(path, mode, cut)
    order = len(path)
    critical = critical_vertices(mode, cut)
    child = [embedded(path[0], mode, cut)]
    for a, b in zip(path, path[1:]):
        if length_increases(a, b, order, mode, cut):
            endpoint = next(iter(critical.intersection((a, b))))
            child.append(endpoint + mode)
        child.append(embedded(b, mode, cut))
    require(sorted(child) == list(range(order + mode)), ("growth permutation", order, mode, cut))
    return child


def transport_cut(old_cut: int, inserted_cut: int, inserted_mode: int) -> int:
    return old_cut if old_cut <= inserted_cut else old_cut + inserted_mode


def path_counts(path: list[int]) -> tuple[int, int, int]:
    observed = Counter(circle_length(a, b, len(path)) for a, b in zip(path, path[1:]))
    require(set(observed).issubset(SUPPORT), ("unexpected edge length", dict(observed)))
    return tuple(observed[x] for x in SUPPORT)  # type: ignore[return-value]


def verify_realization(path: list[int], expected: tuple[int, int, int]) -> None:
    require(len(path) == sum(expected) + 1, ("order", len(path), expected))
    require(sorted(path) == list(range(len(path))), ("not a Hamiltonian path", expected))
    require(path_counts(path) == expected, ("length multiset", expected, path_counts(path)))


State = tuple[list[int], dict[int, int]]


def step(state: State, mode: int) -> State:
    path, cuts = state
    require(set(cuts) == set(MODES), ("cut modes", cuts))
    cut = cuts[mode]
    child = apply_growth(path, mode, cut)
    child_cuts = {
        tested: transport_cut(old_cut, cut, mode) for tested, old_cut in cuts.items()
    }
    for tested in MODES:
        growth_incidence(child, tested, child_cuts[tested])
    return child, child_cuts


def advance_repeated(state: State, mode: int, repetitions: int) -> State:
    for _ in range(repetitions):
        state = step(state, mode)
    return state


def local_edge_admissible(edge: list[int], order: int, mode: int, cut: int) -> bool:
    if not length_increases(edge[0], edge[1], order, mode, cut):
        return True
    return len(critical_vertices(mode, cut).intersection(edge)) == 1


def split_local_sequence(
    sequence: list[int], order: int, mode: int, cut: int
) -> list[int] | None:
    """Subdivide one old path edge, without imposing global incidence counts."""
    critical = critical_vertices(mode, cut)
    out = [embedded(sequence[0], mode, cut)]
    for a, b in zip(sequence, sequence[1:]):
        if length_increases(a, b, order, mode, cut):
            endpoints = critical.intersection((a, b))
            if len(endpoints) != 1:
                return None
            out.append(next(iter(endpoints)) + mode)
        out.append(embedded(b, mode, cut))
    return out


def local_safe_margin_audit() -> tuple[int, str]:
    """Exhaust disjoint-interval local commutation for orders 35 through 41.

    Every old edge of length at most 11 and every legal pair of cuts is tested
    when the critical intervals are disjoint and that edge is locally compatible
    with both growth incidences.  Disjointness is the target-specific invariant
    used in this audit; it is preserved by order-preserving cut transport.  This
    is corroborative finite evidence for the written shortest-arc proof, not a
    replacement for its induction over unbounded orders.
    """
    checked = 0
    digest = hashlib.sha256()
    x, y = MODES
    for order in range(35, 42):
        require(2 * 11 + x + y <= order, ("unsafe audit order", order))
        for cut_x in range(x - 1, order - x):
            for cut_y in range(y - 1, order - y):
                if critical_vertices(x, cut_x).intersection(critical_vertices(y, cut_y)):
                    continue
                for a in range(order):
                    for distance in range(1, 12):
                        b = (a + distance) % order
                        edge = [a, b]
                        if not local_edge_admissible(edge, order, x, cut_x):
                            continue
                        if not local_edge_admissible(edge, order, y, cut_y):
                            continue

                        after_x = split_local_sequence(edge, order, x, cut_x)
                        after_y = split_local_sequence(edge, order, y, cut_y)
                        require(after_x is not None and after_y is not None, "first split")

                        transported_y = transport_cut(cut_y, cut_x, x)
                        transported_x = transport_cut(cut_x, cut_y, y)
                        xy = split_local_sequence(after_x, order + x, y, transported_y)
                        yx = split_local_sequence(after_y, order + y, x, transported_x)
                        require(xy is not None and yx is not None, (
                            "cross-preservation", order, cut_x, cut_y, a, b
                        ))
                        require(xy == yx, ("local noncommutation", order, cut_x, cut_y, a, b, xy, yx))
                        require(
                            max(circle_length(u, v, order + x + y) for u, v in zip(xy, xy[1:])) <= 11,
                            ("descendant length", order, cut_x, cut_y, a, b, xy),
                        )
                        digest.update(bytes((order, cut_x, cut_y, a, b, *xy, 255)))
                        checked += 1
    return checked, digest.hexdigest()


def verify_document(data: dict[str, object], grid: int, run_local_audit: bool) -> dict[str, object]:
    require(grid >= 0, "grid must be nonnegative")
    require(data.get("schema") == "bhr-small-a-mantle-v1", "schema")
    require(tuple(data.get("support", [])) == SUPPORT, "support")
    cases = data.get("cases")
    require(isinstance(cases, list) and len(cases) == 11, "case count")

    seen: set[int] = set()
    source_steps = 0
    family_states = 0
    squares = 0
    record = hashlib.sha256()
    improved_seed_record = hashlib.sha256()
    seed_orders: list[int] = []
    improved_seed_counts: list[tuple[int, int, int]] = []
    improved_prefix_rows = 0
    safe_eleven_prefix_rows = 0
    safe_eleven_prefix_overlapping_rows = 0

    for case_object in cases:
        require(isinstance(case_object, dict), "case object")
        case = case_object
        residue = tuple(case["residue_case"])
        require(residue[:2] == (1, 1) and 1 <= residue[2] <= 11, ("residue", residue))
        s = int(residue[2])
        require(s not in seen, ("duplicate residue", s))
        seen.add(s)

        source = case["source"]
        require(isinstance(source, dict), "source")
        source_path = list(source["path"])
        source_counts = tuple(source["counts"])
        source_cuts = {int(k): int(v) for k, v in source["selected_growth_cuts"].items()}
        require(set(source_cuts) == set(MODES), ("source cuts", s))
        require(source_counts[0] == 1 and source_counts[1] % 2 == 1, ("source parity", s))
        require((source_counts[2] - s) % 11 == 0, ("source residue", s))
        verify_realization(source_path, source_counts)
        for mode in MODES:
            growth_incidence(source_path, mode, source_cuts[mode])

        start = (source_path, source_cuts)
        after_2 = step(start, 2)
        after_11 = step(start, 11)
        first = step(after_2, 11)
        second = step(after_11, 2)
        source_steps += 4
        require(first == second, ("source operations do not commute", s))

        seed = case["safe_seed"]
        require(isinstance(seed, dict), "safe seed")
        seed_path = list(seed["path"])
        seed_counts = tuple(seed["counts"])
        seed_cuts = {int(k): int(v) for k, v in seed["selected_growth_cuts"].items()}
        require(seed_counts == EXPECTED_SEEDS[s], ("seed counts", s, seed_counts))
        require(seed_counts == (source_counts[0], source_counts[1] + 2, source_counts[2] + 11), s)
        require(first == (seed_path, seed_cuts), ("stored seed endpoint", s))
        verify_realization(seed_path, seed_counts)
        maximum = max(circle_length(a, b, len(seed_path)) for a, b in zip(seed_path, seed_path[1:]))
        require(maximum == 11, ("seed maximum", s, maximum))
        require(2 * maximum + sum(MODES) <= len(seed_path), ("safe margin", s, len(seed_path)))
        require(
            not critical_vertices(2, seed_cuts[2]).intersection(
                critical_vertices(11, seed_cuts[11])
            ),
            ("overlapping target seed intervals", s, seed_cuts),
        )
        seed_orders.append(len(seed_path))

        # Proved target-specific refinement: when 11-growth alone reaches order
        # 35 and the two critical intervals are disjoint, the intermediate
        # state is already a safe seed and the initial 2-growth can be omitted.
        prefix_intervals_overlap = bool(
            critical_vertices(2, after_11[1][2]).intersection(
                critical_vertices(11, after_11[1][11])
            )
        )
        if len(after_11[0]) >= 35:
            safe_eleven_prefix_rows += 1
            safe_eleven_prefix_overlapping_rows += int(prefix_intervals_overlap)
        if len(after_11[0]) >= 35 and not prefix_intervals_overlap:
            family_seed = after_11
            family_seed_counts = (
                source_counts[0], source_counts[1], source_counts[2] + 11
            )
            improved_prefix_rows += 1
        else:
            family_seed = (seed_path, seed_cuts)
            family_seed_counts = seed_counts
        verify_realization(family_seed[0], family_seed_counts)
        family_maximum = max(
            circle_length(a, b, len(family_seed[0]))
            for a, b in zip(family_seed[0], family_seed[0][1:])
        )
        require(2 * family_maximum + sum(MODES) <= len(family_seed[0]), (
            "refined safe margin", s, len(family_seed[0])
        ))
        require(
            not critical_vertices(2, family_seed[1][2]).intersection(
                critical_vertices(11, family_seed[1][11])
            ),
            ("overlapping selected refined seed", s, family_seed[1]),
        )
        improved_seed_counts.append(family_seed_counts)
        improved_seed_record.update(json.dumps(
            [s, family_seed_counts, family_seed[1], family_seed[0]],
            separators=(",", ":"), sort_keys=True
        ).encode())
        improved_seed_record.update(b"\n")

        family: dict[tuple[int, int], State] = {}
        for q in range(grid + 1):
            for r in range(grid + 1):
                route_qr = advance_repeated(advance_repeated(family_seed, 2, q), 11, r)
                route_rq = advance_repeated(advance_repeated(family_seed, 11, r), 2, q)
                require(route_qr == route_rq, ("grid route mismatch", s, q, r))
                expected = (
                    1,
                    family_seed_counts[1] + 2 * q,
                    family_seed_counts[2] + 11 * r,
                )
                verify_realization(route_qr[0], expected)
                family[q, r] = route_qr
                record.update(json.dumps(
                    [s, q, r, route_qr[1], route_qr[0]], separators=(",", ":"), sort_keys=True
                ).encode())
                record.update(b"\n")
                family_states += 1

        for q in range(grid):
            for r in range(grid):
                state = family[q, r]
                require(step(step(state, 2), 11) == step(step(state, 11), 2), (
                    "grid square", s, q, r
                ))
                squares += 1

    require(seen == set(range(1, 12)), ("residue coverage", seen))
    require(improved_prefix_rows == 2, ("improved prefix rows", improved_prefix_rows))
    require(
        safe_eleven_prefix_rows == 8,
        ("safe eleven-prefix rows", safe_eleven_prefix_rows),
    )
    require(
        safe_eleven_prefix_overlapping_rows == 6,
        ("overlapping eleven-prefix rows", safe_eleven_prefix_overlapping_rows),
    )
    require(
        sorted(counts[2] for counts in improved_seed_counts) == list(range(20, 31)),
        ("improved c representatives", improved_seed_counts),
    )
    require(
        max(counts[1] for counts in improved_seed_counts) == 13,
        ("improved uniform b threshold", improved_seed_counts),
    )
    local_checked, local_digest = local_safe_margin_audit() if run_local_audit else (0, "skipped")
    return {
        "python": platform.python_version(),
        "residue_classes": len(seen),
        "source_derivation_steps": source_steps,
        "minimum_seed_order": min(seed_orders),
        "maximum_seed_order": max(seed_orders),
        "safe_margin": "35<=36",
        "grid": grid,
        "family_states_checked": family_states,
        "commuting_squares_checked": squares,
        "family_record_sha256": record.hexdigest(),
        "improved_prefix_rows": improved_prefix_rows,
        "safe_eleven_prefix_rows": safe_eleven_prefix_rows,
        "safe_eleven_prefix_overlapping_rows": safe_eleven_prefix_overlapping_rows,
        "improved_seed_set_sha256": improved_seed_record.hexdigest(),
        "improved_uniform_odd_b_threshold": 13,
        "local_edge_cut_configurations_checked": local_checked,
        "local_edge_cut_sha256": local_digest,
    }


def negative_tests(data: dict[str, object]) -> int:
    mutations = []

    duplicate_vertex = deepcopy(data)
    duplicate_vertex["cases"][0]["source"]["path"][0] = duplicate_vertex["cases"][0]["source"]["path"][1]
    mutations.append(duplicate_vertex)

    shifted_cut = deepcopy(data)
    shifted_cut["cases"][4]["safe_seed"]["selected_growth_cuts"]["2"] += 1
    mutations.append(shifted_cut)

    duplicate_residue = deepcopy(data)
    duplicate_residue["cases"][10]["residue_case"] = [1, 1, 10]
    mutations.append(duplicate_residue)

    rejected = 0
    for mutated in mutations:
        try:
            verify_document(mutated, grid=0, run_local_audit=False)
        except (AuditFailure, KeyError, TypeError, ValueError):
            rejected += 1
    require(rejected == len(mutations), ("negative tests", rejected, len(mutations)))
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--grid", type=int, default=8)
    args = parser.parse_args()

    raw = args.certificate.read_bytes()
    certificate_hash = hashlib.sha256(raw).hexdigest()
    require(certificate_hash == PINNED_CERTIFICATE_SHA256, ("certificate hash", certificate_hash))
    data = json.loads(raw)
    summary = verify_document(data, grid=args.grid, run_local_audit=True)
    summary["certificate_sha256"] = certificate_hash
    summary["negative_tests_rejected"] = negative_tests(data)
    for key in sorted(summary):
        print(f"{key}={summary[key]}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
