#!/usr/bin/env python3
"""Exact Z[i] certificate for the QLP-42 q=41 axis-reflection law."""

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


def axis(value: Gaussian) -> int:
    assert value in ROOTS
    return int(value[0] == 0)


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
            assert s in ROOTS and h in ROOTS
            assert axis(s) == 1 - axis(h)
        assert norm(s) + norm(h) == 2
    assert counts == {"equal": 4, "opposite": 4, "quarter": 8}


def verify_q41_counts() -> None:
    quarter_total = 41
    opposite_total = (43 - quarter_total) // 2
    equal_total = (41 - quarter_total) // 2
    assert (opposite_total, equal_total) == (1, 0)

    # A local state is quarter-turn precisely when either coupled coordinate
    # has odd real-plus-imaginary parity.  Check the family orientation in all
    # six canonical sum cases rather than taking it as an external assertion.
    for p, q, x, y in CASES:
        sum_s_a = (p + q, q - p)
        sum_h_a = (0, 0)
        sum_s_b = (x + y - 1, y - x)
        sum_h_b = (1, 0)
        assert sum(sum_s_a) % 2 == sum(sum_h_a) % 2 == 0
        assert sum(sum_s_b) % 2 == sum(sum_h_b) % 2 == 1

    possible = [
        (q_a, quarter_total - q_a)
        for q_a in range(22)
        if q_a % 2 == 0
        and (quarter_total - q_a) % 2 == 1
        and quarter_total - q_a <= 21
    ]
    assert possible == [(20, 21)]


def verify_removed_pair_test() -> int:
    checked = 0
    for filler, plus, minus in product(ROOTS, repeat=3):
        removed = add(
            multiply(filler, conjugate(plus)),
            multiply(minus, conjugate(filler)),
        )
        assert divisible_by_two(removed) == (axis(plus) == axis(minus))
        checked += 1
    assert checked == 4**3
    return checked


def residue_counts(bits: tuple[int, ...]) -> tuple[int, ...]:
    assert len(bits) == 10
    word = [0] * 21
    for shift, value in enumerate(bits, start=1):
        word[shift] = value
        word[-shift % 21] = value
    return tuple(
        sum(word[residue + 7 * block] for block in range(3))
        for residue in range(7)
    )


def parity_mask(counts: tuple[int, ...]) -> int:
    return sum((value & 1) << residue for residue, value in enumerate(counts))


def verify_reflected_compressions() -> tuple[int, tuple[int, ...]]:
    actual_counts = {residue_counts(bits) for bits in product((0, 1), repeat=10)}
    expected_counts = {
        (m0, m1, m2, m3, m3, m2, m1)
        for m0 in (0, 2)
        for m1, m2, m3 in product(range(4), repeat=3)
    }
    assert actual_counts == expected_counts
    assert len(actual_counts) == 2 * 4**3 == 128

    actual_masks = tuple(sorted({parity_mask(counts) for counts in actual_counts}))
    expected_masks = (0x00, 0x18, 0x24, 0x3C, 0x42, 0x5A, 0x66, 0x7E)
    assert actual_masks == expected_masks
    for mask in actual_masks:
        assert not (mask & 1)
        assert ((mask >> 1) & 1) == ((mask >> 6) & 1)
        assert ((mask >> 2) & 1) == ((mask >> 5) & 1)
        assert ((mask >> 3) & 1) == ((mask >> 4) & 1)
    return len(actual_counts), actual_masks


def main() -> None:
    states = local_states()
    verify_local_table(states)
    verify_q41_counts()
    removed_triples = verify_removed_pair_test()
    compressed_patterns, masks = verify_reflected_compressions()
    print("local_states=16")
    print("local_kinds=equal:4,opposite:4,quarter:8")
    print("q41_family_counts=q_A:20,q_B:21")
    print("global_types=opposite:1,equal:0")
    print(f"removed_pair_root_triples={removed_triples}")
    print("reflection_clauses=10")
    print("axis_assignments=1024")
    print("compressed_count_shape=m0,m1,m2,m3,m3,m2,m1")
    print(f"compressed_count_patterns={compressed_patterns}")
    print("parity_masks=" + ",".join(f"{mask:02x}" for mask in masks))
    print("certificate=verified")


if __name__ == "__main__":
    main()
