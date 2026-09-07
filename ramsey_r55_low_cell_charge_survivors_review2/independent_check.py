#!/usr/bin/env python3
"""Independent exact checker for the 189 low-cell charge survivors.

This file imports no code from the reviewed package.  It reconstructs the
published uniform allocation from its mathematical description and finds each
pointwise neighbor row by a degree-class count DP, rather than the target's
per-label bitset DP.  It also checks the target's compact fixture directly.
"""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys


U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
GAPS = (7, 7, 7, 7, 7, None, 9, 9, 9, 7, 7, 7, 7)
FIELDS = {
    "cell",
    "cell_sizes",
    "degrees",
    "deficiencies",
    "local_degrees",
    "anchors",
    "neighbor_selections",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def is_int(value: object, low: int, high: int) -> bool:
    return type(value) is int and low <= value <= high


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def graphical(sequence: list[int]) -> bool:
    """Exact conjugate-partition form of the Erdos--Gallai criterion."""
    n = len(sequence)
    if any(type(x) is not int or x < 0 or x >= n for x in sequence):
        return False
    if sum(sequence) & 1:
        return False
    d = sorted(sequence, reverse=True)
    prefix = 0
    for k, value in enumerate(d, 1):
        prefix += value
        tail = sum(k if x >= k else x for x in d[k:])
        if prefix > k * (k - 1) + tail:
            return False
    return True


def decode_graph6(word: str) -> tuple[list[int], list[list[int]]]:
    """Decode a short graph6 record from the byte-level specification."""
    require(isinstance(word, str) and len(word) > 1, "malformed graph6 record")
    n = ord(word[0]) - 63
    require(n == 22, "unexpected graph6 order")
    need_bits = n * (n - 1) // 2
    require(len(word) == 1 + (need_bits + 5) // 6, "wrong graph6 length")
    chunks = [ord(c) - 63 for c in word[1:]]
    require(all(0 <= x < 64 for x in chunks), "bad graph6 character")
    bits = []
    for chunk in chunks:
        bits.extend((chunk >> shift) & 1 for shift in range(5, -1, -1))
    require(not any(bits[need_bits:]), "nonzero graph6 padding")
    matrix = [[0] * n for _ in range(n)]
    at = 0
    for j in range(1, n):
        for i in range(j):
            matrix[i][j] = matrix[j][i] = bits[at]
            at += 1
    return sorted(sum(row) for row in matrix), matrix


def check_interface(word: str) -> list[int]:
    degrees, matrix = decode_graph6(word)
    require(sum(degrees) == 218 and degrees.count(5) == 1, "bad interface degrees")
    for vertices in itertools.combinations(range(22), 4):
        require(
            not all(matrix[i][j] for i, j in itertools.combinations(vertices, 2)),
            "red K4 in interface",
        )
    for vertices in itertools.combinations(range(22), 5):
        require(
            not all(not matrix[i][j] for i, j in itertools.combinations(vertices, 2)),
            "blue K5 in interface",
        )
    return degrees


def q_threshold(n: int) -> int:
    return (2 * (U[n] - 6) + n - 1) // n


def high_multiplicity(n: int) -> int:
    threshold = q_threshold(n)
    numerator = 2 * (U[n] - 6) - n * (threshold - 1)
    denominator = 14 - threshold
    return (numerator + denominator - 1) // denominator


def cells() -> list[tuple[int, int, int]]:
    return [
        (d, p, q)
        for d in range(18, 25)
        for p in range(18, 25)
        for q in range(q_threshold(d), 14)
    ]


def balanced_word(n: int, total: int, pin: int | None = None) -> list[int]:
    count = n - (pin is not None)
    base, extra = divmod(total - (pin or 0), count)
    result = ([] if pin is None else [pin]) + [base + 1] * extra + [base] * (count - extra)
    require(graphical(result), "independently generated local word is nongraphical")
    return result


def grouped_subset(
    degrees: list[int],
    vertex: int,
    required: list[int],
    cardinality: int,
    total: int,
) -> list[int]:
    """Find a subset by counts within degree classes.

    States store one count-vector for each (cardinality, degree sum).  This is
    independent of the reviewed individual-label bitset recurrence.
    """
    candidates = [v for v in range(43) if v != vertex and v not in required]
    groups: list[tuple[int, list[int]]] = []
    for degree in sorted(set(degrees[v] for v in candidates)):
        groups.append((degree, [v for v in candidates if degrees[v] == degree]))
    need = cardinality - len(required)
    remainder = total - sum(degrees[v] for v in required)
    require(need >= 0 and remainder >= 0, "invalid required subset")
    states: dict[tuple[int, int], tuple[int, ...]] = {(0, 0): ()}
    for degree, labels in groups:
        next_states: dict[tuple[int, int], tuple[int, ...]] = {}
        for (used, weight), vector in states.items():
            for take in range(min(len(labels), need - used) + 1):
                key = used + take, weight + take * degree
                if key[0] <= need and key[1] <= remainder and key not in next_states:
                    next_states[key] = vector + (take,)
        states = next_states
    require((need, remainder) in states, "no degree-class neighbor row")
    vector = states[need, remainder]
    selected = list(required)
    for (_, labels), take in zip(groups, vector):
        selected.extend(labels[:take])
    require(len(selected) == cardinality, "bad reconstructed row cardinality")
    require(sum(degrees[v] for v in selected) == total, "bad reconstructed row sum")
    return sorted(selected)


def build_witness(d: int, p: int, q: int, anchor_degrees: list[int]) -> dict[str, object]:
    require((d, p, q) in set(cells()), "cell outside the scalar cover")
    k = 20 if (d + p) % 2 == 0 else 21
    degrees = [d, p, k] + [22] * 20 + [23] * 20
    require(graphical(degrees) and graphical([42 - x for x in degrees]), "global profile failure")

    red = [6, 6, 6] + [5] * 20 + [9] * 20
    red[2] += (sum(U[x] for x in degrees) - 298) % 3
    omega = sum(
        21 if x in (18, 24) else 12 if x in (19, 23) else 3 if x in (20, 22) else 0
        for x in degrees
    )
    require((1247 - omega) % 2 == 0, "nonintegral deficiency total")
    delta = (1247 - omega) // 2
    blue_budget = delta - sum(red)
    blue = [3] * 43
    priority = [v for v in (0, 1) if degrees[v] == 18]
    order = priority + list(range(3, 43)) + [v for v in (0, 1, 2) if v not in priority]
    for step in range(blue_budget - 129):
        blue[order[step % 43]] += 1

    local: dict[str, list[list[int]]] = {"red": [], "blue": []}
    for v, red_degree in enumerate(degrees):
        for color in ("red", "blue"):
            n = red_degree if color == "red" else 42 - red_degree
            deficiency = (red if color == "red" else blue)[v]
            if color == "red" and 3 <= v < 23:
                word = list(anchor_degrees)
            elif color == "red" and v >= 23:
                word = [5] + [10] * 21 + [11]
            else:
                pin = q if color == "red" and v < 2 else None
                word = balanced_word(n, 2 * (U[n] - deficiency), pin)
            require(graphical(word), "local graphicality failure")
            local[color].append(word)

    half_edges = sum(degrees) // 2
    rows = []
    for v, red_degree in enumerate(degrees):
        if v < 2:
            required = [1 - v]
        elif 3 <= v < 23:
            required = [v + 20]
        elif v >= 23:
            required = [v - 20]
        else:
            required = []
        e_red = U[red_degree] - red[v]
        blue_degree = 42 - red_degree
        e_blue = U[blue_degree] - blue[v]
        target = half_edges + e_red + e_blue - math.comb(blue_degree, 2)
        rows.append(grouped_subset(degrees, v, required, red_degree, target))

    return {
        "cell": [d, p, q],
        "cell_sizes": [q, d - 1 - q, p - 1 - q, 43 - d - p + q],
        "degrees": degrees,
        "deficiencies": {"red": red, "blue": blue},
        "local_degrees": local,
        "anchors": {
            "red": [
                {"vertex": v, "hub": v + 20, "interface": 8}
                for v in range(3, 23)
            ],
            "blue": [],
        },
        "neighbor_selections": rows,
    }


def check_witness(data: dict[str, object], interface_degrees: list[list[int]]) -> dict[str, int | str]:
    """Check the declared relaxation directly, without reviewed-package code."""
    require(type(data) is dict and set(data) == FIELDS, "wrong witness fields")
    key = data["cell"]
    require(type(key) is list and len(key) == 3 and all(type(x) is int for x in key), "bad cell")
    d, p, q = key
    require((d, p, q) in cells(), "cell not covered")
    expected_sizes = [q, d - 1 - q, p - 1 - q, 43 - d - p + q]
    require(data["cell_sizes"] == expected_sizes and min(expected_sizes) >= 0 and sum(expected_sizes) == 41, "partition failure")

    degrees = data["degrees"]
    require(type(degrees) is list and len(degrees) == 43, "degree vector length")
    require(all(is_int(x, 18, 24) for x in degrees), "degree bounds")
    require(degrees[:2] == [d, p], "root degrees")
    require(graphical(degrees) and graphical([42 - x for x in degrees]), "global graphicality")

    deficiencies = data["deficiencies"]
    profiles = data["local_degrees"]
    marks = data["anchors"]
    for value in (deficiencies, profiles, marks):
        require(type(value) is dict and set(value) == {"red", "blue"}, "bad color fields")

    totals: dict[str, int] = {}
    detected: dict[str, set[int]] = {}
    local_checks = 0
    for color in ("red", "blue"):
        side_deficits = deficiencies[color]
        side_profiles = profiles[color]
        require(type(side_deficits) is list and len(side_deficits) == 43, "bad deficits")
        require(type(side_profiles) is list and len(side_profiles) == 43, "bad profiles")
        total = 0
        detected[color] = set()
        for v in range(43):
            n = degrees[v] if color == "red" else 42 - degrees[v]
            delta = side_deficits[v]
            word = side_profiles[v]
            require(is_int(delta, 0, U[n]), "deficiency bounds")
            require(type(word) is list and len(word) == n, "local word length")
            require(all(is_int(x, max(0, n - 18), 13) for x in word), "local degree bounds")
            require(sum(word) == 2 * (U[n] - delta), "local edge total")
            require(graphical(word), "local nongraphical word")
            if delta <= 6:
                threshold = q_threshold(n)
                require(sum(x >= threshold for x in word) >= high_multiplicity(n), "high-partner multiplicity")
            if n == 22 and delta <= 5:
                require(min(word) >= 5, "dense-anchor minimum degree")
                if delta <= 4:
                    require(min(word) >= 6, "deficiency-four minimum degree")
                if 5 in word:
                    require(delta == 5 and word.count(5) == 1, "dense-anchor uniqueness")
                    detected[color].add(v)
            total += U[n] - delta
            local_checks += 1
        require(total % 3 == 0, "triangle divisibility")
        totals[color] = total

    require(deficiencies["red"][0] <= 6, "root is not low-deficiency")
    require(q in profiles["red"][0] and q in profiles["red"][1], "anonymous root reciprocity")
    wedge_sum = sum(value * (42 - value) for value in degrees)
    require(
        2 * (totals["red"] + totals["blue"])
        == 6 * math.comb(43, 3) - 3 * wedge_sum,
        "Goodman identity",
    )

    prescribed: dict[tuple[int, int], str] = {(0, 1): "red"}

    def prescribe(i: int, j: int, color: str) -> None:
        pair = tuple(sorted((i, j)))
        require(i != j and prescribed.get(pair, color) == color, "pair-color conflict")
        prescribed[pair] = color

    charges: dict[str, int] = {}
    for color in ("red", "blue"):
        other = "blue" if color == "red" else "red"
        side_marks = marks[color]
        require(type(side_marks) is list, "bad anchor map")
        seen: set[int] = set()
        fibers: dict[int, list[int]] = {}
        charge = 0
        for mark in side_marks:
            require(type(mark) is dict and set(mark) == {"vertex", "hub", "interface"}, "bad anchor row")
            v, hub, interface = mark["vertex"], mark["hub"], mark["interface"]
            require(is_int(v, 0, 42) and is_int(hub, 0, 42) and is_int(interface, 0, 12), "anchor indices")
            require(v != hub and v not in seen, "duplicate/bad anchor")
            seen.add(v)
            require(v in detected[color], "marked vertex not detected")
            require(sorted(profiles[color][v]) == interface_degrees[interface], "wrong interface degree word")
            hub_degree = degrees[hub] if color == "red" else 42 - degrees[hub]
            require(hub_degree <= 23 and 5 in profiles[color][hub], "bad hub")
            prescribe(v, hub, color)
            fibers.setdefault(hub, []).append(v)
            if hub_degree == 23:
                gap = GAPS[interface]
                require(gap is not None and deficiencies[color][hub] >= gap, "pointwise gap")
                charge += gap
        require(seen == detected[color], "incomplete anchor map")
        for hub, vertices in fibers.items():
            hub_degree = degrees[hub] if color == "red" else 42 - degrees[hub]
            if hub_degree >= 21:
                require(len(vertices) <= 1, "high-degree hub collision")
            elif hub_degree in (19, 20):
                require(len(vertices) <= 4, "low-degree fiber overflow")
                for v, w in itertools.combinations(vertices, 2):
                    prescribe(v, w, other)
        paid = sum(
            deficiencies[color][v]
            for v in range(43)
            if (degrees[v] if color == "red" else 42 - degrees[v]) == 23
        )
        require(paid >= charge, "aggregate charge")
        charges[color] = charge

    rows = data["neighbor_selections"]
    require(type(rows) is list and len(rows) == 43, "neighbor row count")
    m = sum(degrees) // 2
    for v, row in enumerate(rows):
        require(type(row) is list and len(row) == degrees[v], "neighbor row cardinality")
        require(all(is_int(w, 0, 42) and w != v for w in row), "neighbor row label")
        require(len(row) == len(set(row)), "duplicate neighbor")
        e_red = sum(profiles["red"][v]) // 2
        e_blue = sum(profiles["blue"][v]) // 2
        cross = sum(degrees[w] for w in row) - 2 * e_red - degrees[v]
        outside_red = math.comb(42 - degrees[v], 2) - e_blue
        require(cross >= 0 and m == e_red + cross + outside_red + degrees[v], "pointwise edge partition")
    for (v, w), color in prescribed.items():
        expected = color == "red"
        require((w in rows[v]) == expected and (v in rows[w]) == expected, "prescribed pair failure")

    return {
        "red_anchors": len(detected["red"]),
        "blue_anchors": len(detected["blue"]),
        "red_charge": charges["red"],
        "blue_charge": charges["blue"],
        "delta": sum(sum(deficiencies[color]) for color in ("red", "blue")),
        "red_triangles": totals["red"] // 3,
        "blue_triangles": totals["blue"] // 3,
        "local_checks": local_checks,
        "status": "INDEPENDENT_WITNESS_PASS",
    }


def run(target_directory: Path) -> dict[str, object]:
    params = json.loads((target_directory / "parameters.json").read_text(encoding="utf-8"))
    expected = json.loads((target_directory / "expected.json").read_text(encoding="utf-8"))
    fixture = json.loads((target_directory / "allocation.json").read_text(encoding="utf-8"))
    require(len(params["interfaces"]) == 13, "interface input count")
    interface_degrees = [check_interface(word) for word in params["interfaces"]]
    require(interface_degrees[8] == [5] + [9] * 2 + [10] * 14 + [11] * 5, "interface-8 degree word")

    derived_q0 = [q_threshold(n) for n in range(18, 25)]
    derived_multiplicity = [high_multiplicity(n) for n in range(18, 25)]
    require(derived_q0 == params["q0"], "q0 is not derived from U and deficiency six")
    require(derived_multiplicity == params["multiplicity"], "multiplicity table mismatch")
    scalar_cells = cells()
    require(len(scalar_cells) == 189, "wrong scalar cell count")

    stream = hashlib.sha256()
    deltas = []
    blue_budgets = []
    budget_rows: dict[tuple[int, int], list[int]] = {}
    blue_delta_by_degree: dict[int, int] = {}
    distinct_rows = set()
    local_checks = 0
    for key in scalar_cells:
        witness = build_witness(*key, interface_degrees[8])
        result = check_witness(witness, interface_degrees)
        require((result["red_anchors"], result["blue_anchors"]) == (20, 0), "anchor count")
        require((result["red_charge"], result["blue_charge"]) == (180, 0), "charge count")
        deltas.append(result["delta"])
        blue_budgets.append(sum(witness["deficiencies"]["blue"]))
        d, p, _ = key
        summary = [
            d,
            p,
            witness["degrees"][2],
            witness["deficiencies"]["red"][2],
            result["delta"],
            sum(witness["deficiencies"]["red"]),
            sum(witness["deficiencies"]["blue"]),
        ]
        require((d, p) not in budget_rows or budget_rows[d, p] == summary, "budget depends on q")
        budget_rows[d, p] = summary
        for v, red_degree in enumerate(witness["degrees"]):
            blue_degree = 42 - red_degree
            blue_delta_by_degree[blue_degree] = max(
                blue_delta_by_degree.get(blue_degree, 0),
                witness["deficiencies"]["blue"][v],
            )
        local_checks += result["local_checks"]
        for row in witness["neighbor_selections"]:
            distinct_rows.add(tuple(row))
        stream.update(json.dumps([witness, result], sort_keys=True, separators=(",", ":")).encode() + b"\n")

    fixture_result = check_witness(fixture, interface_degrees)
    fixture_rows = fixture["neighbor_selections"]
    fixture_asymmetry = sum(
        (j in fixture_rows[i]) != (i in fixture_rows[j])
        for i in range(43)
        for j in range(i + 1, 43)
    )
    fixture_intersection = len(set(fixture_rows[0]) & set(fixture_rows[1]))
    require(fixture_asymmetry == 400 and fixture_intersection == 17, "published nonphysical fixture changed")
    require(expected["allocation_stream_sha256"] == "32798b0d26183ca9a53a70976dddf267c1fb5b823fdb07b34def560a7b076bdc", "target stream hash changed")
    require(expected["fixture_sha256"] == canonical_hash(fixture), "target fixture hash mismatch")
    require(list(budget_rows.values()) == expected["budget_rows"], "49 target budget rows mismatch")

    coarse_counts = dict(zip(range(9, 14), params["r35_counts"]))
    coarse_labels = sum(coarse_counts[q] for _, _, q in scalar_cells)
    require(coarse_labels == 18767, "coarse-label lift count")

    def rejects(mutant: dict[str, object]) -> bool:
        try:
            check_witness(mutant, interface_degrees)
        except ValueError:
            return True
        return False

    mutants = []
    mutant = copy.deepcopy(fixture)
    mutant["cell"] = [18, 18, 8]
    mutants.append(mutant)
    mutant = copy.deepcopy(fixture)
    mutant["anchors"]["red"].pop()
    mutants.append(mutant)
    mutant = copy.deepcopy(fixture)
    mutant["anchors"]["red"][0]["hub"] = 24
    mutants.append(mutant)
    mutant = copy.deepcopy(fixture)
    mutant["deficiencies"]["red"][23] = 8
    mutants.append(mutant)
    mutant = copy.deepcopy(fixture)
    mutant["neighbor_selections"][0][0] = 0
    mutants.append(mutant)
    require(all(rejects(mutant) for mutant in mutants), "independent checker accepted a perturbation")

    independent_fixture = build_witness(18, 18, 9, interface_degrees[8])
    independent_rows = independent_fixture["neighbor_selections"]
    independent_asymmetry = sum(
        (j in independent_rows[i]) != (i in independent_rows[j])
        for i in range(43)
        for j in range(i + 1, 43)
    )
    independent_intersection = len(set(independent_rows[0]) & set(independent_rows[1]))

    return {
        "status": "INDEPENDENT_189_CHARGE_SURVIVORS_PASS",
        "scalar_cells": len(scalar_cells),
        "degree_pairs": 49,
        "coarse_labels_retained_only": coarse_labels,
        "q0": derived_q0,
        "multiplicity": derived_multiplicity,
        "independent_global_graphical_checks": 2 * len(scalar_cells),
        "independent_local_graphical_checks": local_checks,
        "independent_neighbor_rows": 43 * len(scalar_cells),
        "distinct_neighbor_row_words": len(distinct_rows),
        "delta_range": [min(deltas), max(deltas)],
        "blue_budget_range": [min(blue_budgets), max(blue_budgets)],
        "red_anchors_each": 20,
        "degree23_hubs_each": 20,
        "red_charge_each": 180,
        "blue_anchors_each": 0,
        "maximum_blue_deficiency_by_blue_degree": {
            str(key): blue_delta_by_degree[key] for key in sorted(blue_delta_by_degree)
        },
        "rejected_perturbations": len(mutants),
        "independent_stream_sha256": stream.hexdigest(),
        "target_stream_sha256": expected["allocation_stream_sha256"],
        "target_fixture_sha256": canonical_hash(fixture),
        "target_fixture_status": fixture_result["status"],
        "target_fixture_asymmetric_pairs": fixture_asymmetry,
        "target_fixture_root_intersection": fixture_intersection,
        "independent_fixture_asymmetric_pairs": independent_asymmetry,
        "independent_fixture_root_intersection": independent_intersection,
        "physical_graph_claimed": False,
        "scalar_cells_excluded": 0,
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 -B independent_check.py /path/to/ramsey_r55_low_cell_charge_survivors")
    target_directory = Path(sys.argv[1]).resolve()
    result = run(target_directory)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
