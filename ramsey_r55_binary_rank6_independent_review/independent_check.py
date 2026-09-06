#!/usr/bin/env python3
"""Clean-room audit of the binary-adjacency-rank-six obstruction.

This checker reads no target file or certificate.  It discovers a symplectic
spread as an exact cover of the nonzero vectors, verifies the universal
coordinate graph directly, and checks a principal-Gram reconstruction for
every alternating 6 by 6 binary matrix.
"""

from __future__ import annotations

from functools import lru_cache
import hashlib
import itertools
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def gf2_rank(rows: list[int], width: int) -> int:
    work = list(rows)
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (index for index in range(pivot_row, len(work)) if work[index] >> column & 1),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        for index in range(len(work)):
            if index != pivot_row and work[index] >> column & 1:
                work[index] ^= work[pivot_row]
        pivot_row += 1
    return pivot_row


def gf2_inverse(rows: list[int], dimension: int) -> list[int]:
    work = [row | (1 << (dimension + index)) for index, row in enumerate(rows)]
    for column in range(dimension):
        pivot = next(
            (index for index in range(column, dimension) if work[index] >> column & 1),
            None,
        )
        require(pivot is not None, "singular principal Gram matrix")
        work[column], work[pivot] = work[pivot], work[column]
        for index in range(dimension):
            if index != column and work[index] >> column & 1:
                work[index] ^= work[column]
    low_mask = (1 << dimension) - 1
    require(
        [row & low_mask for row in work] == [1 << index for index in range(dimension)],
        "inverse elimination failed",
    )
    return [row >> dimension for row in work]


def form_value(left: int, right: int, form_rows: tuple[int, ...] | list[int]) -> int:
    image = 0
    scan = left
    while scan:
        bit = scan & -scan
        scan ^= bit
        image ^= form_rows[bit.bit_length() - 1]
    return (image & right).bit_count() & 1


def standard_symplectic_form(half_dimension: int) -> tuple[int, ...]:
    dimension = 2 * half_dimension
    rows = [0] * dimension
    for index in range(half_dimension):
        rows[index] = 1 << (half_dimension + index)
        rows[half_dimension + index] = 1 << index
    return tuple(rows)


@lru_cache(maxsize=None)
def linear_subspaces(dimension: int, subspace_dimension: int) -> tuple[tuple[int, ...], ...]:
    if subspace_dimension == 0:
        return ((),)
    spaces: set[tuple[int, ...]] = set()
    for basis in itertools.combinations(range(1, 1 << dimension), subspace_dimension):
        span = {
            _xor_selected(basis, mask)
            for mask in range(1, 1 << subspace_dimension)
        }
        if len(span) == (1 << subspace_dimension) - 1:
            spaces.add(tuple(sorted(span)))
    return tuple(sorted(spaces))


def _xor_selected(values: tuple[int, ...], mask: int) -> int:
    result = 0
    for index, value in enumerate(values):
        if mask >> index & 1:
            result ^= value
    return result


