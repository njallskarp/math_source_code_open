#!/usr/bin/env python3
"""Independent exact audit of the exceptional m=10 incidence projection.

This verifier does not read the producer's certificate and does not import the
producer's checker.  It enumerates the ten residual clause deficits directly
as sorted multisets, then converts each multiset to its multiplicity vector.

Requires only the Python 3.11+ standard library.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations_with_replacement
import json


EXPECTED_COUNTS = {17: 18, 18: 11, 19: 6, 20: 3, 21: 1}
EXPECTED_DIGEST = "61af373a215e67d106d050518d9630ca50864ba474275b620391ff4cae93dc62"


def multiplicity_vector(deficits: tuple[int, ...]) -> list[int]:
    """Return [x_0,...,x_4] for a sorted ten-deficit multiset."""
    counts = Counter(deficits)
    return [counts[value] for value in range(5)]


def main() -> None:
    # The three selected witnesses contribute one red-neighborhood incidence
    # each.  The ten residual four-clauses contribute at most forty more.
    assert 2 * 21 <= 3 + 10 * 4 < 2 * 22

    frontier: dict[str, dict[str, object]] = {}
    minimum_internal: dict[int, int] = {}

    for rho in range(17, 22):
        total_deficit = 40 - (2 * rho - 3)
        assert total_deficit == 43 - 2 * rho

        profiles = sorted(
            multiplicity_vector(deficits)
            for deficits in combinations_with_replacement(range(5), 10)
            if sum(deficits) == total_deficit
        )

        # Conversion to multiplicities is injective on sorted multisets.
        assert len({tuple(profile) for profile in profiles}) == len(profiles)
        for profile in profiles:
            assert sum(profile) == 10
            assert sum(value * profile[value] for value in range(5)) == total_deficit

        minimum_internal[rho] = min(profile[0] for profile in profiles)
        assert minimum_internal[rho] >= 2 * rho - 33
        frontier[str(rho)] = {"deficit": total_deficit, "profiles": profiles}

    counts = {rho: len(frontier[str(rho)]["profiles"]) for rho in range(17, 22)}
    assert counts == EXPECTED_COUNTS
    assert sum(counts.values()) == 39
    assert frontier["21"]["profiles"] == [[9, 1, 0, 0, 0]]

    canonical = json.dumps(frontier, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(canonical).hexdigest()
    assert digest == EXPECTED_DIGEST

    print(f"accepted counts={counts} total=39")
    print(f"minimum_x0={minimum_internal}")
    print(f"rho21_profiles={frontier['21']['profiles']}")
    print(f"canonical_sha256={digest}")


if __name__ == "__main__":
    main()
