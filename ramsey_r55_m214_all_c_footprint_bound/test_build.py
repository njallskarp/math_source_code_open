#!/usr/bin/env python3
"""Semantic and corruption controls for build.py."""

from __future__ import annotations

import itertools

import build


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def artifacts() -> tuple[str, str]:
    certificate_raw, _ = build.certificate()
    suffix_raw = ("".join(line + "\n" for line in build.suffix_lines())).encode("ascii")
    return certificate_raw.decode("ascii"), suffix_raw.decode("ascii")


def verify_artifacts(certificate: str, suffix: str) -> None:
    certificate_lines = certificate.splitlines()
    require(
        certificate_lines[0] == "index\tfamily\tc\tk\tpattern\tselector\tbound\tH\texterior_rows",
        "certificate header",
    )
    require(len(certificate_lines) == 390, "certificate line count")
    suffix_lines = suffix.splitlines()
    require(len(suffix_lines) == 11672, "suffix line count")
    suffix_index = 0
    for root_index, key in enumerate(build.ROOT_KEYS):
        fields = certificate_lines[root_index + 1].split("\t")
        require(len(fields) == 9, "certificate field count")
        family, common, exceptional_common, pattern = key
        cells = build.root_cells(key)
        core = cells[0] + cells[4]
        exterior = tuple(vertex for vertex in range(2, build.N) if vertex not in core)
        expected_fields = (
            str(root_index),
            family,
            str(common),
            str(exceptional_common),
            pattern,
            str(build.SELECTOR_FIRST + root_index),
            str(common - 8),
            ",".join(map(str, core)),
            str(len(exterior)),
        )
        require(tuple(fields) == expected_fields, "certificate row mismatch")
        for vertex in exterior:
            tokens = suffix_lines[suffix_index].split()
            suffix_index += 1
            require(tokens[-3:] == [">=", "0", ";"], "suffix relation")
            term_tokens = tokens[:-3]
            require(len(term_tokens) == 2 * (common + 1), "suffix arity")
            terms = tuple(
                (int(term_tokens[offset]), int(term_tokens[offset + 1][1:]))
                for offset in range(0, len(term_tokens), 2)
            )
            expected_terms = tuple(
                (1, build.edge_id(vertex, core_vertex)) for core_vertex in core
            ) + ((-(common - 8), build.SELECTOR_FIRST + root_index),)
            require(terms == expected_terms, "suffix term mismatch")
    require(suffix_index == len(suffix_lines), "unconsumed suffix")


def guard_truth_controls() -> int:
    checked = 0
    for common in range(9, 14):
        bound = common - 8
        for footprint_size in range(common + 1):
            for selector in (0, 1):
                lhs = footprint_size - bound * selector
                expected = selector == 0 or footprint_size >= bound
                require((lhs >= 0) == expected, "guard truth table")
                checked += 1
    return checked


def sharp_deletion_controls() -> int:
    controls = 0
    for common in range(9, 14):
        footprint = build.SHARP_EXTRAS[: common - 8]
        core = build.SHARP_T + footprint
        for removed in footprint:
            damaged = set(footprint) - {removed}
            missed = [
                four
                for four in build.independent_sets(core, 4)
                if not set(four).intersection(damaged)
            ]
            require(missed, "smaller footprint unexpectedly hits every independent four")
            controls += 1
    return controls


def corruption_controls(certificate: str, suffix: str) -> int:
    bad = []
    bad.append((certificate.replace("index\tfamily", "INDEX\tfamily", 1), suffix))
    bad.append(("\n".join(certificate.splitlines()[:-1]) + "\n", suffix))
    bad.append((certificate.replace("0\tE8\t9", "1\tE8\t9", 1), suffix))
    bad.append((certificate.replace("\t13245\t1\t", "\t13244\t1\t", 1), suffix))
    bad.append((certificate.replace("15,16,17", "15,16,18", 1), suffix))
    bad.append((certificate, suffix.replace("+1 x", "+2 x", 1)))
    bad.append((certificate, suffix.replace("-1 x13245", "-1 x13246", 1)))
    bad.append((certificate, "\n".join(suffix.splitlines()[:-1]) + "\n"))
    rejected = 0
    for damaged_certificate, damaged_suffix in bad:
        try:
            verify_artifacts(damaged_certificate, damaged_suffix)
        except AssertionError:
            rejected += 1
    require(rejected == len(bad), "corruption escaped")
    return rejected


def main() -> None:
    certificate, suffix = artifacts()
    verify_artifacts(certificate, suffix)
    edge_ids = {
        build.edge_id(left, right)
        for left, right in itertools.combinations(range(build.N), 2)
    }
    require(edge_ids == set(range(1, 904)), "edge-variable bijection")
    print(f"guard_truth_assignments {guard_truth_controls()}")
    print(f"sharp_deletion_controls {sharp_deletion_controls()}")
    print(f"suffix_rows_checked {len(suffix.splitlines())}")
    print(f"edge_ids_checked {len(edge_ids)}")
    print(f"corruptions_rejected {corruption_controls(certificate, suffix)}")
    print("status PASS")


if __name__ == "__main__":
    main()
