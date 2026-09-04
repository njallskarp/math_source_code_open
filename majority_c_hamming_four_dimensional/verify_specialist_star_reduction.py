#!/usr/bin/env python3
"""Exact audits for the Cameron--Horsley rectangle specialization.

CPython 3.12+, standard library only.  The universal cut proof is in
SPECIALIST_PRIOR_ART_REDUCTION.md.  This script checks every restriction-count
type for small corners and the exact extremal reduction for a larger range.
"""

from __future__ import annotations

import argparse


def corner_parameters(s: int, a: int, b: int) -> tuple[int, int, int, int]:
    q, tau = divmod(a * b, s)
    x = a + q
    f = s - q
    assert 0 <= q <= a - 1
    assert 0 <= tau < s
    assert x + f == s + a
    return q, tau, x, f


def audit_exhaustive(max_s: int) -> tuple[int, int, int, int]:
    corners = 0
    restriction_types = 0
    zero_slack = 0
    minimum_slack: int | None = None

    for s in range(2, max_s + 1):
        for a in range(1, s):
            for b in range(1, s):
                q, tau, x, f = corner_parameters(s, a, b)
                m = s + a
                n = s + b
                assert f >= 1
                assert x * s + (n - tau) * s + tau * (s + 1) == m * n
                assert (a + q) * b == q * n + tau
                corners += 1

                for i in range(x + 1):
                    for j1 in range(tau + 1):
                        for j0 in range(n - tau + 1):
                            j = j0 + j1
                            demand = s * (i + j) + j1
                            incident_edges = i * n + j * m - i * j
                            slack = incident_edges - demand
                            assert slack == i * (b - j) + a * j - j1
                            assert slack >= 0
                            restriction_types += 1
                            zero_slack += slack == 0
                            if minimum_slack is None or slack < minimum_slack:
                                minimum_slack = slack

    assert minimum_slack == 0
    return corners, restriction_types, zero_slack, minimum_slack


def audit_extremal(max_s: int) -> tuple[int, int, int, int]:
    corners = 0
    extremal_types = 0
    zero_slack = 0
    minimum_slack: int | None = None

    for s in range(2, max_s + 1):
        for a in range(1, s):
            for b in range(1, s):
                q, tau, x, f = corner_parameters(s, a, b)
                m = s + a
                n = s + b
                assert f >= 1
                assert x * s + n * s + tau == m * n
                corners += 1

                for j in range(n + 1):
                    # For fixed j, the cut slack decreases with j1, so use as
                    # many of the tau large columns as the selection permits.
                    j1 = min(j, tau)
                    assert j - j1 <= n - tau

                    # The coefficient of i is b-j.  Hence an extremal i is 0
                    # for j<=b and x for j>b.
                    i = 0 if j <= b else x
                    slack = i * (b - j) + a * j - j1

                    if j <= b:
                        assert slack == a * j - j1
                        assert slack >= j - j1 >= 0
                    else:
                        endpoint = x * (b - j) + a * j - j1
                        assert slack == endpoint
                        assert endpoint == q * (n - j) + tau - j1
                        assert endpoint >= 0

                    assert slack >= 0
                    extremal_types += 1
                    zero_slack += slack == 0
                    if minimum_slack is None or slack < minimum_slack:
                        minimum_slack = slack

    assert minimum_slack == 0
    return corners, extremal_types, zero_slack, minimum_slack


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exhaustive-max-s", type=int, default=14)
    parser.add_argument("--extremal-max-s", type=int, default=80)
    args = parser.parse_args()

    exhaustive = audit_exhaustive(args.exhaustive_max_s)
    extremal = audit_extremal(args.extremal_max_s)

    print(f"small corners exhaustively audited: {exhaustive[0]}")
    print(f"restriction-count types checked: {exhaustive[1]}")
    print(f"exhaustive zero-slack types: {exhaustive[2]}")
    print(f"exhaustive minimum cut slack: {exhaustive[3]}")
    print(f"large-range corners audited: {extremal[0]}")
    print(f"extremal cut types checked: {extremal[1]}")
    print(f"extremal zero-slack types: {extremal[2]}")
    print(f"extremal minimum cut slack: {extremal[3]}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
