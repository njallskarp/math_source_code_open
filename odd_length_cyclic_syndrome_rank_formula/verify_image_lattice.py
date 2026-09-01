#!/usr/bin/env python3
"""Exhaustively verify the Boolean image-lattice theorem for odd n <= 15."""

from __future__ import annotations

import hashlib
from collections import Counter

from verify_rank_formula import factor_xn_plus_one, poly_mod, reciprocal_orbits


def direct_columns(n: int, b: int) -> list[int]:
    m = (n - 1) // 2
    columns: list[int] = []
    for j in range(n):
        column = 0
        for s in range(1, m + 1):
            bit = ((b >> ((j + s) % n)) ^ (b >> ((j - s) % n))) & 1
            column |= bit << (s - 1)
        columns.append(column)
    return columns


def canonical_basis(vectors: list[int]) -> tuple[int, ...]:
    """Canonical reduced basis, with the pivot index equal to the list index."""
    max_bit = max((value.bit_length() for value in vectors), default=0)
    basis = [0] * max_bit
    for value in vectors:
        for pivot in range(len(basis) - 1, -1, -1):
            if ((value >> pivot) & 1) and basis[pivot]:
                value ^= basis[pivot]
        if value:
            pivot = value.bit_length() - 1
            for other in range(len(basis)):
                if (basis[other] >> pivot) & 1:
                    basis[other] ^= value
            basis[pivot] = value
    return tuple(value for value in basis if value)


def lies_in_span(value: int, basis: tuple[int, ...]) -> bool:
    for pivot in range(len(basis) - 1, -1, -1):
        vector = basis[pivot]
        if vector == 0:
            continue
        leading = vector.bit_length() - 1
        if (value >> leading) & 1:
            value ^= vector
    return value == 0


def subspace_of(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return all(lies_in_span(value, right) for value in left)


def activity_signature(
    b: int, orbits: list[tuple[str, int, tuple[int, ...]]]
) -> tuple[int, ...]:
    return tuple(
        int(any(poly_mod(b, f) != 0 for f in factors))
        for _, _, factors in orbits
    )


def expected_signature_count(
    signature: tuple[int, ...],
    orbits: list[tuple[str, int, tuple[int, ...]]],
) -> int:
    # The factor 2 is the unrestricted x+1 component.
    result = 2
    for active, (orbit_type, d, _) in zip(signature, orbits, strict=True):
        if active:
            component_dimension = d if orbit_type == "S" else 2 * d
            result *= (1 << component_dimension) - 1
    return result


def expected_signature_rank(
    signature: tuple[int, ...],
    orbits: list[tuple[str, int, tuple[int, ...]]],
) -> int:
    return sum(
        (d // 2 if orbit_type == "S" else d)
        for active, (orbit_type, d, _) in zip(signature, orbits, strict=True)
        if active
    )


def main() -> None:
    record_digest = hashlib.sha256()
    tested_axes = 0

    print("odd-length syndrome image-lattice certificate")
    for n in range(3, 16, 2):
        orbits = reciprocal_orbits(factor_xn_plus_one(n))
        signature_images: dict[tuple[int, ...], tuple[int, ...]] = {}
        signature_counts: Counter[tuple[int, ...]] = Counter()

        for b in range(1 << n):
            signature = activity_signature(b, orbits)
            image = canonical_basis(direct_columns(n, b))
            if signature in signature_images:
                assert signature_images[signature] == image
            else:
                signature_images[signature] = image
            signature_counts[signature] += 1

            assert len(image) == expected_signature_rank(signature, orbits)
            record_digest.update(
                (
                    f"n={n};b={b:0{n}b};sig={''.join(map(str, signature))};"
                    f"basis={','.join(map(str, image))}\n"
                ).encode("ascii")
            )
            tested_axes += 1

        orbit_count = len(orbits)
        assert len(signature_images) == 1 << orbit_count
        assert len(set(signature_images.values())) == 1 << orbit_count

        for signature, count in signature_counts.items():
            assert count == expected_signature_count(signature, orbits)

        # Direct subspace containment agrees exactly with coordinate-support
        # containment in the predicted Boolean lattice.
        for left_signature, left_image in signature_images.items():
            for right_signature, right_image in signature_images.items():
                signature_containment = all(
                    left <= right
                    for left, right in zip(
                        left_signature, right_signature, strict=True
                    )
                )
                assert subspace_of(left_image, right_image) == signature_containment

        ranks = sorted({len(image) for image in signature_images.values()})
        print(
            f"n={n:2d} reciprocal_orbits={orbit_count} "
            f"distinct_images={len(signature_images)} "
            f"image_dimensions={','.join(map(str, ranks))}"
        )

    print(f"exhaustive_axes={tested_axes}")
    print(f"image_record_sha256={record_digest.hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
