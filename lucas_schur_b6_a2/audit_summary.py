#!/usr/bin/env python3
"""Compact exact audit map for the provisional canonical (2,6) theorem.

This is a diagnostic projection of the bundled proof checkers, not an
independent verification. It exposes the certificate families, margins,
width-two correction, bases, and parity endpoints in one canonical record.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from math import comb
from pathlib import Path
from types import ModuleType


EXPECTED_AUDIT_SHA256 = "77593a7ce033cd31e707a541a5ece1e281af64d0502b931ade887bc3e6826368"


def load_sibling(name: str, filename: str) -> ModuleType:
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


certificate = load_sibling("lucas_b6_a2_certificate", "verify_fraction.py")
layers = load_sibling("lucas_b6_a2_layers", "verify_layers.py")


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def family_summary(records: list[dict[str, object]]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for residue in (0, 1):
        for quantity in ("A", "C"):
            family = [
                record
                for record in records
                if record["r"] == residue and record["q"] == quantity
            ]
            exact_minimum: tuple[int, int, int] | None = None
            bernstein_minimum: tuple[Fraction, int, int, int] | None = None
            exact_value_count = 0
            bernstein_count = 0
            bernstein_scalar_count = 0
            terms = certificate.quantity_terms(residue, quantity)

            for cell_index, record in enumerate(family):
                if "v" in record:
                    left = tuple(record["l"])
                    active = [
                        term
                        for term in terms
                        if certificate.nonnegative_after_shift(
                            left[0] + term[1][1], left[1] + term[1][2]
                        )
                    ]
                    assert active
                    assert all(argument[1] == 0 for _, argument in active)
                    for offset, value in enumerate(record["v"]):
                        exact_value_count += 1
                        candidate = (value, cell_index, record["l"][1] + offset)
                        if exact_minimum is None or candidate < exact_minimum:
                            exact_minimum = candidate
                    continue

                polynomials = record["b"]
                assert len(polynomials) == 5
                bernstein_count += len(polynomials)
                for basis_index, polynomial in enumerate(polynomials):
                    assert polynomial, (residue, quantity, cell_index, basis_index)
                    for degree, numerator, denominator in polynomial:
                        value = Fraction(numerator, denominator)
                        assert value > 0
                        bernstein_scalar_count += 1
                        candidate = (value, cell_index, basis_index, degree)
                        if bernstein_minimum is None or candidate < bernstein_minimum:
                            bernstein_minimum = candidate

            assert exact_minimum is not None and bernstein_minimum is not None
            exact_record = family[exact_minimum[1]]
            bernstein_record = family[bernstein_minimum[1]]
            result.append({
                "c_mod_2": residue,
                "quantity": quantity,
                "cells": len(family),
                "exact_cells": sum("v" in record for record in family),
                "exact_values": exact_value_count,
                "exact_minimum": exact_minimum[0],
                "exact_minimum_witness": {
                    "cell": exact_minimum[1],
                    "j": exact_minimum[2],
                    "lower": exact_record["l"],
                    "upper": exact_record["u"],
                },
                "bernstein_polynomials": bernstein_count,
                "bernstein_scalar_coefficients": bernstein_scalar_count,
                "bernstein_minimum": fraction_text(bernstein_minimum[0]),
                "bernstein_minimum_witness": {
                    "cell": bernstein_minimum[1],
                    "basis_index": bernstein_minimum[2],
                    "x_degree": bernstein_minimum[3],
                    "lower": bernstein_record["l"],
                    "upper": bernstein_record["u"],
                },
            })
    return result


def finite_summary() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for residue in (0, 1):
        for quantity in ("A", "C"):
            values: list[tuple[int, int, int]] = []
            for c in range(16, 2 * certificate.T_START):
                if c % 2 != residue:
                    continue
                parameter = (c - residue) // 2
                slope, intercept = certificate.domain_end(residue, quantity)
                for pair in range(slope * parameter + intercept):
                    value = certificate.remainder_layer(c, 2 * pair)
                    if quantity == "C":
                        value = 2 * value - certificate.remainder_layer(c, 2 * pair + 1)
                    assert value > 0
                    values.append((value, c, pair))
            minimum = min(values)
            result.append({
                "c_mod_2": residue,
                "quantity": quantity,
                "values_checked": len(values),
                "minimum": minimum[0],
                "minimum_witness": {"c": minimum[1], "j": minimum[2]},
            })
    return result


def base_summary() -> dict[str, object]:
    rows = layers.ell_table(90)
    coefficient_rows: list[list[int]] = []
    minimum: tuple[int, int, int] | None = None
    for c in range(6, 16):
        coefficients = layers.lucas_schur_from_h(c, layers.direct_h(c), rows)
        assert coefficients[:3] == [0, 0, 0]
        assert coefficients[3] == 1 and all(value > 0 for value in coefficients[3:])
        for r in range(4, 3 * c + 1):
            lower = comb(6 * c - 8, r - 4) - (
                comb(6 * c - 8, r - 5) if r >= 5 else 0
            )
            assert coefficients[r] >= lower
        coefficient_rows.append(coefficients)
        for r, value in enumerate(coefficients):
            if value:
                candidate = (value, c, r)
                if minimum is None or candidate < minimum:
                    minimum = candidate
    assert minimum is not None
    canonical = json.dumps(coefficient_rows, separators=(",", ":"))
    return {
        "parameters": [6, 15],
        "row_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "least_nonzero": {
            "coefficient": minimum[0], "c": minimum[1], "r": minimum[2]
        },
    }


def endpoint_summary() -> dict[str, object]:
    even_pairs: list[tuple[int, int, int, int]] = []
    odd_pairs: list[tuple[int, int, int, int]] = []
    odd_middle: list[tuple[int, int, int]] = []
    for c in range(16, 2 * certificate.T_START):
        current = layers.direct_h(c)
        previous = layers.direct_h(c - 10)
        k_values = [
            current[r + 3] - layers.value(previous, r - 27)
            for r in range(3 * c - 2)
        ]
        pair = len(k_values) // 2 - 1
        m = 6 * c - 6 - 4 * pair + 1
        a_value = k_values[2 * pair]
        c_value = 2 * a_value - k_values[2 * pair + 1]
        assert a_value > 0 and c_value > 0
        if c % 2 == 0:
            assert m == 3 and len(k_values) % 2 == 0
            even_pairs.append((min(a_value, c_value), c, pair, m))
        else:
            assert m == 5 and len(k_values) % 2 == 1
            odd_pairs.append((min(a_value, c_value), c, pair, m))
            index = len(k_values) - 1
            value = k_values[index]
            assert index == 3 * c - 3 and index % 2 == 0 and value > 0
            odd_middle.append((value, c, index))

    even_minimum = min(even_pairs)
    odd_pair_minimum = min(odd_pairs)
    odd_middle_minimum = min(odd_middle)
    return {
        "range": [16, 2 * certificate.T_START - 1],
        "even_last_pair_m_values": sorted({entry[3] for entry in even_pairs}),
        "even_last_pair_minimum": {
            "coefficient": even_minimum[0],
            "c": even_minimum[1],
            "j": even_minimum[2],
        },
        "odd_last_pair_m_values": sorted({entry[3] for entry in odd_pairs}),
        "odd_last_pair_minimum": {
            "coefficient": odd_pair_minimum[0],
            "c": odd_pair_minimum[1],
            "j": odd_pair_minimum[2],
        },
        "odd_middle_minimum": {
            "coefficient": odd_middle_minimum[0],
            "c": odd_middle_minimum[1],
            "index": odd_middle_minimum[2],
        },
    }


def build_summary() -> dict[str, object]:
    certificate.verify_quasipolynomial()
    certificate.verify_term_translation()
    certificate.verify_finite_parameters()
    assert all(certificate.quantity_constant("C", j) == (j < 13) for j in range(30))
    assert all(certificate.quantity_constant("A", j) == 0 for j in range(30))

    records = certificate.certificate_records()
    certificate_json = json.dumps(records, sort_keys=True, separators=(",", ":"))
    certificate_sha256 = hashlib.sha256(certificate_json.encode()).hexdigest()
    assert certificate_sha256 == certificate.EXPECTED_CERTIFICATE_SHA256
    return {
        "certificate_sha256": certificate_sha256,
        "families": family_summary(records),
        "finite_complement": finite_summary(),
        "width_two_correction": {"quantity": "C", "j_inclusive": [0, 12]},
        "bases": base_summary(),
        "endpoints": endpoint_summary(),
        "trust": "diagnostic projection; not an independent proof",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = build_summary()
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    if EXPECTED_AUDIT_SHA256:
        assert digest == EXPECTED_AUDIT_SHA256, digest

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("compact exact audit summary passed")
        print(f"certificate SHA-256: {summary['certificate_sha256']}")
        for family in summary["families"]:
            print(
                "family "
                f"rho={family['c_mod_2']} {family['quantity']}: "
                f"cells={family['cells']}, exact={family['exact_cells']}, "
                f"Bernstein={family['bernstein_polynomials']}, "
                f"minimum Bernstein scalar={family['bernstein_minimum']}"
            )
        print(
            "finite complement minima: "
            + ", ".join(
                f"rho={item['c_mod_2']} {item['quantity']}={item['minimum']}"
                for item in summary["finite_complement"]
            )
        )
        print("width-two correction: C_j has +1 exactly for 0 <= j <= 12")
        print(
            "ten-base coefficient-row SHA-256: "
            f"{summary['bases']['row_sha256']}"
        )
        print(
            "endpoint regimes: even last-pair m=3; odd last-pair m=5; "
            f"minimum odd middle={summary['endpoints']['odd_middle_minimum']['coefficient']}"
        )
    print(f"audit-summary SHA-256: {digest}")


if __name__ == "__main__":
    main()
