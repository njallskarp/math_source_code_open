#!/usr/bin/env python3
"""Clean-room audit of the all-order branched-broom separation.

The finite calculation constructs every tree as an adjacency list and obtains
the sibling-leaf potential from the recursive directed deficits

    a(x -> y) = 1                                      if x is a leaf,
                3 + 2 sum_{z~x,z!=y} a(z -> x)         otherwise.

It does not use the producer's closed potential formula, core-distance
formula, weak-composition implementation, or canonical record format.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from math import comb
import sys


FIRST_ORDER = 23
LAST_FINITE_ORDER = 576

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
sys.setrecursionlimit(10_000)


def path_graph(edge_count: int) -> dict[int, set[int]]:
    graph = {v: set() for v in range(edge_count + 1)}
    for v in range(edge_count):
        graph[v].add(v + 1)
        graph[v + 1].add(v)
    return graph


def add_leaf(graph: dict[int, set[int]], parent: int) -> int:
    leaf = len(graph)
    graph[leaf] = {parent}
    graph[parent].add(leaf)
    return leaf


def branched_broom(d: int, e: int, t: int) -> dict[int, set[int]]:
    graph = path_graph(t)
    p, q = 0, t
    for _ in range(d):
        add_leaf(graph, p)
    for _ in range(e):
        arm = add_leaf(graph, q)
        add_leaf(graph, arm)
    return graph


def symmetric_double_broom(a: int, ell: int) -> dict[int, set[int]]:
    graph = path_graph(ell)
    for _ in range(a):
        add_leaf(graph, 0)
        add_leaf(graph, ell)
    return graph


def symmetric_count_via_deficit_recurrence(a: int, ell: int) -> int:
    """Evaluate a symmetric double broom by propagating directed deficits."""
    assert a >= 1 and ell >= 1
    incoming = 2 * a + 3
    for _ in range(ell - 1):
        incoming = 3 + 2 * incoming
    leaf_h = 3 + 2 * ((a - 1) + incoming)
    assert leaf_h % 2 == 1
    excess = (leaf_h - 1) // 2
    return 2 * comb(excess + a - 1, a - 1)


def critical_count(graph: dict[int, set[int]]) -> tuple[int, list[tuple[int, int, int]]]:
    """Return N(T) and the maximizing (parent, leaf count, X) classes."""

    @lru_cache(maxsize=None)
    def deficit(x: int, parent: int) -> int:
        children = graph[x] - {parent}
        if not children:
            return 1
        return 3 + 2 * sum(deficit(child, x) for child in children)

    leaves = [v for v, neighbors in graph.items() if len(neighbors) == 1]
    by_parent: dict[int, list[int]] = defaultdict(list)
    leaf_h: dict[int, int] = {}
    for leaf in leaves:
        parent = next(iter(graph[leaf]))
        by_parent[parent].append(leaf)
        leaf_h[leaf] = sum(deficit(neighbor, leaf) for neighbor in graph[leaf])

    maximum_h = max(leaf_h.values())
    classes: list[tuple[int, int, int]] = []
    total = 0
    for parent, siblings in sorted(by_parent.items()):
        representative = siblings[0]
        if leaf_h[representative] != maximum_h:
            continue
        assert all(leaf_h[z] == maximum_h for z in siblings)
        assert maximum_h % 2 == 1
        excess = (maximum_h - 1) // 2
        width = len(siblings)
        classes.append((parent, width, excess))
        total += comb(excess + width - 1, width - 1)
    return total, classes


def witness_parameters(n: int) -> tuple[int, int, int]:
    if n <= 32:
        d, e = 8, 4
    elif n <= 36:
        d, e = 10, 5
    else:
        m = (n - 1) // 18
        d, e = 5 * m + 3, 2 * m + 2
    return d, e, n - d - 2 * e - 1


def finite_audit() -> dict[str, int | str]:
    digest = sha256()
    minimum_margin: int | None = None
    minimum_order: int | None = None
    final: dict[str, int] | None = None

    for n in range(FIRST_ORDER, LAST_FINITE_ORDER + 1):
        d, e, t = witness_parameters(n)
        candidate_graph = branched_broom(d, e, t)
        assert len(candidate_graph) == n
        candidate, candidate_classes = critical_count(candidate_graph)
        assert len(candidate_classes) == 1
        assert candidate_classes[0][1] == d

        alternatives: list[tuple[int, int, int]] = []
        for a in range(1, (n - 2) // 2 + 1):
            ell = n - 2 * a - 1
            value = symmetric_count_via_deficit_recurrence(a, ell)
            if n <= 40 or (n in {100, 250, 576} and a in {1, (n - 2) // 4}):
                graph = symmetric_double_broom(a, ell)
                assert len(graph) == n
                direct_value, classes = critical_count(graph)
                assert direct_value == value
                assert len(classes) == 2
                assert all(width == a for _, width, _ in classes)
            alternatives.append((value, a, ell))

        best_value, best_a, best_ell = max(alternatives)
        margin = candidate - best_value
        assert margin > 0
        if minimum_margin is None or margin < minimum_margin:
            minimum_margin, minimum_order = margin, n

        record = "|".join(
            str(value)
            for value in (
                n,
                d,
                e,
                t,
                candidate,
                best_a,
                best_ell,
                best_value,
                margin,
            )
        )
        digest.update(record.encode("ascii") + b"\n")
        final = {
            "candidate_bits": candidate.bit_length(),
            "best_bits": best_value.bit_length(),
            "best_a": best_a,
            "d": d,
            "e": e,
            "t": t,
        }

    assert minimum_margin is not None
    assert minimum_order is not None
    assert final is not None
    return {
        "orders_checked": LAST_FINITE_ORDER - FIRST_ORDER + 1,
        "minimum_margin_order": minimum_order,
        "minimum_margin": minimum_margin,
        "order_576_best_a": final["best_a"],
        "order_576_best_bits": final["best_bits"],
        "order_576_candidate_bits": final["candidate_bits"],
        "order_576_d": final["d"],
        "order_576_e": final["e"],
        "order_576_t": final["t"],
        "independent_record_sha256": digest.hexdigest(),
    }


def analytic_audit() -> dict[str, int | str]:
    assert 891**3 < 2**32
    assert 34**3 < 2 * 33**3

    def tail_gap(m: int) -> Fraction:
        lower = 45 * m * m - 12 * m - 12
        upper = 1 + Fraction(1, 8) * (Fraction(55, 3) * m + 15) ** 2
        return lower - upper

    gap_32 = tail_gap(32)
    delta_32 = tail_gap(33) - tail_gap(32)
    second_delta = tail_gap(34) - 2 * tail_gap(33) + tail_gap(32)
    assert gap_32 == Fraction(31151, 72)
    assert delta_32 > 0
    assert second_delta == Fraction(215, 36) > 0

    assert (5 + 2 * 2 + 9, 3 + 2 * 2 - 7 + 1) == (18, 1)
    assert (9 * 5, 9 * 2 - 6 * 5, -6 * 2) == (45, -12, -12)
    assert Fraction(5, 36) - Fraction(1, 8) == Fraction(1, 72)
    assert max(3 - 3 * d for d in range(2, 50)) < 0

    return {
        "tail_gap_m32": f"{gap_32.numerator}/{gap_32.denominator}",
        "tail_first_increment": f"{delta_32.numerator}/{delta_32.denominator}",
        "tail_second_difference": (
            f"{second_delta.numerator}/{second_delta.denominator}"
        ),
        "quadratic_advantage": "1/72",
    }


def main() -> None:
    for key, value in finite_audit().items():
        print(f"{key}={value}")
    for key, value in analytic_audit().items():
        print(f"{key}={value}")
    print("status=VERIFIED")


if __name__ == "__main__":
    main()
