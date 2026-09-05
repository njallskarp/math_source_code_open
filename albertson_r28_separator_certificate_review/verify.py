#!/usr/bin/env python3
"""Clean-room exact review of the r=28 separator/component certificate.

This implementation is deliberately specialized to the two rows (55,768)
and (55,769).  Component multisets are represented by ascending multiplicity
vectors, and subset sums are computed by integer bitsets; neither representation
is used by the upstream checker under review.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from math import comb


R = 28
N = 55
ROWS = (768, 769)


def hill(n: int) -> int:
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def zarankiewicz(a: int, b: int) -> int:
    return (a // 2) * ((a - 1) // 2) * (b // 2) * ((b - 1) // 2)


def crossing_k6n(n: int) -> int:
    return 6 * (n // 2) * ((n - 1) // 2)


def falling(n: int, k: int) -> int:
    answer = 1
    for j in range(k):
        answer *= n - j
    return answer


SMALL_COMPLETE = {
    0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
    5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150,
}


@lru_cache(maxsize=None)
def complete_lower(q: int) -> int:
    if q in SMALL_COMPLETE:
        return SMALL_COMPLETE[q]
    # Every crossing belongs to q-4 of the q vertex-deleted subdrawings.
    return -(-(q * complete_lower(q - 1)) // (q - 4))


@lru_cache(maxsize=None)
def sampled_affine(n: int, m: int, k: int) -> Fraction:
    line = Fraction(5 * m * k * (k - 1), n * (n - 1))
    line -= Fraction(203 * (k - 2), 9)
    return line * Fraction(falling(n, 4), falling(k, 4))


@lru_cache(maxsize=None)
def graph_crossing_lower(n: int, m: int) -> int:
    """Conservative integer floor of the induced-sampling lower bound."""
    if n < 4 or m <= 0:
        return 0
    assert m <= comb(n, 2)
    values = [sampled_affine(n, m, k) for k in range(4, n + 1)]
    best = max([Fraction(0), *values])
    return best.numerator // best.denominator


def bipartite_lower(a: int, b: int) -> int:
    """Kleitman K_6,n counting lower bound, rounded down conservatively."""
    best = 0
    for x, y in ((a, b), (b, a)):
        if x >= 6:
            best = max(best, x * (x - 1) * crossing_k6n(y) // 30)
    return best


def subset_sum_bits(parts: tuple[int, ...]) -> int:
    bits = 1
    for size in parts:
        bits |= bits << size
    return bits


def multipartite_bipartite_lower(parts: tuple[int, ...]) -> int:
    bits = subset_sum_bits(parts)
    total = sum(parts)
    return max(
        bipartite_lower(a, total - a)
        for a in range(total + 1)
        if (bits >> a) & 1
    )


def multiplicity_partitions(
    total: int, odd_minimum: int, barrier_size: int, excess_budget: int
) -> tuple[tuple[int, ...], ...]:
    """Generate every admissible partition by ascending part multiplicities."""

    results: list[tuple[int, ...]] = []
    # State: next part size, remaining sum, odd count, deficiency, (size,count).
    stack: list[tuple[int, int, int, int, tuple[tuple[int, int], ...]]] = [
        (1, total, 0, 0, ())
    ]
    while stack:
        size, remaining, odd_count, deficiency, encoded = stack.pop()
        if remaining == 0:
            if odd_count >= odd_minimum:
                parts = tuple(
                    part
                    for part, count in encoded
                    for _ in range(count)
                )
                results.append(tuple(sorted(parts, reverse=True)))
            continue
        if size > remaining:
            continue
        unit_cost = size * max(0, R - barrier_size - size)
        maximum_count = remaining // size
        for count in range(maximum_count, -1, -1):
            new_deficiency = deficiency + count * unit_cost
            if new_deficiency > excess_budget:
                continue
            new_remaining = remaining - count * size
            new_odd_count = odd_count + (count if size % 2 else 0)
            new_encoded = encoded + (((size, count),) if count else ())
            stack.append(
                (size + 1, new_remaining, new_odd_count, new_deficiency, new_encoded)
            )
    return tuple(sorted(results, reverse=True))


def forced_deficiency(parts: tuple[int, ...], barrier_size: int) -> int:
    return sum(size * max(0, R - barrier_size - size) for size in parts)


def cross_edge_upper(parts: tuple[int, ...], barrier_size: int, budget: int) -> int:
    d_size = sum(parts)
    internal_h_max = sum(comb(size, 2) for size in parts)
    return d_size * (barrier_size - R + 1) + budget + 2 * internal_h_max


def cross_edge_lower(parts: tuple[int, ...], barrier_size: int) -> int:
    d_size = sum(parts)
    from_barrier = barrier_size * max(0, R - barrier_size)
    from_components = d_size * max(0, R - d_size)
    return max(from_barrier, from_components)


def topological_complete_obstruction(
    parts: tuple[int, ...], barrier_size: int, budget: int
) -> tuple[bool, int]:
    number_of_parts = len(parts)
    if number_of_parts >= R:
        return True, -1
    special = tuple(sorted(parts)) == (1,) * (R - 2) + (2,)
    if number_of_parts != R - 1 or not special:
        return False, -1
    upper = cross_edge_upper(parts, barrier_size, budget)
    internal_g_floor = -(-(barrier_size * (R - 1) - upper) // 2)
    disconnected_maximum = comb(barrier_size - 1, 2)
    return internal_g_floor > disconnected_maximum, internal_g_floor


@dataclass(frozen=True)
class SplitWitness:
    value: int
    excess_in_d: int
    h_edges_in_b: int
    h_edges_in_d: int
    g_edges_in_d: int
    g_edges_in_b: int


def split_minimum(
    parts: tuple[int, ...], barrier_size: int, row: int
) -> SplitWitness | None:
    budget = 2 * row - N * (R - 1)
    h_total = comb(N, 2) - row
    d_size = sum(parts)
    complete_d = comb(d_size, 2)
    complete_b = comb(barrier_size, 2)
    deficiency_minimum = forced_deficiency(parts, barrier_size)
    internal_h_minimum = sum(size - 1 for size in parts)
    internal_h_maximum = sum(comb(size, 2) for size in parts)
    fixed_bipartite = multipartite_bipartite_lower(parts)

    candidates: list[SplitWitness] = []
    for excess_in_d in range(deficiency_minimum, budget + 1):
        for h_edges_in_b in range(3, complete_b + 1):
            h_edges_in_d = (
                d_size * (R - 1) - excess_in_d - h_total + h_edges_in_b
            )
            if not (internal_h_minimum <= h_edges_in_d <= internal_h_maximum):
                continue
            g_edges_in_d = complete_d - h_edges_in_d
            g_edges_in_b = complete_b - h_edges_in_b
            lower_d = max(
                complete_lower(len(parts)),
                graph_crossing_lower(d_size, g_edges_in_d),
                fixed_bipartite,
            )
            value = lower_d + graph_crossing_lower(barrier_size, g_edges_in_b)
            candidates.append(
                SplitWitness(
                    value, excess_in_d, h_edges_in_b, h_edges_in_d,
                    g_edges_in_d, g_edges_in_b,
                )
            )
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda w: (
            w.value, w.excess_in_d, w.h_edges_in_b, w.h_edges_in_d
        ),
    )


@dataclass(frozen=True)
class Record:
    row: int
    barrier_size: int
    parts: tuple[int, ...]
    deficiency: int
    bipartite: int
    cross_lower: int
    cross_upper: int
    tk_obstruction: bool
    split: int
    status: str

    def line(self) -> str:
        parts_text = ",".join(map(str, self.parts))
        return "\t".join(
            map(
                str,
                (
                    self.row, self.barrier_size, parts_text, self.deficiency,
                    self.bipartite, self.cross_lower, self.cross_upper,
                    int(self.tk_obstruction), self.split, self.status,
                ),
            )
        )


def classify(row: int, barrier_size: int, parts: tuple[int, ...]) -> Record:
    budget = 2 * row - N * (R - 1)
    deficiency = forced_deficiency(parts, barrier_size)
    bipartite = multipartite_bipartite_lower(parts)
    lower = cross_edge_lower(parts, barrier_size)
    upper = cross_edge_upper(parts, barrier_size, budget)
    tk, _ = topological_complete_obstruction(parts, barrier_size, budget)
    witness = split_minimum(parts, barrier_size, row)
    split_value = hill(R) + 1 if witness is None else witness.value

    if bipartite > hill(R):
        status = "bipartite"
    elif lower > upper:
        status = "cross_edges"
    elif tk:
        status = "topological_K28"
    elif split_value > hill(R):
        status = "split"
    else:
        status = "survives"
    return Record(
        row, barrier_size, parts, deficiency, bipartite, lower, upper,
        tk, split_value, status,
    )


def triangle_free_total(row: int) -> tuple[int, int, int]:
    budget = 2 * row - N * (R - 1)
    h_total = comb(N, 2) - row
    # Since budget < N, min_v x_v=0.  Thus Delta(H)=R-1.
    minimum_excess = 0
    q = (R - 1) - minimum_excess
    residual_order = N - q
    residual_g_edges = comb(residual_order, 2) - (
        h_total - q * (R - 1) + budget
    )
    total = complete_lower(q) + graph_crossing_lower(
        residual_order, residual_g_edges
    )
    return q, residual_g_edges, total


def soundness_controls() -> None:
    for q in range(5, 31):
        assert complete_lower(q) <= hill(q)
        assert graph_crossing_lower(q, comb(q, 2)) <= hill(q)
    for a in range(3, 31):
        for b in range(3, 31):
            assert bipartite_lower(a, b) <= zarankiewicz(a, b)
            assert graph_crossing_lower(a + b, a * b) <= zarankiewicz(a, b)
    for n in range(5, 56):
        for m in range(1, 3 * n - 6):
            assert graph_crossing_lower(n, m) == 0


def main() -> None:
    soundness_controls()
    all_records: list[Record] = []
    output = [
        "PASS clean-room Albertson r=28 separator certificate review",
        "arithmetic=exact_Fraction partition_representation=ascending_multiplicity "
        "subset_sum=integer_bitset",
        "soundness_controls=PASS",
    ]
    expected_survivors = {
        3: ((51, 1), (50, 1, 1)),
        4: ((49, 1, 1),),
    }

    for row in ROWS:
        q, residual_edges, triangle_total = triangle_free_total(row)
        assert triangle_total > hill(R)
        output.append(
            f"row={row} triangle_free q={q} residual_order={N-q} "
            f"residual_edges={residual_edges} split_lower={triangle_total}>Z28={hill(R)}"
        )
        live_by_barrier: dict[int, tuple[tuple[int, ...], ...]] = {}
        initial_total = 0
        for barrier_size in range(3, (N + 1) // 2 + 1):
            total = N - barrier_size
            odd_minimum = barrier_size - 1
            budget = 2 * row - N * (R - 1)
            configurations = multiplicity_partitions(
                total, odd_minimum, barrier_size, budget
            )
            initial_total += len(configurations)
            records = tuple(
                classify(row, barrier_size, parts) for parts in configurations
            )
            all_records.extend(records)
            survivors = tuple(
                record.parts for record in records if record.status == "survives"
            )
            if survivors:
                live_by_barrier[barrier_size] = survivors
            if configurations or survivors:
                reasons: dict[str, int] = {}
                for record in records:
                    reasons[record.status] = reasons.get(record.status, 0) + 1
                reason_text = ",".join(
                    f"{name}:{reasons[name]}" for name in sorted(reasons)
                ) or "none"
                survivor_text = ";".join(
                    ",".join(map(str, parts)) for parts in survivors
                ) or "NONE"
                output.append(
                    f"row={row} b={barrier_size} initial={len(configurations)} "
                    f"reasons={reason_text} survivors={survivor_text}"
                )
        assert live_by_barrier == expected_survivors
        output.append(
            f"row={row} initial_configurations={initial_total} "
            "surviving_barriers=3,4 survivor_multisets="
            "b3:51,1;50,1,1|b4:49,1,1"
        )

    certificate = "\n".join(record.line() for record in all_records) + "\n"
    digest = sha256(certificate.encode()).hexdigest()
    output.append(
        f"entry_records={len(all_records)} certificate_sha256={digest}"
    )
    output.append(
        "conclusion=r28_rows_768_769_triangle_case_only_b3_b4_and_"
        "b4_only_49_1_1; triangle_free=eliminated"
    )
    print("\n".join(output))


if __name__ == "__main__":
    main()
