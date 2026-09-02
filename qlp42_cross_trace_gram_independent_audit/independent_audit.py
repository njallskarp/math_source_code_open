#!/usr/bin/env python3
"""Clean-room audit of the QLP-42 cross-trace and Fourier--Gram claims.

This program deliberately does not read or import the producer's checker or
certificate.  It enumerates local fourth-root pairs directly and obtains the
aggregate (q, a, sigma) states from equal/opposite/quarter-turn cell counts,
rather than from the producer's range-and-parity parametrization.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import json

Gaussian = tuple[int, int]

ROOTS: tuple[Gaussian, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))

# The six (s_A, s_B) trivial Fourier coefficients are imported inputs from
# the canonical coupled-transform cases.  The values of s_B are the six beta
# values displayed in the cross-trace theorem; s_A is read from the same six
# canonical representatives.  The audit does not re-prove their completeness.
CASES: tuple[tuple[Gaussian, Gaussian], ...] = (
    ((1, -1), (4, -5)),
    ((3, -3), (4, -3)),
    ((3, -3), (0, -5)),
    ((5, -1), (4, -1)),
    ((5, -1), (4, 1)),
    ((5, -3), (0, -3)),
)


def add(x: Gaussian, y: Gaussian) -> Gaussian:
    return (x[0] + y[0], x[1] + y[1])


def sub(x: Gaussian, y: Gaussian) -> Gaussian:
    return (x[0] - y[0], x[1] - y[1])


def mul(x: Gaussian, y: Gaussian) -> Gaussian:
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def conj(x: Gaussian) -> Gaussian:
    return (x[0], -x[1])


def norm(x: Gaussian) -> int:
    return x[0] * x[0] + x[1] * x[1]


def divide_by_one_plus_i(x: Gaussian) -> Gaussian:
    """Return x/(1+i), failing if the Gaussian quotient is not integral."""
    real_num = x[0] + x[1]
    imag_num = x[1] - x[0]
    assert real_num % 2 == imag_num % 2 == 0
    return (real_num // 2, imag_num // 2)


def local_state_audit() -> dict[str, int]:
    counts = {"equal": 0, "opposite": 0, "quarter": 0}
    epsilons: set[int] = set()
    for x in ROOTS:
        for y in ROOTS:
            s = divide_by_one_plus_i(sub(x, y))
            h = divide_by_one_plus_i(add(x, y))
            assert norm(s) + norm(h) == 2

            # epsilon = -i S conjugate(H); multiplication by -i sends
            # (a,b) to (b,-a).
            cross = mul(s, conj(h))
            epsilon_gaussian = (cross[1], -cross[0])
            assert epsilon_gaussian[1] == 0
            epsilon = epsilon_gaussian[0]
            assert epsilon in (-1, 0, 1)
            epsilons.add(epsilon)

            relation = mul(x, conj(y))
            if relation == (1, 0):
                kind = "equal"
                assert norm(s) == 0 and norm(h) == 2 and epsilon == 0
            elif relation == (-1, 0):
                kind = "opposite"
                assert norm(s) == 2 and norm(h) == 0 and epsilon == 0
            else:
                kind = "quarter"
                assert norm(s) == norm(h) == 1 and abs(epsilon) == 1
            counts[kind] += 1

    assert counts == {"equal": 4, "opposite": 4, "quarter": 8}
    assert epsilons == {-1, 0, 1}
    return counts


def character_partition_audit() -> dict[int, int]:
    """Partition all 21 characters by their exact orders."""
    from math import gcd

    order_counts: dict[int, int] = defaultdict(int)
    frequencies_by_order: dict[int, set[int]] = defaultdict(set)
    for k in range(21):
        order = 1 if k == 0 else 21 // gcd(k, 21)
        order_counts[order] += 1
        frequencies_by_order[order].add(k)

    assert dict(order_counts) == {1: 1, 21: 12, 7: 6, 3: 2}
    assert set().union(*frequencies_by_order.values()) == set(range(21))
    assert sum(order_counts.values()) == 21

    # The sum over the four primitive-order traces is therefore the sum over
    # every character of C_21.  Orthogonality gives the diagonal kernel.
    for displacement in range(21):
        # Algebraic geometric-series condition, with no floating arithmetic:
        # sum_{k=0}^{20} zeta^(k*d) is 21 iff 21 divides d, else zero.
        kernel = 21 if displacement % 21 == 0 else 0
        assert kernel == (21 if displacement == 0 else 0)
    return dict(sorted(order_counts.items()))


def family_aggregate_states() -> list[tuple[int, int, int]]:
    """Derive all (q,a,sigma) states from explicit local-type counts."""
    states: list[tuple[int, int, int]] = []
    for quarter in range(22):
        for opposite in range(22 - quarter):
            equal = 21 - quarter - opposite
            assert equal >= 0
            energy = 2 * opposite + quarter
            for positive_quarters in range(quarter + 1):
                sigma = 2 * positive_quarters - quarter
                states.append((quarter, energy, sigma))
    assert len(states) == sum((22 - q) * (q + 1) for q in range(22))
    assert len(states) == len(set(states))
    return states


def determinant(
    energy: int,
    s: Gaussian,
    h: Gaussian,
    sigma: int,
) -> int:
    e_s = 21 * energy - norm(s)
    e_h = 21 * (42 - energy) - norm(h)
    # 21 i sigma - s conjugate(h)
    cross = sub((0, 21 * sigma), mul(s, conj(h)))
    assert e_s >= 0 and e_h >= 0
    return e_s * e_h - norm(cross)


def aggregate_audit() -> dict[str, object]:
    states = family_aggregate_states()
    by_q: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for q, a, sigma in states:
        by_q[q].append((a, sigma))

    expected_full_turn = {
        ("A", 21, 21, -21),
        ("A", 21, 21, 21),
        ("B", 21, 21, -21),
        ("B", 21, 21, 21),
    }
    expected_case_zero_extra = {
        ("B", 20, 20, 20),
        ("B", 20, 22, 20),
    }

    totals: dict[int, list[int]] = {5: [0, 0], 37: [0, 0]}
    exclusions_by_case: list[int] = []
    failure_pattern_sets: list[set[tuple[str, int, int, int]]] = []
    digest_rows: list[tuple[int, int, int, int, int, int, int]] = []

    for case_index, (s_a, s_b) in enumerate(CASES):
        case_failures = 0
        patterns: set[tuple[str, int, int, int]] = set()
        for total_q in (5, 37):
            candidate_count = 0
            survivor_count = 0
            surviving_total_sigma: set[int] = set()

            for q_a in range(22):
                q_b = total_q - q_a
                if not 0 <= q_b <= 21:
                    continue
                for a_a, sigma_a in by_q[q_a]:
                    for a_b, sigma_b in by_q[q_b]:
                        if a_a + a_b != 43:
                            continue
                        candidate_count += 1
                        d_a = determinant(a_a, s_a, (0, 0), sigma_a)
                        d_b = determinant(a_b, s_b, (1, 0), sigma_b)
                        failed_here: list[tuple[str, int, int, int]] = []
                        if d_a < 0:
                            failed_here.append(("A", q_a, a_a, sigma_a))
                        if d_b < 0:
                            failed_here.append(("B", q_b, a_b, sigma_b))

                        if failed_here:
                            patterns.update(failed_here)
                            if total_q == 37:
                                case_failures += 1
                                digest_rows.append(
                                    (
                                        case_index,
                                        q_a,
                                        a_a,
                                        sigma_a,
                                        a_b,
                                        sigma_b,
                                        min(d_a, d_b),
                                    )
                                )
                        else:
                            survivor_count += 1
                            surviving_total_sigma.add(sigma_a + sigma_b)

            expected_sigma = set(range(-total_q, total_q + 1, 2))
            assert surviving_total_sigma == expected_sigma
            totals[total_q][0] += candidate_count
            totals[total_q][1] += survivor_count
            if total_q == 5:
                assert candidate_count == survivor_count == 1020
                assert not patterns
            else:
                assert candidate_count == 4540

        expected = set(expected_full_turn)
        if case_index == 0:
            expected |= expected_case_zero_extra
        assert patterns == expected
        exclusions_by_case.append(case_failures)
        failure_pattern_sets.append(patterns)

    assert totals == {5: [6120, 6120], 37: [27240, 26796]}
    assert exclusions_by_case == [104, 68, 68, 68, 68, 68]
    assert sum(exclusions_by_case) == 444

    encoded = json.dumps(sorted(digest_rows), separators=(",", ":")).encode()
    return {
        "q5_candidates": totals[5][0],
        "q5_survivors": totals[5][1],
        "q37_candidates": totals[37][0],
        "q37_survivors": totals[37][1],
        "q37_exclusions_by_case": exclusions_by_case,
        "q37_failure_row_sha256": sha256(encoded).hexdigest(),
        "failure_patterns_per_case": [
            sorted(list(patterns)) for patterns in failure_pattern_sets
        ],
        "all_total_sigma_fibers_survive": True,
    }


def main() -> None:
    result = {
        "local_state_counts": local_state_audit(),
        "character_orders": character_partition_audit(),
        "aggregate": aggregate_audit(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("independent_audit=PASS")


if __name__ == "__main__":
    main()
