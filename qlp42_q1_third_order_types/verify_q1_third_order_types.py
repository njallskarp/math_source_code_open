#!/usr/bin/env python3
"""Exact certificate for the third-order QLP-42 q=1 type classification."""

from __future__ import annotations

from collections import Counter, defaultdict
from csv import DictReader
from itertools import product
from math import comb, gcd
from pathlib import Path
from typing import NamedTuple

G = tuple[int, int]
LENGTH = 21
HALF_SHIFTS = range(1, 11)
WORD_MASK = (1 << LENGTH) - 1
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
REPRESENTATIVES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)
TAU_SIGNATURE = (1 << (4 - 1)) | (1 << (10 - 1))


class State(NamedTuple):
    s: G
    h: G
    x: G
    y: G
    kind: str


class TypeEntry(NamedTuple):
    b_word: int
    b_opposite: int
    required_signature: int
    theta: tuple[int, ...]
    labeled: int
    orbits: int


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


def divide_by_two(value: G) -> G:
    assert value[0] % 2 == value[1] % 2 == 0
    return value[0] // 2, value[1] // 2


def div_one_plus_i(value: G) -> G:
    real, imag = value
    assert (real + imag) % 2 == 0
    assert (imag - real) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def mod_one_plus_i(value: G) -> int:
    return (value[0] + value[1]) & 1


def norm(value: G) -> int:
    return value[0] ** 2 + value[1] ** 2


def axis(root: G) -> int:
    assert norm(root) == 1
    return int(root[0] == 0)


def local_states() -> tuple[State, ...]:
    result = []
    for x, y in product(ROOTS, repeat=2):
        s = div_one_plus_i(subtract(x, y))
        h = div_one_plus_i(add(x, y))
        dot = x[0] * y[0] + x[1] * y[1]
        kind = "equal" if dot == 1 else "opposite" if dot == -1 else "quarter"
        result.append(State(s, h, x, y, kind))
    assert len(result) == len({(state.s, state.h) for state in result}) == 16
    return tuple(result)


def cross_term(center: G, plus: G, minus: G) -> G:
    return add(
        multiply(center, conjugate(plus)),
        multiply(minus, conjugate(center)),
    )


def verify_local_residues(states: tuple[State, ...]) -> tuple[State, ...]:
    oriented = tuple(
        state
        for state in states
        if state.kind == "quarter" and state.s[0] == 0 and state.h[1] == 0
    )
    assert len(oriented) == 4
    for center in oriented:
        for kind, component in (("opposite", "s"), ("equal", "h")):
            active = [state for state in states if state.kind == kind]
            residues = {
                mod_one_plus_i(
                    divide_by_two(
                        cross_term(
                            getattr(center, component),
                            getattr(plus, component),
                            getattr(minus, component),
                        )
                    )
                )
                for plus, minus in product(active, repeat=2)
            }
            assert residues == {0, 1}
            inactive = "h" if component == "s" else "s"
            assert all(
                cross_term(
                    getattr(center, inactive),
                    getattr(plus, inactive),
                    getattr(minus, inactive),
                )
                == (0, 0)
                for plus, minus in product(active, repeat=2)
            )
            assert all(
                mod_one_plus_i(
                    divide_by_two(
                        multiply(
                            getattr(left, component),
                            conjugate(getattr(right, component)),
                        )
                    )
                )
                == 1
                for left, right in product(active, repeat=2)
            )
    return oriented


def rotate(word: int, shift: int) -> int:
    return ((word >> shift) | (word << (LENGTH - shift))) & WORD_MASK


def autocorrelation_signature(word: int) -> int:
    return sum(
        ((word & rotate(word, shift)).bit_count() & 1) << (shift - 1)
        for shift in HALF_SHIFTS
    )


def symmetric_b_word(bits: int) -> int:
    word = 0
    for shift in HALF_SHIFTS:
        if (bits >> (shift - 1)) & 1:
            word |= (1 << shift) | (1 << (LENGTH - shift))
    return word


