#!/usr/bin/env python3
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class ShadowCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((HERE / "objective-eleven-shadow.json").read_text())

    @staticmethod
    def weighted(histogram: dict[str, int]) -> int:
        return sum(int(key) * value for key, value in histogram.items())

    def test_exact_boundary_counts(self) -> None:
        data = self.data
        self.assertEqual(data["exceptional_objective_nine_source_orbit_count"], 65)
        self.assertEqual(data["objective_eleven_shadow_target_orbit_count"], 427)
        self.assertEqual(data["objective_eleven_shadow_target_vertex_count"], 18_361)
        self.assertEqual(data["quotient_shadow_incidence_count"], 528)
        self.assertEqual(data["labeled_shadow_incidence_count"], 22_704)
        self.assertEqual(data["simple_shadow_quotient_edge_count"], 528)
        self.assertEqual(data["parallel_shadow_incidence_excess"], 0)
        self.assertTrue(data["bidirectional_shadow_incidence_totals_agree"])
        self.assertTrue(data["all_sources_have_zero_objective_ten_neighbors"])
        self.assertTrue(
            data["all_sources_have_minimum_external_objective_eleven"]
        )
        self.assertTrue(data["all_targets_are_canonical_free_objective_eleven"])

    def test_degree_histograms_reconcile(self) -> None:
        data = self.data
        source_incidence = data["source_objective_eleven_incidence_degree_histogram"]
        source_simple = data["source_distinct_target_orbit_degree_histogram"]
        target_incidence = data["target_shadow_incidence_degree_histogram"]
        target_simple = data["target_distinct_shadow_source_degree_histogram"]
        pair_multiplicity = data["source_target_orbit_pair_multiplicity_histogram"]
        self.assertEqual(sum(source_incidence.values()), 65)
        self.assertEqual(sum(source_simple.values()), 65)
        self.assertEqual(sum(target_incidence.values()), 427)
        self.assertEqual(sum(target_simple.values()), 427)
        self.assertEqual(self.weighted(source_incidence), 528)
        self.assertEqual(self.weighted(source_simple), 528)
        self.assertEqual(self.weighted(target_incidence), 528)
        self.assertEqual(self.weighted(target_simple), 528)
        self.assertEqual(sum(pair_multiplicity.values()), 528)
        self.assertEqual(self.weighted(pair_multiplicity), 528)
        primary_histogram = data["target_primary_objective_nine_incidence_histogram"]
        self.assertEqual(sum(primary_histogram.values()), 427)
        self.assertEqual(self.weighted(primary_histogram), 800)
        self.assertEqual(
            data["total_primary_objective_nine_incidence_to_shadow_targets"],
            800,
        )
        self.assertEqual(
            data["targets_with_nonshadow_primary_objective_nine_source"], 196
        )

    def test_component_and_reflection_profiles(self) -> None:
        data = self.data
        profiles = data["shadow_incidence_bipartite_component_profiles"]
        self.assertEqual(len(profiles), 8)
        self.assertEqual(sum(row["source_orbits"] for row in profiles), 65)
        self.assertEqual(sum(row["target_orbits"] for row in profiles), 427)
        self.assertEqual(sum(row["edges"] for row in profiles), 528)
        self.assertEqual(data["shadow_incidence_bipartite_cycle_rank"], 44)
        self.assertEqual(528 - 65 - 427 + len(profiles), 44)
        partners = data["component_reflection_partner_indices"]
        self.assertEqual(len(partners), len(profiles))
        for index, partner in enumerate(partners):
            self.assertEqual(partners[partner], index)
            self.assertEqual(profiles[partner], profiles[index])
        self.assertEqual(data["reflection_fixed_component_count"], 4)
        self.assertEqual(data["reflection_paired_component_pair_count"], 2)
        self.assertEqual(data["reflection_fixed_source_orbit_count"], 3)
        self.assertEqual(data["reflection_fixed_target_orbit_count"], 7)
        self.assertEqual(data["dihedral_shadow_source_orbit_count"], 34)
        self.assertEqual(data["dihedral_shadow_target_orbit_count"], 217)


if __name__ == "__main__":
    unittest.main()
