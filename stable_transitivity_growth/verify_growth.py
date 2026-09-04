#!/usr/bin/env python3
"""Exact finite audit for the stable-transitivity growth theorem."""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations, product


def pairs(n: int) -> tuple[tuple[int, int], ...]:
    return tuple((i, j) for i in range(n) for j in range(i + 1, n))


def order_vectors(n: int) -> tuple[tuple[int, ...], ...]:
    edge_list = pairs(n)
    vectors = set()
    for order in permutations(range(n)):
        position = [0] * n
        for index, vertex in enumerate(order):
            position[vertex] = index
        vectors.add(tuple(int(position[i] < position[j]) for i, j in edge_list))
    return tuple(sorted(vectors))


def sum_vectors(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def ttd_semigroups(n: int, maximum: int) -> list[set[tuple[int, ...]]]:
    vectors = order_vectors(n)
    levels = [{(0,) * len(pairs(n))}]
    for _ in range(maximum):
        levels.append({sum_vectors(x, v) for x in levels[-1] for v in vectors})
    return levels


def cyclic_weight(vector: tuple[int, int, int], degree: int) -> int:
    """Weight on 0->1, 1->2, 2->0 in standard (01,02,12) coordinates."""
    return vector[0] + vector[2] + degree - vector[1]


def m_three(vector: tuple[int, int, int], degree: int) -> int:
    ell = cyclic_weight(vector, degree)
    return max(degree - ell, 0, ell - 2 * degree)


def layer_split(vector: tuple[int, ...], degree: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(int(layer < weight) for weight in vector) for layer in range(degree))


def order_masks(n: int) -> tuple[int, ...]:
    edge_list = pairs(n)
    masks = []
    for order in permutations(range(n)):
        position = [0] * n
        for index, vertex in enumerate(order):
            position[vertex] = index
        masks.append(sum((position[i] < position[j]) << bit for bit, (i, j) in enumerate(edge_list)))
    return tuple(masks)


def min_feedback_by_orders(tournament: int, n: int, masks: tuple[int, ...]) -> int:
    return min((tournament ^ order).bit_count() for order in masks)


def max_forward_by_subset_dp(tournament: int, n: int) -> int:
    edge_list = pairs(n)
    bit_of = {edge: bit for bit, edge in enumerate(edge_list)}

    def beats(left: int, right: int) -> bool:
        if left < right:
            return bool(tournament & (1 << bit_of[(left, right)]))
        return not bool(tournament & (1 << bit_of[(right, left)]))

    dp = [0] * (1 << n)
    for subset in range(1, 1 << n):
        best = 0
        for first in range(n):
            if subset & (1 << first):
                rest = subset ^ (1 << first)
                forward = sum(
                    beats(first, other)
                    for other in range(n)
                    if rest & (1 << other)
                )
                best = max(best, dp[rest] + forward)
        dp[subset] = best
    return dp[-1]


def main() -> None:
    rows: list[str] = []

    vectors3 = order_vectors(3)
    assert len(vectors3) == 6
    assert {cyclic_weight(v, 1) for v in vectors3} == {1, 2}
    cycle = (1, 0, 1)
    added = (1, 1, 0)
    right_one = (1, 1, 1)
    right_two = (1, 0, 0)
    assert all(v in vectors3 for v in (added, right_one, right_two))
    assert sum_vectors(cycle, added) == sum_vectors(right_one, right_two)
    row = "triangle_orders=6 cycle_identity=yes"
    print(row)
    rows.append(row)

    maximum_degree = 12
    levels = ttd_semigroups(3, 2 * maximum_degree)
    semigroup_points = 0
    for degree in range(maximum_degree + 1):
        expected = {
            vector
            for vector in product(range(degree + 1), repeat=3)
            if degree <= cyclic_weight(vector, degree) <= 2 * degree
        }
        assert levels[degree] == expected
        semigroup_points += len(expected)
    for degree in range(1, maximum_degree + 1):
        assert max(m_three(vector, degree) for vector in product(range(degree + 1), repeat=3)) == degree
        for vector in product(range(degree + 1), repeat=3):
            layers = layer_split(vector, degree)
            assert len(layers) == degree
            assert all(all(bit in (0, 1) for bit in layer) for layer in layers)
            assert tuple(sum(layer[e] for layer in layers) for e in range(3)) == vector
    row = f"three_vertex_semigroup_degrees=0..{maximum_degree} points={semigroup_points} max_m_equals_k=yes"
    print(row)
    rows.append(row)

    subadditivity_cases = 0
    for degree_left in range(1, 5):
        for degree_right in range(1, 5):
            for left in product(range(degree_left + 1), repeat=3):
                for right in product(range(degree_right + 1), repeat=3):
                    total = sum_vectors(left, right)
                    assert m_three(total, degree_left + degree_right) <= m_three(left, degree_left) + m_three(right, degree_right)
                    subadditivity_cases += 1
    row = f"three_vertex_subadditivity_cases={subadditivity_cases}"
    print(row)
    rows.append(row)

    worst_feedback: list[int] = []
    tournament_count = 0
    for n in range(2, 7):
        edge_count = len(pairs(n))
        masks = order_masks(n)
        worst = 0
        for tournament in range(1 << edge_count):
            via_orders = min_feedback_by_orders(tournament, n, masks)
            via_dp = edge_count - max_forward_by_subset_dp(tournament, n)
            assert via_orders == via_dp
            worst = max(worst, via_orders)
            tournament_count += 1
        worst_feedback.append(worst)
        assert worst <= ((n - 1) ** 2) // 4
    row = f"feedback_audit_n=2..6 tournaments={tournament_count} worst={','.join(map(str,worst_feedback))} independent_dp=agree"
    print(row)
    rows.append(row)

    for n in range(2, 101):
        greedy_forward = sum((j + 1) // 2 for j in range(1, n))
        assert greedy_forward == (n * n) // 4
        assert n * (n - 1) // 2 - greedy_forward == ((n - 1) ** 2) // 4
    row = "greedy_identity_n=2..100 verified"
    print(row)
    rows.append(row)

    digest = sha256("\n".join(rows).encode()).hexdigest()
    print(f"audit_sha256={digest}")


if __name__ == "__main__":
    main()