def enumerate_a_counts() -> tuple[Counter[tuple[int, int]], dict[tuple[int, int], int]]:
    labeled: Counter[tuple[int, int]] = Counter()
    for word in range(1 << LENGTH):
        labeled[(word.bit_count(), autocorrelation_signature(word))] += 1

    burnside_sums: Counter[tuple[int, int]] = labeled.copy()
    for shift in range(1, LENGTH):
        period = gcd(LENGTH, shift)
        for base in range(1 << period):
            word = sum(
                1 << position
                for position in range(LENGTH)
                if (base >> (position % period)) & 1
            )
            labeled_key = (word.bit_count(), autocorrelation_signature(word))
            burnside_sums[labeled_key] += 1

    orbits = {}
    for key, count in labeled.items():
        assert burnside_sums[key] % LENGTH == 0
        orbits[key] = burnside_sums[key] // LENGTH
    assert sum(labeled.values()) == 1 << LENGTH
    return labeled, orbits


def classify_types(
    labeled: Counter[tuple[int, int]], orbits: dict[tuple[int, int], int]
) -> list[TypeEntry]:
    result = []
    for bits in range(1 << 10):
        b_word = symmetric_b_word(bits)
        f_word = ((~b_word) & WORD_MASK) & ~1
        b_signature = autocorrelation_signature(b_word)
        f_signature = autocorrelation_signature(f_word)
        required = 0
        theta = []
        for shift in HALF_SHIFTS:
            bit = shift - 1
            tau = (TAU_SIGNATURE >> bit) & 1
            b_corr = (b_signature >> bit) & 1
            f_corr = (f_signature >> bit) & 1
            a_corr = f_corr if (b_word >> shift) & 1 else tau ^ b_corr
            required |= a_corr << bit
            theta.append(1 ^ tau ^ b_corr ^ f_corr)
        key = (LENGTH - b_word.bit_count(), required)
        count = labeled[key]
        if count:
            result.append(
                TypeEntry(
                    b_word,
                    b_word.bit_count(),
                    required,
                    tuple(theta),
                    count,
                    orbits[key],
                )
            )
    return result


def root_sum_feasible(count: int, target: G) -> bool:
    return (
        abs(target[0]) + abs(target[1]) <= count
        and (target[0] + target[1] - count) % 2 == 0
    )


def pair_sum_domain(theta: int) -> set[G]:
    return {
        add(left, right)
        for left, right in product(ROOTS, repeat=2)
        if axis(left) ^ axis(right) == theta
    }


def accumulated_pair_sums(theta_values: list[int]) -> set[G]:
    result = {(0, 0)}
    for theta in theta_values:
        result = {
            add(partial, pair_sum)
            for partial in result
            for pair_sum in pair_sum_domain(theta)
        }
    return result


def orientation_label(state: State) -> str:
    names = {(1, 0): "1", (0, 1): "i", (-1, 0): "-1", (0, -1): "-i"}
    return f"({names[state.x]},{names[state.y]})"


def classify_cases(
    entries: list[TypeEntry], oriented: tuple[State, ...]
) -> tuple[list[dict[str, int]], list[dict[str, int | str]]]:
    summaries = [defaultdict(int) for _ in REPRESENTATIVES]
    orientations = [defaultdict(lambda: defaultdict(int)) for _ in REPRESENTATIVES]
    for entry in entries:
        s_pair_sums = accumulated_pair_sums(
            [
                entry.theta[shift - 1]
                for shift in HALF_SHIFTS
                if (entry.b_word >> shift) & 1
            ]
        )
        h_pair_sums = accumulated_pair_sums(
            [
                entry.theta[shift - 1]
                for shift in HALF_SHIFTS
                if not ((entry.b_word >> shift) & 1)
            ]
        )
        for case, (p, q, x, y) in enumerate(REPRESENTATIVES):
            sum_s_a = (p + q, q - p)
            sum_s_b = (x + y - 1, y - x)
            if not root_sum_feasible(
                LENGTH - entry.b_opposite, div_one_plus_i(sum_s_a)
            ):
                continue
            if not root_sum_feasible(entry.b_opposite, (0, 0)):
                continue
            allowed = []
            for center in oriented:
                target_s_b = div_one_plus_i(subtract(sum_s_b, center.s))
                target_h_b = div_one_plus_i(subtract((1, 0), center.h))
                if target_s_b in s_pair_sums and target_h_b in h_pair_sums:
                    allowed.append(center)
            assert len(allowed) in (0, 1)
            if not allowed:
                continue
            center = allowed[0]
            summaries[case]["b_masks"] += 1
            summaries[case]["labeled"] += entry.labeled
            summaries[case]["orbits"] += entry.orbits
            label = orientation_label(center)
            orientations[case][label]["b_masks"] += 1
            orientations[case][label]["labeled"] += entry.labeled
            orientations[case][label]["orbits"] += entry.orbits

    flat_orientations = []
    by_label = {orientation_label(state): state for state in oriented}
    for case, groups in enumerate(orientations):
        for label, counts in groups.items():
            state = by_label[label]
            flat_orientations.append(
                {
                    "case": case,
                    "original_pair": label,
                    "s_center": {"(0, -1)": "-i", "(0, 1)": "i"}[str(state.s)],
                    "h_center": {"(1, 0)": "1", "(-1, 0)": "-1"}[str(state.h)],
                    **counts,
                }
            )
    return [dict(summary) for summary in summaries], flat_orientations


