#!/usr/bin/env python3
"""Direct audits for the odd-length exact-sum parity law and its boundary."""

from __future__ import annotations


EXPECTED = {
    3: (44, 44, 0),
    5: (352, 192, 160),
    7: (2368, 884, 1484),
    9: (14336, 5516, 8820),
    11: (80896, 23212, 57684),
}


def d_columns(b: int, n: int) -> tuple[int, ...]:
    dim = (n - 1) // 2
    columns = []
    for index in range(n):
        column = 0
        for shift in range(1, dim + 1):
            plus = (index + shift) % n
            minus = (index - shift) % n
            column |= (((b >> plus) ^ (b >> minus)) & 1) << (shift - 1)
        columns.append(column)
    return tuple(columns)


def syndrome(columns: tuple[int, ...], signs: int) -> int:
    result = 0
    for index, column in enumerate(columns):
        if (signs >> index) & 1:
            result ^= column
    return result


def image(columns: tuple[int, ...]) -> set[int]:
    result = {0}
    for column in columns:
        result |= {value ^ column for value in tuple(result)}
    return result


def exact_target(b: int, signs: int, n: int) -> tuple[int, int]:
    full = (1 << n) - 1
    weight = b.bit_count()
    negative_real = (signs & (full ^ b)).bit_count()
    negative_imaginary = (signs & b).bit_count()
    return n - weight - 2 * negative_real, weight - 2 * negative_imaginary


def parity_rhs(n: int, weight: int, target: tuple[int, int]) -> int:
    x, y = target
    negative_total = (n - x - y) // 2
    negative_imaginary = (weight - y) // 2
    return ((weight & 1) * negative_total + negative_imaginary) & 1


def verify_length(n: int) -> tuple[int, int, int]:
    target_fibers = 0
    equal_slices = 0
    failures = 0
    for b in range(1 << n):
        weight = b.bit_count()
        columns = d_columns(b, n)
        syndromes = image(columns)
        supports: dict[tuple[int, int], set[int]] = {}
        for signs in range(1 << n):
            target = exact_target(b, signs, n)
            value = syndrome(columns, signs)
            rhs = parity_rhs(n, weight, target)
            assert value.bit_count() & 1 == rhs
            supports.setdefault(target, set()).add(value)
        for target, support in supports.items():
            rhs = parity_rhs(n, weight, target)
            expected_slice = {
                value for value in syndromes if value.bit_count() & 1 == rhs
            }
            target_fibers += 1
            if support == expected_slice:
                equal_slices += 1
            else:
                failures += 1
    result = target_fibers, equal_slices, failures
    assert result == EXPECTED[n]
    return result


def verify_minimal_counterexample() -> None:
    n = 5
    b = 0b00001
    target = (4, 1)
    columns = d_columns(b, n)
    support = {
        syndrome(columns, signs)
        for signs in range(1 << n)
        if exact_target(b, signs, n) == target
    }
    syndromes = image(columns)
    rhs = parity_rhs(n, b.bit_count(), target)
    expected_slice = {value for value in syndromes if value.bit_count() & 1 == rhs}
    assert support == {0b00}
    assert expected_slice == {0b00, 0b11}
    print("minimal_full_slice_failure_n=5")
    print("counterexample_axis_word=00001")
    print("counterexample_target=4+1i")
    print("counterexample_support=00")
    print("counterexample_parity_slice=00,11")


def main() -> None:
    assignments = 0
    for n in EXPECTED:
        target_fibers, equal_slices, failures = verify_length(n)
        assignments += 1 << (2 * n)
        print(
            f"n={n} target_fibers={target_fibers} "
            f"equal_slices={equal_slices} failing_slices={failures}"
        )
    assert EXPECTED[3][2] == 0 and EXPECTED[5][2] > 0
    verify_minimal_counterexample()
    print(f"axis_sign_assignments_checked={assignments}")
    print("general_exact_target_parity_law=verified")
    print("certificate=verified")


if __name__ == "__main__":
    main()
