#!/usr/bin/env python3
"""Independent finite-support and exact-arithmetic checks for the review."""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from json import dumps
from math import comb


def choose(n: int, k: int) -> int:
    """Natural-number binomial coefficient, extended by zero off range."""
    return comb(n, k) if 0 <= k <= n else 0


def supported_count(supports: list[frozenset[int]], sample: frozenset[int]) -> int:
    return sum(support <= sample for support in supports)


def check_incidence_identity() -> int:
    """Exercise all n <= 7, including repeated supports and s > n."""
    cases = 0
    for n in range(8):
        universe = tuple(range(n))
        for k in range(n + 1):
            supports = [frozenset(x) for x in combinations(universe, k)]
            # Distinct feature identifiers may deliberately share a support.
            supports.append(supports[0])
            for s in range(k, n + 3):
                samples = [frozenset(x) for x in combinations(universe, s)]
                lhs = sum(supported_count(supports, sample) for sample in samples)
                rhs = len(supports) * choose(n - k, s - k)
                assert lhs == rhs, (n, k, s, lhs, rhs)
                cases += 1
    return cases


def check_sampling_inequality() -> dict[str, int]:
    """Check the summed inequality on a multiplicity-heavy small instance."""
    universe = tuple(range(6))
    edge_supports = [frozenset(x) for x in combinations(universe, 2)]
    edge_supports += [edge_supports[0], edge_supports[0]]
    crossing_supports = [frozenset({0, 1, 2, 3})] * 3
    crossing_supports += [frozenset({0, 1, 4, 5})]
    s = 4
    a = 2
    samples = [frozenset(x) for x in combinations(universe, s)]
    deficit = max(
        0,
        max(
            a * supported_count(edge_supports, sample)
            - supported_count(crossing_supports, sample)
            for sample in samples
        ),
    )
    lhs = a * len(edge_supports) * choose(4, 2)
    rhs = len(crossing_supports) * choose(2, 0) + deficit * choose(6, 4)
    assert lhs <= rhs
    return {"deficit": deficit, "lhs": lhs, "rhs": rhs}


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def check_local_rounding() -> tuple[int, dict[str, int]]:
    """Check 0 <= m <= 1000 and exhibit sharpness of the constant 496."""
    cases = 0
    for m in range(1001):
        threshold = Fraction(5 * m) - Fraction(203 * 22, 9)
        least_natural_c = max(0, ceil_fraction(threshold))
        assert 5 * m <= least_natural_c + 496
        cases += 1
    witness = {"m": 100, "c": 4}
    assert Fraction(5 * witness["m"]) - Fraction(203 * 22, 9) <= witness["c"]
    assert 5 * witness["m"] == witness["c"] + 496
    return cases, witness


def order54_value(deficit: int) -> tuple[Fraction, int]:
    numerator = 5 * 726 * choose(52, 22) - deficit * choose(54, 24)
    denominator = choose(50, 20)
    value = Fraction(numerator, denominator)
    return value, ceil_fraction(value)


def main() -> None:
    incidence_cases = check_incidence_identity()
    sampling = check_sampling_inequality()
    rounding_cases, witness = check_local_rounding()
    value496, floor496 = order54_value(496)
    value495, floor495 = order54_value(495)
    assert value496 == Fraction(10_759_164, 1_771)
    assert floor496 == 6076
    assert value495 == Fraction(1_965_795, 322)
    assert floor495 == 6105

    certificate = {
        "deficit_495": {"ceiling": floor495, "value": str(value495)},
        "deficit_496": {"ceiling": floor496, "value": str(value496)},
        "incidence_cases": incidence_cases,
        "local_rounding_cases": rounding_cases,
        "rounding_496_sharp_witness": witness,
        "sampling_inequality": sampling,
    }
    canonical = dumps(certificate, sort_keys=True, separators=(",", ":"))
    print(dumps(certificate, indent=2, sort_keys=True))
    print(f"certificate_sha256={sha256(canonical.encode()).hexdigest()}")
    print("PASS independent Albertson integral-sampling audit")


if __name__ == "__main__":
    main()
