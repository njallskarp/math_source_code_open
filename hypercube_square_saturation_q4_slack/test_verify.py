import unittest

import verify


class CompatibilitySlackTests(unittest.TestCase):
    def test_cube_incidence_counts(self):
        self.assertEqual(len(verify.EDGES), 32)
        self.assertEqual(len(verify.SQUARES), 24)
        self.assertEqual(len(verify.FACETS), 8)
        self.assertTrue(all(len(facets) == 3 for facets in verify.EDGE_FACETS))

    def test_local_equality_classification(self):
        patterns = verify.equality_patterns(verify.FACETS[0])
        self.assertEqual(len(patterns), 49)
        statistics = [verify.local_statistics(mask, verify.FACETS[0]) for mask in patterns]
        self.assertEqual(statistics.count((0, 0, 0, 0)), 1)
        self.assertEqual(statistics.count((4, 0, 2, 0)), 48)
        self.assertEqual(sum(mask.bit_count() == 7 for mask in patterns), 48)

    def test_only_empty_pattern_glues(self):
        patterns = tuple(verify.equality_patterns(facet) for facet in verify.FACETS)
        self.assertEqual(verify.compatible_equality_patterns(patterns), {0})

    def test_facet_capacity_certificate(self):
        self.assertEqual(verify.capacity_summary(3), {0: 24, 1: 32})
        self.assertEqual(verify.capacity_summary(6), {8: 4, 12: 24})

    def test_full_verifier(self):
        results = verify.verify()
        self.assertEqual(results["asymptotic_constant"], "504/287")
        self.assertEqual(results["improvement_over_7/4"], "7/1148")


if __name__ == "__main__":
    unittest.main()
