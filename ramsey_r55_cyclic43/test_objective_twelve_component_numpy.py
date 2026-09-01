import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


def weighted_sum(histogram: dict[str, int]) -> int:
    return sum(int(value) * count for value, count in histogram.items())


class ObjectiveTwelveComponentNumPyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(
            (HERE / "objective-twelve-component-numpy.json").read_text()
        )

    def test_complete_third_implementation_recount(self) -> None:
        data = self.data
        self.assertTrue(data["all_numpy_closure_checks_pass"])
        self.assertEqual(data["verified_seed_count"], 229)
        self.assertEqual(data["newly_reached_after_seeds"], 9)
        self.assertEqual(data["reachable_addition_count"], 238)
        self.assertEqual(data["objective_errors"], 0)
        self.assertEqual(data["canonical_errors"], 0)
        self.assertEqual(data["nonfree_errors"], 0)
        self.assertEqual(data["lower_neighbor_count"], 0)
        self.assertEqual(data["omitted_sublevel_neighbor_count"], 0)

    def test_every_move_and_escape_level(self) -> None:
        data = self.data
        objectives = data["directed_neighbor_objective_histogram"]
        self.assertEqual(sum(objectives.values()), 238 * 903)
        self.assertEqual(objectives["12"], 1_307 + 464)
        self.assertEqual(
            sum(count for value, count in objectives.items() if int(value) > 12),
            213_143,
        )
        self.assertEqual(min(map(int, objectives)), 12)
        self.assertEqual(max(map(int, objectives)), 56)
        self.assertEqual(
            data["minimum_neighbor_objective_histogram"], {"12": 238}
        )
        self.assertEqual(
            data["external_minimum_objective_histogram"], {"13": 238}
        )
        self.assertEqual(
            sum(data["q13_exit_degree_histogram"].values()), 238
        )
        self.assertEqual(
            weighted_sum(data["q13_exit_degree_histogram"]), 1_924
        )

    def test_induced_addition_multigraph(self) -> None:
        data = self.data
        profiles = data["addition_component_profiles"]
        self.assertEqual(data["addition_component_count"], 61)
        self.assertEqual(sum(profile["vertices"] for profile in profiles), 238)
        self.assertEqual(sum(profile["edges"] for profile in profiles), 232)
        self.assertEqual(
            sum(profile["cycle_rank"] for profile in profiles), 55
        )
        self.assertEqual(data["addition_total_cycle_rank"], 55)
        self.assertEqual(
            sum(profile["seed_vertices"] for profile in profiles), 229
        )
        self.assertEqual(
            sum(profile["final_shell_vertices"] for profile in profiles), 9
        )
        self.assertEqual(data["components_meeting_final_shell"], 3)
        self.assertTrue(data["final_shell_equals_zero_frontier_sources"])
        self.assertEqual(
            data["final_shell_addition_degree_histogram"], {"2": 2, "4": 7}
        )
        self.assertEqual(
            data["final_shell_q13_exit_degree_histogram"], {"3": 2, "8": 7}
        )
        self.assertEqual(
            data["distinct_undirected_pairs_inside_addition"], 230
        )
        self.assertEqual(
            data["undirected_parallel_edge_excess_inside_addition"], 2
        )
        self.assertEqual(data["self_orbit_directed_moves_inside_addition"], 0)
        self.assertEqual(data["asymmetric_inside_pair_errors"], 0)
        self.assertEqual(
            profiles[0],
            {
                "vertices": 36,
                "edges": 58,
                "cycle_rank": 23,
                "seed_vertices": 36,
                "final_shell_vertices": 0,
                "support_family": "two_16_one_5",
            },
        )

    def test_three_exact_support_families(self) -> None:
        data = self.data
        families = data["support_family_summaries"]
        self.assertEqual(data["cross_support_family_edges"], 0)
        self.assertEqual(set(families), {
            "cycle_only",
            "two_16_one_5",
            "two_17_one_21",
        })
        self.assertEqual(
            (
                families["cycle_only"]["vertices"],
                families["cycle_only"]["seed_vertices"],
                families["cycle_only"]["final_shell_vertices"],
                families["cycle_only"]["components"],
                families["cycle_only"]["edges"],
                families["cycle_only"]["cycle_rank"],
            ),
            (190, 183, 7, 56, 166, 32),
        )
        self.assertEqual(
            (
                families["two_16_one_5"]["vertices"],
                families["two_16_one_5"]["seed_vertices"],
                families["two_16_one_5"]["final_shell_vertices"],
                families["two_16_one_5"]["components"],
                families["two_16_one_5"]["edges"],
                families["two_16_one_5"]["cycle_rank"],
            ),
            (38, 38, 0, 3, 58, 23),
        )
        self.assertEqual(
            (
                families["two_17_one_21"]["vertices"],
                families["two_17_one_21"]["seed_vertices"],
                families["two_17_one_21"]["final_shell_vertices"],
                families["two_17_one_21"]["components"],
                families["two_17_one_21"]["edges"],
                families["two_17_one_21"]["cycle_rank"],
            ),
            (10, 8, 2, 2, 8, 0),
        )

    def test_sparse_frontier_interface(self) -> None:
        data = self.data
        self.assertEqual(data["frontier_target_count_streamed"], 1_041_887)
        self.assertTrue(data["frontier_strictly_sorted_and_unique"])
        self.assertEqual(data["frontier_candidate_target_count"], 1_196)
        self.assertEqual(data["missing_frontier_target_count"], 0)
        self.assertEqual(
            sum(data["frontier_target_degree_histogram"].values()), 1_196
        )
        self.assertEqual(
            weighted_sum(data["frontier_target_degree_histogram"]), 1_307
        )
        self.assertEqual(
            sum(data["source_frontier_degree_histogram"].values()), 238
        )
        self.assertEqual(
            weighted_sum(data["source_frontier_degree_histogram"]), 1_307
        )
        self.assertEqual(data["source_frontier_degree_histogram"]["0"], 9)

    def test_hash_pins(self) -> None:
        data = self.data
        self.assertEqual(
            data["frontier_targets_sha256"],
            "653d1068c456d228c12d640a50eca409fceaf570dbb6040b66bebef296b2615c",
        )
        self.assertEqual(
            data["frontier_certificate_sha256"],
            "e4390990fad91c8f9d7e584a7a4dbbc35d02d86b5971139376bee3895c51b5f1",
        )
        self.assertEqual(
            data["component_sha256"],
            "4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3",
        )


if __name__ == "__main__":
    unittest.main()
