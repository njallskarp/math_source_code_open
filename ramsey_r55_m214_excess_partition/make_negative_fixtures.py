#!/usr/bin/env python3
"""Create two deterministic corruptions for rejection tests (generated state only)."""

from __future__ import annotations

import argparse
from pathlib import Path


PROOF_OLD = b": x13245 -> 0;"
PROOF_NEW = b": x13245 -> 1;"
FORMULA_OLD = (
    b"+1 x13332 +1 x13333 +1 x13334 +1 x13335 +1 x13336 "
    b"+1 x13337 +1 x13338 +1 x13339 +1 x13340 +1 x13341 >= 1 ;\n"
)
FORMULA_NEW = FORMULA_OLD.replace(b">= 1 ;", b">= 2 ;")


def mutate_proof(source: Path, destination: Path) -> None:
    data = source.read_bytes()
    if PROOF_OLD not in data:
        raise ValueError("missing first-threshold witness")
    destination.write_bytes(data.replace(PROOF_OLD, PROOF_NEW, 1))


def mutate_formula(source: Path, destination: Path) -> None:
    replaced = 0
    with source.open("rb") as incoming, destination.open("wb") as outgoing:
        for line in incoming:
            if line == FORMULA_OLD:
                outgoing.write(FORMULA_NEW)
                replaced += 1
            else:
                outgoing.write(line)
    if replaced != 1:
        destination.unlink(missing_ok=True)
        raise ValueError(f"expected one final one-hot row, found {replaced}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args()
    args.output_directory.mkdir(parents=True, exist_ok=True)
    mutate_formula(args.formula, args.output_directory / "corrupt_formula.opb")
    mutate_proof(args.proof, args.output_directory / "corrupt_proof.pbp")
    print("PASS negative_fixtures formula=one_hot_rhs_2 proof=u0_witness_1")


if __name__ == "__main__":
    main()
