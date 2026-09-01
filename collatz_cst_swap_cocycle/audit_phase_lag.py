"""Exact audit of the normalized phase-lag identity for Collatz swaps.

Unlike ``audit_swap_cocycle.py``, this checker ranges over *all* contracting
parity words, not only coefficient-first-crossing words.  This is needed to
test whether the hoped-for full-wrap/circle-winding inequality follows from
the adjacent-swap algebra alone.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass

from audit_swap_cocycle import (
    Cylinder,
    coefficient_gap_coordinates,
    cylinder_from_bits,
)


@dataclass(frozen=True)
class StrictDefect:
    """The first zero-index edge with more full wraps than circle wraps."""

    length: int
    source_bits: int
    target_bits: int
    position: int
    odd_count: int
    gap: int
    source_residue: int
    source_endpoint: int
    source_numerator: int
    source_mu: int
    source_kappa: int
    target_residue: int
    target_endpoint: int
    target_numerator: int
    target_mu: int
    target_kappa: int
    displacement: int
    numerator_drop: int
    jump: int
    full_wraps: int
    circle_wraps: int

    def chronological_word(self, bits: int) -> str:
        return "".join(str((bits >> position) & 1) for position in range(self.length))

    def as_record(self) -> str:
        return (
            f"K={self.length};source={self.chronological_word(self.source_bits)};"
            f"target={self.chronological_word(self.target_bits)};j={self.position};"
            f"q={self.odd_count};d={self.gap};"
            f"source_r={self.source_residue};source_z={self.source_endpoint};"
            f"source_B={self.source_numerator};source_mu={self.source_mu};"
            f"source_kappa={self.source_kappa};"
            f"target_r={self.target_residue};target_z={self.target_endpoint};"
            f"target_B={self.target_numerator};target_mu={self.target_mu};"
            f"target_kappa={self.target_kappa};delta={self.displacement};"
            f"E={self.numerator_drop};J={self.jump};W={self.full_wraps};"
            f"C={self.circle_wraps}"
        )


def contracting_states(length: int) -> dict[int, Cylinder]:
    """Return every length-``length`` word with ``3^q < 2^length``."""
    states: dict[int, Cylinder] = {}
    for bits in range(1 << length):
        state = cylinder_from_bits(bits, length)
        if state.pow3 < state.pow2:
            states[bits] = state
    return states


def audit(max_length: int = 18) -> dict[str, int | str]:
    if max_length < 2:
        raise ValueError("max_length must be at least two")

    digest = hashlib.sha256()
    contracting_words = 0
    adjacent_edges = 0
    phase_lag_failures = 0
    window_failures = 0
    full_less_circle = 0
    full_equal_circle = 0
    full_greater_circle = 0
    zero_index_source_edges = 0
    zero_index_source_equal = 0
    zero_index_source_strict = 0
    zero_index_source_antidominance_failures = 0
    maximum_window_index = 0
    first_strict: StrictDefect | None = None

    for length in range(2, max_length + 1):
        modulus = 1 << length
        states = contracting_states(length)
        contracting_words += len(states)
        coordinates = {
            bits: coefficient_gap_coordinates(state)
            for bits, state in states.items()
        }
        maximum_window_index = max(
            maximum_window_index,
            max(kappa for _, _, kappa in coordinates.values()),
        )

        for bits in sorted(states):
            source = states[bits]
            gap, source_mu, source_kappa = coordinates[bits]
            for position in range(length - 1):
                if ((bits >> position) & 3) != 2:
                    continue
                target_bits = bits ^ (3 << position)
                target = states[target_bits]
                _, target_mu, target_kappa = coordinates[target_bits]

                prefix_ones = (bits & ((1 << position) - 1)).bit_count()
                suffix_ones = (bits >> (position + 2)).bit_count()
                local_modulus = 1 << (length - position)
                inverse = pow(3 ** (prefix_ones + 1), -1, local_modulus)
                displacement = (1 << position) * inverse
                numerator_drop = (1 << position) * 3**suffix_ones
                jump_numerator = gap * inverse + 3**suffix_ones
                jump, remainder = divmod(jump_numerator, local_modulus)
                if remainder:
                    raise AssertionError("jump is not integral")

                # Edge and path versions of this identity are respectively
                #   A J = d Delta + (B-B')
                #   A S = d D + (B_0-B_m).
                # It is the exact normalized phase lag between the two wraps.
                if modulus * jump != gap * displacement + numerator_drop:
                    phase_lag_failures += 1
                if source.numerator - target.numerator != numerator_drop:
                    phase_lag_failures += 1
                if (
                    gap * (source.residue + displacement)
                    != modulus
                    * (source_mu + jump - gap * source_kappa)
                    + target.numerator
                ):
                    phase_lag_failures += 1

                full_wrap = (source.residue + displacement) // modulus
                circle_wrap = (source_mu + jump) // gap
                if full_wrap not in (0, 1):
                    raise AssertionError("a canonical residue increment wrapped twice")
                if target.residue != (
                    source.residue + displacement - modulus * full_wrap
                ):
                    phase_lag_failures += 1
                if target_mu != source_mu + jump - gap * circle_wrap:
                    phase_lag_failures += 1
                if target_kappa - source_kappa != full_wrap - circle_wrap:
                    window_failures += 1

                if full_wrap < circle_wrap:
                    full_less_circle += 1
                elif full_wrap == circle_wrap:
                    full_equal_circle += 1
                else:
                    full_greater_circle += 1

                if source_kappa == 0:
                    zero_index_source_edges += 1
                    if full_wrap < circle_wrap or target_kappa not in (0, 1):
                        zero_index_source_antidominance_failures += 1
                    if full_wrap == circle_wrap:
                        zero_index_source_equal += 1
                    elif full_wrap > circle_wrap:
                        zero_index_source_strict += 1
                        candidate = StrictDefect(
                            length=length,
                            source_bits=bits,
                            target_bits=target_bits,
                            position=position,
                            odd_count=source.odd_count,
                            gap=gap,
                            source_residue=source.residue,
                            source_endpoint=source.endpoint,
                            source_numerator=source.numerator,
                            source_mu=source_mu,
                            source_kappa=source_kappa,
                            target_residue=target.residue,
                            target_endpoint=target.endpoint,
                            target_numerator=target.numerator,
                            target_mu=target_mu,
                            target_kappa=target_kappa,
                            displacement=displacement,
                            numerator_drop=numerator_drop,
                            jump=jump,
                            full_wraps=full_wrap,
                            circle_wraps=circle_wrap,
                        )
                        if first_strict is None:
                            first_strict = candidate

                adjacent_edges += 1
                digest.update(
                    (
                        f"{length},{bits:x},{position},{source.residue},"
                        f"{target.residue},{source.numerator},{target.numerator},"
                        f"{source_mu},{target_mu},{source_kappa},{target_kappa},"
                        f"{displacement},{numerator_drop},{jump},"
                        f"{full_wrap},{circle_wrap}\n"
                    ).encode("ascii")
                )

    if first_strict is None:
        raise AssertionError("the unrestricted strict defect was not found")
    return {
        "max_length": max_length,
        "contracting_words": contracting_words,
        "adjacent_edges": adjacent_edges,
        "phase_lag_failures": phase_lag_failures,
        "window_failures": window_failures,
        "full_less_circle": full_less_circle,
        "full_equal_circle": full_equal_circle,
        "full_greater_circle": full_greater_circle,
        "zero_index_source_edges": zero_index_source_edges,
        "zero_index_source_equal": zero_index_source_equal,
        "zero_index_source_strict": zero_index_source_strict,
        "zero_index_source_antidominance_failures": (
            zero_index_source_antidominance_failures
        ),
        "maximum_window_index": maximum_window_index,
        "first_zero_index_source_strict_defect": first_strict.as_record(),
        "sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=18)
    args = parser.parse_args()
    for key, value in audit(args.max_length).items():
        print(f"{key}={value}")
    print("status=exact normalized phase-lag audit passed")


if __name__ == "__main__":
    main()
