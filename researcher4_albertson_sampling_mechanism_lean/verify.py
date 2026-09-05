#!/usr/bin/env python3
"""Independent exact checker for sparse Albertson sampling certificates."""

from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parent

if not __debug__:
    raise RuntimeError("certificate checks require Python without -O")


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


UNIVERSAL_LINES = (
    (Fraction(1), Fraction(3)),
    (Fraction(7, 3), Fraction(25, 3)),
    (Fraction(37, 9), Fraction(155, 9)),
    (Fraction(5), Fraction(203, 9)),
)


def base_bound(order: int, edges: int) -> int:
    return max(
        [0]
        + [
            ceil_fraction(slope * edges - intercept * (order - 2))
            for slope, intercept in UNIVERSAL_LINES
        ]
    )


def lower_hull(values: list[int]) -> list[tuple[int, int]]:
    hull: list[tuple[int, int]] = []
    for point in enumerate(values):
        while len(hull) >= 2:
            x0, y0 = hull[-2]
            x1, y1 = hull[-1]
            x2, y2 = point
            if Fraction(y1 - y0, x1 - x0) >= Fraction(y2 - y1, x2 - x1):
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


def hull_value(hull: list[tuple[int, int]], x: Fraction) -> Fraction:
    positions = [point[0] for point in hull]
    index = bisect_right(positions, x) - 1
    if index == len(hull) - 1 or x == hull[index][0]:
        return Fraction(hull[index][1])
    x0, y0 = hull[index]
    x1, y1 = hull[index + 1]
    return y0 + (x - x0) * Fraction(y1 - y0, x1 - x0)


def sampled_fraction(
    target_order: int,
    sample_order: int,
    target_edges: int,
    slope: int,
    intercept: int,
    scale: int,
) -> Fraction:
    numerator = (
        slope * target_edges * comb(target_order - 2, sample_order - 2)
        - intercept * comb(target_order, sample_order)
    )
    denominator = scale * comb(target_order - 4, sample_order - 4)
    return Fraction(numerator, denominator)


def deletion_fraction(
    target_order: int,
    target_edges: int,
    slope: int,
    intercept: int,
    scale: int,
) -> Fraction:
    return Fraction(
        slope * target_edges * (target_order - 2) - intercept * target_order,
        scale * (target_order - 4),
    )


def deletion_edge_threshold(
    target_order: int,
    slope: int,
    intercept: int,
    scale: int,
    target: int,
) -> int:
    """Least edge count whose natural-number deletion ceiling reaches target."""
    assert target_order > 4 and slope > 0 and scale > 0 and target > 0
    numerator = (
        intercept * target_order
        + scale * (target_order - 4) * (target - 1)
        + 1
    )
    denominator = slope * (target_order - 2)
    return ceil_fraction(Fraction(numerator, denominator))


def recursive_closure(maximum_order: int):
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[tuple[int, int]]] = {}
    digests: dict[int, str] = {}
    digest = sha256()
    for order in range(4, maximum_order + 1):
        values = []
        for edges in range(comb(order, 2) + 1):
            value = base_bound(order, edges)
            for sample_order in range(4, order):
                mean = Fraction(
                    edges * sample_order * (sample_order - 1),
                    order * (order - 1),
                )
                candidate = ceil_fraction(
                    Fraction(comb(order, sample_order), comb(order - 4, sample_order - 4))
                    * hull_value(hulls[sample_order], mean)
                )
                value = max(value, candidate)
            values.append(value)
            digest.update(f"{order}:{edges}:{value}\n".encode("ascii"))
        tables[order] = values
        hulls[order] = lower_hull(values)
        digests[order] = digest.hexdigest()
    return tables, hulls, digests


def fraction_field(data: list[int]) -> Fraction:
    assert isinstance(data, list) and len(data) == 2
    assert all(isinstance(value, int) for value in data)
    assert data[1] > 0
    return Fraction(data[0], data[1])


def run_self_tests() -> None:
    assert ceil_fraction(Fraction(3, 2)) == 2
    assert ceil_fraction(Fraction(-1, 2)) == 0
    test_hull = lower_hull([0, 2, 3])
    assert test_hull == [(0, 0), (2, 3)]
    assert hull_value(test_hull, Fraction(1)) == Fraction(3, 2)
    # Independent finite audit of the parameterized Lean threshold theorem.
    for order in range(5, 10):
        for slope in range(1, 4):
            for intercept in range(6):
                for scale in range(1, 4):
                    for target in range(1, 10):
                        threshold = deletion_edge_threshold(
                            order, slope, intercept, scale, target
                        )
                        for edges in range(threshold + 3):
                            numerator = max(
                                0,
                                slope * edges * (order - 2) - intercept * order,
                            )
                            bound = ceil_fraction(
                                Fraction(numerator, scale * (order - 4))
                            )
                            assert (threshold <= edges) == (target <= bound)


