#!/usr/bin/env python3
"""Definition-level audit of the Albertson r=27, h=20 split-Hall closure."""

from hashlib import sha256


PALETTE = 26
HIGH_VERTICES = 20

# name, |B|, active classes f, chi(X) values, chi(S), e(X), |S|
CASES = (
    ("D20", 20, 7, (7, 8, 9, 10), 7, 87, 13),
    ("D19", 19, 8, (8,), 8, 75, 14),
)


def exhaustive_hall(block_order: int):
    """Check Hall directly for every labelled subset and split cardinality.

    The two normalized lists have size b-1 and differ by exchanging one
    colour.  A canonical initial segment represents the vertices adjacent to
    the split vertex; every other labelled bipartition is isomorphic to it.
    """
    common = (1 << (block_order - 2)) - 1
    first_list = common | (1 << (block_order - 2))
    second_list = common | (1 << (block_order - 1))
    assert first_list.bit_count() == second_list.bit_count() == block_order - 1
    assert (first_list | second_list).bit_count() == block_order

    subset_checks = 0
    tight_checks = 0
    full_vertices = (1 << block_order) - 1
    records = []
    for split_weight in range(1, block_order):
        first_vertices = (1 << split_weight) - 1
        second_vertices = full_vertices ^ first_vertices
        minimum_slack = block_order
        tight = 0
        for chosen in range(1, full_vertices + 1):
            sees_first = bool(chosen & first_vertices)
            sees_second = bool(chosen & second_vertices)
            if sees_first and sees_second:
                list_union = first_list | second_list
            elif sees_first:
                list_union = first_list
            else:
                list_union = second_list
            slack = list_union.bit_count() - chosen.bit_count()
            assert slack >= 0
            minimum_slack = min(minimum_slack, slack)
            tight += slack == 0
            subset_checks += 1
        assert minimum_slack == 0
        assert tight > 0
        tight_checks += tight
        records.append((split_weight, minimum_slack, tight))

    # Strict intermediate weight is essential: with only one list type, the
    # full b-set has a union of b-1 colours and fails Hall by exactly one.
    endpoint_deficits = []
    for split_weight in (0, block_order):
        only_union = second_list if split_weight == 0 else first_list
        deficit = block_order - only_union.bit_count()
        assert deficit == 1
        endpoint_deficits.append((split_weight, deficit))

    return tuple(records), subset_checks, tight_checks, tuple(endpoint_deficits)


def endpoint_degree_audit(case):
    """Scan all binary incidence masks and audit the terminal degree floor."""
    name, block_order, active, chromatic_values, small_chi, high_edges, outside = case
    palette_rows = []
    for chromatic in chromatic_values:
        unused_after_split = PALETTE - (chromatic + 1)
        assert unused_after_split >= small_chi
        palette_rows.append((chromatic, unused_after_split, unused_after_split - small_chi))

    expected_total = block_order * active
    admissible = 0
    minimum_degree_sum = None
    for mask in range(1 << HIGH_VERTICES):
        full_count = mask.bit_count()
        incidence_total = block_order * full_count
        if incidence_total != expected_total:
            continue
        zero_count = HIGH_VERTICES - full_count
        degree_sum = full_count * (active - 1) + zero_count * (27 - outside)
        minimum_degree_sum = (
            degree_sum if minimum_degree_sum is None else min(minimum_degree_sum, degree_sum)
        )
        admissible += 1

    assert admissible > 0
    assert minimum_degree_sum is not None
    assert minimum_degree_sum > 2 * high_edges
    return (
        name,
        block_order,
        active,
        tuple(palette_rows),
        admissible,
        minimum_degree_sum,
        2 * high_edges,
        minimum_degree_sum - 2 * high_edges,
    )


def main():
    hall_records = []
    hall_subset_checks = 0
    tight_hall_checks = 0
    endpoint_failures = 0
    for block_order in (19, 20):
        records, checked, tight, failures = exhaustive_hall(block_order)
        hall_records.append((block_order, records, failures))
        hall_subset_checks += checked
        tight_hall_checks += tight
        endpoint_failures += len(failures)

    case_records = tuple(endpoint_degree_audit(case) for case in CASES)
    assert tuple((row[0], row[4], row[5], row[6], row[7]) for row in case_records) == (
        ("D20", 77520, 224, 174, 50),
        ("D19", 125970, 212, 150, 62),
    )

    payload = (
        tuple(hall_records),
        hall_subset_checks,
        tight_hall_checks,
        endpoint_failures,
        case_records,
    )
    print("PASS definition-level split-Hall and endpoint-degree audit")
    print(
        f"hall_labelled_subsets={hall_subset_checks}; "
        f"tight_hall_subsets={tight_hall_checks}; endpoint_failures={endpoint_failures}"
    )
    print(f"endpoint_masks_scanned={len(CASES) * (1 << HIGH_VERTICES)}")
    for row in case_records:
        min_palette_slack = min(palette_row[2] for palette_row in row[3])
        print(
            f"{row[0]}: endpoint_vectors={row[4]}; "
            f"min_palette_slack={min_palette_slack}; degree_floor={row[5]}; "
            f"handshake={row[6]}; margin={row[7]}"
        )
    print(f"certificate_sha256={sha256(repr(payload).encode()).hexdigest()}")


if __name__ == "__main__":
    main()
