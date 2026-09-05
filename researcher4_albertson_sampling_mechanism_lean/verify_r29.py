#!/usr/bin/env python3
"""Exact checker for the bounded orders 56--59, r=29 recurrence gate."""

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


def critical_edge_floor(r: int, n: int) -> int:
    return ceil_fraction(Fraction((r - 1) * n + (2 * r - 6), 2))


def disconnected_complement_edge_floor(r: int, n: int) -> int:
    first_branch = (
        (n - 1)
        + ceil_fraction(Fraction((r - 2) * (n - 1), 2))
        + (r - 4)
    )
    return min(first_branch, r * r + 3 * r - 19)


def main() -> None:
    certificate = json.loads((ROOT / "r29_certificate.json").read_bytes())
    assert certificate["schema_version"] == 2
    parameters = certificate["parameters"]
    assert parameters["chromatic_number"] == 29
    assert parameters["comparison"] == 8281

    table_spec = certificate["recursive_table"]
    assert table_spec["maximum_order"] == 59
    tables, _, digests = recursive_closure(table_spec["maximum_order"])
    assert digests[59] == table_spec["sha256"]
    for checkpoint in table_spec["checkpoints"]:
        assert digests[checkpoint["maximum_order"]] == checkpoint["sha256"]

    thresholds = {
        int(order): value
        for order, value in parameters["recurrence_thresholds"].items()
    }
    supports = certificate["supports"]
    for support in supports.values():
        source_order = support["source_order"]
        target_order = support["target_order"]
        assert target_order == source_order + 1
        assert support["maximum_edges"] == source_order * (source_order - 1) // 2
        assert support["scale"] > 0 and support["slope"] > 0
        table = tables[source_order]
        assert len(table) == support["maximum_edges"] + 1
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
            target_order,
            support["slope"],
            support["intercept"],
            support["scale"],
            parameters["comparison"],
        ) == thresholds[target_order]

    checked: list[str] = []
    seen_rows: set[tuple[int, int]] = set()
    for row in certificate["rows"]:
        target_order = row["target_order"]
        edges = row["edges"]
        support = supports[row["support"]]
        assert support["target_order"] == target_order
        assert (target_order, edges) not in seen_rows
        seen_rows.add((target_order, edges))
        mean = Fraction(edges * (target_order - 2), target_order)
        assert mean == fraction_field(row["mean"])
        assert support["left"] <= mean <= support["right"]
        bound = deletion_fraction(
            target_order,
            edges,
            support["slope"],
            support["intercept"],
            support["scale"],
        )
        assert bound == fraction_field(row["bound"])
        assert ceil_fraction(bound) == row["ceiling"]
        assert tables[target_order][edges] == row["ceiling"]
        if edges < thresholds[target_order]:
            assert parameters["comparison"] - row["ceiling"] == row["comparison_gap"]
            comparison = f"gap={row['comparison_gap']}"
        else:
            assert row["ceiling"] - parameters["comparison"] == row["comparison_surplus"]
            comparison = f"surplus={row['comparison_surplus']}"
        checked.append(
            f"n={target_order},m={edges},support={row['support']},"
            f"bound={bound},ceiling={row['ceiling']},{comparison},role={row['role']}"
        )

    r = parameters["chromatic_number"]
    candidate_floors = {
        int(order): value
        for order, value in parameters["candidate_edge_floors"].items()
    }
    disconnected_floors = {
        int(order): value
        for order, value in parameters["disconnected_complement_edge_floors"].items()
    }
    expected_open = {
        int(order): value
        for order, value in certificate["expected_open_rows"].items()
    }
    for order in range(56, 60):
        assert critical_edge_floor(r, order) == candidate_floors[order]
        first_table_edge = next(
            edges
            for edges, value in enumerate(tables[order])
            if value >= parameters["comparison"]
        )
        assert first_table_edge == thresholds[order]
        assert list(range(candidate_floors[order], first_table_edge)) == expected_open[order]
    for order, value in disconnected_floors.items():
        assert disconnected_complement_edge_floor(r, order) == value
        assert tables[order][value] >= parameters["comparison"]
        assert (order, value) in seen_rows

    evidence = "\n".join(
        checked
        + [
            f"open-n{order}:{','.join(map(str, expected_open[order]))}"
            for order in range(56, 60)
        ]
    )
    evidence_digest = sha256(evidence.encode("ascii")).hexdigest()
    print("PASS r=29 orders-56--59 recurrence feasibility gate")
    for order in range(56, 60):
        print(f"recursive_table_order{order}_sha256={digests[order]}")
    for line in checked:
        print(line)
    for order in range(56, 60):
        rows = ",".join(map(str, expected_open[order])) or "none"
        print(f"order{order}_open_rows={rows}")
        print(f"order{order}_first_recurrence_closure_edge={thresholds[order]}")
    print(f"checked_evidence_sha256={evidence_digest}")


if __name__ == "__main__":
    main()
