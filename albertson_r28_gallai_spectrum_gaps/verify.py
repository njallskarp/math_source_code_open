#!/usr/bin/env python3
"""Exact checker for the Gallai spectrum gaps closing the r=28 row 769."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations


def edge(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def clique_edges(increment: int) -> int:
    """Edges in K_(increment+1)."""
    return increment * (increment + 1) // 2


def block_spectrum(n: int) -> dict[int, tuple[int, bool, tuple[tuple[str, int, int], ...]]]:
    """Relaxed Gallai-forest edge spectrum on n vertices.

    If a forest has c components and block increments u_B=|B|-1, then
    sum_B u_B=n-c<=n-1.  We allow arbitrary multisets satisfying only this
    identity, clique increments at most 25, at most one clique increment 25,
    and arbitrary odd-cycle blocks.  This is a relaxation of block-tree and
    degree realizability, so a missing edge count is a rigorous obstruction.
    """

    block_types = [
        ("K", u, clique_edges(u), u == 25) for u in range(1, 26)
    ]
    # A non-complete odd cycle has order u+1>=5 odd, hence even u>=4.
    block_types += [("C", u, u + 1, False) for u in range(4, n, 2)]

    states: dict[tuple[int, bool, int], tuple[tuple[str, int, int], ...]] = {
        (0, False, 0): ()
    }
    for kind, increment, edges, is_k26 in block_types:
        previous = list(states.items())
        for (units, used_k26, total_edges), witness in previous:
            copies = (n - 1 - units) // increment
            if is_k26:
                copies = min(copies, 0 if used_k26 else 1)
            for count in range(1, copies + 1):
                key = (
                    units + count * increment,
                    used_k26 or is_k26,
                    total_edges + count * edges,
                )
                states.setdefault(key, witness + ((kind, increment, count),))

    spectrum: dict[int, tuple[int, bool, tuple[tuple[str, int, int], ...]]] = {}
    for (units, used_k26, total_edges), witness in states.items():
        spectrum.setdefault(total_edges, (units, used_k26, witness))
    return spectrum


def block_name(kind: str, increment: int) -> str:
    return f"{kind}{increment + 1}"


def witness_text(
    n: int, witness_data: tuple[int, bool, tuple[tuple[str, int, int], ...]]
) -> str:
    units, _, witness = witness_data
    names = []
    for kind, increment, count in witness:
        names.extend([block_name(kind, increment)] * count)
    return "+".join(names) + f" components={n - units}"


def gap_record(n: int, target_low: int, target_high: int) -> str:
    spectrum = block_spectrum(n)
    hits = sorted(set(spectrum) & set(range(target_low, target_high + 1)))
    assert not hits
    previous = max(e for e in spectrum if e < target_low)
    following = min(e for e in spectrum if e > target_high)
    return (
        f"block_spectrum n={n} target={target_low}..{target_high} hits=NONE "
        f"previous={previous} witness={witness_text(n, spectrum[previous])} "
        f"next={following} witness={witness_text(n, spectrum[following])}"
    )


T = (0, 1, 2)
S = 3
W = (4, 5)
B = frozenset((*T, S))

# The unique height-2583 local orbit with singleton H-degrees (2,3), after
# relabelling T and W: T is a triangle, s is H-anticomplete to T, and
# N_H(w1)={s,t3}, N_H(w2)={s,t1,t2}.
LOCAL_H = frozenset(
    {
        edge(0, 1), edge(0, 2), edge(1, 2),
        edge(4, 3), edge(4, 2),
        edge(5, 3), edge(5, 0), edge(5, 1),
    }
)


def is_local_g_edge(a: int, b: int) -> bool:
    return edge(a, b) not in LOCAL_H


def local_high_edge_minima() -> tuple[int, ...]:
    """Lower-bound e(G[R]) for each k=|R intersect C|.

    In the 49-low profile, four excess-one vertices join the two singleton
    high vertices.  If k of those four lie in C, exactly k vertices of B are
    low.  Both singletons are G-adjacent to every vertex of C.  We count only
    the forced edges within W union B and the 2k forced W--C edges; all other
    possible high--high edges are deliberately ignored.
    """

    minima = []
    for k in range(5):
        candidates = []
        for low_b_tuple in combinations(sorted(B), k):
            high_b = B - frozenset(low_b_tuple)
            high_local = frozenset(W) | high_b
            forced = 2 * k
            forced += sum(
                is_local_g_edge(a, b)
                for a, b in combinations(sorted(high_local), 2)
            )
            candidates.append(forced)
        minima.append(min(candidates))
    assert tuple(minima) == (7, 6, 7, 7, 9)
    return tuple(minima)


def histogram_text(profile: tuple[int, ...]) -> str:
    counts = Counter(profile)
    return ",".join(f"{value}^{counts[value]}" for value in sorted(counts))


def low_edge_range(row: int, profile: tuple[int, ...], e_r_low: int) -> tuple[int, int]:
    high = tuple(x for x in profile if x)
    degree_sum = sum(27 + x for x in high)
    maximum_e_r = len(high) * (len(high) - 1) // 2
    return row - degree_sum + e_r_low, row - degree_sum + maximum_e_r


def main() -> None:
    gap50 = gap_record(50, 582, 591)
    gap49 = gap_record(49, 560, 569)
    assert "previous=581" in gap50 and "next=600" in gap50
    assert "previous=559" in gap49 and "next=576" in gap49

    profiles = (
        (0,) * 50 + (1, 1, 1, 25, 25),
        (0,) * 50 + (1, 1, 2, 24, 25),
        (0,) * 49 + (1, 1, 1, 1, 24, 25),
    )
    local_minima = local_high_edge_minima()

    output = [
        "PASS Albertson r=28 Gallai spectrum-gap elimination",
        gap50,
        gap49,
        "local_degree_2_3_orbit "
        "H_N(w1)=s,t3 H_N(w2)=s,t1,t2 H_edges(s,T)=0",
        "local_eR_min_by_k=" + ",".join(
            f"{k}:{value}" for k, value in enumerate(local_minima)
        ),
    ]

    survivors = 0
    for profile in profiles:
        n_low = profile.count(0)
        e_r_low = 1 if n_low == 50 else min(local_minima)
        low, high = low_edge_range(769, profile, e_r_low)
        assert (n_low, low, high) in ((50, 582, 591), (49, 560, 569))
        spectrum = block_spectrum(n_low)
        hits = sorted(set(spectrum) & set(range(low, high + 1)))
        survivors += int(bool(hits))
        assert not hits
        output.append(
            f"row=769 profile={histogram_text(profile)} "
            f"eR_floor={e_r_low} eL_range={low}..{high} "
            "gallai_spectrum_hits=NONE ELIMINATED"
        )

    assert survivors == 0
    output.append("summary row=769 input_profiles=3 survivors=0")
    digest = sha256(("\n".join(output) + "\n").encode()).hexdigest()
    output.append(f"certificate_sha256={digest}")
    print("\n".join(output))


if __name__ == "__main__":
    main()
