"""Corruption controls for the exact width-two witness."""
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
    changed["first_red_width3_k5"][-1] = 41
    if not rejected(changed):
        raise RuntimeError("accepted incorrect red defect")

    changed = deepcopy(original)
    changed["first_blue_width3_k5"][-1] = 35
    if not rejected(changed):
        raise RuntimeError("accepted incorrect blue defect")

    changed = deepcopy(original)
    changed["cross_rows"][0] = "2" + changed["cross_rows"][0][1:]
    if not rejected(changed):
        raise RuntimeError("accepted nonbinary row")

    changed = deepcopy(original)
    changed["red_core_parent_graph6_base64"] = changed["red_core_parent_graph6_base64"][:-4]
    if not rejected(changed):
        raise RuntimeError("accepted truncated graph6")

    print("PASS rejected flipped incidence bit")
    print("PASS rejected incorrect width-three defects")
    print("PASS rejected nonbinary row and truncated graph6")


if __name__ == "__main__":
    main()

