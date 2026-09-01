import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parent


def load(name: str):
    with (ROOT / name).open() as handle:
        return json.load(handle)


class ObjectiveTwelveComponentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fast_expansion = load("objective-twelve-first-expansion-fast.json")
        cls.direct_expansion = load(
            "objective-twelve-first-expansion-direct.json"
        )
        cls.fast_component = load("objective-twelve-component-fast.json")
        cls.direct_component = load("objective-twelve-component-direct.json")

    def test_first_expansion_independent_agreement(self):
        fields = [
            "first_expansion_new_rotation_orbit_count",
            "new_rotation_orbit_count_by_objective",
            "directed_quotient_moves_to_primary_sublevel_eleven",
            "directed_quotient_moves_inside_first_frontier",
            "directed_quotient_moves_to_new_states",
            "directed_quotient_moves_to_new_lower_states",
            "directed_quotient_moves_to_new_objective_twelve_states",
            "directed_neighbor_objective_histogram",
            "source_minimum_neighbor_objective_histogram",
            "source_distinct_new_target_degree_histogram",
            "source_new_target_incidence_histogram",
            "target_distinct_first_frontier_source_degree_histogram",
            "target_first_frontier_incidence_histogram",
        ]
        for field in fields:
            self.assertEqual(
                self.fast_expansion[field], self.direct_expansion[field], field
            )
        self.assertTrue(self.direct_expansion["all_direct_checks_pass"])
        self.assertEqual(self.direct_expansion["omitted_expected_targets"], 0)
        self.assertEqual(self.direct_expansion["unexpected_targets"], 0)

    def test_first_expansion_representatives(self):
        representatives = self.fast_expansion[
            "new_objective_12_rotation_representatives"
        ]
        self.assertEqual(len(representatives), 229)
        encoded = [tuple(state) for state in representatives]
        self.assertEqual(len(encoded), len(set(encoded)))
        self.assertEqual(
            self.fast_expansion["directed_quotient_moves_to_new_lower_states"],
            0,
        )

    def test_closure_independent_agreement(self):
        fields = [
            "added_to_primary_quotient_incidence",
            "added_to_first_frontier_quotient_incidence",
            "directed_inside_addition_quotient_incidence",
            "directed_outside_above_twelve_from_addition",
            "added_source_minimum_neighbor_objective_histogram",
            "added_source_external_minimum_objective_histogram",
        ]
        for field in fields:
            self.assertEqual(
                self.fast_component[field], self.direct_component[field], field
            )
        self.assertEqual(
            self.fast_component[
                "additional_discoveries_after_first_expansion_by_objective"
            ],
            {"12": 9},
        )
        self.assertEqual(
            self.direct_component["discovered_after_first_expansion"], 9
        )
        self.assertTrue(self.direct_component["all_direct_checks_pass"])

    def test_complete_component_counts_and_edge_identity(self):
        component = self.fast_component
        additions = component[
            "complete_additional_objective_12_rotation_representatives"
        ]
        self.assertEqual(len(additions), 238)
        encoded = [tuple(state) for state in additions]
        self.assertEqual(len(encoded), len(set(encoded)))
        self.assertEqual(
            component["complete_objective_twelve_rotation_orbit_count"],
            1_042_125,
        )
        self.assertEqual(
            component["complete_primary_sublevel_twelve_vertex_count"],
            24_260_213 + 43 * (1_041_887 + 238),
        )
        expected_edges = 133_822_192 + 43 * (
            4_656_506 + 3_318_138 // 2 + 1_307 + 464 // 2
        )
        self.assertEqual(
            component["complete_primary_sublevel_twelve_edge_count"],
            expected_edges,
        )
        self.assertEqual(component["exact_escape_objective"], 13)


if __name__ == "__main__":
    unittest.main()
