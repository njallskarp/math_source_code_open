#!/usr/bin/env python3
"""Small rejection controls for the exact checker."""

from __future__ import annotations

import base64
import itertools
import json

import verify


def expect_failure(action, label: str) -> None:
    try:
        action()
    except (AssertionError, ValueError):
        print(f"PASS rejected {label}")
    else:
        raise AssertionError(f"accepted {label}")


def main() -> None:
    data = json.loads((verify.HERE / "SHARP_WITNESSES.json").read_text(encoding="utf-8"))
    record = base64.b64decode(data["witnesses"][0]["parent_graph6_base64"], validate=True)
    n, edges = verify.decode_graph6(record)
    red_bad = set(edges)
    red_bad.update(itertools.combinations(range(4), 2))
    assert verify.has_clique(n, red_bad, 4, False)
    print("PASS detected injected K4")
    blue_bad = set(edges)
    blue_bad.difference_update(itertools.combinations(range(5), 2))
    assert verify.has_clique(n, blue_bad, 5, True)
    print("PASS detected injected independent five-set")
    expect_failure(lambda: verify.decode_graph6(b"!"), "malformed graph6")
    original = verify.R35_COUNTS[9]
    verify.R35_COUNTS[9] = original + 1
    expect_failure(verify.audit_thresholds, "changed catalog count")
    verify.R35_COUNTS[9] = original
    print("PASS rejection controls")


if __name__ == "__main__":
    main()
