#!/usr/bin/env python3

import json
import unittest
from collections import Counter
from math import comb
from pathlib import Path

from defect_cycle import analyze_cycle, position_edge, transport_position
from defect_orbit_tube import prefix_chain_distance_histogram
from escape_component import analyze as analyze_escape_component
from local_rigidity import complete_graph_edges, direct_count, initial_colors
from objective_four_frontier import cycle_and_boundary_states, rotation_orbit
from solve_cyclic43 import load_certificate, verify_flips


HERE = Path(__file__).resolve().parent


class DirectVerifierTests(unittest.TestCase):
    def test_prefix_chain_histogram_closed_form(self) -> None:
        for length in range(13):
            brute_force = Counter()
            for mask in range(1 << length):
                brute_force[
                    min(
                        (mask ^ ((1 << prefix) - 1)).bit_count()
                        for prefix in range(length + 1)
                    )
                ] += 1
            self.assertEqual(
                prefix_chain_distance_histogram(length), dict(brute_force)
            )

    def test_seed_has_exactly_43_red_cliques(self) -> None:
        result = verify_flips(set())
        self.assertEqual(result["red_k5_count"], 43)
        self.assertEqual(result["blue_k5_count"], 0)

    def test_primary_certificate_has_exactly_two(self) -> None:
        result = verify_flips(load_certificate(HERE / "certificate.json"))
        self.assertEqual(result["monochromatic_k5_count"], 2)
        self.assertEqual(result["red_k5_count"], 2)
        self.assertEqual(result["blue_k5_count"], 0)

    def test_fu_malik_certificate_has_exactly_two(self) -> None:
        result = verify_flips(load_certificate(HERE / "certificate-fm.json"))
        self.assertEqual(result["monochromatic_k5_count"], 2)
        self.assertEqual(result["red_k5_count"], 0)
        self.assertEqual(result["blue_k5_count"], 2)

    def test_certificates_record_exact_optimum(self) -> None:
        for name in ("certificate.json", "certificate-fm.json"):
            payload = json.loads((HERE / name).read_text())
            self.assertEqual(payload["optimum"], 2)

    def test_persisted_local_rigidity_minimizers_recount_to_two(self) -> None:
        cases = (
            ("certificate.json", "local-rigidity-primary.json", "radius_two_minimizer_sample"),
            ("certificate-fm.json", "local-rigidity-fm.json", "radius_two_minimizer_sample"),
            (
                "certificate.json",
                "local-rigidity-radius3-primary.json",
                "radius_three_minimizer_sample",
            ),
            (
                "certificate-fm.json",
                "local-rigidity-radius3-fm.json",
                "radius_three_minimizer_sample",
            ),
        )
        edge_ids, _ = complete_graph_edges()
        for certificate_name, result_name, sample_field in cases:
            colors, _ = initial_colors(load_certificate(HERE / certificate_name))
            payload = json.loads((HERE / result_name).read_text())
            for changed_edge in payload[sample_field]:
                normalized = tuple(changed_edge)
                colors[edge_ids[normalized]] = not colors[edge_ids[normalized]]
            count, _ = direct_count(colors, edge_ids)
            self.assertEqual(count, 2)

    def test_persisted_radius_six_searches_exclude_improvement(self) -> None:
        for name in (
            "local-rigidity-radius6-primary.json",
            "local-rigidity-radius6-fm.json",
        ):
            payload = json.loads((HERE / name).read_text())
            self.assertEqual(payload["radius"], 6)
            self.assertEqual(payload["base_monochromatic_k5_count"], 2)
            self.assertFalse(payload["improvement_found"])
            self.assertEqual(payload["exact_minimum_through_requested_radius"], 2)
            self.assertEqual(len(payload["expanded_by_depth"]), 7)
            self.assertEqual(
                payload["expanded_by_depth"][1:],
                payload["distinct_nonroot_states_by_depth"][1:],
            )

    def test_plateau_bridge_recounts_and_reaches_primary(self) -> None:
        payload = json.loads((HERE / "plateau-bridge.json").read_text())
        source = load_certificate(HERE / payload["certificate"])
        target = load_certificate(HERE / payload["target_certificate"])
        expected_difference = source ^ target
        self.assertEqual(len(expected_difference), 15)
        self.assertEqual(
            {tuple(item) for item in payload["source_target_differing_edges"]},
            expected_difference,
        )

        edge_ids, _ = complete_graph_edges()
        colors, _ = initial_colors(source)
        changed = set()
        for expected_radius, step in enumerate(payload["steps"], start=1):
            changed_edge = tuple(step["new_reversed_edge"])
            changed.add(changed_edge)
            colors[edge_ids[changed_edge]] = not colors[edge_ids[changed_edge]]
            count, witnesses = direct_count(colors, edge_ids)
            self.assertEqual(step["radius"], expected_radius)
            self.assertEqual(count, 2)
            self.assertEqual([list(item) for item in witnesses], step["monochromatic_k5"])

        self.assertEqual(changed, expected_difference)
        self.assertTrue(payload["path_endpoint_matches_target"])

    def test_compact_defect_orbit_certificate(self) -> None:
        payload = json.loads((HERE / "defect-orbit-primary.json").read_text())
        positions = payload["edge_positions"]
        expected = [
            ((42 if index % 2 == 0 else 37) + 17 * (index // 2)) % 43
            for index in range(37)
        ]
        self.assertEqual(positions, expected)
        self.assertEqual(len(set(positions)), 37)
        self.assertEqual((37 + 17 * 18) % 43, payload["first_repeated_next_position"])

        edge_ids, _ = complete_graph_edges()
        colors, _ = initial_colors(load_certificate(HERE / payload["certificate"]))
        changed = []
        for position in positions:
            changed_edge = (0, 42) if position == 42 else (position, position + 1)
            changed.append(changed_edge)
            colors[edge_ids[changed_edge]] = not colors[edge_ids[changed_edge]]
        count, witnesses = direct_count(colors, edge_ids)
        self.assertEqual(count, 2)
        self.assertEqual(
            [list(item) for item in witnesses],
            payload["terminal_monochromatic_k5"],
        )

        escape = tuple(payload["terminal_unused_edge_minimizers"][0])
        colors[edge_ids[escape]] = not colors[edge_ids[escape]]
        escape_count, _ = direct_count(colors, edge_ids)
        self.assertEqual(escape_count, payload["terminal_unused_edge_minimum_count"])
        self.assertEqual(
            sum(payload["terminal_unused_edge_result_count_histogram"].values()),
            payload["terminal_unused_edge_count"],
        )

    def test_full_one_flip_neutral_component_is_cycle_c86(self) -> None:
        payload = json.loads((HERE / "defect-cycle.json").read_text())
        positions = payload["edge_positions"]
        self.assertEqual(
            positions, [transport_position(index) for index in range(86)]
        )
        self.assertEqual(
            Counter(positions), Counter({position: 2 for position in range(43)})
        )
        self.assertEqual(payload["distinct_states_before_return"], 86)
        self.assertEqual(payload["neutral_length_one_degree_histogram"], {"2": 86})
        self.assertEqual(payload["all_edge_neighbor_checks"], 86 * 903)
        self.assertEqual(payload["neutral_all_edge_degree_histogram"], {"2": 86})
        self.assertEqual(payload["states_with_non_length_one_neutral_edges"], [])
        self.assertTrue(payload["full_one_flip_neutral_component_is_cycle_C86"])
        self.assertTrue(payload["neutral_neighbors_are_predecessor_and_successor"])
        self.assertTrue(payload["direct_recount_all_states_equal_two"])
        self.assertEqual(payload["off_component_neighbor_minimum"], 3)
        self.assertEqual(
            payload["off_component_neighbor_minimum_histogram"], {"3": 86}
        )
        self.assertEqual(
            payload["off_component_minimizer_count_histogram"],
            {"8": 43, "9": 43},
        )
        self.assertEqual(payload["off_component_minimizer_count_total"], 731)
        self.assertEqual(
            payload["off_component_minimizer_cyclic_length_histogram"],
            {"1": 731},
        )
        self.assertTrue(payload["off_component_minimizers_follow_modular_window"])
        self.assertTrue(payload["neighbor_spectra_depend_only_on_state_parity"])
        self.assertEqual(payload["distinct_all_edge_neighbor_spectrum_count"], 2)
        self.assertEqual(
            payload["all_edge_neighbor_spectrum_class_size_histogram"],
            {"43": 2},
        )

        aggregate_spectrum = payload[
            "aggregate_all_edge_neighbor_objective_histogram"
        ]
        even_spectrum = payload["even_state_all_edge_neighbor_objective_histogram"]
        odd_spectrum = payload["odd_state_all_edge_neighbor_objective_histogram"]
        self.assertEqual(sum(aggregate_spectrum.values()), 86 * 903)
        self.assertEqual(sum(even_spectrum.values()), 903)
        self.assertEqual(sum(odd_spectrum.values()), 903)
        self.assertEqual(even_spectrum["3"], 8)
        self.assertEqual(odd_spectrum["3"], 9)
        self.assertEqual(
            aggregate_spectrum,
            {
                objective: 43
                * (
                    even_spectrum.get(objective, 0)
                    + odd_spectrum.get(objective, 0)
                )
                for objective in aggregate_spectrum
            },
        )

        primary = load_certificate(HERE / payload["certificate"])
        fu_malik = load_certificate(HERE / payload["fu_malik_certificate"])
        active = primary.copy()
        relative_mask = 0
        seen = {relative_mask}
        edge_ids, _ = complete_graph_edges()
        colors, _ = initial_colors(primary)
        direct_samples = {38, 50, 70, 85}
        for state_index, position in enumerate(positions, start=1):
            changed_edge = position_edge(position)
            relative_mask ^= 1 << position
            if changed_edge in active:
                active.remove(changed_edge)
            else:
                active.add(changed_edge)
            colors[edge_ids[changed_edge]] = not colors[edge_ids[changed_edge]]
            if state_index < 86:
                self.assertNotIn(relative_mask, seen)
                seen.add(relative_mask)
            if state_index == payload["fu_malik_state_index"]:
                self.assertEqual(active, fu_malik)
            if state_index in direct_samples:
                count, _ = direct_count(colors, edge_ids)
                self.assertEqual(count, 2)
        self.assertEqual(relative_mask, 0)
        self.assertEqual(active, primary)

        rerun = analyze_cycle(
            HERE / payload["certificate"],
            HERE / payload["fu_malik_certificate"],
            HERE / payload["bridge"],
        )
        for field in (
            "edge_positions",
            "distinct_states_before_return",
            "neutral_length_one_degree_histogram",
            "fu_malik_state_index",
            "closing_bridge_positions",
            "length_one_neutral_component_is_cycle_C86",
        ):
            self.assertEqual(rerun[field], payload[field])

    def test_complete_sublevel_three_component_certificate(self) -> None:
        payload = json.loads((HERE / "escape-component.json").read_text())
        self.assertEqual(payload["objective_two_vertex_count"], 86)
        self.assertEqual(payload["objective_three_boundary_vertex_count"], 731)
        self.assertEqual(payload["candidate_sublevel_three_vertex_count"], 817)
        self.assertEqual(payload["candidate_sublevel_three_edge_count"], 1505)
        self.assertEqual(payload["boundary_component_count"], 43)
        self.assertEqual(payload["boundary_component_size_histogram"], {"17": 43})
        self.assertEqual(
            payload["boundary_induced_degree_histogram"], {"1": 86, "2": 645}
        )
        self.assertEqual(payload["boundary_induced_edge_count"], 688)
        self.assertEqual(payload["center_boundary_edge_count"], 731)
        self.assertEqual(payload["center_induced_edge_count"], 86)
        self.assertEqual(payload["boundary_rotation_orbit_count"], 17)
        self.assertEqual(payload["boundary_dihedral_orbit_count"], 9)
        self.assertEqual(payload["direct_recount_representative_count"], 17)
        self.assertEqual(
            payload["all_edge_rotation_representative_neighbor_checks"],
            17 * 903,
        )
        self.assertEqual(
            payload["symmetry_lifted_boundary_neighbor_checks"], 731 * 903
        )
        self.assertTrue(payload["boundary_vertices_are_distinct"])
        self.assertTrue(payload["boundary_components_are_P17"])
        self.assertTrue(
            payload["each_boundary_vertex_has_unique_objective_two_neighbor"]
        )
        self.assertTrue(
            payload["all_objective_three_neighbors_remain_in_boundary_paths"]
        )
        self.assertTrue(payload["full_sublevel_three_component_through_C86_is_closed"])
        self.assertTrue(
            payload[
                "full_sublevel_three_component_through_C86_is_C86_plus_43_P17"
            ]
        )

        aggregate = payload["aggregate_boundary_neighbor_objective_histogram"]
        self.assertEqual(sum(aggregate.values()), 731 * 903)
        self.assertEqual(aggregate["2"], 731)
        self.assertEqual(aggregate["3"], 2 * 688)
        degrees = payload["candidate_sublevel_three_degree_histogram"]
        self.assertEqual(
            sum(int(degree) * count for degree, count in degrees.items()),
            2 * 1505,
        )

        records = payload["boundary_dihedral_representative_records"]
        self.assertEqual(len(records), 9)
        primary = load_certificate(HERE / payload["certificate"])
        edge_ids, _ = complete_graph_edges()
        for record in records:
            colors, _ = initial_colors(primary)
            if record["center_parity"]:
                changed_edge = position_edge(42)
                colors[edge_ids[changed_edge]] = not colors[edge_ids[changed_edge]]
            exit_edge = position_edge(record["exit_position_orbit"][0])
            colors[edge_ids[exit_edge]] = not colors[edge_ids[exit_edge]]
            count, witnesses = direct_count(colors, edge_ids)
            self.assertEqual(count, 3)
            self.assertEqual(
                [list(witness) for witness in witnesses],
                record["direct_recount_witnesses"],
            )
            self.assertEqual(sum(record["neighbor_objective_histogram"].values()), 903)

        rerun = analyze_escape_component(
            HERE / payload["certificate"], HERE / payload["cycle_certificate"]
        )
        for field in (
            "objective_three_boundary_vertex_count",
            "boundary_component_size_histogram",
            "boundary_induced_degree_histogram",
            "candidate_sublevel_three_vertex_count",
            "candidate_sublevel_three_edge_count",
            "even_exit_dihedral_orbits",
            "odd_exit_dihedral_orbits",
        ):
            self.assertEqual(rerun[field], payload[field])

    def test_complete_sublevel_four_component_certificate(self) -> None:
        payload = json.loads((HERE / "objective-four-component.json").read_text())
        self.assertTrue(payload["complete_sublevel_four_component_is_closed"])
        self.assertEqual(payload["first_objective_four_frontier_vertex_count"], 3311)
        self.assertEqual(
            payload["first_objective_four_frontier_rotation_orbit_count"], 77
        )
        self.assertEqual(payload["additional_objective_four_rotation_orbit_count"], 1)
        self.assertEqual(payload["objective_four_component_rotation_orbit_count"], 78)
        self.assertEqual(payload["objective_four_component_vertex_count"], 3354)
        self.assertEqual(payload["complete_sublevel_four_component_vertex_count"], 4171)
        self.assertEqual(payload["complete_sublevel_four_component_edge_count"], 10621)
        self.assertEqual(payload["objective_four_directed_center_edge_count"], 946)
        self.assertEqual(payload["objective_four_directed_boundary_edge_count"], 4988)
        self.assertEqual(payload["objective_four_induced_edge_count"], 3182)
        self.assertEqual(
            payload["direct_recount_objective_four_representative_count"], 78
        )
        self.assertEqual(
            payload["new_objective_at_most_three_rotation_orbit_histogram"],
            {"0": 0, "1": 0, "2": 0, "3": 0},
        )

        aggregate = payload["aggregate_objective_four_neighbor_objective_histogram"]
        self.assertEqual(sum(aggregate.values()), 3354 * 903)
        self.assertEqual(aggregate["2"], 946)
        self.assertEqual(aggregate["3"], 4988)
        self.assertEqual(aggregate["4"], 2 * 3182)
        degrees = payload["objective_four_vertex_sublevel_four_degree_histogram"]
        self.assertEqual(sum(degrees.values()), 3354)
        self.assertEqual(
            sum(int(degree) * count for degree, count in degrees.items()),
            946 + 4988 + 2 * 3182,
        )
        self.assertEqual(
            1505 + aggregate["2"] + aggregate["3"] + aggregate["4"] // 2,
            10621,
        )

        primary = frozenset(load_certificate(HERE / payload["certificate"]))
        cycle = json.loads((HERE / payload["cycle_certificate"]).read_text())
        centers, boundaries = cycle_and_boundary_states(
            primary, cycle["edge_positions"]
        )
        self.assertEqual(len(set(centers)), 86)
        self.assertEqual(len(boundaries), 731)
        self.assertEqual(len(rotation_orbit(centers[0])), 43)

    def test_complete_sublevel_five_component_certificate(self) -> None:
        payload = json.loads((HERE / "objective-five-component.json").read_text())
        self.assertTrue(payload["complete_sublevel_five_component_is_closed"])
        self.assertEqual(payload["objective_five_frontier_rotation_orbit_count"], 306)
        self.assertEqual(payload["objective_five_frontier_vertex_count"], 13_158)
        self.assertEqual(
            payload["objective_five_directed_low_component_edge_count"], 29_541
        )
        self.assertEqual(payload["objective_five_frontier_induced_edge_count"], 12_728)
        self.assertEqual(payload["complete_sublevel_five_component_vertex_count"], 17_329)
        self.assertEqual(payload["complete_sublevel_five_component_edge_count"], 52_890)
        self.assertEqual(
            payload["exact_one_flip_escape_level_from_sublevel_five_component"], 6
        )
        self.assertEqual(payload["new_objective_five_rotation_orbit_count"], 0)
        self.assertEqual(
            payload["new_objective_at_most_four_rotation_orbit_histogram"],
            {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0},
        )
        self.assertEqual(
            payload["direct_recount_objective_five_representative_count"], 306
        )

        aggregate = payload[
            "aggregate_objective_five_frontier_neighbor_objective_histogram"
        ]
        self.assertEqual(sum(aggregate.values()), 13_158 * 903)
        self.assertEqual(aggregate["2"], 1_806)
        self.assertEqual(aggregate["3"], 7_826)
        self.assertEqual(aggregate["4"], 19_909)
        self.assertEqual(aggregate["5"], 2 * 12_728)
        self.assertGreater(aggregate["6"], 0)

        signatures = payload[
            "objective_five_frontier_source_incidence_signature_histogram"
        ]
        self.assertEqual(sum(signatures.values()), 13_158)
        directed_incidence = sum(
            sum(map(int, signature.split(","))) * count
            for signature, count in signatures.items()
        )
        self.assertEqual(directed_incidence, 29_541)
        self.assertEqual(4_171 + 13_158, 17_329)
        self.assertEqual(10_621 + 29_541 + 12_728, 52_890)

    def test_objective_six_frontier_certificate(self) -> None:
        payload = json.loads((HERE / "objective-six-frontier.json").read_text())
        self.assertEqual(payload["sublevel_five_source_rotation_type_count"], 403)
        self.assertEqual(
            payload["sublevel_five_all_edge_rotation_representative_neighbor_checks"],
            403 * 903,
        )
        self.assertEqual(
            payload["sublevel_five_symmetry_lifted_neighbor_checks"],
            17_329 * 903,
        )
        self.assertEqual(
            payload["objective_six_directed_rotation_representative_count"], 3_011
        )
        self.assertEqual(
            payload["objective_six_directed_sublevel_five_edge_count"],
            3_011 * 43,
        )
        self.assertEqual(payload["objective_six_frontier_rotation_orbit_count"], 1_144)
        self.assertEqual(payload["objective_six_frontier_vertex_count"], 1_144 * 43)
        self.assertTrue(payload["objective_six_frontier_has_trivial_rotation_stabilizers"])

        edge_histogram = payload["objective_six_directed_source_edge_histogram"]
        representative_histogram = payload[
            "objective_six_directed_source_rotation_representative_histogram"
        ]
        self.assertEqual(sum(edge_histogram.values()), 129_473)
        self.assertEqual(
            {source: 43 * count for source, count in representative_histogram.items()},
            edge_histogram,
        )

        signatures = payload[
            "objective_six_frontier_source_incidence_signature_histogram"
        ]
        self.assertEqual(len(signatures), 21)
        self.assertEqual(sum(signatures.values()), 49_192)
        coordinate_totals = [0, 0, 0, 0]
        for signature, count in signatures.items():
            coordinates = list(map(int, signature.split(",")))
            for index, coordinate in enumerate(coordinates):
                coordinate_totals[index] += coordinate * count
        self.assertEqual(
            coordinate_totals,
            [edge_histogram[str(source)] for source in (2, 3, 4, 5)],
        )
        self.assertEqual(sum(coordinate_totals), 129_473)
        self.assertEqual(
            payload["direct_recount_objective_six_incidence_signature_count"], 21
        )

    def test_objective_six_component_and_independent_recount(self) -> None:
        component = json.loads(
            (HERE / "objective-six-component-fast.json").read_text()
        )
        independent = json.loads(
            (HERE / "objective-six-component-independent.json").read_text()
        )
        representatives = json.loads(
            (HERE / "objective-six-component-representatives.json").read_text()
        )["objective_six_rotation_representatives"]

        self.assertEqual(
            component["objective_six_first_frontier_rotation_orbit_count"],
            1_144,
        )
        self.assertEqual(
            component["objective_six_component_rotation_orbit_count"], 1_183
        )
        self.assertEqual(
            component["additional_objective_six_rotation_orbit_count"], 39
        )
        self.assertEqual(component["objective_six_component_vertex_count"], 50_869)
        self.assertEqual(
            component["objective_six_component_induced_edge_count"], 55_126
        )
        self.assertTrue(component["complete_sublevel_six_component_is_closed"])
        self.assertEqual(
            component["complete_sublevel_six_component_vertex_count"], 68_198
        )
        self.assertEqual(
            component["complete_sublevel_six_component_edge_count"], 237_489
        )
        self.assertEqual(
            component["exact_one_flip_escape_level_from_sublevel_six_component"],
            7,
        )

        histogram = component[
            "aggregate_objective_six_component_neighbor_objective_histogram"
        ]
        self.assertEqual(sum(histogram.values()), 50_869 * 903)
        self.assertEqual(
            {objective: histogram[objective] for objective in ("2", "3", "4", "5")},
            {"2": 1_677, "3": 15_480, "4": 36_034, "5": 76_282},
        )
        self.assertEqual(histogram["6"], 2 * 55_126)
        self.assertGreater(histogram["7"], 0)
        self.assertEqual(17_329 + 50_869, 68_198)
        self.assertEqual(52_890 + 129_473 + 55_126, 237_489)

        self.assertEqual(len(representatives), 1_183)
        self.assertEqual(len({tuple(item) for item in representatives}), 1_183)
        self.assertEqual(
            independent["independent_direct_recount_representative_count"], 1_183
        )
        self.assertEqual(independent["rotation_orbit_count"], 1_183)
        self.assertEqual(independent["missing_same_layer_neighbor_count"], 0)
        self.assertEqual(
            independent["same_layer_directed_edge_count"], 2 * 55_126
        )
        self.assertEqual(
            independent["aggregate_neighbor_objective_histogram"], histogram
        )
        self.assertEqual(
            independent["lower_neighbor_histogram"],
            {"2": 1_677, "3": 15_480, "4": 36_034, "5": 76_282},
        )

    def test_defect_orbit_tube_certificate_and_union_size(self) -> None:
        payload = json.loads(
            (HERE / "defect-orbit-tube-radius5.json").read_text()
        )
        self.assertEqual(payload["path_edge_count"], 37)
        self.assertEqual(payload["center_count"], 38)
        self.assertEqual(payload["tube_radius"], 5)
        self.assertTrue(
            all(
                center["exact_minimum_through_requested_radius"] == 2
                for center in payload["centers"]
            )
        )
        self.assertEqual(
            sum(
                center["candidate_branches_considered"]
                for center in payload["centers"]
            ),
            payload["total_candidate_branches_considered"],
        )

        nearest = prefix_chain_distance_histogram(payload["path_edge_count"])
        self.assertEqual(
            {str(distance): count for distance, count in nearest.items()},
            payload["path_coordinate_nearest_prefix_distance_histogram"],
        )
        outside_coordinates = 903 - payload["path_edge_count"]
        radius = payload["tube_radius"]
        union_size = sum(
            count
            * sum(
                comb(outside_coordinates, extra)
                for extra in range(radius - distance + 1)
            )
            for distance, count in nearest.items()
            if distance <= radius
        )
        self.assertEqual(
            union_size, payload["distinct_coloring_count_in_ball_union"]
        )

        primary = json.loads(
            (HERE / "local-rigidity-radius6-primary.json").read_text()
        )
        self.assertEqual(
            payload["centers"][0]["expanded_by_depth"],
            primary["expanded_by_depth"][:6],
        )

    def test_bridge_tube_certificates_and_union_sizes(self) -> None:
        for radius in (5, 6):
            payload = json.loads(
                (HERE / f"bridge-tube-radius{radius}.json").read_text()
            )
            self.assertEqual(payload["center_count"], 16)
            self.assertEqual(payload["tube_radius"], radius)
            self.assertTrue(
                all(
                    center["exact_minimum_through_requested_radius"] == 2
                    for center in payload["centers"]
                )
            )
            self.assertEqual(
                sum(
                    center["candidate_branches_considered"]
                    for center in payload["centers"]
                ),
                payload["total_candidate_branches_considered"],
            )

            path_length = payload["bridge_edge_count"]
            nearest = Counter()
            for mask in range(1 << path_length):
                nearest[
                    min(
                        (mask ^ ((1 << prefix) - 1)).bit_count()
                        for prefix in range(path_length + 1)
                    )
                ] += 1
            self.assertEqual(
                {str(distance): count for distance, count in sorted(nearest.items())},
                payload["path_coordinate_nearest_prefix_distance_histogram"],
            )
            outside_coordinates = 903 - path_length
            union_size = sum(
                count
                * sum(
                    comb(outside_coordinates, extra)
                    for extra in range(radius - distance + 1)
                )
                for distance, count in nearest.items()
                if distance <= radius
            )
            self.assertEqual(
                union_size, payload["distinct_coloring_count_in_ball_union"]
            )
            self.assertEqual(
                sum(comb(903, distance) for distance in range(radius + 1)),
                payload["single_ball_size"],
            )

            endpoint_files = (
                "local-rigidity-radius6-fm.json",
                "local-rigidity-radius6-primary.json",
            )
            for center, endpoint_file in zip(
                (payload["centers"][0], payload["centers"][-1]), endpoint_files
            ):
                endpoint = json.loads((HERE / endpoint_file).read_text())
                self.assertEqual(
                    center["expanded_by_depth"],
                    endpoint["expanded_by_depth"][: radius + 1],
                )


if __name__ == "__main__":
    unittest.main()
