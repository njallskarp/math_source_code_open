#!/usr/bin/env python3
"""Independent exhaustive audit of the missing-edge deletion threshold.

This checker uses only Python's standard library.  It does not import the
reviewed Lean project or its tests.  Graphs are labelled finite simple graphs.
"""

from itertools import combinations
from math import comb


MAX_N = 6


def predecessor_capacity(t: int) -> int:
    """Lean's `(t - 1).choose 2`, including natural-number subtraction."""

    return comb(max(t - 1, 0), 2)


def threshold(f: int) -> int:
    """Least support size whose pair capacity can contain f positive edges."""

    assert f > 0
    s = 0
    while comb(s, 2) < f:
        s += 1
    return s


def main() -> None:
    graph_count = 0
    premise_count = 0
    characterization_count = 0
    exact_min_support = [None] * (comb(MAX_N, 2) + 1)
    equality_witness = None

    for n in range(MAX_N + 1):
        edges = list(combinations(range(n), 2))
        max_edges = len(edges)
        for mask in range(1 << max_edges):
            graph_count += 1
            degrees = [0] * n
            m = mask.bit_count()
            for bit, (u, v) in enumerate(edges):
                if mask >> bit & 1:
                    degrees[u] += 1
                    degrees[v] += 1

            support = sum(degree > 0 for degree in degrees)
            if n == MAX_N:
                previous = exact_min_support[m]
                if previous is None or support < previous:
                    exact_min_support[m] = support

            # Budgets above the complete-graph capacity add no new behavior:
            # once m < f, every deletion is automatically improved.
            for f in range(m, max_edges + 2):
                improved = sum(m - degree <= max(f - 1, 0) for degree in degrees)

                if f > 0:
                    expected = n if m < f else support
                    assert improved == expected, (n, mask, m, f, improved, expected)
                    characterization_count += 1

                for t in range(n + 1):
                    if predecessor_capacity(t) < f:
                        premise_count += 1
                        assert improved >= t, (n, mask, m, f, t, improved)

                    if (
                        equality_witness is None
                        and predecessor_capacity(t) == f
                        and improved < t
                    ):
                        equality_witness = (n, mask, m, f, t, improved)

    assert equality_witness == (3, 1, 1, 1, 3, 2)

    for f in range(1, len(exact_min_support)):
        assert exact_min_support[f] == threshold(f), (
            f,
            exact_min_support[f],
            threshold(f),
        )

    print(f"labelled_graphs_n_le_{MAX_N}={graph_count}")
    print(f"checked_theorem_premises={premise_count}")
    print(f"checked_exact_characterizations={characterization_count}")
    print("minimum_support_at_exact_budget=" + ",".join(
        f"{f}:{exact_min_support[f]}" for f in range(1, len(exact_min_support))
    ))
    n, mask, m, f, t, improved = equality_witness
    print(
        "strict_gap_counterexample="
        f"n:{n},mask:{mask},edges:{m},budget:{f},t:{t},improved:{improved}"
    )
    print("status=PASS")


if __name__ == "__main__":
    main()
