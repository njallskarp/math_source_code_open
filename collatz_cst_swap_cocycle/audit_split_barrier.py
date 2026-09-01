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


def relative_coefficient_crossing(prefix, candidate_lift: int) -> int:
    """First suffix length that contracts from the post-``p10`` lift.

    The returned computation is exact.  It is used only as a certificate: a
    candidate suffix that remains coefficient-safe longer than this orbit
    cannot have the full local lift equal to ``candidate_lift``.
    """
    prefix_power = 3 * prefix.pow3
    numerator = prefix_power * candidate_lift + 3 * prefix.endpoint + 1
    quotient, remainder = divmod(numerator, 4)
    if remainder:
        raise AssertionError("the p10 base lift is not integral")
    value = quotient
    suffix_power = 1
    suffix_modulus = 1
    for length in range(1, 10_001):
        if value & 1:
            value = (3 * value + 1) // 2
            suffix_power *= 3
        else:
            value //= 2
        suffix_modulus *= 2
        if prefix_power * suffix_power < 4 * prefix.pow2 * suffix_modulus:
            return length
    raise AssertionError("relative coefficient crossing exceeded audit cap")


def first_suffix_parity_mismatch(
    prefix, candidate_lift: int, suffix_bits: int, suffix_length: int
) -> int:
    """Return the one-based first mismatch with the prescribed suffix."""
    prefix_power = 3 * prefix.pow3
    numerator = prefix_power * candidate_lift + 3 * prefix.endpoint + 1
    value, remainder = divmod(numerator, 4)
    if remainder:
        raise AssertionError("the p10 candidate lift is not integral")
    for index in range(suffix_length):
        observed = value & 1
        expected = (suffix_bits >> index) & 1
        if observed != expected:
            return index + 1
        value = value // 2 if observed == 0 else (3 * value + 1) // 2
    return 0


