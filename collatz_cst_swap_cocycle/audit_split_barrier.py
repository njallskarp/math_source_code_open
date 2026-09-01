"""Independent exact audit of the prefix/suffix split barrier.

This checker uses the Python parity-cylinder implementation and arbitrary
precision integers.  The faster C++ checker uses a separate fixed-width
implementation to extend the exhaustive frontier.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter

from audit_swap_cocycle import cylinder_from_bits, first_crossing_cylinders


def chronological_word(bits: int, length: int) -> str:
    return "".join(str((bits >> position) & 1) for position in range(length))


def audit(max_length: int = 26) -> dict[str, int | str | dict[int, int]]:
    groups = first_crossing_cylinders(max_length)
    digest = hashlib.sha256()
    first_crossings = sum(len(states) for states in groups.values())
    candidate_edges = 0
    wrapped_edges = 0
    positive_prefix_surplus = 0
    nonpositive_prefix_surplus = 0
    descent_failures = 0
    certificate_bits: Counter[int] = Counter()
    wrapped_by_prefix: Counter[int] = Counter()
    residual_by_prefix: Counter[int] = Counter()
    maximum_certificate_bits = 0
    maximum_certificate_example = ""
    first_residual_prefix_at_least_six = "none"
    minimum_margin: int | None = None
    minimum_margin_length = 0
    minimum_margin_word = ""

    for length in sorted(groups):
        states = groups[length]
        modulus = 1 << length
        for bits in sorted(states):
            target = states[bits]
            if length > 2 and (
                minimum_margin is None or target.margin < minimum_margin
            ):
                minimum_margin = target.margin
                minimum_margin_length = length
                minimum_margin_word = chronological_word(bits, length)
            if length > 2 and target.margin <= 0:
                descent_failures += 1

            for position in range(length - 1):
                # Target is p10s in chronological notation.
                if ((bits >> position) & 3) != 1:
                    continue
                prefix = cylinder_from_bits(bits, position)
                if prefix.pow3 < 2 * prefix.pow2:
                    continue
                candidate_edges += 1

                scale = 1 << position
                local_modulus = 1 << (length - position)
                target_lift, remainder = divmod(
                    target.residue - prefix.residue, scale
                )
                if remainder or target_lift < 0:
                    raise AssertionError("target does not lift its prefix")
                inverse = pow(3 * prefix.pow3, -1, local_modulus)
                if target_lift >= inverse:
                    continue
                wrapped_edges += 1
                wrapped_by_prefix[position] += 1

                suffix = cylinder_from_bits(
                    bits >> (position + 2), length - position - 2
                )
                gap = modulus - target.pow3
                prefix_surplus = (
                    local_modulus * prefix.residue
                    - suffix.pow3 * (3 * prefix.endpoint + 1)
                    - 4 * suffix.numerator
                )
                if (
                    gap * target_lift + prefix_surplus
                    != local_modulus * target.margin
                ):
                    raise AssertionError("split barrier identity failed")

                if prefix_surplus > 0:
                    positive_prefix_surplus += 1
                    required_bits = 0
                else:
                    nonpositive_prefix_surplus += 1
                    residual_by_prefix[position] += 1
                    if (
                        position >= 6
                        and first_residual_prefix_at_least_six == "none"
                    ):
                        first_residual_prefix_at_least_six = (
                            f"K:{length},j:{position},"
                            f"word:{chronological_word(bits, length)}"
                        )
                    required_bits = 0
                    for bits_used in range(2, length - position + 1):
                        lift_lower_bound = target_lift & ((1 << bits_used) - 1)
                        if gap * lift_lower_bound + prefix_surplus > 0:
                            required_bits = bits_used
                            break
                    if required_bits == 0:
                        raise AssertionError(
                            "the full split coordinate did not certify descent"
                        )
                    if required_bits > maximum_certificate_bits:
                        maximum_certificate_bits = required_bits
                        maximum_certificate_example = (
                            f"K:{length},j:{position},"
                            f"word:{chronological_word(bits, length)}"
                        )
                certificate_bits[required_bits] += 1
                digest.update(
                    (
                        f"{length},{bits:x},{position},{target.residue},"
                        f"{target.endpoint},{target_lift},{prefix_surplus},"
                        f"{required_bits}\n"
                    ).encode("ascii")
                )

    return {
        "max_length": max_length,
        "first_crossings": first_crossings,
        "candidate_edges": candidate_edges,
        "wrapped_edges": wrapped_edges,
        "positive_prefix_surplus": positive_prefix_surplus,
        "nonpositive_prefix_surplus": nonpositive_prefix_surplus,
        "descent_failures": descent_failures,
        "minimum_margin": minimum_margin or 0,
        "minimum_margin_length": minimum_margin_length,
        "minimum_margin_word": minimum_margin_word,
        "certificate_bits": dict(sorted(certificate_bits.items())),
        "wrapped_by_prefix": dict(sorted(wrapped_by_prefix.items())),
        "residual_by_prefix": dict(sorted(residual_by_prefix.items())),
        "maximum_certificate_bits": maximum_certificate_bits,
        "maximum_certificate_example": maximum_certificate_example,
        "first_residual_prefix_at_least_six": (
            first_residual_prefix_at_least_six
        ),
        "sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=26)
    args = parser.parse_args()
    for key, value in audit(args.max_length).items():
        print(f"{key}={value}")
    print("status=independent exact split-barrier audit passed")


if __name__ == "__main__":
    main()
