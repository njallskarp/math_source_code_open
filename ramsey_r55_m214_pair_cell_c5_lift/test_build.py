#!/usr/bin/env python3
"""Definition-level tests for the missed-pair-cell C5 lift."""

from __future__ import annotations

import hashlib
import itertools

import build


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rejected(callable_object) -> None:
    try:
        callable_object()
    except (ValueError, KeyError):
        return
    raise AssertionError("invalid input was accepted")


def eval_row(terms: list[tuple[int, int]], values: dict[int, int], rhs: int) -> bool:
    return sum(coefficient * values[variable] for coefficient, variable in terms) >= rhs


def main() -> None:
    check(len(build.ROOT_KEYS) == 389, "root count")
    check(len(build.MISSED_KEYS) == 10_612, "missed support")
    check(len(build.RED_INSIDE_KEYS) == 74_513, "inside support")
    check(build.ROOT_PAIRS == 169_662, "root pairs")
    check(build.DEFINITION_ROWS == 329_888, "definition rows")
    check(build.ROOT_ROWS == 508_986, "root rows")
    check(build.SUFFIX_ROWS == 838_874, "suffix rows")
    check(build.VARIABLES == 98_758, "variable count")
    check(build.CONSTRAINTS == 2_969_925, "constraint count")
    check(
        [build.ROOT_PAIR_COUNTS[c] for c in range(9, 14)]
        == [38_688, 36_270, 33_930, 31_668, 29_106],
        "root pair distribution",
    )
    check(
        build.key_hash(build.MISSED_KEYS)
        == "63e2a26d70b743d2833cebbb931a48a7b8d6ce6f4611b2ea720c57f4145dcb20",
        "missed support hash",
    )
    check(
        build.key_hash(build.RED_INSIDE_KEYS)
        == "b7bca6f69d62b7e2fcfac24163f7252f0107850bd7870e4a8a4ba20151603afc",
        "inside support hash",
    )

    all_physical = {
        build.edge_id(i, j) for i, j in itertools.combinations(range(build.N), 2)
    }
    check(all_physical == set(range(1, 904)), "physical edge identifiers")
    check(
        set(build.MISSED_IDS.values())
        == set(range(build.MISSED_FIRST, build.RED_INSIDE_FIRST)),
        "missed identifier interval",
    )
    check(
        set(build.RED_INSIDE_IDS.values())
        == set(range(build.RED_INSIDE_FIRST, build.VARIABLES + 1)),
        "inside identifier interval",
    )
    for left, right, i, j in build.RED_INSIDE_KEYS:
        check((left, right, i) in build.MISSED_IDS, "missing first endpoint variable")
        check((left, right, j) in build.MISSED_IDS, "missing second endpoint variable")

    missed_truths = 0
    for left_value, right_value, missed_value in itertools.product(range(2), repeat=3):
        values = {1: missed_value, 2: left_value, 3: right_value}
        rows = (
            ([(-1, 1), (-1, 2)], -1),
            ([(-1, 1), (-1, 3)], -1),
            ([(1, 1), (1, 2), (1, 3)], 1),
        )
        feasible = all(eval_row(terms, values, rhs) for terms, rhs in rows)
        check(feasible == (missed_value == (1-left_value)*(1-right_value)), "missed truth")
        missed_truths += 1

    inside_truths = 0
    for mi, mj, edge, inside in itertools.product(range(2), repeat=4):
        values = {1: inside, 2: mi, 3: mj, 4: edge}
        rows = (
            ([(-1, 1), (1, 2)], 0),
            ([(-1, 1), (1, 3)], 0),
            ([(-1, 1), (1, 4)], 0),
            ([(1, 1), (-1, 2), (-1, 3), (-1, 4)], -2),
        )
        feasible = all(eval_row(terms, values, rhs) for terms, rhs in rows)
        check(feasible == (inside == mi*mj*edge), "inside truth")
        inside_truths += 1

    guard_truths = 0
    for common in range(9, 14):
        for selector, pair_edge in itertools.product(range(2), repeat=2):
            for missed in range(common + 1):
                for inside in range(missed * (missed - 1) // 2 + 1):
                    active_blue = selector == 1 and pair_edge == 0
                    rows = (
                        (
                            -missed + (common - 5) * pair_edge
                            - (common - 5) * selector
                            >= -common
                        ),
                        (
                            inside - missed + (common - 2) * pair_edge
                            - (common - 2) * selector
                            >= -common
                        ),
                        (
                            inside - 3 * missed + (3 * common - 10) * pair_edge
                            - (3 * common - 10) * selector
                            >= -3 * common
                        ),
                    )
                    expected = (
                        not active_blue or missed <= 5,
                        not active_blue or inside >= missed - 2,
                        not active_blue or inside >= 3 * missed - 10,
                    )
                    check(rows == expected, "guard truth")
                    guard_truths += 3

    sharp = build.sharpness_certificate()
    check([record["e"] for record in sharp["records"]] == [1, 2, 5], "sharp edges")
    check(
        [(record["first_facet_slack"], record["second_facet_slack"])
         for record in sharp["records"]]
        == [(0, 2), (0, 0), (2, 0)],
        "sharp facets",
    )
    certificate = build.root_certificate()
    check(certificate.count(b"\n") == 390, "certificate rows")
    check(
        hashlib.sha256(certificate).hexdigest()
        == "35de5fa4bfdfb756903859bc83caf9f2f096913805b5068def4bf6fd2fb24d67",
        "certificate hash",
    )

    rejected(lambda: build.edge_id(-1, 2))
    rejected(lambda: build.edge_id(2, 2))
    rejected(lambda: build.edge_id(0, 43))
    rejected(lambda: build.opb_row([], 0))
    rejected(lambda: build.root_cells(("E8", 99, 0, "H")))

    print(
        "{"
        f'"guard_row_checks":{guard_truths},'
        f'"inside_truth_assignments":{inside_truths},'
        f'"missed_truth_assignments":{missed_truths},'
        '"negative_controls":5,'
        '"status":"PASS"'
        "}"
    )


if __name__ == "__main__":
    main()
