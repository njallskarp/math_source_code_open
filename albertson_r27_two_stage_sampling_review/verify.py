#!/usr/bin/env python3
"""Clean-room exact audit of the Albertson r=27 integral-sampling lemma.

The checker uses only Python integers and fractions.Fraction.  It independently
reconstructs every binomial multiplicity in the induced-subgraph double count,
then tests a second vertex-deletion average that improves the (54, 726) case.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from math import comb


def ceil_fraction(value: Fraction) -> int:
    """Exact ceiling, including negative values."""
    return -((-value.numerator) // value.denominator)


def local_integer_bound(vertices: int, edges: int) -> int:
    """Integral form of 5e - 203(v-2)/9."""
    return 5 * edges + ceil_fraction(Fraction(-203 * (vertices - 2), 9))


def sampled_by_counts(n: int, m: int, s: int) -> Fraction:
    """Double-counted lower bound before the final global ceiling."""
    assert 4 <= s <= n
    numerator = (
        5 * m * comb(n - 2, s - 2)
        + ceil_fraction(Fraction(-203 * (s - 2), 9)) * comb(n, s)
    )
    return Fraction(numerator, comb(n - 4, s - 4))


def sampled_simplified(n: int, m: int, s: int) -> Fraction:
    """Algebraically simplified version of sampled_by_counts."""
    local_constant = ceil_fraction(Fraction(-203 * (s - 2), 9))
    return (
        Fraction(5 * m * (n - 2) * (n - 3), (s - 2) * (s - 3))
        + Fraction(
            local_constant * n * (n - 1) * (n - 2) * (n - 3),
            s * (s - 1) * (s - 2) * (s - 3),
        )
    )


def continuous_sampled(n: int, m: int, s: int) -> Fraction:
    """Comparator without the local integer ceiling."""
    return (
        Fraction(5 * m * (n - 2) * (n - 3), (s - 2) * (s - 3))
        - Fraction(
            203 * n * (n - 1) * (n - 2) * (n - 3),
            9 * s * (s - 1) * (s - 3),
        )
    )


def best_sample(n: int, m: int) -> tuple[int, Fraction, int]:
    """Return (integer conclusion, unrounded bound, least optimizing s)."""
    candidates = [(sampled_by_counts(n, m, s), -s) for s in range(4, n + 1)]
    value, negative_s = max(candidates)
    return ceil_fraction(value), value, -negative_s


def deletion_cost(degree: int) -> int:
    """Best sampled bound for G-v when G has (n,m)=(54,726)."""
    return best_sample(53, 726 - degree)[0]


def worst_degree_multiset() -> tuple[int, Counter[int]]:
    """DP over all degree multisets with 54 entries >=26 and total 1452.

    Graphicality is deliberately ignored, enlarging the feasible set.  Therefore
    its minimum remains a valid lower bound for every actual 27-critical graph.
    """
    # State (number of vertices, used excess above 26) -> (cost, excess tuple).
    states: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {
        (0, 0): (0, ())
    }
    for count in range(54):
        next_states: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
        for (_, used), (cost, witness) in states.items():
            for excess in range(min(27, 48 - used) + 1):
                key = (count + 1, used + excess)
                candidate = (
                    cost + deletion_cost(26 + excess),
                    witness + (excess,),
                )
                if key not in next_states or candidate[0] < next_states[key][0]:
                    next_states[key] = candidate
        states = next_states
    minimum, excesses = states[(54, 48)]
    return minimum, Counter(26 + excess for excess in excesses)


def main() -> None:
    # Definition-level and simplified formulas agree on boundary and dense tests.
    for n in range(4, 65):
        for s in range(4, n + 1):
            for m in (0, n, n * (n - 1) // 2):
                assert sampled_by_counts(n, m, s) == sampled_simplified(n, m, s)
        assert sampled_by_counts(n, 2 * n, n) == local_integer_bound(n, 2 * n)

    expected = {
        (54, 726): (6076, Fraction(10759164, 1771), 24),
        (53, 713): (6009, Fraction(31923025, 5313), 24),
        (53, 714): (6037, Fraction(32069650, 5313), 24),
        (53, 715): (6064, Fraction(1952535, 322), 23),
    }
    reproduced: dict[str, dict[str, str | int]] = {}
    for (n, m), target in expected.items():
        result = best_sample(n, m)
        assert result == target
        reproduced[f"{n},{m}"] = {
            "ceiling": result[0],
            "fraction": str(result[1]),
            "s": result[2],
        }

    continuous = max(continuous_sampled(54, 726, s) for s in range(4, 55))
    assert continuous == Fraction(977041, 161)
    assert ceil_fraction(continuous) == 6069

    # A compact hand-proof bound for every possible degree.  Degree 26 uses
    # s=24; degrees >=27 use s=25 (with the outer ceiling at degree 27).
    assert ceil_fraction(sampled_by_counts(53, 700, 24)) == 5650
    assert sampled_by_counts(53, 699, 25) == Fraction(61846, 11)
    for degree in range(26, 54):
        assert deletion_cost(degree) >= 5650 - 27 * (degree - 26)
        if degree >= 28:
            stated = Fraction(1594583 - 6375 * degree, 253)
            assert sampled_by_counts(53, 726 - degree, 25) == stated
            assert stated > 5650 - 27 * (degree - 26)

    minimum_sum, worst_histogram = worst_degree_multiset()
    assert minimum_sum == 303804
    assert worst_histogram == Counter({27: 48, 26: 6})
    two_stage = ceil_fraction(Fraction(minimum_sum, 50))
    assert two_stage == 6077

    certificate = {
        "reproduced": reproduced,
        "continuous_54_726": str(continuous),
        "minimum_vertex_deleted_sum": minimum_sum,
        "worst_relaxed_degree_histogram": dict(sorted(worst_histogram.items())),
        "two_stage_54_726": two_stage,
        "remaining_deficit_to_6084": 6084 - two_stage,
    }
    canonical = json.dumps(certificate, sort_keys=True, separators=(",", ":"))
    digest = sha256(canonical.encode("ascii")).hexdigest()

    print("PASS clean-room integral-sampling audit")
    for case, result in reproduced.items():
        print(
            f"n,m={case}: s={result['s']} fraction={result['fraction']} "
            f"ceiling={result['ceiling']}"
        )
    print("two-stage n=54,m=726: sum=303804 divisor=50 ceiling=6077")
    print("worst relaxed degree histogram: 26:6,27:48")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
