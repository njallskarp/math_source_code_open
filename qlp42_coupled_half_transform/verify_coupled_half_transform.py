#!/usr/bin/env python3
"""Exact checks for the coupled half-sum/half-difference QLP-42 transform."""

from __future__ import annotations

from itertools import product

G = tuple[int, int]
ROOTS: tuple[G, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
REPRESENTATIVES = (
    (1, 0, 5, 0),
    (3, 0, 4, 1),
    (3, 0, 3, -2),
    (3, 2, 3, 2),
    (3, 2, 2, 3),
    (4, 1, 2, -1),
)


def add(a: G, b: G) -> G:
    return a[0] + b[0], a[1] + b[1]


def sub(a: G, b: G) -> G:
    return a[0] - b[0], a[1] - b[1]


def mul(a: G, b: G) -> G:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def conj(a: G) -> G:
    return a[0], -a[1]


def scale(k: int, a: G) -> G:
    return k * a[0], k * a[1]


def sum_g(values) -> G:
    result = (0, 0)
    for value in values:
        result = add(result, value)
    return result


def div_one_plus_i(a: G) -> G:
    assert (a[0] + a[1]) % 2 == 0 and (a[1] - a[0]) % 2 == 0
    return (a[0] + a[1]) // 2, (a[1] - a[0]) // 2


def paf(sequence: list[G]) -> list[G]:
    n = len(sequence)
    return [
        sum_g(
            mul(sequence[j], conj(sequence[(j + shift) % n]))
            for j in range(n)
        )
        for shift in range(n)
    ]


def transform(sequence: list[G]) -> tuple[list[G], list[G]]:
    n = len(sequence)
    assert n % 2 == 0 and (n // 2) % 2 == 1
    m = n // 2
    x = [sequence[((m + 1) * j) % n] for j in range(m)]
    y = [sequence[((m + 1) * j + m) % n] for j in range(m)]
    s = [div_one_plus_i(sub(a, b)) for a, b in zip(x, y)]
    h = [div_one_plus_i(add(a, b)) for a, b in zip(x, y)]
    return s, h


def main() -> None:
    # The local state map is a bijection from ordered fourth-root pairs to 16
    # coupled ternary states (S,H).
    state_to_pair: dict[tuple[G, G], tuple[G, G]] = {}
    for x, y in product(ROOTS, repeat=2):
        s = div_one_plus_i(sub(x, y))
        h = div_one_plus_i(add(x, y))
        assert all(coordinate in (-1, 0, 1) for z in (s, h) for coordinate in z)
        assert s[0] * s[0] + s[1] * s[1] + h[0] * h[0] + h[1] * h[1] == 2
        assert mul(s, conj(h))[0] == 0
        assert (s, h) not in state_to_pair
        state_to_pair[(s, h)] = (x, y)
    assert len(state_to_pair) == 16

    # Exhaustively check both autocorrelation identities for every fourth-root
    # word of length 6.  This tests all 4^6 words and all independent shifts.
    words_checked = 0
    for word in product(ROOTS, repeat=6):
        sequence = list(word)
        s, h = transform(sequence)
        p_sequence = paf(sequence)
        p_s = paf(s)
        p_h = paf(h)
        for shift in range(3):
            assert add(p_sequence[shift], p_sequence[shift + 3]) == scale(2, p_h[shift])
            assert sub(p_sequence[shift], p_sequence[shift + 3]) == scale(
                2 * ((-1) ** shift), p_s[shift]
            )
        words_checked += 1
    assert words_checked == 4**6

    # Derive the two length-21 targets for the canonical norm-32 residual.
    combined = [-2] * 42
    combined[0] = 84
    for shift in (4, 11, 31, 38):
        combined[shift] = -4
    for shift in (10, 17, 25, 32):
        combined[shift] = 0
    target_s = [
        ((-1) ** shift) * (combined[shift] - combined[shift + 21]) // 2
        for shift in range(21)
    ]
    target_h = [
        (combined[shift] + combined[shift + 21]) // 2
        for shift in range(21)
    ]
    assert target_s[0] == 43
    assert {
        shift: value for shift, value in enumerate(target_s) if shift and value
    } == {4: -2, 10: 2, 11: 2, 17: -2}
    assert target_h == [41] + [-2] * 20

    # The six canonical order-two compression cases fix the transformed sums.
    transformed_sums = []
    for p, q, x, y in REPRESENTATIVES:
        transformed_sums.append(
            {
                "sum_s_a": (p + q, q - p),
                "sum_h_a": (0, 0),
                "sum_s_b": (x + y - 1, y - x),
                "sum_h_b": (1, 0),
            }
        )
    assert len(set(tuple(item.values()) for item in transformed_sums)) == 6

    print(f"local_states={len(state_to_pair)}")
    print(f"length_6_words_checked={words_checked}")
    print("S_target_nonzero={0:43,4:-2,10:2,11:2,17:-2}")
    print("H_target={0:41,all_nonzero:-2}")
    print("canonical_sum_cases=6")
    print("certificate=verified")


if __name__ == "__main__":
    main()
