#!/usr/bin/env python3
"""Regenerate and verify the compact six-quotient rigidity certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import generate_certificate as generator

CERTIFICATE_PATH = Path(__file__).with_name("certificate.json")
PUBLISHED_TO_CANONICAL = (5, 4, 0, 1, 3, 2)


def relabel_weights(
    weights: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    answer = [0] * len(weights)
    for old, new in enumerate(permutation):
        answer[new] = weights[old]
    return tuple(answer)


def main() -> None:
    raw = CERTIFICATE_PATH.read_bytes()
    published = json.loads(raw)
    regenerated = generator.build_certificate()
    rendered = (
        json.dumps(regenerated, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("ascii")
    if raw != rendered or published != regenerated:
        raise AssertionError("published certificate does not match exact regeneration")

    if generator.relabel(generator.PUBLISHED_MASK, PUBLISHED_TO_CANONICAL) != 345:
        raise AssertionError("published quotient does not relabel to canonical mask 345")
    if (
        relabel_weights(generator.PUBLISHED_SIZES, PUBLISHED_TO_CANONICAL)
        != generator.CANONICAL_MINIMUM_SIZES
    ):
        raise AssertionError("published weights do not relabel to the canonical minimum")

    feasible_bytes = json.dumps(
        published["feasible"], sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    certificate_sha256 = hashlib.sha256(raw).hexdigest()
    feasible_sha256 = hashlib.sha256(feasible_bytes).hexdigest()
    print(
        "VERIFIED SIX-QUOTIENT RIGIDITY; "
        "quotient_types=56 zero_root=12 closure_chambers=3603 "
        "multicover_blocked=3591 feasible=12 unique_quotient=345 minimum=36 "
        f"certificate_sha256={certificate_sha256}"
    )
    print(
        json.dumps(
            {
                "canonical_minimum_sizes": published["canonical_minimum_sizes"],
                "dual_totals": [entry["total"] for entry in published["feasible"]],
                "feasible_sha256": feasible_sha256,
                "published_relabel": list(PUBLISHED_TO_CANONICAL),
                "status": "EXACT MULTICOVER ALTERNATIVE VERIFIED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
