#!/usr/bin/env python3
"""Verify the exceptional m=10 red-link incidence frontier exactly."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def enumerate_profiles(total_clauses: int, total_deficit: int) -> list[list[int]]:
    """Enumerate canonical count vectors [x0,...,x4]."""
    profiles: list[list[int]] = []
    for x4 in range(total_clauses + 1):
        for x3 in range(total_clauses - x4 + 1):
            for x2 in range(total_clauses - x4 - x3 + 1):
                for x1 in range(total_clauses - x4 - x3 - x2 + 1):
                    x0 = total_clauses - x1 - x2 - x3 - x4
                    if x1 + 2 * x2 + 3 * x3 + 4 * x4 == total_deficit:
                        profiles.append([x0, x1, x2, x3, x4])
    profiles.sort()
    return profiles


def main() -> None:
    require(len(sys.argv) == 2, "usage: verify_exceptional_m10_link_incidence.py CERTIFICATE.json")
    certificate = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    blue_clauses = certificate["selected_blue_clauses"]
    side_clauses = certificate["selected_blue_clauses_through_pivot"]
    off_clauses = certificate["selected_blue_clauses_avoiding_pivot"]
    witnesses = certificate["forced_distinct_one_flip_witnesses"]
    residual = certificate["residual_blue_clauses"]

    require((blue_clauses, side_clauses, off_clauses) == (23, 10, 13), "wrong clause split")
    require(off_clauses == blue_clauses - side_clauses, "off-pivot clause count mismatch")
    require((witnesses, residual) == (3, 10), "wrong witness/residual split")
    require(off_clauses == witnesses + residual, "off-pivot decomposition mismatch")
    require(certificate["blue_selected_degree_on_red_neighborhood"] == 2, "degree floor changed")

    # Three witnesses contribute one red-neighborhood incidence each; the
    # other ten four-clauses contribute at most four each.
    require(3 + 10 * 4 == 43, "capacity calculation changed")
    require(2 * 21 <= 43 < 2 * 22, "rho cutoff should be exactly 21")
    require(certificate["rho_range"] == [17, 21], "certificate rho range changed")

    recomputed: dict[str, dict[str, object]] = {}
    for rho in range(17, 22):
        total_deficit = 4 * residual - (2 * rho - witnesses)
        require(total_deficit == 43 - 2 * rho, "deficit identity changed")
        profiles = enumerate_profiles(residual, total_deficit)
        recomputed[str(rho)] = {"deficit": total_deficit, "profiles": profiles}

        claimed = certificate["profiles_by_rho"][str(rho)]
        require(claimed["total_deficit"] == total_deficit, f"wrong deficit for rho={rho}")
        require(claimed["profiles"] == profiles, f"wrong canonical profiles for rho={rho}")
        for profile in profiles:
            require(sum(profile) == residual, "profile does not contain ten clauses")
            require(sum(delta * profile[delta] for delta in range(5)) == total_deficit,
                    "profile has wrong total deficit")
            require(profile[0] >= 2 * rho - 33,
                    "profile violates the forced internal-blue-K4 staircase")

    profile_count = sum(len(item["profiles"]) for item in recomputed.values())
    require(profile_count == certificate["canonical_profile_count"] == 39, "profile count changed")
    canonical_blob = json.dumps(recomputed, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(canonical_blob).hexdigest()
    require(digest == certificate["canonical_profiles_sha256"], "canonical profile hash mismatch")

    counts = {rho: len(recomputed[str(rho)]["profiles"]) for rho in range(17, 22)}
    print(
        "verified: exceptional m=10 forces 17<=rho<=21; "
        f"canonical profile counts={counts}; total=39; sha256={digest}"
    )


if __name__ == "__main__":
    main()
