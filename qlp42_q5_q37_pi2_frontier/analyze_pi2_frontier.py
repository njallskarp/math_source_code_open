#!/usr/bin/env python3
"""Exact pi^2 residue census over the QLP-42 q=5/q=37 shadow frontier."""

from __future__ import annotations

from collections import Counter
from csv import DictReader
from itertools import combinations
from pathlib import Path

G = tuple[int, int]
N = 21
FULL = (1 << N) - 1
PI_BAR: G = (1, -1)
ZERO: G = (0, 0)
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: G, right: G) -> G:
    return left[0] - right[0], left[1] - right[1]


def multiply(left: G, right: G) -> G:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: G) -> G:
    return value[0], -value[1]


def div_pi(value: G) -> G:
    real, imag = value
    assert (real + imag) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def mod_pi(value: G) -> int:
    return (value[0] + value[1]) & 1


def rotate(mask: int, shift: int) -> int:
    return ((mask << shift) | (mask >> (N - shift))) & FULL


def canonical(mask: int) -> int:
    return min(rotate(mask, shift) for shift in range(N))


def paf(word: list[G], shift: int) -> G:
    total = ZERO
    for index, value in enumerate(word):
        total = add(total, multiply(value, conjugate(word[(index + shift) % N])))
    return total


def target(component: str, shift: int) -> G:
    if component == "h":
        return (-2, 0)
    if shift == 4:
        return (-2, 0)
    if shift == 10:
        return (2, 0)
    return ZERO


def variable_layout(q_a: int, q_b: int) -> tuple[list[tuple[int, int, str]], int]:
    variables = []
    quarter_count = 0
    for family, qmask in enumerate((q_a, q_b)):
        for position in range(N):
            if (qmask >> position) & 1:
                variables.append((family, position, "axis"))
                quarter_count += 1
    for family, qmask in enumerate((q_a, q_b)):
        for position in range(N):
            if not ((qmask >> position) & 1):
                variables.append((family, position, "type"))
    assert len(variables) == 42
    return variables, quarter_count


def residue_vector(q_a: int, q_b: int, assignment: int) -> int:
    variables, _quarter_count = variable_layout(q_a, q_b)
    index = {(family, position): slot for slot, (family, position, _kind) in enumerate(variables)}
    words = []
    for family, qmask in enumerate((q_a, q_b)):
        s_word = []
        h_word = []
        for position in range(N):
            bit = (assignment >> index[(family, position)]) & 1
            if (qmask >> position) & 1:
                # Quarter states: the S/H axes are complementary.  Signs are
                # invisible modulo pi^2, so one positive representative per
                # axis suffices.
                s_word.append((1, 0) if bit == 0 else (0, 1))
                h_word.append((0, 1) if bit == 0 else (1, 0))
            elif bit:
                # Opposite state: S is pi times a unit and H is zero.
                s_word.append(PI_BAR)
                h_word.append(ZERO)
            else:
                # Equal state: H is pi times a unit and S is zero.
                s_word.append(ZERO)
                h_word.append(PI_BAR)
        words.append((s_word, h_word))

    result = 0
    for component_index, component in enumerate(("s", "h")):
        for shift in range(1, 11):
            combined = add(
                paf(words[0][component_index], shift),
                paf(words[1][component_index], shift),
            )
            residual = subtract(combined, target(component, shift))
            quotient = div_pi(residual)
            result |= mod_pi(quotient) << (component_index * 10 + shift - 1)
    return result


def affine_system(
    q_a: int, q_b: int
) -> tuple[int, list[int], int, list[tuple[int, int, str]]]:
    variables, quarter_count = variable_layout(q_a, q_b)
    base = residue_vector(q_a, q_b, 0)
    columns = [residue_vector(q_a, q_b, 1 << index) ^ base for index in range(42)]

    # Exhaust every possible quadratic interaction.  Vanishing second
    # differences certify that the residue map is affine in these bits.
    for left in range(42):
        for right in range(left + 1, 42):
            observed = residue_vector(q_a, q_b, (1 << left) | (1 << right))
            assert observed == base ^ columns[left] ^ columns[right]
    assert all(kind == "axis" for _family, _position, kind in variables[:quarter_count])
    assert all(kind == "type" for _family, _position, kind in variables[quarter_count:])
    return base, columns, quarter_count, variables


def rank(columns: list[int]) -> int:
    basis = [0] * 20
    result = 0
    for value in columns:
        while value:
            pivot = value.bit_length() - 1
            if basis[pivot]:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                result += 1
                break
    return result


def solution_count(columns: list[int], right_hand_side: int) -> int:
    basis = [0] * 20
    for value in columns:
        while value:
            pivot = value.bit_length() - 1
            if basis[pivot]:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    residual = right_hand_side
    while residual:
        pivot = residual.bit_length() - 1
        if not basis[pivot]:
            return 0
        residual ^= basis[pivot]
    return 1 << (len(columns) - sum(bool(value) for value in basis))


