import unittest

import verify_ratio


class SharpFacetRatioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = verify_ratio.verify_ratio()

    def test_complete_local_classification(self):
        self.assertEqual(self.results["q3_squarefree_patterns"], 2902)
        self.assertEqual(self.results["q3_positive_objective_patterns"], 48)

    def test_facet_gluing_certificate(self):
        self.assertEqual(self.results["facet_gluing_nodes"], 140515)
        self.assertEqual(self.results["facet_gluing_pruned"], 120236)
        self.assertEqual(self.results["facet_gluing_violations"], 0)

    def test_independent_edge_branch_certificate(self):
        self.assertEqual(self.results["edge_branch_nodes"], 9455)
        self.assertEqual(self.results["edge_branch_pruned"], 4340)
        self.assertEqual(self.results["edge_branch_violations"], 0)

    def test_attaining_witness(self):
        self.assertEqual(self.results["witness_mask"], "0x2313ff54")
        self.assertEqual(self.results["witness_ratio"], "3/17")

    def test_global_constant(self):
        self.assertEqual(self.results["asymptotic_constant"], "119/66")
        self.assertEqual(self.results["improvement_over_7/4"], "7/132")


if __name__ == "__main__":
    unittest.main()