@lru_cache(maxsize=None)
def isotropic_spread(form_rows: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    dimension = len(form_rows)
    require(dimension % 2 == 0, "alternating rank must be even")
    if dimension == 0:
        return ((),)
    half = dimension // 2
    require(gf2_rank(list(form_rows), dimension) == dimension, "form is degenerate")
    require(
        all(not form_value(vector, vector, form_rows) for vector in range(1 << dimension)),
        "form is not alternating",
    )
    candidates = [
        space
        for space in linear_subspaces(dimension, half)
        if all(
            form_value(left, right, form_rows) == 0
            for left, right in itertools.combinations(space, 2)
        )
    ]
    candidate_masks = [sum(1 << vector for vector in space) for space in candidates]
    by_vector = {
        vector: [index for index, mask in enumerate(candidate_masks) if mask >> vector & 1]
        for vector in range(1, 1 << dimension)
    }
    universe = sum(1 << vector for vector in range(1, 1 << dimension))
    failed: set[int] = set()

    def exact_cover(remaining: int) -> tuple[int, ...] | None:
        if not remaining:
            return ()
        if remaining in failed:
            return None
        vectors = [vector for vector in range(1, 1 << dimension) if remaining >> vector & 1]
        options_by_vector = []
        for vector in vectors:
            options = [
                index
                for index in by_vector[vector]
                if candidate_masks[index] & remaining == candidate_masks[index]
            ]
            if not options:
                failed.add(remaining)
                return None
            options_by_vector.append((len(options), vector, options))
        _, _, options = min(options_by_vector)
        for index in options:
            continuation = exact_cover(remaining ^ candidate_masks[index])
            if continuation is not None:
                return (index,) + continuation
        failed.add(remaining)
        return None

    cover = exact_cover(universe)
    require(cover is not None, "no isotropic exact cover found")
    spread = tuple(sorted(candidates[index] for index in cover))
    expected_classes = (1 << half) + 1
    require(len(spread) == expected_classes, "wrong spread size")
    require(
        sorted(vector for space in spread for vector in space)
        == list(range(1, 1 << dimension)),
        "spread is not a partition",
    )
    return spread


def alternating_rows(order: int, edge_mask: int) -> list[int]:
    rows = [0] * order
    for index, (left, right) in enumerate(itertools.combinations(range(order), 2)):
        if edge_mask >> index & 1:
            rows[left] |= 1 << right
            rows[right] |= 1 << left
    return rows


def principal_gram_model(rows: list[int]) -> tuple[list[int], tuple[int, ...], tuple[int, ...]]:
    """Represent A as X M X^T using a nonsingular principal Gram block.

    Pairwise Schur pivots select the principal indices.  Coordinates and the
    inverse form are then reconstructed from the original matrix, rather than
    from rank-one factor words.
    """

    order = len(rows)
    residual = list(rows)
    active = (1 << order) - 1
    selected: list[int] = []
    while any(residual[index] & active for index in range(order) if active >> index & 1):
        left = next(
            index
            for index in range(order)
            if active >> index & 1 and residual[index] & active
        )
        right = ((residual[left] & active) & -(residual[left] & active)).bit_length() - 1
        old_left, old_right = residual[left], residual[right]
        for index in range(order):
            if residual[index] >> left & 1:
                residual[index] ^= old_right
            if residual[index] >> right & 1:
                residual[index] ^= old_left
        selected.extend((left, right))
        active &= ~(1 << left | 1 << right)

    dimension = len(selected)
    rank = gf2_rank(rows, order)
    require(dimension == rank and rank % 2 == 0, "principal rank selection failed")
    if not selected:
        require(not any(rows), "zero-rank reconstruction failed")
        return [0] * order, (), ()

    gram = [
        sum(((rows[selected[i]] >> selected[j]) & 1) << j for j in range(dimension))
        for i in range(dimension)
    ]
    inverse = tuple(gf2_inverse(gram, dimension))
    require(
        all(not (inverse[index] >> index & 1) for index in range(dimension))
        and all(
            (inverse[i] >> j & 1) == (inverse[j] >> i & 1)
            for i in range(dimension)
            for j in range(dimension)
        ),
        "inverse Gram form is not alternating",
    )
    coordinates = [
        sum(((rows[vertex] >> selected[index]) & 1) << index for index in range(dimension))
        for vertex in range(order)
    ]
    require(
        all(
            form_value(coordinates[i], coordinates[j], inverse) == (rows[i] >> j & 1)
            for i in range(order)
            for j in range(order)
        ),
        "principal-Gram reconstruction failed",
    )
    return coordinates, inverse, tuple(selected)


def color_from_form(coordinates: list[int], form_rows: tuple[int, ...]) -> list[int]:
    spread = isotropic_spread(form_rows)
    colors = {0: 0}
    for color, space in enumerate(spread):
        for vector in space:
            colors[vector] = color
    coloring = [colors[vector] for vector in coordinates]
    require(
        all(
            coloring[i] != coloring[j] or form_value(coordinates[i], coordinates[j], form_rows) == 0
            for i, j in itertools.combinations(range(len(coordinates)), 2)
        ),
        "improper pullback coloring",
    )
    return coloring


def universal_coordinate_audit() -> dict[str, object]:
    form = standard_symplectic_form(3)
    spread = isotropic_spread(form)
    colors = {0: 0}
    for color, space in enumerate(spread):
        for vector in space:
            colors[vector] = color
    vertices = range(1, 64)
    adjacency_rows = [
        sum(1 << (right - 1) for right in vertices if form_value(left, right, form))
        for left in vertices
    ]
    degrees = [row.bit_count() for row in adjacency_rows]
    common = [
        (adjacency_rows[left - 1] & adjacency_rows[right - 1]).bit_count()
        for left, right in itertools.combinations(vertices, 2)
    ]
    require(set(degrees) == {32}, "wrong universal degree")
    require(set(common) == {16}, "wrong common-neighbour count")
    require(gf2_rank(adjacency_rows, 63) == 6, "wrong universal binary rank")
    require(
        all(
            colors[left] != colors[right]
            for left, right in itertools.combinations(vertices, 2)
            if form_value(left, right, form)
        ),
        "spread fails to color the universal graph",
    )
    # The checked parameters give A^2=16(I+J).  On the all-ones line the
    # eigenvalue is 32; on its orthogonal complement the eigenvalues are
    # +/-4.  Trace(A)=0 fixes their multiplicities as 27 and 35.
    positive_eigenvalue, negative_eigenvalue = 4, -4
    positive_multiplicity = (62 - 32 // positive_eigenvalue) // 2
    negative_multiplicity = 62 - positive_multiplicity
    require(
        32 + positive_multiplicity * positive_eigenvalue
        + negative_multiplicity * negative_eigenvalue
        == 0,
        "spectrum multiplicities do not have zero trace",
    )
    hoffman_bound = 1 - 32 // negative_eigenvalue
    require(hoffman_bound == len(spread) == 9, "sharp chromatic bounds disagree")
    encoded = json.dumps(spread, separators=(",", ":")).encode()
    return {
        "ambient_vectors_including_zero": 64,
        "nonzero_universal_vertices": 63,
        "binary_adjacency_rank": 6,
        "regular_degree": 32,
        "common_neighbours_every_distinct_pair": 16,
        "lagrangian_subspaces": sum(
            1
            for space in linear_subspaces(6, 3)
            if all(
                form_value(left, right, form) == 0
                for left, right in itertools.combinations(space, 2)
            )
        ),
        "spread_classes": len(spread),
        "nonzero_vectors_per_class": len(spread[0]),
        "spread_sha256": hashlib.sha256(encoded).hexdigest(),
        "strongly_regular_parameters": [63, 32, 16, 16],
        "spectrum_with_multiplicities": [[32, 1], [4, 27], [-4, 35]],
        "hoffman_chromatic_lower_bound": hoffman_bound,
        "chromatic_number": len(spread),
    }


def alternating_matrix_audit() -> dict[str, object]:
    histogram: dict[int, int] = {}
    principal_models = 0
    order = 6
    for edge_mask in range(1 << (order * (order - 1) // 2)):
        rows = alternating_rows(order, edge_mask)
        rank = gf2_rank(rows, order)
        require(rank % 2 == 0, "odd alternating rank")
        coordinates, inverse, selected = principal_gram_model(rows)
        require(len(inverse) == len(selected) == rank, "model dimension mismatch")
        require(len(coordinates) == order, "coordinate count mismatch")
        histogram[rank] = histogram.get(rank, 0) + 1
        principal_models += 1
    return {
        "alternating_6_by_6_matrices": principal_models,
        "rank_histogram": {str(rank): histogram[rank] for rank in sorted(histogram)},
        "all_ranks_even": True,
        "all_principal_gram_models_reconstructed": True,
    }


def synthetic_physical_audit() -> dict[str, object]:
    form = standard_symplectic_form(3)
    coordinate_sets = []
    for active_pairs in range(4):
        allowed = sum(1 << index | 1 << (index + 3) for index in range(active_pairs))
        seed = [0]
        for index in range(active_pairs):
            seed.extend((1 << index, 1 << (index + 3)))
        coordinates = seed + [((17 * index + 11) & 63) & allowed for index in range(43 - len(seed))]
        coordinate_sets.append(coordinates)

    results = []
    for source_coordinates in coordinate_sets:
        order = len(source_coordinates)
        rows = [
            sum(
                form_value(source_coordinates[i], source_coordinates[j], form) << j
                for j in range(order)
            )
            for i in range(order)
        ]
        coordinates, recovered_form, selected = principal_gram_model(rows)
        coloring = color_from_form(coordinates, recovered_form)
        classes = [[index for index, color in enumerate(coloring) if color == value] for value in set(coloring)]
        largest = max(classes, key=len)
        rank = len(selected)
        bound = (1 << (rank // 2)) + 1 if rank else 1
        require(len(set(coloring)) <= bound <= 9, "color bound failed")
        require(len(largest) >= 5, "43-vertex independent five-set missing")
        require(
            all(not (rows[i] >> j & 1) for i, j in itertools.combinations(largest[:5], 2)),
            "reported physical five-set is not independent",
        )
        results.append(
            {
                "rank": rank,
                "colors_used": len(set(coloring)),
                "largest_class": len(largest),
                "witness": largest[:5],
            }
        )
    return {
        "order": 43,
        "instances": len(results),
        "rank_0_2_4_6_results": results,
        "pigeonhole_threshold_for_nine_colors": 37,
        "threshold_minus_one_only_forces": 4,
    }


def main() -> None:
    core = {
        "status": "INDEPENDENTLY_VERIFIED_R55_BINARY_RANK_SIX_OBSTRUCTION",
        "universal_coordinate_graph": universal_coordinate_audit(),
        "alternating_matrix_controls": alternating_matrix_audit(),
        "synthetic_physical_controls": synthetic_physical_audit(),
        "derived_ramsey_consequence": {
            "rank_at_most": 6,
            "color_bound": 9,
            "order_at_least_for_independent_five": 37,
            "hypothetical_r55_order": 43,
            "minimum_binary_rank_in_each_color": 8,
        },
        "trust_boundary": (
            "written principal-Gram and pullback proofs, CPython exact integer/bit semantics, "
            "exhaustive finite checks; no target source, target certificate, solver, or catalog imported"
        ),
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode()
    result = {**core, "evidence_sha256": hashlib.sha256(canonical).hexdigest()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
