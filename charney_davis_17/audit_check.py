#!/usr/bin/env python3
"""Dependency-free adversarial checks for the frozen Charney--Davis audit.

This program checks finite arithmetic interfaces. It is not a proof of the
published topological inputs and is not independent mathematical acceptance.
"""

from itertools import combinations, product
from random import Random


def edges(n: int) -> list[tuple[int, int]]:
    return list(combinations(range(n), 2))


def graph_data(n: int, mask: int) -> tuple[list[int], int, int]:
    edge_list = edges(n)
    present = {edge_list[i] for i in range(len(edge_list)) if mask >> i & 1}
    degrees = [0] * n
    for u, v in present:
        degrees[u] += 1
        degrees[v] += 1
    triangles = sum(
        (a, b) in present and (a, c) in present and (b, c) in present
        for a, b, c in combinations(range(n), 3)
    )
    complement_triangles = sum(
        (a, b) not in present
        and (a, c) not in present
        and (b, c) not in present
        for a, b, c in combinations(range(n), 3)
    )
    return degrees, triangles, complement_triangles


def check_complement_identity() -> int:
    checked = 0
    for n in range(1, 7):
        for mask in range(1 << len(edges(n))):
            q, triangles_h, triangles_g = graph_data(n, mask)
            m = sum(q) // 2
            rhs = (
                n * (n - 1) * (n - 2) // 6
                - (n - 2) * m
                + sum(x * (x - 1) // 2 for x in q)
                - triangles_h
            )
            assert triangles_g == rhs
            checked += 1
    return checked


def check_gamma_three_identity_samples() -> int:
    n = 17
    edge_count = len(edges(n))
    rng = Random(172025)
    masks = [0, (1 << edge_count) - 1]
    masks.extend(rng.getrandbits(edge_count) for _ in range(256))
    for mask in masks:
        q, triangles_h, triangles_g = graph_data(n, mask)
        m = sum(q) // 2
        graph_edges = n * (n - 1) // 2 - m
        h_three = triangles_g - 4 * graph_edges + 10 * n - 20
        gamma_one = n - 12
        gamma_two = graph_edges - 9 * n + 48
        gamma_three = h_three - 20 - 6 * gamma_one - 2 * gamma_two
        rhs = 348 + sum(x * (x - 10) for x in q) - 2 * triangles_h
        assert 2 * gamma_three == rhs
    return len(masks)


def check_rigid_profile() -> list[tuple[int, int, int, tuple[int, ...]]]:
    survivors: list[tuple[int, int, int, tuple[int, ...]]] = []
    # Count vectors (a3,a4,a5,a6), not labelled 17-tuples.
    for counts in product(range(18), repeat=4):
        if sum(counts) != 17:
            continue
        degree_sum = sum((q + 3) * counts[q] for q in range(4))
        for gamma_two in range(1, 6):
            if degree_sum != 62 - 2 * gamma_two:
                continue
            for gamma_three in range(-6, 0):
                if 3 * gamma_three + 4 * gamma_two < 0:
                    continue
                weighted = sum(
                    counts[q] * (q + 3) * (q - 7) for q in range(4)
                )
                twice_t = 348 + weighted - 2 * gamma_three
                if twice_t >= 0 and twice_t % 2 == 0:
                    survivors.append(
                        (gamma_two, gamma_three, twice_t // 2, counts)
                    )
    expected = [(5, -6, 0, (16, 1, 0, 0))]
    assert survivors == expected
    return survivors


def check_degree_four_link() -> tuple[int, int, int]:
    complement_edges = (62 - 2 * 5) // 2
    edges_inside_b = complement_edges - 4 - 4 * 2
    link_edges = 12 * 11 // 2 - edges_inside_b
    link_gamma_two = link_edges - 7 * 12 + 30
    assert (edges_inside_b, link_edges, link_gamma_two) == (14, 52, -2)
    return edges_inside_b, link_edges, link_gamma_two


def main() -> None:
    graphs = check_complement_identity()
    gamma_samples = check_gamma_three_identity_samples()
    survivors = check_rigid_profile()
    local = check_degree_four_link()
    print(f"complement identity: PASS ({graphs} simple graphs, n <= 6)")
    print(f"gamma3 specialization: PASS ({gamma_samples} deterministic n=17 samples)")
    print(f"rigid integer profile: PASS {survivors[0]}")
    print(f"degree-four link: PASS H[B]={local[0]}, edges={local[1]}, gamma2={local[2]}")
    print("scope: arithmetic self-check only; published topology remains trusted input")


if __name__ == "__main__":
    main()
