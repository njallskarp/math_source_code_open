#!/usr/bin/env python3

import json
import unittest
from collections import Counter
from math import comb
from pathlib import Path

from local_rigidity import complete_graph_edges, direct_count, initial_colors
from solve_cyclic43 import load_certificate, verify_flips


HERE = Path(__file__).resolve().parent


class DirectVerifierTests(unittest.TestCase):
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
