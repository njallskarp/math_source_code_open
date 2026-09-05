"""Negative controls for malformed witness data and advertised certificates."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from verify import audit, construct


HERE = Path(__file__).resolve().parent


def rejected(data):
    try:
        audit(construct(data), data)
    except (KeyError, TypeError, ValueError):
        return True
    return False


def main():
    original = json.loads((HERE / "WITNESS.json").read_text())
    audit(construct(original), original)

    changed = deepcopy(original)
    row = changed["cross_rows"][0]
    changed["cross_rows"][0] = ("0" if row[0] == "1" else "1") + row[1:]
    if not rejected(changed):
        raise RuntimeError("accepted flipped incidence bit")

    changed = deepcopy(original)
    changed["coupled_diagonal_edges"][0] = [4, 33]
    if not rejected(changed):
        raise RuntimeError("accepted incorrect coupled edge")

    changed = deepcopy(original)
    changed["blue_unit_five_sets"][0][-1] = 33
    if not rejected(changed):
        raise RuntimeError("accepted incorrect forcing set")

    changed = deepcopy(original)
    changed["cross_rows"][0] = "2" + changed["cross_rows"][0][1:]
    if not rejected(changed):
        raise RuntimeError("accepted nonbinary row")

    changed = deepcopy(original)
    changed["red_core_parent_graph6_base64"] = changed["red_core_parent_graph6_base64"][:-4]
    if not rejected(changed):
        raise RuntimeError("accepted truncated graph6")

    print("PASS rejected flipped incidence bit")
    print("PASS rejected incorrect coupled edge and forcing set")
    print("PASS rejected nonbinary row and truncated graph6")


if __name__ == "__main__":
    main()

