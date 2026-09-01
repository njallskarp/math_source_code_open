#!/usr/bin/env python3
"""Exact fourth-order Gaussian lift filter for the QLP-42 q=1, b=16 row."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from random import Random

G = tuple[int, int]
N = 21
PI = (1, 1)
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
DEPENDENCY_SHA256 = "109e66dec98a02afef5ed017ca5d579dd18daca5ebd5765de43f647cd41bc5ab"


@dataclass(frozen=True)
class LiftResult:
    b_index: int
    a_word: int
    b_word: int
    rank: int
    soluble: bool


def add(left: G, right: G) -> G:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: G, right: G) -> G:
    return left[0] - right[0], left[1] - right[1]


def scale(value: G, coefficient: int) -> G:
    return value[0] * coefficient, value[1] * coefficient


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
    assert (imag - real) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def pi3_bit(value: G) -> int:
    for _ in range(3):
        value = div_pi(value)
    return (value[0] + value[1]) & 1


def unit(axis: int, sign: int) -> G:
    value = (1, 0) if axis == 0 else (0, 1)
    return scale(value, -1 if sign else 1)


def paf(word: list[G], shift: int) -> G:
    result = (0, 0)
    for index, value in enumerate(word):
        result = add(
            result,
            multiply(value, conjugate(word[(index + shift) % len(word)])),
        )
    return result


def target_s(shift: int) -> G:
    if shift == 4:
        return -2, 0
    if shift == 10:
        return 2, 0
    return 0, 0


def load_dependency():
    path = Path(__file__).parent.parent / "qlp42_q1_b16_compression" / "verify_b16_mod7.py"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == DEPENDENCY_SHA256
    spec = importlib.util.spec_from_file_location("b16_mod7_dependency", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def mod7_survivors(module) -> list[tuple[int, int, int]]:
    classified, patterns, orbit_total = module.classify()
    assert orbit_total == 75
    domains = {count: module.root_sum_domain(count) for count in range(4)}
    a_cache = {
        counts: module.enumerate_a_fingerprints(counts, domains)[2]
        for counts in {pattern[0] for pattern in patterns}
    }
    feasible_patterns = set()
    for pattern in patterns:
        targets = {
            module.complement_target(module.fingerprint(word))
            for word in module.enumerate_b_words(pattern, domains)
        }
        if targets & a_cache[pattern[0]]:
            feasible_patterns.add(pattern)
    assert len(feasible_patterns) == 24

    records = []
    for b_index, (b_word, a_words, pair_patterns) in enumerate(classified):
        for a_word, pattern in zip(a_words, pair_patterns, strict=True):
            if pattern in feasible_patterns:
                records.append((b_index, a_word, b_word))
    assert len(records) == 756
    assert len({b_index for b_index, _, _ in records}) == 18
    assert len(
        {
            (b_index, module.orbit_representative(a_word))
            for b_index, a_word, _ in records
        }
    ) == 36
    return records


def theta_values(module, b_word: int) -> tuple[int, ...]:
    full = (1 << N) - 1
    f_word = ((~b_word) & full) & ~1
    b_signature = module.correlation_signature(b_word)
    f_signature = module.correlation_signature(f_word)
    return tuple(
        1
        ^ int(shift in (4, 10))
        ^ ((b_signature >> (shift - 1)) & 1)
        ^ ((f_signature >> (shift - 1)) & 1)
        for shift in range(1, 11)
    )


def build_words(
    module, a_word: int, b_word: int, variables: list[int] | None = None
) -> tuple[list[G], list[G], list[G], list[G]]:
    # Variables: 21 A axes; 10 common B-pair axes; 20 B signs; 2 center signs.
    values = variables if variables is not None else [0] * 53
    assert len(values) == 53 and set(values) <= {0, 1}
    s_a = [(0, 0)] * N
    h_a = [(0, 0)] * N
    s_b = [(0, 0)] * N
    h_b = [(0, 0)] * N

    for index in range(N):
        active = multiply(PI, unit(values[index], 0))
        (s_a if (a_word >> index) & 1 else h_a)[index] = active

    theta = theta_values(module, b_word)
    for shift in range(1, 11):
        common_axis = values[20 + shift]
        plus = multiply(PI, unit(common_axis, values[30 + shift]))
        minus = multiply(
            PI,
            unit(common_axis ^ theta[shift - 1], values[40 + shift]),
        )
        component = s_b if (b_word >> shift) & 1 else h_b
        component[shift] = plus
        component[N - shift] = minus

    s_b[0] = scale((0, -1), -1 if values[51] else 1)
    h_b[0] = scale((1, 0), -1 if values[52] else 1)
    return s_a, h_a, s_b, h_b


def residual_vector(
    module, a_word: int, b_word: int, variables: list[int] | None = None
) -> int:
    s_a, h_a, s_b, h_b = build_words(module, a_word, b_word, variables)
    result = 0
    for component, (left, right) in enumerate(((s_a, s_b), (h_a, h_b))):
        for shift in range(1, 11):
            target = target_s(shift) if component == 0 else (-2, 0)
            residual = subtract(add(paf(left, shift), paf(right, shift)), target)
            result |= pi3_bit(residual) << (10 * component + shift - 1)
    return result


def row_basis(columns: list[int]) -> dict[int, int]:
    basis: dict[int, int] = {}
    for value in columns:
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return basis


def in_span(value: int, basis: dict[int, int]) -> bool:
    while value:
        pivot = value.bit_length() - 1
        if pivot not in basis:
            return False
        value ^= basis[pivot]
    return True


def verify_local_affinity() -> int:
    checks = 0
    # A diagonal product is 2*u*conj(v); modulo pi^4 its fourth-order
    # variation is affine in the two axes and independent of both signs.
    diagonal_values = {}
    baseline = scale(multiply(unit(0, 0), conjugate(unit(0, 0))), 2)
    for left_axis in (0, 1):
        for right_axis in (0, 1):
            for left_sign in (0, 1):
                for right_sign in (0, 1):
                    value = scale(
                        multiply(
                            unit(left_axis, left_sign),
                            conjugate(unit(right_axis, right_sign)),
                        ),
                        2,
                    )
                    diagonal_values[(left_axis, right_axis, left_sign, right_sign)] = pi3_bit(
                        subtract(value, baseline)
                    )
                    checks += 1
    singles = [
        diagonal_values[tuple(int(index == bit) for index in range(4))]
        for bit in range(4)
    ]
    for assignment, value in diagonal_values.items():
        assert value == sum(
            single for single, enabled in zip(singles, assignment, strict=True) if enabled
        ) % 2

    # Each center-cross pair has fixed reflected-axis XOR theta. Exhaust all
    # common-axis, two neighbor-sign, and center-sign variables.
    for center_axis in (0, 1):
        for theta in (0, 1):
            values = {}
            for common_axis in (0, 1):
                for plus_sign in (0, 1):
                    for minus_sign in (0, 1):
                        for center_sign in (0, 1):
                            center = unit(center_axis, center_sign)
                            plus = multiply(PI, unit(common_axis, plus_sign))
                            minus = multiply(PI, unit(common_axis ^ theta, minus_sign))
                            cross = add(
                                multiply(center, conjugate(plus)),
                                multiply(minus, conjugate(center)),
                            )
                            assignment = (
                                common_axis,
                                plus_sign,
                                minus_sign,
                                center_sign,
                            )
                            values[assignment] = cross
                            checks += 1
            base = values[(0, 0, 0, 0)]
            bits = {
                assignment: pi3_bit(subtract(value, base))
                for assignment, value in values.items()
            }
            singles = [
                bits[tuple(int(index == bit) for index in range(4))]
                for bit in range(4)
            ]
            for assignment, value in bits.items():
                assert value == sum(
                    single
                    for single, enabled in zip(singles, assignment, strict=True)
                    if enabled
                ) % 2
    assert checks == 80
    return checks


def classify_lifts(module, records: list[tuple[int, int, int]]) -> tuple[list[LiftResult], int]:
    rng = Random(0xB16_4004)
    results = []
    direct_checks = 0
    for b_index, a_word, b_word in records:
        base = residual_vector(module, a_word, b_word)
        columns = []
        for variable in range(53):
            assignment = [0] * 53
            assignment[variable] = 1
            columns.append(residual_vector(module, a_word, b_word, assignment) ^ base)
        basis = row_basis(columns)
        soluble = in_span(base, basis)
        results.append(LiftResult(b_index, a_word, b_word, len(basis), soluble))

        assignment = [rng.randrange(2) for _ in range(53)]
        predicted = base
        for column, enabled in zip(columns, assignment, strict=True):
            if enabled:
                predicted ^= column
        assert residual_vector(module, a_word, b_word, assignment) == predicted
        direct_checks += 1
    return results, direct_checks


def positions(word: int) -> str:
    return ",".join(str(index) for index in range(N) if (word >> index) & 1)


def orbit_rows(module, results: list[LiftResult]) -> list[tuple[str, str, int, int]]:
    grouped: dict[tuple[int, tuple[int, ...]], list[LiftResult]] = {}
    for result in results:
        key = (result.b_index, module.orbit_representative(result.a_word))
        grouped.setdefault(key, []).append(result)
    rows = []
    for group in grouped.values():
        assert len(group) == 21
        assert len({(item.rank, item.soluble, item.b_word) for item in group}) == 1
        item = group[0]
        equal_positions = tuple(
            index for index in range(1, N) if not (item.b_word >> index) & 1
        )
        representative = module.orbit_representative(item.a_word)
        rows.append(
            (
                ",".join(map(str, equal_positions)),
                ",".join(map(str, representative)),
                item.rank,
                int(item.soluble),
            )
        )
    return sorted(rows)


def main() -> None:
    module = load_dependency()
    local_checks = verify_local_affinity()
    records = mod7_survivors(module)
    results, direct_checks = classify_lifts(module, records)
    rows = orbit_rows(module, results)

    labeled = Counter((result.rank, result.soluble) for result in results)
    orbits = Counter((rank, bool(soluble)) for _, _, rank, soluble in rows)
    assert labeled == {
        (18, True): 147,
        (19, True): 105,
        (19, False): 84,
        (20, True): 420,
    }
    assert orbits == {
        (18, True): 7,
        (19, True): 5,
        (19, False): 4,
        (20, True): 20,
    }
    surviving_b_masks = len({result.b_index for result in results if result.soluble})

    if "--dump-orbits" in sys.argv:
        print("b_equal_positions\ta_opposite_orbit_representative\trank\tsoluble")
        for row in rows:
            print(*row, sep="\t")
        return

    output = [
        f"dependency_sha256={DEPENDENCY_SHA256}",
        f"local_affinity_checks={local_checks}",
        f"direct_affine_checks={direct_checks}",
        f"mod7_surviving_b_masks={len({item[0] for item in records})}",
        f"mod7_surviving_labeled_pairs={len(records)}",
        f"mod7_surviving_a_rotation_orbits={len(rows)}",
        f"rank18_solvable_labeled={labeled[(18, True)]}",
        f"rank18_solvable_orbits={orbits[(18, True)]}",
        f"rank19_solvable_labeled={labeled[(19, True)]}",
        f"rank19_solvable_orbits={orbits[(19, True)]}",
        f"rank19_inconsistent_labeled={labeled[(19, False)]}",
        f"rank19_inconsistent_orbits={orbits[(19, False)]}",
        f"rank20_solvable_labeled={labeled[(20, True)]}",
        f"rank20_solvable_orbits={orbits[(20, True)]}",
        f"fourth_order_surviving_b_masks={surviving_b_masks}",
        f"fourth_order_surviving_labeled_pairs={sum(result.soluble for result in results)}",
        f"fourth_order_surviving_a_rotation_orbits={sum(soluble for *_, soluble in rows)}",
        "global_remaining_labeled_pairs=193473",
        "global_remaining_a_rotation_orbits=9213",
        "certificate=verified",
    ]
    expected = (Path(__file__).parent / "verification_output.txt").read_text(
        encoding="utf-8"
    )
    assert expected == "\n".join(output) + "\n"
    table = (Path(__file__).parent / "orbit_table.tsv").read_text(encoding="utf-8")
    generated = ["b_equal_positions\ta_opposite_orbit_representative\trank\tsoluble"]
    generated.extend("\t".join(map(str, row)) for row in rows)
    assert table == "\n".join(generated) + "\n"
    print(*output, sep="\n")


if __name__ == "__main__":
    main()
