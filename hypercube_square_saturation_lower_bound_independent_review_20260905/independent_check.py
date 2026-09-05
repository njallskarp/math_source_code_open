#!/usr/bin/env python3
"""Independent exact audit of the local Q3 slack bound and the d=3 global chain.

The representation and checks here were written for the review of Discovery Net
artifact bafkreigxcubdt4tl4rurx3uvax66gtccwp36dfacvtasnrdlj3xvfyhzhy.
Only Python integers, sets, and exhaustive finite loops are used.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations


def q3_incidence() -> tuple[list[tuple[int, int]], list[frozenset[int]]]:
    """Build the 12 edges and six square faces of Q3 from vertex bit flips."""
    edges = sorted(
        (vertex, vertex ^ (1 << axis))
        for axis in range(3)
        for vertex in range(8)
        if not (vertex & (1 << axis))
    )
    edge_id = {edge: index for index, edge in enumerate(edges)}

    faces: list[frozenset[int]] = []
    for axis1, axis2 in combinations(range(3), 2):
        remaining = 3 - axis1 - axis2
        for fixed_bit in (0, 1):
            base = fixed_bit << remaining
            vertices = {
                base,
                base ^ (1 << axis1),
                base ^ (1 << axis2),
                base ^ (1 << axis1) ^ (1 << axis2),
            }
            face = frozenset(
                index
                for index, (left, right) in enumerate(edges)
                if left in vertices and right in vertices
            )
            assert len(face) == 4
            faces.append(face)

    assert len(edges) == 12
    assert len(faces) == 6 and len(set(faces)) == 6
    assert all(sum(edge in face for face in faces) == 2 for edge in range(12))
    return edges, faces


def main() -> None:
    _, faces = q3_incidence()
    adjacent_pairs: dict[tuple[int, int], int] = {}
    for left, right in combinations(range(6), 2):
        shared = faces[left] & faces[right]
        if shared:
            assert len(shared) == 1
            adjacent_pairs[(left, right)] = next(iter(shared))
    assert len(adjacent_pairs) == 12

    pattern_count = Counter()
    min_twice_margin: dict[int, int] = defaultdict(lambda: 10**9)
    equality_count = Counter()
    exact_equality_signatures = Counter()
    saturated_sizes = Counter()
    global_chain_checks = 0

    for mask in range(1 << 12):
        selected = {edge for edge in range(12) if mask & (1 << edge)}
        face_counts = [len(face & selected) for face in faces]
        if max(face_counts) == 4:
            continue

        active = {index for index, count in enumerate(face_counts) if count == 3}
        t = len(active)
        missing_by_face = {
            face: next(iter(faces[face] - selected)) for face in active
        }
        r = len(set(missing_by_face.values()))
        q = t - r

        boundary = 0
        active_inactive_selected = 0
        repeated_pairs = 0
        for (left, right), shared_edge in adjacent_pairs.items():
            left_active = left in active
            right_active = right in active
            if left_active != right_active:
                boundary += 1
                if shared_edge in selected:
                    active_inactive_selected += 1
            elif left_active:
                if (
                    missing_by_face[left] == shared_edge
                    and missing_by_face[right] == shared_edge
                ):
                    repeated_pairs += 1

        b = sum(
            count for index, count in enumerate(face_counts) if index not in active
        )
        assert q == repeated_pairs
        assert boundary == active_inactive_selected + t - 2 * q
        assert b >= active_inactive_selected

        twice_margin = 2 * b + 4 * q - t
        assert twice_margin >= 0
        if twice_margin == 0:
            exact_equality_signatures[
                (t, q, b, boundary, active_inactive_selected)
            ] += 1
        pattern_count[t] += 1
        if twice_margin < min_twice_margin[t]:
            min_twice_margin[t] = twice_margin
            equality_count[t] = 1
        elif twice_margin == min_twice_margin[t]:
            equality_count[t] += 1

        # A Q3-only end-to-end check of all identities in the global proof.
        omitted = set(range(12)) - selected
        saturated = all(
            any(
                edge in faces[face] and face_counts[face] == 3
                for face in range(6)
            )
            for edge in omitted
        )
        if saturated:
            edge_count = len(selected)
            missing_count = 12 - edge_count
            witness_counts = Counter(missing_by_face.values())
            assert all(witness_counts[edge] >= 1 for edge in omitted)
            assert sum(witness_counts.values()) == t
            a_global = t - missing_count
            b_global = 2 * edge_count - 3 * t
            assert a_global >= 0 and b_global >= 0
            assert b_global + 3 * a_global == 2 * edge_count - 3 * missing_count
            assert q == sum(value * (value - 1) // 2 for value in witness_counts.values())
            assert b_global == b
            assert b_global + 3 * a_global >= missing_count / 2
            assert 11 * edge_count >= 84
            saturated_sizes[edge_count] += 1
            global_chain_checks += 1

    # The face-boundary graph is K_{2,2,2}; audit its isoperimetric minima
    # independently of selected-edge patterns.
    boundary_minima: dict[int, int] = {}
    for subset_mask in range(1 << 6):
        subset = {face for face in range(6) if subset_mask & (1 << face)}
        boundary = sum(
            (left in subset) != (right in subset)
            for left, right in adjacent_pairs
        )
        boundary_minima[len(subset)] = min(
            boundary_minima.get(len(subset), 10**9), boundary
        )

    assert boundary_minima == {0: 0, 1: 4, 2: 6, 3: 6, 4: 6, 5: 4, 6: 0}
    assert sum(pattern_count.values()) == 2902
    assert saturated_sizes == Counter({8: 66, 9: 8})
    assert global_chain_checks == 74

    print("q3_incidence=edges:12,faces:6,adjacent_face_pairs:12")
    print(
        "face_boundary_minima="
        + ",".join(f"t{t}:{boundary_minima[t]}" for t in range(7))
    )
    print(
        "square_free_by_active_faces="
        + ",".join(f"t{t}:{pattern_count[t]}" for t in range(7))
    )
    print(
        "min_twice_local_margin="
        + ",".join(f"t{t}:{min_twice_margin[t]}" for t in range(7))
    )
    print(
        "min_margin_multiplicity="
        + ",".join(f"t{t}:{equality_count[t]}" for t in range(7))
    )
    print(
        "exact_equality_signatures="
        + ";".join(
            f"t{t},q{q},b{b},delta{boundary},a{a}:{count}"
            for (t, q, b, boundary, a), count in sorted(
                exact_equality_signatures.items()
            )
        )
    )
    print("square_saturated_q3=" + ",".join(
        f"e{edges}:{saturated_sizes[edges]}" for edges in sorted(saturated_sizes)
    ))
    print(f"global_chain_checks={global_chain_checks}")
    print("integer_bound_d7=ceil(3136/19)=166")
    print("status=PASS")


if __name__ == "__main__":
    main()
