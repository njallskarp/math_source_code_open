#!/usr/bin/env python3
"""Independent type-count audit using a frozen F_53 table slice."""

from __future__ import annotations

from collections import Counter
from math import comb


F53 = {
    664: 4783, 665: 4808, 666: 4832, 667: 4856, 668: 4881,
    686: 5333, 687: 5359, 688: 5385, 689: 5411, 690: 5437,
    691: 5463, 692: 5489, 707: 5899, 708: 5928, 709: 5956,
    710: 5985, 711: 6013, 712: 6042, 713: 6071, 714: 6100,
    715: 6130, 716: 6159,
}

CASES = (
    (768, (25, 25), (1,), (21468, 21470), 9026658),
    (768, (24, 25), (2,), (21465, 21467), 9026500),
    (768, (24, 25), (1, 1), (21438, 21443), 9026449),
    (769, (25, 25), (3,), (20752, 20752), 9066280),
    (769, (24, 25), (4,), (20749, 20749), 9066122),
    (769, (25, 25), (1, 2), (20752, 20778), 9066280),
    (769, (24, 25), (1, 3), (20749, 20775), 9066122),
    (769, (24, 25), (2, 2), (20749, 20749), 9066071),
    (769, (25, 25), (1, 1, 1), (20752, 20830), 9066329),
    (769, (24, 25), (1, 1, 2), (20749, 20801), 9066121),
    (769, (24, 25), (1, 1, 1, 1), (20749, 20853), 9066168),
)


def baseline_by_types(row: int, values: tuple[int, ...]) -> int:
    counts = Counter(values)
    types = sorted(counts)
    total = 0
    for i, a in enumerate(types):
        for b in types[i:]:
            pairs = comb(counts[a], 2) if a == b else counts[a] * counts[b]
            total += pairs * F53[row - 53 - a - b]
    assert sum(counts.values()) == 55
    return total


def ceiling(numerator: int, denominator: int = 1275) -> int:
    return (numerator + denominator - 1) // denominator


def main() -> None:
    bounds = {768: set(), 769: set()}
    for row, singleton_excesses, extras, penalty_range, expected_baseline in CASES:
        values = tuple(sorted(singleton_excesses + extras + (0,) * (53 - len(extras))))
        baseline = baseline_by_types(row, values)
        assert baseline == expected_baseline
        sum_range = (baseline - penalty_range[1], baseline - penalty_range[0])
        rounded = (ceiling(sum_range[0]), ceiling(sum_range[1]))
        assert rounded[0] == rounded[1]
        bounds[row].add(rounded[0])
    assert bounds == {768: {7063}, 769: {7095}}
    print("PASS independent type-count audit")
    print("cases=11 frozen_F53_entries=22 denominator=1275")
    print("bounds=768:7063,769:7095")


if __name__ == "__main__":
    main()
