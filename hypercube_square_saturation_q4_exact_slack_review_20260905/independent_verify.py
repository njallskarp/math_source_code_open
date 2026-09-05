#!/usr/bin/env python3
"""Independent exact audit of the Q3/Q4 slack hinge in the 504/287 bound.

The program deliberately starts from labeled cube vertices and edge sets.  It
does not import the target contribution's checker or certificate.  All local
quantities use Python integers; in particular ``two_sigma`` is twice the
half-integral slack sigma.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations


Edge = tuple[int, int]


def canonical_edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def cube_edges(dimension: int) -> tuple[Edge, ...]:
    return tuple(
        canonical_edge(vertex, vertex ^ (1 << coordinate))
        for coordinate in range(dimension)
        for vertex in range(1 << dimension)
        if not (vertex >> coordinate) & 1
    )


def square_masks(dimension: int, edge_index: dict[Edge, int]) -> tuple[int, ...]:
    masks: list[int] = []
    for first, second in combinations(range(dimension), 2):
        for base in range(1 << dimension):
            if (base >> first) & 1 or (base >> second) & 1:
                continue
            vertices = (
                base,
                base ^ (1 << first),
                base ^ (1 << second),
                base ^ (1 << first) ^ (1 << second),
            )
            boundary = (
                canonical_edge(vertices[0], vertices[1]),
                canonical_edge(vertices[0], vertices[2]),
                canonical_edge(vertices[1], vertices[3]),
                canonical_edge(vertices[2], vertices[3]),
            )
            masks.append(sum(1 << edge_index[edge] for edge in boundary))
    return tuple(masks)


@dataclass(frozen=True)
class SlackData:
    edges: int
    active_faces: int
    repeated_witnesses: int
    inactive_incidences: int
    two_sigma: int


def q3_slack(selected: int, faces: tuple[int, ...]) -> SlackData | None:
    counts = tuple((selected & face).bit_count() for face in faces)
    if any(count == 4 for count in counts):
        return None
    active = tuple(index for index, count in enumerate(counts) if count == 3)
    missing = tuple((faces[index] & ~selected).bit_length() - 1 for index in active)
    t = len(active)
    q = t - len(set(missing))
    b = sum(counts[index] for index in range(len(faces)) if index not in active)
    return SlackData(selected.bit_count(), t, q, b, 2 * b + 4 * q - t)


def q3_equality_patterns() -> tuple[
    tuple[int, ...], tuple[int, ...], Counter[tuple[int, int, int, int]]
]:
    edges = cube_edges(3)
    index = {edge: position for position, edge in enumerate(edges)}
    faces = square_masks(3, index)
    square_free: list[int] = []
    equality: list[int] = []
    profiles: Counter[tuple[int, int, int, int]] = Counter()
    for selected in range(1 << len(edges)):
        data = q3_slack(selected, faces)
        if data is None:
            continue
        square_free.append(selected)
        if data.two_sigma < 0:
            raise AssertionError(f"negative local slack at mask {selected:#x}")
        if data.two_sigma == 0:
            equality.append(selected)
            profiles[
                (
                    data.edges,
                    data.active_faces,
                    data.repeated_witnesses,
                    data.inactive_incidences,
                )
            ] += 1
    return (tuple(square_free), tuple(equality), profiles)


def q3_priced_patterns(max_two_sigma: int) -> tuple[tuple[int, int], ...]:
    edges = cube_edges(3)
    index = {edge: position for position, edge in enumerate(edges)}
    faces = square_masks(3, index)
    priced: list[tuple[int, int]] = []
    for selected in range(1 << len(edges)):
        data = q3_slack(selected, faces)
        if data is not None and data.two_sigma <= max_two_sigma:
            priced.append((selected, data.two_sigma))
    return tuple(priced)


def insert_bit(local_vertex: int, coordinate: int, fixed: int) -> int:
    lower = local_vertex & ((1 << coordinate) - 1)
    upper = local_vertex >> coordinate
    return lower | (fixed << coordinate) | (upper << (coordinate + 1))


def embedded_facet_patterns(
    q3_patterns: tuple[int, ...],
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    q3_edges = cube_edges(3)
    q4_edges = cube_edges(4)
    q4_index = {edge: position for position, edge in enumerate(q4_edges)}
    facets: list[tuple[int, tuple[int, ...]]] = []
    for coordinate in range(4):
        for fixed in (0, 1):
            local_to_global = tuple(
                q4_index[
                    canonical_edge(
                        insert_bit(u, coordinate, fixed),
                        insert_bit(v, coordinate, fixed),
                    )
                ]
                for u, v in q3_edges
            )
            facet_mask = sum(1 << edge for edge in local_to_global)
            patterns = tuple(
                sum(
                    1 << global_edge
                    for local_edge, global_edge in enumerate(local_to_global)
                    if (local_pattern >> local_edge) & 1
                )
                for local_pattern in q3_patterns
            )
            facets.append((facet_mask, patterns))
    return tuple(facets)


def glue_zero_slack_facets(
    facets: tuple[tuple[int, tuple[int, ...]], ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return all global masks whose eight facet restrictions have zero slack."""
    states: set[tuple[int, int]] = {(0, 0)}  # (selected bits, decided bits)
    layer_counts: list[int] = []
    for facet_mask, patterns in facets:
        next_states: set[tuple[int, int]] = set()
        for selected, decided in states:
            overlap = decided & facet_mask
            for pattern in patterns:
                if (selected ^ pattern) & overlap:
                    continue
                next_states.add((selected | pattern, decided | facet_mask))
        states = next_states
        layer_counts.append(len(states))
    all_edges_mask = (1 << len(cube_edges(4))) - 1
    if any(decided != all_edges_mask for _, decided in states):
        raise AssertionError("the eight facets did not decide every Q4 edge")
    return tuple(sorted(selected for selected, _ in states)), tuple(layer_counts)


