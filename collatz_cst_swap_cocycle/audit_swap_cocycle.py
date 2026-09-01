"""Exact audit of the adjacent-swap cocycle for CST parity cylinders."""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Cylinder:
    """Least nonnegative representative and endpoint of one parity cylinder."""

    length: int
    odd_count: int
    residue: int
    endpoint: int
    pow2: int
    pow3: int

    @staticmethod
    def empty() -> Cylinder:
        return Cylinder(0, 0, 0, 0, 1, 1)

    def extend(self, bit: int) -> Cylinder:
        if bit not in (0, 1):
            raise ValueError("bit must be 0 or 1")
        if bit == 0:
            lift = self.endpoint & 1
            intermediate = self.endpoint + self.pow3 * lift
            if intermediate & 1:
                raise AssertionError("even extension is incompatible")
            endpoint = intermediate // 2
            odd_count = self.odd_count
            pow3 = self.pow3
        else:
            lift = (1 - self.endpoint) & 1
            intermediate = self.endpoint + self.pow3 * lift
            if not intermediate & 1:
                raise AssertionError("odd extension is incompatible")
            endpoint = (3 * intermediate + 1) // 2
            odd_count = self.odd_count + 1
            pow3 = 3 * self.pow3
        return Cylinder(
            self.length + 1,
            odd_count,
            self.residue + self.pow2 * lift,
            endpoint,
            2 * self.pow2,
            pow3,
        )

    @property
    def numerator(self) -> int:
        """The B in T^K(x)=(3^q*x+B)/2^K."""
        return self.pow2 * self.endpoint - self.pow3 * self.residue

    @property
    def margin(self) -> int:
        """Least-residue descent margin r-T^K(r)."""
        return self.residue - self.endpoint


def first_crossing_cylinders(max_length: int) -> dict[int, dict[int, Cylinder]]:
    """Enumerate words whose coefficient first becomes <1 at their last bit.

    A word is encoded chronologically, with its first parity bit in bit 0.
    Once a branch crosses, it is recorded and not extended.
    """
    if max_length < 1:
        raise ValueError("max_length must be positive")
    groups: dict[int, dict[int, Cylinder]] = defaultdict(dict)
    stack = [(0, Cylinder.empty())]
    while stack:
        bits, state = stack.pop()
        if state.length == max_length:
            continue
        for bit in (0, 1):
            extension = state.extend(bit)
            extension_bits = bits | (bit << state.length)
            if extension.pow3 < extension.pow2:
                groups[extension.length][extension_bits] = extension
            else:
                stack.append((extension_bits, extension))
    return dict(groups)


def audit(max_length: int = 26) -> dict[str, int | str]:
    """Verify every admissible 01->10 edge through ``max_length`` exactly."""
    groups = first_crossing_cylinders(max_length)
    digest = hashlib.sha256()
    cylinders = sum(len(group) for group in groups.values())
    edges = 0
    wrapped = 0
    unwrapped = 0
    minimum_jump = None
    maximum_jump = 0

    for length in sorted(groups):
        states = groups[length]
        modulus = 1 << length
        for bits in sorted(states):
            source = states[bits]
            for position in range(length - 1):
                # Source has 01; target moves that 1 one place earlier to 10.
                if ((bits >> position) & 3) != 2:
                    continue
                target_bits = bits ^ (3 << position)
                target = states.get(target_bits)
                if target is None:
                    raise AssertionError("left shift did not preserve first crossing")

                prefix_ones = (bits & ((1 << position) - 1)).bit_count()
                suffix_ones = (bits >> (position + 2)).bit_count()
                if prefix_ones + suffix_ones + 1 != source.odd_count:
                    raise AssertionError("weight decomposition failed")

                local_modulus = 1 << (length - position)
                inverse = pow(3 ** (prefix_ones + 1), -1, local_modulus)
                complement = local_modulus - inverse
                gap = modulus - source.pow3
                suffix_power = 3**suffix_ones
                numerator_delta = (1 << position) * suffix_power
                residue_delta = (1 << position) * inverse

                if source.numerator - target.numerator != numerator_delta:
                    raise AssertionError("affine numerator swap identity failed")
                expected_residue = (source.residue + residue_delta) % modulus
                if target.residue != expected_residue:
                    raise AssertionError("2-adic residue swap identity failed")

                jump_numerator = gap * inverse + suffix_power
                if jump_numerator % local_modulus:
                    raise AssertionError("jump integrality failed")
                positive_jump = jump_numerator // local_modulus
                wrapped_here = source.residue + residue_delta >= modulus
                expected_margin_delta = positive_jump - (gap if wrapped_here else 0)
                actual_margin_delta = target.margin - source.margin
                if actual_margin_delta != expected_margin_delta:
                    raise AssertionError("margin cocycle identity failed")

                negative_jump_numerator = gap * complement - suffix_power
                if negative_jump_numerator % local_modulus:
                    raise AssertionError("complementary jump integrality failed")
                negative_jump = negative_jump_numerator // local_modulus
                if positive_jump + negative_jump != gap:
                    raise AssertionError("jump complementarity failed")
                if not (0 < positive_jump < gap and 0 < negative_jump < gap):
                    raise AssertionError("first-crossing jump bounds failed")
                if wrapped_here:
                    wrapped += 1
                    if actual_margin_delta != -negative_jump:
                        raise AssertionError("wrapped edge did not decrease margin")
                else:
                    unwrapped += 1
                    if actual_margin_delta != positive_jump:
                        raise AssertionError("unwrapped edge did not increase margin")

                edges += 1
                minimum_jump = (
                    positive_jump
                    if minimum_jump is None
                    else min(minimum_jump, positive_jump, negative_jump)
                )
                maximum_jump = max(maximum_jump, positive_jump, negative_jump)
                digest.update(
                    (
                        f"{length},{bits:x},{position},{source.residue},"
                        f"{source.endpoint},{target.residue},{target.endpoint},"
                        f"{positive_jump},{negative_jump},{int(wrapped_here)}\n"
                    ).encode("ascii")
                )

    return {
        "max_length": max_length,
        "first_crossing_cylinders": cylinders,
        "adjacent_edges": edges,
        "unwrapped_edges": unwrapped,
        "wrapped_edges": wrapped,
        "minimum_jump": minimum_jump or 0,
        "maximum_jump": maximum_jump,
        "sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=26)
    args = parser.parse_args()
    for key, value in audit(args.max_length).items():
        print(f"{key}={value}")
    print("status=exact adjacent-swap cocycle audit passed")


if __name__ == "__main__":
    main()
