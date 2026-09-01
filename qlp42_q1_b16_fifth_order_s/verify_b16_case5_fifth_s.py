#!/usr/bin/env python3
"""Exact fifth-order S-component test for QLP-42 q=1, b=16 case 5."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from collections import Counter, defaultdict
from csv import DictReader
from pathlib import Path

G = tuple[int, int]
N = 21
PI = (1, 1)
FOURTH_DEPENDENCY_SHA256 = (
    "a5f616a19e241bcdced0962a2843631d1bb13a30de41cfbc05a2c0999e74bacf"
)
SUM_DEPENDENCY_SHA256 = (
    "d0ecc7b462f6a3e87eb1a3feb0acb13dcd326ddcc83cd84c6aa23c48349fc730"
)
EXCLUDED_DEPENDENCY_SHA256 = (
    "27e72ae20e6d45ff441c976a053cb86d0f6b8c9f5177b022f5dbde982a4d2e1b"
)


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: G, right: G) -> G:
    return left[0] - right[0], left[1] - right[1]


def scale(value: G, coefficient: int) -> G:
    return value[0] * coefficient, value[1] * coefficient


def load_fourth():
    path = (
        Path(__file__).parent.parent
        / "qlp42_q1_b16_fourth_order"
        / "verify_b16_fourth_order.py"
    )
    assert hashlib.sha256(path.read_bytes()).hexdigest() == FOURTH_DEPENDENCY_SHA256
    spec = importlib.util.spec_from_file_location("b16_fourth_dependency", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_excluded_dependency() -> set[tuple[str, str]]:
    directory = Path(__file__).parent.parent / "qlp42_q1_b16_sum_intersection"
    verifier = directory / "verify_b16_sum_intersection.py"
    table = directory / "excluded_case5_orbits.tsv"
    assert hashlib.sha256(verifier.read_bytes()).hexdigest() == SUM_DEPENDENCY_SHA256
    assert hashlib.sha256(table.read_bytes()).hexdigest() == EXCLUDED_DEPENDENCY_SHA256
    with table.open(encoding="utf-8", newline="") as handle:
        rows = list(DictReader(handle, delimiter="\t"))
    excluded = {
        (row["b_equal_positions"], row["a_opposite_orbit_representative"])
        for row in rows
    }
    assert len(excluded) == 4
    return excluded


def quotient_parities(fourth, value: G) -> tuple[int, int]:
    for _ in range(3):
        value = fourth.div_pi(value)
    return value[0] & 1, value[1] & 1


def verify_local_fifth_order_formulas(fourth) -> int:
    checks = 0
    diagonal_baseline = fourth.scale(
        fourth.multiply(fourth.unit(0, 0), fourth.conjugate(fourth.unit(0, 0))),
        2,
    )
    for left_axis in (0, 1):
        for right_axis in (0, 1):
            for left_sign in (0, 1):
                for right_sign in (0, 1):
                    value = fourth.scale(
                        fourth.multiply(
                            fourth.unit(left_axis, left_sign),
                            fourth.conjugate(fourth.unit(right_axis, right_sign)),
                        ),
                        2,
                    )
                    actual = quotient_parities(
                        fourth, fourth.subtract(value, diagonal_baseline)
                    )
                    product = left_axis & right_axis
                    expected = (
                        left_axis ^ product ^ left_sign ^ right_sign,
                        right_axis ^ product ^ left_sign ^ right_sign,
                    )
                    assert actual == expected
                    checks += 1

    for center_axis in (0, 1):
        for theta in (0, 1):
            center_baseline = fourth.add(
                fourth.multiply(
                    fourth.unit(center_axis, 0),
                    fourth.conjugate(active(fourth, 0, 0)),
                ),
                fourth.multiply(
                    active(fourth, theta, 0),
                    fourth.conjugate(fourth.unit(center_axis, 0)),
                ),
            )
            for common_axis in (0, 1):
                for plus_sign in (0, 1):
                    for minus_sign in (0, 1):
                        for center_sign in (0, 1):
                            center = fourth.unit(center_axis, center_sign)
                            plus = active(fourth, common_axis, plus_sign)
                            minus = active(fourth, common_axis ^ theta, minus_sign)
                            value = fourth.add(
                                fourth.multiply(center, fourth.conjugate(plus)),
                                fourth.multiply(minus, fourth.conjugate(center)),
                            )
                            actual = quotient_parities(
                                fourth, fourth.subtract(value, center_baseline)
                            )
                            shared = (
                                common_axis
                                ^ (common_axis & plus_sign)
                                ^ (common_axis & minus_sign)
                                ^ center_sign
                                ^ (common_axis & center_axis)
                                ^ (plus_sign & center_axis)
                                ^ (minus_sign & center_axis)
                                ^ (common_axis & theta)
                                ^ (minus_sign & theta)
                                ^ (center_sign & theta)
                            )
                            expected = (
                                shared ^ plus_sign,
                                shared ^ minus_sign,
                            )
                            assert actual == expected
                            checks += 1
    assert checks == 80
    return checks


def delta_bits(fourth, values: list[G], baseline: list[G]) -> int:
    result = 0
    for shift in range(1, 11):
        value = fourth.subtract(fourth.paf(values, shift), fourth.paf(baseline, shift))
        for _ in range(3):
            value = fourth.div_pi(value)
        result |= (value[0] & 1) << (shift - 1)
        result |= (value[1] & 1) << (10 + shift - 1)
    return result


def residual_bits(fourth, a_values: list[G], b_values: list[G]) -> int:
    result = 0
    for shift in range(1, 11):
        residual = fourth.subtract(
            fourth.add(fourth.paf(a_values, shift), fourth.paf(b_values, shift)),
            fourth.target_s(shift),
        )
        for _ in range(3):
            residual = fourth.div_pi(residual)
        result |= (residual[0] & 1) << (shift - 1)
        result |= (residual[1] & 1) << (10 + shift - 1)
    return result


def active(fourth, axis: int, sign: int) -> G:
    return fourth.multiply(PI, fourth.unit(axis, sign))


def positions(word: int) -> str:
    return ",".join(str(index) for index in range(N) if (word >> index) & 1)


def case_five_orbits(fourth, base_module, excluded):
    records = fourth.mod7_survivors(base_module)
    results, _ = fourth.classify_lifts(base_module, records)
    grouped = {}
    for result in results:
        key = (result.b_index, base_module.orbit_representative(result.a_word))
        grouped.setdefault(key, []).append(result)
    assert len(grouped) == 36
    assert {len(group) for group in grouped.values()} == {21}
    assert sum(group[0].soluble for group in grouped.values()) == 32
    survivors = []
    for group in grouped.values():
        result = group[0]
        if not result.soluble:
            continue
        equal_word = ((1 << N) - 1) ^ result.b_word ^ 1
        key = (
            positions(equal_word),
            ",".join(map(str, base_module.orbit_representative(result.a_word))),
        )
        if key not in excluded:
            survivors.append(result)
    assert len(survivors) == 28
    return survivors


def half_states(values: list[G], columns: list[int]) -> dict[G, set[int]]:
    states: dict[G, set[int]] = {(0, 0): {0}}
    for value, column in zip(values, columns, strict=True):
        changed = scale(value, -2)
        next_states = {key: set(residues) for key, residues in states.items()}
        for partial_sum, residues in states.items():
            destination = next_states.setdefault(add(partial_sum, changed), set())
            destination.update(residue ^ column for residue in residues)
        states = next_states
    return states


def sum_counts(values: list[G]) -> Counter[G]:
    states: Counter[G] = Counter({(0, 0): 1})
    for value in values:
        changed = scale(value, -2)
        next_states = states.copy()
        for partial_sum, multiplicity in states.items():
            next_states[add(partial_sum, changed)] += multiplicity
        states = next_states
    return states


def b_delta_set(fourth, base_module, result) -> tuple[set[int], int, int]:
    theta = fourth.theta_values(base_module, result.b_word)
    shifts = [shift for shift in range(1, 11) if (result.b_word >> shift) & 1]
    assert len(shifts) == 8
    baseline = [(0, 0)] * N
    for shift in shifts:
        baseline[shift] = active(fourth, 0, 0)
        baseline[N - shift] = active(fourth, theta[shift - 1], 0)
    baseline[0] = (0, -1)

    reachable = set()
    exact_assignments = 0
    sign_affinity_checks = 0
    for axes in range(1 << 8):
        word = [(0, 0)] * N
        sign_positions = []
        for index, shift in enumerate(shifts):
            axis = (axes >> index) & 1
            word[shift] = active(fourth, axis, 0)
            word[N - shift] = active(fourth, axis ^ theta[shift - 1], 0)
            sign_positions.extend((shift, N - shift))
        word[0] = (0, -1)
        sign_positions.append(0)

        axis_delta = delta_bits(fourth, word, baseline)
        columns = []
        for position in sign_positions:
            changed = word.copy()
            changed[position] = scale(changed[position], -1)
            columns.append(delta_bits(fourth, changed, word))

        audit_mask = ((axes + 1) * 0x1F35 ^ (result.b_index + 1) * 0x2A7D) & (
            (1 << len(sign_positions)) - 1
        )
        audit_word = word.copy()
        predicted = axis_delta
        for index, (position, column) in enumerate(
            zip(sign_positions, columns, strict=True)
        ):
            if (audit_mask >> index) & 1:
                audit_word[position] = scale(audit_word[position], -1)
                predicted ^= column
        assert delta_bits(fourth, audit_word, baseline) == predicted
        sign_affinity_checks += 1

        values = [word[position] for position in sign_positions]
        midpoint = len(values) // 2
        left = half_states(values[:midpoint], columns[:midpoint])
        right = half_states(values[midpoint:], columns[midpoint:])
        left_counts = sum_counts(values[:midpoint])
        right_counts = sum_counts(values[midpoint:])
        baseline_sum = (
            sum(value[0] for value in values),
            sum(value[1] for value in values),
        )
        required = subtract((0, -3), baseline_sum)
        exact_assignments += sum(
            multiplicity * right_counts.get(subtract(required, left_sum), 0)
            for left_sum, multiplicity in left_counts.items()
        )
        for left_sum, left_residues in left.items():
            right_residues = right.get(subtract(required, left_sum))
            if right_residues is None:
                continue
            for left_residue in left_residues:
                reachable.update(
                    axis_delta ^ left_residue ^ right_residue
                    for right_residue in right_residues
                )
    assert exact_assignments == 804_968
    assert sign_affinity_checks == 256
    return reachable, exact_assignments, sign_affinity_checks


def a_exact_words(fourth, a_word: int) -> tuple[list[G], list[list[G]]]:
    active_positions = [position for position in range(N) if (a_word >> position) & 1]
    assert len(active_positions) == 5
    baseline = [(0, 0)] * N
    for position in active_positions:
        baseline[position] = active(fourth, 0, 0)
    exact = []
    for real_position in active_positions:
        word = [(0, 0)] * N
        for position in active_positions:
            word[position] = active(
                fourth,
                0 if position == real_position else 1,
                0 if position == real_position else 1,
            )
        assert tuple(map(sum, zip(*word, strict=True))) == (5, -3)
        exact.append(word)
    return baseline, exact


def main() -> None:
    fourth = load_fourth()
    base_module = fourth.load_dependency()
    excluded = load_excluded_dependency()
    local_formula_checks = verify_local_fifth_order_formulas(fourth)
    survivors = case_five_orbits(fourth, base_module, excluded)
    by_b = defaultdict(list)
    for result in survivors:
        by_b[result.b_index].append(result)

    rows = []
    surviving = []
    exact_assignment_counts = set()
    sign_affinity_checks = 0
    for b_index, results in sorted(by_b.items()):
        b_reachable, exact_assignments, audits = b_delta_set(
            fourth, base_module, results[0]
        )
        exact_assignment_counts.add(exact_assignments)
        sign_affinity_checks += audits
        for result in results:
            baseline_words = fourth.build_words(
                base_module, result.a_word, result.b_word
            )
            combined_baseline = residual_bits(
                fourth, baseline_words[0], baseline_words[2]
            )
            a_baseline, a_words = a_exact_words(fourth, result.a_word)
            feasible = any(
                (combined_baseline ^ delta_bits(fourth, word, a_baseline))
                in b_reachable
                for word in a_words
            )
            if feasible:
                surviving.append(result)
            equal_word = ((1 << N) - 1) ^ result.b_word ^ 1
            rows.append(
                {
                    "b_equal_positions": positions(equal_word),
                    "a_opposite_orbit_representative": ",".join(
                        map(str, base_module.orbit_representative(result.a_word))
                    ),
                    "fourth_order_rank": str(result.rank),
                    "b_fifth_residue_fingerprints": str(len(b_reachable)),
                    "fifth_s_soluble": str(int(feasible)),
                }
            )
    if "--dump-orbits" in sys.argv:
        print(*rows[0], sep="\t")
        for row in rows:
            print(*row.values(), sep="\t")
        return

    with (Path(__file__).parent / "orbit_table.tsv").open(
        encoding="utf-8", newline=""
    ) as handle:
        expected_rows = list(DictReader(handle, delimiter="\t"))
    assert rows == expected_rows

    assert exact_assignment_counts == {804_968}
    assert sign_affinity_checks == 4_608
    surviving_b_masks = len({result.b_index for result in surviving})
    assert (surviving_b_masks, len(surviving)) == (11, 16)

    output = [
        f"fourth_dependency_sha256={FOURTH_DEPENDENCY_SHA256}",
        f"sum_dependency_sha256={SUM_DEPENDENCY_SHA256}",
        f"excluded_dependency_sha256={EXCLUDED_DEPENDENCY_SHA256}",
        f"local_fifth_order_formula_checks={local_formula_checks}",
        f"direct_sign_affinity_checks={sign_affinity_checks}",
        f"exact_b_s_phase_assignments_per_mask={next(iter(exact_assignment_counts))}",
        f"exact_b_s_phase_assignments_total={18 * next(iter(exact_assignment_counts))}",
        f"case5_input_b_masks={len(by_b)}",
        f"case5_input_labeled_pairs={21 * len(survivors)}",
        f"case5_input_a_rotation_orbits={len(survivors)}",
        f"fifth_s_surviving_b_masks={surviving_b_masks}",
        f"fifth_s_surviving_labeled_pairs={21 * len(surviving)}",
        f"fifth_s_surviving_a_rotation_orbits={len(surviving)}",
        f"fifth_s_eliminated_b_masks={len(by_b) - surviving_b_masks}",
        f"fifth_s_eliminated_labeled_pairs={21 * (len(survivors) - len(surviving))}",
        f"fifth_s_eliminated_a_rotation_orbits={len(survivors) - len(surviving)}",
        "certificate=verified",
    ]
    expected_output = (Path(__file__).parent / "verification_output.txt").read_text(
        encoding="utf-8"
    )
    assert expected_output == "\n".join(output) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
