#!/usr/bin/env python3
"""Malformed-origin, coverage, branch and cube-translation controls."""

from copy import deepcopy
import json
from verify import ROOT, verify


def main():
    data = json.loads((ROOT / "certificate.json").read_text())
    raw = (ROOT / "selection.json").read_bytes()
    verify(data, raw)
    changes = []
    bad = deepcopy(data)
    bad["blue_pair_witnesses"][0][2] = [0, 1, 2]
    changes.append(bad)
    bad = deepcopy(data)
    bad["blue_pair_witnesses"][0][2] = [0, 2, 4]
    changes.append(bad)
    bad = deepcopy(data)
    bad["red_pair_witnesses"][0][2] = [0, 2]
    changes.append(bad)
    bad = deepcopy(data)
    bad["red_pair_witnesses"][0][2] = [1, 2]
    changes.append(bad)
    bad = deepcopy(data)
    bad["blue_pair_witnesses"].pop()
    changes.append(bad)
    bad = deepcopy(data)
    bad["red_pair_witnesses"].append(bad["red_pair_witnesses"][0])
    changes.append(bad)
    bad = deepcopy(data)
    bad["target_edges"] = 12
    changes.append(bad)
    bad = deepcopy(data)
    bad["anchors"] = [0, 1, 2]
    changes.append(bad)
    bad = deepcopy(data)
    bad["forced_pair"] = [8, 10]
    changes.append(bad)
    bad = deepcopy(data)
    bad["cell"] = [7, 8, 9, 10, 11, 12, 14]
    changes.append(bad)
    rejected = 0
    for bad in changes:
        try:
            verify(bad, raw)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("corrupt certificate accepted")
    try:
        verify(data, raw.replace(b'"08e2"', b'"08e3"'))
    except ValueError:
        rejected += 1
    else:
        raise RuntimeError("changed selection accepted")
    print(f"PASS: positive control and {rejected} rejected corruptions; 19 Boolean row-deletion witnesses checked")


if __name__ == "__main__":
    main()
