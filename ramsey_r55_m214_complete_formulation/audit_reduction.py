#!/usr/bin/env python3
"""Definition-level checks for the mathematical bridge behind the OPB system."""

from __future__ import annotations

import itertools


def bit_index(n: int, i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    return i * (2 * n - i - 1) // 2 + (j - i - 1)


def edge(mask: int, n: int, i: int, j: int) -> int:
    return (mask >> bit_index(n, i, j)) & 1


def audit_degree_neighborhood_identity() -> tuple[int, int]:
    graphs = 0
    vertex_checks = 0
    for n in range(7):
        pairs = n * (n - 1) // 2
        for mask in range(1 << pairs):
            graphs += 1
            degrees = [sum(edge(mask, n, v, w) for w in range(n) if w != v) for v in range(n)]
            red_edges = sum(degrees) // 2
            for v in range(n):
                red_neighbors = [w for w in range(n) if w != v and edge(mask, n, v, w)]
                blue_neighbors = [w for w in range(n) if w != v and not edge(mask, n, v, w)]
                t_red = sum(edge(mask, n, i, j) for i, j in itertools.combinations(red_neighbors, 2))
                t_blue = sum(1 - edge(mask, n, i, j) for i, j in itertools.combinations(blue_neighbors, 2))
                rhs = (
                    len(blue_neighbors) * (len(blue_neighbors) - 1) // 2
                    - red_edges
                    + sum(degrees[w] for w in red_neighbors)
                )
                assert t_red + t_blue == rhs
                vertex_checks += 1
    return graphs, vertex_checks


def audit_branch_arithmetic() -> tuple[int, int, int, int, int]:
    degree_sum = 13 * 20 + 30 * 21
    assert degree_sum == 890
    red_edges = degree_sum // 2
    assert red_edges == 445

    # The height-2099 identity specialized to this degree sequence.
    total_deficiency_twice = 1247 - 3 * 13
    assert total_deficiency_twice == 1208
    total_deficiency = total_deficiency_twice // 2
    assert total_deficiency == 604
    baseline_deficiency = 2 * 43 * 7
    assert total_deficiency - baseline_deficiency == 2
    assert total_deficiency_twice - 2 * baseline_deficiency == 4

    red_baseline_edges = 13 * (100 - 7) + 30 * (107 - 7)
    assert red_baseline_edges == 4209
    possible_red_excess = [e for e in range(3) if (red_baseline_edges - e) % 3 == 0]
    assert possible_red_excess == [0]
    red_triangles = red_baseline_edges // 3
    assert red_triangles == 1403

    blue_baseline_edges = 13 * (114 - 7) + 30 * (107 - 7)
    assert blue_baseline_edges == 4391
    blue_excess = 2
    assert (blue_baseline_edges - blue_excess) % 3 == 0
    blue_triangles = (blue_baseline_edges - blue_excess) // 3
    assert blue_triangles == 1463
    return red_edges, total_deficiency, red_triangles, blue_triangles, blue_excess


def audit_exceptional_incidence_and_anchors() -> tuple[int, int, int, int]:
    incidence = 13 * 20
    baseline = 43 * 6
    surplus = incidence - baseline
    assert (incidence, baseline, surplus) == (260, 258, 2)

    # Enumerate all placements of the two indistinguishable excess units.
    observed = set()
    for first in range(43):
        for second in range(first, 43):
            a = [6] * 43
            a[first] += 1
            a[second] += 1
            exact_central = sum(a[v] == 6 for v in range(13, 43))
            observed.add(exact_central)
    assert observed == {28, 29, 30}
    return incidence, surplus, min(observed), max(observed)


def audit_anchor_normalization() -> tuple[int, int, int, int, int]:
    # Choose one exact central vertex and relabel within degree classes.
    red_exceptional = set(range(6))
    red_central = set(range(14, 29))
    assert len(red_exceptional) == 6
    assert len(red_central) == 15
    assert len(set(range(13)) - red_exceptional) == 7
    assert len(set(range(14, 43)) - red_central) == 14
    cross_total = 445 - 21 - 100 - (210 - 100)
    assert cross_total == 214
    return 6, 15, 7, 14, cross_total


def turan_k5_edges(n: int) -> int:
    quotient, remainder = divmod(n, 4)
    parts = [quotient + 1] * remainder + [quotient] * (4 - remainder)
    return (n * n - sum(part * part for part in parts)) // 2


def minimum_k5_free_component_order(minimum_degree: int) -> int:
    for order in range(minimum_degree + 1, 44):
        if order * minimum_degree <= 2 * turan_k5_edges(order):
            return order
    raise AssertionError("no component order found")


def audit_backbone_consequences() -> tuple[int, int, int, int, int, int]:
    # At most two of the 30 central vertices are not exact. An exact anchor has
    # 15 central red neighbors and 14 central blue neighbors.
    minimum_red_degree = 15 - 2
    minimum_blue_degree = 14 - 2
    assert (minimum_red_degree, minimum_blue_degree) == (13, 12)

    red_component = minimum_k5_free_component_order(minimum_red_degree)
    blue_component = minimum_k5_free_component_order(minimum_blue_degree)
    assert (red_component, blue_component) == (18, 16)
    assert 2 * red_component > 30 and 2 * blue_component > 30

    # Deleting at most three red vertices or one blue vertex still leaves too
    # few vertices for two K5-free components with the residual minimum degree.
    red_after_three = minimum_k5_free_component_order(minimum_red_degree - 3)
    blue_after_one = minimum_k5_free_component_order(minimum_blue_degree - 1)
    assert (red_after_three, blue_after_one) == (14, 15)
    assert 2 * red_after_three > 30 - 3
    assert 2 * blue_after_one > 30 - 1

    # A geodesic of length six contains three vertices at pairwise distance at
    # least three, whose closed neighborhoods would be disjoint.
    assert 3 * (minimum_red_degree + 1) > 30
    assert 3 * (minimum_blue_degree + 1) > 30
    diameter_bound = 5
    return (
        minimum_red_degree,
        minimum_blue_degree,
        red_component,
        blue_component,
        red_after_three,
        diameter_bound,
    )


def main() -> None:
    graphs, vertex_checks = audit_degree_neighborhood_identity()
    red_edges, deficiency, red_triangles, blue_triangles, blue_excess = audit_branch_arithmetic()
    incidence, surplus, anchors_min, anchors_max = audit_exceptional_incidence_and_anchors()
    ae, ac, be, bc, cross = audit_anchor_normalization()
    min_red, min_blue, red_component, blue_component, red_deleted, diameter = audit_backbone_consequences()
    print(f"PASS identity graphs={graphs} vertex_checks={vertex_checks}")
    print(
        "PASS m214_arithmetic "
        f"red_edges={red_edges} total_deficiency={deficiency} "
        f"red_triangles={red_triangles} blue_triangles={blue_triangles} blue_excess={blue_excess}"
    )
    print(
        "PASS exceptional_incidence "
        f"incidence={incidence} surplus={surplus} exact_anchors={anchors_min}..{anchors_max}"
    )
    print(f"PASS normalized_anchor split={ae}+{ac}/{be}+{bc} cross_total={cross}")
    print(
        "PASS backbone "
        f"min_degrees={min_red}/{min_blue} component_min={red_component}/{blue_component} "
        f"red_after_delete3_min={red_deleted} connectivity>=4/2 diameter<={diameter}"
    )


if __name__ == "__main__":
    main()
