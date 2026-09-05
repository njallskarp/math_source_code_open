"""Mutation controls for the standard-library checker."""
from __future__ import annotations

from copy import deepcopy
import json

from verify import audit, construct, HERE


def rejected(data):
    try:
        audit(construct(data), data)
    except (ValueError, KeyError, TypeError):
        return True
    return False


def main():
    data = json.loads((HERE / "WITNESS.json").read_text())
    audit(construct(data), data)
    count = 0
    for row in range(22):
        for column in range(20):
            corrupt = deepcopy(data)
            value = corrupt["cross_rows"][row][column]
            replacement = "0" if value == "1" else "1"
            corrupt["cross_rows"][row] = (
                corrupt["cross_rows"][row][:column]
                + replacement
                + corrupt["cross_rows"][row][column + 1:]
            )
            assert rejected(corrupt)
            count += 1
    for key, value in (("format", "wrong"), ("anchors", [0, 3, 8])):
        corrupt = deepcopy(data)
        corrupt[key] = value
        assert rejected(corrupt)
        count += 1
    print(f"PASS {count} witness corruptions rejected")


if __name__ == "__main__":
    main()
