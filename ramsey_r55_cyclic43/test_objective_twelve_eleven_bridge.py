#!/usr/bin/env python3

import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class ObjectiveTwelveElevenBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fast = json.loads(
            (HERE / "objective-twelve-eleven-bridge.json").read_text()
        )
        cls.direct = json.loads(
            (HERE / "objective-twelve-eleven-bridge-direct.json").read_text()
        )

    def test_complete_bridge_lies_in_first_frontier(self) -> None:
        fast = self.fast
        self.assertEqual(
            fast["objective_twelve_shadow_boundary_rotation_orbit_count"], 2_823
        )
        self.assertEqual(
            fast["objective_eleven_first_frontier_rotation_orbit_count"],
            372_974,
        )
        self.assertEqual(
            fast["distinct_objective_eleven_bridge_rotation_orbit_count"], 8_696
        )
        self.assertEqual(
            fast[
                "bridge_in_first_objective_eleven_frontier_rotation_orbit_count"
            ],
            8_696,
        )
        self.assertEqual(
            fast[
                "bridge_outside_first_objective_eleven_frontier_rotation_orbit_count"
            ],
            0,
        )
        self.assertEqual(fast["target_outside_first_frontier_bridge_degree_histogram"], {"0": 2_823})
        self.assertTrue(all(fast["bridge_in_first_frontier_flags"]))
        representatives = fast["objective_eleven_bridge_rotation_representatives"]
        self.assertEqual(len(representatives), 8_696)
        self.assertEqual(len({tuple(state) for state in representatives}), 8_696)

    def test_exact_incidence_and_component_aggregates(self) -> None:
        fast = self.fast
        self.assertEqual(
            fast["objective_twelve_to_eleven_quotient_incidence"], 11_243
        )
        self.assertEqual(
            fast["objective_twelve_to_eleven_labeled_incidence"], 483_449
        )
        self.assertEqual(fast["distinct_objective_twelve_eleven_pairs"], 11_243)
        self.assertEqual(fast["objective_twelve_eleven_parallel_edge_excess"], 0)
        self.assertEqual(
            fast["bridge_distinct_target_degree_histogram"],
            {"1": 6_149, "2": 2_547},
        )
        self.assertEqual(
            fast["first_frontier_bridge_minimum_p10_source_objective_histogram"],
            {"6": 120, "7": 1_600, "8": 6_027, "9": 941, "10": 8},
        )
        self.assertEqual(fast["bridge_bipartite_component_count"], 985)
        self.assertEqual(fast["bridge_bipartite_cycle_rank"], 709)
        profiles = fast["bridge_bipartite_component_profile_histogram"]
        self.assertEqual(sum(item["component_count"] for item in profiles), 985)
        self.assertEqual(
            sum(
                item["component_count"] * item["objective_twelve_orbits"]
                for item in profiles
            ),
            2_823,
        )
        self.assertEqual(
            sum(
                item["component_count"] * item["objective_eleven_orbits"]
                for item in profiles
            ),
            8_696,
        )
        self.assertEqual(
            sum(
                item["component_count"] * item["distinct_edges"]
                for item in profiles
            ),
            11_243,
        )
        self.assertEqual(
            sum(
                item["component_count"] * item["cycle_rank"]
                for item in profiles
            ),
            709,
        )

    def test_independent_direct_recount_agrees(self) -> None:
        direct = self.direct
        common_fields = (
            "distinct_objective_eleven_bridge_rotation_orbit_count",
            "bridge_in_first_objective_eleven_frontier_rotation_orbit_count",
            "bridge_outside_first_objective_eleven_frontier_rotation_orbit_count",
            "objective_twelve_to_eleven_quotient_incidence",
            "distinct_objective_twelve_eleven_pairs",
            "objective_twelve_eleven_parallel_edge_excess",
            "target_distinct_bridge_degree_histogram",
            "target_first_frontier_bridge_degree_histogram",
            "target_outside_first_frontier_bridge_degree_histogram",
            "bridge_distinct_target_degree_histogram",
            "first_frontier_bridge_minimum_p10_source_objective_histogram",
            "first_frontier_bridge_p10_incidence_degree_histogram",
            "bridge_bipartite_component_count",
            "bridge_bipartite_cycle_rank",
        )
        for field in common_fields:
            self.assertEqual(self.fast[field], direct[field])
        self.assertTrue(direct["direct_bridge_array_agrees_entry_for_entry"])
        self.assertTrue(direct["all_direct_checks_pass"])
        for field in (
            "target_objective_errors",
            "missing_claimed_bridge_states",
            "target_aligned_array_errors",
            "bridge_aligned_array_errors",
        ):
            self.assertEqual(direct[field], 0)


if __name__ == "__main__":
    unittest.main()
