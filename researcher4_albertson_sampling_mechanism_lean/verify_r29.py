#!/usr/bin/env python3
"""Exact checker for the bounded order-57, r=29 recurrence gate."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from verify import (
    ceil_fraction,
    deletion_edge_threshold,
    deletion_fraction,
    recursive_closure,
)


ROOT = Path(__file__).resolve().parent

if not __debug__:
    raise RuntimeError("certificate checks require Python without -O")


def fraction_field(value: list[int]) -> Fraction:
    assert isinstance(value, list) and len(value) == 2
    assert all(isinstance(term, int) for term in value)
    assert value[1] > 0
    return Fraction(value[0], value[1])


def main() -> None:
    certificate = json.loads((ROOT / "r29_certificate.json").read_bytes())
    assert certificate["schema_version"] == 1
    parameters = certificate["parameters"]
    assert parameters == {
        "chromatic_number": 29,
        "order": 57,
        "comparison": 8281,
        "critical_edge_floor": 824,
        "recurrence_threshold": 829,
    }

    table_spec = certificate["recursive_table"]
    tables, _, digests = recursive_closure(table_spec["maximum_order"])
    assert digests[57] == table_spec["sha256"]
    for checkpoint in table_spec["checkpoints"]:
        assert digests[checkpoint["maximum_order"]] == checkpoint["sha256"]

    supports = certificate["supports"]
    for support in supports.values():
        assert support["source_order"] == 56
        assert support["maximum_edges"] == 1540
        assert support["scale"] > 0
        table = tables[56]
        for edges, value in enumerate(table):
            assert support["slope"] * edges <= (
                support["scale"] * value + support["intercept"]
            )
        for endpoint, value in zip(
            (support["left"], support["right"]),
            support["endpoint_values"],
            strict=True,
        ):
            assert table[endpoint] == value
            assert support["slope"] * endpoint == (
                support["scale"] * value + support["intercept"]
            )
        assert deletion_edge_threshold(
            57,
            support["slope"],
            support["intercept"],
            support["scale"],
            parameters["comparison"],
        ) == parameters["recurrence_threshold"]

    checked: list[str] = []
    for row in certificate["rows"]:
        edges = row["edges"]
        support = supports[row["support"]]
        mean = Fraction(edges * 55, 57)
        assert mean == fraction_field(row["mean"])
        assert support["left"] <= mean <= support["right"]
        bound = deletion_fraction(
            57,
            edges,
            support["slope"],
            support["intercept"],
            support["scale"],
        )
        assert bound == fraction_field(row["bound"])
        assert ceil_fraction(bound) == row["ceiling"]
        assert tables[57][edges] == row["ceiling"]
        if edges < parameters["recurrence_threshold"]:
            assert parameters["comparison"] - row["ceiling"] == row["comparison_gap"]
        else:
            assert row["ceiling"] - parameters["comparison"] == row["comparison_surplus"]
        checked.append(f"{edges}:{bound}:{row['ceiling']}")

    r = parameters["chromatic_number"]
    n = parameters["order"]
    edge_floor = ceil_fraction(Fraction((r - 1) * n + (2 * r - 6), 2))
    assert edge_floor == parameters["critical_edge_floor"]
    first_table_edge = next(
        edges
        for edges, value in enumerate(tables[57])
        if value >= parameters["comparison"]
    )
    assert first_table_edge == parameters["recurrence_threshold"]
    open_rows = list(range(edge_floor, first_table_edge))
    assert open_rows == [824, 825, 826, 827, 828]

    evidence = "\n".join(checked + [f"open:{','.join(map(str, open_rows))}"])
    evidence_digest = sha256(evidence.encode("ascii")).hexdigest()
    print("PASS r=29 order-57 recurrence feasibility gate")
    print(f"recursive_table_order57_sha256={digests[57]}")
    for row in certificate["rows"]:
        comparison = (
            f"gap={row['comparison_gap']}"
            if "comparison_gap" in row
            else f"surplus={row['comparison_surplus']}"
        )
        print(
            f"m={row['edges']}: bound={fraction_field(row['bound'])}; "
            f"ceiling={row['ceiling']}; {comparison}"
        )
    print("open_rows=824,825,826,827,828")
    print("first_recurrence_closure_edge=829")
    print(f"checked_evidence_sha256={evidence_digest}")


if __name__ == "__main__":
    main()