def embedded_priced_facets(
    local_patterns: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, tuple[tuple[int, int], ...]], ...]:
    q3_edges = cube_edges(3)
    q4_edges = cube_edges(4)
    q4_index = {edge: position for position, edge in enumerate(q4_edges)}
    facets: list[tuple[int, tuple[tuple[int, int], ...]]] = []
    for coordinate in range(4):
        for fixed in (0, 1):
            local_to_global = tuple(
                q4_index[
                    canonical_edge(
                        insert_bit(u, coordinate, fixed),
                        insert_bit(v, coordinate, fixed),
                    )
                ]
                for u, v in q3_edges
            )
            facet_mask = sum(1 << edge for edge in local_to_global)
            patterns = tuple(
                (
                    sum(
                        1 << global_edge
                        for local_edge, global_edge in enumerate(local_to_global)
                        if (local_pattern >> local_edge) & 1
                    ),
                    two_sigma,
                )
                for local_pattern, two_sigma in local_patterns
            )
            facets.append((facet_mask, patterns))
    return tuple(facets)


def glue_with_slack_budget(
    facets: tuple[tuple[int, tuple[tuple[int, int], ...]], ...], budget: int
) -> tuple[tuple[tuple[int, int], ...], tuple[int, ...]]:
    """Enumerate every global pattern with total facet 2*sigma <= budget."""
    states: set[tuple[int, int, int]] = {(0, 0, 0)}
    layer_counts: list[int] = []
    for facet_mask, patterns in facets:
        next_states: set[tuple[int, int, int]] = set()
        for selected, decided, cost in states:
            overlap = decided & facet_mask
            for pattern, pattern_cost in patterns:
                new_cost = cost + pattern_cost
                if new_cost > budget or (selected ^ pattern) & overlap:
                    continue
                next_states.add((selected | pattern, decided | facet_mask, new_cost))
        states = next_states
        layer_counts.append(len(states))
    all_edges_mask = (1 << len(cube_edges(4))) - 1
    if any(decided != all_edges_mask for _, decided, _ in states):
        raise AssertionError("the eight facets did not decide every Q4 edge")
    return (
        tuple(sorted((selected, cost) for selected, _, cost in states)),
        tuple(layer_counts),
    )


def permute_vertex(vertex: int, coordinate_image: tuple[int, ...]) -> int:
    return sum(
        ((vertex >> old_coordinate) & 1) << new_coordinate
        for old_coordinate, new_coordinate in enumerate(coordinate_image)
    )


def hypercube_orbit(pattern: int) -> frozenset[int]:
    edges = cube_edges(4)
    edge_index = {edge: index for index, edge in enumerate(edges)}
    orbit: set[int] = set()
    for coordinate_image in permutations(range(4)):
        for translation in range(16):
            transformed = 0
            for edge_index_old, (u, v) in enumerate(edges):
                if not (pattern >> edge_index_old) & 1:
                    continue
                image = canonical_edge(
                    permute_vertex(u, coordinate_image) ^ translation,
                    permute_vertex(v, coordinate_image) ^ translation,
                )
                transformed |= 1 << edge_index[image]
            orbit.add(transformed)
    return frozenset(orbit)


def facet_capacity_audit(
    facets: tuple[tuple[int, tuple[int, ...]], ...],
) -> dict[int, int]:
    """Maximum edges supported by only k designated nonempty Q3 facets."""
    q4_edge_count = len(cube_edges(4))
    incident_facets = tuple(
        frozenset(index for index, (mask, _) in enumerate(facets) if mask >> edge & 1)
        for edge in range(q4_edge_count)
    )
    if set(map(len, incident_facets)) != {3}:
        raise AssertionError("a Q4 edge must lie in exactly three Q3 facets")
    maxima: dict[int, int] = {}
    for chosen_bits in range(1 << len(facets)):
        chosen = frozenset(
            index for index in range(len(facets)) if chosen_bits >> index & 1
        )
        capacity = sum(neighborhood <= chosen for neighborhood in incident_facets)
        maxima[len(chosen)] = max(maxima.get(len(chosen), 0), capacity)
    return maxima