def main() -> None:
    run_self_tests()
    certificate_bytes = (ROOT / "certificate.json").read_bytes()
    certificate = json.loads(certificate_bytes)
    assert certificate["schema_version"] == 2

    table_spec = certificate["recursive_table"]
    tables, _, table_digests = recursive_closure(table_spec["maximum_order"])
    table_digest = table_digests[table_spec["maximum_order"]]
    assert table_digest == table_spec["sha256"]
    for checkpoint in table_spec["checkpoints"]:
        assert table_digests[checkpoint["maximum_order"]] == checkpoint["sha256"]

    supports = certificate["supports"]
    for support in supports.values():
        assert support["scale"] > 0
        assert 0 <= support["left"] <= support["right"] <= support["maximum_edges"]
        table = tables[support["source_order"]]
        assert len(table) == support["maximum_edges"] + 1
        for edges, value in enumerate(table):
            assert support["slope"] * edges <= (
                support["scale"] * value + support["intercept"]
            )
        assert len(support["endpoint_values"]) == 2
        for endpoint, expected_value in zip(
            (support["left"], support["right"]),
            support["endpoint_values"],
        ):
            assert table[endpoint] == expected_value
            assert support["slope"] * endpoint == (
                support["scale"] * table[endpoint] + support["intercept"]
            )

    checked = []
    for step in certificate["sampling_steps"]:
        support = supports[step["support"]]
        mean = Fraction(
            step["target_edges"] * step["sample_order"] * (step["sample_order"] - 1),
            step["target_order"] * (step["target_order"] - 1),
        )
        assert mean == fraction_field(step["mean"])
        assert support["left"] <= mean <= support["right"]
        bound = sampled_fraction(
            step["target_order"],
            step["sample_order"],
            step["target_edges"],
            support["slope"],
            support["intercept"],
            support["scale"],
        )
        assert bound == fraction_field(step["bound"])
        assert ceil_fraction(bound) == step["ceiling"]
        if "baseline_ceiling" in step:
            assert step["ceiling"] - step["baseline_ceiling"] == step["gain"]
        if "comparison_threshold" in step:
            assert (
                step["ceiling"] >= step["comparison_threshold"]
            ) == step["meets_threshold"]
        checked.append((step["name"], str(bound), step["ceiling"]))

    for step in certificate["deletion_steps"]:
        support = supports[step["support"]]
        mean = Fraction(
            step["target_edges"] * (step["target_order"] - 2),
            step["target_order"],
        )
        assert mean == fraction_field(step["mean"])
        assert support["left"] <= mean <= support["right"]
        bound = deletion_fraction(
            step["target_order"],
            step["target_edges"],
            support["slope"],
            support["intercept"],
            support["scale"],
        )
        assert bound == fraction_field(step["bound"])
        assert ceil_fraction(bound) == step["ceiling"]
        checked.append((step["name"], str(bound), step["ceiling"]))

    direct_rows = certificate["integer_aware_direct_steps"]
    for step in direct_rows:
        local_floor = (
            step["intercept_numerator"] * (step["sample_order"] - 2)
            // step["intercept_denominator"]
        )
        assert local_floor == step["local_floor"]
        bound = sampled_fraction(
            step["target_order"],
            step["sample_order"],
            step["target_edges"],
            step["slope"],
            local_floor,
            1,
        )
        assert bound == fraction_field(step["bound"])
        assert ceil_fraction(bound) == step["ceiling"]
        checked.append((step["name"], str(bound), step["ceiling"]))

    for step in direct_rows:
        if not step["name"].startswith("r28_"):
            continue
        candidates = []
        for sample_order in range(4, step["target_order"] + 1):
            local_floor = (
                step["intercept_numerator"] * (sample_order - 2)
                // step["intercept_denominator"]
            )
            candidates.append(
                (
                    sampled_fraction(
                        step["target_order"],
                        sample_order,
                        step["target_edges"],
                        step["slope"],
                        local_floor,
                        1,
                    ),
                    sample_order,
                )
            )
        best_bound, best_order = max(candidates)
        assert best_order == step["sample_order"]
        assert best_bound == fraction_field(step["bound"])

    threshold_checks = []
    for diagnostic in certificate["threshold_diagnostics"]:
        table = tables[diagnostic["order"]]
        threshold = diagnostic["comparison_threshold"]
        first_edges = next(
            edges for edges, value in enumerate(table) if value >= threshold
        )
        assert first_edges == diagnostic["first_edges"]
        support = supports[diagnostic["support"]]
        affine_threshold = deletion_edge_threshold(
            diagnostic["order"],
            support["slope"],
            support["intercept"],
            support["scale"],
            threshold,
        )
        assert affine_threshold == diagnostic["affine_threshold"]
        assert affine_threshold == first_edges
        assert [
            [edges, table[edges]] for edges, _ in diagnostic["window"]
        ] == diagnostic["window"]
        threshold_checks.append(
            (diagnostic["name"], first_edges, table[first_edges])
        )

    result_digest = sha256(
        json.dumps(
            {"steps": checked, "thresholds": threshold_checks},
            separators=(",", ":"),
            sort_keys=True,
        ).encode("ascii")
    ).hexdigest()
    print("PASS sparse affine sampling certificate")
    print(f"recursive_table_sha256={table_digest}")
    for checkpoint in table_spec["checkpoints"]:
        print(
            f"recursive_table_order{checkpoint['maximum_order']}_sha256="
            f"{checkpoint['sha256']}"
        )
    for name, bound, ceiling in checked:
        print(f"{name}: bound={bound}; ceiling={ceiling}")
    for name, first_edges, value in threshold_checks:
        print(f"{name}: first_edges={first_edges}; value={value}")
    print(f"checked_results_sha256={result_digest}")


if __name__ == "__main__":
    main()
