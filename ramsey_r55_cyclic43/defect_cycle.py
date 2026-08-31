#!/usr/bin/env python3
"""Classify the length-one neutral component through the primary Cyclic(43) optimum."""

from __future__ import annotations

import argparse
import itertools
import json
from array import array
from collections import Counter
from pathlib import Path

from local_rigidity import (
    complete_graph_edges,
    direct_count,
    is_monochromatic,
    initial_colors,
)
from solve_cyclic43 import ORDER, cyclic_distance, edge, load_certificate


def position_edge(position: int) -> tuple[int, int]:
    if not 0 <= position < ORDER:
        raise ValueError(position)
    return (0, ORDER - 1) if position == ORDER - 1 else (position, position + 1)


def edge_position(changed_edge: tuple[int, int]) -> int:
    if changed_edge == (0, ORDER - 1):
        return ORDER - 1
    if changed_edge[1] == changed_edge[0] + 1:
        return changed_edge[0]
    raise ValueError(f"not a cyclic length-one edge: {changed_edge}")


def transport_position(index: int) -> int:
    base = 42 if index % 2 == 0 else 37
    return (base + 17 * (index // 2)) % ORDER


def analyze_cycle(
    certificate: Path,
    fu_malik_certificate: Path,
    bridge_path: Path,
    direct_verify: bool = False,
    all_edge_neighbors: bool = False,
) -> dict[str, object]:
    flips = load_certificate(certificate)
    fu_malik_flips = load_certificate(fu_malik_certificate)
    colors, edges = initial_colors(flips)
    edge_ids, _ = complete_graph_edges()
    incident = [array("I") for _ in edges]
    red_counts = array("b")

    for vertices in itertools.combinations(range(ORDER), 5):
        five_id = len(red_counts)
        ids = [
            edge_ids[edge(a, b)] for a, b in itertools.combinations(vertices, 2)
        ]
        red_counts.append(sum(colors[edge_id] for edge_id in ids))
        for edge_id in ids:
            incident[edge_id].append(five_id)

    if len(red_counts) != 962_598:
        raise AssertionError(len(red_counts))
    if any(len(indexes) != 10_660 for indexes in incident):
        raise AssertionError("incorrect edge/five-set incidence")

    length_one_edges = [position_edge(position) for position in range(ORDER)]
    length_one_ids = [edge_ids[item] for item in length_one_edges]
    current_count = sum(is_monochromatic(count) for count in red_counts)
    if current_count != 2:
        raise AssertionError(current_count)

    def resulting_count(edge_id: int) -> int:
        delta = -1 if colors[edge_id] else 1
        result = current_count
        for five_id in incident[edge_id]:
            count = red_counts[five_id]
            result += is_monochromatic(count + delta) - is_monochromatic(count)
        return result

    def toggle(edge_id: int) -> None:
        nonlocal current_count
        delta = -1 if colors[edge_id] else 1
        for five_id in incident[edge_id]:
            count = red_counts[five_id]
            current_count += (
                is_monochromatic(count + delta) - is_monochromatic(count)
            )
            red_counts[five_id] += delta
        colors[edge_id] = not colors[edge_id]

    period = 2 * ORDER
    positions = [transport_position(index) for index in range(period)]
    if Counter(positions) != Counter({position: 2 for position in range(ORDER)}):
        raise AssertionError("transport does not use every edge twice")

    relative_mask = 0
    seen = {relative_mask: 0}
    active_flips = flips.copy()
    objective_sequence = [current_count]
    neutral_degrees = []
    neutral_neighbor_positions = []
    all_edge_neutral_degrees = []
    non_length_one_neutral_edges: list[dict[str, object]] = []
    aggregate_neighbor_objectives: Counter[int] = Counter()
    neighbor_spectrum_indices: dict[tuple[tuple[int, int], ...], int] = {}
    neighbor_spectrum_class_states: list[list[int]] = []
    off_component_minima = []
    off_component_minimizer_counts = []
    off_component_minimizer_positions = []
    off_component_minimizer_lengths: Counter[int] = Counter()
    fu_malik_state_index: int | None = None

    for index, position in enumerate(positions):
        if all_edge_neighbors:
            resulting_counts = [
                resulting_count(edge_id) for edge_id in range(len(edges))
            ]
            state_spectrum = Counter(resulting_counts)
            aggregate_neighbor_objectives.update(state_spectrum)
            spectrum_signature = tuple(sorted(state_spectrum.items()))
            spectrum_class = neighbor_spectrum_indices.get(spectrum_signature)
            if spectrum_class is None:
                spectrum_class = len(neighbor_spectrum_class_states)
                neighbor_spectrum_indices[spectrum_signature] = spectrum_class
                neighbor_spectrum_class_states.append([])
            neighbor_spectrum_class_states[spectrum_class].append(index)
            all_neutral_ids = [
                edge_id
                for edge_id, count in enumerate(resulting_counts)
                if count == 2
            ]
            all_edge_neutral_degrees.append(len(all_neutral_ids))
            neutral = sorted(
                edge_position(edges[edge_id])
                for edge_id in all_neutral_ids
                if edges[edge_id] in length_one_edges
            )
            other_edges = [
                edges[edge_id]
                for edge_id in all_neutral_ids
                if edges[edge_id] not in length_one_edges
            ]
            if other_edges:
                non_length_one_neutral_edges.append(
                    {"state_index": index, "edges": other_edges}
                )
            cycle_neighbor_ids = {
                length_one_ids[positions[(index - 1) % period]],
                length_one_ids[positions[index]],
            }
            off_minimum = min(
                count
                for edge_id, count in enumerate(resulting_counts)
                if edge_id not in cycle_neighbor_ids
            )
            off_minimizers = [
                edge_id
                for edge_id, count in enumerate(resulting_counts)
                if edge_id not in cycle_neighbor_ids and count == off_minimum
            ]
            off_component_minima.append(off_minimum)
            off_component_minimizer_counts.append(len(off_minimizers))
            if any(
                cyclic_distance(*edges[edge_id]) != 1
                for edge_id in off_minimizers
            ):
                raise AssertionError("off-component minimizer is not length one")
            off_component_minimizer_positions.append(
                sorted(edge_position(edges[edge_id]) for edge_id in off_minimizers)
            )
            off_component_minimizer_lengths.update(
                cyclic_distance(*edges[edge_id]) for edge_id in off_minimizers
            )
        else:
            neutral = [
                candidate
                for candidate, edge_id in enumerate(length_one_ids)
                if resulting_count(edge_id) == 2
            ]
        expected = sorted(
            {positions[(index - 1) % period], positions[index]}
        )
        if neutral != expected:
            raise AssertionError((index, neutral, expected))
        neutral_degrees.append(len(neutral))
        neutral_neighbor_positions.append(neutral)

        changed_edge = length_one_edges[position]
        toggle(length_one_ids[position])
        relative_mask ^= 1 << position
        if changed_edge in active_flips:
            active_flips.remove(changed_edge)
        else:
            active_flips.add(changed_edge)
        objective_sequence.append(current_count)
        state_index = index + 1

        if active_flips == fu_malik_flips:
            if fu_malik_state_index is not None:
                raise AssertionError("Fu-Malik state occurs more than once")
            fu_malik_state_index = state_index
        if state_index < period:
            if relative_mask in seen:
                raise AssertionError((state_index, seen[relative_mask]))
            seen[relative_mask] = state_index
        elif relative_mask != 0:
            raise AssertionError("cycle does not close")

    bridge = json.loads(bridge_path.read_text())
    bridge_positions = [
        edge_position(tuple(step["new_reversed_edge"])) for step in bridge["steps"]
    ]
    if fu_malik_state_index is None:
        raise AssertionError("cycle does not visit Fu-Malik certificate")
    if positions[fu_malik_state_index:] != bridge_positions:
        raise AssertionError("bridge is not the closing cycle segment")
    if active_flips != flips:
        raise AssertionError("cycle endpoint does not equal primary certificate")
    if set(objective_sequence) != {2}:
        raise AssertionError(objective_sequence)

    result: dict[str, object] = {
        "certificate": certificate.name,
        "fu_malik_certificate": fu_malik_certificate.name,
        "bridge": bridge_path.name,
        "order": ORDER,
        "edge_class": "cyclic length one",
        "transport_even_formula": "p_(2k) = 42 + 17k mod 43",
        "transport_odd_formula": "p_(2k+1) = 37 + 17k mod 43",
        "transport_period": period,
        "edge_positions": positions,
        "edge_position_multiplicity": 2,
        "distinct_states_before_return": len(seen),
        "returns_to_primary": relative_mask == 0 and active_flips == flips,
        "monochromatic_k5_count_at_every_state": 2,
        "neutral_length_one_degree_histogram": {
            str(degree): count
            for degree, count in sorted(Counter(neutral_degrees).items())
        },
        "neutral_neighbors_are_predecessor_and_successor": all(
            neighbors
            == sorted({positions[(index - 1) % period], positions[index]})
            for index, neighbors in enumerate(neutral_neighbor_positions)
        ),
        "fu_malik_state_index": fu_malik_state_index,
        "closing_bridge_length": len(bridge_positions),
        "closing_bridge_positions": bridge_positions,
        "length_one_neutral_component_is_cycle_C86": True,
        "scope_note": (
            "All 43 cyclic length-one reversals are tested at each of the 86 "
            "states. This classifies the connected optimum-2 component through "
            "the primary certificate inside the length-one edge subcube only; "
            "other edge lengths may provide exits."
        ),
    }
    if direct_verify:
        direct_colors, _ = initial_colors(flips)
        direct_counts = []
        for position in positions:
            count, _ = direct_count(direct_colors, edge_ids)
            direct_counts.append(count)
            edge_id = edge_ids[position_edge(position)]
            direct_colors[edge_id] = not direct_colors[edge_id]
        if set(direct_counts) != {2} or direct_colors != initial_colors(flips)[0]:
            raise AssertionError((direct_counts, direct_colors == colors))
        result["direct_recount_state_count"] = len(direct_counts)
        result["direct_recount_all_states_equal_two"] = True
    if all_edge_neighbors:
        expected_spectrum_states = [
            list(range(parity, period, 2)) for parity in range(2)
        ]
        if neighbor_spectrum_class_states != expected_spectrum_states:
            raise AssertionError(neighbor_spectrum_class_states)
        spectrum_signatures: list[tuple[tuple[int, int], ...] | None] = [
            None
        ] * len(neighbor_spectrum_indices)
        for signature, class_index in neighbor_spectrum_indices.items():
            spectrum_signatures[class_index] = signature
        if any(signature is None for signature in spectrum_signatures):
            raise AssertionError(spectrum_signatures)

        expected_minimizer_positions = []
        for state_index in range(period):
            k = state_index // 2
            final_offset = 0 if state_index % 2 else -1
            expected_minimizer_positions.append(
                sorted(
                    17 * offset % ORDER
                    for offset in range(k - 8, k + final_offset + 1)
                )
            )
        if off_component_minimizer_positions != expected_minimizer_positions:
            raise AssertionError("modular minimizer window mismatch")

        result["all_edge_neighbor_checks"] = period * len(edges)
        result["aggregate_all_edge_neighbor_objective_histogram"] = {
            str(objective): count
            for objective, count in sorted(aggregate_neighbor_objectives.items())
        }
        result["distinct_all_edge_neighbor_spectrum_count"] = len(
            neighbor_spectrum_indices
        )
        result["neighbor_spectra_depend_only_on_state_parity"] = True
        result["even_state_all_edge_neighbor_objective_histogram"] = {
            str(objective): count for objective, count in spectrum_signatures[0]
        }
        result["odd_state_all_edge_neighbor_objective_histogram"] = {
            str(objective): count for objective, count in spectrum_signatures[1]
        }
        result["all_edge_neighbor_spectrum_class_size_histogram"] = {
            str(size): count
            for size, count in sorted(
                Counter(map(len, neighbor_spectrum_class_states)).items()
            )
        }
        result["neutral_all_edge_degree_histogram"] = {
            str(degree): count
            for degree, count in sorted(Counter(all_edge_neutral_degrees).items())
        }
        result["states_with_non_length_one_neutral_edges"] = (
            non_length_one_neutral_edges
        )
        result["full_one_flip_neutral_component_is_cycle_C86"] = not (
            non_length_one_neutral_edges
        )
        result["off_component_neighbor_minimum"] = min(off_component_minima)
        result["off_component_neighbor_minimum_histogram"] = {
            str(minimum): count
            for minimum, count in sorted(Counter(off_component_minima).items())
        }
        result["off_component_minimizer_count_histogram"] = {
            str(count): frequency
            for count, frequency in sorted(
                Counter(off_component_minimizer_counts).items()
            )
        }
        result["off_component_minimizer_count_total"] = sum(
            off_component_minimizer_counts
        )
        result["off_component_minimizer_cyclic_length_histogram"] = {
            str(length): count
            for length, count in sorted(off_component_minimizer_lengths.items())
        }
        result["off_component_minimizers_follow_modular_window"] = True
        result["off_component_even_state_minimizer_formula"] = (
            "S_(2k) = {17j mod 43 : k-8 <= j <= k-1}"
        )
        result["off_component_odd_state_minimizer_formula"] = (
            "S_(2k+1) = {17j mod 43 : k-8 <= j <= k}"
        )
        if not non_length_one_neutral_edges:
            result["scope_note"] = (
                "All 903 single-edge reversals are tested at each of the 86 "
                "states. This classifies the complete one-flip-connected "
                "optimum-2 component through the primary certificate; paths "
                "through higher objective values remain outside the claim."
            )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--fu-malik", type=Path, required=True)
    parser.add_argument("--bridge", type=Path, required=True)
    parser.add_argument("--direct-verify", action="store_true")
    parser.add_argument("--all-edge-neighbors", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze_cycle(
        args.certificate,
        args.fu_malik,
        args.bridge,
        direct_verify=args.direct_verify,
        all_edge_neighbors=args.all_edge_neighbors,
    )
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
