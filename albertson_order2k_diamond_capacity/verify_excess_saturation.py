#!/usr/bin/env python3
"""Exact algebra checker for the order-2k excess saturation certificate.

Python 3.10+; standard library only.  This checks identities and parity-level
dispatch.  The Kostochka--Stiebitz lower bound is an external theorem input.
"""

from __future__ import annotations

import hashlib
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def frontier_levels(k: int) -> list[dict[str, int]]:
    require(k >= 4, "the cited theorem is used only for k>=4")
    result = []
    for t in range(3):
        n = 2 * k
        m = k * k - 3 + t
        excess = 2 * m - (k - 1) * n
        low_lower_bound = n - excess
        require(excess == 2 * (k - 3) + 2 * t, "excess identity failed")
        require(low_lower_bound == 6 - 2 * t, "low-vertex identity failed")
        result.append({"t": t, "n": n, "m": m, "X": excess, "low_lb": low_lower_bound})
    require([item["X"] for item in result]
            == list(range(2 * (k - 3), 2 * k, 2)), "parity dispatch failed")
    return result


def separation_family(k: int) -> dict[str, int]:
    require(k >= 6, "the separation family requires k>=6")
    n = 2 * k
    total_pairs = n * (n - 1) // 2
    edges_h = 7 * k - 16
    edges_g = total_pairs - edges_h
    excess = 2 * edges_g - (k - 1) * n
    require(edges_g == 2 * k * k - 8 * k + 16, "separation edge formula failed")
    require(excess == 2 * k * k - 14 * k + 32, "separation excess formula failed")
    return {"k": k, "n": n, "eH": edges_h, "eG": edges_g, "X": excess}


def main() -> None:
    checks = {str(k): frontier_levels(k) for k in (4, 6, 29)}
    separation = separation_family(29)
    require([(x["m"], x["X"], x["low_lb"]) for x in checks["29"]]
            == [(838, 52, 6), (839, 54, 4), (840, 56, 2)],
            "r=29 frontier dispatch failed")
    require(separation == {"k": 29, "n": 58, "eH": 187, "eG": 1466, "X": 1308},
            "r=29 separation specialization failed")

    payload = json.dumps({"frontier": checks, "separation": separation},
                         sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest()
    for item in checks["29"]:
        print(f"t={item['t']} n={item['n']} m={item['m']} "
              f"X={item['X']} low_lb={item['low_lb']}")
    print(f"separation k=29 n={separation['n']} eH={separation['eH']} "
          f"eG={separation['eG']} X={separation['X']}")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
