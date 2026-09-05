#!/usr/bin/env python3
"""Mutation tests for the independent certificate checker."""

import copy
import json
from pathlib import Path

from check_certificate import require, validate


def main():
    good = json.loads(Path(__file__).with_name("certificate.json").read_text())
    validate(good)
    mutations = []
    bad = copy.deepcopy(good)
    bad["incidence_orbits"].pop()
    mutations.append(bad)
    bad = copy.deepcopy(good)
    bad["incidence_orbits"][14]["family"] = "C_right_77"
    mutations.append(bad)
    bad = copy.deepcopy(good)
    bad["incidence_orbits"][0]["labeled_multiplicity"] += 1
    mutations.append(bad)
    bad = copy.deepcopy(good)
    bad["families"][4]["partner_min"] = 9
    mutations.append(bad)
    bad = copy.deepcopy(good)
    bad["families"][1]["excess"] = [[4, 1], [5, 1]]
    mutations.append(bad)
    bad = copy.deepcopy(good)
    bad["families"][2]["anchor_choices_min"] = 17
    mutations.append(bad)
    bad = copy.deepcopy(good)
    bad["excess_placements"]["E77"] += 390
    mutations.append(bad)
    bad = copy.deepcopy(good)
    bad["incidence_orbits"][0]["bins"][0] -= 1
    mutations.append(bad)
    bad = copy.deepcopy(good)
    bad["families"].pop()
    mutations.append(bad)
    for index, bad in enumerate(mutations):
        rejected = False
        try:
            validate(bad)
        except ValueError:
            rejected = True
        require(rejected, f"mutation {index} was accepted")
    print(f"PASS negative controls={len(mutations)}")


if __name__ == "__main__":
    main()