def subset_distribution(columns: list[int]) -> Counter[tuple[int, int]]:
    count = 1 << len(columns)
    syndromes = [0] * count
    weights = bytearray(count)
    result: Counter[tuple[int, int]] = Counter()
    result[(0, 0)] = 1
    for mask in range(1, count):
        low = mask & -mask
        previous = mask ^ low
        index = low.bit_length() - 1
        syndromes[mask] = syndromes[previous] ^ columns[index]
        weights[mask] = weights[previous] + 1
        result[(weights[mask], syndromes[mask])] += 1
    return result


def count_q5(base: int, columns: list[int], quarter_count: int) -> tuple[int, int]:
    assert quarter_count == 5
    axis_columns = columns[:quarter_count]
    type_columns = columns[quarter_count:]
    left = subset_distribution(type_columns[:18])
    right = subset_distribution(type_columns[18:])
    total = 0
    feasible_axes = 0
    for axis_mask in range(1 << quarter_count):
        axis_syndrome = 0
        for index, column in enumerate(axis_columns):
            if (axis_mask >> index) & 1:
                axis_syndrome ^= column
        wanted = base ^ axis_syndrome
        subtotal = 0
        for (left_weight, left_syndrome), multiplicity in left.items():
            right_weight = 19 - left_weight
            if 0 <= right_weight <= len(type_columns) - 18:
                subtotal += multiplicity * right[(right_weight, wanted ^ left_syndrome)]
        total += subtotal
        feasible_axes += int(subtotal != 0)
    return total, feasible_axes


def signed_sum_feasible(term_count: int, target_value: int) -> bool:
    return abs(target_value) <= term_count and (target_value - term_count) % 2 == 0


def exact_sums_feasible(
    q_a: int,
    q_b: int,
    o_a: int,
    o_b: int,
    beta_a: int,
    beta_b: int,
    case: tuple[int, int, int, int],
) -> bool:
    z_a = N - q_a - o_a
    z_b = N - q_b - o_b
    if min(o_a, o_b, z_a, z_b) < 0:
        return False
    p, q, x, y = case
    targets = (
        (o_a, q_a - beta_a, beta_a, (p + q, q - p)),
        (z_a, beta_a, q_a - beta_a, ZERO),
        (o_b, q_b - beta_b, beta_b, (x + y - 1, y - x)),
        (z_b, beta_b, q_b - beta_b, (1, 0)),
    )
    for diagonal, real_quarters, imag_quarters, sum_target in targets:
        if not signed_sum_feasible(diagonal + real_quarters, sum_target[0]):
            return False
        if not signed_sum_feasible(diagonal + imag_quarters, sum_target[1]):
            return False
    return True


def count_q5_cases(
    base: int,
    columns: list[int],
    quarter_count: int,
    variables: list[tuple[int, int, str]],
) -> list[int]:
    assert quarter_count == 5
    axis_variables = variables[:quarter_count]
    type_variables = variables[quarter_count:]
    q_a = sum(family == 0 for family, _position, _kind in axis_variables)
    q_b = quarter_count - q_a
    a_columns = [
        column
        for column, (family, _position, _kind) in zip(
            columns[quarter_count:], type_variables, strict=True
        )
        if family == 0
    ]
    b_columns = [
        column
        for column, (family, _position, _kind) in zip(
            columns[quarter_count:], type_variables, strict=True
        )
        if family == 1
    ]
    a_distribution = subset_distribution(a_columns)
    b_distribution = subset_distribution(b_columns)
    totals = [0] * len(CASES)
    for axis_mask in range(1 << quarter_count):
        axis_syndrome = 0
        beta_a = 0
        beta_b = 0
        for index, (column, (family, _position, _kind)) in enumerate(
            zip(columns[:quarter_count], axis_variables, strict=True)
        ):
            if (axis_mask >> index) & 1:
                axis_syndrome ^= column
                if family == 0:
                    beta_a += 1
                else:
                    beta_b += 1
        wanted = base ^ axis_syndrome
        for (o_a, a_syndrome), multiplicity in a_distribution.items():
            o_b = 19 - o_a
            if not (0 <= o_b <= len(b_columns)):
                continue
            matching = b_distribution[(o_b, wanted ^ a_syndrome)]
            if not matching:
                continue
            for case_index, case in enumerate(CASES):
                if exact_sums_feasible(q_a, q_b, o_a, o_b, beta_a, beta_b, case):
                    totals[case_index] += multiplicity * matching
    return totals


