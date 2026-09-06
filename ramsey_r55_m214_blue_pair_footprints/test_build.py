#!/usr/bin/env python3
"""Semantic and corruption controls for the blue-pair suffix."""

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
        certificate_lines[0] == "index\tfamily\tc\tk\tpattern\tselector\tbound\tH\texterior\tpair_rows",
        "certificate header",
    )
    require(len(certificate_lines) == 157, "certificate line count")
    suffix_lines = suffix.splitlines()
    require(len(suffix_lines) == 74958, "suffix line count")
    certificate_index = 1
    suffix_index = 0
    for root_index, key in enumerate(build.ROOT_KEYS):
        common = key[1]
        if common not in (9, 10):
            continue
        family, _, exceptional_common, pattern = key
        cells = build.root_cells(key)
        core = cells[0] + cells[4]
        exterior = tuple(vertex for vertex in range(2, build.N) if vertex not in core)
        pair_rows = len(exterior) * (len(exterior) - 1) // 2
        fields = certificate_lines[certificate_index].split("\t")
        certificate_index += 1
        expected_fields = (
            str(root_index), family, str(common), str(exceptional_common), pattern,
            str(build.SELECTOR_FIRST + root_index), str(common - 5),
            ",".join(map(str, core)), str(len(exterior)), str(pair_rows),
        )
        require(tuple(fields) == expected_fields, "certificate row mismatch")
        bound = common - 5
        for left, right in itertools.combinations(exterior, 2):
            tokens = suffix_lines[suffix_index].split()
            suffix_index += 1
            require(tokens[-3:] == [">=", "0", ";"], "suffix relation")
            term_tokens = tokens[:-3]
            require(len(term_tokens) == 2 * (2 * common + 2), "suffix arity")
            terms = tuple(
                (int(term_tokens[offset]), int(term_tokens[offset + 1][1:]))
                for offset in range(0, len(term_tokens), 2)
            )
            expected_terms = (
                tuple((1, build.edge_id(left, vertex)) for vertex in core)
                + tuple((1, build.edge_id(right, vertex)) for vertex in core)
                + ((bound, build.edge_id(left, right)),
                   (-bound, build.SELECTOR_FIRST + root_index))
            )
            require(terms == expected_terms, "suffix term mismatch")
    require(certificate_index == len(certificate_lines), "unconsumed certificate")
    require(suffix_index == len(suffix_lines), "unconsumed suffix")


def guard_truth_controls() -> int:
    checked = 0
    for common in (9, 10):
        bound = common - 5
        for incidence_sum in range(2 * common + 1):
            for blue_pair_edge in (0, 1):
                for selector in (0, 1):
                    lhs = incidence_sum + bound * blue_pair_edge - bound * selector
                    expected = selector == 0 or blue_pair_edge == 1 or incidence_sum >= bound
                    require((lhs >= 0) == expected, "guard truth table")
                    checked += 1
    return checked


def structural_controls() -> tuple[int, tuple[int, ...]]:
    certificate = build.sharpness_certificate()
    require(len(certificate["records"]) == 5, "sharp case count")
    strict = tuple(
        common
        for common in range(9, 14)
        if common - 5 > 2 * (common - 8)
    )
    require(strict == (9, 10), "nonredundant codegrees")
    return len(certificate["records"]), strict


def corruption_controls(certificate: str, suffix: str) -> int:
    bad = [
        (certificate.replace("index\tfamily", "INDEX\tfamily", 1), suffix),
        ("\n".join(certificate.splitlines()[:-1]) + "\n", suffix),
        (certificate.replace("0\tE8\t9", "1\tE8\t9", 1), suffix),
        (certificate.replace("\t13245\t4\t", "\t13244\t4\t", 1), suffix),
        (certificate.replace("\t32\t496", "\t32\t495", 1), suffix),
        (certificate, suffix.replace("+1 x", "+2 x", 1)),
        (certificate, suffix.replace("+4 x", "+3 x", 1)),
        (certificate, "\n".join(suffix.splitlines()[:-1]) + "\n"),
    ]
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
    sharp_cases, strict = structural_controls()
    print(f"guard_truth_assignments {guard_truth_controls()}")
    print(f"suffix_rows_checked {len(suffix.splitlines())}")
    print(f"edge_ids_checked {len(edge_ids)}")
    print(f"sharp_cases {sharp_cases}")
    print("strict_projection_codegrees " + " ".join(map(str, strict)))
    print(f"corruptions_rejected {corruption_controls(certificate, suffix)}")
    print("status PASS")


if __name__ == "__main__":
    main()
