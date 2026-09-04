import unittest

import verify


class NFWidthFiveTests(unittest.TestCase):
    def test_symbolic_certificate(self) -> None:
        cutoff, transitions, checks = verify.verify_symbolic_certificate()
        self.assertGreaterEqual(cutoff, 7)
        self.assertEqual(transitions, 15)
        self.assertGreater(checks, 100)

    def test_formula_transitions_through_100(self) -> None:
        states, transitions = verify.verify_type_formula(100)
        self.assertEqual(states, transitions)
        self.assertGreater(states, 5000)

    def test_definition_level_through_7(self) -> None:
        states, facets = verify.verify_definition_level(7)
        self.assertEqual(states, sum(m + 7 for m in range(2, 8)))
        self.assertGreater(facets, 1000)

    def test_boundary_orbit_lengths(self) -> None:
        for m in range(2, 16):
            self.assertEqual(len(verify.predicted_orbit(m)), m + 7)

    def test_noninitial_nonfirst_states_have_large_facet(self) -> None:
        verify.verify_nongraph_states(100)


if __name__ == "__main__":
    unittest.main()
