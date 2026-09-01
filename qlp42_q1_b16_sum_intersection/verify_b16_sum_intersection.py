#!/usr/bin/env python3
"""Exact-sum intersection with the QLP-42 q=1, b=16 fourth-order filter."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from collections import Counter
from csv import DictReader
from pathlib import Path

G = tuple[int, int]
PI = (1, 1)
N = 21
COMPONENT_MASK = (1 << 10) - 1
DEPENDENCY_SHA256 = "a5f616a19e241bcdced0962a2843631d1bb13a30de41cfbc05a2c0999e74bacf"
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


def component_bits(value: int, component: int) -> int:
    return (value >> (10 * component)) & COMPONENT_MASK


def load_fourth_order():
    path = (
        Path(__file__).parent.parent
        / "qlp42_q1_b16_fourth_order"
        / "verify_b16_fourth_order.py"
    )
    assert hashlib.sha256(path.read_bytes()).hexdigest() == DEPENDENCY_SHA256
    spec = importlib.util.spec_from_file_location("b16_fourth_order_dependency", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def orbit_representatives(fourth, base_module):
    records = fourth.mod7_survivors(base_module)
    results, direct_checks = fourth.classify_lifts(base_module, records)
    assert direct_checks == 756

    grouped = {}
    for result in results:
        key = (result.b_index, base_module.orbit_representative(result.a_word))
        grouped.setdefault(key, []).append(result)
    assert len(grouped) == 36
    assert {len(group) for group in grouped.values()} == {21}
    assert all(
        len({(item.b_word, item.rank, item.soluble) for item in group}) == 1
        for group in grouped.values()
    )
    survivors = [group[0] for _, group in sorted(grouped.items()) if group[0].soluble]
    assert len(survivors) == 32
    return survivors


def affine_columns(fourth, base_module, result) -> tuple[int, list[int]]:
    base = fourth.residual_vector(base_module, result.a_word, result.b_word)
    columns = []
    for variable in range(53):
        assignment = [0] * 53
        assignment[variable] = 1
        columns.append(
            fourth.residual_vector(
                base_module, result.a_word, result.b_word, assignment
            )
            ^ base
        )
    return base, columns


def active_value(fourth, axis: int, sign: int) -> G:
    return fourth.multiply(PI, fourth.unit(axis, sign))


def direct_component_residual(
    fourth, left: list[G], right: list[G], component: int
) -> int:
    result = 0
    for shift in range(1, 11):
        target = fourth.target_s(shift) if component == 0 else (-2, 0)
        residual = fourth.subtract(
            fourth.add(fourth.paf(left, shift), fourth.paf(right, shift)), target
        )
        result |= fourth.pi3_bit(residual) << (shift - 1)
    return result


def verify_phase_group_deltas(fourth, base_module, result, columns: list[int]) -> int:
    """Audit every local phase choice against direct exact autocorrelation."""
    words = fourth.build_words(base_module, result.a_word, result.b_word)
    theta = fourth.theta_values(base_module, result.b_word)
    checks = 0
    for component in (0, 1):
        left = words[component]
        right = words[component + 2]
        baseline = direct_component_residual(fourth, left, right, component)

        for position in range(N):
            a_is_active = bool((result.a_word >> position) & 1) == (component == 0)
            if not a_is_active:
                continue
            for axis in (0, 1):
                for sign in (0, 1):
                    changed = left.copy()
                    changed[position] = active_value(fourth, axis, sign)
                    actual = (
                        direct_component_residual(fourth, changed, right, component)
                        ^ baseline
                    )
                    expected = (
                        component_bits(columns[position], component) if axis else 0
                    )
                    assert actual == expected
                    checks += 1

        for shift in range(1, 11):
            b_is_active = bool((result.b_word >> shift) & 1) == (component == 0)
            if not b_is_active:
                continue
            for common_axis in (0, 1):
                for plus_sign in (0, 1):
                    for minus_sign in (0, 1):
                        changed = right.copy()
                        changed[shift] = active_value(fourth, common_axis, plus_sign)
                        changed[N - shift] = active_value(
                            fourth,
                            common_axis ^ theta[shift - 1],
                            minus_sign,
                        )
                        actual = (
                            direct_component_residual(fourth, left, changed, component)
                            ^ baseline
                        )
                        expected = 0
                        if common_axis:
                            expected ^= component_bits(columns[20 + shift], component)
                        if plus_sign:
                            expected ^= component_bits(columns[30 + shift], component)
                        if minus_sign:
                            expected ^= component_bits(columns[40 + shift], component)
                        assert actual == expected
                        checks += 1

        for sign in (0, 1):
            changed = right.copy()
            if component == 0:
                changed[0] = (0, -1 if not sign else 1)
                expected = component_bits(columns[51], component) if sign else 0
            else:
                changed[0] = (1 if not sign else -1, 0)
                expected = component_bits(columns[52], component) if sign else 0
            actual = (
                direct_component_residual(fourth, left, changed, component) ^ baseline
            )
            assert actual == expected
            checks += 1
    assert checks == 168
    return checks


def phase_groups(
    fourth, base_module, result, component: int, columns: list[int]
) -> tuple[list[tuple[tuple[G, int], ...]], list[tuple[tuple[G, int], ...]]]:
    """Return complete A and B local phase choices as (sum contribution, residue delta)."""
    a_groups = []
    b_groups = []

    for position in range(N):
        a_is_active = bool((result.a_word >> position) & 1) == (component == 0)
        if not a_is_active:
            continue
        options = []
        for axis in (0, 1):
            for sign in (0, 1):
                delta = component_bits(columns[position], component) if axis else 0
                options.append((active_value(fourth, axis, sign), delta))
        assert len({value for value, _ in options}) == 4
        a_groups.append(tuple(sorted(set(options))))

    theta = fourth.theta_values(base_module, result.b_word)
    for shift in range(1, 11):
        b_is_active = bool((result.b_word >> shift) & 1) == (component == 0)
        if not b_is_active:
            continue
        options = []
        phase_pairs = set()
        for common_axis in (0, 1):
            for plus_sign in (0, 1):
                for minus_sign in (0, 1):
                    plus = active_value(fourth, common_axis, plus_sign)
                    minus = active_value(
                        fourth, common_axis ^ theta[shift - 1], minus_sign
                    )
                    phase_pairs.add((plus, minus))
                    delta = 0
                    if common_axis:
                        delta ^= component_bits(columns[20 + shift], component)
                    if plus_sign:
                        delta ^= component_bits(columns[30 + shift], component)
                    if minus_sign:
                        delta ^= component_bits(columns[40 + shift], component)
                    options.append((add(plus, minus), delta))
        assert len(phase_pairs) == 8
        b_groups.append(tuple(sorted(set(options))))

    if component == 0:
        b_groups.append(
            (
                ((0, -1), 0),
                ((0, 1), component_bits(columns[51], component)),
            )
        )
        assert (len(a_groups), len(b_groups)) == (5, 9)
    else:
        b_groups.append(
            (
                ((1, 0), 0),
                ((-1, 0), component_bits(columns[52], component)),
            )
        )
        assert (len(a_groups), len(b_groups)) == (16, 3)
    return a_groups, b_groups


def reachable(groups: list[tuple[tuple[G, int], ...]]) -> dict[G, set[int]]:
    """Exact forward dynamic program for Gaussian sums and ten residue bits."""
    states: dict[G, set[int]] = {(0, 0): {0}}
    for options in groups:
        next_states: dict[G, set[int]] = {}
        for partial_sum, residues in states.items():
            for value, delta in options:
                destination = next_states.setdefault(add(partial_sum, value), set())
                destination.update(residue ^ delta for residue in residues)
        states = next_states
    return states


def target_sums(case: tuple[int, int, int, int], component: int) -> tuple[G, G]:
    p, q, x, y = case
    if component == 0:
        return (p + q, q - p), (x + y - 1, y - x)
    return (0, 0), (1, 0)


def positions(word: int) -> str:
    return ",".join(str(index) for index in range(N) if (word >> index) & 1)


def analyze(fourth, base_module, survivors):
    case_orbits = Counter()
    case_b_masks: dict[int, set[int]] = {case: set() for case in range(len(CASES))}
    excluded_case_five = []
    reachability_tables = 0
    local_phase_checks = 0

    for result in survivors:
        base, columns = affine_columns(fourth, base_module, result)
        local_phase_checks += verify_phase_group_deltas(
            fourth, base_module, result, columns
        )
        component_data = []
        for component in (0, 1):
            a_groups, b_groups = phase_groups(
                fourth, base_module, result, component, columns
            )
            a_reachable = reachable(a_groups)
            b_reachable = reachable(b_groups)
            reachability_tables += 2
            component_data.append(
                (
                    component_bits(base, component),
                    a_reachable,
                    b_reachable,
                )
            )

        feasible_cases = []
        for case_number, case in enumerate(CASES):
            feasible = True
            for component, (base_bits, a_reachable, b_reachable) in enumerate(
                component_data
            ):
                target_a, target_b = target_sums(case, component)
                a_residues = a_reachable.get(target_a, set())
                b_residues = b_reachable.get(target_b, set())
                if not any(
                    (base_bits ^ residue) in b_residues for residue in a_residues
                ):
                    feasible = False
                    break
            if feasible:
                feasible_cases.append(case_number)
                case_orbits[case_number] += 1
                case_b_masks[case_number].add(result.b_index)

        assert feasible_cases in (list(range(6)), list(range(5)))
        if 5 not in feasible_cases:
            equal_word = ((1 << N) - 1) ^ result.b_word ^ 1
            excluded_case_five.append(
                (
                    positions(equal_word),
                    ",".join(map(str, base_module.orbit_representative(result.a_word))),
                    result.rank,
                )
            )

    assert case_orbits == {0: 32, 1: 32, 2: 32, 3: 32, 4: 32, 5: 28}
    assert {case: len(masks) for case, masks in case_b_masks.items()} == {
        0: 18,
        1: 18,
        2: 18,
        3: 18,
        4: 18,
        5: 18,
    }
    assert len(excluded_case_five) == 4
    assert local_phase_checks == 5_376
    return (
        case_orbits,
        case_b_masks,
        sorted(excluded_case_five),
        reachability_tables,
        local_phase_checks,
    )


def read_tsv(name: str) -> list[dict[str, str]]:
    with (Path(__file__).parent / name).open(encoding="utf-8", newline="") as handle:
        return list(DictReader(handle, delimiter="\t"))


def main() -> None:
    fourth = load_fourth_order()
    base_module = fourth.load_dependency()
    survivors = orbit_representatives(fourth, base_module)
    (
        case_orbits,
        case_b_masks,
        excluded,
        reachability_tables,
        local_phase_checks,
    ) = analyze(fourth, base_module, survivors)

    case_rows = []
    for case_number, case in enumerate(CASES):
        surviving_orbits = case_orbits[case_number]
        case_rows.append(
            {
                "case": str(case_number),
                "representative": "(" + ",".join(map(str, case)) + ")",
                "surviving_b_masks": str(len(case_b_masks[case_number])),
                "surviving_labeled_pairs": str(21 * surviving_orbits),
                "surviving_a_rotation_orbits": str(surviving_orbits),
                "eliminated_labeled_pairs": str(21 * (32 - surviving_orbits)),
                "eliminated_a_rotation_orbits": str(32 - surviving_orbits),
            }
        )
    assert case_rows == read_tsv("case_table.tsv")

    excluded_rows = [
        {
            "b_equal_positions": equal_positions,
            "a_opposite_orbit_representative": representative,
            "fourth_order_rank": str(rank),
        }
        for equal_positions, representative, rank in excluded
    ]
    assert excluded_rows == read_tsv("excluded_case5_orbits.tsv")

    output = [
        f"dependency_sha256={DEPENDENCY_SHA256}",
        f"fourth_order_surviving_orbits={len(survivors)}",
        f"direct_local_phase_checks={local_phase_checks}",
        f"exact_reachability_tables={reachability_tables}",
    ]
    output.extend(
        f"case={case_number};b_masks={len(case_b_masks[case_number])};"
        f"labeled={21 * case_orbits[case_number]};orbits={case_orbits[case_number]}"
        for case_number in range(len(CASES))
    )
    output.extend(("case5_excluded_orbits=4", "certificate=verified"))
    expected = (Path(__file__).parent / "verification_output.txt").read_text(
        encoding="utf-8"
    )
    assert expected == "\n".join(output) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
