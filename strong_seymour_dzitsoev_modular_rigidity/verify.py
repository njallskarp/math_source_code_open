#!/usr/bin/env python3
"""Regenerate and verify the published modular-rigidity certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import generate_certificate as generator

CERTIFICATE_PATH = Path(__file__).with_name("certificate.json")


def main() -> None:
    raw = CERTIFICATE_PATH.read_bytes()
    certificate = json.loads(raw)
    rendered = (
        json.dumps(generator.build_certificate(), sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    if raw != rendered:
        raise AssertionError("certificate does not match exact regeneration")
    print(
        "VERIFIED DZITSOEV MODULAR RIGIDITY; "
        f"quotient_mask={certificate['canonical_quotient_mask']} "
        f"quotient_automorphisms={certificate['quotient_automorphism_count']} "
        f"order={certificate['expanded_order']} "
        f"modules={certificate['module_count_including_empty_and_full']} "
        f"maximal_proper_modules={len(certificate['maximal_proper_modules_hex'])} "
        f"cross_pair_closures={certificate['pair_counts']['cross_fiber_forcing_full']} "
        f"pair_closure_sha256={certificate['expanded_pair_closure_sha256']} "
        f"certificate_sha256={hashlib.sha256(raw).hexdigest()}"
    )


if __name__ == "__main__":
    main()
