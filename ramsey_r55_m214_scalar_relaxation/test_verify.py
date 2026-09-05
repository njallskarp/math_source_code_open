#!/usr/bin/env python3
"""Definition-level acceptance and rejection tests for the compact checker."""

from __future__ import annotations

import copy
import json

from verify_pseudomodel import DEFAULT_CERTIFICATE, verify


def must_reject(data: dict, label: str) -> None:
    try:
        verify(data, emit=False)
    except (AssertionError, KeyError, TypeError, ValueError):
        print(f"PASS rejects_{label}")
        return
    raise AssertionError(f"mutation unexpectedly accepted: {label}")


def main() -> None:
    data = json.loads(DEFAULT_CERTIFICATE.read_text())
    verify(data, emit=False)
    print("PASS accepts_certificate")

    bad = copy.deepcopy(data)
    bad["M"] = 215
    must_reject(bad, "wrong_M")

    bad = copy.deepcopy(data)
    bad["central_signatures"][0] = bad["central_signatures"][1]
    must_reject(bad, "duplicate_signature")

    bad = copy.deepcopy(data)
    bad["central_red_graph"]["deleted_edge"] = [0, 1]
    must_reject(bad, "wrong_backbone_edge")

    bad = copy.deepcopy(data)
    bad["assigned_local_profiles"]["central_signature_size_7"] = [100, 100]
    must_reject(bad, "wrong_local_profile")


if __name__ == "__main__":
    main()
