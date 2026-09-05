#!/usr/bin/env python3
"""Independent composition/census checker; imports no generator or solver."""

import hashlib
import itertools
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compositions(total):
    for a in range(total + 1):
        for b in range(total - a + 1):
            for c in range(total - a - b + 1):
                yield [a, b, c, total - a - b - c]


def composition_weight(bins):
    remaining = sum(bins)
    weight = 1
    for size in bins:
        weight *= comb(remaining, size)
        remaining -= size
    return weight


def validate(data):
    require(set(data) == {"schema", "bin_order", "excess_placements", "families", "incidence_orbits"},
            "wrong certificate fields")
    require(data["schema"] == 1 and data["bin_order"] == ["00", "01", "10", "11"], "schema/bins")
    # Independent enumeration of two indistinguishable excess units BEFORE choosing an anchor.
    counts = Counter()
    for i, j in itertools.combinations_with_replacement(range(43), 2):
        units_in_e = int(i < 13) + int(j < 13)
        if units_in_e % 2:
            continue
        counts[("E" if units_in_e else "C") + ("8" if i == j else "77")] += 1
    require(dict(counts) == data["excess_placements"], "excess placement census")
    require(sum(counts.values()) == 556, "parity total")

    expected = []
    totals = {}
    for kind, epsilon in [("E77", None), ("C77", 0), ("C77", 1)]:
        size = 30 if kind == "E77" else 28
        margin = 20 - 7 if kind == "E77" else 21 - 7 - epsilon
        group = []
        for bins in compositions(size):
            if bins[2] + bins[3] != margin or bins[1] + bins[3] != margin:
                continue
            family = "E_right_77" if kind == "E77" else "C_right_77"
            if bins[0] == 0:
                require(kind == "C77" and epsilon == 0 and bins == [0, 14, 14, 0],
                        "unexpected no-common-blue orbit")
                family = "C_split_77_partition"
            group.append({"kind": kind, "epsilon": epsilon, "bins": bins,
                          "labeled_multiplicity": composition_weight(bins), "family": family})
        group.sort(key=lambda row: row["bins"][3])
        require(sum(row["labeled_multiplicity"] for row in group) == comb(size, margin) ** 2,
                "full pair-of-subsets coverage")
        expected.extend(group)
        totals[f"{kind}:{epsilon}"] = len(group)
    require(data["incidence_orbits"] == expected, "entry-level incidence orbit mismatch")

    names = ["E_left_8", "E_right_77", "C_right_8", "C_right_77", "C_split_77_partition"]
    marks = [[[5, 2]], [[11, 1], [12, 1]], [[42, 2]], [[41, 1], [42, 1]], [[28, 1], [42, 1]]]
    choices = [20 - 8, min(r["bins"][0] for r in expected if r["kind"] == "E77"),
               29 - (21 - 8), min(r["bins"][0] for r in expected if r["family"] == "C_right_77"), 28]
    wanted_families = []
    for i, name in enumerate(names):
        exact = 15 - int(i == 4)
        # The other 21-exact neighbors each have codegree at most 13.
        required = 200 - (21 - exact) * 13
        floor = (required + exact - 1) // exact
        require((floor - 1) * exact < required <= floor * exact, "sharp integer averaging")
        wanted_families.append({"name": name, "excess": marks[i], "anchor_choices_min": choices[i],
                                "exact_central_red_neighbors": exact, "partner_min": floor})
    require(data["families"] == wanted_families, "five-family transfer table")

    # Boundary/small-instance check: orbit multiplicities against literal pairs of subsets.
    small_pairs = 0
    for size in range(7):
        for margin in range(size + 1):
            subsets = list(map(set, itertools.combinations(range(size), margin)))
            observed = Counter()
            for left in subsets:
                for right in subsets:
                    bins = [0] * 4
                    for vertex in range(size):
                        bins[2 * int(vertex in left) + int(vertex in right)] += 1
                    observed[tuple(bins)] += 1
                    small_pairs += 1
            calculated = {tuple(b): composition_weight(b) for b in compositions(size)
                          if b[2] + b[3] == margin and b[1] + b[3] == margin}
            require(dict(observed) == calculated, "literal small-universe census")
    return totals, small_pairs


def main():
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name("certificate.json")
    require(len(sys.argv) <= 2, "usage: check_certificate.py [certificate.json]")
    raw = path.read_bytes()
    data = json.loads(raw)
    totals, small_pairs = validate(data)
    print("PASS excess placements=556 families=5")
    print(f"PASS incidence orbits={sum(totals.values())} groups=14,15,14 small_subset_pairs={small_pairs}")
    print("PASS exact-partner lower bounds=9,9,9,9,8 upper_bound=13")
    print("certificate_sha256=" + hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
