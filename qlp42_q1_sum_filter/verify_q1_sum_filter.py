#!/usr/bin/env python3
"""Exact verifier for the Gaussian-sum filter in the QLP-42 q=1 branch."""

from __future__ import annotations

from collections import Counter
from csv import DictReader
from itertools import product
from pathlib import Path

G = tuple[int, int]
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIAGONALS: tuple[G, ...] = ((1, 1), (1, -1), (-1, 1), (-1, -1))
REPRESENTATIVES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)
EXPECTED_COUNTS = {
    0: tuple(range(4, 21, 2)),
    1: tuple(range(4, 19, 2)),
    2: tuple(range(4, 19, 2)),
    3: tuple(range(4, 17, 2)),
    4: tuple(range(4, 17, 2)),
    5: tuple(range(2, 17, 2)),
}
EXPECTED_PATTERN_COUNTS = {0: 123, 1: 120, 2: 120, 3: 113, 4: 113, 5: 116}
EXPECTED_BOUNDARY = {
    0: "o=4:sigma=-1;o=20:tau=+1",
    1: "none",
    2: "o=4:sigma=-1",
    3: "none",
    4: "none",
    5: "o=2:sigma=-1",
}


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def sub(left: G, right: G) -> G:
    return left[0] - right[0], left[1] - right[1]


def div_one_plus_i(value: G) -> G:
    assert (value[0] + value[1]) % 2 == 0
    assert (value[1] - value[0]) % 2 == 0
    return (value[0] + value[1]) // 2, (value[1] - value[0]) // 2


def reachable_diagonal_sum(count: int, target: G) -> bool:
    return all(abs(coordinate) <= count and (coordinate - count) % 2 == 0 for coordinate in target)


def check_diagonal_sum_criterion() -> None:
    reachable = {(0, 0)}
    for count in range(22):
        predicted = {
            (real, imag)
            for real in range(-count, count + 1)
            for imag in range(-count, count + 1)
            if reachable_diagonal_sum(count, (real, imag))
        }
        assert reachable == predicted
        reachable = {add(value, step) for value in reachable for step in DIAGONALS}


def exceptional_sign_pairs() -> set[tuple[int, int]]:
    result = set()
    states = set()
    for x, y in product(ROOTS, repeat=2):
        s = div_one_plus_i(sub(x, y))
        h = div_one_plus_i(add(x, y))
        states.add((s, h))
        if s[0] == 0 and abs(s[1]) == 1 and abs(h[0]) == 1 and h[1] == 0:
            result.add((s[1], h[0]))
    assert len(states) == 16
    assert result == set(product((-1, 1), repeat=2))
    return result


def feasible_signs(case: int, opposite_b: int) -> set[tuple[int, int]]:
    p, q, x, y = REPRESENTATIVES[case]
    opposite_a = 21 - opposite_b
    equal_a = opposite_b
    equal_b = 20 - opposite_b
    sum_s_a = (p + q, q - p)
    sum_s_b = (x + y - 1, y - x)
    result = set()
    for sigma, tau in exceptional_sign_pairs():
        if (
            reachable_diagonal_sum(opposite_a, sum_s_a)
            and reachable_diagonal_sum(equal_a, (0, 0))
            and reachable_diagonal_sum(
                opposite_b, (sum_s_b[0], sum_s_b[1] - sigma)
            )
            and reachable_diagonal_sum(equal_b, (1 - tau, 0))
        ):
            result.add((sigma, tau))
    return result


def reflected_pattern_histogram() -> Counter[int]:
    histogram: Counter[int] = Counter()
    for k0 in (0, 2):
        for k1, k2, k3 in product(range(4), repeat=3):
            histogram[2 * (k0 + k1 + k2 + k3)] += 1
    assert sum(histogram.values()) == 128
    return histogram


def main() -> None:
    check_diagonal_sum_criterion()
    exceptional_sign_pairs()
    histogram = reflected_pattern_histogram()
    with (Path(__file__).parent / "case_filter.tsv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(DictReader(handle, delimiter="\t"))
    assert len(rows) == 6

    for case, row in enumerate(rows):
        allowed = tuple(
            opposite_b
            for opposite_b in range(0, 21, 2)
            if feasible_signs(case, opposite_b)
        )
        assert allowed == EXPECTED_COUNTS[case]
        pattern_count = sum(histogram[value] for value in allowed)
        assert pattern_count == EXPECTED_PATTERN_COUNTS[case]
        assert row == {
            "case": str(case),
            "representative": "(" + ",".join(map(str, REPRESENTATIVES[case])) + ")",
            "possible_o": ",".join(map(str, allowed)),
            "reflected_patterns": str(pattern_count),
            "boundary_sign_restrictions": EXPECTED_BOUNDARY[case],
        }

    assert feasible_signs(0, 4) == {(-1, -1), (-1, 1)}
    assert feasible_signs(0, 20) == {(-1, 1), (1, 1)}
    assert feasible_signs(2, 4) == {(-1, -1), (-1, 1)}
    assert feasible_signs(5, 2) == {(-1, -1), (-1, 1)}

    output = ["diagonal_sum_counts_checked=0..21"]
    for case in range(6):
        output.append(
            f"case={case}; possible_o="
            + ",".join(map(str, EXPECTED_COUNTS[case]))
            + f"; reflected_patterns={EXPECTED_PATTERN_COUNTS[case]}"
        )
    output.append("certificate=verified")
    assert (Path(__file__).parent / "verification_output.txt").read_text(
        encoding="utf-8"
    ) == "\n".join(output) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
