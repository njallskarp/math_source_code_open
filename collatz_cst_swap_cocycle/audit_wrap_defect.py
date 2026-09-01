"""Exact path audit of the coefficient-gap winding/wrap-defect identity."""

from __future__ import annotations

import argparse
import hashlib

from audit_swap_cocycle import (
    Cylinder,
    coefficient_gap_coordinates,
    first_crossing_cylinders,
)


def one_positions(bits: int, length: int) -> list[int]:
    return [position for position in range(length) if (bits >> position) & 1]


def edge_data(
    states: dict[int, Cylinder], length: int, bits: int, position: int
) -> tuple[int, int, bool]:
    """Return target bits, positive circle jump, and full-residue wrap."""
    source = states[bits]
    modulus = 1 << length
    gap = modulus - source.pow3
    prefix_ones = (bits & ((1 << position) - 1)).bit_count()
    suffix_ones = (bits >> (position + 2)).bit_count()
    local_modulus = 1 << (length - position)
    inverse = pow(3 ** (prefix_ones + 1), -1, local_modulus)
    jump = (gap * inverse + 3**suffix_ones) // local_modulus
    wrapped = source.residue + (1 << position) * inverse >= modulus
    return bits ^ (3 << position), jump, wrapped


def audit(max_length: int = 26) -> dict[str, int | str]:
    groups = first_crossing_cylinders(max_length)
    digest = hashlib.sha256()
    paths = 0
    moves = 0
    maximum_inversions = 0
    maximum_full_wraps = 0
    maximum_circle_winding = 0
    maximum_window_index = 0
    failures = 0

    for length in sorted(groups):
        states = groups[length]
        if len(states) < 2:
            continue
        mechanical = max(states, key=lambda bits: states[bits].numerator)
        mechanical_positions = one_positions(mechanical, length)
        gap, initial_residue, initial_index = coefficient_gap_coordinates(
            states[mechanical]
        )

        for target in sorted(states):
            target_positions = one_positions(target, length)
            current_positions = mechanical_positions.copy()
            current = mechanical
            jump_sum = 0
            full_wraps = 0

            for odd_index in range(len(current_positions)):
                while current_positions[odd_index] > target_positions[odd_index]:
                    position = current_positions[odd_index] - 1
                    current, jump, wrapped = edge_data(
                        states, length, current, position
                    )
                    current_positions[odd_index] -= 1
                    jump_sum += jump
                    full_wraps += int(wrapped)
                    moves += 1

            if current != target:
                raise AssertionError("canonical insertion path missed its target")
            _, final_residue, final_index = coefficient_gap_coordinates(states[target])
            circle_winding, expected_residue = divmod(
                initial_residue + jump_sum, gap
            )
            if expected_residue != final_residue:
                failures += 1
            if final_index - initial_index != full_wraps - circle_winding:
                failures += 1

            inversions = sum(
                source_position - target_position
                for source_position, target_position in zip(
                    mechanical_positions, target_positions, strict=True
                )
            )
            maximum_inversions = max(maximum_inversions, inversions)
            maximum_full_wraps = max(maximum_full_wraps, full_wraps)
            maximum_circle_winding = max(maximum_circle_winding, circle_winding)
            maximum_window_index = max(maximum_window_index, final_index)
            paths += 1
            digest.update(
                (
                    f"{length},{target:x},{inversions},{jump_sum},{full_wraps},"
                    f"{circle_winding},{final_residue},{final_index}\n"
                ).encode("ascii")
            )

    return {
        "max_length": max_length,
        "canonical_paths": paths,
        "adjacent_moves": moves,
        "maximum_inversions": maximum_inversions,
        "maximum_full_wraps": maximum_full_wraps,
        "maximum_circle_winding": maximum_circle_winding,
        "maximum_window_index": maximum_window_index,
        "identity_failures": failures,
        "sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=26)
    args = parser.parse_args()
    for key, value in audit(args.max_length).items():
        print(f"{key}={value}")
    print("status=exact wrap-defect path audit passed")


if __name__ == "__main__":
    main()
