#!/usr/bin/env python3

import json
import unittest
from collections import Counter
from math import comb
from pathlib import Path

from defect_cycle import analyze_cycle, position_edge, transport_position
from defect_orbit_tube import prefix_chain_distance_histogram
from local_rigidity import complete_graph_edges, direct_count, initial_colors
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
