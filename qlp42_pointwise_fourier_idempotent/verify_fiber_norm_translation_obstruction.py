#!/usr/bin/env python3
"""Verify the translation obstruction to compressed QLP fiber norms."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

Gaussian = tuple[int, int]
State = tuple[int, int, int, int, int, int]

MU4: tuple[Gaussian, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def multiply_conjugate(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] + left[1] * right[1],
        left[1] * right[0] - left[0] * right[1],
    )


def divide_by_one_plus_i(value: Gaussian) -> Gaussian:
    real, imag = value
    assert (real + imag) % 2 == 0
    assert (imag - real) % 2 == 0
    return (real + imag) // 2, (imag - real) // 2


def local_states() -> tuple[State, ...]:
    result = []
    for x_value in MU4:
        for y_value in MU4:
            s_value = divide_by_one_plus_i(subtract(x_value, y_value))
            h_value = divide_by_one_plus_i(add(x_value, y_value))
            cross = multiply_conjugate(s_value, h_value)
            assert cross[0] == 0 and cross[1] in (-1, 0, 1)
            result.append((*s_value, *h_value, abs(cross[1]), cross[1]))
    assert len(result) == len(set(result)) == 16
    return tuple(result)


STATES = local_states()


def rotate_right(word: tuple[int, ...]) -> tuple[int, ...]:
    return word[-1:] + word[:-1]


def periodic_norm(values: tuple[Gaussian, ...]) -> tuple[Gaussian, ...]:
    length = len(values)
    return tuple(
        (
            sum(
                multiply_conjugate(values[index], values[(index + shift) % length])[0]
                for index in range(length)
            ),
            sum(
                multiply_conjugate(values[index], values[(index + shift) % length])[1]
                for index in range(length)
            ),
        )
        for shift in range(length)
    )


def projection(word: tuple[int, ...], offset: int) -> tuple[Gaussian, ...]:
    return tuple(STATES[label][offset : offset + 2] for label in word)


def lift(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(label for label in word for _ in range(3))


def primitive_fiber_condition(first: tuple[int, ...], second: tuple[int, ...]) -> bool:
    for label in range(16):
        for row in range(7):
            differences = {
                int(second[3 * row + column] == label)
                - int(first[3 * row + column] == label)
                for column in range(3)
            }
            if len(differences) != 1:
                return False
    return True


def main() -> None:
    certificate_path = Path(__file__).with_name(
        "fiber_norm_translation_certificate.json"
    )
    raw = certificate_path.read_bytes()
    certificate = json.loads(raw)
    assert certificate["schema"] == "qlp42-fiber-norm-translation-obstruction-v1"

    quarter = tuple(index for index, state in enumerate(STATES) if state[4] == 1)
    nonquarter = tuple(index for index, state in enumerate(STATES) if state[4] == 0)
    assert len(quarter) == len(nonquarter) == 8

    checked = 0
    for exceptional_class, background_class in (
        (quarter, nonquarter),
        (nonquarter, quarter),
    ):
        for exceptional in exceptional_class:
            for background in background_class:
                first = (exceptional,) + (background,) * 6
                second = (background, exceptional) + (background,) * 5
                assert second == rotate_right(first)
                assert Counter(first) == Counter(second)

                for offset in (0, 2):
                    assert periodic_norm(projection(first, offset)) == periodic_norm(
                        projection(second, offset)
                    )

                first_lift = lift(first)
                second_lift = lift(second)
                assert primitive_fiber_condition(first_lift, second_lift)
                support_difference = sum(
                    STATES[left][4] != STATES[right][4]
                    for left, right in zip(first_lift, second_lift, strict=True)
                )
                assert support_difference == 6
                checked += 1

    assert checked == certificate["verified_ordered_cross_class_pairs"] == 128
    assert certificate["expected_support_symmetric_difference_after_lift"] == 6
    digest = hashlib.sha256(raw).hexdigest()

    print("compressed_group=C7")
    print("fiber_group=C3")
    print("ordered_cross_class_pairs=128")
    print("compressed_norm_projections_per_pair=2")
    print("primitive_indicator_fiber_condition=verified")
    print("support_symmetric_difference=6")
    print("universal_fiber_norm_detector=disproved")
    print("canonical_qlp_witness_claim=false")
    print(f"fiber_norm_translation_certificate_sha256={digest}")
    print("translation_obstruction=verified")


if __name__ == "__main__":
    main()
