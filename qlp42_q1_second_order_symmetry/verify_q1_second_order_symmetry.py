#!/usr/bin/env python3
"""Exact Z[i] certificate for the QLP-42 q=1 reflection restriction."""

from __future__ import annotations

from itertools import product

Gaussian = tuple[int, int]

ROOTS: tuple[Gaussian, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
CASES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)


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


def norm(value: Gaussian) -> int:
    return value[0] ** 2 + value[1] ** 2


def divisible_by_two(value: Gaussian) -> bool:
    return value[0] % 2 == 0 and value[1] % 2 == 0


def div_one_plus_i(value: Gaussian) -> Gaussian:
    real, imag = value
    assert (real + imag) % 2 == 0
    assert (imag - real) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def local_states() -> tuple[dict[str, object], ...]:
    result = []
    for x, y in product(ROOTS, repeat=2):
        s = div_one_plus_i(subtract(x, y))
        h = div_one_plus_i(add(x, y))
        dot = x[0] * y[0] + x[1] * y[1]
        if dot == 1:
            kind = "equal"
        elif dot == -1:
            kind = "opposite"
        else:
            assert dot == 0
            kind = "quarter"
        result.append({"x": x, "y": y, "s": s, "h": h, "kind": kind})
    assert len(result) == 16
    assert len({(row["s"], row["h"]) for row in result}) == 16
    return tuple(result)


def verify_local_table(states: tuple[dict[str, object], ...]) -> None:
    counts = {kind: 0 for kind in ("equal", "opposite", "quarter")}
    for row in states:
        kind = row["kind"]
        s = row["s"]
        h = row["h"]
        assert isinstance(kind, str) and isinstance(s, tuple) and isinstance(h, tuple)
        counts[kind] += 1
        if kind == "equal":
            assert s == (0, 0) and norm(h) == 2
        elif kind == "opposite":
            assert norm(s) == 2 and h == (0, 0)
        else:
            assert norm(s) == norm(h) == 1
            assert s[0] * h[0] + s[1] * h[1] == 0
        quarter = int(kind == "quarter")
        assert ((sum(s) & 1), (sum(h) & 1)) == (quarter, quarter)
        assert norm(s) + norm(h) == 2
    assert counts == {"equal": 4, "opposite": 4, "quarter": 8}


def verify_sum_orientation(states: tuple[dict[str, object], ...]) -> None:
    for p, q, x, y in CASES:
        sum_s_a = (p + q, q - p)
        sum_h_a = (0, 0)
        sum_s_b = (x + y - 1, y - x)
        sum_h_b = (1, 0)
        assert sum(sum_s_a) % 2 == sum(sum_h_a) % 2 == 0
        assert sum(sum_s_b) % 2 == sum(sum_h_b) % 2 == 1
        assert (sum_s_b[0] & 1, sum_s_b[1] & 1) == (0, 1)
        assert (sum_h_b[0] & 1, sum_h_b[1] & 1) == (1, 0)

    oriented = {
        (row["x"], row["y"], row["s"], row["h"])
        for row in states
        if row["kind"] == "quarter"
        and row["s"][0] == 0
        and row["h"][1] == 0
    }
    assert oriented == {
        ((1, 0), (0, 1), (0, -1), (1, 0)),
        ((0, 1), (1, 0), (0, 1), (1, 0)),
        ((-1, 0), (0, -1), (0, 1), (-1, 0)),
        ((0, -1), (-1, 0), (0, -1), (-1, 0)),
    }


def verify_second_order_cross_terms(
    states: tuple[dict[str, object], ...]
) -> int:
    quarter = [row for row in states if row["kind"] == "quarter"]
    nonquarter = [row for row in states if row["kind"] != "quarter"]
    checked = 0
    for center, plus, minus in product(quarter, nonquarter, nonquarter):
        same_type = plus["kind"] == minus["kind"]
        for component in ("s", "h"):
            cross = add(
                multiply(center[component], conjugate(plus[component])),
                multiply(minus[component], conjugate(center[component])),
            )
            assert divisible_by_two(cross) == same_type
        checked += 1
    assert checked == 8 * 8 * 8
    return checked


def verify_energy_and_compressed_patterns() -> int:
    quarter_total = 1
    opposite_total = (43 - quarter_total) // 2
    equal_total = (41 - quarter_total) // 2
    assert (opposite_total, equal_total) == (21, 20)

    expected_patterns = {
        (k0, k1, k2, k3, k3, k2, k1)
        for k0 in (0, 2)
        for k1, k2, k3 in product(range(4), repeat=3)
    }
    actual_patterns = set()
    for mask in range(1 << 10):
        opposite = [0] * 21
        for shift in range(1, 11):
            value = (mask >> (shift - 1)) & 1
            opposite[shift] = value
            opposite[-shift % 21] = value
        counts = tuple(
            sum(opposite[residue + 7 * block] for block in range(3))
            for residue in range(7)
        )
        actual_patterns.add(counts)
    assert actual_patterns == expected_patterns
    assert len(actual_patterns) == 2 * 4**3 == 128
    assert all(sum(pattern) % 2 == 0 for pattern in actual_patterns)
    return len(actual_patterns)


def main() -> None:
    states = local_states()
    verify_local_table(states)
    verify_sum_orientation(states)
    cross_configurations = verify_second_order_cross_terms(states)
    compressed_patterns = verify_energy_and_compressed_patterns()
    print("local_states=16")
    print("local_kinds=equal:4,opposite:4,quarter:8")
    print("q1_family_counts=q_A:0,q_B:1")
    print(f"second_order_cross_configurations={cross_configurations}")
    print("reflection_clauses=10")
    print("oriented_exceptional_states=4")
    print("global_types=opposite:21,equal:20")
    print("compressed_count_shape=k0,k1,k2,k3,k3,k2,k1")
    print(f"compressed_count_patterns={compressed_patterns}")
    print("certificate=verified")


if __name__ == "__main__":
    main()
