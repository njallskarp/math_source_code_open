import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class ObjectiveTwelveTopologyCertificateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(
            (HERE / "objective-twelve-topology-independent.json").read_text()
        )

    def test_independent_component_reconstruction(self) -> None:
        data = self.data
        self.assertTrue(data["all_independent_topology_checks_pass"])
        self.assertTrue(data["full_profile_match"])
        self.assertTrue(data["q11_summary_match"])
        self.assertEqual(data["full_component_count"], 4)
        self.assertEqual(data["active_source_count"], 563_783)
        self.assertEqual(data["inactive_source_count"], 408)
        self.assertEqual(
            sum(component["target_vertices"] for component in data["full_components"]),
            data["target_count"],
        )
        self.assertEqual(
            sum(component["edges"] for component in data["full_components"]),
            data["incidence_count"],
        )
        self.assertEqual(
            sum(component["cycle_rank"] for component in data["full_components"]),
            data["full_cycle_rank"],
        )

    def test_q11_subgraph_summary(self) -> None:
        data = self.data
        self.assertEqual(data["q11_active_source_count"], 372_716)
        self.assertEqual(data["q11_inactive_source_count"], 408)
        self.assertEqual(data["q11_component_count"], 33_358)
        self.assertEqual(data["q11_cycle_rank"], 759_978)
        self.assertEqual(
            data["q11_largest_component"],
            {
                "source_vertices": 9_258,
                "target_vertices": 19_399,
                "edges": 54_902,
                "cycle_rank": 26_246,
            },
        )

    def test_exceptional_stars_are_cycle_edge_perturbations(self) -> None:
        data = self.data
        stars = data["exceptional_star_components"]
        self.assertEqual(
            [
                (star["source_id"], star["source_objective"], star["target_count"])
                for star in stars
            ],
            [(8_207, 8, 15), (11_778, 8, 12)],
        )
        self.assertTrue(
            all(star["source_state_uses_only_cycle_edges"] for star in stars)
        )
        self.assertEqual(
            [star["source_cycle_edge_positions"] for star in stars],
            [
                [5, 6, 13, 14, 15, 16, 22, 23, 25, 29, 31, 32, 38, 39, 40, 41],
                [5, 6, 7, 8, 14, 15, 16, 22, 23, 24, 30, 31, 32, 38, 39, 40, 41],
            ],
        )
        self.assertEqual(data["exceptional_source_state_hamming_distance"], 7)
        self.assertEqual(
            data["exceptional_source_state_symmetric_difference"],
            [273, 308, 468, 732, 750, 812, 825],
        )

    def test_stream_hashes(self) -> None:
        data = self.data
        self.assertEqual(
            data["incidence_stream_sha256"],
            "5751813a0f55aa342f78d98fef290716272534e8e8ae32b29bcdd5dbe6416443",
        )
        self.assertEqual(
            data["source_states_sha256"],
            "9363321bea9fa4a9fa4910e17065f5a7b6990648c4d558a35245463599691d1c",
        )
        self.assertEqual(
            data["source_objectives_sha256"],
            "825ad243414175291c83631c710c3bb535d79f6b0524d9c6727bd0660a0d907c",
        )
        self.assertEqual(
            data["stream_metadata_sha256"],
            "8d69afec18d29230af5c49268cf9bc24a933952557fc32d768af031600611bbc",
        )


if __name__ == "__main__":
    unittest.main()