def read_tsv(name: str) -> list[dict[str, str]]:
    with (Path(__file__).parent / name).open(encoding="utf-8", newline="") as handle:
        return list(DictReader(handle, delimiter="\t"))


def main() -> None:
    states = local_states()
    oriented = verify_local_residues(states)
    labeled, orbits = enumerate_a_counts()

    labeled_by_weight = Counter()
    orbits_by_weight = Counter()
    for (weight, _signature), count in labeled.items():
        labeled_by_weight[weight] += count
    for (weight, _signature), count in orbits.items():
        orbits_by_weight[weight] += count
    baseline_labeled = sum(
        comb(10, pairs) * labeled_by_weight[LENGTH - 2 * pairs]
        for pairs in range(11)
    )
    baseline_orbits = sum(
        comb(10, pairs) * orbits_by_weight[LENGTH - 2 * pairs]
        for pairs in range(11)
    )
    assert (baseline_labeled, baseline_orbits) == (215_008_364, 10_239_544)

    entries = classify_types(labeled, orbits)
    assert len(entries) == 480
    assert sum(entry.labeled for entry in entries) == 194_439
    assert sum(entry.orbits for entry in entries) == 9_259

    weight_rows = []
    weight_counts = defaultdict(lambda: [0, 0, 0])
    for entry in entries:
        aggregate = weight_counts[entry.b_opposite]
        aggregate[0] += 1
        aggregate[1] += entry.labeled
        aggregate[2] += entry.orbits
    for weight, (b_masks, raw_count, orbit_count) in sorted(weight_counts.items()):
        weight_rows.append(
            {
                "b_opposite": str(weight),
                "b_masks": str(b_masks),
                "labeled_type_pairs": str(raw_count),
                "a_rotation_orbits": str(orbit_count),
            }
        )
    assert weight_rows == read_tsv("weight_table.tsv")
    assert set(weight_counts) == set(range(4, 21, 2))

    case_summaries, orientation_rows = classify_cases(entries, oriented)
    case_rows = []
    for case, summary in enumerate(case_summaries):
        case_rows.append(
            {
                "case": str(case),
                "representative": "(" + ",".join(map(str, REPRESENTATIVES[case])) + ")",
                "b_masks": str(summary["b_masks"]),
                "labeled_type_pairs": str(summary["labeled"]),
                "a_rotation_orbits": str(summary["orbits"]),
            }
        )
    assert case_rows == read_tsv("case_table.tsv")
    normalized_orientation_rows = [
        {
            "case": str(row["case"]),
            "original_pair": str(row["original_pair"]),
            "s_center": str(row["s_center"]),
            "h_center": str(row["h_center"]),
            "b_masks": str(row["b_masks"]),
            "labeled_type_pairs": str(row["labeled"]),
            "a_rotation_orbits": str(row["orbits"]),
        }
        for row in orientation_rows
    ]
    assert normalized_orientation_rows == read_tsv("orientation_table.tsv")

    output = [
        "local_states=16",
        "divided_cross_residues=verified",
        f"baseline_reflected_type_pairs={baseline_labeled}",
        f"baseline_a_rotation_orbits={baseline_orbits}",
        f"third_order_b_masks={len(entries)}",
        f"third_order_labeled_type_pairs={sum(entry.labeled for entry in entries)}",
        f"third_order_a_rotation_orbits={sum(entry.orbits for entry in entries)}",
    ]
    output.extend(
        f"case={case};b_masks={summary['b_masks']};"
        f"labeled={summary['labeled']};orbits={summary['orbits']}"
        for case, summary in enumerate(case_summaries)
    )
    output.extend(("unique_exceptional_orientation=verified", "certificate=verified"))
    expected_output = (Path(__file__).parent / "verification_output.txt").read_text(
        encoding="utf-8"
    )
    assert expected_output == "\n".join(output) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
