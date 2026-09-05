#!/usr/bin/env python3
"""Positive and corruption-control tests for verify.py."""

from __future__ import annotations

from copy import deepcopy

import verify


def expect_failure(action, label: str) -> None:
    try:
        action()
    except (AssertionError, ValueError):
        return
    raise AssertionError(f"accepted corruption: {label}")


def main() -> None:
    data = verify.load_data()
    verify.audit(data)

    missing_deletion = deepcopy(data)
    missing_deletion["red_anchor_core"]["delete_edges"].pop()
    expect_failure(lambda: verify.audit(missing_deletion), "missing red-core deletion")

    wrong_cross_width = deepcopy(data)
    wrong_cross_width["red_cross_rule"]["width"] = 9
    expect_failure(lambda: verify.audit(wrong_cross_width), "wrong cyclic width")

    expect_failure(lambda: verify.decode_graph6(b"~"), "truncated graph6")
    print("PASS valid anchor witness")
    print("PASS rejected missing deletion, wrong cross width, and truncated graph6")


if __name__ == "__main__":
    main()
