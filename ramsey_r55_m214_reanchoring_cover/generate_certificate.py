#!/usr/bin/env python3
"""Produce the complete two-mark incidence-orbit certificate, not Ramsey graphs."""

import json
from math import factorial


def orbit_rows(kind, size, margin, epsilon):
    rows = []
    for intersection in range(margin + 1):
        bins = [size - 2 * margin + intersection,
                margin - intersection, margin - intersection, intersection]
        if min(bins) < 0:
            continue
        multiplicity = factorial(size)
        for count in bins:
            multiplicity //= factorial(count)
        family = "E_right_77" if kind == "E77" else (
            "C_right_77" if bins[0] else "C_split_77_partition")
        rows.append({"kind": kind, "epsilon": epsilon, "bins": bins,
                     "labeled_multiplicity": multiplicity, "family": family})
    return rows


def certificate():
    return {
        "schema": 1,
        "bin_order": ["00", "01", "10", "11"],
        "excess_placements": {"E8": 13, "E77": 78, "C8": 30, "C77": 435},
        "families": [
            {"name": "E_left_8", "excess": [[5, 2]], "anchor_choices_min": 12,
             "exact_central_red_neighbors": 15, "partner_min": 9},
            {"name": "E_right_77", "excess": [[11, 1], [12, 1]], "anchor_choices_min": 4,
             "exact_central_red_neighbors": 15, "partner_min": 9},
            {"name": "C_right_8", "excess": [[42, 2]], "anchor_choices_min": 16,
             "exact_central_red_neighbors": 15, "partner_min": 9},
            {"name": "C_right_77", "excess": [[41, 1], [42, 1]], "anchor_choices_min": 1,
             "exact_central_red_neighbors": 15, "partner_min": 9},
            {"name": "C_split_77_partition", "excess": [[28, 1], [42, 1]],
             "anchor_choices_min": 28, "exact_central_red_neighbors": 14, "partner_min": 8}
        ],
        "incidence_orbits": orbit_rows("E77", 30, 13, None)
            + orbit_rows("C77", 28, 14, 0) + orbit_rows("C77", 28, 13, 1),
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), sort_keys=True, indent=2))