def audit(max_length: int = 26) -> dict[str, int | str | dict[int, int]]:
    groups = first_crossing_cylinders(max_length)
    digest = hashlib.sha256()
    first_crossings = sum(len(states) for states in groups.values())
    candidate_edges = 0
    wrapped_edges = 0
    positive_prefix_surplus = 0
    nonpositive_prefix_surplus = 0
    low_two_bit_certificates = 0
    base_shadow_certificates = 0
    unresolved_after_base_shadow = 0
    adaptive_shadow_certificates = 0
    excluded_lift_ladder_certificates = 0
    excluded_lift_ladder_candidates = 0
    excluded_lift_ladder_parity_bits = 0
    maximum_excluded_lift_ladder_steps = 0
    maximum_excluded_lift_mismatch_depth = 0
    excluded_lift_ladder_step_histogram: Counter[int] = Counter()
    excluded_lift_mismatch_histogram: Counter[int] = Counter()
    excluded_lift_ladder_bit_bound = 0
    suffix_rank_formula_failures = 0
    valuation_mismatch_failures = 0
    descent_failures = 0
    certificate_bits: Counter[int] = Counter()
    symbolic_certificate_bits: Counter[int] = Counter()
    wrapped_by_prefix: Counter[int] = Counter()
    residual_by_prefix: Counter[int] = Counter()
    maximum_certificate_bits = 0
    maximum_certificate_example = ""
    maximum_symbolic_certificate_bits = 0
    maximum_symbolic_certificate_example = ""
    first_residual_prefix_at_least_six = "none"
    minimum_margin: int | None = None
    minimum_margin_length = 0
    minimum_margin_word = ""
    crossing_cache: dict[tuple[int, int, int], int] = {}

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
                    symbolic_bits = 0
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
                    lift_mod_four = target_lift & 3
                    base_barrier = gap * lift_mod_four + prefix_surplus
                    if base_barrier <= 0:
                        step_gain = 4 * gap
                        ladder_steps = (-base_barrier) // step_gain + 1
                        forced_lower_bound = lift_mod_four + 4 * ladder_steps
                        if forced_lower_bound > target_lift:
                            raise AssertionError(
                                "excluded-lift ladder overshot the true lift"
                            )
                        if gap * forced_lower_bound + prefix_surplus <= 0:
                            raise AssertionError(
                                "excluded-lift ladder did not clear the barrier"
                            )
                        suffix_length = length - position - 2
                        suffix_bits = bits >> (position + 2)
                        suffix_modulus = 1 << suffix_length
                        prefix_power = 3 * prefix.pow3
                        shadow_zero = (
                            prefix_power * lift_mod_four
                            + 3 * prefix.endpoint
                            + 1
                        ) // 4
                        actual_rank = (target_lift - lift_mod_four) // 4
                        suffix_rank = (
                            (suffix.residue - shadow_zero)
                            * pow(prefix_power, -1, suffix_modulus)
                        ) % suffix_modulus
                        if suffix_rank != actual_rank:
                            suffix_rank_formula_failures += 1
                            raise AssertionError("suffix-rank formula failed")
                        excluded_lift_ladder_step_histogram[
                            ladder_steps
                        ] += 1
                        excluded_lift_ladder_bit_bound += (
                            2 * ladder_steps + suffix_length - 2
                        )
                        for rank in range(ladder_steps):
                            candidate_lift = lift_mod_four + 4 * rank
                            mismatch = first_suffix_parity_mismatch(
                                prefix,
                                candidate_lift,
                                suffix_bits,
                                suffix_length,
                            )
                            if mismatch == 0:
                                raise AssertionError(
                                    "a lower candidate matched the full suffix"
                                )
                            delta = actual_rank - rank
                            valuation_mismatch = (
                                (delta & -delta).bit_length()
                            )
                            if mismatch != valuation_mismatch:
                                valuation_mismatch_failures += 1
                                raise AssertionError(
                                    "valuation mismatch law failed"
                                )
                            excluded_lift_ladder_candidates += 1
                            excluded_lift_ladder_parity_bits += mismatch
                            excluded_lift_mismatch_histogram[mismatch] += 1
                            maximum_excluded_lift_mismatch_depth = max(
                                maximum_excluded_lift_mismatch_depth, mismatch
                            )
                        excluded_lift_ladder_certificates += 1
                        maximum_excluded_lift_ladder_steps = max(
                            maximum_excluded_lift_ladder_steps, ladder_steps
                        )
                    base_shadow_certified = False
                    if gap * lift_mod_four + prefix_surplus > 0:
                        low_two_bit_certificates += 1
                    else:
                        cache_key = (
                            bits & ((1 << position) - 1),
                            position,
                            lift_mod_four,
                        )
                        crossing = crossing_cache.get(cache_key)
                        if crossing is None:
                            crossing = relative_coefficient_crossing(
                                prefix, lift_mod_four
                            )
                            crossing_cache[cache_key] = crossing
                        suffix_length = length - position - 2
                        forced_lower_bound = lift_mod_four + 4
                        if suffix_length > crossing:
                            if forced_lower_bound > target_lift:
                                raise AssertionError(
                                    "shadow forcing did not lower-bound the lift"
                                )
                            if gap * forced_lower_bound + prefix_surplus > 0:
                                base_shadow_certificates += 1
                                base_shadow_certified = True
                            else:
                                unresolved_after_base_shadow += 1
                        else:
                            unresolved_after_base_shadow += 1
                    symbolic_bits = required_bits
                    if required_bits == 2:
                        symbolic_bits = 2
                    elif base_shadow_certified:
                        symbolic_bits = 2
                        adaptive_shadow_certificates += 1
                    else:
                        suffix_length = length - position - 2
                        for bits_used in range(3, required_bits):
                            lift_lower_bound = target_lift & (
                                (1 << bits_used) - 1
                            )
                            crossing = relative_coefficient_crossing(
                                prefix, lift_lower_bound
                            )
                            forced_lower_bound = (
                                lift_lower_bound + (1 << bits_used)
                            )
                            if (
                                suffix_length > crossing
                                and gap * forced_lower_bound + prefix_surplus > 0
                            ):
                                if forced_lower_bound > target_lift:
                                    raise AssertionError(
                                        "adaptive shadow forcing did not "
                                        "lower-bound the lift"
                                    )
                                symbolic_bits = bits_used
                                adaptive_shadow_certificates += 1
                                break
                certificate_bits[required_bits] += 1
                symbolic_certificate_bits[symbolic_bits] += 1
                if symbolic_bits > maximum_symbolic_certificate_bits:
                    maximum_symbolic_certificate_bits = symbolic_bits
                    maximum_symbolic_certificate_example = (
                        f"K:{length},j:{position},"
                        f"word:{chronological_word(bits, length)}"
                    )
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
        "low_two_bit_certificates": low_two_bit_certificates,
        "base_shadow_certificates": base_shadow_certificates,
        "base_shadow_prefixes": len(crossing_cache),
        "unresolved_after_base_shadow": unresolved_after_base_shadow,
        "adaptive_shadow_certificates": adaptive_shadow_certificates,
        "excluded_lift_ladder_certificates": (
            excluded_lift_ladder_certificates
        ),
        "excluded_lift_ladder_candidates": excluded_lift_ladder_candidates,
        "excluded_lift_ladder_parity_bits": (
            excluded_lift_ladder_parity_bits
        ),
        "maximum_excluded_lift_ladder_steps": (
            maximum_excluded_lift_ladder_steps
        ),
        "maximum_excluded_lift_mismatch_depth": (
            maximum_excluded_lift_mismatch_depth
        ),
        "excluded_lift_ladder_step_histogram": dict(
            sorted(excluded_lift_ladder_step_histogram.items())
        ),
        "excluded_lift_mismatch_histogram": dict(
            sorted(excluded_lift_mismatch_histogram.items())
        ),
        "excluded_lift_ladder_bit_bound": excluded_lift_ladder_bit_bound,
        "suffix_rank_formula_failures": suffix_rank_formula_failures,
        "valuation_mismatch_failures": valuation_mismatch_failures,
        "descent_failures": descent_failures,
        "minimum_margin": minimum_margin or 0,
        "minimum_margin_length": minimum_margin_length,
        "minimum_margin_word": minimum_margin_word,
        "certificate_bits": dict(sorted(certificate_bits.items())),
        "symbolic_certificate_bits": dict(
            sorted(symbolic_certificate_bits.items())
        ),
        "wrapped_by_prefix": dict(sorted(wrapped_by_prefix.items())),
        "residual_by_prefix": dict(sorted(residual_by_prefix.items())),
        "maximum_certificate_bits": maximum_certificate_bits,
        "maximum_certificate_example": maximum_certificate_example,
        "maximum_symbolic_certificate_bits": maximum_symbolic_certificate_bits,
        "maximum_symbolic_certificate_example": (
            maximum_symbolic_certificate_example
        ),
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
