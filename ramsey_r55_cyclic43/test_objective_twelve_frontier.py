import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class ObjectiveTwelveFrontierCertificateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(
            (HERE / "objective-twelve-frontier-certificate.json").read_text()
        )

    def test_exact_lifts_and_target_decompositions(self) -> None:
        data = self.data
        self.assertEqual(
            data["objective_twelve_frontier_vertex_count"],
            43 * data["objective_twelve_frontier_rotation_orbit_count"],
        )
        self.assertEqual(
            data["frontier_labeled_incidence"],
            43 * data["frontier_quotient_incidence"],
        )
        self.assertEqual(
            data["objective_twelve_frontier_rotation_orbit_count"],
            data["lower_only_target_count"]
            + data["q11_only_target_count"]
            + data["mixed_lower_q11_target_count"],
        )
        self.assertEqual(
            data["lower_derived_target_count"],
            data["lower_only_target_count"]
            + data["mixed_lower_q11_target_count"],
        )
        self.assertEqual(
            data["q11_derived_target_count"],
            data["q11_only_target_count"]
            + data["mixed_lower_q11_target_count"],
        )
        self.assertFalse(data["all_boundary_targets_adjacent_to_q11_layer"])

    def test_incidence_and_component_partitions(self) -> None:
        data = self.data
        self.assertEqual(
            sum(data["raw_incidence_by_source_objective"].values()),
            data["frontier_quotient_incidence"],
        )
        self.assertEqual(
            sum(data["distinct_pair_count_by_source_objective"].values()),
            data["distinct_source_target_pairs"],
        )
        self.assertEqual(
            data["frontier_quotient_incidence"]
            - data["distinct_source_target_pairs"],
            data["source_target_parallel_edge_excess"],
        )
        components = data["full_boundary_bipartite_components"]["components"]
        self.assertEqual(len(components), 4)
        self.assertEqual(
            sum(component["target_vertices"] for component in components),
            data["objective_twelve_frontier_rotation_orbit_count"],
        )
        self.assertEqual(
            sum(component["edges"] for component in components),
            data["frontier_quotient_incidence"],
        )
        self.assertEqual(
            sum(component["cycle_rank"] for component in components),
            data["full_boundary_bipartite_components"]["cycle_rank"],
        )
        for component in components:
            self.assertEqual(
                component["cycle_rank"],
                component["edges"]
                - component["source_vertices"]
                - component["target_vertices"]
                + 1,
            )

    def test_independent_recount_and_scope(self) -> None:
        data = self.data
        self.assertTrue(data["all_optimized_checks_pass"])
        self.assertTrue(data["all_direct_checks_pass"])
        self.assertEqual(data["direct_unexpected_targets"], 0)
        self.assertEqual(data["direct_omitted_targets"], 0)
        self.assertEqual(data["direct_objective_errors"], 0)
        self.assertEqual(data["direct_nonfree_target_encounters"], 0)
        self.assertEqual(
            data["direct_five_set_evaluations"],
            data["total_source_rotation_orbit_count"] * 962_598,
        )
        self.assertEqual(
            data["shadow_boundary_target_count_found"],
            data["shadow_boundary_target_count_expected"],
        )
        self.assertEqual(
            sum(
                data[
                    "lower_only_target_minimum_source_objective_histogram"
                ].values()
            ),
            data["lower_only_target_count"],
        )


if __name__ == "__main__":
    unittest.main()
