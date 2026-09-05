"""Mutation controls for the orbit certificate."""
from __future__ import annotations

from copy import deepcopy
import json

from verify import HERE, audit


def rejected(certificate):
    try:
        audit(certificate)
    except (ValueError, KeyError, TypeError):
        return True
    return False


def main():
    certificate = json.loads((HERE / "ORBIT_CERTIFICATE.json").read_text())
    audit(certificate)
    corruptions = []
    changed = deepcopy(certificate)
    changed["group_order"] = 47
    corruptions.append(changed)
    changed = deepcopy(certificate)
    changed["format"] = "wrong"
    corruptions.append(changed)
    for index in range(5):
        changed = deepcopy(certificate)
        changed["orbits"][index]["orbit_size"] += 1
        corruptions.append(changed)
        changed = deepcopy(certificate)
        changed["orbits"][index]["stabilizer_order"] += 1
        corruptions.append(changed)
        changed = deepcopy(certificate)
        changed["orbits"][index]["representative"][0] = "111"
        corruptions.append(changed)
    assert all(rejected(changed) for changed in corruptions)
    print(f"PASS {len(corruptions)} orbit-certificate corruptions rejected")


if __name__ == "__main__":
    main()