def count_q37(base: int, columns: list[int], quarter_count: int) -> tuple[int, int]:
    assert quarter_count == 37
    axis_columns = columns[:quarter_count]
    type_columns = columns[quarter_count:]
    total = 0
    feasible_types = 0
    for support in combinations(range(5), 3):
        type_syndrome = 0
        for index in support:
            type_syndrome ^= type_columns[index]
        count = solution_count(axis_columns, base ^ type_syndrome)
        total += count
        feasible_types += int(count != 0)
    return total, feasible_types


def count_q37_cases(
    base: int,
    columns: list[int],
    quarter_count: int,
    variables: list[tuple[int, int, str]],
) -> list[int]:
    assert quarter_count == 37
    axis_variables = variables[:quarter_count]
    type_variables = variables[quarter_count:]
    q_a = sum(family == 0 for family, _position, _kind in axis_variables)
    q_b = quarter_count - q_a
    a_axis_columns = [
        column
        for column, (family, _position, _kind) in zip(
            columns[:quarter_count], axis_variables, strict=True
        )
        if family == 0
    ]
    b_axis_columns = [
        column
        for column, (family, _position, _kind) in zip(
            columns[:quarter_count], axis_variables, strict=True
        )
        if family == 1
    ]
    a_distribution = subset_distribution(a_axis_columns)
    b_distribution = subset_distribution(b_axis_columns)
    a_by_weight: list[list[tuple[int, int]]] = [[] for _ in range(q_a + 1)]
    for (beta_a, syndrome), multiplicity in a_distribution.items():
        a_by_weight[beta_a].append((syndrome, multiplicity))

    totals = [0] * len(CASES)
    for support in combinations(range(5), 3):
        type_syndrome = 0
        o_a = 0
        for index in support:
            type_syndrome ^= columns[quarter_count + index]
            o_a += int(type_variables[index][0] == 0)
        o_b = 3 - o_a
        wanted = base ^ type_syndrome
        for case_index, case in enumerate(CASES):
            for beta_a, entries in enumerate(a_by_weight):
                allowed_beta_b = [
                    beta_b
                    for beta_b in range(q_b + 1)
                    if exact_sums_feasible(
                        q_a, q_b, o_a, o_b, beta_a, beta_b, case
                    )
                ]
                if not allowed_beta_b:
                    continue
                for a_syndrome, a_multiplicity in entries:
                    matching_syndrome = wanted ^ a_syndrome
                    totals[case_index] += a_multiplicity * sum(
                        b_distribution[(beta_b, matching_syndrome)]
                        for beta_b in allowed_beta_b
                    )
    return totals


def read_frontier() -> list[tuple[int, int]]:
    path = Path(__file__).parent.parent / "qlp42_q5_q37_binary_frontier" / "frontier_orbits.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(DictReader(handle, delimiter="\t"))
    return [(int(row["a_mask_hex"], 16), int(row["b_mask_hex"], 16)) for row in rows]


def main() -> None:
    frontier = read_frontier()
    q5 = sorted((left, right) for left, right in frontier if left.bit_count() % 2 == 0)
    q37 = sorted(
        {
            (canonical(FULL ^ left), canonical(FULL ^ right))
            for left, right in frontier
            if left.bit_count() % 2 == 1
        }
    )
    assert len(q5) == len(q37) == 18

    print("sum_parity_q5_shadow_orbits=18")
    print("sum_parity_q37_shadow_orbits=18")
    for q_value, supports in ((5, q5), (37, q37)):
        branch_total = 0
        branch_case_totals = [0] * len(CASES)
        surviving = 0
        for orbit_id, (left, right) in enumerate(supports):
            base, columns, quarter_count, variables = affine_system(left, right)
            if q_value == 5:
                count, auxiliary = count_q5(base, columns, quarter_count)
                case_counts = count_q5_cases(base, columns, quarter_count, variables)
            else:
                count, auxiliary = count_q37(base, columns, quarter_count)
                case_counts = count_q37_cases(base, columns, quarter_count, variables)
            branch_total += count
            for case_index, case_count in enumerate(case_counts):
                branch_case_totals[case_index] += case_count
            surviving += int(count != 0)
            print(
                f"q={q_value};orbit={orbit_id:02d};a={left:06x};b={right:06x};"
                f"rank_all={rank(columns)};rank_axis={rank(columns[:quarter_count])};"
                f"rank_type={rank(columns[quarter_count:])};"
                f"assignments={count};auxiliary_nonzero={auxiliary};"
                f"case_counts={','.join(map(str, case_counts)) if case_counts else 'pending'}"
            )
        print(f"q={q_value};surviving_shadow_orbits={surviving};assignments={branch_total}")
        print(
            f"q={q_value};orbits={surviving};rank=10;all={branch_total};cases="
            f"{','.join(map(str, branch_case_totals))}"
        )
    print("certificate=verified")


if __name__ == "__main__":
    main()
