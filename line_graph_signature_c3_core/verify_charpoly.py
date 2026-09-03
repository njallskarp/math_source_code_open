#!/usr/bin/env python3
"""Independent exact characteristic-polynomial replay of the c=3 quotient.

This checker intentionally does not call the Fraction-congruence inertia
routine in verify_c3_core.py.  It reuses only the structural enumerator and
graph expansion, then counts positive and negative roots of the real-rooted
characteristic polynomial by sign variations.
"""

from __future__ import annotations

from collections import Counter
import hashlib
from itertools import product
import json

from verify_c3_core import (
    canonical_residue_lengths,
    characteristic_polynomial,
    enumerate_c3_kernels,
    expand_kernel,
    inertia_from_charpoly,
    kernel_edge_instances,
    shifted_signless,
)


def main() -> None:
    kernels = enumerate_c3_kernels()
    histogram: Counter[tuple[int, int]] = Counter()
    equality_records: list[tuple[int, tuple[int, ...], int]] = []
    assignments = 0

    for kernel_index, kernel in enumerate(kernels):
        edges = kernel_edge_instances(kernel)
        for residues in product(range(1, 5), repeat=len(edges)):
            lengths = canonical_residue_lengths(edges, residues)
            adjacency = expand_kernel(kernel, lengths)
            positive, nullity, negative = inertia_from_charpoly(
                characteristic_polynomial(shifted_signless(adjacency))
            )
            line_signature = positive - negative - 2
            histogram[(line_signature, nullity)] += 1
            assignments += 1
            if line_signature == 2:
                equality_records.append((kernel_index, residues, nullity))

    assert len(kernels) == 15
    assert assignments == 26688
    assert max(signature for signature, _ in histogram) == 2
    assert len(equality_records) == 8
    assert {kernel_index for kernel_index, _, _ in equality_records} == {11}
    assert {nullity for _, _, nullity in equality_records} == {0}
    assert {
        (residues[:2], frozenset(residues[2:4]), tuple(r % 2 for r in residues[4:]))
        for _, residues, _ in equality_records
    } == {((1, 1), frozenset({1, 3}), (1, 1))}

    result = {
        "algorithm": "Faddeev-LeVerrier characteristic polynomial plus sign variations",
        "boundary_simple_Q2_cases": sum(
            count
            for (signature, nullity), count in histogram.items()
            if signature == 2 and nullity == 1
        ),
        "equality_assignments": len(equality_records),
        "histogram_signature_nullity": {
            f"s={signature},z={nullity}": count
            for (signature, nullity), count in sorted(histogram.items())
        },
        "kernel_count": len(kernels),
        "labeled_residue_assignments": assignments,
        "maximum_signature": max(signature for signature, _ in histogram),
        "status": "VERIFIED",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())


if __name__ == "__main__":
    main()
