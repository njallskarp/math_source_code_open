#!/usr/bin/env python3
"""Exact census for the QLP-42 q=5/q=37 full binary-shadow frontier."""

from __future__ import annotations

from collections import Counter, defaultdict
from csv import DictReader
from itertools import combinations
from pathlib import Path

N = 21
Q = 5
FULL = (1 << N) - 1
HALF_SHIFTS = range(1, (N + 1) // 2)


def rotate(mask: int, shift: int, length: int = N) -> int:
    full = (1 << length) - 1
    shift %= length
    return ((mask << shift) | (mask >> (length - shift))) & full


def canonical_rotation(mask: int, length: int = N) -> int:
    return min(rotate(mask, shift, length) for shift in range(length))


def autocorrelation_signature(mask: int) -> int:
    """Nonzero periodic binary autocorrelations modulo two."""
    return sum(
        (((mask & rotate(mask, shift)).bit_count() & 1) << (shift - 1))
        for shift in HALF_SHIFTS
    )


def masks_of_weight(weight: int):
    for support in combinations(range(N), weight):
        yield sum(1 << position for position in support)


def compress_mod7(mask: int) -> int:
    result = 0
    for residue in range(7):
        parity = sum((mask >> (residue + 7 * layer)) & 1 for layer in range(3)) & 1
        result |= parity << residue
    return result


def quotient_orbit_id(left: int, right: int) -> tuple[int, int]:
    return canonical_rotation(compress_mod7(left), 7), canonical_rotation(
        compress_mod7(right), 7
    )


def main() -> None:
    by_weight: list[list[int]] = [
        list(masks_of_weight(weight)) for weight in range(Q + 1)
    ]
    assert [len(words) for words in by_weight] == [1, 21, 210, 1330, 5985, 20349]

    signature = {
        mask: autocorrelation_signature(mask) for words in by_weight for mask in words
    }
    labeled_groups: Counter[tuple[int, int]] = Counter()
    orbit_groups: Counter[tuple[int, int]] = Counter()
    for weight, words in enumerate(by_weight):
        for mask in words:
            labeled_groups[(weight, signature[mask])] += 1
            if canonical_rotation(mask) == mask:
                orbit_groups[(weight, signature[mask])] += 1

    grouped_rows = []
    grouped_total_labeled = 0
    grouped_total_orbits = 0
    for left_weight in range(Q + 1):
        right_weight = Q - left_weight
        labeled = 0
        orbits = 0
        signatures = 0
        for invariant in range(1 << len(tuple(HALF_SHIFTS))):
            left_labeled = labeled_groups[(left_weight, invariant)]
            right_labeled = labeled_groups[(right_weight, invariant)]
            if left_labeled and right_labeled:
                signatures += 1
                labeled += left_labeled * right_labeled
                orbits += (
                    orbit_groups[(left_weight, invariant)]
                    * orbit_groups[(right_weight, invariant)]
                )
        grouped_rows.append((left_weight, right_weight, signatures, labeled, orbits))
        grouped_total_labeled += labeled
        grouped_total_orbits += orbits

    # A direct definition-level pass over all C(42,5) support pairs.  This
    # does not trust the signature-group multiplication used above.
    raw_pairs = 0
    compatible_pairs = 0
    pair_orbits: set[tuple[int, int]] = set()
    quotient_labeled: Counter[tuple[int, int]] = Counter()
    quotient_orbits: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(
        set
    )
    direct_rows = []
    for left_weight in range(Q + 1):
        right_weight = Q - left_weight
        split_raw = 0
        split_compatible = 0
        split_orbits: set[tuple[int, int]] = set()
        for left in by_weight[left_weight]:
            for right in by_weight[right_weight]:
                split_raw += 1
                if signature[left] != signature[right]:
                    continue
                split_compatible += 1
                canonical_pair = (
                    canonical_rotation(left),
                    canonical_rotation(right),
                )
                quotient = quotient_orbit_id(left, right)
                split_orbits.add(canonical_pair)
                pair_orbits.add(canonical_pair)
                quotient_labeled[quotient] += 1
                quotient_orbits[quotient].add(canonical_pair)
        raw_pairs += split_raw
        compatible_pairs += split_compatible
        direct_rows.append(
            (left_weight, right_weight, split_raw, split_compatible, len(split_orbits))
        )

    assert raw_pairs == 850_668  # Vandermonde: sum C(21,a)C(21,5-a)=C(42,5).
    assert compatible_pairs == grouped_total_labeled
    assert len(pair_orbits) == grouped_total_orbits
    assert [row[:2] + row[3:] for row in direct_rows] == [
        row[:2] + row[3:] for row in grouped_rows
    ]

    # For odd length, c_(1-u)(s)=1+c_u(s) in F_2.  Complementing both
    # words therefore preserves compatibility and sends total weight 5 to 37.
    for mask in range(1 << N):
        assert autocorrelation_signature(FULL ^ mask) == (
            autocorrelation_signature(mask) ^ ((1 << len(tuple(HALF_SHIFTS))) - 1)
        )

    assert len(quotient_labeled) == 12
    assert set(quotient_labeled) == set(quotient_orbits)
    assert sum(quotient_labeled.values()) == compatible_pairs
    assert sum(len(values) for values in quotient_orbits.values()) == len(pair_orbits)

    with (Path(__file__).parent / "frontier_orbits.tsv").open(
        encoding="utf-8", newline=""
    ) as handle:
        manifest = list(DictReader(handle, delimiter="\t"))
    expected_manifest = []
    for left, right in sorted(pair_orbits):
        qleft, qright = quotient_orbit_id(left, right)
        expected_manifest.append(
            {
                "q_a": str(left.bit_count()),
                "q_b": str(right.bit_count()),
                "a_mask_hex": f"{left:06x}",
                "b_mask_hex": f"{right:06x}",
                "v_a_hex": f"{qleft:02x}",
                "v_b_hex": f"{qright:02x}",
            }
        )
    assert manifest == expected_manifest

    print(f"raw_q5_support_pairs={raw_pairs}")
    print(f"compatible_q5_labeled_pairs={compatible_pairs}")
    print(f"compatible_q5_independent_rotation_orbits={len(pair_orbits)}")
    print("q5_q37_complement_bijection=verified")
    print(f"mod7_quotient_orbits={len(quotient_labeled)}")
    print(f"canonical_orbit_manifest_rows={len(manifest)}")
    for row in direct_rows:
        print(
            "split="
            + ",".join(map(str, row[:2]))
            + f";raw={row[2]};compatible={row[3]};orbits={row[4]}"
        )
    for quotient in sorted(quotient_labeled):
        print(
            f"quotient={quotient[0]:02x},{quotient[1]:02x};"
            f"labeled={quotient_labeled[quotient]};"
            f"orbits={len(quotient_orbits[quotient])}"
        )
    print("certificate=verified")


if __name__ == "__main__":
    main()
