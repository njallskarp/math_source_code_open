#!/usr/bin/env python3
"""Clean-room exact audit of the height-2915 creation-sensitive certificate.

This checker imports no code from the target repository.  It reads only the
published seed and certificate, pins both by SHA-256, reconstructs the graph
and all relevant colored-five-set inequalities directly, and verifies the
integer coefficient identity edge by edge.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


SEED_RELATIVE = Path("ramsey_r55_k5_neutral_component/EXIT_GRAPH.json")
CERTIFICATE_RELATIVE = Path("ramsey_r55_creation_sensitive_cover/certificate.json")
SEED_SHA256 = "9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916"
CERTIFICATE_SHA256 = "50129540618fb010e8421778a3ca1f13b836bb820be1b52bc7e3577bb0b6c696"
TARGET_SOURCE_COMMIT = "1b50304a2f69cdcda5f00c60529be3fdf849cec6"
TARGET_PUBLICATION_COMMIT = "94a93c6794fc7c37f76a81936a02a666f9abea6e"

VERTICES = tuple(range(43))
EXCEPTIONAL = frozenset(range(3))
CENTRAL = frozenset(range(3, 43))
CENTRAL_EDGES = tuple(combinations(sorted(CENTRAL), 2))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":")) + "\n"
    return sha256(payload.encode("utf-8")).hexdigest()


def decode_seed(path: Path) -> tuple[int, ...]:
    require(file_sha256(path) == SEED_SHA256, "seed SHA-256 mismatch")
    document = json.loads(path.read_text())
    require(
        type(document) is dict
        and set(document) == {"format", "red_adjacency_hex"}
        and document["format"] == "r55-triple-degree-exact-mixed-graph-v1",
        "seed schema mismatch",
    )
    encoded = document["red_adjacency_hex"]
    require(type(encoded) is list and len(encoded) == 43, "seed row count")
    rows = tuple(int(value, 16) for value in encoded)
    require(all(0 <= row < 1 << 43 for row in rows), "seed bit range")
    require(all(not (rows[u] >> u & 1) for u in VERTICES), "seed loop")
    require(
        all((rows[u] >> v & 1) == (rows[v] >> u & 1) for u, v in combinations(VERTICES, 2)),
        "seed asymmetry",
    )
    return rows


def is_red(rows: tuple[int, ...], edge: tuple[int, int]) -> bool:
    u, v = edge
    return bool(rows[u] >> v & 1)


def color_sides(rows: tuple[int, ...], root: int, red: bool) -> tuple[int, ...]:
    return tuple(v for v in VERTICES if v != root and is_red(rows, tuple(sorted((root, v)))) == red)


def count_edges_of_color(rows: tuple[int, ...], vertices: tuple[int, ...], red: bool) -> int:
    return sum(is_red(rows, edge) == red for edge in combinations(vertices, 2))


def graph_audit(rows: tuple[int, ...]) -> tuple[list[tuple[int, tuple[int, ...]]], set[tuple[int, int]], str]:
    degrees = tuple(row.bit_count() for row in rows)
    require(degrees == (20,) * 3 + (21,) * 40, "degree profile mismatch")
    require(sum(degrees) // 2 == 450, "red edge count mismatch")
    require(all(is_red(rows, edge) for edge in combinations(sorted(EXCEPTIONAL), 2)), "E is not red K3")

    profiles = tuple(
        (
            count_edges_of_color(rows, color_sides(rows, root, True), True),
            count_edges_of_color(rows, color_sides(rows, root, False), False),
        )
        for root in sorted(EXCEPTIONAL)
    )
    require(profiles == ((92, 107),) * 3, "exceptional profiles mismatch")

    old_cliques: list[tuple[int, tuple[int, ...]]] = []
    mixed_old = 0
    for five in combinations(VERTICES, 5):
        colors = {is_red(rows, edge) for edge in combinations(five, 2)}
        if len(colors) == 1:
            red = int(colors.pop())
            old_cliques.append((red, five))
            mixed_old += int(bool(EXCEPTIONAL.intersection(five)))
    by_color = Counter(red for red, _ in old_cliques)
    require((by_color[1], by_color[0], mixed_old) == (176, 177, 0), "old K5 census mismatch")

    visible: set[tuple[int, int]] = set()
    for root in sorted(EXCEPTIONAL):
        for red in (False, True):
            side = sorted(CENTRAL.intersection(color_sides(rows, root, red)))
            visible.update(combinations(side, 2))
    require(len(visible) == 656 and len(set(CENTRAL_EDGES) - visible) == 124, "visibility census mismatch")
    return old_cliques, visible, canonical_digest([[red, list(five)] for red, five in old_cliques])


def colored_five_row(
    rows: tuple[int, ...], red: int, five: tuple[int, ...]
) -> tuple[dict[tuple[int, int], int], int, int]:
    """Return coefficients, RHS, and number of initially opposite free edges."""
    require(type(red) is int and red in (0, 1), "invalid forbidden color")
    require(len(five) == 5 and five == tuple(sorted(set(five))), "invalid five-set")
    coefficients: dict[tuple[int, int], int] = {}
    holes = 0
    for edge in combinations(five, 2):
        if edge[0] in EXCEPTIONAL:
            require(is_red(rows, edge) == bool(red), "fixed edge blocks forbidden color")
        else:
            same = is_red(rows, edge) == bool(red)
            coefficients[edge] = 1 if same else -1
            holes += int(not same)
    return coefficients, 1 - holes, holes


def full_mixed_audit(rows: tuple[int, ...]) -> tuple[int, Counter[int], Counter[int], str]:
    examined = 0
    rows_found: list[list[object]] = []
    widths: Counter[int] = Counter()
    holes: Counter[int] = Counter()
    for five in combinations(VERTICES, 5):
        if not EXCEPTIONAL.intersection(five):
            continue
        examined += 1
        for red in (0, 1):
            try:
                coefficients, rhs, hole_count = colored_five_row(rows, red, five)
            except ValueError:
                continue
            widths[len(coefficients)] += 1
            holes[hole_count] += 1
            rows_found.append(
                [
                    red,
                    list(five),
                    [[u, v, coefficient] for (u, v), coefficient in sorted(coefficients.items())],
                    rhs,
                ]
            )
    require(examined == 304590, "mixed five-set visit count")
    require(len(rows_found) == 31153 and widths == Counter({6: 31125, 3: 28}), "full mixed formula census")
    require(holes[1] == 2556, "one-hole formula census")
    return examined, widths, holes, canonical_digest(rows_found)


def load_certificate(path: Path) -> dict[str, object]:
    require(file_sha256(path) == CERTIFICATE_SHA256, "certificate SHA-256 mismatch")
    certificate = json.loads(path.read_text())
    require(
        type(certificate) is dict
        and set(certificate)
        == {
            "format",
            "seed_sha256",
            "denominator",
            "old_cliques",
            "mixed_cliques",
            "degrees",
            "profiles",
            "upper_penalties",
        },
        "certificate schema mismatch",
    )
    require(certificate["format"] == "r55-creation-sensitive-cover-dual-v1", "certificate format")
    require(certificate["seed_sha256"] == SEED_SHA256, "certificate seed provenance")
    return certificate


def audit_certificate(
    rows: tuple[int, ...], certificate: dict[str, object], visible: set[tuple[int, int]]
) -> dict[str, object]:
    denominator = certificate["denominator"]
    require(type(denominator) is int and denominator > 0, "invalid denominator")
    load = {edge: 0 for edge in CENTRAL_EDGES}
    seen: set[tuple[int, tuple[int, ...]]] = set()
    old_weight = 0
    mixed_weighted_rhs = 0
    selected_holes: Counter[int] = Counter()
    selected_missing: set[tuple[int, int]] = set()
    selected_types: Counter[tuple[int, int]] = Counter()

    for category in ("old_cliques", "mixed_cliques"):
        entries = certificate[category]
        require(type(entries) is list, f"{category} is not a list")
        for entry in entries:
            require(type(entry) is list and len(entry) == 3, f"invalid {category} row")
            red, raw_five, weight = entry
            require(
                type(raw_five) is list
                and all(type(v) is int for v in raw_five)
                and type(weight) is int
                and weight > 0,
                f"invalid {category} row fields",
            )
            five = tuple(raw_five)
            require((red, five) not in seen, "duplicate weighted five-set")
            seen.add((red, five))
            coefficients, rhs, hole_count = colored_five_row(rows, red, five)
            if category == "old_cliques":
                require(not EXCEPTIONAL.intersection(five), "old row meets E")
                require(hole_count == 0 and rhs == 1, "old row is not a seed K5")
                old_weight += weight
            else:
                roots = len(EXCEPTIONAL.intersection(five))
                require(roots in (1, 2), "selected mixed row root count")
                require(hole_count == 1 and rhs == 0, "selected mixed row is not one-hole")
                selected_holes[hole_count] += 1
                selected_types[(red, roots)] += 1
                missing = next(edge for edge, coefficient in coefficients.items() if coefficient == -1)
                require(missing in visible, "selected trigger is not visible")
                selected_missing.add(missing)
                mixed_weighted_rhs += weight * rhs
            for edge, coefficient in coefficients.items():
                load[edge] += weight * coefficient

    degree_multipliers: dict[int, int] = {}
    for entry in certificate["degrees"]:
        require(type(entry) is list and len(entry) == 2, "invalid degree multiplier")
        vertex, weight = entry
        require(
            type(vertex) is int
            and vertex in CENTRAL
            and type(weight) is int
            and weight != 0
            and vertex not in degree_multipliers,
            "invalid degree multiplier fields",
        )
        degree_multipliers[vertex] = weight

    profile_multipliers: dict[tuple[int, int], int] = {}
    for entry in certificate["profiles"]:
        require(type(entry) is list and len(entry) == 3, "invalid profile multiplier")
        root, red, weight = entry
        require(
            type(root) is int
            and root in EXCEPTIONAL
            and type(red) is int
            and red in (0, 1)
            and type(weight) is int
            and weight != 0
            and (root, red) not in profile_multipliers,
            "invalid profile multiplier fields",
        )
        profile_multipliers[root, red] = weight

    # A flip changes the red indicator by +1 on an initially blue edge and
    # by -1 on an initially red edge.  The same signed expression is a degree
    # change and a red-edge count change inside each fixed root side.  On a
    # blue side its negative is the corresponding blue-profile change.
    for edge in CENTRAL_EDGES:
        u, v = edge
        sign = 1 if not is_red(rows, edge) else -1
        equality_coefficient = degree_multipliers.get(u, 0) + degree_multipliers.get(v, 0)
        for (root, red), weight in profile_multipliers.items():
            if (
                is_red(rows, tuple(sorted((root, u)))) == bool(red)
                and is_red(rows, tuple(sorted((root, v)))) == bool(red)
            ):
                equality_coefficient += weight
        load[edge] += sign * equality_coefficient

    penalties: dict[tuple[int, int], int] = {}
    for entry in certificate["upper_penalties"]:
        require(type(entry) is list and len(entry) == 3, "invalid upper-box penalty")
        u, v, penalty = entry
        edge = (u, v)
        require(
            all(type(value) is int for value in entry)
            and edge in load
            and penalty > 0
            and edge not in penalties,
            "invalid upper-box penalty fields",
        )
        penalties[edge] = penalty

    residual = [
        denominator * int(edge in visible) - load[edge] + penalties.get(edge, 0)
        for edge in CENTRAL_EDGES
    ]
    require(min(residual) >= 0, "negative edge residual")
    numerator = old_weight + mixed_weighted_rhs - sum(penalties.values())
    bound = Fraction(numerator, denominator)
    require(bound > 38 and bound <= 39, "claimed integer boundary mismatch")

    expected_degrees = (3, 4, 5, 6, 7, 8, 9, 10, 13, 17, 39, 40, 41, 42)
    expected_profiles = ((0, 0), (0, 1), (1, 0), (1, 1), (2, 1))
    require(tuple(sorted(degree_multipliers)) == expected_degrees, "reduced degree set mismatch")
    require(tuple(sorted(profile_multipliers)) == expected_profiles, "reduced profile set mismatch")
    require(selected_types == Counter({(0, 1): 104, (1, 1): 119, (1, 2): 1}), "selected type census")

    without_penalties = [
        denominator * int(edge in visible) - load[edge] for edge in CENTRAL_EDGES
    ]
    require(min(without_penalties) < 0, "penalty corruption control did not fail")

    return {
        "scale": denominator,
        "old_rows": len(certificate["old_cliques"]),
        "mixed_rows": len(certificate["mixed_cliques"]),
        "old_weight": old_weight,
        "mixed_weighted_rhs": mixed_weighted_rhs,
        "degree_rows": len(degree_multipliers),
        "profile_rows": len(profile_multipliers),
        "box_rows": len(penalties),
        "box_penalty": sum(penalties.values()),
        "numerator": numerator,
        "bound": f"{bound.numerator}/{bound.denominator}",
        "integer_lower_bound": (numerator + denominator - 1) // denominator,
        "min_residual": min(residual),
        "max_residual": max(residual),
        "residual_sha256": canonical_digest(residual),
        "one_hole_rows": selected_holes[1],
        "distinct_visible_triggers": len(selected_missing),
        "degree_vertices": expected_degrees,
        "profile_sides": expected_profiles,
    }


def truth_table_audit() -> int:
    tested = 0
    for width in (3, 6):
        for forbidden in (0, 1):
            for original_bits in range(1 << width):
                original = tuple((original_bits >> i) & 1 for i in range(width))
                holes = sum(color != forbidden for color in original)
                coefficients = tuple(1 if color == forbidden else -1 for color in original)
                rhs = 1 - holes
                for flip_bits in range(1 << width):
                    flips = tuple((flip_bits >> i) & 1 for i in range(width))
                    lhs = sum(coefficient * flip for coefficient, flip in zip(coefficients, flips))
                    final = tuple(color ^ flip for color, flip in zip(original, flips))
                    require((lhs >= rhs) == (not all(color == forbidden for color in final)), "truth table mismatch")
                    tested += 1
    require(tested == 8320, "truth table case count")
    return tested


def tamper_controls(rows: tuple[int, ...], certificate: dict[str, object]) -> int:
    controls = 0
    bad = deepcopy(certificate["old_cliques"][0])
    bad[0] = 1 - bad[0]
    try:
        _, rhs, holes = colored_five_row(rows, bad[0], tuple(bad[1]))
    except ValueError:
        controls += 1
    else:
        require(not (holes == 0 and rhs == 1), "wrong old color accepted")
        controls += 1

    bad = deepcopy(certificate["mixed_cliques"][0])
    bad[0] = 1 - bad[0]
    try:
        _, rhs, holes = colored_five_row(rows, bad[0], tuple(bad[1]))
    except ValueError:
        controls += 1
    else:
        require(not (holes == 1 and rhs == 0), "wrong mixed color accepted")
        controls += 1

    require(certificate["upper_penalties"], "missing published penalties")
    controls += 1  # audit_certificate checked that deleting all penalties overloads an edge.
    require(controls == 3, "tamper control count")
    return controls


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target-root",
        type=Path,
        required=True,
        help="checkout of helgithorskarp/math_results at the pinned publication commit",
    )
    args = parser.parse_args()

    seed_path = args.target_root / SEED_RELATIVE
    certificate_path = args.target_root / CERTIFICATE_RELATIVE
    rows = decode_seed(seed_path)
    old_cliques, visible, old_digest = graph_audit(rows)
    examined, widths, hole_histogram, mixed_digest = full_mixed_audit(rows)
    certificate = load_certificate(certificate_path)
    result = audit_certificate(rows, certificate, visible)
    truth_cases = truth_table_audit()
    controls = tamper_controls(rows, certificate)

    print("independent R(5,5) creation-sensitive certificate audit: PASS")
    print(
        f"seed: red_edges=450 degrees=20^3+21^40 profiles=(92,107)^3 "
        f"old_K5=176R+177B mixed_old_K5=0"
    )
    print(f"visibility: visible={len(visible)} invisible={len(CENTRAL_EDGES) - len(visible)}")
    print(
        f"full mixed formula: visited={examined} rows={sum(widths.values())} "
        f"width3={widths[3]} width6={widths[6]} one_hole={hole_histogram[1]}"
    )
    print(
        f"selected certificate: old={result['old_rows']} mixed={result['mixed_rows']} "
        f"one_hole={result['one_hole_rows']} triggers={result['distinct_visible_triggers']}"
    )
    print(
        f"identity: scale={result['scale']} old_weight={result['old_weight']} "
        f"box_penalty={result['box_penalty']} numerator={result['numerator']} "
        f"bound={result['bound']} integer_lower_bound={result['integer_lower_bound']}"
    )
    print(
        f"residual: min={result['min_residual']} max={result['max_residual']} "
        f"sha256={result['residual_sha256']}"
    )
    print(
        "proved weaker hypothesis set: degrees="
        + ",".join(map(str, result["degree_vertices"]))
        + " profiles="
        + ",".join(f"{root}{'R' if red else 'B'}" for root, red in result["profile_sides"])
    )
    print(f"truth_table_cases={truth_cases} tamper_controls={controls}/3")
    print(f"old_K5_sha256={old_digest}")
    print(f"full_mixed_formula_sha256={mixed_digest}")
    print(f"seed_sha256={file_sha256(seed_path)}")
    print(f"certificate_sha256={file_sha256(certificate_path)}")


if __name__ == "__main__":
    main()
