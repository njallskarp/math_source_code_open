import unittest

import verify


class NFWidthFourTests(unittest.TestCase):
    def test_all_formula_transitions_through_100(self) -> None:
        states, transitions = verify.verify_type_formula(100)
        self.assertEqual(states, transitions)
        self.assertGreater(states, 5000)

    def test_definition_level_through_7(self) -> None:
        states, facets = verify.verify_definition_level(7)
        self.assertEqual(states, sum(m + 6 for m in range(2, 8)))
        self.assertGreater(facets, 1000)

    def test_small_boundary_orbit_lengths(self) -> None:
        for m in range(2, 8):
            self.assertEqual(len(verify.predicted_orbit(m)), m + 6)

    def test_wave_and_tail_transitions(self) -> None:
        verify.verify_weight_monotonicity()
        for m in range(4, 40):
            for s in range(2, m - 2):
                self.assertEqual(
                    verify.delta_types(verify.wave_types(s, m), m),
                    verify.wave_types(s - 1, m),
                )
            self.assertEqual(
                verify.delta_types(verify.wave_types(1, m), m),
                verify.penultimate_types(m),
            )
        for m in range(3, 40):
            self.assertEqual(
                verify.delta_types(verify.penultimate_types(m), m),
                verify.tail_types(m),
            )
        for m in range(2, 40):
            self.assertEqual(
                verify.delta_types(verify.tail_types(m), m),
                verify.initial_types(m),
            )

    def test_all_noninitial_nonfirst_states_have_large_facet(self) -> None:
        verify.verify_nongraph_states(100)


if __name__ == "__main__":
    unittest.main()
