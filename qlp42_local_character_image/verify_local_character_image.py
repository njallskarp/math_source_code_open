#!/usr/bin/env python3
"""Verify the local-character image obstruction for QLP-42."""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache

Gaussian = tuple[int, int]
State = tuple[int, int, int, int, int, int]

MU4: tuple[Gaussian, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIAGONALS: tuple[Gaussian, ...] = ((1, 1), (1, -1), (-1, 1), (-1, -1))
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)
EXPECTED_MISSING = {
    0: (37,),
    1: (-37, 35, 37),
    2: (-37, 35, 37),
    3: (-37, -35, 35, 37),
    4: (-37, -35, 35, 37),
    5: (-37, 35, 37),
}


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def multiply(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def divide_by_one_plus_i(value: Gaussian) -> Gaussian:
    real, imag = value
    assert (real + imag) % 2 == 0
    assert (imag - real) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def local_states() -> tuple[State, ...]:
    result = []
    for x in MU4:
        for y in MU4:
            s = divide_by_one_plus_i(subtract(x, y))
            h = divide_by_one_plus_i(add(x, y))
            cross = multiply(s, conjugate(h))
            epsilon_pair = cross[1], -cross[0]
            assert epsilon_pair[1] == 0
            epsilon = epsilon_pair[0]
            assert epsilon in (-1, 0, 1)
            result.append((*s, *h, abs(epsilon), epsilon))
    assert len(set(result)) == 16
    return tuple(result)


STATES = local_states()
STATE_INDEX = {state: index for index, state in enumerate(STATES)}


def unit_sum_formula(length: int) -> tuple[Gaussian, ...]:
    return tuple(
        (real, imag)
        for real in range(-length, length + 1)
        for imag in range(-length, length + 1)
        if abs(real) + abs(imag) <= length
        and (length - abs(real) - abs(imag)) % 2 == 0
    )


def diagonal_sum_formula(length: int) -> tuple[Gaussian, ...]:
    return tuple(
        (real, imag)
        for real in range(-length, length + 1)
        for imag in range(-length, length + 1)
        if (real - length) % 2 == 0 and (imag - length) % 2 == 0
    )


UNIT_SUMS = tuple(unit_sum_formula(length) for length in range(22))
DIAGONAL_SUMS = tuple(set(diagonal_sum_formula(length)) for length in range(22))


def verify_sum_formulas() -> None:
    units = {(0, 0)}
    diagonals = {(0, 0)}
    for length in range(22):
        assert units == set(UNIT_SUMS[length])
        assert diagonals == DIAGONAL_SUMS[length]
        units = {add(value, step) for value in units for step in MU4}
        diagonals = {add(value, step) for value in diagonals for step in DIAGONALS}


def family_support(s_target: Gaussian, h_target: Gaussian):
    witnesses = {}
    for quarter in range(22):
        for sigma in range(-quarter, quarter + 1, 2):
            plus = (quarter + sigma) // 2
            minus = (quarter - sigma) // 2
            found = None
            for opposite in range(22 - quarter):
                equal = 21 - quarter - opposite
                for u_plus in UNIT_SUMS[plus]:
                    if found is not None:
                        break
                    for u_minus in UNIT_SUMS[minus]:
                        s_quarter = add(u_plus, u_minus)
                        h_quarter = (
                            u_plus[1] - u_minus[1],
                            -u_plus[0] + u_minus[0],
                        )
                        s_diagonal = subtract(s_target, s_quarter)
                        h_diagonal = subtract(h_target, h_quarter)
                        if (
                            s_diagonal in DIAGONAL_SUMS[opposite]
                            and h_diagonal in DIAGONAL_SUMS[equal]
                        ):
                            found = (
                                opposite,
                                equal,
                                u_plus,
                                u_minus,
                                s_diagonal,
                                h_diagonal,
                            )
                            break
                if found is not None:
                    break
            if found is not None:
                witnesses[(quarter, sigma)] = found
    return witnesses


def unit_decomposition(length: int, target: Gaussian) -> list[Gaussian]:
    real, imag = target
    result = []
    result.extend([(1 if real > 0 else -1, 0)] * abs(real))
    result.extend([(0, 1 if imag > 0 else -1)] * abs(imag))
    remaining = length - abs(real) - abs(imag)
    assert remaining >= 0 and remaining % 2 == 0
    result.extend([(1, 0), (-1, 0)] * (remaining // 2))
    assert len(result) == length
    assert tuple(map(sum, zip(*result, strict=True))) == target if result else target == (0, 0)
    return result


def diagonal_decomposition(length: int, target: Gaussian) -> list[Gaussian]:
    real, imag = target
    positive_real = (length + real) // 2
    positive_imag = (length + imag) // 2
    result = [
        (
            1 if index < positive_real else -1,
            1 if index < positive_imag else -1,
        )
        for index in range(length)
    ]
    assert len(result) == length
    assert tuple(map(sum, zip(*result, strict=True))) == target if result else target == (0, 0)
    return result


def state_counts(
    s_target: Gaussian,
    h_target: Gaussian,
    quarter: int,
    sigma: int,
    witness,
) -> tuple[int, ...]:
    opposite, equal, u_plus, u_minus, s_diagonal, h_diagonal = witness
    plus = (quarter + sigma) // 2
    minus = (quarter - sigma) // 2
    states = []
    states.extend((*value, 0, 0, 0, 0) for value in diagonal_decomposition(opposite, s_diagonal))
    states.extend((0, 0, *value, 0, 0) for value in diagonal_decomposition(equal, h_diagonal))
    for value in unit_decomposition(plus, u_plus):
        h_value = value[1], -value[0]
        states.append((*value, *h_value, 1, 1))
    for value in unit_decomposition(minus, u_minus):
        h_value = -value[1], value[0]
        states.append((*value, *h_value, 1, -1))
    assert len(states) == 21
    counts = [0] * 16
    for state in states:
        counts[STATE_INDEX[state]] += 1
    aggregate = tuple(
        sum(counts[index] * STATES[index][coordinate] for index in range(16))
        for coordinate in range(6)
    )
    assert aggregate == (*s_target, *h_target, quarter, sigma)
    return tuple(counts)


def family_targets(case) -> tuple[tuple[Gaussian, Gaussian], tuple[Gaussian, Gaussian]]:
    p, q, x, y = case
    return (
        ((p + q, q - p), (0, 0)),
        ((x + y - 1, y - x), (1, 0)),
    )


def diagonal_minimum(target: Gaussian) -> int:
    if (target[0] - target[1]) % 2:
        return 10**9
    minimum = max(abs(target[0]), abs(target[1]))
    if (minimum - target[0]) % 2:
        minimum += 1
    return minimum


@lru_cache(maxsize=None)
def mu(target: Gaussian, unit_count: int) -> int:
    return min(
        diagonal_minimum(
            (target[0] - 2 * unit_sum[0], target[1] - 2 * unit_sum[1])
        )
        for unit_sum in UNIT_SUMS[unit_count]
    )


def plus_minus_target(s_target: Gaussian, h_target: Gaussian, sign: int) -> Gaussian:
    assert sign in (-1, 1)
    if sign == 1:
        return s_target[0] - h_target[1], s_target[1] + h_target[0]
    return s_target[0] + h_target[1], s_target[1] - h_target[0]


def family_diagonal_budget(targets, sign: int, oriented_count: int) -> int:
    values = []
    lower = max(0, oriented_count - 21)
    upper = min(21, oriented_count)
    transformed = [plus_minus_target(s, h, sign) for s, h in targets]
    for first_count in range(lower, upper + 1):
        second_count = oriented_count - first_count
        values.append(
            mu(transformed[0], first_count) + mu(transformed[1], second_count)
        )
    return min(values)


def main() -> None:
    verify_sum_formulas()
    opposite = [state for state in STATES if state[4] == 0 and state[2:4] == (0, 0)]
    equal = [state for state in STATES if state[4] == 0 and state[:2] == (0, 0)]
    quarter = [state for state in STATES if state[4] == 1]
    assert (len(opposite), len(equal), len(quarter)) == (4, 4, 8)

    support_cache = {}
    manifest = []
    missing = {5: {}, 37: {}}
    survivors = {5: 0, 37: 0}
    budget_excluded = {}

    for case_index, case in enumerate(CASES):
        targets_a, targets_b = family_targets(case)
        for targets in (targets_a, targets_b):
            support_cache.setdefault(targets, family_support(*targets))
        support_a = support_cache[targets_a]
        support_b = support_cache[targets_b]

        for branch in (5, 37):
            case_missing = []
            for sigma in range(-branch, branch + 1, 2):
                chosen = None
                for key_a in sorted(support_a):
                    key_b = branch - key_a[0], sigma - key_a[1]
                    if key_b in support_b:
                        chosen = key_a, key_b
                        break
                if chosen is None:
                    case_missing.append(sigma)
                    continue
                key_a, key_b = chosen
                counts_a = state_counts(*targets_a, *key_a, support_a[key_a])
                counts_b = state_counts(*targets_b, *key_b, support_b[key_b])
                manifest.append([branch, case_index, sigma, counts_a, counts_b])
                survivors[branch] += 1
            missing[branch][case_index] = tuple(case_missing)

        flagged = []
        for sigma in range(-37, 38, 2):
            plus_count = (37 + sigma) // 2
            minus_count = (37 - sigma) // 2
            plus_budget = family_diagonal_budget(
                (targets_a, targets_b), 1, plus_count
            )
            minus_budget = family_diagonal_budget(
                (targets_a, targets_b), -1, minus_count
            )
            if plus_budget > 5 or minus_budget > 5:
                flagged.append(sigma)
                assert max(plus_budget, minus_budget) >= 7
        budget_excluded[case_index] = tuple(flagged)

    assert missing[5] == {case_index: () for case_index in range(6)}
    assert missing[37] == EXPECTED_MISSING
    assert budget_excluded == EXPECTED_MISSING
    assert survivors == {5: 36, 37: 210}
    assert len(manifest) == 246
    digest = hashlib.sha256(
        json.dumps(manifest, separators=(",", ":")).encode("ascii")
    ).hexdigest()

    print("local_states=16")
    print("q5_fiber_points=36")
    print("q5_excluded=0")
    print("q37_fiber_points=228")
    print("q37_excluded=18")
    print("q37_surviving=210")
    print("excluded_by_case=1,3,3,4,4,3")
    print("minimum_excluded_diagonal_budget=7")
    print(f"survivor_count_manifest_sha256={digest}")
    print("support_or_cell_words_enumerated=0")
    print("certificate=verified")


if __name__ == "__main__":
    main()