def main() -> None:
    square_free, equality, profiles = q3_equality_patterns()
    facets = embedded_facet_patterns(equality)
    compatible, layer_counts = glue_zero_slack_facets(facets)
    capacities = facet_capacity_audit(facets)
    priced_facets = embedded_priced_facets(q3_priced_patterns(6))
    low_slack, low_slack_layers = glue_with_slack_budget(priced_facets, 6)
    minimizers = tuple(selected for selected, cost in low_slack if selected)

    expected_profiles = Counter({(0, 0, 0, 0): 1, (7, 4, 0, 2): 48})
    assert len(square_free) == 2902
    assert profiles == expected_profiles
    assert compatible == (0,)
    assert capacities[3] == 1 < 7
    assert capacities[6] == 12 < 14
    assert len(low_slack) == 65
    assert all(cost == 0 for selected, cost in low_slack if not selected)
    assert all(cost == 6 for selected, cost in low_slack if selected)
    assert len(minimizers) == 64
    assert {selected.bit_count() for selected in minimizers} == {17}

    q4_edges = cube_edges(4)
    q4_edge_index = {edge: index for index, edge in enumerate(q4_edges)}
    q4_faces = square_masks(4, q4_edge_index)
    assert all(
        all((selected & face).bit_count() <= 3 for face in q4_faces)
        for selected in minimizers
    )
    local_cost_profiles = Counter(
        tuple(
            sorted(
                dict(patterns)[selected & facet_mask]
                for facet_mask, patterns in priced_facets
            )
        )
        for selected in minimizers
    )
    assert local_cost_profiles == Counter({(0, 0, 0, 0, 0, 0, 0, 6): 64})
    assert hypercube_orbit(minimizers[0]) == frozenset(minimizers)

    # Eight omitted edges meet the 24 squares exactly once each, so the
    # elementary 24-edge cap for a square-free Q4 is attained.
    exact_cover_edges = (
        (0, 1),
        (4, 6),
        (3, 7),
        (14, 15),
        (2, 10),
        (9, 11),
        (8, 12),
        (5, 13),
    )
    omitted = sum(1 << q4_edge_index[edge] for edge in exact_cover_edges)
    square_free_24 = ((1 << len(q4_edges)) - 1) ^ omitted
    assert square_free_24.bit_count() == 24
    assert all((square_free_24 & face).bit_count() == 3 for face in q4_faces)

    strengthened_constant = Fraction(84, 47)
    target_constant = Fraction(504, 287)
    bound_d7 = Fraction(84 * 7 * 2**7, 47 * 7 + 121)
    integer_bound_d7 = (bound_d7.numerator + bound_d7.denominator - 1) // bound_d7.denominator
    assert strengthened_constant - target_constant == Fraction(60, 1927)
    assert integer_bound_d7 == 168

    digest_material = "\n".join(
        [
            *(f"q3:{mask:03x}" for mask in equality),
            *(f"q4:{mask:08x}" for mask in compatible),
            *(f"q4min:{mask:08x}" for mask in minimizers),
            f"q4max:{square_free_24:08x}",
            "layers:" + ",".join(map(str, layer_counts)),
            "low-slack-layers:" + ",".join(map(str, low_slack_layers)),
            "capacity:" + ",".join(f"{k}:{capacities[k]}" for k in sorted(capacities)),
        ]
    ).encode("ascii")

    print(f"q3_all_patterns={1 << len(cube_edges(3))}")
    print(f"q3_square_free_patterns={len(square_free)}")
    print(f"q3_zero_slack_patterns={len(equality)}")
    print("q3_zero_slack_profiles=1*(0,0,0,0)+48*(7,4,0,2)")
    print("q4_zero_slack_compatible_patterns=1")
    print("q4_only_compatible_pattern=empty")
    print(f"facet_gluing_layer_counts={','.join(map(str, layer_counts))}")
    print(f"max_supported_edges_k3={capacities[3]}")
    print(f"max_supported_edges_k6={capacities[6]}")
    print("q4_min_positive_facet_slack=3")
    print("q4_minimizers=64")
    print("q4_minimizer_edges=17")
    print("q4_minimizer_orbits=1")
    print("q4_minimizer_stabilizer_order=6")
    print("q4_square_free_edge_cap=24_attained")
    print(f"low_slack_layer_counts={','.join(map(str, low_slack_layers))}")
    print("strengthened_bound=sat(Q_d,Q_2)>=84*d*2^d/(47*d+121)_for_d>=4")
    print("strengthened_asymptotic_constant=84/47")
    print(f"integer_bound_d7={integer_bound_d7}")
    print(f"audit_sha256={sha256(digest_material).hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
