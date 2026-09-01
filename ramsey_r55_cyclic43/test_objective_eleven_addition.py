#!/usr/bin/env python3

import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class ObjectiveElevenAdditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(
            (HERE / "objective-eleven-addition-structure.json").read_text()
        )

    def test_global_and_addition_counts(self) -> None:
        data = self.data
        self.assertEqual(
            data["complete_objective_eleven_frontier_rotation_orbit_count"],
            372_974,
        )
        self.assertEqual(
            data["complete_objective_eleven_frontier_quotient_incidence"],
            1_557_119,
        )
        self.assertTrue(data["optimized_and_independent_global_frontiers_agree"])
        self.assertEqual(
            data["objective_ten_addition_source_rotation_orbit_count"], 527
        )
        self.assertEqual(
            data["addition_touched_objective_eleven_target_rotation_orbit_count"],
            3_393,
        )
        self.assertEqual(data["addition_objective_eleven_quotient_incidence"], 4_339)
        self.assertEqual(
            data["addition_objective_eleven_labeled_incidence"], 43 * 4_339
        )
        self.assertEqual(data["addition_source_target_parallel_incidence_excess"], 0)

    def test_exclusive_target_partition(self) -> None:
        data = self.data
        exclusive = data[
            "addition_exclusive_objective_eleven_target_rotation_orbit_count"
        ]
        shared = data[
            "addition_shared_objective_eleven_target_rotation_orbit_count"
        ]
        self.assertEqual(exclusive, 2_393)
        self.assertEqual(shared, 1_000)
        self.assertEqual(exclusive + shared, 3_393)
        self.assertEqual(
            data["addition_exclusive_objective_eleven_target_vertex_count"],
            43 * exclusive,
        )
        self.assertEqual(
            data["target_preaddition_incidence_histogram"]["0"], exclusive
        )

    def test_source_and_target_incidence_histograms(self) -> None:
        data = self.data
        source_histogram = data[
            "addition_source_distinct_target_degree_histogram"
        ]
        source_incidence = data["addition_source_incidence_histogram"]
        target_histogram = data[
            "target_distinct_addition_source_degree_histogram"
        ]
        target_incidence = data["target_addition_incidence_histogram"]
        self.assertEqual(source_histogram, source_incidence)
        self.assertEqual(target_histogram, target_incidence)
        self.assertEqual(sum(source_histogram.values()), 527)
        self.assertEqual(sum(target_histogram.values()), 3_393)
        self.assertEqual(
            sum(int(degree) * count for degree, count in source_histogram.items()),
            4_339,
        )
        self.assertEqual(
            sum(int(degree) * count for degree, count in target_histogram.items()),
            4_339,
        )

    def test_component_coupling(self) -> None:
        data = self.data
        support = data["target_component_support_size_histogram"]
        self.assertEqual(support, {"1": 2_655, "2": 730, "3": 8})
        self.assertEqual(sum(support.values()), 3_393)
        self.assertEqual(
            data["targets_incident_to_multiple_addition_components"], 738
        )
        self.assertEqual(
            data["addition_component_intersection_simple_edge_count"], 29
        )
        self.assertEqual(
            data["addition_component_intersection_connected_component_count"],
            9,
        )
        profiles = data["addition_component_objective_eleven_profiles"]
        self.assertEqual(len(profiles), 21)
        self.assertEqual(sum(item["source_orbit_count"] for item in profiles), 527)
        self.assertEqual(
            sum(item["objective_eleven_quotient_incidence"] for item in profiles),
            4_339,
        )
        self.assertEqual(
            [item["source_orbit_count"] for item in profiles[:5]],
            [178, 131, 116, 50, 15],
        )

    def test_reflection_orbits(self) -> None:
        data = self.data
        self.assertEqual(
            data["reflection_fixed_touched_target_rotation_orbit_count"], 5
        )
        self.assertEqual(
            data["reflection_fixed_exclusive_target_rotation_orbit_count"], 5
        )
        self.assertEqual(data["touched_target_dihedral_orbit_count"], 1_699)
        self.assertEqual(data["exclusive_target_dihedral_orbit_count"], 1_199)
        self.assertEqual((3_393 + 5) // 2, 1_699)
        self.assertEqual((2_393 + 5) // 2, 1_199)


if __name__ == "__main__":
    unittest.main()
