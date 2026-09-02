#!/usr/bin/env python3
"""Exact aggregate checker for the per-family Fourier–Gram sieve."""

from __future__ import annotations

from collections import Counter, defaultdict

G = tuple[int, int]
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)


def norm(value: G) -> int:
    return value[0] * value[0] + value[1] * value[1]


def signed_sums(q: int) -> range:
    return range(-q, q + 1, 2)


def counts_possible(a: int, q: int) -> bool:
    return a >= q and a + q <= 42 and (a - q) % 2 == 0


def determinant(es: int, eh: int, cross: G) -> int:
    return es * eh - norm(cross)


def enumerate_case(q_total: int, case: tuple[int, int, int, int]):
    p, r, x, y = case
    s_a = (p + r, r - p)
    s_b = (x + y - 1, y - x)
    candidates = []
    survivors = []

    for q_a in range(22):
        q_b = q_total - q_a
        if not 0 <= q_b <= 21:
            continue
        for a_a in range(43):
            a_b = 43 - a_a
            if not counts_possible(a_a, q_a):
                continue
            if not counts_possible(a_b, q_b):
                continue

            es_a = 21 * a_a - norm(s_a)
            eh_a = 21 * (42 - a_a)
            es_b = 21 * a_b - norm(s_b)
            eh_b = 21 * (42 - a_b) - 1
            assert min(es_a, eh_a, es_b, eh_b) >= 0

            for sigma_a in signed_sums(q_a):
                for sigma_b in signed_sums(q_b):
                    d_a = determinant(es_a, eh_a, (0, 21 * sigma_a))
                    d_b = determinant(
                        es_b,
                        eh_b,
                        (-s_b[0], 21 * sigma_b - s_b[1]),
                    )
                    row = (
                        q_a,
                        q_b,
                        a_a,
                        a_b,
                        sigma_a,
                        sigma_b,
                        d_a,
                        d_b,
                    )
                    candidates.append(row)
                    if d_a >= 0 and d_b >= 0:
                        survivors.append(row)
    return candidates, survivors


def failure_patterns(rows):
    patterns: dict[str, set[tuple[int, int, int]]] = defaultdict(set)
    for q_a, q_b, a_a, a_b, sigma_a, sigma_b, d_a, d_b in rows:
        if d_a < 0:
            patterns["A"].add((q_a, a_a, sigma_a))
        if d_b < 0:
            patterns["B"].add((q_b, a_b, sigma_b))
    return {family: values for family, values in patterns.items()}


def main() -> None:
    totals = Counter()
    case37_excluded = []
    complete_sigma = {q: set(signed_sums(q)) for q in (5, 37)}

    universal_full = {
        "A": {(21, 21, -21), (21, 21, 21)},
        "B": {(21, 21, -21), (21, 21, 21)},
    }

    for case_index, case in enumerate(CASES):
        for q_total in (5, 37):
            candidates, survivors = enumerate_case(q_total, case)
            totals[(q_total, "candidates")] += len(candidates)
            totals[(q_total, "survivors")] += len(survivors)

            surviving_sigma = {row[4] + row[5] for row in survivors}
            assert surviving_sigma == complete_sigma[q_total]

            failures = failure_patterns(candidates)
            if q_total == 5:
                assert failures == {}
                assert len(candidates) == len(survivors) == 1020
            else:
                expected = {key: set(value) for key, value in universal_full.items()}
                if case_index == 0:
                    expected["B"].update({(20, 20, 20), (20, 22, 20)})
                assert failures == expected
                case37_excluded.append(len(candidates) - len(survivors))
                assert len(candidates) == 4540

    assert totals[(5, "candidates")] == 6120
    assert totals[(5, "survivors")] == 6120
    assert totals[(37, "candidates")] == 27240
    assert totals[(37, "survivors")] == 26796
    assert case37_excluded == [104, 68, 68, 68, 68, 68]

    print("q5_aggregate_candidates=6120")
    print("q5_aggregate_excluded=0")
    print("q37_aggregate_candidates=27240")
    print("q37_aggregate_excluded=444")
    print("q37_case_exclusions=104,68,68,68,68,68")
    print("universal_failure=qX:21,aX:21,abs_sigmaX:21")
    print("case0_extra_failure=family:B,qB:20,sigmaB:20,aB:20_or_22")
    print("total_sigma_fiber_points_excluded=0")
    print("frontier_cells_enumerated=0")
    print("certificate=verified")


if __name__ == "__main__":
    main()
