#!/usr/bin/env python3
"""Positive and mutation tests for the dependency-free MUS verifier."""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import tempfile

from verify_signed_k4_mus import verify


def expect_rejection(data: pathlib.Path, certificate: dict[str, object]) -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = pathlib.Path(directory) / "mutated.json"
        path.write_text(json.dumps(certificate))
        try:
            verify(data, path)
        except ValueError:
            return
        raise AssertionError("mutated certificate was accepted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6", type=pathlib.Path)
    parser.add_argument("certificate", type=pathlib.Path)
    args = parser.parse_args()

    positive = verify(args.graph6, args.certificate)
    if not positive["verified"]:
        raise AssertionError("positive verification failed")
    original = json.loads(args.certificate.read_text())

    bad_witness = copy.deepcopy(original)
    bad_witness["deletion_witnesses"][0]["assignment"] = "0" * 42
    expect_rejection(args.graph6, bad_witness)

    truncated_proof = copy.deepcopy(original)
    truncated_proof["drup_proof"] = truncated_proof["drup_proof"][:-1]
    expect_rejection(args.graph6, truncated_proof)

    bad_clause = copy.deepcopy(original)
    bad_clause["core"]["clauses"][0]["vertices_zero_based"][0] = 1
    expect_rejection(args.graph6, bad_clause)
    print("positive certificate accepted; three independent mutations rejected")


if __name__ == "__main__":
    main()
